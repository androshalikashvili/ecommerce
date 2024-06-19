from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Review, CartItem, Category, Brand
from .forms import CustomUserCreationForm, ReviewForm, CartItemForm
from django.contrib.auth import login, authenticate
from django.db.models import Avg, Q
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator

def home(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()


    category = request.GET.get('category')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    search = request.GET.get('search')

    if category:
        products = products.filter(category__name=category)
    if brand:
        products = products.filter(brand__name=brand)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_rating:
        products = products.filter(rating__gte=min_rating)
    if search:
        products = products.filter(name__icontains=search)

    paginator = Paginator(products, 3)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    def clean_query_params(params):
        query_dict = params.copy()
        if 'page' in query_dict:
            del query_dict['page']
        return query_dict.urlencode()

    context = {
        'categories': categories,
        'brands': brands,
        'products': page_obj,
        'category': category,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'search': search,
        'query_params': clean_query_params(request.GET)
    }
    return render(request, 'shop/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    avg_rating = product.reviews.aggregate(average_rating=Avg('rating'))['average_rating']
    form = ReviewForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                return redirect('product_detail', slug=product.slug)

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        for item in cart_items:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('cart')

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'shop/register.html', context)


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')



@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    return redirect('cart')

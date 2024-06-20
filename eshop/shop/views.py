from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Review, CartItem, Category, Brand
from .forms import ReviewForm
from django.db.models import Avg, Q
from django.core.paginator import Paginator
from userprofile.models import Order
from userprofile.forms import OrderForm
from django.contrib import messages

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
        try:
            min_rating = float(min_rating)
            products = products.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)
        except ValueError:
            pass
    if search:
        products = products.filter(name__icontains=search)

    paginator = Paginator(products, 3)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

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
    user = request.user
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    orders = Order.objects.filter(user=user)

    if request.method == 'POST':

        if 'create_order' in request.POST:
            o_form = OrderForm(request.POST, request.FILES)
            if o_form.is_valid():
                custom_order = o_form.save(commit=False)
                custom_order.user = user
                custom_order.save()
                messages.success(request, 'The order has been created!')
                return redirect('cart')

        elif 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id, user=user)
            o_form = OrderForm(request.POST, request.FILES, instance=order)
            if o_form.is_valid():
                o_form.save()
                messages.success(request, 'Order has been updated!')
                return redirect('cart')

        elif 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id, user=user)
            order.delete()
            messages.success(request, 'Order has been deleted!')
            return redirect('cart')

        elif 'update_cart' in request.POST:
            for item in cart_items:
                quantity = request.POST.get(f'quantity_{item.id}')
                if quantity:
                    item.quantity = int(quantity)
                    item.save()
            return redirect('cart')
        
    context = {
        'cart_items': cart_items,
        'total': total,
        'orders': orders,
        'order_form': OrderForm(),
    }
    return render(request, 'shop/cart.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('cart')
    else:
        form = OrderForm()
    return render(request, 'userprofile/create_order.html', {'form': form})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = OrderForm(instance=order)
    return render(request, 'userprofile/edit_order.html', {'form': form})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('cart')
    return render(request, 'userprofile/delete_order.html', {'order': order})


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

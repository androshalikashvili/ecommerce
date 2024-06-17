from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            custom_order = form.save(commit=False)
            custom_order.user = user
            custom_order.save()
            return redirect('profile')
    else:
        form = OrderForm()

    context = {
        'user': user,
        'orders': orders,
        'form': form,
    }
    return render(request, 'userprofile/user_profile.html', context)
    # return render(request, 'shop/cart.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('profile')
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
            return redirect('profile')
    else:
        form = OrderForm(instance=order)
    return render(request, 'userprofile/edit_order.html', {'form': form})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('profile')
    return render(request, 'userprofile/delete_order.html', {'order': order})

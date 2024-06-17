from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm

@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'userprofile/user_profile.html', {'orders': orders})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('user_profile')
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
            return redirect('user_profile')
    else:
        form = OrderForm(instance=order)
    return render(request, 'userprofile/edit_order.html', {'form': form})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('user_profile')
    return render(request, 'userprofile/delete_order.html', {'order': order})

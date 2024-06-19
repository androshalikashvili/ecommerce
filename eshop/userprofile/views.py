from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Profile
from .forms import OrderForm, UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    orders = Order.objects.filter(user=user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        elif 'create_order' in request.POST:
            u_form = UserUpdateForm(instance=user)
            p_form = ProfileUpdateForm(instance=profile)
            o_form = OrderForm(request.POST, request.FILES)
            if o_form.is_valid():
                custom_order = o_form.save(commit=False)
                custom_order.user = user
                custom_order.save()
                messages.success(request, 'The order has been created!')
                return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)
        o_form = OrderForm()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'o_form': o_form,
        'orders': orders,
    }
    return render(request, 'userprofile/user_profile.html', context)


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

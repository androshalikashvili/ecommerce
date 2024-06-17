from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['image', 'description', 'proposed_price', 'delivery_address']

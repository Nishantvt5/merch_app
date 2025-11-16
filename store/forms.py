from django import forms
from .models import CartItem

class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;'
        })
    )

    class Meta:
        model = CartItem
        fields = ['quantity']
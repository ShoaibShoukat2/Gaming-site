from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'game_id': forms.TextInput(attrs={'placeholder': 'Enter Game ID'}),
            'totalPrice': forms.NumberInput(attrs={'placeholder': 'Enter Total Price'}),
        }




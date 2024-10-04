from typing import Any
from django.shortcuts import render
from .models import *
from order.forms import OrderForm
from django.views import generic
from order.models import PromoCode

class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product_detail'
    template_name = 'product/detail.html'

    def get_queryset(self):
        return Product.objects.prefetch_related('products')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_methods'] = PaymentMethod.objects.all()
        context['order_form'] = OrderForm

        # # Assuming PromoCode is the model for promo codes
        if self.request.user.is_authenticated:
                        
            user = self.request.user
        #     # Fetch promo codes for logged-in user (you can adjust the filtering logic)
            context['promo_codes'] = PromoCode.objects.filter(user=user)
        else:
            context['promo_codes'] = PromoCode.objects.none()

        return context
    


    












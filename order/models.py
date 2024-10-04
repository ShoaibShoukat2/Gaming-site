from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from user_account.models import User
from product.models import *


''' order models '''
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accept', 'Accept'),
        ('cancle', 'Cancle'), 
        ('success', 'Success')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='User')
    game_id = models.CharField(max_length=150, verbose_name='Game ID')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productdetails", verbose_name='Product')
    product_item = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_product_item')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_method', verbose_name='Payment Method')
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="pending", null=True, blank=True, verbose_name='Order Status')
    totalPrice = models.FloatField(null=True, blank=True, verbose_name='Total Price')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    
     # New attributes with default values
    chatgpt_login_email = models.EmailField(max_length=254, null=True, blank=True, default="user@example.com", verbose_name="ChatGPT Login Email")
    chatgpt_login_password = models.CharField(max_length=128, null=True, blank=True, default="defaultpassword", verbose_name="ChatGPT Login Password")
    password_optional = models.CharField(max_length=128, null=True, blank=True, default="optionalpassword", verbose_name="Password (Optional)")
    udemy_course_url = models.URLField(null=True, blank=True, default="http://example.com", verbose_name="Udemy Course URL")
    udemy_account_email = models.EmailField(max_length=254, null=True, blank=True, default="user@udemy.com", verbose_name="Udemy Account Email")


    def __str__(self):
        return f"Order {self.id} - {self.user if self.user else 'No User'}"
    
    # def get_total_cost(self):
    #     return sum([item.get_cost() for item in self.order_items.all()])
    
    def get_total_cost(self):
        total = sum([item.get_cost() for item in self.order_items.all()])
        if self.promo_code and self.promo_code.is_valid():
            total = self.promo_code.apply_discount(total)
        return total
    



''' Promo Code model '''

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Promo Code')
    discount_percentage = models.FloatField(verbose_name='Discount Percentage')
    max_uses = models.IntegerField(default=1, verbose_name='Maximum Uses')  # Optional: How many times a code can be used
    valid_from = models.DateTimeField(verbose_name='Valid From')
    valid_to = models.DateTimeField(verbose_name='Valid To')
    active = models.BooleanField(default=True, verbose_name='Is Active')
    
    # New field: user the promo code is associated with
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='User')

    def is_valid(self):
        """Check if the promo code is currently valid."""
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def __str__(self):
        return f"{self.code} - {self.user if self.user else 'General'}"

    def apply_discount(self, total_amount):
        """Apply discount to the total order amount."""
        return total_amount * (1 - self.discount_percentage / 100)
    
    





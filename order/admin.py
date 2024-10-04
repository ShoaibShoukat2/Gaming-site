from django.contrib import admin
from .models import Order, PromoCode

''' order register in admin panel'''


class OrderAdmin(admin.ModelAdmin):
    model= Order
    list_display =['user','game_id','product','payment_method','order_status','chatgpt_login_email','udemy_course_url','udemy_account_email']    
admin.site.register(Order, OrderAdmin)




# Customize the PromoCode display in admin
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'max_uses', 'valid_from', 'valid_to', 'active', 'is_valid','user')  # Fields to display
    list_filter = ('active', 'valid_from', 'valid_to')  # Optional: Filters for the list view
    search_fields = ('code',)  # Optional: Searchable fields in the list view

# Register the model with the custom admin
admin.site.register(PromoCode, PromoCodeAdmin)



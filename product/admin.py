from django.contrib import admin
from . models import  *
from django.utils.html import format_html
from django.conf import settings

''' Slider Admin'''
class SliderAdmin(admin.ModelAdmin):
    model = Slider
    list_display = ['id', 'display_avatar']

    def display_avatar(self, obj):
        banner_image_url = obj.banner_image.url if obj.banner_image else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<center><img src="{}" width="50%" height="50%" /></center>', banner_image_url)

    display_avatar.short_description = 'Banner Image'

admin.site.register(Slider, SliderAdmin)


''' category register '''
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display =['name']
admin.site.register(Category, CategoryAdmin)


''' product item  and produt register in admin panel using tabular inline '''
class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    extra = 1  

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductItemAdmin]
    model = Product
    list_display = ['product_name', 'get_category']

    def get_category(self, obj):
        return obj.category.name if obj.category else 'N/A'
    get_category.short_description = 'Category'


admin.site.register(Product, ProductAdmin)


''' payment method '''
class PaymentMethodAdmin(admin.ModelAdmin):
    model = PaymentMethod
    list_display =['name','display_avatar']

    def display_avatar(self, obj):
        logo_url = obj.logo.url if obj.logo else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<center><img src="{}" width="50%" height="50%" /></center>', logo_url)

    display_avatar.short_description = 'Payment Method Logo'

admin.site.register(PaymentMethod, PaymentMethodAdmin)
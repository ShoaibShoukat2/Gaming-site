from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField



''' Slider'''
class Slider(models.Model):
    banner_image = models.ImageField(upload_to='BannerImage/', verbose_name='Select Banner Image')

    class Meta:
        ordering = ['id']
        





'''product category'''
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = AutoSlugField(populate_from='name', null=True, blank=True, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

'''Product model'''
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_category', verbose_name='Select Product Category')
    product_name = models.CharField(max_length=150, verbose_name='Enter Product Name')
    product_image = models.ImageField(upload_to='ProductImage/', verbose_name="Select Product Image")
    short_descriptions= RichTextField(verbose_name='Enter Short Descriptions')
    descriptions = RichTextField(verbose_name='Descriptions')
    slug = AutoSlugField(populate_from='product_name', null=True, blank=True, unique=True)
    is_trending= models.BooleanField(default=False, verbose_name='Is Trending')
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.product_name
    
    

'''product model'''
class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', verbose_name='Select Product')
    item_name = models.CharField(max_length=150, verbose_name='Enter Product Item Name')
    item_icon = models.ImageField(upload_to='ProductImage/', null=True, blank=True,verbose_name='Select Product Item Icon')
    item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Enter Product Item Price')
    slug = AutoSlugField(populate_from='item_name', null=True, blank=True, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.item_name




''' payment method '''
class PaymentMethod(models.Model):
    name= models.CharField(max_length=150, verbose_name='Enter Payment Method Name')
    logo = models.ImageField(upload_to='paymentmethod/')



    def __str__(self):
        return self.name
    
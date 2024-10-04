from django.urls import path
from . import views
from .views import *

app_name='product'

urlpatterns = [
    path('detail/<slug:slug>',ProductDetailView.as_view(), name='product_detail'),
]






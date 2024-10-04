from django.urls import path
from . import views
from .views import *

app_name='order'

urlpatterns = [
    path('place',views.order, name='place_order'),
    path('verify', views.verifyKhalti, name='verify'),

   
]














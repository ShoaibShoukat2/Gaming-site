from django.urls import path
from . import views
from .views import *

from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static 



app_name='frontend'

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('term-and-condition', views.term_and_condition, name='term_and_condition'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('contact-us', views.contact_us, name='contact_page'),
    path('about-us', views.about_us, name='about_page'),

    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user-order', views.order, name='order'),
    path('history', views.history, name='history'),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]





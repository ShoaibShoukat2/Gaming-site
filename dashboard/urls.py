from django.urls import path
from . import views
from .views import *
app_name ='dashboard'

urlpatterns = [
    path('', views.index, name='index'),

    path('banner',SliderListView.as_view(), name="banner_list"),
    path('banner/add',BannerCreateView.as_view(), name="banner_create"),
    path('banner/update/<int:id>',BannerUpdateDetailView.as_view(), name="bannar_update"),
    path('bannar/delete', views.Bannerdelete, name='delete_bannar'),

    path('change-password', views.change_password, name="change_password"),
    path('login', views.login, name='login'),
    path('logout', views.userlogout, name='userlogout'),
    path('update-profile/', views.update_profile, name='update_profile'),

    path('product/category', CategoryListView.as_view(), name='product_category'),
    path('product/category/add',CategoryCreateView.as_view(), name='product_category_create'),
    path('product/category/update/<int:id>', CategoryUpdateDetailView.as_view(), name='product_category_update'),
    path('product/category/delete', views.categorydelete, name='delete_category'),

    path('product', ProductListView.as_view(), name='product'),
    path('product/add', views.add_edit_Product, name='product_create'),
    path('product/update/<int:product_id>', views.add_edit_Product, name='product_update'),
    path('product/delete',views.productdelete, name='delete_product'),

    path('payment-method',PaymentListView.as_view(), name="payment_list"),
    path('payment-method/add',PaymentCreateView.as_view(), name="payment_create"),
    path('payment-method/update/<int:id>',PaymentUpdateDetailView.as_view(), name="payment_update"),
    path('payment-method/delete', views.Paymentdelete, name='delete_payment'),

    path('order/<int:id>/',OrderDetailView.as_view(), name='edit_Order'),
    path('order/', OrderListView.as_view(), name='Order'),
    path('order-delete/<int:id>/', OrderDeleteView.as_view(), name='deleteorder'),

    path('customer/', CustomerListView.as_view(), name='customer'),
    path('customer/delete', CustomerDeleteView.as_view(), name='delete_customer'),

    path('add/terms-and-condition',views.TermsAndConditions, name='add_TermsAndCondition'),
    path('terms-and-condition/', TermsAndConditionListView.as_view(), name='terms'),

    path('add/company-detail',views.organizationSettings, name='add_OrganizationSetting'),

    path('add/help-center',views.HelpCenters, name='add_HelpCenter'),
    path('help-center/', HelpCenterListView.as_view(), name='helpCenter'),
    ]







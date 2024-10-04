from django.urls import path
from . import views
from .views import PasswordResetRequestView, PasswordResetConfirmView

app_name ='user_account'




urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.userlogout, name="logout"),
    path('register', views.register, name='register'),
    path('login-email', views.user_login, name='login-email'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),    
        
    
    # path('profile', views.userprofile, name ="profile"),
    # path('change/password', views.change_password_view, name='change_password'),
    # path('my-account/', views.my_account, name='my_account'),
    path('user-profile', views.userprofile, name='profile'),
    path('profile/update/', views.update_user_profile, name='update_user_profile'),
    path('profile/avatar/update/', views.update_avatar, name='update_avatar'),
    path('update-password/', views.update_password, name='update_password'),
    
    
    
    # Password reset urls
    

    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    
]


















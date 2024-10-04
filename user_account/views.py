from django.shortcuts import render, redirect
from .forms import *
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import auth
from django.contrib import messages
from .decorators import login_required
from django.conf import settings
from order.models import  *
import logging
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
import random
import requests
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView



from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from user_account.models import User




logger = logging.getLogger(__name__)



def login(request):
    # Redirect if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('frontend:index')

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            print("Attempting to log in with email:", email)
            print("Password:",password)


            # Authenticate the user by email and password
            user = authenticate(request, email=email, password=password)






            if user is not None:
                print("Authentication successful. Logging in user:", user)
                auth_login(request, user)  # Use Django's login function
                messages.success(request, "Login successful!")
                return redirect('frontend:index')
            else:
                print("Authentication failed.")
                messages.warning(request, "Invalid email or password.")

        else:
            messages.warning(request, "Invalid form data. Please try again.")

    login_form = UserLoginForm()  # Create an empty form for GET request
    return render(request, "account/login.html", {'user_login_form': login_form})







def register(request):
    user_register_form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)

        # Print posted data for debugging
        print("Form POST data:", request.POST)

        if form.is_valid():
            print("Form is valid.")

            # Store user data in session but don't save to the database yet
            request.session['user_data'] = {
                'username': form.cleaned_data.get('username'),
                'email': form.cleaned_data.get('email'),
                'phone_no': form.cleaned_data.get('phone_no'),
                'password': form.cleaned_data.get('password1'), 
            }
            



            # Generate OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp

            # Send OTP via Sparrow SMS
            try:
                phone_number = form.cleaned_data['phone_no']  # Assuming phone_no is in the form
                print(f"Attempting to send OTP {otp} to {phone_number}")

                # Function to send OTP (replace this with actual Sparrow SMS API call)
                send_otp_via_sparrow_sms(phone_number, otp)

                # Confirm OTP sent for debugging
                print(f"OTP {otp} sent to {phone_number}")

                # Redirect to OTP verification page
                return redirect('user_account:verify_otp')
            
            


            

            except Exception as e:
                # Print the exception details
                print(f"Failed to send OTP: {e}")
                messages.error(request, 'Error occurred while sending OTP. Please try again.')

        else:
            # If form is not valid, print errors for debugging
            print("Form is not valid. Errors:", form.errors)

            error_messages = [str(error) for error in form.errors.values()]
            for message in error_messages:
                print(f"Validation error: {message}")
                messages.warning(request, message)

    return render(request, 'account/register.html', {'user_register_form': user_register_form})












def send_otp_via_sparrow_sms(phone_number, otp):
    """Send OTP using Sparrow SMS API"""
    url = "https://api.sparrowsms.com/v2/sms/"
    payload = {
        'token': settings.SPARROW_SMS_TOKEN,    # Your Sparrow SMS token
        'from': settings.SPARROW_SMS_SENDER_ID, # Your approved Sender ID
        'to': phone_number,
        'text': f'Your OTP code is {otp}. Please use it to verify your account.'
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code != 200:
        raise Exception(f"Sparrow SMS API returned an error: {response.text}")
    
 


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == str(stored_otp):
            # OTP is valid, now save the user to the database
            user_data = request.session.get('user_data')

            if user_data:
                # Create a new user instance
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                user.is_user = True
                user.save()

                # Clear session data
                request.session.pop('user_data')
                request.session.pop('otp')

                # Redirect to success page or login page
                messages.success(request, "Your account has been successfully created!")
                return redirect('user_account:login')



        else:
            # Invalid OTP
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('user_account:verify_otp')

    return render(request, 'account/verify_otp.html')







def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Debugging: Check what values are being passed
        print(f'Login attempt with email: {email}, password: {password}')
        
        # Authenticate using email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            print(f'User {email} logged in successfully.')
            return redirect('frontend:index')
        else:
            print(f'Invalid login attempt for email: {email}')
    
    return redirect('user_account:login')





@login_required
def userlogout(request):
    auth.logout(request)
    messages.info(request,"logout successfully..")
    return redirect('frontend:index')


@login_required
def userprofile(request):
    
    
    user = request.user  # Fetch the logged-in user
    
    # Create a form instance with the current user's data
    form = UserRegisterForm(instance=user)
    
    avatar_url = request.user.avatar.url if request.user.avatar else None
        
        
    context = {
        'form': form,
        'avatar_url': avatar_url,
    }

    
    return render(request, 'account/profile.html', context)





@login_required
def update_user_profile(request):
    user = request.user
    

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_account:profile')
        else:
            print(form.errors)  
    else:
        form = UserRegisterForm(instance=user)
        

    context = {'form': form}
    return render(request, 'account/profile.html', context)







@login_required
def update_avatar(request):
    if request.method == 'POST':
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user)

        # Check if a file has been uploaded
        if 'avatar' in request.FILES:
            uploaded_file = request.FILES['avatar']
            print("Avatar uploaded:", uploaded_file.name)

            # Check if the user already has an avatar
            if not request.user.avatar:
                print("No existing avatar. A new one will be created.")
            else:
                print("Existing avatar found. It will be updated.")

        else:
            print("No avatar uploaded.")

        # Validate and save the form
        if form.is_valid():
            form.save()  # This will either update or create the avatar
            return redirect('user_account:profile')
    else:
        form = AvatarUpdateForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'account/update_avatar.html', context)



@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST, user=request.user)
        
        if form.is_valid():
            try:
                form.save()
                
                # Ensure the user stays logged in after the password change
                update_session_auth_hash(request, request.user)
                
                messages.success(request, 'Your password has been updated successfully.')
                return redirect('user_account:profile')
            
            except Exception as e:
                logger.error(f"Error updating password for user {request.user.username}: {e}")
                messages.error(request, 'An error occurred while updating your password. Please try again later.')
                
                
        else:
            # Capture specific form errors
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"Error with {field}: {error}")
                    
            messages.error(request, 'Please correct the errors below password try again.')
            
            return redirect('user_account:profile')


    else:
        form = PasswordUpdateForm(user=request.user)

    return render(request, 'account/profile.html', {'form': form})





import traceback



class PasswordResetRequestView(View):
    def get(self, request):
            print("GET request received for password reset.")
            try:
                return render(request, 'account/Passworrd_Reset_Request.html')
            except Exception as e:
                print(f"Error rendering template: {e}")







    def post(self, request):
        email = request.POST.get('email')
        print(f"POST request received. Email: {email}")

        # Retrieve the user based on the email
        user = User.objects.filter(email=email).first()

        if user:
            print("User found. Generating password reset token.")
            
            try:
                # Generate the password reset token and UID
                token = default_token_generator.make_token(user)
                print(f"Token generated: {token}")
                
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print(f"UID generated: {uid}")
                
                # Get the domain of the current site (localhost)
                domain = get_current_site(request).domain
                print(f"Domain retrieved: {domain}")
                
                
                # Construct the reset link
                link = reverse('user_account:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_url = f'http://{domain}{link}'
                print(f"Reset URL generated: {reset_url}")

                # Prepare the email subject and message
                subject = 'Password Reset Request'
                message = f"Hello {user.name},\n\nYou requested a password reset. Please click the link below to reset your password:\n\n{reset_url}\n\nIf you did not request a password reset, please ignore this email."
        


                # For testing on localhost, print the email details
                print(f"Sending email to: {email}")
                print(f"Email Subject: {subject}")
                print(f"Email Message: {message}")
                
                # Send email (console backend for localhost)
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                print("Email sent successfully.")
                messages.success(request, 'We have sent you an email to reset your password.')
            
            except Exception as e:
                print(f"An error occurred: {e}")
                messages.error(request, 'There was an error processing your request. Please try again.')

        else:
            print("No account found with this email.")
            messages.error(request, 'No account found with this email.')


        return redirect('user_account:password_reset_request')
        
        






class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'Password_Reset_Confirm.html', {'valid_link': True, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'This link is invalid.')
            return redirect('user_account:password_reset_request')

    def post(self, request, uidb64, token):
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            try:
                uid = force_bytes(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('user_account:login')
            else:
                messages.error(request, 'This link is invalid.')
                return redirect('password_reset_request')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('user_account:Password_Reset_Confirm', uidb64=uidb64, token=token)























# def delete_account(request):
#     user = request.user
#     user.delete()
#     messages.success(request,"Account Deleted Successfully !")
#     return redirect('frontend:profile')


# @login_required
# def change_password_view(request):
#     if request.method == 'POST':
#         old_password = request.POST.get('old_password')
#         new_password = request.POST.get('new_password')
#         confirm = request.POST.get('new_password2')

#         if new_password != confirm:
#             messages.warning(request,"New password and confirm password not match.")
        
#             if request.user.change_password(old_password, new_password):
#                 messages.success(request, 'Password changed successfully.')
            
#             return redirect('account:profile')

#         else:
#             messages.error(request, 'Invalid old password. Please try again.')

#         return redirect('account:profile')  
#     else:
#         return redirect('account:profile')  


# @login_required
# def my_account(request):
#     user = request.user
#     orders = Order.objects.filter(user= user).prefetch_related('order_items')
#     print(orders)
#     return render(request,'account/my_account.html',{'orders':orders})



# def profile(request):
#     return render(request,'account/profile.html')









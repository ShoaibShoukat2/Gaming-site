from . models import User
from django import forms
from django.contrib.auth.hashers import make_password, check_password
import re
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth import authenticate

''' user login form '''
class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())





class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password =forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model  = User
        fields = ['name', 'email', 'phone_no', 'address', 'avatar', 'password', 'confirm_password']

    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'
            field.required = True


    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_No = cleaned_data.get('phone_no')

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match!")
        
        if len(password) < 8:
            raise forms.ValidationError("Password contain at least 8 character long.")
       
        if not re.match(r'^[0-9]{10}$', phone_No):
            raise forms.ValidationError("Enter a valid phone number.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Use set_password method of the User model
        
        if commit:
            user.save()

        return user
  

    
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_no', 'address']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'
            field.required = True
            
    


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super(AvatarUpdateForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        
        




class PasswordUpdateForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password', 'class': 'form-control'}),
        label='Current Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control'}),
        label='Confirm New Password'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if self.user and not check_password(current_password, self.user.password):
            raise forms.ValidationError("Current password is incorrect.")

        if new_password1 != new_password2:
            raise forms.ValidationError("New passwords don't match!")

        if len(new_password1) < 8:
            raise forms.ValidationError("New password must be at least 8 characters long.")

        return cleaned_data


    def save(self):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
        
        










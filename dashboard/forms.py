from django import forms
from django.contrib.auth import get_user_model
from product.models import *
from order.models import *
from user_account.models import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from ckeditor.widgets import CKEditorWidget


''' Slider form '''
class SliderForm(forms.ModelForm):
    class Meta:
        model  = Slider
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(SliderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

'''User Form'''
class UserBasicForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2','phone_no', 'avatar', 'is_user', 'is_admin')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone_no', 'avatar')

'''Category form'''
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

'''Product form'''
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'short_descriptions', 'product_image', 'product_name', 'descriptions', 'is_trending']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = '__all__'



'''Payment Method Form'''
class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model  = PaymentMethod
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'


'''form for changing order status'''
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']

''''form for adding terms and condition'''
class TermsAndConditionForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = '__all__'

''''form for adding organization detail'''
class OrganizationSettingForm(forms.ModelForm):
    help_center = forms.CharField(widget=CKEditorWidget(attrs={'class': 'full-width-ckeditor'}))
    class Meta:
        model = OrganizationSetting
        fields = '__all__'

''''form for adding Help center detail'''
class HelpCenterForm(forms.ModelForm):
    terms = forms.CharField(widget=CKEditorWidget(attrs={'class': 'full-width-ckeditor'}))
    class Meta:
        model = HelpCenter
        fields = '__all__'







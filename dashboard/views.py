
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from product.models import *
from order.models import *
from user_account.models import *
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from . forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.generic.base import View
from .decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login


'''Index Section'''
@login_required
def index(request):
    return render(request,'dashboard/base_index/index.html')



'''slider section'''
# This view shows the list of slider image
class SliderListView(generic.ListView):
    model = Slider
    template_name ='dashboard/slider/slider.html'
    context_object_name ='sliders'


# This view is used to create new slider image using generics create view
class BannerCreateView(generic.CreateView):
    model = Slider
    template_name ='dashboard/slider/create_slider.html'
    form_class = SliderForm
    def get_success_url(self) -> str:
        messages.success(self.request,"New Bannar  added successfully !")
        return reverse_lazy("dashboard:banner_list")
    
# This view is used to update individual slider based on their id
class BannerUpdateDetailView(generic.UpdateView):
    model = Slider
    template_name ='dashboard/slider/create_slider.html'
    context_object_name ='slider'
    pk_url_kwarg ='id'
    form_class = SliderForm
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse_lazy('dashboard:bannar_update', kwargs={'id': self.object.id})

# This view is used to delete individual slider
def Bannerdelete(request):
    if request.method == "POST":
        id = request.POST.get('bannar_id')
        instance = get_object_or_404(Slider, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:banner_list')
    else:
        return redirect('dashboard:banner_list')


'''Login Section'''
def login(request):
    try:
        if request.user.is_authenticated: #This line checks if the user is already authenticated/logged in. If so, it redirects the user to the dashboard index page.
            return redirect('dashboard:index')
        if request.method == "POST":
            email = request.POST['useremail'] #extract the email submitted via the login form
            password = request.POST['password'] #extract the password submitted via the login form
            user_obj = authenticate(email=email, password=password) #This line attempts to authenticate the user using the provided email and password. The authenticate function is part of Django's authentication system.
            if not user_obj: #This line checks if the authentication failed 
                messages.warning(request, "Invalid username and password...")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # Check the user's role and redirect accordingly
            if user_obj.is_admin:  # If authentication succeeds and the user is an admin, it logs in the user using auth.login
                auth.login(request, user_obj)
                messages.success(request, "Admin login successful!")
                return redirect('dashboard:index')
            
            else:
                messages.warning(request, 'Invalid Password')
            return redirect('dashboard:index')
        return render(request, 'dashboard/login/login.html')
    except Exception as e: #This block catches any exceptions that might occur during the execution of the code.
        messages.warning(request, 'Something went wrong...')
        return render(request, 'dashboard/login/login.html')


'''Update Profile section'''
@login_required
def update_profile(request):
    user = request.user
    
    if not user.is_admin:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard:update_profile')
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = UserForm(instance=user)

    return render(request, 'dashboard/updateProfile/updateProfile.html', {'form': form})


'''Change password'''
@login_required
def change_password(request):
    if request.method == 'POST': #This line checks if the request method is POST, which typically indicates that a form has been submitted.
        form = PasswordChangeForm(request.user, request.POST) # PasswordChangeForm is used for changing passwords in Django.
        if form.is_valid(): #This line checks if the submitted form data is valid according to the rules defined in the PasswordChangeForm
            user = form.save() #If the form is valid, this line saves the changes to the user's password.
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:login') 
        else:
            messages.error(request,form.errors) 
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/changePassword/change_password.html', {'form': form})


'''Logout Section'''
@login_required
def userlogout(request):
    auth.logout(request) #This line logs out the user associated with the current request. The logout() function is provided by Django's authentication framework (django.contrib.auth), which handles user authentication and related tasks.
    messages.info(request,"logout successfully..")
    return redirect('dashboard:login')


'''Category Section'''
class CategoryListView(generic.ListView):
    model = Category
    template_name ='dashboard/category/category.html'
    context_object_name ='categories'
    
class CategoryCreateView(generic.CreateView):
    model = Category
    template_name ='dashboard/category/create_category.html'
    form_class = CategoryForm
    def get_success_url(self) -> str:
        messages.success(self.request,"New Category added successfully !")
        return reverse_lazy("dashboard:product_category")
    
class CategoryUpdateDetailView(generic.UpdateView):
    model = Category
    template_name ='dashboard/category/create_category.html'
    pk_url_kwarg ='id'
    form_class = CategoryForm
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse_lazy('dashboard:product_category_update', kwargs={'id': self.object.id})

def categorydelete(request):
    if request.method == "POST":
        id = request.POST.get('category_id')
        instance = get_object_or_404(Category, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:product_category')
    else:
        return redirect('dashboard:product_category')


'''Product section'''
class ProductListView(generic.ListView):
    model = Product
    context_object_name ='products'
    template_name ='dashboard/product/product.html'

def add_edit_Product(request, product_id=None):
    if product_id:
        product_instance = get_object_or_404(Product, id=product_id)
    else:
        product_instance = Product()

    ProductItemFormSet = inlineformset_factory(Product, ProductItem, form=ProductItemForm, extra=1)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product_instance)
        formset = ProductItemFormSet(request.POST, request.FILES, instance=product_instance)

        if product_form.is_valid() and formset.is_valid():
            product_instance = product_form.save()
            formset.instance = product_instance
            formset.save()
            if product_id:
                messages.success(request, 'Product updated successfully.')
                return redirect('dashboard:product_update', product_id=product_instance.id)
            else:
                messages.success(request, 'Product added successfully.')
                return redirect('dashboard:product_create')
    else:
        product_form = ProductForm(instance=product_instance)
        formset = ProductItemFormSet(instance=product_instance)

    context = {
        'product_form': product_form,
        'formset': formset,
        'instance': product_instance,
        'is_inline_formset_used': True,
    }

    return render(request, 'dashboard/product/product_create.html', context)



def productdelete(request):
    if request.method == "POST":
        id = request.POST.get('product_id')
        instance = get_object_or_404(Product, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:product')
    else:
        return redirect('dashboard:product')





'''Payment Method section'''
# This view shows the list of PaymentMethod
class PaymentListView(generic.ListView):
    model = PaymentMethod
    template_name ='dashboard/paymentMethod/payment.html'
    context_object_name ='payments'


# This view is used to create new PaymentMethod using generics create view
class PaymentCreateView(generic.CreateView):
    model = PaymentMethod
    template_name ='dashboard/paymentMethod/create_payment.html'
    form_class = PaymentMethodForm
    def get_success_url(self) -> str:
        messages.success(self.request,"New Payment method  added successfully !")
        return reverse_lazy("dashboard:payment_list")
    
# This view is used to update individual PaymentMethod based on their id
class PaymentUpdateDetailView(generic.UpdateView):
    model = PaymentMethod
    template_name ='dashboard/paymentMethod/create_payment.html'
    context_object_name ='payments'
    pk_url_kwarg ='id'
    form_class = PaymentMethodForm
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse_lazy('dashboard:payment_update', kwargs={'id': self.object.id})

# This view is used to delete individual payment
def Paymentdelete(request):
    if request.method == "POST":
        id = request.POST.get('payment_id')
        instance = get_object_or_404(PaymentMethod, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:payment_list')
    else:
        return redirect('dashboard:payment_list')





'''Order Section'''
class OrderListView(View):
    template_name = 'dashboard/order/order.html'

    def get(self, request):
        orders = Order.objects.all().select_related('user', 'product','product_item' )
        context = {
            'orders': orders,
            'pending_status': 'pending'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        order_id = request.POST.get('order_id')
        instance = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('order_status')
        
        if instance.order_status != 'pending' and new_status == 'pending':
            messages.error(request, 'Order status cannot be changed back to pending.')
        else:
            form = OrderStatusForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Order status updated successfully.')
            else:
                messages.error(request, 'Please correct the errors below.')
        return redirect('dashboard:Order')


class OrderDetailView(View):
    template_name = 'dashboard/order/edit_order.html'

    def get(self, request, id=None):
        order = get_object_or_404(Order, id=id)
        product_items = ProductItem.objects.filter(product=order.product)  # Fetch related ProductItems
        form = OrderStatusForm(instance=order)
        return render(request, self.template_name, {'form': form, 'order': order, 'product_items': product_items})

class OrderDeleteView(View):
    template_name = 'dashboard/order/order.html'
    
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        return render(request, self.template_name, {'order': order})
    
    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('dashboard:Order')



'''User section'''

User = get_user_model()

class CustomerListView(generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = 'dashboard/user/customer.html'

class CustomerDeleteView(generic.DeleteView):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('dashboard:customer')



'''Terms and Condition section'''
def TermsAndConditions(request):
    instance = None
    try:
        if id:
            instance = TermsAndCondition.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the privacy and policy.')
        return redirect('dashboard:add_TermsAndCondition')
    if request.method == 'POST':
        form = TermsAndConditionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'TermsAndCondition edited successfully.')
                return redirect('dashboard:add_TermsAndCondition')  # Redirect to the edited TermsAndCondition's details page
            else:  # Add operation
                messages.success(request, 'TermsAndCondition added successfully.')
                return redirect('dashboard:add_TermsAndCondition')  # Redirect to the page for adding new TermsAndCondition
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = TermsAndConditionForm(instance=instance)
    context = {'form': form, 'instance': instance}
    return render(request, 'dashboard/organization/terms_create.html', context)


class TermsAndConditionListView(generic.ListView):
    model = TermsAndCondition
    context_object_name = 'terms'
    template_name = 'dashboard/organization/terms.html'


'''Organization detail section'''
def organizationSettings(request):
    instance = None
    try:
        if id:
            instance = OrganizationSetting.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the terms and condition.')
        return redirect('dashboard:add_OrganizationSetting')
    if request.method == 'POST':
        form = OrganizationSettingForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'OrganizationSetting edited successfully.')
                return redirect('dashboard:add_OrganizationSetting')  # Redirect to the edited OrganizationSetting's details page
            else:  # Add operation
                messages.success(request, 'OrganizationSetting added successfully.')
                return redirect('dashboard:add_OrganizationSetting')  # Redirect to the page for adding new OrganizationSetting
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = OrganizationSettingForm(instance=instance)
    context = {'form': form, 'instance': instance}
    return render(request, 'dashboard/organization/organizationDetail_create.html', context)





'''Helpcenter section'''

def HelpCenters(request):
    instance = None
    try:
        if id:
            instance = HelpCenter.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Help center.')
        return redirect('dashboard:add_HelpCenter')
    if request.method == 'POST':
        form = HelpCenterForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'HelpCenter edited successfully.')
                return redirect('dashboard:add_HelpCenter')  # Redirect to the edited HelpCenter's details page
            else:  # Add operation
                messages.success(request, 'HelpCenter added successfully.')
                return redirect('dashboard:add_HelpCenter')
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = HelpCenterForm(instance=instance)
    context = {'form': form, 'instance': instance}
    return render(request, 'dashboard/organization/helpCenter_create.html', context)


class HelpCenterListView(generic.ListView):
    model = HelpCenter
    context_object_name = 'help'
    template_name = 'dashboard/organization/helpCenter.html'
    
    
    

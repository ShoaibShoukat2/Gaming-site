from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from product.models import *
from dashboard.models import *
from django.views import generic
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    model = Slider
    template_name = 'frontend/index.html'
    context_object_name = 'sliders'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category'] = Category.objects.all()
        context['trending_products'] = Product.objects.filter(is_trending= True)
        context['latest_product'] = Product.objects.all().order_by('-id')[:5]
        return context
    




def term_and_condition(request):
    term_and_condition_instance = TermsAndCondition.objects.first()
    return render(request,'frontend/terms_and_condition.html',{'term_and_condition_instance':term_and_condition_instance})


def privacy_policy(request):
    return render(request,'frontend/privacy-policy.html')


def login(request):
    return render(request,'frontend/login.html')




@login_required
def dashboard(request):
    
    user = request.user


    

    return render(request,'frontend/user_dashboard.html',{'user': user})





def order(request):
    return render(request,'frontend/order.html')


def history(request):
    return render(request,'frontend/history.html')



#404 error handling
def custom_404_view(request, exception):
    return render(request, 'frontend/404.html')



def contact_us(request):
    
    
    
    
    return render(request,'frontend/contactus.html')


def about_us(request):
    
    return render(request,'frontend/aboutus.html')




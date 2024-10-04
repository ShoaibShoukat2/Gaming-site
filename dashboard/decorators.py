from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_fun):
    def wrapper_fun(request, *arg, **kwargs):
        if request.user.is_authenticated:
            return view_fun(request, *arg, **kwargs)
        else:
            messages.warning(request, "Login required...")
            return redirect('dashboard:login')
    return wrapper_fun

import re
from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth import login,logout,authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'main/home.html')


def sign_up(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phoneno=request.POST.get('phone')
        state=request.POST.get('states')
        district=request.POST.get('districts')
        print(name," ",email," ",password," ",phoneno," ",state," ",district)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = User.objects.create_user(name=name,email=email,password=password,phone_no=phoneno,state=state,district=district)
            login(request,user)
            return redirect('/home')
        return HttpResponse("User already exists!!")

    else:
        pass
    return render(request, 'registration/signup.html')


def log_in(request):
    if request.method == 'POST':
        print("joelannanjoelannanjoelannanjoelannan")
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # print("Helllooooooo")
            return redirect('home')
        else:
            pass
    # else:
    #     return HttpResponse("Wrong credds bud!")
    return render(request, 'registration/login.html')



#ADDED PRODUCT PAGE JUST FOR PRESENTATION
def product(request):
    return render(request, 'main/product.html')
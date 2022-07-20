
import re
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import datetime

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'main/home.html',{'products':products})

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
            #BY DEFAULT USER IS BORROWER = 0, LENDER AANENGI 1
            user = User.objects.create_user(name=name,email=email,password=password,phoneno=phoneno,state=state,district=district)
            login(request,user)
            return redirect('/home')
        return HttpResponse("User already exists!!")

    else:
        pass
    return render(request, 'registration/signup.html')


def log_in(request):
    if request.method == 'POST':
        next_url = request.POST.get('next')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # print("Helllooooooo")
            #USED TO REDIRECT TO A SPECIFIC URL AFTER LOGIN
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            pass
    # else:
    #     return HttpResponse("Wrong credds bud!")
    return render(request, 'registration/login.html')

@login_required(login_url='/login')
def product(request, idn):
    product = Product.objects.get(id=idn)
    userid = int(request.user.id)
    try:
        reqs = PReq.objects.filter(borrower = request.user,  product = product)
        req = reqs.latest('created_at')
        status = int(req.status)
    except ObjectDoesNotExist:
        status = 1
    # img1 = product.p_image1
    # img2 = product.p_image2
    # img3 = product.p_image3
    # image = [img1,img2,img3]
    #image = ProdImage.objects.filter(product=product)
    #user = request.user
    #DYNAMICALLY LOAD PRODUCT INFO
    return render(request, 'main/product.html',{'product':product,'userid':userid, 'status':status})

@login_required(login_url='/login')
def lend(request):
    if request.method == 'POST':
        prod=Product()
        prod.p_name=request.POST.get('name')
        prod.p_rate=request.POST.get('rate')
        prod.p_desc=request.POST.get('desc')
        p_date=request.POST.get('date')
        mon = int(p_date[0:2])
        yr = int(p_date[3:7])
        prod.date = datetime.date(yr, mon, 1)
        prod.user = request.user
        if len(request.FILES) != 0:
            prod.p_image1=request.FILES['file1']
            if len(request.FILES) == 2:
                prod.p_image2=request.FILES['file2']
            if len(request.FILES) == 3:
                prod.p_image2=request.FILES['file2']
                prod.p_image3=request.FILES['file3']
        prod.save()
        return redirect('home')
    else:
        pass
    return render(request, 'main/lend.html')

@login_required(login_url='/login')
def activity(request):
    reqs=[]
    requests = PReq.objects.all()
    present_user = request.user
    my_products = Product.objects.filter(user = present_user)
    for pro in my_products:
        for req in requests:
            if req.product == pro:
                reqs.append(req)
    #print(reqs)
    return render(request, 'main/activity.html',{'requests':reqs})

@login_required(login_url='/login')
def borrow(request, idn):
    req = PReq()
    req.borrower = request.user
    req.product = Product.objects.get(id=idn)
    req.save()
    return redirect('home')

@login_required(login_url='/login')
def accept(request, idn):
    req = PReq.objects.get(id=idn)
    req.status = 1
    idn = req.product.id
    product = Product.objects.get(id=idn)
    product.status = 1
    req.save()
    product.save()
    return redirect('activity')

@login_required(login_url='/login')
def decline(request, idn):
    req = PReq.objects.get(id=idn)
    req.status = 2
    idno = req.product.id
    product = Product.objects.get(id=idno)
    product.status = 0
    req.save()
    product.save()
    return redirect('activity')

@login_required(login_url='/login')
def filterit(request):
    products = Product.objects.all().order_by('p_rate','rating')
    return render(request, 'main/home.html',{'products':products})

@login_required(login_url='/login')
def prodreceived(request, idn):
    req = PReq.objects.get(id=idn)
    req.status = 3
    #req.product.status = 0
    prodid = req.product.id
    product = Product.objects.get(id=prodid)
    product.status = 0
    req.save()
    product.save()
    return redirect('activity')

@login_required(login_url='/login')
def reportuser(request, idn):
    return render(request, 'main/reportuser.html')

@login_required(login_url='/login')
def reportcomment(request):
    return render(request, 'main/reportcomment.html')

@login_required(login_url='/login')
def reportsuccess(request):
    return render(request, 'main/reportsuccess.html')

@login_required(login_url='/login')
def wishlist(request):
    return render(request, 'main/wishlist.html')

#profile view
@login_required(login_url='/login')
def profile(request):
    return render(request, 'main/profile.html')


#profile edit
@login_required(login_url='/login')
def profileedit(request):
    return render(request, 'main/profileedit.html')
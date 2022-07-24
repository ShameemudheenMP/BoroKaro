
from math import fabs
import re
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
import datetime
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django. db. models import Q

# Create your views here.

#sort by date function
def myFunc(e):
    return e.created_at

def home(request):
    products = Product.objects.all()
    try:
        prodids = list(Wishlist.objects.filter(user=request.user).values_list('product', flat=True).order_by('id'))
        return render(request, 'main/home.html',{'products':products,'prodids':prodids})
    except:
        return render(request, 'main/home.html',{'products':products})

def sign_up(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phoneno=request.POST.get('phoneno')
        state=request.POST.get('states')
        district=request.POST.get('districts')
        #print(name," ",email," ",password," ",phoneno," ",state," ",district)
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
    comments = Comment.objects.filter(product = product).order_by('-created_at')
    wishreq = Wishlist.objects.filter(user=request.user, product = product)
    com = 0
    wish = 0
    if comments:
        com = 1
    if wishreq:
        wish = 1
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
    return render(request, 'main/product.html',{'product':product,'userid':userid, 'status':status,'comments':comments,'com':com,'wish':wish})

@login_required(login_url='/login')
def lend(request):
    if request.user.u_type == 0:
        return redirect(reverse('actlend', kwargs={"idn": request.user.id}))
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
def actlend(request,idn):
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
    return render(request, 'main/actlend.html')

@login_required(login_url='/login')
def activity(request):
    reqs=[]
    breqs=[]#borrower inu rent history nokkaanulla reqs
    requests = PReq.objects.all()
    present_user = request.user
    coms = Comment.objects.filter(user = present_user).order_by('-created_at')
    com=0
    if coms:
        com=1
    my_products = Product.objects.filter(user = present_user)
    for pro in my_products:
        for req in requests:
            if req.product == pro:
                reqs.append(req)
    if reqs:
        reqs.sort(reverse=True,key=myFunc)
    breq = PReq.objects.filter(borrower = present_user,status__in=['1','3'])
    for req in breq:
        breqs.append(req)
    bacc=0
    if breqs:
        bacc=1
        breqs.sort(reverse=True,key=myFunc)
    pend = 0
    acc = 0
    dec = 0
    for req in reqs:
        if req.status == 0:
            pend = 1
        elif req.status == 1 or req.status == 3:
            acc = 1
        elif req.status == 2:
            dec = 1
    return render(request, 'main/activity.html',{'requests':reqs, 
    'breqs':breqs, 'bacc':bacc, 'pending':pend, 'accepted':acc, 'declined':dec,'comments':coms,'com':com})

@login_required(login_url='/login')
def borrow(request, idn):
    d = 0
    if 'days' in request.POST:
        d = int(request.POST.get('days'))
    req = PReq()
    req.borrower = request.user
    req.product = Product.objects.get(id=idn)
    req.days = d
    req.save()
    return redirect(reverse('product', kwargs={"idn": idn}))

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
    try:
        rep = ReportUser.objects.get(r_by=request.user,r_user=idn)
        return render(request, 'main/reportsuccess.html')
    except:
        return render(request, 'main/reportuser.html',{'userid':idn})

@login_required(login_url='/login')
def repous(request,idn):
    if request.method == 'POST':
        rep = ReportUser()
        rep.r_user = idn
        rep.r_by = request.user
        rep.desc = request.POST.get('description')
        rep.save()
        return render(request, 'main/reportsuccess.html')
    else:
        pass
    return None

@login_required(login_url='/login')
def reportcomment(request,idn):
    comment = Comment.objects.get(id=idn)
    try:
        rep = ReportComment.objects.get(comment=comment,user=request.user)
        return render(request, 'main/reportsuccess.html')
    except:
        return render(request, 'main/reportcomment.html',{'comid':idn})

@login_required(login_url='/login')
def repoco(request,idn):
    if request.method == 'POST':
        comment = Comment.objects.get(id=idn)
        rep = ReportComment()
        rep.comment = comment
        rep.user = request.user
        rep.desc = request.POST.get('description')
        rep.save()
        return render(request, 'main/reportsuccess.html')
    else:
        pass
    return None

@login_required(login_url='/login')
def reportsuccess(request):
    return render(request, 'main/reportsuccess.html')

@login_required(login_url='/login')
def wishlist(request,idn):
    if request.method == 'POST':
        #avoid creating duplicate wishlist entry
        prod = Product.objects.get(id=idn)
        test1 = request.POST.get('productpageb1')
        if test1 == '10':
            try:
                wish = Wishlist.objects.get(user=request.user,product=prod)
                return redirect(reverse('product', kwargs={"idn": idn}))
            except:
                wish = Wishlist()
                wish.product = prod
                wish.user = request.user
                wish.save()
                return redirect(reverse('product', kwargs={"idn": idn}))
        test2 = request.POST.get('homepageb1')
        if test2 == '10':
            try:
                wish = Wishlist.objects.get(user=request.user,product=prod)
                return redirect('home')
            except:
                wish = Wishlist()
                wish.product = prod
                wish.user = request.user
                wish.save()
                return redirect('home')
        test3 = request.POST.get('wishpageb1')
        if test3 == '10':
            try:
                wish = Wishlist.objects.get(user=request.user,product=prod)
                return redirect('viewwish')
            except:
                wish = Wishlist()
                wish.product = prod
                wish.user = request.user
                wish.save()
                return redirect('viewwish')
    else:
        pass

@login_required(login_url='/login')
def unwish(request,idn):
    if request.method == 'POST':
        prod = Product.objects.get(id=idn)
        test1 = request.POST.get('productpageb2')
        if test1 == '20':
            Wishlist.objects.filter(user=request.user,product=prod).delete()
            return redirect(reverse('product', kwargs={"idn": idn}))
        test2 = request.POST.get('homepageb2')
        if test2 == '20':
            Wishlist.objects.filter(user=request.user,product=prod).delete()
            return redirect('home')
        test3 = request.POST.get('wishpageb2')
        if test3 == '20':
            Wishlist.objects.filter(user=request.user,product=prod).delete()
            return redirect('viewwish')
    else:
        pass

@login_required(login_url='/login')
def viewwish(request):
    wish = Wishlist.objects.filter(user=request.user)
    prodids = list(Wishlist.objects.filter(user=request.user).values_list('product', flat=True).order_by('id'))
    empty = 0
    if wish:
        empty = 1
    return render(request, 'main/wishlist.html',{'wishes':wish,'empty':empty,'prodids':prodids})

#profile view
@login_required(login_url='/login')
def profile(request,idn):
    prof_user = User.objects.get(id=idn)
    userid = request.user.id
    l = int(prof_user.len_rate)
    b = int(prof_user.bor_rate)
    lx = 5 - l
    bx = 5 - b
    le = []
    bo = []
    lex = []
    box = []
    for i in range(l):
        le.append(str(i))
    for i in range(b):
        bo.append(str(i))
    for i in range(lx):
        lex.append(str(i))
    for i in range(bx):
        box.append(str(i))
    return render(request, 'main/profile.html',{'userid':userid,'prof_user':prof_user,'l':le,'b':bo,'lx':lex,'bx':box})

#profile edit
@login_required(login_url='/login')
def profileedit(request,idn):
    prof_user = User.objects.get(id=idn)
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phoneno=request.POST.get('phoneno')
        address=request.POST.get('address')
        #state=request.POST.get('state')
        #district=request.POST.get('district')
        if password == '':
            User.objects.filter(id=idn).update(name=name,email=email,phoneno=phoneno,address=address)
        else:
            passwordcopy=password
            password=make_password(password,hasher='default')
            User.objects.filter(id=idn).update(name=name,email=email,password=password,phoneno=phoneno,address=address)
            user = authenticate(request, email=email, password=passwordcopy)
            login(request, user)
        return redirect(reverse('profileedit', kwargs={"idn": idn}))
    else:
        pass
    return render(request, 'main/profileedit.html',{'prof_user':prof_user})

#add comment in product page or via product rating page
@login_required(login_url='/login')
def comment(request,idn):
    if request.method == 'POST':
        com = Comment()
        com.product = Product.objects.get(id=idn)
        com.user = request.user
        com.content = request.POST.get('comment')
        com.save()
        #return redirect('product/<idn>')
        return redirect(reverse('product', kwargs={"idn": idn}))
    else:
        pass
    return None

#rating Section :
#Borrower Rating
@login_required(login_url='/login')
def rateborrower(request,idn):
    return render(request, 'main/rateborrower.html')

#Lender Rating
@login_required(login_url='/login')
def ratelender(request,idn):
    return render(request, 'main/ratelender.html')


def productlist(request):
    products = Product.objects.filter().values_list('p_name', flat=True)
    productList = list(set(list(products)))
    return JsonResponse(productList, safe=False)
    
def searchProduct(request):
    if request.method == 'POST':
        searchedProduct = request.POST.get('searched_prod')
        # products = Product.objects.filter(p_name__contains = searchedProduct)
        # print(searchedProduct)
        # return render(request, 'main/home.html',{'products':products})
        products = Product.objects.all()
        if searchedProduct:
            products = products.filter(Q(p_name__icontains = searchedProduct))
            print(products)
            return render(request, 'main/home.html',{'products':products})
        else:
            pass
    else:
        pass
    return None
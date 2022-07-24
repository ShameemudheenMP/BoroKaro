
import re
from winreg import HKEY_LOCAL_MACHINE
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import datetime
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from datetime import timedelta
import pytz

# Create your views here.

#sort by date function
def myFunc(e):
    return e.created_at

def home(request):
    products = Product.objects.all()
    tz = pytz.timezone('Asia/Kolkata') # dont use this timezone since datetime.now returns UTC time and products are rated at UTC time
    #initial lookup period is 14 days or 2 weeks
    for product in products:
        rating_count = 0
        prod_ratings=[]
        #first check if this product has at least one rating, if not directly set its rating value to 0
        rating_present = len(list(ProductRating.objects.filter(product=product).values_list('val', flat=True).order_by('created_at')))
        if rating_present:
            #check if product ratings exist within current lookup period and if not, increment threshold by 2 weeks inside a while loop
            threshold = 14
            compare_date = datetime.now(tz) - timedelta(days=threshold)
            while( ProductRating.objects.filter(created_at__gt=compare_date,product=product).count() <= 0):
                threshold = threshold + 14
                compare_date = datetime.now(tz) - timedelta(days=threshold)
            #use the obtained optimal threshold to filter required ratings and calculate average of those ratings
            prod_ratings = list(ProductRating.objects.filter(created_at__gt=compare_date,product=product).values_list('val', flat=True).order_by('created_at'))
            rating_count = len(prod_ratings)
            product.rating = round(sum(prod_ratings)/rating_count)
        else:
            product.rating =  0
        product.rating_count = rating_count
        product.save()
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
    breq = PReq.objects.filter(borrower = present_user,status__in=['1','3','4','5','6'])
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
        elif req.status == 1 or req.status == 3 or req.status == 5 or req.status == 6:
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
    len_ratings = list(LenderRating.objects.filter(lender_id=idn).values_list('val', flat=True).order_by('id'))
    count2 = len(len_ratings)
    if count2:
        len_rate = round(sum(len_ratings)/count2)
    else:
        len_rate = 0
    prof_user.len_rate = len_rate
    bor_ratings = list(BorrowerRating.objects.filter(borrower_id=idn).values_list('val', flat=True).order_by('id'))
    count1 = len(bor_ratings)
    if count1:
        bor_rate = round(sum(bor_ratings)/count1)
    else:
        bor_rate = 0
    prof_user.bor_rate = bor_rate
    prof_user.save()
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
    return render(request, 'main/profile.html',{'userid':userid,'prof_user':prof_user,'l':le,'b':bo,'lx':lex,'bx':box,
    'count1':count1,'count2':count2})

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
        state=request.POST.get('states')
        district=request.POST.get('districts')
        if password == '':
            User.objects.filter(id=idn).update(name=name,email=email,phoneno=phoneno,address=address,state=state,district=district)
        else:
            passwordcopy=password
            password=make_password(password,hasher='default')
            User.objects.filter(id=idn).update(name=name,email=email,password=password,phoneno=phoneno,address=address,state=state,district=district)
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
    req = PReq.objects.get(id=idn)
    product = Product.objects.get(id=req.product.id)
    if request.method == 'POST':
        bor_rate = int(request.POST.get('borrowerRating'))
        if bor_rate >=1 and bor_rate<=5:
            bor_r = BorrowerRating()
            bor_r.lender = request.user
            bor_r.borrower_id = req.borrower.id
            bor_r.product = product
            bor_r.val = bor_rate
            bor_r.save()
            if req.status == 3:
                req.status = 4
            elif req.status == 5:
                req.status = 6
            req.save()
        return redirect('activity')
    else:
        return render(request, 'main/rateborrower.html', {'request':req})

#Lender Rating
@login_required(login_url='/login')
def ratelender(request,idn):
    product = Product.objects.get(id=idn)
    if request.method == 'POST':
        len_rate = int(request.POST.get('lenderRating'))
        if len_rate >=1 and len_rate <=5:
            len_r = LenderRating()
            len_r.borrower = request.user
            len_r.lender_id = product.user.id
            len_r.val = len_rate
            len_r.save()
            reqs = PReq.objects.filter(borrower = request.user,  product = product, status__in=['1','3','4'])
            req = reqs.latest('created_at')
            if req.status == 1 or req.status == 3:
                req.status = 5
            elif req.status == 4:
                req.status = 6
            req.save()
        prod_rate = int(request.POST.get('productRating'))
        if prod_rate >=1 and prod_rate <=5:
            prod_r = ProductRating()
            prod_r.product = product
            prod_r.user = request.user
            prod_r.val = prod_rate
            prod_r.save()
        comment = request.POST.get('comment')
        if comment:
            com = Comment()
            com.product = Product.objects.get(id=idn)
            com.user = request.user
            com.content = comment
            com.save()
        return redirect('activity')
    else:
        return render(request, 'main/ratelender.html',{'product':product})
from calendar import month
from enum import auto
from operator import mod
from pickle import FALSE
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime

def default_start_time():
    now = datetime.now()
    start = now.replace(microsecond=0)
    ans = start.strftime("%I:%M %p %d/%m/%Y")
    return ans

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    #u_id = models.AutoField("User ID", primary_key=True)
    username = None
    u_type = models.IntegerField(default=0)
    name = models.CharField(max_length=26)
    email = models.EmailField(unique=True)
    phoneno = models.CharField(max_length=11)
    STATE_CHOICES = [
        ('KL','Kerala'),
        ('TN','Tamilnadu'),
        ('KA','Karnataka')
    ]
    state = models.CharField(max_length=2,choices=STATE_CHOICES,default='KL')

    DISTRICT_CHOICES = [
        ('TVM','Thiruvananthapuram'),
        ('KLM','Kollam'),
        ('KTM','Kottayam'),
        ('MPM','Malappuram')
    ]

    district = models.CharField(max_length=3,choices=STATE_CHOICES,default='TVM')
    address = models.CharField(max_length=90,default='')
    len_rate = models.IntegerField(default=0)
    bor_rate = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def __str__(self):
        return "%d" % (self.id)

class Product(models.Model):
    p_name = models.CharField(max_length=50)
    p_rate = models.IntegerField(default=0)
    p_desc = models.CharField(max_length=90)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_image1 = models.ImageField(upload_to = 'uploads/',blank=True)
    p_image2 = models.ImageField(upload_to = 'uploads/',blank=True)
    p_image3 = models.ImageField(upload_to = 'uploads/',blank=True)
    date =  models.DateField(auto_now=False, auto_now_add=False)
    status = models.IntegerField(default=0) #0 for available, 1 for not available
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

# class ProdImage(models.Model):
#     product = models.ForeignKey(Product, related_name='prodimage',on_delete=models.CASCADE)
#     image = models.ImageField(upload_to = 'uploads/')

class PReq(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.IntegerField(default=0) #0 for pending, 1 for accepted, 2 for declined, 3 for prod_rcvd
    days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.CharField(max_length=20,default=default_start_time)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.CharField(max_length=20,default=default_start_time)

class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class ReportUser(models.Model):
    r_by = models.ForeignKey(User, on_delete=models.CASCADE)
    r_user = models.IntegerField(default=0)
    desc = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

#USER SHOULD NOT REQUEST HIS OWN PRODUCT - DONE
#product recvd nekki kazhinjaal pinne aa button kanikkaruth activity page il - DONE
#disable borrow button (not remove) if product is not available - DONE
#user should not be able to request the same product more than once if the existing request is in pending list - DONE
#DAYS VECHULLA REQ - DONE
#COMMENTS - DONE
#REPORT COMMENTS - DONE
#REPORT USER - DONE
#comment section and product lender details il ninnu users ne click cheythu profile view cheyyaan pattanam - done
#profile page - done (some error in district info) & edit profile
#WISHLIST
#OCR
#rent history
#RATINGS
#SEARCH FILTER, REQUEST FILTER, RENT HISTORY FILTER
#ratings kanikkumbo athinte koode user count bracket il kanikkenam
#CHAT
#OWNER CAN DELETE A PRODUCT AND USER CAN REMOVE HIS COMMENT
#a user should not access another user's activity or lend page
from calendar import month
from operator import mod
from pickle import FALSE
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    address = models.CharField(max_length=50,default='')
    
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
    p_desc = models.CharField(max_length=70)
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
    days = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

#USER SHOULD NOT REQUEST HIS OWN PRODUCT - DONE
#product recvd nekki kazhinjaal pinne aa button kanikkaruth activity page il - DONE
#disable borrow button (not remove) if product is not available - DONE
#user should not be able to request the same product more than once if the existing request is in pending list - DONE
#DAYS VECHULLA REQ
#RENT HISTORY
#COMMENTS
#REPORT USER, COMMENTS
#WISHLIST
#OCR
#SEARCH FILTER, REQUEST FILTER, RENT HISTORY FILTER
#RATINGS
#PROFILE PAGE & EDIT PROFILE
#CHAT
#OWNER CAN DELETE A PRODUCT AND USER CAN REMOVE HIS COMMENT
#login required for all pages other than home page

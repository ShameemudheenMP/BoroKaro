from calendar import month
from operator import mod
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

    username = None
    u_type = models.IntegerField(null=True)
    name = models.CharField(max_length=26)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=11, null=True)
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Product(models.Model):
    p_name = models.CharField(max_length=50)
    p_rate = models.IntegerField(default=0)
    p_desc = models.CharField(max_length=70)
    p_image1 = models.ImageField(upload_to = user_directory_path)
    p_image2 = models.ImageField(upload_to = user_directory_path)
    p_image3 = models.ImageField(upload_to = user_directory_path)
    u_id = models.IntegerField(default=0)
    month =  models.DateField(auto_now=False, auto_now_add=False)
    year = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)


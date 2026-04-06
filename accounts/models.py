from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.

class CustomUser(AbstractUser):
    username=None
    phone_number=models.CharField(max_length=100, null=True, blank=True, default=None)
    email=models.EmailField(unique=True)
    user_bio = models.CharField(max_length=50, blank=True, default='')
    user_profile_image = models.ImageField(upload_to='profile', null=True, blank=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=UserManager()
from django.db import models
from datetime import datetime,date
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
User=get_user_model()
# Create your models here.
class todo(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title1=models.CharField(max_length=100)
    desc=models.CharField(max_length=200,blank=True,null=True)
    done=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)  #...... alternative to default=timezone.now
    due_date=models.DateField(null=True,blank=True)
    completed_at=models.DateTimeField(default=timezone.now,null=True,blank=True)
    order= models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']  
    PRIORITY_CHOICES = [
        ('Low',    'Low'),
        ('Medium', 'Medium'),
        ('High',   'High'),
    ]
    priority  = models.CharField(         
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='High'
    )


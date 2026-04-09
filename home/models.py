from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    address=models.TextField(blank=True,null=True)
    email=models.EmailField()
    image=models.ImageField()
    file=models.FileField()
    
class Cars(models.Model):
    car_name=models.CharField(max_length=100)
    speed=models.IntegerField(default=0)
    def __str__(self):
        return f"{self.speed}+{self.car_name}"
      
@receiver(post_save,sender=Cars)
def call_car_api(sender,instance,**kwargs):
    print("Car object created")
    print(sender,instance,kwargs)
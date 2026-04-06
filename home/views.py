from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User=get_user_model()
from .utils import send_email_to_client,send_email_with_attachment
from django.conf import settings
from home.models import Cars
import random
# Create your views here.
def home(request):
    return HttpResponse("Hey I am a boy")


def html(request):
    # Cars.objects.create(car_name=f"Nexon-{random.randint(0,100)}")
    peoples=[{"name":'ajay','age':18},{"name":'anup','age':15},{"name":'anjali','age':16},{"name":'advik','age':6}]
    text="loerem100sddnlsdncsnjkvnclsdcbfvbLMnEEeebjkBCblLDCNLJVBLCb"
    return render(request,"home/index.html",context={'peoples':peoples,'text':text})
def about(request):
    context={'page':'About'}
    return render(request,"home/about.html",context)
def contact(request):
    context={'page':'Contact'}
    return render(request,"home/contact.html",context)
def base(request):
    return render(request,"home/base.html")

def send_email(request):
    subject="This email is from Anup's django server with Attachment"
    message="Hey please check this attachment and let me know   !!!"
    recipient_list=["kingknightofmedival@gmail.com"]
    file_path=f"{settings.BASE_DIR}/manage.py"
    send_email_with_attachment(subject,message,recipient_list,file_path)
    return redirect('/')


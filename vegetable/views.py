from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your views here.
@login_required(login_url='/login/')
def recipe_func(request):
    if request.method=="POST":
        data=request.POST
        recipe_img=request.FILES.get('recipe_img')
        recipe_name=data.get('recipe_name')
        recipe_desc=data.get('recipe_desc')
        print(recipe_name)
        print(recipe_desc)
        print(recipe_img)
        vege.objects.create(
            recipe_name=recipe_name,recipe_desc=recipe_desc,recipe_img=recipe_img
        )
        return redirect('/Recipe/')
    queryset=vege.objects.all()

    if request.GET.get('search_te'):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search_te'))
        
    context={'recipe':queryset}
    return render(request,"vegetable/recipe.html",context)

def update_recipe(request,slug):
    queryset=vege.objects.get(slug=slug)
    
    if request.method=="POST":
        data=request.POST
        recipe_img=request.FILES.get('recipe_img')
        recipe_name=data.get('recipe_name')
        recipe_desc=data.get('recipe_desc')

        queryset.recipe_name=recipe_name
        queryset.recipe_desc=recipe_desc
        if recipe_img:
            queryset.recipe_img=recipe_img
        
        queryset.save()
        return redirect('/Recipe/')
    context={"recipe":queryset}
    return render(request,"vegetable/up_recipe.html",context)



def delete_recipe(request,id):
    queryset=vege.objects.get(id=id)
    queryset.delete()
    return redirect('/Recipe/')


def register_user(request):
    if request.method=="POST":
        data=request.POST
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        email=data.get("email")
        password=data.get("password")

        user=User.objects.filter(email=email)
        if user.exists():
            messages.info(request,"Username already exists")
            return redirect('/register/')


        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(password)
        user.save()

        messages.info(request,"Account created successfully")

        return redirect('/register/')
    return render(request,"vegetable/register.html")

def login_user(request):
    if request.method=="POST":
        data=request.POST
        email=data.get("email")
        password=data.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login/')
        
        user=authenticate(email=email,password=password)

        if user is None:
            messages.error(request,"Invalid Password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect("/Recipe/")

    return render(request,"vegetable/login.html")

def logout_user(request):
    logout(request)
    return redirect('/login/')
from django.db.models import Q,Sum
def get_students(request):
    queryset=Student.objects.all()
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-age')
    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(
            Q(name__icontains=search)|
            Q(department__department__icontains=search)|
            Q(student_id__student_id__icontains=search)|
            Q(email__icontains=search)|
            Q(age__icontains=search)

        )
    paginator=Paginator(queryset,16)
    page_num=request.GET.get('page',1)
    page_obj=paginator.get_page(page_num)
    return render(request,'vegetable/report/student.html',{'queryset':page_obj})

def see_marks(request,student_id):
    queryset=SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks=queryset.aggregate(total_marks=Sum('marks'))
    return render(request,'vegetable/report/see_marks.html',{'queryset':queryset,'total_marks':total_marks})
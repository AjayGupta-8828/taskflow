from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import connection
User=get_user_model()

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def reorder_tasks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                todo.objects.filter(id=item['id']).update(order=item['order'])
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # ← This handles GET and any other method gracefully
    return JsonResponse({'status': 'error', 'message': 'POST request required'}, status=405)

# Create your views here.
@login_required(login_url='/login1/')
def todocheck(request):
    if request.method=="POST":
        data=request.POST
        title1=data.get("title1")
        desc=data.get("desc")
        due_date=data.get("due_date")
        if not due_date:
            due_date = None
        priority = request.POST.get('priority', 'High')
        if title1:
            todo.objects.create(
                user=request.user,title1=title1,desc=desc,due_date=due_date, priority=priority
            )
        return redirect('/todo/')
    queryset=todo.objects.filter(done=False,user=request.user)
    if request.GET.get('search_te'):
        queryset=queryset.filter(title1__icontains=request.GET.get('search_te'))
    context={'tasks':queryset}
    return render(request,"practice/base1.html",context)

@login_required
def update_todo(request,id):
    queryset=todo.objects.get(user=request.user,id=id)
    
    if request.method=="POST":
        data=request.POST
        title1=data.get("title1")
        desc=data.get("desc")
        due_date=data.get("due_date")

        queryset.title1=title1
        queryset.desc=desc
        queryset.priority = data.get('priority', queryset.priority)
        if due_date:
            queryset.due_date=due_date
        
        queryset.save()
        return redirect('/todo/')
    context={"tasks":queryset}
    return render(request,"practice/up_todo.html",context)

@login_required
def delete_todo(request,id):
    queryset=todo.objects.get(user=request.user,id=id)
    queryset.delete()
    return redirect('/todo/')

@login_required
def done_task(request,id):
    queryset=todo.objects.get(user=request.user,id=id)
    if request.method=="POST":
       data=request.POST
       if request.POST.get("done"):
            queryset.title1=queryset.title1
            queryset.completed_at=timezone.now()
            queryset.done=True
            queryset.save()
    completed_tasks=todo.objects.filter(user=request.user,done=True)
    context={"tasks":completed_tasks}
    return redirect("/todo/")
    
@login_required(login_url='/login1/')
def comptaskpage(request):
    completed_tasks=todo.objects.filter(user=request.user,done=True)
    context={"tasks":completed_tasks}
    return render(request,"practice/comptask.html",context)

@login_required    
def delete_comptask(request,id):
    queryset=todo.objects.get(user=request.user,id=id)
    queryset.delete()
    return redirect('/completed_tasks/')


def register_user1(request):
    if request.method=="POST":
        data=request.POST
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        email=data.get("email")
        password=data.get("password")

        user=User.objects.filter(email=email)
        if user.exists():
            messages.info(request,"Username already exists")
            return redirect('/register1/')


       # ✅ Correct way matching new manager
        user = User.objects.create_user(
            email=email,           # ← passed as first argument now
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        messages.info(request,"Account created successfully")

        return redirect('/register1/')
    return render(request,"practice/register1.html")

def login_user1(request):
    if request.method=="POST":
        data=request.POST
        email=data.get("email")
        password=data.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login1/')
        
        user=authenticate(email=email,password=password)

        if user is None:
            messages.error(request,"Invalid Password")
            return redirect('/login1/')
        else:
            login(request,user)
            return redirect("/todo/")

    return render(request,"practice/login1.html")

def logout_user1(request):
    logout(request)
    return redirect('/login1/')





# Just to check whether the database connection is working fine or not

def db_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        if result == (1,):
            return HttpResponse("Database connection is working!")
        else:
            return HttpResponse("Unexpected database response.")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {e}")
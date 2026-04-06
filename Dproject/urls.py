"""
URL configuration for Dproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home.views import *
from vegetable.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from practice.views import *


urlpatterns = [
    path('',html,name='html'),
    path('home/',home,name="home"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('admin/', admin.site.urls),
    path("base/",base,name="base"),
    path("Recipe/",recipe_func,name="recipe"),
    path("delete_recipe/<int:id>/",delete_recipe,name="delete_recipe"),
    path("update_recipe/<slug>/",update_recipe,name="update_recipe"),
     path("register/",register_user,name="register"),
     path("login/",login_user,name="login"),
    path("logout/",logout_user,name="logout"),
    path("student/",get_students,name="student"),
    path("see_marks/<student_id>/",see_marks,name="see_marks"),
    path("send_email/",send_email,name="send_email"),
    path("todo/",todocheck,name="todocheck"),
    path("update_todo/<int:id>/",update_todo,name="update_todo"),
    path("delete_todo/<int:id>/",delete_todo,name="delete_todo"),
    path("done_task/<int:id>/",done_task,name="done_task"),
    path("completed_tasks/",comptaskpage,name="comptaskpage"),
    path("delete_comptask/<int:id>/",delete_comptask,name="delete_comptask"),
    path("register1/",register_user1,name="register1"),
     path("login1/",login_user1,name="login1"),
    path("logout1/",logout_user1,name="logout1"),
    path('reorder_tasks/', reorder_tasks, name='reorder_tasks'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()
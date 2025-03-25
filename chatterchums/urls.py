"""
URL configuration for chatterchums project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from .views import *
from forums.views import home



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('forums/', include('forums.urls', namespace='forums')),
    path('', home, name='home'),
<<<<<<< HEAD
    path('addForum/', add_forum, name='addForum'),
    path('addChat/', add_chat, name='addChat'),
    path('<str:forum_name>/', forum, name='forum'),
    path('language/<str:language>/', language, name='language'),
    path('login/<str:username>/', login_user, name='login_user')
=======
    path('about/',about_view,  name ='about')
>>>>>>> 1370a83c285b5998de00f28909f38cc5cd2fbffc
]

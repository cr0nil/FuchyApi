"""fuchyRestApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.views.generic import TemplateView
from .views import (registration_view, getListJobs, login_view, getJobDetails, getMyJobs)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'fuchyRestApi'

# app_name = "fuchyRestApi"
urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', login_view, name="login"),
    path('job',getListJobs),
    path('myJobs',getMyJobs),
    path('job/<int:pk>/',getJobDetails)
]

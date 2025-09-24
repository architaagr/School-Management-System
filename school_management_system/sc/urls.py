"""
URL configuration for sc project.

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
from django.urls import path
from . import views

urlpatterns = [
    path('enter_marks/', views.enter_marks, name='enter_marks'),
    path('view_marks/', views.view_marks, name='view_marks'),
    path('view_student_details/', views.details, name='view_student_details'),
    path('enter_std_details/', views.std_details, name='std_details'),
    path('enter_tch_details/', views.tch_details, name='tch_details'),
    path('view_std_details/', views.details, name='details'),
    path('view_tch_details/', views.view_tch_details, name='tch_details'),
    path('select_student/', views.dropdownsearch, name='select_student'),
    path('tch_details/', views.tch_details, name='tch_details'),
    path('home/' , views.home, name='home'),
    path('teacher/' , views.teacher, name='teacher'),
    path('student/' , views.student, name='student'),
    path('login/', views.login, name='login'),
    path('view_marks_as_std/' , views.view_marks_as_std, name='view_marks_as_std'),
    path('update_marks/' , views.enter_marks, name='update_marks')
]

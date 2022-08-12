"""newdjangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.shortcuts import redirect
from newdjangoProject import views

# app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>', views.detail, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'<int:course_no>/add_interest/',
         views.add_interest, name='add_interest'),
    path(r'courses/<int:course_no>/', views.coursedetail, name='coursedetail'),
    path(r'placeorder', views.placeorder, name='placeorder'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myaccount/', views.myaccount, name='myaccount'),
    path(r'myaccount//', lambda req: redirect('/myapp/myaccount/')),
    path(r'register/', views.register, name='register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'forgot_password/', views.forgot_password, name='forgot_password'),
    path(r'send_new_password/', views.send_new_password, name='send_new_password'),
    path(r'edit_profile/', views.edit_profile, name='edit_profile')
]

from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.step1, name='step1'),
    path('step2/', views.step2, name='step2'),
    path('step3/', views.step3, name='step3'),
    path('success/', views.success, name='success'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
]

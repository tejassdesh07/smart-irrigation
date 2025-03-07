from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.step1, name='step1'),
    path('step2/', views.step2, name='step2'),
    path('step3/', views.step3, name='step3'),
    path('success/', views.success, name='success'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('report/<int:report_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('user/edit/<int:user_id>/', views.update_user, name='update_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user-list/', views.user_list, name='user_list'),
    path('zone/edit/<int:zone_id>/', views.edit_zone, name='edit_zone'),
    path('zone/delete/<int:zone_id>/', views.delete_zone, name='delete_zone'),

]

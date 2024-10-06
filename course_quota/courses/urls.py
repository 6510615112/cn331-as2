from django.urls import path
from courses import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('course_list', views.course_list, name='course_list'),
    path('login/', views.student_login, name='login'),
    path('register/', views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('request/<int:course_id>/', views.request_quota, name='request_quota'),
    path('quota_requests/', views.quota_requests_list, name='quota_requests_list'),
    path('approve/<int:request_id>/', views.approve_quota_request, name='approve_quota_request'),
    path('my_requests/', views.my_quota_requests, name='my_quota_requests'),
    path('cancel/<int:request_id>/', views.cancel_quota_request, name='cancel_quota_request'),
    path('my_enrolled_courses/', views.my_enrolled_courses, name='my_enrolled_courses'),
    path('course/<int:course_id>/requests/', views.course_quota_requests, name='course_quota_requests'),
]

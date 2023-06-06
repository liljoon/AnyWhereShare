from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_mode, name='user_mode'),
    path('user_mode/', views.user_mode, name='user_mode'),
    path('guest_mode/', views.guest_mode, name='guest_mode'),
    path('user_set/', views.user_set, name='user_set'),
    path('change_pw/', views.change_pw, name='change_pw'),
]
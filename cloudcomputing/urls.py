from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('user_mode/', views.user_mode, name='user_mode'),
    path('guest_mode/', views.guest_mode, name='guest_mode'),
    path('user_set/', views.user_set, name='user_set'),
    path('help/', views.help, name='help'),
    path('login/', views.login, name='login'),
    path('create/', views.create, name='change_pw'),
    path('trash/', views.trash, name='change_pw'),
    path('guest_login/', views.guest_login, name='guest_login'),
]

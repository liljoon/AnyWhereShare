from django.urls import path
from . import views

urlpatterns = [
    path('', views.showShareLink.as_view(), name='showShareLink'),
]
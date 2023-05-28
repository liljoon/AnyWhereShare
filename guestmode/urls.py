from django.urls import path, include
from . import views

urlpatterns = [
	path('generate/', views.Generating.as_view()),
]

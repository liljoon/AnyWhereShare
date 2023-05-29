from django.urls import path, include
from . import views

urlpatterns = [
	path('generate/', views.Generating.as_view()),
	path('upload/', views.Upload.as_view()),
]

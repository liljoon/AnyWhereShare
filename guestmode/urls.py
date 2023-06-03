from django.urls import path, include
from . import views

urlpatterns = [
	path('generate/', views.Generating.as_view()),
	path('upload/', views.Upload.as_view()),
	path('list/', views.ListFilesView.as_view()),
	path('login/', views.LoginView.as_view()),
]

from django.urls import path, include
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register('sharing', views.sharingViewSet)

urlpatterns = [
	#path('', views.showShareLink.as_view(), name='showShareLink'),
	#path('', include(router.urls)),
	path('test/', views.sharingAPIView.as_view())
]

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GuestUser
from .serializers import GuestUserSerializer
from rest_framework.permissions import *
# Create your views here.

import random, string
def generate_passwd():
	while True:
		passwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
		if len(GuestUser.objects.filter(passwd=passwd)) == 0:
			break
	return passwd

class Generating(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]
	def get(self, request):
		new_user = GuestUser(passwd=generate_passwd())
		new_user.save()
		serial = GuestUserSerializer(new_user)
		print(new_user.passwd)
		return Response(serial.data)


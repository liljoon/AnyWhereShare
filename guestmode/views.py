from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GuestUser, FileInfo
from .serializers import GuestUserSerializer
from rest_framework.permissions import *
from rest_framework import status
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

from .s3_utils import uploadFile, generateDownloadUrl

class Upload(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		file = request.FILES.get('file')
		passwd = request.data.get('passwd')
		try:
			user = GuestUser.objects.get(passwd=passwd)
			uploadFile(file, passwd)
			file_info = FileInfo(owner=user, file_name=file.name, download_url=generateDownloadUrl(file, passwd))
			file_info.save()

			return Response({'message': '파일 업로드 성공'}, status=status.HTTP_201_CREATED)

		except:
			return Response({'error': '파일 업로드 실패'}, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GuestUser, FileInfo
from .serializers import GuestUserSerializer, FilesListSerializer
from rest_framework.permissions import *
from rest_framework import status
from django.http import HttpResponseRedirect
import os
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
		return Response(serial.data)

class ListFilesView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		passwd = request.data.get('passwd')
		try:
			user = GuestUser.objects.get(passwd=passwd)
			file_list = FileInfo.objects.filter(owner=user)
			serial = FilesListSerializer(file_list, many=True)
			return Response(serial.data, status=status.HTTP_200_OK)

		except:
			return Response({'error': '일치하는 유저 없음'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		passwd = request.data.get('passwd')
		try:
			user = GuestUser.objects.get(passwd=passwd)
			return Response({'error': '로그인 성공!'}, status=status.HTTP_200_OK)

		except:
			return Response({'error': '일치하는 유저 없음'}, status=status.HTTP_400_BAD_REQUEST)


from .s3_utils import uploadFile, generateDownloadUrl

class Upload(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		file = request.FILES.get('file')
		passwd = request.COOKIES.get('passwd')
		try:
			user = GuestUser.objects.get(passwd=passwd)
			uploadFile(file, passwd)
			file_info = FileInfo(
				owner=user,
				file_name=file.name,
				download_url=generateDownloadUrl(file, passwd),
				suffix_name= os.path.splitext(file.name)[1],
				size=file.size
				)
			file_info.save()

			return HttpResponseRedirect('/guest_mode/')
			#return Response({'message': '파일 업로드 성공'}, status=status.HTTP_201_CREATED)

		except:
			return Response({'error': '파일 업로드 실패'}, status=status.HTTP_400_BAD_REQUEST)


class FileInfoView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		idx = request.GET.get("id")
		file = FileInfo.objects.get(id=idx)
		serial = FilesListSerializer(file)

		return Response(serial.data, status=status.HTTP_200_OK)

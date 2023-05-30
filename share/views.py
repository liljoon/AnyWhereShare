from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import requests
from config.settings import get_secret
from .models import sharing
from .serializers import sharingSerializer
from rest_framework import viewsets
from rest_framework.permissions import *
from rest_framework.views      import APIView
from rest_framework.response      import Response
from rest_framework import status


# Create your views here.

# 사용법 : /share/?url=https://naver.com 접속 시 짧은 url 출력
class showShareLink(View):
    def get(self, request):
        url = request.GET.get('url', None);
        headers = {
            'Authorization': f'Bearer {get_secret("bitly_API_Key")}',
            'Content-Type': 'application/json',
        }
        data = f'{{ "long_url": "{url}" }}'

        response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
        print(response.json())
        return render(request, 'shareLink.html', {'url':response.json()['id'] })

class sharingViewSet(viewsets.ModelViewSet):
    queryset = sharing.objects.all()
    serializer_class = sharingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

import random, string
def generate_code():
	while True:
		code = ''.join(random.choice(string.digits) for _ in range(6))
		qs = sharing.objects.filter(code=code)
		if len(qs) == 0:
			break
	return code


class sharingAPIView(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]
	def get(self, request, format=None):
		url = request.GET.get('url')
		code = request.GET.get('code')
		# url, code 들어오면 그것에 대해 반환
		if url:
			qs = sharing.objects.filter(url_origin=url)
		elif code:
			qs = sharing.objects.filter(code=code)
			if len(qs) == 0: # 없는 코드일 경우
				return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)
		if len(qs) == 0: # 이미 만들어진 링크가 없다면 생성
			# bitly 인증
			headers = {
				'Authorization': f'Bearer {get_secret("bitly_API_Key")}',
				'Content-Type': 'application/json',
			}
			data = f'{{ "long_url": "{url}" }}' # 원본 url 전송
			# url 단축
			response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
			# 단축된 url 저장
			id = response.json()['id']
			# 단축된 url을 기반으로 qr api 호출
			response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{id}/qr', headers=headers)
			qr = response.json()['qr_code']
			#sharing model에 전부 저장
			to_save = sharing(qr_img_b64=qr, url_origin=url, url=id, code=generate_code())
			to_save.save()
			# 응답
			serial = sharingSerializer(to_save)
			return Response(serial.data)
		else: # 이미 만들어져있으면 찾아서 반환
			serial = sharingSerializer(qs[0])
			return Response(serial.data)

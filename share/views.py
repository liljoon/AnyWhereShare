from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import requests
from config.settings import get_secret

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

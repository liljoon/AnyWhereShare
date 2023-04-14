from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import AccountDetailSerializer
from .models import Account
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

import json, bcrypt
class ListAccountsView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountDetailSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupAccountsView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        try:
            req_userid = data['userId']
            req_password = bcrypt.hashpw(data['password'].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            req_username = data['username']
            req_email = data['email']
            if Account.objects.filter(email=req_email).exists():
                return JsonResponse({'message': '이미 존재하는 이메일'}, status=status.HTTP_200_OK)
            account = Account.objects.create(
                userId = req_userid,
                password = req_password,
                username = req_username,
                email = req_email,
                accountType = 'RE',
            )
            account.save()

            refresh = RefreshToken.for_user(account)
            res = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie('access', access_token, httponly=True)
            res.set_cookie('refresh', refresh_token, httponly=True)
            return res
        except KeyError:
            return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

# class SignupAccountsView(APIView):
#     def post(self, request):
#         serializer = AccountSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             if Account.objects.filter(email=serializer.validated_data['email']).exists():
#                 return JsonResponse({'message': '이미 존재하는 이메일'}, status=status.HTTP_200_OK)
#             account = serializer.save()
#
#             token = TokenObtainPairSerializer.get_token(account)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     'user': serializer.data,
#                     'message': '회원가입 성공',
#                     'token': {
#                         'access': access_token,
#                         'refresh': refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie('access', access_token, httponly=True)
#             res.set_cookie('refresh', refresh_token, httponly=True)
#
#             return res
#         return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)


class DuplicateView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        data = json.loads(request.body)
        try:
            req_userid = data['userId']
            if accounts.filter(userId=req_userid).exists():
                return JsonResponse({'isDuplicated': True, 'message': '아이디 중복'}, status=status.HTTP_200_OK)
            return JsonResponse({'isDuplicated': False, 'message': '아이디 사용 가능'}, status=status.HTTP_200_OK)
        except KeyError:
            return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

# class LoginAccountsView(APIView):
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             req_userid = data['userId']
#             if Account.objects.filter(userId=req_userid).exists():
#                 user = Account.objects.get(userId=req_userid)
#             if not bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
#                 return JsonResponse({'message': '아이디나 비밀번호가 틀림'}, status=status.HTTP_200_OK)
#             return JsonResponse({'message': '로그인 성공'}, status=status.HTTP_200_OK)
#         except KeyError:
#             return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAccountsView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        try:
            req_userid = data['userId']
            if Account.objects.filter(userId=req_userid).exists():
                user = Account.objects.get(userId=req_userid)
            if not bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                return JsonResponse({'message': '아이디나 비밀번호가 틀림'}, status=status.HTTP_200_OK)

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    'message': '로그인 성공',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie('access', access_token, httponly=True)
            response.set_cookie('refresh', refresh_token, httponly=True)
            return response
        except KeyError:
            return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAccountsView(APIView):
    def get(self, request):
        response = JsonResponse({
            'message': 'Logout success'
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


class HelloView(APIView):
    def get(self, request):
        return Response('hello')

class DetailAccountsView(APIView):
    def get(self, request, userId):
        try:
            account = get_object_or_404(Account, pk=userId)
            serializer = AccountDetailSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
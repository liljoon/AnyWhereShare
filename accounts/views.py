from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import AccountSignupSerializer
from .models import Account
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import json


class ListAccountsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSignupSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupAccountsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DuplicateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        accounts = Account.objects.all()
        data = json.loads(request.body)
        try:
            req_userid = data['userId']
            if accounts.filter(userId=req_userid).exists():
                return Response({'isDuplicated': True, 'message': '아이디 중복'}, status=status.HTTP_200_OK)
            return Response({'isDuplicated': False, 'message': '아이디 사용 가능'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAccountsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 유저 인증
        user = authenticate(
            userId=request.data.get("userId"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = AccountSignupSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutAccountsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        try:
            response = Response({
                "message": "로그아웃 성공"
                }, status=status.HTTP_200_OK)
            response.delete_cookie("access")
            response.delete_cookie("refresh")
            return response
        except:
            response = Response({
                "message": "로그아웃 실패"
                }, status=status.HTTP_400_BAD_REQUEST)
            return response



class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, {}!'.format(request.user.username)}
        return Response(content)

class DetailAccountsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, userId):
        try:
            account = get_object_or_404(Account, pk=userId)
            serializer = AccountSignupSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return JsonResponse({'message': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserDetailSerializer, UserLoginSerializer
from datetime import datetime, timedelta
from config import settings
import jwt


def jwt_auth(func):
    def wrap(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return Response({'error': '인증 실패'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            _, token = auth_header.split(' ')
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = decoded_payload
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': '유효하지 않은 토큰'}, status=status.HTTP_401_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)
    return wrap


class ListAccountsView(APIView):
    @jwt_auth
    def get(self, request):
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)


class DuplicateView(APIView):
    def get(self, request):
        userId = request.data.get('userId')
        if User.objects.filter(userId=userId).exists():
            return Response({'isDuplicated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'isDuplicated': False}, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        return Response({'message': '회원가입 실패'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        userId = request.data.get('userId')
        password = request.data.get('password')
        user = User.objects.filter(userId=userId, password=password).first()
        if not user:
            return Response({'message': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)

        # JWT Payload 생성
        payload = {
            'userId': user.userId,
            'exp': datetime.utcnow() + timedelta(minutes=30),  # 30분 뒤 만료
        }

        # JWT Token 발행
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token, 'message': '로그인 성공'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    @jwt_auth
    def get(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': '로그아웃 성공'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawalView(APIView):
    @jwt_auth
    def delete(self, request):
        userId = request.data.get('userId')
        user = User.objects.filter(userId=userId).first()
        if user:
            user.delete()
            return Response({'message': '회원탈퇴 성공'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '회원탈퇴 실패'}, status=status.HTTP_404_NOT_FOUND)

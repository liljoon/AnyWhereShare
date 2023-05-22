from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserDetailSerializer, UserLoginSerializer
from datetime import datetime, timedelta
from config import settings
import jwt, bcrypt


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

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            # upload to s3
            file_path = '.' + file_serializer.data.get('file')
            user = request.user
            data = s3_interface.upload_file(s3_interface.BUCKET, user.username, file_path, path+file_path.split('/')[-1])
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DuplicateView(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        if User.objects.filter(user_id=user_id).exists():
            return Response({'is_duplicated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'is_duplicated': False}, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        return Response({'message': '회원가입 실패'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response({'message': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({'message': '비밀번호 오류'}, status=status.HTTP_401_UNAUTHORIZED)
        # JWT Payload 생성
        payload = {
            'user_id': user.user_id,
            'exp': datetime.utcnow() + timedelta(minutes=30),  # 30분 뒤 만료
        }

        # JWT Token 발행
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token, 'message': '로그인 성공'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    @jwt_auth
    def get(self, request):
        try:
            response = Response({'message': '로그아웃 성공'}, status=status.HTTP_200_OK)
            response.delete_cookie('Authorization')
            return response
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawalView(APIView):
    @jwt_auth
    def delete(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response({'message': '회원탈퇴 실패'}, status=status.HTTP_404_NOT_FOUND)
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({'message': '비밀번호 오류'}, status=status.HTTP_401_UNAUTHORIZED)
        # JWT Payload 생성
        user.delete()
        return Response({'message': '회원탈퇴 성공'}, status=status.HTTP_200_OK)
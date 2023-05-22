from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from file.models import Resource
from account import views
from config import settings
import jwt
import boto3


def get_user_id(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        # 토큰이 만료되었을 경우 처리 로직
        return Response({'error': '만료된 토큰'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        # 유효하지 않은 토큰일 경우 처리 로직
        return Response({'error': '유효하지 않은 토큰'}, status=status.HTTP_401_UNAUTHORIZED)


class UploadView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
    )
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)

        file = request.FILES.get('file')
        path = request.data.get('path')
        if file:
            try:
                # 파일을 s3에 업로드
                self.s3_client.upload_fileobj(
                    file,
                    settings.S3_BUCKET_NAME,
                    user_id + path + "/" + file.name,
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '파일 업로드 실패'}, status=status.HTTP_400_BAD_REQUEST)

class DownloadView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
    )
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)

        file = request.FILES.get('file')
        path = request.data.get('path')
        if file:
            try:
                # 파일명만으로 업로드하면 파일명이 동일할 때 덮어쓰기 될 수 있으므로 uuid를 사용해 이름을 지정한다
                filename = str(uuid.uuid1()).replace('-', '')
                # 파일을 s3에 업로드
                self.s3_client.upload_fileobj(
                    file,
                    settings.S3_BUCKET_NAME,
                    user_id + path + "/" + file.name,
            )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '파일 업로드 실패'}, status=status.HTTP_400_BAD_REQUEST)
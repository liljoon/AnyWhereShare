from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from file.models import Resource
from account.models import User
from account import views
from config import settings
from datetime import datetime
import jwt
import boto3
from botocore.exceptions import ClientError
import os


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


            size = file.size
            resource_type = 'F'
            resource_name = os.path.splitext(file.name)[0] if resource_type == 'F' else file.name
            suffix_name = os.path.splitext(file.name)[1] if resource_type == 'F' else ''
            created_at = datetime.now()
            modified_at = datetime.now()
            user_account_id = User.objects.filter(user_id=user_id).first()

            # Split the path into individual parts
            path_parts = path.strip('/').split('/')

            parent_resource = None
            for part in path_parts:
                # Check if the folder already exists
                resource = Resource.objects.filter(user_account_id=user_account_id, resource_name=part, resource_type='D',
                                                   parent_resource_id=parent_resource).first()

                if resource:
                    # Folder already exists
                    parent_resource = resource
                else:
                    # Create a new folder
                    resource = Resource.objects.create(
                        parent_resource_id=parent_resource,
                        resource_name=part,
                        resource_type='D',
                        suffix_name='',
                        path=(f'{parent_resource.path}/' if parent_resource else '')+(parent_resource.resource_name if parent_resource else ''),  # Calculate the full path
                        is_bookmark=0,
                        is_valid=1,
                        created_at=created_at,
                        modified_at=modified_at,
                        size=0,
                        user_account_id=user_account_id
                    )
                    parent_resource = resource

            resource = Resource(
                parent_resource_id=parent_resource,
                resource_name=resource_name,
                resource_type=resource_type,
                suffix_name=suffix_name,
                path=(f'{parent_resource.path}/' if parent_resource else '')+(parent_resource.resource_name if parent_resource else ''),
                is_bookmark=0,
                is_valid=1,
                created_at=created_at,
                modified_at=modified_at,
                size=size,
                user_account_id=User.objects.filter(user_id=user_id).first()
            )
            resource.save()
            # Update the sizes of parent directories
            parent_resource = resource.parent_resource_id
            while parent_resource is not None:
                parent_resource.size += size
                parent_resource.save()
                parent_resource = parent_resource.parent_resource_id

            return Response({'message': '파일 업로드 성공'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': '파일 업로드 실패'}, status=status.HTTP_400_BAD_REQUEST)


class DownloadView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
    )

    @views.jwt_auth
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')

        if not path:
            return Response({'error': 'path 파라미터가 반드시 존재해야함'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = user_id + "/" + path
        print(file_path)
        if not self.s3_file_exists(file_path):
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        file = self.s3_download_file(file_path)
        if not file:
            return Response({'error': '다운로드 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = FileResponse(file)
        filename = os.path.basename(path)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response

    def s3_file_exists(self, file_path):
        try:
            self.s3_client.head_object(Bucket=settings.S3_BUCKET_NAME, Key=file_path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise

    def s3_download_file(self, file_path):
        try:
            response = self.s3_client.get_object(Bucket=settings.S3_BUCKET_NAME, Key=file_path)
            file = response['Body']
            return file
        except ClientError as e:
            return None
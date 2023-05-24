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
                    f'{user_id}/{path}{file.name}'
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

            # 폴더가 필요없는 루트디렉토리에 파일생성하는경우
            if '/' not in path:
                resource = Resource(
                    resource_name=resource_name,
                    resource_type=resource_type,
                    suffix_name=suffix_name,
                    is_bookmark=0,
                    is_valid=1,
                    created_at=created_at,
                    modified_at=modified_at,
                    size=size,
                    user_account_id=User.objects.filter(user_id=user_id).first()
                )
                resource.save()
                return Response({'message': '파일 업로드 성공'}, status=status.HTTP_201_CREATED)

            # 생성할 경로를 /기준으로 split
            path_parts = path.strip('/').split('/')
            parent_resource = None

            # 제일 최상위 폴더마다 순회
            for part in path_parts:
                # 폴더가 존재하는지 확인
                resource = Resource.objects.filter(user_account_id=user_account_id, resource_name=part, resource_type='D',
                                                   parent_resource_id=parent_resource).first()

                if resource:
                    # 이미 있으면 skip
                    parent_resource = resource
                else:
                    # 없으면 부모 폴더 생성
                    resource = Resource.objects.create(
                        parent_resource_id=parent_resource,
                        resource_name=part,
                        resource_type='D',
                        suffix_name='',
                        path=(parent_resource.path if parent_resource else '') +
                             (parent_resource.resource_name + '/' if parent_resource else ''),
                        is_bookmark=0,
                        is_valid=1,
                        created_at=created_at,
                        modified_at=modified_at,
                        size=0,
                        user_account_id=user_account_id
                    )
                    parent_resource = resource

            # 마지막 파일을 생성
            resource = Resource(
                parent_resource_id=parent_resource,
                resource_name=resource_name,
                resource_type=resource_type,
                suffix_name=suffix_name,
                path=(parent_resource.path if parent_resource else '') +
                     (parent_resource.resource_name + '/' if parent_resource else ''),
                is_bookmark=0,
                is_valid=1,
                created_at=created_at,
                modified_at=modified_at,
                size=size,
                user_account_id=User.objects.filter(user_id=user_id).first()
            )
            resource.save()

            # 부모 폴더도 저장
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
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

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


class DeleteView(APIView):
    @views.jwt_auth
    def delete(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

        # Split the path into directory, file name, and extension
        directory, file_name, extension = self._split_path(path)
        print(directory, file_name, extension)
        # Find the resource with the given path
        resource = Resource.objects.filter(path=directory,resource_name=file_name, suffix_name=extension,
                                           user_account_id=user_id, is_valid=1).first()

        if not resource:
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        # Soft delete the resource and all its sub-resources
        self._soft_delete_resource(resource)

        return Response({'message': '파일 삭제 성공'}, status=status.HTTP_200_OK)

    def _soft_delete_resource(self, resource):
        # Soft delete the resource by setting is_valid to 0
        resource.is_valid = 0
        resource.save()

        # Soft delete all the sub-resources recursively
        sub_resources = Resource.objects.filter(parent_resource_id=resource.resource_id)
        for sub_resource in sub_resources:
            self._soft_delete_resource(sub_resource)

    def _split_path(self, path):
        # path = "a/" -> directory="", file_name="a", extension=""
        # path = "a/b/c/test.txt" -> directory="a/b/c/", file_name="test", extension=".txt"
        # path = "test.txt" -> directory="", file_name"test", extension=".txt"
        parts = path.rstrip('/').split('/')
        directory = '/'.join(parts[:-1]) + '/' if len(parts) > 1 else ''
        file_name = parts[-1] if parts else ''
        extension = '.' + file_name.split('.')[-1] if '.' in file_name else ''
        file_name = file_name.split('.')[0] if extension else file_name
        return directory, file_name, extension

class ListFilesView(APIView):
    @views.jwt_auth
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the resource with the given path and user_id
        resource = Resource.objects.filter(path=path, is_valid=1, user_account_id=user_id).first()

        if not resource:
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        # Get all the sub-resources recursively
        sub_resources = self._get_sub_resources(resource)

        # Serialize the resources to JSON list
        serialized_data = self._serialize_resources(sub_resources)

        return Response(serialized_data, status=status.HTTP_200_OK)

    def _get_sub_resources(self, resource):
        # Get all the sub-resources recursively
        sub_resources = []
        self._get_sub_resources_recursive(resource, sub_resources)
        return sub_resources

    def _get_sub_resources_recursive(self, resource, sub_resources):
        # Add the resource to the sub-resources list if it is valid
        if resource.is_valid:
            sub_resources.append(resource)

        # Get the sub-resources recursively
        sub_resources_queryset = Resource.objects.filter(parent_resource_id=resource.id)
        for sub_resource in sub_resources_queryset:
            self._get_sub_resources_recursive(sub_resource, sub_resources)

    def _serialize_resources(self, resources):
        # Serialize the resources to JSON list
        serialized_data = []
        for resource in resources:
            serialized_data.append({
                'resource_id': resource.id,
                'resource_name': resource.resource_name,
                'resource_type': resource.resource_type,
                'suffix_name': resource.suffix_name,
                'path': resource.path,
                'is_bookmark': resource.is_bookmark,
                'is_valid': resource.is_valid,
                'created_at': resource.created_at,
                'modified_at': resource.modified_at,
                'size': resource.size,
                'user_account_id': resource.user_account_id.user_id,
            })
        return serialized_data
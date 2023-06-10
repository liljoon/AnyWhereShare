from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from file.models import Resource
from file.serializers import ResourceSerializer
from account.models import User
from account import views
from config import settings
from datetime import datetime
from botocore.exceptions import ClientError
import jwt
import boto3
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


def split_path(path):
    # path = "a/" -> directory="", file_name="a", extension=""
    # path = "a/b/c/test.txt" -> directory="a/b/c/", file_name="test", extension=".txt"
    # path = "test.txt" -> directory="", file_name"test", extension=".txt"
    parts = path.rstrip('/').split('/')
    directory = '/'.join(parts[:-1]) + '/' if len(parts) > 1 else ''
    file_name = parts[-1] if parts else ''
    extension = '.' + file_name.split('.')[-1] if '.' in file_name else ''
    file_name = file_name.split('.')[0] if extension else file_name
    return directory, file_name, extension


class NewFolderView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
    )
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)

        name = request.data.get('name')
        path = request.data.get('path')
        if name and path:
            if path == "/":
                path = ""
            try:
                # 파일을 s3에 업로드
                self.s3_client.put_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    Key=(f'{user_id}/{path}')
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            parent_resource = Resource.objects.filter(path=path, user_account_id=User.objects.filter(user_id=user_id).first()).first()
            resource = Resource(
                resource_name=name,
                resource_type='F',
                suffix_name='',
                is_bookmark=0,
                is_valid=1,
                created_at=datetime.now(),
                modified_at=datetime.now(),
                size=0,
                path=path,
                user_account_id=User.objects.filter(user_id=user_id).first(),
                parent_resource_id=parent_resource
            )
            resource.save()
            return Response({'message': '폴더 생성 성공'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': '파일 업로드 실패'}, status=status.HTTP_400_BAD_REQUEST)

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
        if not self._s3_file_exists(file_path):
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        file = self._s3_download_file(file_path)
        if not file:
            return Response({'error': '다운로드 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = FileResponse(file)
        filename = os.path.basename(path)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response

    def _s3_file_exists(self, file_path):
        try:
            self.s3_client.head_object(Bucket=settings.S3_BUCKET_NAME, Key=file_path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise

    def _s3_download_file(self, file_path):
        try:
            response = self.s3_client.get_object(Bucket=settings.S3_BUCKET_NAME, Key=file_path)
            file = response['Body']
            return file
        except ClientError as e:
            return Response({'error': '다운로드 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteView(APIView):
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

        # Split the path into directory, file name, and extension
        directory, file_name, extension = split_path(path)
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


class ListFilesView(APIView):
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
        elif path == '/':
            resources = Resource.objects.filter(path='', user_account_id=user_id)
        else:
            resources = Resource.objects.filter(path=path, user_account_id=user_id)

        if not resources:
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResourceSerializer(resources, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class ListTrashView(APIView):
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)

        resources = Resource.objects.filter(is_valid=0, user_account_id=user_id)

        if not resources:
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResourceSerializer(resources, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class RecoverView(APIView):
    @views.jwt_auth
    def post(self, request):
        resource_id = request.data.get('resource_id')

        if not resource_id:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

        resource = Resource.objects.filter(resource_id=resource_id).first()

        if not resource:
            return Response({'error': '해당 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        # Soft delete the resource and all its sub-resources
        self._recover_resource(resource)

        return Response({'message': '파일 삭제 성공'}, status=status.HTTP_200_OK)


    def _recover_resource(self, resource):
        # Soft delete the resource by setting is_valid to 0
        resource.is_valid = 1
        resource.save()

        # Soft delete all the sub-resources recursively
        sub_resources = Resource.objects.filter(parent_resource_id=resource.resource_id)
        for sub_resource in sub_resources:
            self._soft_delete_resource(sub_resource)


class RealDeleteView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
    )

    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')
        resource_id = request.data.get('resource_id')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
        if not resource_id:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the resource with the given path
        resource = Resource.objects.filter(resource_id=resource_id, is_valid=0).first()

        if not resource:
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        file_path = user_id + "/" + path

        # S3에서 파일을 삭제합니다.
        if not self._s3_delete_file(file_path):
            return Response({'error': '파일 삭제 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Soft delete the resource and all its sub-resources
        self._real_delete_resource(resource)

        return Response({'message': '파일 삭제 성공'}, status=status.HTTP_200_OK)

    def _s3_delete_file(self, file_path):
        try:
            self.s3_client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=file_path)
            return True
        except ClientError:
            return False

    def _real_delete_resource(self, resource):
        print(resource.resource_id)
        # Soft delete the resource by setting is_valid to 0
        resource.delete()


class SearchView(APIView):
    @views.jwt_auth
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        file_name = request.data.get('file_name')

        if not file_name:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)

        resources = Resource.objects.filter(resource_name__icontains=file_name, user_account_id=user_id)

        serializer = ResourceSerializer(resources, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class InfoView(APIView):
    @views.jwt_auth
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
        directory, file_name, extension = split_path(path)
        resource = Resource.objects.filter(path=directory, resource_name=file_name, suffix_name=extension,
                                           user_account_id=user_id, is_valid=1).first()

        if not resource:
            return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResourceSerializer(resource)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class ModifyView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY
    )
    @views.jwt_auth
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user_id = get_user_id(token)
        path = request.data.get('path')
        new_name = request.data.get('new_name')
        new_path = request.data.get('new_path')

        if not path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_name and not new_path:
            return Response({'error': '잘못된 요청'}, status=status.HTTP_400_BAD_REQUEST)
        elif new_name and not new_path:
            directory, file_name, extension = split_path(path)
            resource = Resource.objects.filter(path=directory, resource_name=file_name, suffix_name=extension,
                                               user_account_id=user_id, is_valid=1).first()
            if not resource:
                return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

            resource.resource_name = new_name.split('.')[0]
            resource.suffix_name = extension
            resource.modified_at = datetime.now()
            resource.save()

            try:
                self.s3_client.copy_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    CopySource={
                        'Bucket': settings.S3_BUCKET_NAME,
                        'Key': f'{user_id}/{path}'
                    },
                    Key=f'{user_id}/{directory}{new_name}'
                )
                self.s3_client.delete_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    Key=f'{user_id}/{path}'
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': '파일 이름변경 성공'}, status=status.HTTP_200_OK)
        elif not new_name and new_path:
            directory, file_name, extension = split_path(path)
            resource = Resource.objects.filter(path=directory, resource_name=file_name, suffix_name=extension,
                                               user_account_id=user_id, is_valid=1).first()
            if not resource:
                return Response({'error': '해당 경로의 파일이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

            parent_directory, parent_file_name, _ = split_path(new_path)
            parent_resource = Resource.objects.filter(path=parent_directory, resource_name=parent_file_name,
                                                      resource_type='D', user_account_id=user_id, is_valid=1).first()
            if not parent_resource: # 옮길 위치가 존재하지 않는 폴더일때
                return Response({'error': '해당 폴더는 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

            resource.path = new_path
            resource.parent_resource_id = parent_resource
            resource.modified_at = datetime.now()
            resource.save()

            try:
                self.s3_client.copy_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    CopySource={
                        'Bucket': settings.S3_BUCKET_NAME,
                        'Key': f'{user_id}/{path}'
                    },
                    Key=f'{user_id}/{new_path}{resource.resource_name}{resource.suffix_name}'
                )
                self.s3_client.delete_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    Key=f'{user_id}/{path}'
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': '파일 이동 성공'}, status=status.HTTP_200_OK)

import boto3
import json
from config import settings

S3 = boto3.client(
    's3',
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY,
    region_name='ap-northeast-2'
)
BUCKET = settings.S3_BUCKET_NAME


def list_path(bucket, user, path):
    files = []
    # get list
    objects = S3.list_objects(Bucket=bucket, Prefix='{}/{}'.format(user, path), Delimiter='/')

    # get sub directorys
    common_prefixes = objects.get('CommonPrefixes')
    if common_prefixes:
        for obj in common_prefixes:
            files.append({'type': 'directory', 'name': obj.get('Prefix').split('/')[-2]})

    # get files
    contents = objects.get('Contents')
    if contents:
        for obj in contents:
            file = obj.get('Key').split('/')[-1]
            if file != '':
                files.append({'type': 'file', 'name': file})

    return {'files': files}


def upload_file(user, file_obj, path):
    return S3.upload_file(file_obj, BUCKET, user + "/" + path)


def download_file(bucket, user, local_path, key):
    return S3.download_file(bucket, user + "/" + key, local_path)


def delete_path(bucket, user, path):
    return S3.delete_object(Bucket=bucket, Key=user + "/" + path)


def make_directory(bucket, user, path):
    return S3.put_object(Bucket=BUCKET, Key=user + "/" + path)


def move_file(bucket, user, old_path, new_path):
    S3.copy_object(Bucket=bucket, CopySource=bucket + "/" + user + "/" + old_path, Key=user + "/" + new_path)
    S3.delete_object(Bucket=bucket, Key=user + "/" + old_path)
    return


def copy_file(bucket, user, old_path, new_path):
    S3.copy_object(Bucket=bucket, CopySource=bucket + "/" + user + "/" + old_path, Key=user + "/" + new_path)
    return
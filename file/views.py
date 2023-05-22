from django.shortcuts import render
import boto3
from config import settings


def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_ACCESS_SECRET_KEY,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3


def get_list(prefix):
    response = s3.list_objects(Bucket=settings.S3_BUCKET_NAME, Prefix=prefix)
    contents_list = response['Contents']
    file_list = []
    for content in contents_list:
        key = content['Key']
        size = content['Size']
        file_list.append((key, size))
    # 파일명 출력
    for file in file_list:
        print(file)


if __name__ == "__main__":
    s3 = s3_connection()
    try:
        get_list('bigtog/')
        # s3.download_file(BUCKET_NAME, "test.txt", './help.txt')
        s3.put_object(Bucket=settings.S3_BUCKET_NAME, Key="bigtog/test")
    except Exception as e:
        print(e)
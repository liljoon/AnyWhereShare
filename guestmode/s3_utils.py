import boto3
from config.settings import get_secret

servicename = 's3'
region_name = get_secret("S3_REGION_NAME")
access_key = get_secret("S3_ACCESS_KEY")
secret_key = get_secret("S3_ACCESS_SECRET_KEY")
bucket_name= get_secret("S3_BUCKET_NAME")

s3 = boto3.client(servicename, region_name=region_name,\
                  aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def uploadFile(file, owner_passwd):
	s3.upload_fileobj(file, bucket_name, f'{owner_passwd}/{file.name}')

def generateDownloadUrl(file, owner_passwd):
	url = s3.generate_presigned_url(
		ClientMethod='get_object',
		Params={'Bucket': bucket_name, 'Key': f'{owner_passwd}/{file.name}'},
		ExpiresIn=600 # 10minute
		)
	return url

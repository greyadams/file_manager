from fastapi import UploadFile
from boto3 import client
from src.config import config

s3 = client('s3',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            endpoint_url=config.S3_ENDPOINT_URL)


def upload_to_s3(file: UploadFile):
    s3.upload_fileobj(file.file, 'files', file.filename)


def delete_from_s3(file_path: str):
    s3.delete_object(Bucket='files', Key=file_path)

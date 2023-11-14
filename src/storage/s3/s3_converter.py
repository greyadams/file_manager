from typing import List

from src.storage.connector import Storage, StorageRepository
from src import config
from boto3 import client


from src.storage.domain import DomainFile


class File:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename


class S3Storage(Storage):
    def __init__(self, name: str):
        self.name = name
        self.aws_access_key_id = config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        self.s3_endpoint_url = config.S3_ENDPOINT_URL
        self.s3 = client('s3', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                         endpoint_url=config.S3_ENDPOINT_URL)

    async def upload(self, file: File, bucket: str) -> str:

        self.s3.upload_fileobj(file, bucket, file.filename)
        # return self.s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': file.filename})
        return f"https://{bucket}.s3.amazonaws.com/{file.filename}"
    def delete_user_file(self, file: File, bucket: str):
        self.s3.delete_object(bucket, file.filename)

    def delete_files(self, files: List, bucket: str):
        for file in files:
            self.s3.delete_object(bucket, file)


class S3Repository(StorageRepository):
    def __init__(self, storage: S3Storage) -> None:
        self.storage = storage

    def convert(self, domain_file: DomainFile) -> File:
        return File(domain_file.file, domain_file.filename)

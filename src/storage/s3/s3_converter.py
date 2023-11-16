from typing import List, Any

from starlette.concurrency import run_in_threadpool

from src.storage.connector import Storage, StorageRepository
from src import config
from boto3 import client
from io import BytesIO
from src.storage.domain import DomainFile


class File:
    # def __init__(self, file: DomainFile = None):
    #     self.file = file.file
    #     self.filename = file.filename
    def __init__(self, domain_file: DomainFile):
        self.domain_file = domain_file
        self._file_buffer = BytesIO(domain_file.content)
        self.filename = domain_file.filename

    def read(self, size=-1):
        return self._file_buffer.read(size)

    def seek(self, offset, whence=0):
        return self._file_buffer.seek(offset, whence)


class S3Storage(Storage):
    def __init__(self, name: str):
        self.name = name
        self.aws_access_key_id = config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        self.s3_endpoint_url = config.S3_ENDPOINT_URL
        self.s3 = client('s3', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                         endpoint_url=config.S3_ENDPOINT_URL)

    def upload(self, file: File, bucket: str, file_name: str):
        file.seek(0)
        self.s3.upload_fileobj(file, bucket, file_name)
        # return self.s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': file.filename})

    def delete_user_file(self, file: File, bucket: str):
        self.s3.delete_object(bucket, file.filename)

    def delete_files(self, files: List, bucket: str):
        for file in files:
            self.s3.delete_object(bucket, file)


class S3Repository(StorageRepository):
    def __init__(self, storage: S3Storage) -> None:
        self.storage = storage

    def convert(self, domain_file: DomainFile) -> File:
        return File(domain_file)

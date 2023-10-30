from src.api.endpoints.router import DomainFile
from boto3 import client
from src import config
from src.storage.connector import Storage, StorageRepository
from src.storage.domain import File

s3 = client('s3',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            endpoint_url=config.S3_ENDPOINT_URL)


class S3Storage(Storage):
    def __init__(self, name: str):
        self.name = name
        self.aws_access_key_id = config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        self.s3_endpoint_url = config.S3_ENDPOINT_URL

    def upload(self, file: File, bucket: str) -> str:
        s3.upload_fileobj(file.file, 'files', file.filename)
        return s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': file.filename})

    def delete(self, file: File, bucket: str):
        s3.delete_fileobj(file.file, 'files', file.filename)


class S3Repository(StorageRepository):
    def __init__(self, storage: S3Storage) -> None:
        self.storage = storage

    def convert(self, domain_file: DomainFile) -> File:
        return File(file=domain_file.file, filename=domain_file.filename)

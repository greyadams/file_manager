import unittest
import boto3
from src.main_old import upload_to_s3

class TestS3FileUpload(unittest.TestCase):

    def setUp(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = 'your-test-bucket'
        self.test_file_path = 'path/to/your/test/file.txt'
        self.s3_key = 'test/file.txt'

    def test_upload_file(self):
        # Вызов функции для загрузки файла
        upload_to_s3(self.test_file_path, self.bucket_name, self.s3_key)

        # Проверка, что файл был загружен
        objects = self.s3.list_objects(Bucket=self.bucket_name, Prefix=self.s3_key)
        self.assertIn('Contents', objects)

        # Дополнительные проверки, например, сравнение содержимого файла

if __name__ == '__main__':
    unittest.main()
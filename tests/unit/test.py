import unittest
from fastapi.testclient import TestClient
from src.main_old import app

client = TestClient(app)


class TestFastAPIRoutes(unittest.TestCase):

    def test_upload_correct_user_file(self):
        with open("test.jpg", "rb") as f:
            response = client.post("/fss/v1/user123/file", files={"file": f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User file uploaded successfully")

    def test_invalid_file_format_user(self):
        with open("test.txt", "rb") as f:  # предполагается, что у вас есть файл test.txt в той же директории
            response = client.post("/fss/v1/user123/file", files={"file": f})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid file format.")

    def test_upload_product_file(self):
        with open("test.jpg", "rb") as f:  # предполагается, что у вас есть файл test.jpg в той же директории
            response = client.post("/fss/v1/user123/1/file", files={"file": f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Product file uploaded successfully")

    def test_delete_user_file(self):
        response = client.delete("/fss/v1/1/file/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User file deleted successfully")

    def test_delete_product_files(self):
        response = client.delete("/fss/v1/1/product/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product files deleted successfully", response.json()["message"])

    def test_delete_user_file_not_found(self):
        response = client.delete("/fss/v1/999/file/999")  # предполагается, что такого файла не существует
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User file not found")


if __name__ == '__main__':
    unittest.main()
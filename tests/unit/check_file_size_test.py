import unittest
from unittest.mock import Mock, patch
from fastapi import UploadFile, HTTPException

# Import functions from app for testing
from src.main_old import check_file_size


class TestCheckFileSize(unittest.TestCase):

    def test_check_file_size_valid(self):
        mock_upload_file = Mock(spec=UploadFile)
        mock_upload_file.size = 50
        self.assertTrue(check_file_size(mock_upload_file))

    def test_check_file_size_invalid(self):
        mock_upload_file = Mock(spec=UploadFile)
        mock_upload_file.size = 50 * 1024 * 1025
        with self.assertRaises(HTTPException):
            self.assertTrue(check_file_size(mock_upload_file))

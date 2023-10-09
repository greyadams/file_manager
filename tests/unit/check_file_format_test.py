import unittest
from unittest.mock import Mock, patch
from fastapi import UploadFile, HTTPException

# Import functions from app for testing
from src.main_old import check_file_format


class TestCheckFileFormat(unittest.TestCase):

    # Replace magic.Magic with Mock
    @patch('src.main.magic.Magic')
    def test_check_file_format_jpeg(self, MockedMagic):
        # Create a mock-instance of magic-object

        # return_value is using for setting a value, which will be returned by magic.Magic()
        # when it will be called.
        # return_value uses when we need to mock a method (not an attribute)
        instance = MockedMagic.return_value
        instance.from_buffer.return_value = 'image/jpeg'

        # Imitate the UploadFile()-object

        # Create mock - object of UploadFile - object
        mock_upload_file = Mock(spec=UploadFile)
        # Create mock - object of file
        mock_file_object = Mock()
        mock_file_object.read.return_value = b'fake_file_contents'
        mock_upload_file.file = mock_file_object

        # Check function (it should return True, because mock - file is jpeg)
        self.assertTrue(check_file_format(mock_upload_file))

    # Replace magic.Magic with Mock
    @patch('src.main.magic.Magic')
    def test_check_file_format_png(self, MockedMagic):
        # Create a mock-instance of magic-object

        # return_value is using for setting a value, which will be returned by magic.Magic()
        # when it will be called.
        instance = MockedMagic.return_value
        instance.from_buffer.return_value = 'image/png'

        # Imitate the UploadFile()-object

        # Create mock - object of UploadFile - object
        mock_upload_file = Mock(spec=UploadFile)

        # Create mock - object of file
        mock_file_object = Mock()
        mock_file_object.read.return_value = b'fake_file_contents'
        mock_upload_file.file = mock_file_object

        # Check function (it should return True, because mock - file is png)
        self.assertTrue(check_file_format(mock_upload_file))

    # Replace magic.Magic with Mock
    @patch('src.main.magic.Magic')
    def test_check_file_format_invalid_txt(self, MockedMagic):
        instance = MockedMagic.return_value
        instance.from_buffer.return_value = 'text/plain'
        mock_upload_file = Mock(spec=UploadFile)
        mock_file_object = Mock()
        mock_file_object.read.return_value = b'fake_file_contents'
        mock_upload_file.file = mock_file_object

        with self.assertRaises(HTTPException):
            self.assertTrue(check_file_format(mock_upload_file))
        # Check function (it should return False, because mock - file is plain)
        # self.assertFalse(check_file_format(mock_upload_file))

    @patch('src.main.magic.Magic')
    def test_check_file_format_invalid_video(self, MockedMagic):
        instance = MockedMagic.return_value
        instance.from_buffer.return_value = 'video/mp4'
        mock_upload_file = Mock(spec=UploadFile)
        mock_file_object = Mock()
        mock_file_object.read.return_value = b'fake_file_contents'
        mock_upload_file.file = mock_file_object

        with self.assertRaises(HTTPException):
            self.assertTrue(check_file_format(mock_upload_file))
        # Check function (it should return False, because mock - file is mp4)
        # self.assertFalse(check_file_format(mock_upload_file))

    @patch('src.main.magic.Magic')
    def test_check_file_format_invalid_image(self, MockedMagic):
        instance = MockedMagic.return_value
        instance.from_buffer.return_value = 'image/tiff'
        mock_upload_file = Mock(spec=UploadFile)
        mock_file_object = Mock()
        mock_file_object.read.return_value = b'fake_file_contents'
        mock_upload_file.file = mock_file_object

        with self.assertRaises(HTTPException):
            self.assertTrue(check_file_format(mock_upload_file))
        # Check function (it should return False, because mock - file is tiff)
        # self.assertFalse(check_file_format(mock_upload_file))

    @patch('src.main.magic.Magic')
    def test_check_file_format_invalid_json(self, MockedMagic):
        instance = MockedMagic.return_value
        instance.from_buffer.return_value = 'application/json'
        mock_upload_file = Mock(spec=UploadFile)
        mock_file_object = Mock()
        mock_file_object.read.return_value = b'fake_file_contents'
        mock_upload_file.file = mock_file_object

        with self.assertRaises(HTTPException):
            self.assertTrue(check_file_format(mock_upload_file))
        # Check function (it should return False, because mock - file is json)
        # self.assertFalse(check_file_format(mock_upload_file))


if __name__ == "__main__":
    unittest.main()

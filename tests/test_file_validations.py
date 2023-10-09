import pytest
from fastapi import HTTPException
from src.services.file_validations import FileValidations
from io import BytesIO

# Define the MockUploadFile class to mimic UploadFile
class MockUploadFile:
    def __init__(self, filename, content_type, size, file_data):
        self.filename = filename
        self.content_type = content_type
        self.size = size
        self._file_data = file_data

    def read(self):
        return self._file_data

# Function to create a valid image file
def valid_image_file():
    content_type = "image/jpeg"
    size = 1000
    file_data = b"Valid image content"

    return MockUploadFile(filename="valid_image.jpg", content_type=content_type, size=size, file_data=file_data)

# Function to create an invalid image file with unsupported format
def invalid_format_image_file():
    content_type = "application/pdf"
    size = 1000
    file_data = b"Invalid image content"

    return MockUploadFile(filename="invalid_image.pdf", content_type=content_type, size=size, file_data=file_data)

# Function to create an image file exceeding the size limit
def oversized_image_file():
    content_type = "image/jpeg"
    size = 60 * 1024 * 1024  # Exceeds the 50 MB limit
    file_data = b"Oversized image content"

    return MockUploadFile(filename="oversized_image.jpg", content_type=content_type, size=size, file_data=file_data)

# Test the check_file_format function
@pytest.mark.parametrize("file_fixture, expected_result", [
    (valid_image_file, True),  # Valid image format
    (invalid_format_image_file, HTTPException(status_code=400, detail="File format is not supported.")),  # Invalid format
])
def test_check_file_format(file_fixture, expected_result):
    if isinstance(expected_result, bool):
        assert FileValidations.check_file_format(file_fixture()) == expected_result
    else:
        with pytest.raises(HTTPException) as exc_info:
            FileValidations.check_file_format(file_fixture())
        assert exc_info.value.status_code == expected_result.status_code
        assert exc_info.value.detail == expected_result.detail

# Test the check_file_size function
@pytest.mark.parametrize("file_fixture, expected_result", [
    (valid_image_file, True),  # Valid size
    (oversized_image_file, HTTPException(status_code=400, detail="File size exceeds the limit of 50 MB.")),  # Oversized
])
def test_check_file_size(file_fixture, expected_result):
    if isinstance(expected_result, bool):
        assert FileValidations.check_file_size(file_fixture()) == expected_result
    else:
        with pytest.raises(HTTPException) as exc_info:
            FileValidations.check_file_size(file_fixture())
        assert exc_info.value.status_code == expected_result.status_code
        assert exc_info.value.detail == expected_result.detail

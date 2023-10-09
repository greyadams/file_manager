from fastapi import UploadFile, HTTPException
import magic


class FileValidations:

    @staticmethod
    def check_file_format(upload_file: UploadFile):
        mime = magic.Magic()
        contents = upload_file.file.read()
        upload_file.file.seek(0)
        file_type = mime.from_buffer(contents)
        if file_type not in ['image/jpeg', 'image/png']:
            raise HTTPException(status_code=400, detail="File format is not supported.")
        return True

    @staticmethod
    def check_file_size(file: UploadFile):
        if file.size > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds the limit of 50 MB.")
        return True

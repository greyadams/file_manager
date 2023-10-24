from fastapi import APIRouter, UploadFile, File, Path, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.services.file_services import upload_file, delete_user_file, delete_product_files
from src.services.s3_services import upload_to_s3, delete_from_s3
from src.database import SessionLocal, get_db
from src.database.psql.repository import PostgresRepository
from datetime import datetime
import magic

router = APIRouter()


class DomainFile:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename



def upload_file_to_domain_file(file: UploadFile) -> DomainFile:
    return DomainFile(file.file, file.filename)


def upload_file_to_domain_meta_data(file: UploadFile, user_id: int, file_path: str, product_id: int = None) -> DomainMetaData:
    return DomainMetaData(user_id, product_id, file.filename, file_path)


class FileValidations:

    @staticmethod
    def check_file_format(file: UploadFile):
        mime = magic.Magic()
        contents = file.file.read()
        file.file.seek(0)
        file_type = mime.from_buffer(contents)
        if file_type not in ['image/jpeg', 'image/png']:
            raise HTTPException(status_code=400, detail="File format is not supported.")
        return True

    @staticmethod
    def check_file_size(file: UploadFile):
        if file.size > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds the limit of 50 MB.")
        return True


@router.post("/fss/v1/{user_id}/file")
async def upload_user_file(user_id: int = Path(...), file: UploadFile = File(...)):
    if FileValidations.check_file_format(file) and FileValidations.check_file_size(file):
        domain_file = upload_file_to_domain_file(file)
        if upload_to_s3(domain_file):
            file_path = f'http://localhost:9000/files/{domain_file.filename}'
        else:
            raise HTTPException(status_code=404, detail="Failed to upload file to S3")

        metadata = upload_file_to_domain_meta_data(file, user_id, file_path)
        if PostgresRepository.upload_file_to_db(metadata):
            return JSONResponse(content={"message": "User file uploaded successfully", "url": file_path})
        else:
            raise HTTPException(status_code=404, detail="Failed to upload file to DB")

###Пример хэндлера как класса
# from fastapi import APIRouter, Depends, HTTPException, Path, File, UploadFile
#
# router = APIRouter()
#
# class UserFileHandler:
#
#     def __init__(self, user_id: int = Path(...), file: UploadFile = File(...)):
#         self.user_id = user_id
#         self.file = file
#
#     def validate_file(self):
#         return FileValidations.check_file_format(self.file) and FileValidations.check_file_size(self.file)
#
#     def upload_file(self):
#         if self.validate_file():
#             domain_file = upload_file_to_domain_file(self.file)
#             if upload_to_s3(domain_file):
#                 return f'http://localhost:9000/files/{domain_file.filename}'
#             else:
#                 raise HTTPException(status_code=404, detail="Failed to upload file to S3")
#
#     def upload_metadata_to_db(self, file_path):
#         metadata = upload_file_to_domain_meta_data(self.file, self.user_id, file_path)
#         if PostgresRepository.upload_file_to_db(metadata):
#             return True
#         else:
#             raise HTTPException(status_code=404, detail="Failed to upload file to DB")
#
# @router.post("/fss/v1/{user_id}/file")
# async def upload_user_file(handler: UserFileHandler = Depends(UserFileHandler)):
#     file_path = handler.upload_file()
#     if handler.upload_metadata_to_db(file_path):
#         return {"message": "User file uploaded successfully", "url": file_path}


@router.post("/fss/v1/{user_id}/{product_id}/file")
async def upload_product_file(user_id: int = Path(...), product_id: int = Path(...), file: UploadFile = File(...),
                              db: SessionLocal = Depends(get_db)):
    # Validation
    # Convert request to DomainFile and call upload file service.
    # Return and handle errors
    # Check mb better to make handlers like class methods!
    check_file_format(file)
    check_file_size(file)
    upload_to_s3(file)
    upload_file(db, user_id, product_id, file.filename)

    public_url = f'http://localhost:9000/files/{file.filename}'
    return JSONResponse(content={"message": "Product file uploaded successfully", "url": public_url})


@router.delete("/fss/v1/{user_id}/file/{file_id}")
async def delete_user_file(user_id: int = Path(...), file_id: int = Path(...), session: SessionLocal = Depends(get_db)):
    file_info = delete_user_file(session, user_id, file_id)

    if file_info:
        return JSONResponse(content={"message": "User file deleted successfully"})

    return JSONResponse(content={"message": "User file not found"})


@router.delete("/fss/v1/{user_id}/product/{product_id}")
async def delete_product_files(user_id: int = Path(...), product_id: int = Path(...),
                               session: SessionLocal = Depends(get_db)):
    files_to_delete = delete_product_files(session, user_id, product_id)
    if files_to_delete:
        return JSONResponse(content={"message": f"{len(files_to_delete)} Product files deleted successfully"})

    return JSONResponse(content={"message": "Product files not found"})

from fastapi import APIRouter, UploadFile, File, Path, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.database.domain import DomainMetaData
from src.services.file_services import upload_file, delete_user_file, delete_product_files
import magic

from src.storage.domain import DomainFile

router = APIRouter()


def file_to_domain_file(file: UploadFile = None, filename: str = None) -> DomainFile:
    if file is None:
        return DomainFile(None, filename)
    return DomainFile(file.file, file.filename)


def file_to_domain_meta_data(user_id: int, filename: str = None, file: UploadFile = None,
                             product_id: int = None) -> DomainMetaData:
    if file is None:
        return DomainMetaData(user_id, filename, product_id)
    return DomainMetaData(user_id, file.filename, product_id)


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
    FileValidations.check_file_format(file)
    FileValidations.check_file_size(file)
    if FileValidations.check_file_format(file) and FileValidations.check_file_size(file):
        domain_file = file_to_domain_file(file)
        domain_meta_data = file_to_domain_meta_data(user_id, None, file)

        if isinstance(upload_file(domain_meta_data, domain_file), str):
            return JSONResponse(content={"message": "User file uploaded successfully",
                                         "url": upload_file(domain_meta_data, domain_file)})
        else:
            raise HTTPException(status_code=404, detail="Failed to upload file")


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
async def upload_product_file(user_id: int = Path(...), product_id: int = Path(...), file: UploadFile = File(...)):
    FileValidations.check_file_format(file)
    FileValidations.check_file_size(file)
    if FileValidations.check_file_format(file) and FileValidations.check_file_size(file):
        domain_file = file_to_domain_file(file)
        domain_meta_data = file_to_domain_meta_data(user_id, file.filename, file, product_id)

        if isinstance(upload_file(domain_meta_data, domain_file), str):
            return JSONResponse(content={"message": "Product file uploaded successfully",
                                         "url": upload_file(domain_meta_data, domain_file)})
        else:
            raise HTTPException(status_code=404, detail="Failed to upload product file")
    # Validation
    # Convert request to DomainFile and call upload file service.
    # Return and handle errors
    # Check mb better to make handlers like class methods!
    # check_file_format(file)
    # check_file_size(file)
    # upload_to_s3(file)
    # upload_file(db, user_id, product_id, file.filename)
    #
    # public_url = f'http://localhost:9000/files/{file.filename}'
    # return JSONResponse(content={"message": "Product file uploaded successfully", "url": public_url})
    #


@router.delete("/fss/v1/{user_id}/file/{file_id}")
async def delete_user_file(user_id: int = Path(...), filename: str = Path(...)):
    domain_meta_data = file_to_domain_meta_data(user_id, filename)
    domain_file = file_to_domain_file(None, filename)

    result = await delete_user_file(domain_meta_data, domain_file)

    if result:
        return JSONResponse(content={"message": "User file deleted successfully"})
    return JSONResponse(content={"message": "User file not found"})


@router.delete("/fss/v1/{user_id}/product/{product_id}")
async def delete_product_files(user_id: int = Path(...), product_id: int = Path(...)):
    domain_meta_data = file_to_domain_meta_data(user_id, None, None, product_id)
    result = await delete_product_files(domain_meta_data)
    # files_to_delete = delete_product_files(session, user_id, product_id)
    if result:
        return JSONResponse(content={"message": f"{len(str(result))} Product files deleted successfully"})
    return JSONResponse(content={"message": "Product files not found"})

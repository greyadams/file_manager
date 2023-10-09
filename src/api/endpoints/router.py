from fastapi import APIRouter, UploadFile, File, Path, Depends
from fastapi.responses import JSONResponse
from src.services.file_services import upload_file, delete_user_file, delete_product_files
from src.services.file_validations import check_file_format, check_file_size
from src.services.s3_services import upload_to_s3, delete_from_s3
from src.database import SessionLocal, get_db

router = APIRouter()


@router.post("/fss/v1/{user_id}/file")
async def upload_user_file(user_id: str = Path(...), file: UploadFile = File(...), db: SessionLocal = Depends(get_db)):
    check_file_format(file)
    check_file_size(file)
    upload_to_s3(file)
    upload_file(db, user_id, file.filename)

    public_url = f'http://localhost:9000/files/{file.filename}'
    return JSONResponse(content={"message": "User file uploaded successfully", "url": public_url})


@router.post("/fss/v1/{user_id}/{product_id}/file")
async def upload_product_file(user_id: int = Path(...), product_id: int = Path(...), file: UploadFile = File(...),
                              db: SessionLocal = Depends(get_db)):
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

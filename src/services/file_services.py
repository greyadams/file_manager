from fastapi import UploadFile
from src.database import SessionLocal
from src.services.s3_services import upload_to_s3, delete_from_s3
from src.models.models import FileData


def upload_file(session: SessionLocal, file: UploadFile, user_id, filename, product_id=None):
    # upload_to_s3(file) -- возможно нужно разделить функции по работе с бд и файловым хранилищем.
    db_file = FileData(user_id=user_id, filename=filename, file_path=filename, product_id=product_id)
    session.add(db_file)
    session.commit()


def delete_user_file(session: SessionLocal, user_id: int, file_id: int):
    file_info = session.query(FileData).filter_by(id=file_id, user_id=user_id).first()
    if file_info:
        delete_from_s3(file_info.file_path)
        session.delete(file_info)
        session.commit()
        return file_info
    return None


def delete_product_files(session: SessionLocal, user_id: int, product_id: int):
    files_to_delete = session.query(FileData).filter_by(user_id=user_id, product_id=product_id).all()
    deleted_count = session.query(FileData).filter_by(user_id=user_id, product_id=product_id).delete()

    if deleted_count > 0:
        for file_info in files_to_delete:
            delete_from_s3(file_info.file_path)
        session.commit()
        return deleted_count
    return None

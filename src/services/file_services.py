from fastapi import UploadFile
from src.db import SessionLocal
from src.database.psql.repository import DomainMetaData, PostgresRepository
from src.services.s3_services import delete_from_s3


def upload_file_to_db(domain_metadata: DomainMetaData, session: SessionLocal):
    # upload_to_s3(file) -- возможно нужно разделить функции по работе с бд и файловым хранилищем.
    db_file = PostgresRepository.domain_meta_data_to_file_data(domain_metadata)
    session.add(db_file)
    session.commit()

def upload_file_v2(database, storage, DomainFile):
    database.upload(DomainFile.metadata())
    storage.upload(DomainFile.data())
    try:
        database
    except:
        database

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

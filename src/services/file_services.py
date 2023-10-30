from src.database.domain import DomainMetaData
from src.database.psql.repository import PostgresRepository, PostgresDatabase
from sqlalchemy import text

from src.services.s3_services import S3Storage, S3Repository
from src.storage.domain import DomainFile


def upload_file(domain_meta_data: DomainMetaData,
                repository: PostgresRepository,
                database: PostgresDatabase,
                domain_file: DomainFile,
                storage: S3Storage,
                storage_repository: S3Repository,
                ) -> str:
    # Connect to db
    database.connect()

    # Convert DomainMetaData to FileData
    file_data = repository.convert(domain_meta_data)

    file = storage_repository.convert(domain_file)
    url = storage.upload(file, 'files')
    # First realization of function (with query and exec)

    query = str(text(
        "INSERT INTO file_data (user_id, product_id, filename, file_path, created_at) VALUES (:user_id, :product_id, :filename, :file_path, :created_at)"))
    params = {
        "user_id": file_data.user_id,
        "product_id": file_data.product_id,
        "filename": file_data.filename,
        "file_path": url,
        "created_at": file_data.created_at
    }
    # Выполняем запрос с использованием метода exec
    database.exec(query, params)

    # Second realization of function (without query and exec)

    # Add file_data into session and commit it
    database.session.add(file_data)
    database.session.commit()

    # Отключаемся от базы данных
    database.disconnect()
    return url


# def upload_file_v2(database, storage, DomainFile):
#     database.upload(DomainFile.metadata())
#     storage.upload(DomainFile.data())
#     try:
#         database
#     except:
#         database

# def delete_user_file(session: SessionLocal, user_id: int, file_id: int):
#     file_info = session.query(FileData).filter_by(id=file_id, user_id=user_id).first()
#     if file_info:
#         delete_from_s3(file_info.file_path)
#         session.delete(file_info)
#         session.commit()
#         return file_info
#     return None

def delete_file_from_db(domain_meta_data: DomainMetaData, repository: PostgresRepository, database: PostgresDatabase):
    # Connect to db
    database.connect()
    # Convert DomainMetaData to FileData
    user_id = domain_meta_data.user_id
    product_id = domain_meta_data.product_id

    # SQL-запрос для удаления записей на основе user_id и product_id
    query = str(text("DELETE FROM file_data WHERE user_id = :user_id AND product_id = :product_id"))
    params = {
        "user_id": user_id,
        "product_id": product_id
    }

    # Выполняем запрос с использованием метода exec
    database.exec(query, params)
# def delete_product_files(session: SessionLocal, user_id: int, product_id: int):
#     files_to_delete = session.query(FileData).filter_by(user_id=user_id, product_id=product_id).all()
#     deleted_count = session.query(FileData).filter_by(user_id=user_id, product_id=product_id).delete()
#
#     if deleted_count > 0:
#         for file_info in files_to_delete:
#             delete_from_s3(file_info.file_path)
#         session.commit()
#         return deleted_count
#     return None

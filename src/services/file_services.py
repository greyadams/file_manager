from src.database.domain import DomainMetaData
from src.database.psql.repository import PostgresRepository, PostgresDatabase
from sqlalchemy import text

from src.storage.s3.s3_converter import S3Storage, S3Repository
from src.storage.domain import DomainFile
from src import config


def upload_file(domain_meta_data: DomainMetaData,
                domain_file: DomainFile,
                ) -> str:
    # Connect to db
    database = PostgresDatabase(config.DATABASE_URL)
    database.connect()

    # Convert DomainMetaData to FileData
    repository = PostgresRepository(database)
    file_data = repository.convert(domain_meta_data)

    # Storage operations
    storage = S3Storage(config.S3_BUCKET)
    storage_repository = S3Repository(storage)
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

def delete_user_file(domain_meta_data: DomainMetaData, domain_file: DomainFile):
    # Connect to db
    database = PostgresDatabase(config.DATABASE_URL)
    database.connect()

    # Convert DomainMetaData to FileData
    repository = PostgresRepository(database)
    file_data = repository.convert(domain_meta_data)
    user_id = file_data.user_id
    product_id = file_data.product_id
    # Storage operations
    storage = S3Storage(config.S3_BUCKET)
    storage_repository = S3Repository(storage)
    file = storage_repository.convert(domain_file)
    storage.delete_user_file(file, 'files')

    # SQL-запрос для удаления записей на основе user_id и product_id
    query = str(text("DELETE FROM file_data WHERE user_id = :user_id AND product_id = :product_id"))
    params = {
        "user_id": user_id,
        "product_id": product_id
    }

    # Выполняем запрос с использованием метода exec
    database.exec(query, params)
    return True


def get_product_files(domain_meta_data: DomainMetaData):
    # Connect to db
    database = PostgresDatabase(config.DATABASE_URL)
    database.connect()

    repository = PostgresRepository(database)
    file_data = repository.convert(domain_meta_data)
    user_id = file_data.user_id
    product_id = file_data.product_id

    query = str(text("SELECT filename FROM file_data WHERE user_id = :user_id AND product_id = :product_id"))
    params = {
        "user_id": user_id,
        "product_id": product_id
    }
    results = database.session.exec(query, params).all()
    filename_list = []
    for row in results:
        filename_list.append({'filename': row[0]})
    return filename_list


def delete_product_files(domain_meta_data: DomainMetaData):
    storage = S3Storage(config.S3_BUCKET)
    file_to_delete = get_product_files(domain_meta_data)
    storage.delete_files(file_to_delete, 'files')
    return file_to_delete
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

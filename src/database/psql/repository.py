from src.database.psql.models.models import FileData
from datetime import datetime


class DomainMetaData:
    def __init__(self, user_id, product_id, filename, file_path):
        self.user_id = user_id
        self.product_id = product_id
        self.filename = filename
        self.file_path = file_path
        self.created_at = datetime.now()


class PostgresRepository:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

    @staticmethod
    def domain_meta_data_to_file_data(domain_meta_data: DomainMetaData) -> FileData:
        return FileData(
            user_id=domain_meta_data.user_id,
            product_id=domain_meta_data.product_id,
            filename=domain_meta_data.filename,
            file_path=domain_meta_data.file_path,
            created_at=domain_meta_data.created_at
        )


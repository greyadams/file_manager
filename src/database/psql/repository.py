from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.psql.models.models import FileData
from src.database.domain import DomainMetaData
from src.database.connector import Database, Repository


class PostgresDatabase(Database):
    def __init__(self, url: str) -> None:
        self.url = url
        self.engine = None
        self.SessionLocal = None
        self.session = None

    def connect(self):
        self.engine = create_engine(self.url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.SessionLocal()

    def disconnect(self):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()

    def exec(self, query: str, params: Any = None):
        # Реализация выполнения SQL-запроса (пример)
        self.session.execute(query, params)
        self.session.commit()


class PostgresRepository(Repository):
    def __init__(self, database: PostgresDatabase) -> None:
        self.database = database

    def convert(self, domain_meta_data: DomainMetaData) -> FileData:
        return FileData(
            user_id=domain_meta_data.user_id,
            product_id=domain_meta_data.product_id,
            filename=domain_meta_data.filename,
            file_path=domain_meta_data.file_path,
            created_at=domain_meta_data.created_at
        )

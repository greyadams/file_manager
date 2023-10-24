from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class FileData(Base):
    __tablename__ = 'FileData'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    product_id = Column(Integer, index=True, nullable=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

from fastapi import FastAPI, UploadFile, File, HTTPException, Path
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from boto3 import client
import magic
from sqlalchemy import create_engine, Column, Integer, String, MetaData, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class FileData(Base):
    __tablename__ = 'FileData'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    product_id = Column(Integer, index=True, nullable=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


# Подключение к базе данных PostgreSQL
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(DATABASE_URL)

# Создаем все несуществующие таблицы
Base.metadata.create_all(bind=engine)


def check_file_format(upload_file: UploadFile):
    mime = magic.Magic()
    contents = upload_file.file.read()
    upload_file.file.seek(0)  # Возвращаем указатель обратно на начало файла, если его нужно будет снова читать
    file_type = mime.from_buffer(contents)
    if file_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=400, detail="File format is not supported.")
    return True


def check_file_size(file: UploadFile):
    if file.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 50 MB.")
    return True


def upload_to_s3(file: UploadFile):
    s3.upload_fileobj(file.file, 'files', file.filename)


def add_file_to_db(user_id, filename, product_id=None):
    new_file = FileData(user_id=user_id, filename=filename, file_path=filename, product_id=product_id)
    session.add(new_file)
    session.commit()


app = FastAPI()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

s3 = client('s3',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            endpoint_url='http://localhost:9000')


@app.post("/fss/v1/{user_id}/file")
async def upload_user_file(user_id: str = Path(...), file: UploadFile = File(...)):
    check_file_format(file)
    check_file_size(file)
    upload_to_s3(file)
    add_file_to_db(user_id, file.filename)

    public_url = f'http://localhost:9000/files/{file.filename}'
    return JSONResponse(content={"message": "User file uploaded successfully", "url": public_url})


@app.post("/fss/v1/{user_id}/{product_id}/file")
async def upload_product_file(user_id: int = Path(...), product_id: int = Path(...), file: UploadFile = File(...)):
    check_file_format(file)
    check_file_size(file)
    upload_to_s3(file)
    add_file_to_db(user_id, file.filename, product_id)

    public_url = f'http://localhost:9000/files/{file.filename}'
    return JSONResponse(content={"message": "Product file uploaded successfully", "url": public_url})


# Роут для удаления файла пользователя
@app.delete("/fss/v1/{user_id}/file/{file_id}")
async def delete_user_file(user_id: int = Path(...), file_id: int = Path(...)):
    # Получаем информацию о файле из базы данных
    file_info = session.query(FileData).filter_by(id=file_id, user_id=user_id).first()

    if file_info:
        # Удаляем файл из хранилища S3
        s3.delete_object(Bucket='files', Key=file_info.file_path)

        # Удаляем запись из базы данных
        session.delete(file_info)  # Изменено
        session.commit()

        return JSONResponse(content={"message": "User file deleted successfully"})

    return JSONResponse(content={"message": "User file not found"})


# Роут для удаления файла продукта
@app.delete("/fss/v1/{user_id}/product/{product_id}")
async def delete_product_files(user_id: int = Path(...), product_id: int = Path(...)):
    try:
        # Удаление всех записей, которые соответствуют условиям
        deleted_count = session.query(FileData).filter_by(user_id=user_id, product_id=product_id).delete()

        if deleted_count > 0:
            # Здесь можно добавить код для удаления соответствующих файлов из S3, если это необходимо
            session.commit()
            return JSONResponse(content={"message": f"{deleted_count} Product files deleted successfully"})
        else:

            return JSONResponse(content={"message": "Product files not found", "deleted_count": deleted_count})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

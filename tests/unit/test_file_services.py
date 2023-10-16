import pytest
from unittest.mock import Mock

from fastapi import UploadFile
from src.models.models import FileData
from src.database import SessionLocal, Base, engine
from src.services.file_services import upload_file, delete_user_file, delete_product_files


@pytest.fixture(scope="session", autouse=True)
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def create_test_file(db_session, user_id, file_id):
    test_file = FileData(id=file_id, user_id=user_id, filename=f'test_file_{file_id}.txt',
                         file_path=f'path/to/test_file_{file_id}.txt')
    db_session.add(test_file)
    db_session.commit()


@pytest.mark.parametrize(
    "user_id, filename, product_id, expected",
    [
        (1, 'test.txt', 2, {'user_id': 1, 'filename': 'test.txt', 'product_id': 2}),
        (2, 'file2.txt', None, {'user_id': 2, 'filename': 'file2.txt', 'product_id': None}),
        (3, 'file3.txt', 3, {'user_id': 3, 'filename': 'file3.txt', 'product_id': 3})
    ]
)
def test_upload_file(mocker, db_session, user_id, filename, product_id, expected):
    mock_upload_file = mocker.MagicMock(spec=UploadFile)
    mock_upload_file.file = filename
    mock_upload_file.filename = Mock(return_value=b'test.txt')
    upload_file(db_session, mock_upload_file, user_id, filename, product_id)

    db_file = db_session.query(FileData).filter_by(user_id=user_id, filename=filename, product_id=product_id).first()
    assert db_file is not None
    assert db_file.user_id == expected['user_id']
    assert db_file.filename == expected['filename']
    assert db_file.product_id == expected['product_id']


@pytest.mark.parametrize("user_id, file_id", [(1, 1), (2, 2), (3, 3)])
def test_delete_user_file(db_session, user_id, file_id):
    deleted_file = delete_user_file(db_session, user_id, file_id)
    assert deleted_file is not None

    db_file = db_session.query(FileData).filter_by(id=file_id, user_id=user_id).first()
    assert db_file is None


@pytest.mark.parametrize("user_id, file_id", [(1, 1), (2, 2), (3, 3)])
def test_delete_user_file(db_session, user_id, file_id):
    # Создание тестовых данных
    create_test_file(db_session, user_id, file_id)

    # Проверка, что данные действительно добавлены
    assert db_session.query(FileData).filter_by(id=file_id, user_id=user_id).first() is not None

    # Тестирование функции удаления
    deleted_file = delete_user_file(db_session, user_id, file_id)
    assert deleted_file is not None

    # Проверка, что данные удалены
    assert db_session.query(FileData).filter_by(id=file_id, user_id=user_id).first() is None

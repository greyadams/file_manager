import unittest
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import config  # Замените "your_module" на актуальное имя вашего модуля
class TestGetDB(unittest.TestCase):

    def setUp(self):
        # Создаем временную базу данных для тестов
        self.engine = create_engine('sqlite:///:memory:')
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def tearDown(self):
        # Очищаем ресурсы после завершения теста
        self.engine.dispose()

    def test_get_db(self):
        # Создаем мок объект для вашего конфига
        config.DATABASE_URL = 'sqlite:///:memory:'  # Устанавливаем временную базу данных для теста
        mock_config = Mock()
        mock_config.DATABASE_URL = config.DATABASE_URL

        # Меняем импорт config на мок объект
        with unittest.mock.patch('src.config.config', mock_config):
            from src.database import get_db  # Замените "your_module" на актуальное имя вашего модуля

            # Вызываем функцию get_db
            db = get_db()

            # Проверяем, что db не равно None
            self.assertIsNotNone(db)

            # Закрываем сессию базы данных
            db.close()

if __name__ == '__main__':
    unittest.main()
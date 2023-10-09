import unittest
from unittest.mock import Mock
from src.models.models import FileData
from src.services.file_services import upload_file, delete_user_file, delete_product_files  # Замените "your_module" на актуальное имя вашего модуля

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        # Создаем мок объект для сессии
        self.session = Mock()

    def test_upload_file(self):
        # Задаем параметры для функции upload_file
        user_id = 1
        filename = "example.txt"
        product_id = 2
        file = Mock()

        # Вызываем функцию upload_file
        upload_file(self.session, file, user_id, filename, product_id)

        # Проверяем, что вызывается upload_to_s3
        self.session.upload_to_s3.assert_called_once_with(file)

        # Проверяем, что создается объект FileData и добавляется в сессию
        self.session.add.assert_called_once_with(FileData(user_id=user_id, filename=filename, file_path=filename, product_id=product_id))
        self.session.commit.assert_called_once()

    def test_delete_user_file(self):
        # Задаем параметры для функции delete_user_file
        user_id = 1
        file_id = 2
        file_info = Mock()
        file_info.file_path = "example.txt"

        # Мокируем query и filter_by
        self.session.query.return_value.filter_by.return_value.first.return_value = file_info

        # Вызываем функцию delete_user_file
        result = delete_user_file(self.session, user_id, file_id)

        # Проверяем, что вызывается delete_from_s3 и объект удаляется из сессии
        self.session.delete.assert_called_once_with(file_info)
        self.session.commit.assert_called_once()
        self.session.delete_from_s3.assert_called_once_with(file_info.file_path)

        # Проверяем, что функция возвращает ожидаемый результат
        self.assertEqual(result, file_info)

    def test_delete_product_files(self):
        # Задаем параметры для функции delete_product_files
        user_id = 1
        product_id = 2
        file_info1 = Mock()
        file_info1.file_path = "file1.txt"
        file_info2 = Mock()
        file_info2.file_path = "file2.txt"
        files_to_delete = [file_info1, file_info2]

        # Мокируем query и filter_by
        self.session.query.return_value.filter_by.return_value.all.return_value = files_to_delete
        self.session.query.return_value.filter_by.return_value.delete.return_value = len(files_to_delete)

        # Вызываем функцию delete_product_files
        result = delete_product_files(self.session, user_id, product_id)

        # Проверяем, что вызывается delete_from_s3 для каждого файла и объекты удаляются из сессии
        self.session.delete.assert_has_calls([unittest.mock.call(file_info1), unittest.mock.call(file_info2)])
        self.session.commit.assert_called_once()
        self.session.delete_from_s3.assert_has_calls([unittest.mock.call(file_info1.file_path), unittest.mock.call(file_info2.file_path)])

        # Проверяем, что функция возвращает ожидаемый результат
        self.assertEqual(result, len(files_to_delete))

if __name__ == '__main__':
    unittest.main()

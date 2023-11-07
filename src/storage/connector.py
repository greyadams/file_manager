from abc import ABC, abstractmethod
from typing import Any


class Storage(ABC):
    @abstractmethod
    def upload(self, file: Any, bucket: str):
        pass

    @abstractmethod
    def delete_user_file(self, file: Any, bucket: str):
        pass

    @abstractmethod
    def delete_files(self, files: Any, bucket: str):
        pass


class StorageRepository(ABC):
    @abstractmethod
    def convert(self, storage: str):
        pass

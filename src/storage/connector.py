from abc import ABC, abstractmethod
from typing import Any


class Storage(ABC):
    @abstractmethod
    def upload(self, file: Any, bucket: str):
        pass

    @abstractmethod
    def delete(self, file: Any, bucket: str):
        pass


class StorageRepository(ABC):
    @abstractmethod
    def convert(self, storage: str):
        pass

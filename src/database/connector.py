from abc import ABC, abstractmethod
from typing import Any


class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def exec(self, query: str, params: Any = None):
        pass


class Repository(ABC):
    @abstractmethod
    def convert(self, database: str):
        pass

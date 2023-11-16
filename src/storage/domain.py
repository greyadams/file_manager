from fastapi import UploadFile
from typing import Any
from io import BytesIO

from starlette.concurrency import run_in_threadpool


class DomainFile:
    def __init__(self, content: bytes, filename: str, content_type: str):
        self.content = content
        self.filename = filename
        self.content_type = content_type



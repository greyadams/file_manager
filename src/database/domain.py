from datetime import datetime


class DomainMetaData:
    def __init__(self, user_id: int, product_id: int, filename: str, file_path: str):
        self.user_id = user_id
        self.product_id = product_id
        self.filename = filename
        self.file_path = file_path
        self.created_at = datetime.now()

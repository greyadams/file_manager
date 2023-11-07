from datetime import datetime


class DomainMetaData:
    def __init__(self, user_id: int, filename: str, product_id: int = None,  file_path: str = None):
        self.user_id = user_id
        self.product_id = product_id
        self.filename = filename
        self.file_path = file_path
        self.created_at = datetime.now()

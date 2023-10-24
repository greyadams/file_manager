class DomainFile:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename


class File:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename


class S3Repository:
    @staticmethod
    def domain_meta_data_to_file_data(domain_file: DomainFile) -> File:
        return File(domain_file.file, domain_file.filename)

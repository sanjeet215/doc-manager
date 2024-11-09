import os
import mimetypes
from datetime import datetime
from abc import ABC, abstractmethod



class BaseDocumentMetadata(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = {}
        self.file_size = os.path.getsize(file_path)
        self.file_type, _ = mimetypes.guess_type(file_path)

    @abstractmethod
    def extract_metadata(self):
        self.metadata['file_path'] = self.file_path
        self.metadata['file_type'] = self.file_type or "Unknown"
        self.metadata['file_size'] = self.file_size
        self.metadata['created_datetime'] = datetime.fromtimestamp(
            os.path.getctime(self.file_path)
        ).isoformat()
        self.metadata['modified_datetime'] = datetime.fromtimestamp(
            os.path.getmtime(self.file_path)
        ).isoformat()

    def get_metadata(self):
        return self.metadata
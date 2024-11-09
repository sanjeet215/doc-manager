from app.services.baseDocumentMetadata import BaseDocumentMetadata
from docx import Document

class DOCXMetadata(BaseDocumentMetadata):
    def extract_metadata(self):
        super().extract_metadata()
        doc = Document(self.file_path)
        properties = doc.core_properties
        self.metadata['title'] = properties.title or "Unknown"
        self.metadata['author'] = properties.author or "Unknown"
        self.metadata['created_datetime'] = properties.created.isoformat() if properties.created else "Unknown"
        self.metadata['last_modified_by'] = properties.last_modified_by or "Unknown"
        self.metadata['modified_datetime'] = properties.modified.isoformat() if properties.modified else "Unknown"
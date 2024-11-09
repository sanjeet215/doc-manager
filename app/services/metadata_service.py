
import mimetypes

from app.services.docxMetadata import DOCXMetadata
from app.services.imageMetadata import ImageMetadata
from app.services.pdfMetadata import PDFMetadata


class DocumentMetadata:
    # Factory function to select the correct metadata class based on file type
    def __init__(self):
        self.metadata = None

    @staticmethod
    def get_document_metadata(file_path: str):
        file_type, _ = mimetypes.guess_type(file_path)
        if file_type == 'application/pdf':
            return PDFMetadata(file_path)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return DOCXMetadata(file_path)
        elif file_type in ['image/jpeg', 'image/png']:
            return ImageMetadata(file_path)
        else:
            raise ValueError("Unsupported file type")


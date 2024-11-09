from app.services.baseDocumentMetadata import BaseDocumentMetadata
from PIL import Image

class ImageMetadata(BaseDocumentMetadata):
    def extract_metadata(self):
        super().extract_metadata()
        with Image.open(self.file_path) as img:
            self.metadata['width'], self.metadata['height'] = img.size
            self.metadata['format'] = img.format
            self.metadata['mode'] = img.mode
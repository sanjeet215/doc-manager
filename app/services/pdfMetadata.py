from PyPDF2 import PdfFileReader
from app.services.baseDocumentMetadata import BaseDocumentMetadata


class PDFMetadata(BaseDocumentMetadata):
    def extract_metadata(self):
        super().extract_metadata()
        # with open(self.file_path, 'rb') as file:
        #     pdf = PdfFileReader(file)
        #     info = pdf.getDocumentInfo()
        #     self.metadata['title'] = info.title if info else "Unknown"
        #     self.metadata['author'] = info.author if info else "Unknown"
        #     self.metadata['producer'] = info.producer if info else "Unknown"
        #     self.metadata['number_of_pages'] = pdf.numPages
        #     self.metadata['created_datetime'] = info.get('/CreationDate', 'Unknown')
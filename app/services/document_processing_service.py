# app/services/document_processing_service.py
import os
from fastapi import HTTPException, UploadFile
from werkzeug.utils import secure_filename
from app.services.metadata_service import DocumentMetadata
from app.core.logging_config import setup_logging

logger = setup_logging()
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpeg', 'png'}

# Helper function to check allowed extensions
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to save file and extract metadata
async def process_file_and_extract_metadata(file: UploadFile):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join("uploads", secure_filename(file.filename))
    os.makedirs("uploads", exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.debug("File saved at %s", file_path)

        # Extract metadata
        document_metadata = DocumentMetadata.get_document_metadata(file_path)
        document_metadata.extract_metadata()
        metadata = document_metadata.get_metadata()
        logger.debug("Metadata extracted: %s", metadata)

        return metadata

    except Exception as e:
        logger.error("Error while processing file: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Temporary file %s removed", file_path)

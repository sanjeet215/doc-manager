# app/services/document_processing_service.py
import os
import aiofiles

from fastapi import HTTPException, UploadFile
from typing import Optional, Dict
from werkzeug.utils import secure_filename
from app.services.metadata_service import DocumentMetadata
from app.core.logging_config import setup_logging

logger = setup_logging()

ALLOWED_FILE_EXTENSIONS = {'png', 'pdf', 'docx', 'jpeg', 'jpg'}


# Helper function to check allowed extensions
def allowed_file(filename: str) -> bool:
    if '.' not in filename:
        logger.info(f"File has no extension: {filename}")
        return False
    extension = filename.rsplit('.', 1)[1].strip().lower()  # strip spaces and ensure lowercase
    logger.info(f"File extension:{extension}")
    is_valid_extension = extension in ALLOWED_FILE_EXTENSIONS
    logger.info(f"is_valid_extension: {is_valid_extension}")
    return is_valid_extension


# Function to save file and extract metadata
async def process_file_and_extract_metadata(file: UploadFile):
    if not allowed_file(file.filename):
        logger.info(f"process_file_and_extract_metadata: file name:{file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join("uploads", secure_filename(file.filename))
    os.makedirs("uploads", exist_ok=True)

    try:
        # with open(file_path, "wb") as f:
        #     f.write(await file.read())
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())
        logger.debug("File saved at %s", file_path)

        # Extract metadata
        metadata = await get_metadata(file_path)
        logger.info("Metadata extracted: %s", metadata)

        # if processing_options.get("generate_pdf") == "true":
        #     generate_pdf(metadata, file_path)

        return metadata

    except Exception as e:
        logger.error("Error while processing file: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Temporary file %s removed", file_path)


async def get_metadata(file_path):
    document_metadata = DocumentMetadata.get_document_metadata(file_path)
    document_metadata.extract_metadata()
    metadata = document_metadata.get_metadata()
    return metadata

# def generate_pdf(metadata, file_path):
#     pass
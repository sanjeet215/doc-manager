# app/services/document_processing_service.py
import os
import aiofiles

from fastapi import HTTPException, UploadFile
from werkzeug.utils import secure_filename
from app.services.metadata_service import DocumentMetadata
from app.core.logging_config import setup_logging
from ..models.operationEnum import OperationEnum
from app.services.utils.convert_images_to_pdf_fpdf import convert_image_to_pdf_fpf

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
async def process_file_and_extract_metadata(file: UploadFile, operation: OperationEnum):
    logger.info(f"process_file_and_extract_metadata: file name:{file.filename} , operation: {operation}")

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join("uploads", secure_filename(file.filename))
    os.makedirs("uploads", exist_ok=True)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())
        logger.debug(f"File saved at {file_path}")

        # Extract metadata
        metadata = await get_metadata(file_path)
        logger.info(f"Metadata extracted: {metadata}")

        await process_based_on_operation(operation,file_path)

        return metadata

    except Exception as e:
        logger.error(f"Error while processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Temporary file %s removed", file_path)


async def get_metadata(file_path):
    logger.info(f"get_metadata file path: {file_path}")
    document_metadata = DocumentMetadata.get_document_metadata(file_path)
    document_metadata.extract_metadata()
    metadata = document_metadata.get_metadata()
    return metadata

async def process_based_on_operation(operation,file_path):
    logger.info(f"process_based_on_operation: {operation}, file: {file_path}")
    if operation == OperationEnum.only_pdf:
        #output_file_path = os.path.join("uploadsNew", secure_filename(file.filename))
        output_file_path = "uploadsNew"
        await convert_image_to_pdf_fpf(file_path,output_file_path)
        logger.info(f"process_based_on_operation generating PDF only: {operation}")



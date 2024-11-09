from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile
import os

from werkzeug.utils import secure_filename
from ..models.documentResponse import DocumentMetadataResponse
from app.services.metadata_service import DocumentMetadata
from ..core.logging_config import setup_logging

logger = setup_logging()

router = APIRouter()
app = FastAPI()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpeg', 'png'}


# Helper function to check allowed extensions
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/document/metadata", response_model=DocumentMetadataResponse)
async def get_document_metadata(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        temp_file_path = f"temp_{file.filename}"
        logger.info("get_document_metadata: temp_file_path: %s", temp_file_path)

        file_path = os.path.join("uploads", secure_filename(file.filename))
        os.makedirs("uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        logger.info(f"File saved at {file_path}")

        document_metadata = DocumentMetadata.get_document_metadata(file_path)
        document_metadata.extract_metadata()
        metadata = document_metadata.get_metadata()
        logger.info("get_document_metadata: metadata: %s", metadata)

        # Clean up the temporary file
        os.remove(file_path)
        logger.debug("<< get_document_metadata")
        return DocumentMetadataResponse(**metadata)
    except Exception as e:
        logger.error("get_document_metadata: error while reading the document: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# # Allowed file extensions (adjust as necessary)
# ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpeg', 'png'}
#
# # Helper function to check allowed extensions
# def allowed_file(filename: str) -> bool:
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Endpoint to handle file uploads
# @app.post("/document/metadata", response_model=DocumentMetadataResponse)
# async def get_document_metadata(file: UploadFile = File(...)):
#     logger.info(">> get_document_metadata")
#
#     # Check if the file type is allowed
#     if not allowed_file(file.filename):
#         raise HTTPException(status_code=400, detail="Invalid file type")
#
#     # Create a secure filename and save the file
#     file_path = os.path.join("uploads", secure_filename(file.filename))
#     os.makedirs("uploads", exist_ok=True)  # Ensure the 'uploads' directory exists
#
#     # Save the file to the specified path
#     try:
#         with open(file_path, "wb") as f:
#             f.write(await file.read())
#         logger.info(f"File saved at {file_path}")
#     except Exception as e:
#         logger.error(f"Failed to save file: {e}")
#         raise HTTPException(status_code=500, detail="Failed to save file")
#
#     # Process the saved file to extract metadata
#     try:
#         # Assuming `DocumentMetadata` is a class with methods to extract metadata
#         document_metadata = DocumentMetadata.get_document_metadata(file_path)
#         document_metadata.extract_metadata()
#         metadata = document_metadata.get_metadata()
#
#         # Return the extracted metadata
#         return DocumentMetadataResponse(**metadata)
#
#     except Exception as e:
#         logger.error(f"Failed to extract metadata: {e}")
#         raise HTTPException(status_code=500, detail="Failed to extract metadata")

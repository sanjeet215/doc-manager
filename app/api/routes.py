from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from app.services.document_processing_service import process_file_and_extract_metadata
from app.models.documentResponse import DocumentMetadataResponse
from ..core.logging_config import setup_logging
from ..models.operationEnum import OperationEnum

logger = setup_logging()
router = APIRouter()


@router.post("/document/metadata", response_model=DocumentMetadataResponse)
async def get_document_metadata(file: UploadFile = File(...), operation: Optional[OperationEnum] = Form(None)):
    try:
        logger.info(f"get_document_metadata request: {operation}")
        metadata = await process_file_and_extract_metadata(file)
        return DocumentMetadataResponse(**metadata)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"get_document_metadata: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

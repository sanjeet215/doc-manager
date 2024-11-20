from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from typing import Optional
from app.services.document_processing_service import process_file_and_extract_metadata
from app.models.documentResponse import DocumentMetadataResponse
from ..core.logging_config import setup_logging
from ..models.operationEnum import OperationEnum
from pydantic import BaseModel

import json

logger = setup_logging()
router = APIRouter()


@router.post("/document/metadata", response_model=DocumentMetadataResponse)
async def get_document_metadata(file: UploadFile = File(...), operation: Optional[OperationEnum] = Form(None),page_size: Optional[str] = Form(None)):
    try:
        logger.info(f"get_document_metadata request: {operation}, page size: {page_size}")
        metadata = await process_file_and_extract_metadata(file,operation,page_size)
        return DocumentMetadataResponse(**metadata)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"get_document_metadata: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


class DocumentRequestModel(BaseModel):
    operation: Optional[str] = None


@router.post("/document/metadata/v2")
async def get_document_metadata_v2(file: UploadFile = File(...),  # Default parameter for file upload
                                   request: Optional[str] = Form(None),
                                   ):
    if request:
        logger.info(f"get_document_metadata_v2:request: {request}")
        try:
            # Parse the JSON string into a dictionary
            request_data = json.loads(request)

            # Convert the dictionary to the Pydantic model
            document_request = DocumentRequestModel(**request_data)
            operation = document_request.operation
            logger.info(f"get_document_metadata:operation: {operation}")
            metadata = await process_file_and_extract_metadata(file)
            return DocumentMetadataResponse(**metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'request' field")
    else:
        operation = 'Not provided'
        logger.warning(f"get_document_metadata_v2: operation: {operation}")

from pydantic import BaseModel

class DocumentMetadataResponse(BaseModel):
    file_path: str
    file_type: str
    file_size: int
    created_datetime: str
    modified_datetime: str
    title: str = "Unknown"
    author: str = "Unknown"
    producer: str = "Unknown"
    number_of_pages: int = 0
    width: int = 0
    height: int = 0
    format: str = "Unknown"
    mode: str = "Unknown"

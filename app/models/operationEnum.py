from enum import Enum

# Define the processing options within the request model
class OperationEnum(str, Enum):
        only_pdf = "ONLY_PDF"
        pdf_compress = "PDF_COMPRESS"
        pdf_high_compress = "PDF_HIGH_COMPRESS"
        ai_convert_and_compress = "AI_CONVERT_AND_COMPRESS"
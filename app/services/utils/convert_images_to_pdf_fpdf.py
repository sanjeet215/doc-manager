from PIL import Image
from fpdf import FPDF
from app.core.logging_config import setup_logging

logger = setup_logging()


async def convert_image_to_pdf_fpf(image_path, output_file_path):
    logger.info(f"convert_image_to_pdf_fpf: image_path: {image_path}, output_pdf: {output_file_path}")
    # Load the image
    image = Image.open(image_path)
    # Convert to RGB if it's in a different mode (e.g., RGBA or P)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Initialize the PDF
    pdf = FPDF()
    pdf.add_page()

    # Save the image as a temporary file in JPG format
    temp_image = "temp_image.jpg"
    image.save(temp_image, "JPEG")

    # Add the image to the PDF
    pdf.image(temp_image, x=0, y=0, w=210)  # A4 width in mm is 210
    pdf.output(output_file_path+"/result.pdf")

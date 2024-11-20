import os
from PIL import Image
from fpdf import FPDF
from app.core.logging_config import setup_logging

logger = setup_logging()

# Conversion constant for inches to millimeters
INCH_TO_MM = 25.4


async def convert_image_to_pdf_fpf(image_path, output_folder_path):
    logger.info(
        f"convert_image_to_pdf_with_dynamic_size: image_path: {image_path}, output_folder: {output_folder_path}")

    # Load the image
    image = Image.open(image_path)

    # Convert to RGB if it's in a different mode (e.g., RGBA or P)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Get the dimensions of the image in inches (assuming you want to use specific inch dimensions)
    width_in, height_in = 15.60, 11.01  # Replace with actual values if available
    width_mm = width_in * INCH_TO_MM
    height_mm = height_in * INCH_TO_MM

    # Calculate the scale factor to fit the image within the page with a margin
    margin_mm = 10  # Set margin in mm on each side
    max_width_mm = width_mm - 2 * margin_mm
    max_height_mm = height_mm - 2 * margin_mm
    image_width_mm, image_height_mm = image.size[0] * 0.264583, image.size[1] * 0.264583
    scale = min(max_width_mm / image_width_mm, max_height_mm / image_height_mm)

    # Calculate resized dimensions
    new_width_mm = image_width_mm * scale
    new_height_mm = image_height_mm * scale

    # Initialize PDF with the custom page size
    pdf = FPDF(unit="mm", format=(width_mm, height_mm))
    pdf.add_page()

    # Save the image as a temporary file in JPEG format
    temp_image = "temp_image.jpg"
    image.save(temp_image, "JPEG")

    # Center the image on the page
    x_pos = (width_mm - new_width_mm) / 2
    y_pos = (height_mm - new_height_mm) / 2
    pdf.image(temp_image, x=x_pos, y=y_pos, w=new_width_mm, h=new_height_mm)

    # Extract the original file name without extension
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_pdf_path = os.path.join(output_folder_path, f"{base_name}.pdf")

    # Save the PDF with the new name
    pdf.output(output_pdf_path)

    # Remove the temporary image file
    if os.path.exists(temp_image):
        os.remove(temp_image)
        logger.info(f"Temporary file {temp_image} removed after PDF generation.")

    logger.info(f"PDF generated at {output_pdf_path}")

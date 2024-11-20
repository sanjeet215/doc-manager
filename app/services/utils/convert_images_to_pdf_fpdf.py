from fpdf import FPDF
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)
INCH_TO_MM = 25.4  # Conversion constant

# Define standard page sizes in mm
PAGE_SIZES = {
    "A4": (210, 297),
    "A5": (148, 210),
    "Letter": (216, 279),
}


async def convert_image_to_pdf_fpf(image_path, output_folder_path, page_size="A4"):
    """
    Converts an image to a PDF with the specified page size, ensuring it fits properly with margins.

    :param image_path: Path to the input image.
    :param output_folder_path: Path to the folder where the PDF will be saved.
    :param page_size: Page size for the PDF. Options: "A4", "A5", "Letter", or "suggested" for original size.
    :return: Path to the generated PDF.
    """
    if page_size in PAGE_SIZES:
        # Get the dimensions of the standard page size
        width_mm, height_mm = PAGE_SIZES[page_size]
        suggested_size = False
    else:
        # If "suggested" size is specified or an invalid page size is provided, use the original image size
        suggested_size = True
        image = Image.open(image_path)
        width_mm = image.width * 0.264583  # Pixel to mm conversion
        height_mm = image.height * 0.264583
        logger.info(f"Using suggested size: width={width_mm}mm, height={height_mm}mm")

    logger.info(
        f"convert_image_to_pdf_fpf: image_path: {image_path}, output_folder: {output_folder_path}, "
        f"page_size: {page_size if not suggested_size else 'Original Dimensions'}"
    )

    # Load the image
    image = Image.open(image_path)

    # Convert to RGB if it's in a different mode (e.g., RGBA or P)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Calculate the scale factor to fit the image within the page with a margin
    margin_mm = 10  # Set margin in mm on each side
    max_width_mm = width_mm - 2 * margin_mm
    max_height_mm = height_mm - 2 * margin_mm
    image_width_mm, image_height_mm = image.size[0] * 0.264583, image.size[1] * 0.264583

    # Scale the image to fit within the page dimensions while maintaining the aspect ratio
    scale = min(max_width_mm / image_width_mm, max_height_mm / image_height_mm)

    # Calculate resized dimensions
    new_width_mm = image_width_mm * scale
    new_height_mm = image_height_mm * scale

    # Initialize PDF with the selected page size or suggested size
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
    return output_pdf_path

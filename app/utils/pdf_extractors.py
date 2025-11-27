"""
PDF extraction utilities using various libraries.
Each extractor returns plain text with all extracted content.
"""

import io
from pathlib import Path
from typing import Any

# PyMuPDF (fitz)
import fitz

# pdfplumber
import pdfplumber

# pypdf
from pypdf import PdfReader

# pdfminer.six
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdfminer.layout import LAParams

# OCR
import pytesseract
from PIL import Image

from app.config import get_settings

settings = get_settings()

# Configure tesseract if path is specified
if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


class PyMuPDFExtractor:
    """Extract text, tables, images, and metadata using PyMuPDF (fitz)."""

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract all content from PDF using PyMuPDF.

        Args:
            file_path: Path to PDF file

        Returns:
            Plain text with all extracted content
        """
        output_parts = []
        doc = fitz.open(file_path)

        try:
            # Extract metadata
            metadata = doc.metadata
            if metadata:
                output_parts.append("=== METADATA ===")
                for key, value in metadata.items():
                    if value:
                        output_parts.append(f"{key}: {value}")
                output_parts.append("")

            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                output_parts.append(f"=== PAGE {page_num + 1} ===")

                # Extract text
                text = page.get_text()
                if text.strip():
                    output_parts.append(text)

                # Extract tables
                tables = page.find_tables()
                if tables:
                    output_parts.append("\n--- Tables ---")
                    for table_num, table in enumerate(tables, 1):
                        output_parts.append(f"\nTable {table_num}:")
                        try:
                            table_data = table.extract()
                            for row in table_data:
                                output_parts.append(" | ".join(str(cell) if cell else "" for cell in row))
                        except Exception as e:
                            output_parts.append(f"Error extracting table: {e}")

                # Extract images and try OCR
                images = page.get_images()
                if images:
                    output_parts.append("\n--- Images ---")
                    for img_num, img in enumerate(images, 1):
                        try:
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]

                            # Try OCR on image
                            image = Image.open(io.BytesIO(image_bytes))
                            ocr_text = pytesseract.image_to_string(
                                image, lang=settings.ocr_language
                            )
                            if ocr_text.strip():
                                output_parts.append(f"\nImage {img_num} OCR text:")
                                output_parts.append(ocr_text)
                        except Exception as e:
                            output_parts.append(f"Error processing image {img_num}: {e}")

                output_parts.append("")

        finally:
            doc.close()

        return "\n".join(output_parts)


class PDFPlumberExtractor:
    """Extract text, tables, and metadata using pdfplumber."""

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract all content from PDF using pdfplumber.

        Args:
            file_path: Path to PDF file

        Returns:
            Plain text with all extracted content
        """
        output_parts = []

        with pdfplumber.open(file_path) as pdf:
            # Extract metadata
            if pdf.metadata:
                output_parts.append("=== METADATA ===")
                for key, value in pdf.metadata.items():
                    if value:
                        output_parts.append(f"{key}: {value}")
                output_parts.append("")

            # Process each page
            for page_num, page in enumerate(pdf.pages, 1):
                output_parts.append(f"=== PAGE {page_num} ===")

                # Extract text
                text = page.extract_text()
                if text:
                    output_parts.append(text)

                # Extract tables
                tables = page.extract_tables()
                if tables:
                    output_parts.append("\n--- Tables ---")
                    for table_num, table in enumerate(tables, 1):
                        output_parts.append(f"\nTable {table_num}:")
                        for row in table:
                            output_parts.append(" | ".join(str(cell) if cell else "" for cell in row))

                # Extract images and try OCR
                try:
                    images = page.images
                    if images:
                        output_parts.append("\n--- Images ---")
                        for img_num, img in enumerate(images, 1):
                            try:
                                # Convert page to image and crop to image bbox
                                im = page.to_image()
                                bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                                cropped = im.original.crop(bbox)

                                # Try OCR
                                ocr_text = pytesseract.image_to_string(
                                    cropped, lang=settings.ocr_language
                                )
                                if ocr_text.strip():
                                    output_parts.append(f"\nImage {img_num} OCR text:")
                                    output_parts.append(ocr_text)
                            except Exception as e:
                                output_parts.append(f"Error processing image {img_num}: {e}")
                except Exception as e:
                    output_parts.append(f"Error extracting images: {e}")

                output_parts.append("")

        return "\n".join(output_parts)


class PyPDFExtractor:
    """Extract text and metadata using pypdf."""

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract all content from PDF using pypdf.

        Args:
            file_path: Path to PDF file

        Returns:
            Plain text with all extracted content
        """
        output_parts = []

        with open(file_path, "rb") as file:
            reader = PdfReader(file)

            # Extract metadata
            if reader.metadata:
                output_parts.append("=== METADATA ===")
                for key, value in reader.metadata.items():
                    if value:
                        output_parts.append(f"{key}: {value}")
                output_parts.append("")

            # Process each page
            for page_num, page in enumerate(reader.pages, 1):
                output_parts.append(f"=== PAGE {page_num} ===")

                # Extract text
                text = page.extract_text()
                if text:
                    output_parts.append(text)

                # Extract images and try OCR
                if hasattr(page, "images"):
                    images = page.images
                    if images:
                        output_parts.append("\n--- Images ---")
                        for img_num, image in enumerate(images, 1):
                            try:
                                # Get image data
                                image_data = image.data
                                pil_image = Image.open(io.BytesIO(image_data))

                                # Try OCR
                                ocr_text = pytesseract.image_to_string(
                                    pil_image, lang=settings.ocr_language
                                )
                                if ocr_text.strip():
                                    output_parts.append(f"\nImage {img_num} OCR text:")
                                    output_parts.append(ocr_text)
                            except Exception as e:
                                output_parts.append(f"Error processing image {img_num}: {e}")

                output_parts.append("")

        return "\n".join(output_parts)


class PDFMinerExtractor:
    """Extract text using pdfminer.six."""

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract all content from PDF using pdfminer.six.

        Args:
            file_path: Path to PDF file

        Returns:
            Plain text with all extracted content
        """
        output_parts = []

        # Extract text with layout analysis
        laparams = LAParams()
        text = pdfminer_extract_text(file_path, laparams=laparams)

        output_parts.append("=== EXTRACTED TEXT ===")
        if text:
            output_parts.append(text)

        # Note: pdfminer.six is primarily for text extraction
        # For tables, images, and metadata, use other libraries
        output_parts.append("\nNote: pdfminer.six specializes in text extraction.")
        output_parts.append("For advanced features (tables, images), consider PyMuPDF or pdfplumber.")

        return "\n".join(output_parts)


# Extractor factory
def get_extractor(tool: str):
    """
    Get the appropriate extractor class for the specified tool.

    Args:
        tool: Name of the extraction tool

    Returns:
        Extractor class

    Raises:
        ValueError: If tool is not supported
    """
    extractors = {
        "pymupdf": PyMuPDFExtractor,
        "pdfplumber": PDFPlumberExtractor,
        "pypdf": PyPDFExtractor,
        "pdfminer": PDFMinerExtractor,
    }

    if tool not in extractors:
        raise ValueError(f"Unsupported tool: {tool}. Available: {list(extractors.keys())}")

    return extractors[tool]

"""
PDF extraction utilities using various libraries.
Each extractor returns structured data with type and content fields.
"""

import io
from pathlib import Path
from typing import List, Dict, Any

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
    def extract(file_path: str) -> List[Dict[str, str]]:
        """
        Extract all content from PDF using PyMuPDF.

        Args:
            file_path: Path to PDF file

        Returns:
            List of dictionaries with type and content fields
        """
        output: List[Dict[str, str]] = []
        doc = fitz.open(file_path)

        try:
            # Extract metadata
            metadata = doc.metadata
            if metadata:
                metadata_str = "\n".join(f"{key}: {value}" for key, value in metadata.items() if value)
                if metadata_str.strip():
                    output.append({"type": "metadata", "content": metadata_str})

            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]

                # Extract text
                text = page.get_text()
                if text.strip():
                    output.append({"type": "text", "content": text})

                # Extract tables
                tables = page.find_tables()
                if tables:
                    for table_num, table in enumerate(tables, 1):
                        try:
                            table_data = table.extract()
                            table_content = []
                            for row in table_data:
                                row_text = " | ".join(str(cell) if cell else "" for cell in row)
                                table_content.append(row_text)
                            table_str = f"Table {table_num}:\n" + "\n".join(table_content)
                            output.append({"type": "table", "content": table_str})
                        except Exception as e:
                            output.append({"type": "table", "content": f"Error extracting table: {e}"})

                # Extract images and try OCR
                images = page.get_images()
                if images:
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
                                output.append({"type": "image", "content": f"Image {img_num} OCR text:\n{ocr_text}"})
                        except Exception as e:
                            output.append({"type": "image", "content": f"Error processing image {img_num}: {e}"})

        finally:
            doc.close()

        return output


class PDFPlumberExtractor:
    """Extract text, tables, and metadata using pdfplumber."""

    @staticmethod
    def extract(file_path: str) -> List[Dict[str, str]]:
        """
        Extract all content from PDF using pdfplumber.

        Args:
            file_path: Path to PDF file

        Returns:
            List of dictionaries with type and content fields
        """
        output: List[Dict[str, str]] = []

        with pdfplumber.open(file_path) as pdf:
            # Extract metadata
            if pdf.metadata:
                metadata_str = "\n".join(f"{key}: {value}" for key, value in pdf.metadata.items() if value)
                if metadata_str.strip():
                    output.append({"type": "metadata", "content": metadata_str})

            # Process each page
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text()
                if text:
                    output.append({"type": "text", "content": text})

                # Extract tables
                tables = page.extract_tables()
                if tables:
                    for table_num, table in enumerate(tables, 1):
                        table_content = []
                        for row in table:
                            # Join cells with pipe separator
                            row_text = " | ".join(str(cell) if cell else "" for cell in row)
                            if row_text.strip():
                                table_content.append(row_text)
                        if table_content:
                            table_str = f"Table {table_num}:\n" + "\n".join(table_content)
                            output.append({"type": "table", "content": table_str})

                # Extract images and try OCR
                try:
                    images = page.images
                    if images:
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
                                    output.append({"type": "image", "content": f"Image {img_num} OCR text:\n{ocr_text}"})
                            except Exception as e:
                                output.append({"type": "image", "content": f"Error processing image {img_num}: {e}"})
                except Exception as e:
                    output.append({"type": "image", "content": f"Error extracting images: {e}"})

        return output


class PyPDFExtractor:
    """Extract text and metadata using pypdf."""

    @staticmethod
    def extract(file_path: str) -> List[Dict[str, str]]:
        """
        Extract all content from PDF using pypdf.

        Args:
            file_path: Path to PDF file

        Returns:
            List of dictionaries with type and content fields
        """
        output: List[Dict[str, str]] = []

        with open(file_path, "rb") as file:
            reader = PdfReader(file)

            # Extract metadata
            if reader.metadata:
                metadata_str = "\n".join(f"{key}: {value}" for key, value in reader.metadata.items() if value)
                if metadata_str.strip():
                    output.append({"type": "metadata", "content": metadata_str})

            # Process each page
            for page_num, page in enumerate(reader.pages, 1):
                # Extract text
                text = page.extract_text()
                if text:
                    output.append({"type": "text", "content": text})

                # Extract images and try OCR
                if hasattr(page, "images"):
                    images = page.images
                    if images:
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
                                    output.append({"type": "image", "content": f"Image {img_num} OCR text:\n{ocr_text}"})
                            except Exception as e:
                                output.append({"type": "image", "content": f"Error processing image {img_num}: {e}"})

        return output


class PDFMinerExtractor:
    """Extract text using pdfminer.six."""

    @staticmethod
    def extract(file_path: str) -> List[Dict[str, str]]:
        """
        Extract all content from PDF using pdfminer.six.

        Args:
            file_path: Path to PDF file

        Returns:
            List of dictionaries with type and content fields
        """
        output: List[Dict[str, str]] = []

        # Extract text with layout analysis
        laparams = LAParams()
        text = pdfminer_extract_text(file_path, laparams=laparams)

        if text:
            output.append({"type": "text", "content": text})

        # Note: pdfminer.six is primarily for text extraction
        # For tables, images, and metadata, use other libraries

        return output


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

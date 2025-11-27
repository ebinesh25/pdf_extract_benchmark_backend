"""
Celery tasks for PDF extraction using various tools.
"""

from celery import Task
from app.celery_app import celery_app
from app.utils.pdf_extractors import get_extractor
from app.utils.file_handler import delete_file


class PDFExtractionTask(Task):
    """Base task for PDF extraction with cleanup."""

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """Clean up uploaded file after task completes."""
        if args and len(args) > 0:
            file_path = args[0]
            delete_file(file_path)


@celery_app.task(
    bind=True,
    base=PDFExtractionTask,
    name="extract_pdf_pymupdf",
    max_retries=3,
    default_retry_delay=60
)
def extract_pdf_pymupdf(self, file_path: str) -> dict:
    """
    Extract text from PDF using PyMuPDF (fitz).

    Args:
        file_path: Path to the PDF file

    Returns:
        dict: Result with extracted text or error
    """
    try:
        extractor = get_extractor("pymupdf")
        text = extractor.extract(file_path)
        return {
            "status": "success",
            "tool": "pymupdf",
            "text": text,
            "error": None
        }
    except Exception as e:
        error_msg = f"PyMuPDF extraction failed: {str(e)}"
        return {
            "status": "error",
            "tool": "pymupdf",
            "text": None,
            "error": error_msg
        }


@celery_app.task(
    bind=True,
    base=PDFExtractionTask,
    name="extract_pdf_pdfplumber",
    max_retries=3,
    default_retry_delay=60
)
def extract_pdf_pdfplumber(self, file_path: str) -> dict:
    """
    Extract text from PDF using pdfplumber.

    Args:
        file_path: Path to the PDF file

    Returns:
        dict: Result with extracted text or error
    """
    try:
        extractor = get_extractor("pdfplumber")
        text = extractor.extract(file_path)
        return {
            "status": "success",
            "tool": "pdfplumber",
            "text": text,
            "error": None
        }
    except Exception as e:
        error_msg = f"pdfplumber extraction failed: {str(e)}"
        return {
            "status": "error",
            "tool": "pdfplumber",
            "text": None,
            "error": error_msg
        }


@celery_app.task(
    bind=True,
    base=PDFExtractionTask,
    name="extract_pdf_pypdf",
    max_retries=3,
    default_retry_delay=60
)
def extract_pdf_pypdf(self, file_path: str) -> dict:
    """
    Extract text from PDF using pypdf.

    Args:
        file_path: Path to the PDF file

    Returns:
        dict: Result with extracted text or error
    """
    try:
        extractor = get_extractor("pypdf")
        text = extractor.extract(file_path)
        return {
            "status": "success",
            "tool": "pypdf",
            "text": text,
            "error": None
        }
    except Exception as e:
        error_msg = f"pypdf extraction failed: {str(e)}"
        return {
            "status": "error",
            "tool": "pypdf",
            "text": None,
            "error": error_msg
        }


@celery_app.task(
    bind=True,
    base=PDFExtractionTask,
    name="extract_pdf_pdfminer",
    max_retries=3,
    default_retry_delay=60
)
def extract_pdf_pdfminer(self, file_path: str) -> dict:
    """
    Extract text from PDF using pdfminer.six.

    Args:
        file_path: Path to the PDF file

    Returns:
        dict: Result with extracted text or error
    """
    try:
        extractor = get_extractor("pdfminer")
        text = extractor.extract(file_path)
        return {
            "status": "success",
            "tool": "pdfminer",
            "text": text,
            "error": None
        }
    except Exception as e:
        error_msg = f"pdfminer extraction failed: {str(e)}"
        return {
            "status": "error",
            "tool": "pdfminer",
            "text": None,
            "error": error_msg
        }

"""
API routes for PDF extraction (synchronous).
"""

from fastapi import APIRouter, UploadFile, File

from app.schemas.extraction import (
    ExtractionResponse,
    ExtractionTool,
    ErrorResponse
)
from app.utils.file_handler import validate_pdf_file, save_upload_file, delete_file
from app.utils.pdf_extractors import get_extractor

router = APIRouter(prefix="/extract", tags=["PDF Extraction"])


@router.post(
    "/pymupdf",
    response_model=ExtractionResponse,
    status_code=200,
    summary="Extract PDF using PyMuPDF",
    description="Extract text from PDF using PyMuPDF (fitz). "
                "Extracts text, tables, images (with OCR), and metadata. "
                "Returns results immediately (synchronous)."
)
async def extract_with_pymupdf(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionResponse:
    """Extract text from PDF using PyMuPDF."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    try:
        extractor = get_extractor("pymupdf")
        text = extractor.extract(file_path)

        return ExtractionResponse(
            status="success",
            tool=ExtractionTool.PYMUPDF,
            text=text,
            error=None
        )
    except Exception as e:
        return ExtractionResponse(
            status="error",
            tool=ExtractionTool.PYMUPDF,
            text=None,
            error=f"PyMuPDF extraction failed: {str(e)}"
        )
    finally:
        delete_file(file_path)


@router.post(
    "/pdfplumber",
    response_model=ExtractionResponse,
    status_code=200,
    summary="Extract PDF using pdfplumber",
    description="Extract text from PDF using pdfplumber. "
                "Excellent for table extraction and detailed layout analysis. "
                "Returns results immediately (synchronous)."
)
async def extract_with_pdfplumber(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionResponse:
    """Extract text from PDF using pdfplumber."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    try:
        extractor = get_extractor("pdfplumber")
        text = extractor.extract(file_path)

        return ExtractionResponse(
            status="success",
            tool=ExtractionTool.PDFPLUMBER,
            text=text,
            error=None
        )
    except Exception as e:
        return ExtractionResponse(
            status="error",
            tool=ExtractionTool.PDFPLUMBER,
            text=None,
            error=f"pdfplumber extraction failed: {str(e)}"
        )
    finally:
        delete_file(file_path)


@router.post(
    "/pypdf",
    response_model=ExtractionResponse,
    status_code=200,
    summary="Extract PDF using pypdf",
    description="Extract text from PDF using pypdf. "
                "Lightweight library good for simple text extraction. "
                "Returns results immediately (synchronous)."
)
async def extract_with_pypdf(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionResponse:
    """Extract text from PDF using pypdf."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    try:
        extractor = get_extractor("pypdf")
        text = extractor.extract(file_path)

        return ExtractionResponse(
            status="success",
            tool=ExtractionTool.PYPDF,
            text=text,
            error=None
        )
    except Exception as e:
        return ExtractionResponse(
            status="error",
            tool=ExtractionTool.PYPDF,
            text=None,
            error=f"pypdf extraction failed: {str(e)}"
        )
    finally:
        delete_file(file_path)


@router.post(
    "/pdfminer",
    response_model=ExtractionResponse,
    status_code=200,
    summary="Extract PDF using pdfminer.six",
    description="Extract text from PDF using pdfminer.six. "
                "Deep text analysis with position information. "
                "Returns results immediately (synchronous)."
)
async def extract_with_pdfminer(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionResponse:
    """Extract text from PDF using pdfminer.six."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    try:
        extractor = get_extractor("pdfminer")
        text = extractor.extract(file_path)

        return ExtractionResponse(
            status="success",
            tool=ExtractionTool.PDFMINER,
            text=text,
            error=None
        )
    except Exception as e:
        return ExtractionResponse(
            status="error",
            tool=ExtractionTool.PDFMINER,
            text=None,
            error=f"pdfminer extraction failed: {str(e)}"
        )
    finally:
        delete_file(file_path)

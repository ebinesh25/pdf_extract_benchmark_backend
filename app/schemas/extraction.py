"""
Pydantic schemas for PDF extraction API (synchronous).
"""

from enum import Enum
from pydantic import BaseModel, Field


class ExtractionTool(str, Enum):
    """Supported PDF extraction tools."""
    PYMUPDF = "pymupdf"
    PDFPLUMBER = "pdfplumber"
    PYPDF = "pypdf"
    PDFMINER = "pdfminer"


class ExtractionResponse(BaseModel):
    """Response from PDF extraction."""
    status: str = Field(..., description="Extraction status (success/error)")
    tool: ExtractionTool = Field(..., description="Extraction tool used")
    text: str | None = Field(None, description="Extracted text content")
    error: str | None = Field(None, description="Error message if extraction failed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "tool": "pymupdf",
                    "text": "=== METADATA ===\nTitle: Sample Document\n\n=== PAGE 1 ===\nThis is the extracted text...",
                    "error": None
                },
                {
                    "status": "error",
                    "tool": "pymupdf",
                    "text": None,
                    "error": "PyMuPDF extraction failed: Invalid PDF file"
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Invalid file type. Allowed: .pdf"
            }
        }
    }

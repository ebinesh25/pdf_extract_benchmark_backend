"""
Pydantic schemas for PDF extraction API (synchronous).
"""

from enum import Enum
from typing import List, Dict
from pydantic import BaseModel, Field


class ExtractionTool(str, Enum):
    """Supported PDF extraction tools."""
    PYMUPDF = "pymupdf"
    PDFPLUMBER = "pdfplumber"
    PYPDF = "pypdf"
    PDFMINER = "pdfminer"


class ExtractionContent(BaseModel):
    """Individual content item extracted from PDF."""
    type: str = Field(..., description="Type of content: text, table, metadata, or image")
    content: str = Field(..., description="The actual content")


class ExtractionResponse(BaseModel):
    """Response from PDF extraction."""
    status: str = Field(..., description="Extraction status (success/error)")
    tool: ExtractionTool = Field(..., description="Extraction tool used")
    data: List[ExtractionContent] | None = Field(None, description="Structured extracted content")
    text: str | None = Field(None, description="Legacy text field for backward compatibility")
    error: str | None = Field(None, description="Error message if extraction failed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "tool": "pymupdf",
                    "data": [
                        {
                            "type": "metadata",
                            "content": "Title: Sample Document\nAuthor: John Doe"
                        },
                        {
                            "type": "text",
                            "content": "This is the extracted text from page 1..."
                        },
                        {
                            "type": "table",
                            "content": "Table 1:\nName | Age | City\nJohn | 30 | NYC"
                        }
                    ],
                    "text": None,
                    "error": None
                },
                {
                    "status": "error",
                    "tool": "pymupdf",
                    "data": None,
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

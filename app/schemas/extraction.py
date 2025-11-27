"""
Pydantic schemas for PDF extraction API.
"""

from enum import Enum
from pydantic import BaseModel, Field


class ExtractionTool(str, Enum):
    """Supported PDF extraction tools."""
    PYMUPDF = "pymupdf"
    PDFPLUMBER = "pdfplumber"
    PYPDF = "pypdf"
    PDFMINER = "pdfminer"


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"


class ExtractionSubmitResponse(BaseModel):
    """Response when PDF extraction task is submitted."""
    task_id: str = Field(..., description="Unique task identifier")
    status: str = Field(..., description="Initial task status")
    tool: ExtractionTool = Field(..., description="Extraction tool used")
    message: str = Field(..., description="Human-readable message")

    model_config = {
        "json_schema_extra": {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "PENDING",
                "tool": "pymupdf",
                "message": "PDF extraction task submitted successfully"
            }
        }
    }


class ExtractionResult(BaseModel):
    """Result of PDF extraction."""
    status: str = Field(..., description="Extraction status (success/error)")
    tool: ExtractionTool = Field(..., description="Extraction tool used")
    text: str | None = Field(None, description="Extracted text content")
    error: str | None = Field(None, description="Error message if extraction failed")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "tool": "pymupdf",
                "text": "This is the extracted text from the PDF...",
                "error": None
            }
        }
    }


class TaskStatusResponse(BaseModel):
    """Response with task status and results."""
    task_id: str = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(..., description="Current task status")
    result: ExtractionResult | None = Field(None, description="Extraction result if completed")
    error: str | None = Field(None, description="Error message if task failed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "status": "PENDING",
                    "result": None,
                    "error": None
                },
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "status": "SUCCESS",
                    "result": {
                        "status": "success",
                        "tool": "pymupdf",
                        "text": "Extracted text content...",
                        "error": None
                    },
                    "error": None
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

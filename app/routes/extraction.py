"""
API routes for PDF extraction.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from celery.result import AsyncResult

from app.schemas.extraction import (
    ExtractionSubmitResponse,
    TaskStatusResponse,
    ExtractionTool,
    TaskStatus,
    ExtractionResult,
    ErrorResponse
)
from app.utils.file_handler import validate_pdf_file, save_upload_file
from app.tasks.extraction import (
    extract_pdf_pymupdf,
    extract_pdf_pdfplumber,
    extract_pdf_pypdf,
    extract_pdf_pdfminer
)
from app.celery_app import celery_app

router = APIRouter(prefix="/extract", tags=["PDF Extraction"])


@router.post(
    "/pymupdf",
    response_model=ExtractionSubmitResponse,
    status_code=202,
    summary="Extract PDF using PyMuPDF",
    description="Submit a PDF for text extraction using PyMuPDF (fitz). "
                "Extracts text, tables, images (with OCR), and metadata."
)
async def extract_with_pymupdf(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionSubmitResponse:
    """Extract text from PDF using PyMuPDF."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    task = extract_pdf_pymupdf.delay(file_path)

    return ExtractionSubmitResponse(
        task_id=task.id,
        status="PENDING",
        tool=ExtractionTool.PYMUPDF,
        message="PDF extraction task submitted successfully"
    )


@router.post(
    "/pdfplumber",
    response_model=ExtractionSubmitResponse,
    status_code=202,
    summary="Extract PDF using pdfplumber",
    description="Submit a PDF for text extraction using pdfplumber. "
                "Excellent for table extraction and detailed layout analysis."
)
async def extract_with_pdfplumber(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionSubmitResponse:
    """Extract text from PDF using pdfplumber."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    task = extract_pdf_pdfplumber.delay(file_path)

    return ExtractionSubmitResponse(
        task_id=task.id,
        status="PENDING",
        tool=ExtractionTool.PDFPLUMBER,
        message="PDF extraction task submitted successfully"
    )


@router.post(
    "/pypdf",
    response_model=ExtractionSubmitResponse,
    status_code=202,
    summary="Extract PDF using pypdf",
    description="Submit a PDF for text extraction using pypdf. "
                "Lightweight library good for simple text extraction."
)
async def extract_with_pypdf(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionSubmitResponse:
    """Extract text from PDF using pypdf."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    task = extract_pdf_pypdf.delay(file_path)

    return ExtractionSubmitResponse(
        task_id=task.id,
        status="PENDING",
        tool=ExtractionTool.PYPDF,
        message="PDF extraction task submitted successfully"
    )


@router.post(
    "/pdfminer",
    response_model=ExtractionSubmitResponse,
    status_code=202,
    summary="Extract PDF using pdfminer.six",
    description="Submit a PDF for text extraction using pdfminer.six. "
                "Deep text analysis with position information."
)
async def extract_with_pdfminer(
    file: UploadFile = File(..., description="PDF file to extract text from")
) -> ExtractionSubmitResponse:
    """Extract text from PDF using pdfminer.six."""
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)

    task = extract_pdf_pdfminer.delay(file_path)

    return ExtractionSubmitResponse(
        task_id=task.id,
        status="PENDING",
        tool=ExtractionTool.PDFMINER,
        message="PDF extraction task submitted successfully"
    )


@router.get(
    "/task/{task_id}",
    response_model=TaskStatusResponse,
    summary="Get task status and results",
    description="Check the status of a PDF extraction task and retrieve results if completed.",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """Get the status and results of a PDF extraction task."""
    task_result = AsyncResult(task_id, app=celery_app)

    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")

    # Map Celery states to our TaskStatus enum
    status = task_result.state

    # Build response based on task state
    if status == "PENDING":
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            result=None,
            error=None
        )
    elif status == "STARTED":
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.STARTED,
            result=None,
            error=None
        )
    elif status == "SUCCESS":
        result_data = task_result.result
        extraction_result = ExtractionResult(
            status=result_data.get("status", "success"),
            tool=result_data.get("tool"),
            text=result_data.get("text"),
            error=result_data.get("error")
        )
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.SUCCESS,
            result=extraction_result,
            error=None
        )
    elif status == "FAILURE":
        error_msg = str(task_result.result) if task_result.result else "Task failed"
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.FAILURE,
            result=None,
            error=error_msg
        )
    elif status == "RETRY":
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.RETRY,
            result=None,
            error="Task is being retried"
        )
    else:
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            result=None,
            error=None
        )

from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException

from app.schemas.extraction import ExtractionTool
from app.schemas.benchmarking import BenchmarkResponse
from app.utils.file_handler import validate_pdf_file, save_upload_file, delete_file
from app.utils.benchmarking import BenchmarkEngine

router = APIRouter(prefix="/benchmark", tags=["Benchmarking"])

@router.post(
    "",
    response_model=BenchmarkResponse,
    summary="Benchmark PDF Extraction Tools",
    description="Run selected extraction tools on a PDF file and compare their performance (speed, accuracy)."
)
async def benchmark_pdf(
    file: UploadFile = File(..., description="PDF file to benchmark"),
    tools: List[ExtractionTool] = Query(..., description="List of tools to benchmark (e.g., pymupdf, pdfplumber)"),
    ground_truth: Optional[str] = Form(None, description="Ground truth text for accuracy calculation")
) -> BenchmarkResponse:
    """
    Benchmark selected PDF extraction tools.
    """
    await validate_pdf_file(file)
    file_path = await save_upload_file(file)
    
    try:
        results = BenchmarkEngine.benchmark_file(
            file_path=file_path,
            tools=tools,
            ground_truth=ground_truth
        )
        
        return BenchmarkResponse(
            filename=file.filename,
            file_size_bytes=file.size if file.size else 0,
            results=results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmarking failed: {str(e)}")
        
    finally:
        delete_file(file_path)

from typing import List, Optional
from pydantic import BaseModel
from app.schemas.extraction import ExtractionTool

class BenchmarkResult(BaseModel):
    tool: ExtractionTool
    execution_time_ms: float
    accuracy_score: Optional[float] = None
    extracted_text_length: int
    error: Optional[str] = None
    
    # Static info
    cost_per_page: str = "Free"
    features: List[str] = []

class BenchmarkResponse(BaseModel):
    filename: str
    file_size_bytes: int
    results: List[BenchmarkResult]

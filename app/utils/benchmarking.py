from typing import List, Optional, Dict
import asyncio
import time
from app.schemas.extraction import ExtractionTool
from app.schemas.benchmarking import BenchmarkResult
from app.utils.pdf_extractors import get_extractor

TOOL_FEATURES = {
    ExtractionTool.PYMUPDF: [
        "Text extraction",
        "Table extraction", 
        "Image extraction (with OCR)",
        "Metadata extraction",
        "High speed"
    ],
    ExtractionTool.PDFPLUMBER: [
        "Text extraction",
        "Table extraction",
        "Detailed layout analysis",
        "Metadata extraction"
    ],
    ExtractionTool.PYPDF: [
        "Text extraction",
        "Metadata extraction",
        "Page manipulation",
        "Lightweight"
    ],
    ExtractionTool.PDFMINER: [
        "Text extraction",
        "Layout analysis",
        "Position information"
    ]
}

class BenchmarkEngine:
    
    @staticmethod
    def normalize_extracted_text(text: str) -> str:
        import re

        # Replace newlines and tabs with spaces
        text = re.sub(r"[\n\r\t]+", " ", text)

        # Collapse multiple spaces into one
        text = re.sub(r"\s{2,}", " ", text)

        return text.strip()

    @staticmethod
    def extract_text_from_structured_data(data: List[Dict[str, str]]) -> str:
        """Extract and concatenate only text content from structured data."""
        text_parts = []
        for item in data:
            if item.get("type") == "text":
                text_parts.append(item.get("content", ""))
        return " ".join(text_parts)

        

    @staticmethod
    def calculate_accuracy(ground_truth: str, extracted: str) -> float:
        """Compute similarity between extracted text and ground truth
        Calculate similarity ratio between ground truth and extracted text.
        Returns a float between 0.0 and 1.0.
        """
        if not ground_truth or not extracted:
            return 0.0
        
        # Normalize text for better comparison (optional, but recommended)
        # For now, we'll do simple whitespace normalization
        gt_normalized = " ".join(ground_truth.split())
        ext_normalized = BenchmarkEngine.normalize_extracted_text(extracted)
        
        import difflib
        matcher = difflib.SequenceMatcher(None, gt_normalized, ext_normalized)
        return matcher.ratio()

    @staticmethod
    async def benchmark_file(
        file_path: str,
        tools: List[ExtractionTool],
        ground_truth: Optional[str] = None
    ) -> List[BenchmarkResult]:

        async def run_benchmark(tool_name: ExtractionTool) -> BenchmarkResult:
            start_time = time.perf_counter()
            extracted_data: List[Dict[str, str]] | None = None
            extracted_text: str | None = None
            error_msg = None

            try:
                extractor_class = get_extractor(tool_name.value)

                # Heavy CPU work in thread
                extracted_data = await asyncio.to_thread(
                    extractor_class.extract, file_path
                )

                # Convert structured data to text format for display
                if extracted_data:
                    for data in extracted_data:
                        if data.get("type") == "text":
                            extracted_text = data.get("content")

            except Exception as e:
                error_msg = str(e)

            end_time = time.perf_counter()
            exec_time_ms = (end_time - start_time) * 1000

            # Accuracy (optional) - compare only text content
            accuracy = None
            if ground_truth and extracted_data and not error_msg:
                # Extract only text content from structured data for accuracy comparison
                text_content = BenchmarkEngine.extract_text_from_structured_data(extracted_data)
                accuracy = await asyncio.to_thread(
                    BenchmarkEngine.calculate_accuracy,
                    ground_truth,
                    text_content
                )

            return BenchmarkResult(
                tool=tool_name,
                execution_time_ms=round(exec_time_ms, 2),
                accuracy_score=round(accuracy, 4) if accuracy else None,
                extracted_text_length=len(str(extracted_data)) if extracted_data else 0,
                extracted_text=extracted_text,
                extracted_data=extracted_data,
                error=error_msg,
                features=TOOL_FEATURES.get(tool_name, [])
            )

        # Run all tools concurrently
        return await asyncio.gather(*(run_benchmark(tool) for tool in tools))

from typing import List, Optional
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
        ext_normalized = " ".join(extracted.split())
        
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
            extracted_text:str | None = None
            error_msg = None

            try:
                extractor_class = get_extractor(tool_name.value)

                # Heavy CPU work in thread
                extracted_text = await asyncio.to_thread(
                    extractor_class.extract, file_path
                )

            except Exception as e:
                error_msg = str(e)

            end_time = time.perf_counter()
            exec_time_ms = (end_time - start_time) * 1000

            # Accuracy (optional)
            accuracy = None
            if ground_truth and extracted_text and not error_msg:
                accuracy = await asyncio.to_thread(
                    BenchmarkEngine.calculate_accuracy,
                    ground_truth,
                    extracted_text
                )

            return BenchmarkResult(
                tool=tool_name,
                execution_time_ms=round(exec_time_ms, 2),
                accuracy_score=round(accuracy, 4) if accuracy else None,
                extracted_text_length=len(extracted_text) if extracted_text else 0,
                extracted_text=extracted_text,
                error=error_msg,
                features=TOOL_FEATURES.get(tool_name, [])
            )

        # Run all tools concurrently
        return await asyncio.gather(*(run_benchmark(tool) for tool in tools))

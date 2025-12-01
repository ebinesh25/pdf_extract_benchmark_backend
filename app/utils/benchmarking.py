import time
import difflib
from typing import List, Optional, Dict
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
    def calculate_accuracy(ground_truth: str, extracted_text: str) -> float:
        """
        Calculate similarity ratio between ground truth and extracted text.
        Returns a float between 0.0 and 1.0.
        """
        if not ground_truth or not extracted_text:
            return 0.0
        
        # Normalize text for better comparison (optional, but recommended)
        # For now, we'll do simple whitespace normalization
        gt_normalized = " ".join(ground_truth.split())
        ext_normalized = " ".join(extracted_text.split())
        
        return difflib.SequenceMatcher(None, gt_normalized, ext_normalized).ratio()

    @staticmethod
    def benchmark_file(
        file_path: str, 
        tools: List[ExtractionTool], 
        ground_truth: Optional[str] = None
    ) -> List[BenchmarkResult]:
        """
        Run benchmarking for the specified tools on the given file.
        """
        results = []

        for tool_name in tools:
            start_time = time.perf_counter()
            extracted_text = ""
            error_msg = None
            
            try:
                extractor_class = get_extractor(tool_name.value)
                # Instantiate if it's a class, or call static method directly if designed that way
                # Looking at pdf_extractors.py, they are classes with static 'extract' method
                # But get_extractor returns the class itself.
                extracted_text = extractor_class.extract(file_path)
            except Exception as e:
                error_msg = str(e)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000

            accuracy = None
            if ground_truth and not error_msg:
                accuracy = BenchmarkEngine.calculate_accuracy(ground_truth, extracted_text)

            results.append(BenchmarkResult(
                tool=tool_name,
                execution_time_ms=round(execution_time_ms, 2),
                accuracy_score=round(accuracy, 4) if accuracy is not None else None,
                extracted_text_length=len(extracted_text) if extracted_text else 0,
                error=error_msg,
                features=TOOL_FEATURES.get(tool_name, [])
            ))

        return results

Benchmarking Guide
==================

This document provides detailed information about the benchmarking capabilities of the PDF Extraction Backend.

Overview
--------

The benchmarking system allows you to compare the performance of different PDF extraction tools across various metrics:

* **Execution Time**: How fast each tool processes the document
* **Accuracy**: How accurately each tool extracts content (when ground truth is provided)
* **Text Length**: Amount of content extracted by each tool
* **Features**: Supported features for each tool
* **Cost**: Processing cost per page (currently all tools are free)

Benchmarking Endpoint
--------------------

The benchmarking endpoint allows you to run multiple extraction tools on the same PDF file and compare their performance.

.. http:post:: /benchmark

   Run selected extraction tools on a PDF file and compare their performance.

   **Request Parameters**:

   .. list-table:: Request Parameters
      :header-rows: 1

      * - Parameter
        - Type
        - Required
        - Description
      * - file
        - UploadFile
        - Yes
        - PDF file to benchmark
      * - tools
        - List[ExtractionTool]
        - Yes
        - List of tools to benchmark
      * - ground_truth
        - Optional[str]
        - No
        - Ground truth text for accuracy calculation

   **Example Request**:

   .. code-block:: bash

      curl -X POST "http://localhost:8000/api/v1/benchmark" \
           -H "accept: application/json" \
           -H "Content-Type: multipart/form-data" \
           -F "file=@document.pdf" \
           -F 'tools=["pymupdf", "pdfplumber", "pypdf", "pdfminer"]' \
           -F "ground_truth=This is the expected text content..."

Response Format
---------------

The benchmarking endpoint returns a comprehensive comparison of all tested tools:

.. code-block:: json

   {
     "filename": "document.pdf",
     "file_size_bytes": 1024000,
     "results": [
       {
         "tool": "pymupdf",
         "execution_time_ms": 150.5,
         "accuracy_score": 0.95,
         "extracted_text_length": 2500,
         "extracted_text": "Extracted text content...",
         "extracted_data": null,
         "error": null,
         "cost_per_page": "Free",
         "features": ["text", "images", "metadata"]
       },
       {
         "tool": "pdfplumber",
         "execution_time_ms": 200.3,
         "accuracy_score": 0.92,
         "extracted_text_length": 2450,
         "extracted_text": "Extracted text content...",
         "extracted_data": null,
         "error": null,
         "cost_per_page": "Free",
         "features": ["text", "tables", "metadata"]
       }
     ]
   }

Response Fields
~~~~~~~~~~~~~~~

* **filename**: Name of the benchmarked file
* **file_size_bytes**: Size of the file in bytes
* **results**: Array of benchmark results for each tool

For each tool result:

* **tool**: The extraction tool name
* **execution_time_ms**: Processing time in milliseconds
* **accuracy_score**: Accuracy score (0-1) when ground truth is provided
* **extracted_text_length**: Length of extracted text in characters
* **extracted_text**: The actual extracted text content
* **extracted_data**: Structured data (tables, metadata, etc.)
* **error**: Error message if extraction failed
* **cost_per_page**: Processing cost per page
* **features**: List of supported features

Performance Metrics
-------------------

Execution Time
~~~~~~~~~~~~~~

Execution time measures how long each tool takes to process the document:

* **Fast** (< 100ms): Excellent performance for real-time applications
* **Medium** (100-500ms): Good performance for most applications
* **Slow** (> 500ms): May impact user experience in real-time scenarios

**Typical Performance by Tool**:

.. list-table:: Expected Performance by Tool
   :header-rows: 1

   * - Tool
     - Small Files (< 1MB)
     - Medium Files (1-10MB)
     - Large Files (> 10MB)
   * - PyMuPDF
     - 50-100ms
     - 100-300ms
     - 300-1000ms
   * - pdfplumber
     - 100-200ms
     - 200-500ms
     - 500-1500ms
   * - pypdf
     - 30-80ms
     - 80-200ms
     - 200-800ms
   * - pdfminer.six
     - 200-400ms
     - 400-1000ms
     - 1000-3000ms

Accuracy Score
~~~~~~~~~~~~~~

When ground truth is provided, the system calculates an accuracy score using text similarity metrics:

* **Score Range**: 0.0 to 1.0
* **Excellent** (> 0.9): Very high accuracy
* **Good** (0.7-0.9): Acceptable accuracy for most use cases
* **Fair** (0.5-0.7): May require post-processing
* **Poor** (< 0.5): Significant differences from expected text

**Accuracy Calculation**:

The accuracy score is calculated using a combination of:

* **Text similarity**: Character and word-level similarity
* **Length similarity**: Comparison of extracted text length
* **Content overlap**: Common phrases and sentences

Feature Comparison
~~~~~~~~~~~~~~~~~

Each extraction tool supports different features:

.. list-table:: Feature Comparison
   :header-rows: 1

   * - Feature
     - PyMuPDF
     - pdfplumber
     - pypdf
     - pdfminer.six
   * - Text Extraction
     - ✓
     - ✓
     - ✓
     - ✓
   * - Table Extraction
     - ✓
     - ✓✓
     - ✓
     - ✓
   * - Image Extraction
     - ✓✓
     - ✗
     - ✗
     - ✗
   * - OCR Support
     - ✓✓
     - ✗
     - ✗
     - ✗
   * - Metadata
     - ✓✓
     - ✓
     - ✓
     - ✓✓
   * - Position Info
     - ✓
     - ✓✓
     - ✗
     - ✓✓
   * - Font Information
     - ✓
     - ✓
     - ✗
     - ✓✓

* ✓✓ = Excellent support
* ✓ = Good support
* ✗ = Not supported

Usage Examples
--------------

Python Benchmarking Client
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   import json
   from pathlib import Path

   class BenchmarkClient:
       def __init__(self, base_url="http://localhost:8000"):
           self.base_url = base_url
           self.api_prefix = "/api/v1"
       
       def benchmark_file(self, pdf_path, tools=None, ground_truth=None):
           """Benchmark a PDF file with specified tools."""
           if tools is None:
               tools = ["pymupdf", "pdfplumber", "pypdf", "pdfminer"]
           
           url = f"{self.base_url}{self.api_prefix}/benchmark"
           
           with open(pdf_path, 'rb') as f:
               files = {'file': f}
               data = {
                   'tools': json.dumps(tools),
               }
               if ground_truth:
                   data['ground_truth'] = ground_truth
               
               response = requests.post(url, files=files, data=data)
           
           return response.json()
       
       def compare_tools(self, pdf_path, ground_truth=None):
           """Compare all tools and return performance summary."""
           result = self.benchmark_file(pdf_path, ground_truth=ground_truth)
           
           if 'results' not in result:
               return result
           
           # Sort by execution time
           by_speed = sorted(result['results'], key=lambda x: x['execution_time_ms'])
           
           # Sort by accuracy (if available)
           by_accuracy = None
           if any(r.get('accuracy_score') for r in result['results']):
               by_accuracy = sorted(
                   [r for r in result['results'] if r.get('accuracy_score')],
                   key=lambda x: x['accuracy_score'],
                   reverse=True
               )
           
           return {
               'file_info': {
                   'filename': result['filename'],
                   'size_bytes': result['file_size_bytes']
               },
               'fastest_tool': by_speed[0]['tool'],
               'slowest_tool': by_speed[-1]['tool'],
               'most_accurate': by_accuracy[0]['tool'] if by_accuracy else None,
               'detailed_results': result['results']
           }
       
       def generate_report(self, pdf_path, output_file=None, ground_truth=None):
           """Generate a detailed benchmark report."""
           result = self.benchmark_file(pdf_path, ground_truth=ground_truth)
           
           report = []
           report.append(f"Benchmark Report for {result['filename']}")
           report.append(f"File Size: {result['file_size_bytes']:,} bytes")
           report.append("=" * 50)
           
           for tool_result in result['results']:
               report.append(f"\nTool: {tool_result['tool']}")
               report.append(f"  Execution Time: {tool_result['execution_time_ms']:.2f} ms")
               report.append(f"  Text Length: {tool_result['extracted_text_length']:,} chars")
               
               if tool_result.get('accuracy_score'):
                   report.append(f"  Accuracy Score: {tool_result['accuracy_score']:.3f}")
               
               if tool_result.get('error'):
                   report.append(f"  Error: {tool_result['error']}")
               else:
                   report.append(f"  Status: Success")
               
               report.append(f"  Features: {', '.join(tool_result['features'])}")
           
           report_text = '\n'.join(report)
           
           if output_file:
               with open(output_file, 'w') as f:
                   f.write(report_text)
           
           return report_text

   # Usage examples
   client = BenchmarkClient()
   
   # Basic benchmark
   result = client.benchmark_file('document.pdf')
   print(json.dumps(result, indent=2))
   
   # Compare tools with ground truth
   comparison = client.compare_tools('document.pdf', ground_truth="Expected text content...")
   print(f"Fastest tool: {comparison['fastest_tool']}")
   print(f"Most accurate: {comparison['most_accurate']}")
   
   # Generate detailed report
   report = client.generate_report('document.pdf', 'benchmark_report.txt')
   print(report)

Batch Benchmarking
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from concurrent.futures import ThreadPoolExecutor
   import pandas as pd

   def batch_benchmark(pdf_directory, output_csv='benchmark_results.csv'):
       """Benchmark all PDFs in a directory."""
       client = BenchmarkClient()
       pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
       
       all_results = []
       
       def benchmark_single(pdf_file):
           pdf_path = os.path.join(pdf_directory, pdf_file)
           try:
               result = client.benchmark_file(pdf_path)
               
               # Extract summary metrics
               for tool_result in result['results']:
                   all_results.append({
                       'filename': pdf_file,
                       'file_size': result['file_size_bytes'],
                       'tool': tool_result['tool'],
                       'execution_time_ms': tool_result['execution_time_ms'],
                       'text_length': tool_result['extracted_text_length'],
                       'accuracy_score': tool_result.get('accuracy_score'),
                       'error': tool_result.get('error'),
                       'status': 'success' if not tool_result.get('error') else 'error'
                   })
           except Exception as e:
               print(f"Error benchmarking {pdf_file}: {e}")
       
       # Run benchmarks in parallel
       with ThreadPoolExecutor(max_workers=4) as executor:
           executor.map(benchmark_single, pdf_files)
       
       # Save to CSV
       df = pd.DataFrame(all_results)
       df.to_csv(output_csv, index=False)
       
       return df

   # Usage
   results_df = batch_benchmark('./test_pdfs/')
   print(results_df.head())

JavaScript Benchmarking Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   class BenchmarkClient {
       constructor(baseUrl = 'http://localhost:8000') {
           this.baseUrl = baseUrl;
           this.apiPrefix = '/api/v1';
       }
       
       async benchmarkFile(pdfFile, tools = null, groundTruth = null) {
           const url = `${this.baseUrl}${this.apiPrefix}/benchmark`;
           const formData = new FormData();
           
           formData.append('file', pdfFile);
           formData.append('tools', JSON.stringify(tools || ['pymupdf', 'pdfplumber', 'pypdf', 'pdfminer']));
           
           if (groundTruth) {
               formData.append('ground_truth', groundTruth);
           }
           
           const response = await fetch(url, {
               method: 'POST',
               body: formData
           });
           
           return await response.json();
       }
       
       async compareTools(pdfFile, groundTruth = null) {
           const result = await this.benchmarkFile(pdfFile, null, groundTruth);
           
           if (!result.results) {
               return result;
           }
           
           // Sort by execution time
           const bySpeed = [...result.results].sort((a, b) => a.execution_time_ms - b.execution_time_ms);
           
           // Sort by accuracy (if available)
           let byAccuracy = null;
           const withAccuracy = result.results.filter(r => r.accuracy_score !== null);
           if (withAccuracy.length > 0) {
               byAccuracy = [...withAccuracy].sort((a, b) => b.accuracy_score - a.accuracy_score);
           }
           
           return {
               fileInfo: {
                   filename: result.filename,
                   sizeBytes: result.file_size_bytes
               },
               fastestTool: bySpeed[0].tool,
               slowestTool: bySpeed[bySpeed.length - 1].tool,
               mostAccurate: byAccuracy ? byAccuracy[0].tool : null,
               detailedResults: result.results
           };
       }
       
       generateReport(result) {
           let report = [];
           report.push(`Benchmark Report for ${result.filename}`);
           report.push(`File Size: ${result.file_size_bytes.toLocaleString()} bytes`);
           report.push('='.repeat(50));
           
           result.results.forEach(toolResult => {
               report.push(`\nTool: ${toolResult.tool}`);
               report.push(`  Execution Time: ${toolResult.execution_time_ms.toFixed(2)} ms`);
               report.push(`  Text Length: ${toolResult.extracted_text_length.toLocaleString()} chars`);
               
               if (toolResult.accuracy_score !== null) {
                   report.push(`  Accuracy Score: ${toolResult.accuracy_score.toFixed(3)}`);
               }
               
               if (toolResult.error) {
                   report.push(`  Error: ${toolResult.error}`);
               } else {
                   report.push('  Status: Success');
               }
               
               report.push(`  Features: ${toolResult.features.join(', ')}`);
           });
           
           return report.join('\n');
       }
   }

   // Usage example
   const client = new BenchmarkClient();
   
   document.getElementById('benchmark-form').addEventListener('submit', async (e) => {
       e.preventDefault();
       
       const fileInput = document.getElementById('pdf-file');
       const groundTruthInput = document.getElementById('ground-truth');
       const resultsDiv = document.getElementById('results');
       
       const comparison = await client.compareTools(
           fileInput.files[0],
           groundTruthInput.value
       );
       
       resultsDiv.innerHTML = `
           <h3>Benchmark Results</h3>
           <p>Fastest Tool: <strong>${comparison.fastestTool}</strong></p>
           <p>Most Accurate: <strong>${comparison.mostAccurate || 'N/A'}</strong></p>
           <pre>${client.generateReport(comparison.detailedResults)}</pre>
       `;
   });

cURL Examples
~~~~~~~~~~~~~

.. code-block:: bash

   # Benchmark all tools
   curl -X POST "http://localhost:8000/api/v1/benchmark" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf" \
        -F 'tools=["pymupdf", "pdfplumber", "pypdf", "pdfminer"]'

   # Benchmark specific tools with ground truth
   curl -X POST "http://localhost:8000/api/v1/benchmark" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf" \
        -F 'tools=["pymupdf", "pdfplumber"]' \
        -F "ground_truth=This is the expected text content for accuracy calculation."

   # Save results to file
   curl -X POST "http://localhost:8000/api/v1/benchmark" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf" \
        -F 'tools=["pymupdf", "pdfplumber"]' \
        | jq '.' > benchmark_results.json

Benchmarking Strategies
-----------------------

Tool Selection Strategy
~~~~~~~~~~~~~~~~~~~~~~~

Based on benchmarking results, here are recommended strategies for different use cases:

**Performance-Critical Applications**:
1. Use **pypdf** for simple text extraction (fastest)
2. Use **PyMuPDF** for complex documents (good balance of speed and features)
3. Avoid **pdfminer.six** for real-time applications

**Accuracy-Critical Applications**:
1. Use **PyMuPDF** for general documents
2. Use **pdfplumber** for documents with tables
3. Use **pdfminer.six** for detailed text analysis

**Feature-Rich Applications**:
1. Use **PyMuPDF** for OCR and image extraction
2. Use **pdfplumber** for table extraction
3. Use **pdfminer.six** for font and positioning information

Document Type Recommendations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Tool Recommendations by Document Type
   :header-rows: 1

   * - Document Type
     - Primary Tool
     - Secondary Tool
     - Reason
   * - Simple text documents
     - pypdf
     - PyMuPDF
     - Fast and lightweight
   * - Financial statements
     - pdfplumber
     - PyMuPDF
     - Excellent table extraction
   * - Scanned documents
     - PyMuPDF
     - pdfplumber
     - OCR support
   * - Academic papers
     - pdfminer.six
     - PyMuPDF
     - Detailed text analysis
   * - Legal documents
     - PyMuPDF
     - pdfminer.six
     - Good accuracy and metadata
   * - Image-heavy PDFs
     - PyMuPDF
     - pdfplumber
     - Image extraction support

Performance Optimization
------------------------

Caching Strategy
~~~~~~~~~~~~~~~~

Implement caching to avoid repeated benchmarking:

.. code-block:: python

   import hashlib
   import json
   from pathlib import Path

   class CachedBenchmarkClient(BenchmarkClient):
       def __init__(self, base_url="http://localhost:8000", cache_dir="./benchmark_cache"):
           super().__init__(base_url)
           self.cache_dir = Path(cache_dir)
           self.cache_dir.mkdir(exist_ok=True)
       
       def _get_file_hash(self, pdf_path):
           """Generate hash for file content."""
           with open(pdf_path, 'rb') as f:
               return hashlib.md5(f.read()).hexdigest()
       
       def _get_cache_path(self, pdf_path, tools, ground_truth):
           """Generate cache file path."""
           file_hash = self._get_file_hash(pdf_path)
           tools_str = '_'.join(sorted(tools))
           cache_key = f"{file_hash}_{tools_str}"
           
           if ground_truth:
               gt_hash = hashlib.md5(ground_truth.encode()).hexdigest()
               cache_key += f"_{gt_hash}"
           
           return self.cache_dir / f"{cache_key}.json"
       
       def benchmark_file(self, pdf_path, tools=None, ground_truth=None):
           """Benchmark with caching."""
           if tools is None:
               tools = ["pymupdf", "pdfplumber", "pypdf", "pdfminer"]
           
           cache_path = self._get_cache_path(pdf_path, tools, ground_truth)
           
           # Check cache first
           if cache_path.exists():
               with open(cache_path, 'r') as f:
                   return json.load(f)
           
           # Run benchmark
           result = super().benchmark_file(pdf_path, tools, ground_truth)
           
           # Cache the result
           with open(cache_path, 'w') as f:
               json.dump(result, f)
           
           return result

Parallel Processing
~~~~~~~~~~~~~~~~~~~

For batch benchmarking, use parallel processing:

.. code-block:: python

   from concurrent.futures import ProcessPoolExecutor
   import multiprocessing

   def parallel_benchmark(pdf_files, max_workers=None):
       """Run benchmarks in parallel across multiple processes."""
       if max_workers is None:
           max_workers = multiprocessing.cpu_count()
       
       client = BenchmarkClient()
       
       def benchmark_single(pdf_path):
           try:
               return client.benchmark_file(pdf_path)
           except Exception as e:
               return {"error": str(e), "filename": pdf_path}
       
       with ProcessPoolExecutor(max_workers=max_workers) as executor:
           results = list(executor.map(benchmark_single, pdf_files))
       
       return results

Monitoring and Analytics
------------------------

Benchmark Metrics Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Track benchmarking metrics over time:

.. code-block:: python

   import sqlite3
   from datetime import datetime

   class BenchmarkTracker:
       def __init__(self, db_path="benchmark_metrics.db"):
           self.db_path = db_path
           self._init_db()
       
       def _init_db(self):
           """Initialize database schema."""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           
           cursor.execute('''
               CREATE TABLE IF NOT EXISTS benchmarks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp DATETIME,
                   filename TEXT,
                   file_size INTEGER,
                   tool TEXT,
                   execution_time_ms REAL,
                   accuracy_score REAL,
                   text_length INTEGER,
                   status TEXT,
                   error_message TEXT
               )
           ''')
           
           conn.commit()
           conn.close()
       
       def record_benchmark(self, result):
           """Record benchmark results to database."""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           
           timestamp = datetime.now()
           
           for tool_result in result['results']:
               cursor.execute('''
                   INSERT INTO benchmarks 
                   (timestamp, filename, file_size, tool, execution_time_ms, 
                    accuracy_score, text_length, status, error_message)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ''', (
                   timestamp,
                   result['filename'],
                   result['file_size_bytes'],
                   tool_result['tool'],
                   tool_result['execution_time_ms'],
                   tool_result.get('accuracy_score'),
                   tool_result['extracted_text_length'],
                   'success' if not tool_result.get('error') else 'error',
                   tool_result.get('error')
               ))
           
           conn.commit()
           conn.close()
       
       def get_performance_trends(self, tool, days=30):
           """Get performance trends for a specific tool."""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           
           cursor.execute('''
               SELECT DATE(timestamp) as date, 
                      AVG(execution_time_ms) as avg_time,
                      AVG(accuracy_score) as avg_accuracy,
                      COUNT(*) as benchmark_count
               FROM benchmarks 
               WHERE tool = ? 
               AND timestamp > datetime('now', '-{} days')
               GROUP BY DATE(timestamp)
               ORDER BY date
           '''.format(days), (tool,))
           
           return cursor.fetchall()
           conn.close()

Troubleshooting
---------------

Common Benchmarking Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Memory errors with large files**
   * Reduce the number of tools in a single benchmark
   * Process files sequentially instead of in parallel
   * Increase available system memory

2. **Inconsistent accuracy scores**
   * Ensure ground truth is comprehensive and accurate
   * Check for encoding issues in ground truth text
   * Consider using multiple ground truth samples

3. **Timeout errors**
   * Increase timeout settings for large files
   * Implement progress tracking for long-running benchmarks
   * Consider splitting large documents into chunks

4. **Cache invalidation issues**
   * Implement proper cache invalidation strategies
   * Use file modification time for cache validation
   * Consider content-based hashing for cache keys

For more information about the extraction tools and their specific features, see the :doc:`extraction` documentation.
Usage Examples
==============

This document provides practical examples of how to use the PDF Extraction Backend API for various use cases.

Basic Usage
-----------

Simple Text Extraction
~~~~~~~~~~~~~~~~~~~~~~

Extract text from a PDF using PyMuPDF:

.. code-block:: python

   import requests

   # Simple text extraction
   with open('document.pdf', 'rb') as f:
       files = {'file': f}
       response = requests.post(
           'http://localhost:8000/api/v1/extract/pymupdf',
           files=files
       )
   
   result = response.json()
   
   if result['status'] == 'success':
       # Extract all text content
       text_content = []
       for item in result['data']:
           if item['type'] == 'text':
               text_content.append(item['content'])
       
       full_text = '\n'.join(text_content)
       print(f"Extracted {len(full_text)} characters of text")
   else:
       print(f"Extraction failed: {result['error']}")

Extract Specific Content Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract different types of content from a PDF:

.. code-block:: python

   import requests
   import json

   def extract_content(pdf_path, tool='pymupdf'):
       """Extract and categorize content from PDF."""
       with open(pdf_path, 'rb') as f:
           files = {'file': f}
           response = requests.post(
               f'http://localhost:8000/api/v1/extract/{tool}',
               files=files
           )
       
       result = response.json()
       
       if result['status'] != 'success':
           return None
       
       # Categorize content
       categorized = {
           'text': [],
           'tables': [],
           'metadata': [],
           'images': []
       }
       
       for item in result['data']:
           content_type = item['type']
           if content_type in categorized:
               categorized[content_type].append(item['content'])
       
       return categorized

   # Usage
   content = extract_content('document.pdf')
   
   if content:
       print(f"Text sections: {len(content['text'])}")
       print(f"Tables found: {len(content['tables'])}")
       print(f"Metadata items: {len(content['metadata'])}")
       print(f"Images found: {len(content['images'])}")

Advanced Examples
-----------------

Batch Processing
~~~~~~~~~~~~~~~

Process multiple PDF files in batch:

.. code-block:: python

   import os
   import requests
   from concurrent.futures import ThreadPoolExecutor
   import json
   from pathlib import Path

   class BatchProcessor:
       def __init__(self, base_url="http://localhost:8000", max_workers=4):
           self.base_url = base_url
           self.max_workers = max_workers
       
       def process_single_file(self, pdf_path, tool='pymupdf'):
           """Process a single PDF file."""
           try:
               with open(pdf_path, 'rb') as f:
                   files = {'file': f}
                   response = requests.post(
                       f'{self.base_url}/api/v1/extract/{tool}',
                       files=files,
                       timeout=30
                   )
               
               result = response.json()
               return {
                   'file': pdf_path.name,
                   'status': result['status'],
                   'tool': tool,
                   'result': result
               }
           except Exception as e:
               return {
                   'file': pdf_path.name,
                   'status': 'error',
                   'tool': tool,
                   'error': str(e)
               }
       
       def process_directory(self, directory_path, tool='pymupdf'):
           """Process all PDFs in a directory."""
           pdf_files = list(Path(directory_path).glob('*.pdf'))
           
           with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
               futures = [
                   executor.submit(self.process_single_file, pdf_file, tool)
                   for pdf_file in pdf_files
               ]
               
               results = [future.result() for future in futures]
           
           return results
       
       def save_results(self, results, output_file):
           """Save batch processing results to JSON file."""
           with open(output_file, 'w') as f:
               json.dump(results, f, indent=2)
           
           # Print summary
           successful = sum(1 for r in results if r['status'] == 'success')
           total = len(results)
           print(f"Processed {successful}/{total} files successfully")

   # Usage
   processor = BatchProcessor()
   results = processor.process_directory('./pdfs/', tool='pymupdf')
   processor.save_results(results, 'batch_results.json')

Tool Comparison
~~~~~~~~~~~~~~~

Compare extraction results from different tools:

.. code-block:: python

   import requests
   import json
   from concurrent.futures import ThreadPoolExecutor

   class ToolComparator:
       def __init__(self, base_url="http://localhost:8000"):
           self.base_url = base_url
           self.tools = ['pymupdf', 'pdfplumber', 'pypdf', 'pdfminer']
       
       def extract_with_tool(self, pdf_path, tool):
           """Extract PDF using specified tool."""
           try:
               with open(pdf_path, 'rb') as f:
                   files = {'file': f}
                   response = requests.post(
                       f'{self.base_url}/api/v1/extract/{tool}',
                       files=files,
                       timeout=30
                   )
               
               result = response.json()
               return {
                   'tool': tool,
                   'status': result['status'],
                   'text_length': sum(
                       len(item['content']) 
                       for item in result.get('data', []) 
                       if item['type'] == 'text'
                   ),
                   'data_count': len(result.get('data', [])),
                   'error': result.get('error'),
                   'raw_result': result
               }
           except Exception as e:
               return {
                   'tool': tool,
                   'status': 'error',
                   'error': str(e),
                   'text_length': 0,
                   'data_count': 0
               }
       
       def compare_tools(self, pdf_path):
           """Compare all tools on a single PDF."""
           with ThreadPoolExecutor(max_workers=4) as executor:
               futures = [
                   executor.submit(self.extract_with_tool, pdf_path, tool)
                   for tool in self.tools
               ]
               
               results = {future.result()['tool']: future.result() for future in futures}
           
           # Generate comparison report
           successful_tools = [
               tool for tool, result in results.items() 
               if result['status'] == 'success'
           ]
           
           if successful_tools:
               max_text = max(results[tool]['text_length'] for tool in successful_tools)
               best_tool = max(
                   successful_tools, 
                   key=lambda tool: results[tool]['text_length']
               )
           else:
               max_text = 0
               best_tool = None
           
           return {
               'file': pdf_path.name,
               'successful_tools': successful_tools,
               'best_tool_for_text': best_tool,
               'max_text_length': max_text,
               'detailed_results': results
           }
       
       def generate_comparison_report(self, comparison_result):
           """Generate a readable comparison report."""
           report = []
           report.append(f"Comparison Report for {comparison_result['file']}")
           report.append("=" * 50)
           
           if comparison_result['successful_tools']:
               report.append(f"Successful extractions: {', '.join(comparison_result['successful_tools'])}")
               report.append(f"Best tool for text extraction: {comparison_result['best_tool_for_text']}")
               report.append(f"Maximum text length: {comparison_result['max_text_length']} characters")
           else:
               report.append("No tools successfully extracted content")
           
           report.append("\nDetailed Results:")
           for tool, result in comparison_result['detailed_results'].items():
               report.append(f"\n{tool.upper()}:")
               report.append(f"  Status: {result['status']}")
               if result['status'] == 'success':
                   report.append(f"  Text Length: {result['text_length']} characters")
                   report.append(f"  Data Items: {result['data_count']}")
               else:
                   report.append(f"  Error: {result['error']}")
           
           return '\n'.join(report)

   # Usage
   comparator = ToolComparator()
   comparison = comparator.compare_tools('document.pdf')
   report = comparator.generate_comparison_report(comparison)
   print(report)

Content Analysis
~~~~~~~~~~~~~~~~

Analyze extracted content for specific patterns:

.. code-block:: python

   import re
   import requests
   from collections import Counter

   class ContentAnalyzer:
       def __init__(self, base_url="http://localhost:8000"):
           self.base_url = base_url
       
       def extract_and_analyze(self, pdf_path, tool='pymupdf'):
           """Extract content and perform analysis."""
           # Extract content
           with open(pdf_path, 'rb') as f:
               files = {'file': f}
               response = requests.post(
                   f'{self.base_url}/api/v1/extract/{tool}',
                   files=files
               )
           
           result = response.json()
           
           if result['status'] != 'success':
               return None
           
           # Combine all text content
           all_text = '\n'.join([
               item['content'] 
               for item in result['data'] 
               if item['type'] == 'text'
           ])
           
           # Perform analysis
           analysis = {
               'word_count': len(all_text.split()),
               'char_count': len(all_text),
               'line_count': len(all_text.split('\n')),
               'email_addresses': self.extract_emails(all_text),
               'phone_numbers': self.extract_phone_numbers(all_text),
               'urls': self.extract_urls(all_text),
               'keywords': self.extract_keywords(all_text),
               'sentences': self.extract_sentences(all_text)
           }
           
           return {
               'file': pdf_path.name,
               'tool': tool,
               'extraction_result': result,
               'analysis': analysis
           }
       
       def extract_emails(self, text):
           """Extract email addresses from text."""
           email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
           return re.findall(email_pattern, text)
       
       def extract_phone_numbers(self, text):
           """Extract phone numbers from text."""
           phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
           return re.findall(phone_pattern, text)
       
       def extract_urls(self, text):
           """Extract URLs from text."""
           url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
           return re.findall(url_pattern, text)
       
       def extract_keywords(self, text, top_n=10):
           """Extract most common keywords from text."""
           # Simple keyword extraction (remove common words)
           common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
           words = [
               word.lower() for word in text.split() 
               if word.isalpha() and word.lower() not in common_words and len(word) > 3
           ]
           word_freq = Counter(words)
           return word_freq.most_common(top_n)
       
       def extract_sentences(self, text, max_sentences=5):
           """Extract first few sentences from text."""
           sentences = re.split(r'[.!?]+', text)
           sentences = [s.strip() for s in sentences if s.strip()]
           return sentences[:max_sentences]

   # Usage
   analyzer = ContentAnalyzer()
   analysis = analyzer.extract_and_analyze('document.pdf')
   
   if analysis:
       print(f"Analysis for {analysis['file']}:")
       print(f"Words: {analysis['analysis']['word_count']}")
       print(f"Characters: {analysis['analysis']['char_count']}")
       print(f"Emails found: {len(analysis['analysis']['email_addresses'])}")
       print(f"Phone numbers found: {len(analysis['analysis']['phone_numbers'])}")
       print(f"URLs found: {len(analysis['analysis']['urls'])}")
       print(f"Top keywords: {analysis['analysis']['keywords'][:5]}")

Benchmarking Examples
---------------------

Performance Benchmarking
~~~~~~~~~~~~~~~~~~~~~~~~~

Run comprehensive benchmarks on multiple files:

.. code-block:: python

   import requests
   import json
   import time
   from pathlib import Path
   import pandas as pd

   class PerformanceBenchmark:
       def __init__(self, base_url="http://localhost:8000"):
           self.base_url = base_url
           self.tools = ['pymupdf', 'pdfplumber', 'pypdf', 'pdfminer']
       
       def benchmark_single_file(self, pdf_path):
           """Benchmark all tools on a single file."""
           results = {}
           
           for tool in self.tools:
               try:
                   start_time = time.time()
                   
                   with open(pdf_path, 'rb') as f:
                       files = {'file': f}
                       response = requests.post(
                           f'{self.base_url}/api/v1/extract/{tool}',
                           files=files,
                           timeout=60
                       )
                   
                   end_time = time.time()
                   execution_time = (end_time - start_time) * 1000  # Convert to ms
                   
                   result = response.json()
                   
                   results[tool] = {
                       'execution_time_ms': execution_time,
                       'status': result['status'],
                       'text_length': sum(
                           len(item['content']) 
                           for item in result.get('data', []) 
                           if item['type'] == 'text'
                       ),
                       'data_items': len(result.get('data', [])),
                       'error': result.get('error')
                   }
                   
               except Exception as e:
                   results[tool] = {
                       'execution_time_ms': 0,
                       'status': 'error',
                       'text_length': 0,
                       'data_items': 0,
                       'error': str(e)
                   }
           
           return {
               'file': pdf_path.name,
               'file_size_bytes': pdf_path.stat().st_size,
               'results': results
           }
       
       def benchmark_directory(self, directory_path, output_csv='benchmark_results.csv'):
           """Benchmark all PDFs in a directory."""
           pdf_files = list(Path(directory_path).glob('*.pdf'))
           all_results = []
           
           for pdf_file in pdf_files:
               print(f"Benchmarking {pdf_file.name}...")
               result = self.benchmark_single_file(pdf_file)
               all_results.append(result)
           
           # Convert to DataFrame for analysis
           df_data = []
           for result in all_results:
               for tool, tool_result in result['results'].items():
                   df_data.append({
                       'file': result['file'],
                       'file_size': result['file_size_bytes'],
                       'tool': tool,
                       'execution_time_ms': tool_result['execution_time_ms'],
                       'status': tool_result['status'],
                       'text_length': tool_result['text_length'],
                       'data_items': tool_result['data_items'],
                       'error': tool_result['error']
                   })
           
           df = pd.DataFrame(df_data)
           df.to_csv(output_csv, index=False)
           
           # Generate summary statistics
           summary = self.generate_summary(df)
           
           return {
               'detailed_results': all_results,
               'summary': summary,
               'dataframe': df
           }
       
       def generate_summary(self, df):
           """Generate summary statistics from benchmark results."""
           summary = {}
           
           # Success rate by tool
           success_rate = df.groupby('tool')['status'].apply(
               lambda x: (x == 'success').mean()
           )
           summary['success_rate'] = success_rate.to_dict()
           
           # Average execution time by tool
           avg_time = df[df['status'] == 'success'].groupby('tool')['execution_time_ms'].mean()
           summary['average_execution_time'] = avg_time.to_dict()
           
           # Average text length by tool
           avg_text_length = df[df['status'] == 'success'].groupby('tool')['text_length'].mean()
           summary['average_text_length'] = avg_text_length.to_dict()
           
           # Fastest tool (average)
           if not avg_time.empty:
               summary['fastest_tool'] = avg_time.idxmin()
               summary['slowest_tool'] = avg_time.idxmax()
           
           return summary

   # Usage
   benchmark = PerformanceBenchmark()
   results = benchmark.benchmark_directory('./test_pdfs/', 'performance_benchmark.csv')
   
   print("Benchmark Summary:")
   print(f"Success rates: {results['summary']['success_rate']}")
   print(f"Average execution times: {results['summary']['average_execution_time']}")
   print(f"Fastest tool: {results['summary']['fastest_tool']}")

Accuracy Benchmarking
~~~~~~~~~~~~~~~~~~~~

Benchmark with ground truth for accuracy measurement:

.. code-block:: python

   import requests
   import json
   from difflib import SequenceMatcher

   class AccuracyBenchmark:
       def __init__(self, base_url="http://localhost:8000"):
           self.base_url = base_url
           self.tools = ['pymupdf', 'pdfplumber', 'pypdf', 'pdfminer']
       
       def calculate_similarity(self, text1, text2):
           """Calculate text similarity score."""
           return SequenceMatcher(None, text1, text2).ratio()
       
       def benchmark_with_ground_truth(self, pdf_path, ground_truth_text):
           """Benchmark tools against ground truth."""
           results = {}
           
           for tool in self.tools:
               try:
                   with open(pdf_path, 'rb') as f:
                       files = {'file': f}
                       response = requests.post(
                           f'{self.base_url}/api/v1/extract/{tool}',
                           files=files
                       )
                   
                   result = response.json()
                   
                   if result['status'] == 'success':
                       # Extract all text
                       extracted_text = '\n'.join([
                           item['content'] 
                           for item in result.get('data', []) 
                           if item['type'] == 'text'
                       ])
                       
                       # Calculate accuracy metrics
                       similarity = self.calculate_similarity(extracted_text, ground_truth_text)
                       
                       results[tool] = {
                           'status': 'success',
                           'similarity_score': similarity,
                           'extracted_length': len(extracted_text),
                           'ground_truth_length': len(ground_truth_text),
                           'length_ratio': len(extracted_text) / len(ground_truth_text) if ground_truth_text else 0,
                           'extracted_text': extracted_text[:500] + '...' if len(extracted_text) > 500 else extracted_text
                       }
                   else:
                       results[tool] = {
                           'status': 'error',
                           'error': result.get('error'),
                           'similarity_score': 0,
                           'extracted_length': 0,
                           'ground_truth_length': len(ground_truth_text),
                           'length_ratio': 0
                       }
                       
               except Exception as e:
                   results[tool] = {
                       'status': 'error',
                       'error': str(e),
                       'similarity_score': 0,
                       'extracted_length': 0,
                       'ground_truth_length': len(ground_truth_text),
                       'length_ratio': 0
                   }
           
           # Find best tool
           successful_results = {k: v for k, v in results.items() if v['status'] == 'success'}
           if successful_results:
               best_tool = max(successful_results.keys(), key=lambda k: successful_results[k]['similarity_score'])
           else:
               best_tool = None
           
           return {
               'file': pdf_path.name,
               'ground_truth_length': len(ground_truth_text),
               'best_tool': best_tool,
               'results': results
           }
       
       def generate_accuracy_report(self, benchmark_result):
           """Generate a detailed accuracy report."""
           report = []
           report.append(f"Accuracy Benchmark for {benchmark_result['file']}")
           report.append(f"Ground Truth Length: {benchmark_result['ground_truth_length']} characters")
           report.append("=" * 60)
           
           if benchmark_result['best_tool']:
               report.append(f"Best performing tool: {benchmark_result['best_tool']}")
           else:
               report.append("No tool successfully extracted content")
           
           report.append("\nDetailed Results:")
           for tool, result in benchmark_result['results'].items():
               report.append(f"\n{tool.upper()}:")
               report.append(f"  Status: {result['status']}")
               
               if result['status'] == 'success':
                   report.append(f"  Similarity Score: {result['similarity_score']:.3f}")
                   report.append(f"  Extracted Length: {result['extracted_length']} characters")
                   report.append(f"  Length Ratio: {result['length_ratio']:.3f}")
                   report.append(f"  Sample Text: {result['extracted_text'][:200]}...")
               else:
                   report.append(f"  Error: {result['error']}")
           
           return '\n'.join(report)

   # Usage
   accuracy_benchmark = AccuracyBenchmark()
   
   # Example with ground truth
   ground_truth = """
   This is a sample PDF document for testing extraction accuracy.
   It contains multiple paragraphs and various text elements.
   The purpose is to evaluate how well different extraction tools perform.
   """
   
   result = accuracy_benchmark.benchmark_with_ground_truth('test_document.pdf', ground_truth)
   report = accuracy_benchmark.generate_accuracy_report(result)
   print(report)

Web Interface Examples
-----------------------

JavaScript/HTML Client
~~~~~~~~~~~~~~~~~~~~~~

Complete web interface for PDF extraction:

.. code-block:: html

   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>PDF Extraction Tool</title>
       <style>
           body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
           .container { display: flex; gap: 20px; }
           .upload-section { flex: 1; }
           .results-section { flex: 1; }
           .tool-selector { margin: 20px 0; }
           .result-item { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
           .loading { display: none; color: blue; }
           .error { color: red; }
           .success { color: green; }
           textarea { width: 100%; height: 200px; }
           button { padding: 10px 20px; margin: 5px; }
       </style>
   </head>
   <body>
       <h1>PDF Extraction Tool</h1>
       
       <div class="container">
           <div class="upload-section">
               <h2>Upload PDF</h2>
               <input type="file" id="pdfFile" accept=".pdf">
               
               <div class="tool-selector">
                   <h3>Select Extraction Tool:</h3>
                   <label><input type="radio" name="tool" value="pymupdf" checked> PyMuPDF</label>
                   <label><input type="radio" name="tool" value="pdfplumber"> pdfplumber</label>
                   <label><input type="radio" name="tool" value="pypdf"> pypdf</label>
                   <label><input type="radio" name="tool" value="pdfminer"> pdfminer</label>
               </div>
               
               <button onclick="extractPDF()">Extract Text</button>
               <button onclick="benchmarkAll()">Benchmark All Tools</button>
               
               <div class="loading" id="loading">Processing...</div>
               <div class="error" id="error"></div>
           </div>
           
           <div class="results-section">
               <h2>Results</h2>
               <div id="results"></div>
           </div>
       </div>

       <script>
           const API_BASE = 'http://localhost:8000/api/v1';
           
           async function extractPDF() {
               const file = document.getElementById('pdfFile').files[0];
               if (!file) {
                   showError('Please select a PDF file');
                   return;
               }
               
               const tool = document.querySelector('input[name="tool"]:checked').value;
               showLoading(true);
               clearError();
               clearResults();
               
               try {
                   const formData = new FormData();
                   formData.append('file', file);
                   
                   const response = await fetch(`${API_BASE}/extract/${tool}`, {
                       method: 'POST',
                       body: formData
                   });
                   
                   const result = await response.json();
                   displayResult(result, tool);
                   
               } catch (error) {
                   showError(`Error: ${error.message}`);
               } finally {
                   showLoading(false);
               }
           }
           
           async function benchmarkAll() {
               const file = document.getElementById('pdfFile').files[0];
               if (!file) {
                   showError('Please select a PDF file');
                   return;
               }
               
               showLoading(true);
               clearError();
               clearResults();
               
               try {
                   const formData = new FormData();
                   formData.append('file', file);
                   formData.append('tools', JSON.stringify(['pymupdf', 'pdfplumber', 'pypdf', 'pdfminer']));
                   
                   const response = await fetch(`${API_BASE}/benchmark`, {
                       method: 'POST',
                       body: formData
                   });
                   
                   const result = await response.json();
                   displayBenchmarkResults(result);
                   
               } catch (error) {
                   showError(`Error: ${error.message}`);
               } finally {
                   showLoading(false);
               }
           }
           
           function displayResult(result, tool) {
               const resultsDiv = document.getElementById('results');
               
               if (result.status === 'success') {
                   let html = `<div class="result-item success">`;
                   html += `<h3>Extraction with ${tool}</h3>`;
                   html += `<p>Status: ${result.status}</p>`;
                   
                   // Display different content types
                   const textContent = result.data.filter(item => item.type === 'text');
                   const tableContent = result.data.filter(item => item.type === 'table');
                   const metadataContent = result.data.filter(item => item.type === 'metadata');
                   
                   if (textContent.length > 0) {
                       html += `<h4>Text Content:</h4>`;
                       html += `<textarea readonly>${textContent.map(item => item.content).join('\n\n')}</textarea>`;
                   }
                   
                   if (tableContent.length > 0) {
                       html += `<h4>Tables:</h4>`;
                       tableContent.forEach(item => {
                           html += `<pre>${item.content}</pre>`;
                       });
                   }
                   
                   if (metadataContent.length > 0) {
                       html += `<h4>Metadata:</h4>`;
                       html += `<pre>${metadataContent.map(item => item.content).join('\n')}</pre>`;
                   }
                   
                   html += `</div>`;
                   resultsDiv.innerHTML = html;
               } else {
                   showError(`Extraction failed: ${result.error}`);
               }
           }
           
           function displayBenchmarkResults(result) {
               const resultsDiv = document.getElementById('results');
               
               let html = `<div class="result-item">`;
               html += `<h3>Benchmark Results for ${result.filename}</h3>`;
               html += `<p>File Size: ${(result.file_size_bytes / 1024 / 1024).toFixed(2)} MB</p>`;
               
               // Sort by execution time
               const sortedResults = result.results.sort((a, b) => a.execution_time_ms - b.execution_time_ms);
               
               html += `<h4>Performance Comparison:</h4>`;
               html += `<table border="1" style="width: 100%; border-collapse: collapse;">`;
               html += `<tr><th>Tool</th><th>Time (ms)</th><th>Text Length</th><th>Status</th></tr>`;
               
               sortedResults.forEach(toolResult => {
                   html += `<tr>`;
                   html += `<td>${toolResult.tool}</td>`;
                   html += `<td>${toolResult.execution_time_ms.toFixed(2)}</td>`;
                   html += `<td>${toolResult.extracted_text_length.toLocaleString()}</td>`;
                   html += `<td>${toolResult.error ? 'Error' : 'Success'}</td>`;
                   html += `</tr>`;
               });
               
               html += `</table>`;
               html += `</div>`;
               
               resultsDiv.innerHTML = html;
           }
           
           function showLoading(show) {
               document.getElementById('loading').style.display = show ? 'block' : 'none';
           }
           
           function showError(message) {
               document.getElementById('error').textContent = message;
           }
           
           function clearError() {
               document.getElementById('error').textContent = '';
           }
           
           function clearResults() {
               document.getElementById('results').innerHTML = '';
           }
       </script>
   </body>
   </html>

React Component Example
~~~~~~~~~~~~~~~~~~~~~~~

React component for PDF extraction:

.. code-block:: jsx

   import React, { useState } from 'react';
   
   const PDFExtractor = () => {
       const [file, setFile] = useState(null);
       const [selectedTool, setSelectedTool] = useState('pymupdf');
       const [results, setResults] = useState(null);
       const [loading, setLoading] = useState(false);
       const [error, setError] = useState(null);
       
       const tools = ['pymupdf', 'pdfplumber', 'pypdf', 'pdfminer'];
       
       const handleFileChange = (e) => {
           setFile(e.target.files[0]);
           setError(null);
           setResults(null);
       };
       
       const extractPDF = async () => {
           if (!file) {
               setError('Please select a PDF file');
               return;
           }
           
           setLoading(true);
           setError(null);
           
           try {
               const formData = new FormData();
               formData.append('file', file);
               
               const response = await fetch(`http://localhost:8000/api/v1/extract/${selectedTool}`, {
                   method: 'POST',
                   body: formData
               });
               
               const result = await response.json();
               setResults(result);
               
           } catch (err) {
               setError(`Error: ${err.message}`);
           } finally {
               setLoading(false);
           }
       };
       
       const benchmarkAll = async () => {
           if (!file) {
               setError('Please select a PDF file');
               return;
           }
           
           setLoading(true);
           setError(null);
           
           try {
               const formData = new FormData();
               formData.append('file', file);
               formData.append('tools', JSON.stringify(tools));
               
               const response = await fetch('http://localhost:8000/api/v1/benchmark', {
                   method: 'POST',
                   body: formData
               });
               
               const result = await response.json();
               setResults(result);
               
           } catch (err) {
               setError(`Error: ${err.message}`);
           } finally {
               setLoading(false);
           }
       };
       
       const renderResults = () => {
           if (!results) return null;
           
           if (results.results) {
               // Benchmark results
               return (
                   <div>
                       <h3>Benchmark Results for {results.filename}</h3>
                       <p>File Size: {(results.file_size_bytes / 1024 / 1024).toFixed(2)} MB</p>
                       
                       <table>
                           <thead>
                               <tr>
                                   <th>Tool</th>
                                   <th>Time (ms)</th>
                                   <th>Text Length</th>
                                   <th>Status</th>
                               </tr>
                           </thead>
                           <tbody>
                               {results.results.map((result, index) => (
                                   <tr key={index}>
                                       <td>{result.tool}</td>
                                       <td>{result.execution_time_ms.toFixed(2)}</td>
                                       <td>{result.extracted_text_length.toLocaleString()}</td>
                                       <td>{result.error ? 'Error' : 'Success'}</td>
                                   </tr>
                               ))}
                           </tbody>
                       </table>
                   </div>
               );
           } else {
               // Extraction results
               return (
                   <div>
                       <h3>Extraction Results</h3>
                       <p>Status: {results.status}</p>
                       <p>Tool: {results.tool}</p>
                       
                       {results.status === 'success' && results.data && (
                           <div>
                               {results.data.map((item, index) => (
                                   <div key={index}>
                                       <h4>{item.type.charAt(0).toUpperCase() + item.type.slice(1)}:</h4>
                                       <pre style={{ whiteSpace: 'pre-wrap', maxHeight: '200px', overflow: 'auto' }}>
                                           {item.content}
                                       </pre>
                                   </div>
                               ))}
                           </div>
                       )}
                       
                       {results.status === 'error' && (
                           <p style={{ color: 'red' }}>Error: {results.error}</p>
                       )}
                   </div>
               );
           }
       };
       
       return (
           <div>
               <h1>PDF Extraction Tool</h1>
               
               <div>
                   <h2>Upload PDF</h2>
                   <input type="file" accept=".pdf" onChange={handleFileChange} />
                   
                   <div>
                       <h3>Select Tool:</h3>
                       {tools.map(tool => (
                           <label key={tool}>
                               <input
                                   type="radio"
                                   value={tool}
                                   checked={selectedTool === tool}
                                   onChange={(e) => setSelectedTool(e.target.value)}
                               />
                               {tool}
                           </label>
                       ))}
                   </div>
                   
                   <button onClick={extractPDF} disabled={loading}>
                       Extract Text
                   </button>
                   <button onClick={benchmarkAll} disabled={loading}>
                       Benchmark All Tools
                   </button>
                   
                   {loading && <p>Processing...</p>}
                   {error && <p style={{ color: 'red' }}>{error}</p>}
               </div>
               
               <div>
                   <h2>Results</h2>
                   {renderResults()}
               </div>
           </div>
       );
   };
   
   export default PDFExtractor;

These examples demonstrate various ways to integrate the PDF Extraction Backend into different applications and workflows. For more detailed API information, see the :doc:`endpoints` documentation.
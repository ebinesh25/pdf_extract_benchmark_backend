PDF Extraction Guide
====================

This document provides detailed information about the PDF extraction endpoints and how to use them effectively.

Overview
--------

The PDF Extraction Backend supports four different extraction tools, each with unique strengths and use cases:

* **PyMuPDF**: Fast processing with OCR support
* **pdfplumber**: Excellent for table extraction
* **pypdf**: Lightweight for simple text extraction
* **pdfminer.six**: Deep text analysis with position information

Extraction Tools
---------------

PyMuPDF (fitz)
~~~~~~~~~~~~~~

PyMuPDF is a high-performance library for PDF extraction with the following features:

* **Speed**: Fastest extraction among supported tools
* **OCR Support**: Can extract text from scanned documents
* **Image Extraction**: Can extract images from PDFs
* **Metadata**: Extracts document metadata
* **Cross-platform**: Works on Windows, macOS, and Linux

**Best for**:
* General text extraction
* Documents with images
* Scanned PDFs (with OCR)
* Performance-critical applications

**Example Usage**:

.. code-block:: python

   import requests

   with open('document.pdf', 'rb') as f:
       files = {'file': f}
       response = requests.post('http://localhost:8000/api/v1/extract/pymupdf', files=files)
   
   result = response.json()
   print(f"Status: {result['status']}")
   print(f"Tool: {result['tool']}")
   
   for item in result['data']:
       print(f"Type: {item['type']}")
       print(f"Content: {item['content'][:100]}...")

**Implementation**:

The PyMuPDF extractor is implemented as follows:

.. literalinclude:: ../app/utils/pdf_extractors.py
   :language: python
   :lines: 36-107
   :caption: PyMuPDF extractor implementation

pdfplumber
~~~~~~~~~~

pdfplumber excels at extracting structured data, particularly tables:

* **Table Extraction**: Best-in-class table detection and extraction
* **Layout Analysis**: Detailed understanding of page layout
* **Character Positioning**: Precise character and word positioning
* **Shape Detection**: Can identify and extract shapes and lines

**Best for**:
* Documents with tables
* Financial statements
* Reports with structured layouts
* Documents requiring precise positioning

**Example Usage**:

.. code-block:: python

   import requests

   with open('financial_report.pdf', 'rb') as f:
       files = {'file': f}
       response = requests.post('http://localhost:8000/api/v1/extract/pdfplumber', files=files)
   
   result = response.json()
   
   # Extract table content
   for item in result['data']:
       if item['type'] == 'table':
           print("Table found:")
           print(item['content'])

**Implementation**:

The pdfplumber extractor is implemented as follows:

.. literalinclude:: ../app/utils/pdf_extractors.py
   :language: python
   :lines: 110-176
   :caption: pdfplumber extractor implementation

pypdf
~~~~~

pypdf is a lightweight library focused on basic text extraction:

* **Lightweight**: Minimal dependencies and small footprint
* **Simple**: Easy to use for basic extraction needs
* **Fast**: Good performance for simple documents
* **Reliable**: Stable and well-maintained

**Best for**:
* Simple text extraction
* Documents with basic formatting
* Resource-constrained environments
* Batch processing of simple documents

**Example Usage**:

.. code-block:: python

   import requests

   with open('simple_document.pdf', 'rb') as f:
       files = {'file': f}
       response = requests.post('http://localhost:8000/api/v1/extract/pypdf', files=files)
   
   result = response.json()
   
   # Extract all text content
   text_content = []
   for item in result['data']:
       if item['type'] == 'text':
           text_content.append(item['content'])
   
   full_text = '\n'.join(text_content)
   print(full_text)

**Implementation**:

The pypdf extractor is implemented as follows:

.. literalinclude:: ../app/utils/pdf_extractors.py
   :language: python
   :lines: 179-230
   :caption: pypdf extractor implementation

pdfminer.six
~~~~~~~~~~~~

pdfminer.six provides deep text analysis with detailed positioning information:

* **Position Analysis**: Detailed character and word positioning
* **Font Information**: Extracts font details and styling
* **Text Hierarchy**: Identifies headings and structure
* **Detailed Metadata**: Comprehensive document information

**Best for**:
* Documents requiring detailed text analysis
* Academic papers
* Legal documents
* Documents with complex formatting

**Example Usage**:

.. code-block:: python

   import requests

   with open('research_paper.pdf', 'rb') as f:
       files = {'file': f}
       response = requests.post('http://localhost:8000/api/v1/extract/pdfminer', files=files)
   
   result = response.json()
   
   # Extract and analyze content
   for item in result['data']:
       print(f"Content Type: {item['type']}")
       print(f"Content: {item['content'][:200]}...")
       print("---")

**Implementation**:

The pdfminer extractor is implemented as follows:

.. literalinclude:: ../app/utils/pdf_extractors.py
   :language: python
   :lines: 233-259
   :caption: pdfminer extractor implementation

Response Format
---------------

All extraction endpoints return a standardized response format:

.. code-block:: json

   {
     "status": "success|error",
     "tool": "pymupdf|pdfplumber|pypdf|pdfminer",
     "data": [
       {
         "type": "text|table|metadata|image",
         "content": "Extracted content"
       }
     ],
     "text": null,
     "error": "Error message if status is error"
   }

Content Types
~~~~~~~~~~~~~

The extracted data is categorized into different types:

* **text**: Plain text content from the document
* **table**: Structured table data
* **metadata**: Document metadata (title, author, creation date, etc.)
* **image**: Information about extracted images

Error Handling
--------------

When extraction fails, the API returns an error response:

.. code-block:: json

   {
     "status": "error",
     "tool": "pymupdf",
     "data": null,
     "text": null,
     "error": "PyMuPDF extraction failed: Invalid PDF file"
   }

Common error scenarios:

* **Invalid PDF file**: The uploaded file is not a valid PDF
* **Corrupted PDF**: The PDF file is damaged or unreadable
* **Password protected**: The PDF is password-protected
* **Memory limitations**: The file is too large for available memory

Best Practices
--------------

File Size Considerations
~~~~~~~~~~~~~~~~~~~~~~~

* **Small files** (< 10MB): All tools work well
* **Medium files** (10-50MB): Consider using PyMuPDF for better performance
* **Large files** (> 50MB): Monitor memory usage and consider chunking

Tool Selection
~~~~~~~~~~~~~~

Choose the right tool based on your needs:

.. list-table:: Tool Selection Guide
   :header-rows: 1

   * - Use Case
     - Recommended Tool
     - Reason
   * - General text extraction
     - PyMuPDF
     - Fast and reliable
   * - Table extraction
     - pdfplumber
     - Best table detection
   * - Simple documents
     - pypdf
     - Lightweight and fast
   * - Detailed analysis
     - pdfminer.six
     - Comprehensive extraction
   * - Scanned documents
     - PyMuPDF
     - OCR support

Performance Tips
~~~~~~~~~~~~~~~~

* **Batch processing**: Use async requests for multiple files
* **Caching**: Cache results for repeated extractions
* **Tool selection**: Choose the most appropriate tool for your document type
* **Memory management**: Monitor memory usage with large files

Integration Examples
-------------------

Python Client
~~~~~~~~~~~~~

The PDF extraction client can be implemented using the file validation and handling utilities:

.. literalinclude:: ../app/utils/file_handler.py
   :language: python
   :lines: 11-38
   :caption: PDF file validation implementation

.. code-block:: python

   import requests
   import json
   from pathlib import Path

   class PDFExtractionClient:
       def __init__(self, base_url="http://localhost:8000"):
           self.base_url = base_url
           self.api_prefix = "/api/v1"
       
       def extract_with_tool(self, pdf_path, tool="pymupdf"):
           """Extract PDF using specified tool."""
           url = f"{self.base_url}{self.api_prefix}/extract/{tool}"
           
           with open(pdf_path, 'rb') as f:
               files = {'file': f}
               response = requests.post(url, files=files)
           
           return response.json()
       
       def extract_text_only(self, pdf_path, tool="pymupdf"):
           """Extract only text content."""
           result = self.extract_with_tool(pdf_path, tool)
           
           if result['status'] == 'success':
               text_items = [item['content'] for item in result['data'] if item['type'] == 'text']
               return '\n'.join(text_items)
           else:
               return None

   # Usage example
   client = PDFExtractionClient()
   result = client.extract_with_tool('document.pdf', 'pymupdf')
   text = client.extract_text_only('document.pdf', 'pdfplumber')

JavaScript Client
~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   class PDFExtractionClient {
       constructor(baseUrl = 'http://localhost:8000') {
           this.baseUrl = baseUrl;
           this.apiPrefix = '/api/v1';
       }
       
       async extractWithTool(pdfFile, tool = 'pymupdf') {
           const url = `${this.baseUrl}${this.apiPrefix}/extract/${tool}`;
           const formData = new FormData();
           formData.append('file', pdfFile);
           
           const response = await fetch(url, {
               method: 'POST',
               body: formData
           });
           
           return await response.json();
       }
       
       async extractTextOnly(pdfFile, tool = 'pymupdf') {
           const result = await this.extractWithTool(pdfFile, tool);
           
           if (result.status === 'success') {
               const textItems = result.data
                   .filter(item => item.type === 'text')
                   .map(item => item.content);
               return textItems.join('\n');
           }
           
           return null;
       }
   }

   // Usage example
   const client = new PDFExtractionClient();
   
   // With file input
   document.getElementById('pdf-input').addEventListener('change', async (e) => {
       const file = e.target.files[0];
       if (file) {
           const result = await client.extractWithTool(file, 'pymupdf');
           console.log(result);
       }
   });

cURL Examples
~~~~~~~~~~~~~

.. code-block:: bash

   # Extract with PyMuPDF
   curl -X POST "http://localhost:8000/api/v1/extract/pymupdf" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf"

   # Extract with pdfplumber
   curl -X POST "http://localhost:8000/api/v1/extract/pdfplumber" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf"

   # Extract with pypdf
   curl -X POST "http://localhost:8000/api/v1/extract/pypdf" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf"

   # Extract with pdfminer
   curl -X POST "http://localhost:8000/api/v1/extract/pdfminer" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf"

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

1. **"Invalid PDF file" error**
   * Ensure the file is a valid PDF
   * Check if the file is corrupted
   * Verify the file extension is .pdf

2. **Memory errors with large files**
   * Try using a more memory-efficient tool (pypdf)
   * Process files in smaller chunks
   * Increase available memory

3. **Slow extraction performance**
   * Use PyMuPDF for faster processing
   * Consider preprocessing large files
   * Implement caching for repeated extractions

4. **Missing text from scanned documents**
   * Use PyMuPDF with OCR support
   * Ensure OCR dependencies are installed
   * Check image quality in the PDF

Debugging Tips
~~~~~~~~~~~~~~

* Use the health check endpoints to verify API status
* Check the database health endpoint for connectivity issues
* Monitor memory usage during extraction
* Test with different tools to compare results
* Use the interactive documentation at /docs for testing

For more advanced usage and benchmarking information, see the :doc:`benchmarking` documentation.
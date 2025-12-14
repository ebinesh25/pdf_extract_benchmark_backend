API Endpoints
=============

This document provides detailed information about all available API endpoints in the PDF Extraction Backend.

Base URL
--------

The base URL for all API endpoints is: ``http://localhost:8000/api/v1``

General Endpoints
-----------------

Root Endpoint
~~~~~~~~~~~~~

.. http:get:: /

   Returns basic API information and available extraction tools.

   **Example Request**:

   .. code-block:: http

      GET / HTTP/1.1
      Host: localhost:8000

   **Example Response**:

   .. code-block:: json

      {
        "name": "PDF Extraction Backend",
        "version": "0.1.0",
        "description": "PDF extraction backend supporting multiple extraction tools",
        "docs": "/docs",
        "available_tools": [
          {
            "name": "pymupdf",
            "description": "PyMuPDF (fitz) is a PDF library based on the MuPDF open source project.",
            "tags": ["opensource"]
          }
        ]
      }

Models Endpoint
~~~~~~~~~~~~~~~

.. http:get:: /models

   Returns a list of all available extraction models/tools.

   **Example Request**:

   .. code-block:: http

      GET /models HTTP/1.1
      Host: localhost:8000

   **Example Response**:

   .. code-block:: json

      [
        {
          "name": "pymupdf",
          "description": "PyMuPDF (fitz) is a PDF library based on the MuPDF open source project.",
          "tags": ["opensource"]
        },
        {
          "name": "pdfplumber",
          "description": "pdfplumber is a PDF library based on the MuPDF open source project.",
          "tags": ["OCR", "opensource"]
        }
      ]

Health Check Endpoints
-----------------------

Basic Health Check
~~~~~~~~~~~~~~~~~~

.. http:get:: /health

   Returns the health status of the API.

   **Example Request**:

   .. code-block:: http

      GET /health HTTP/1.1
      Host: localhost:8000

   **Example Response**:

   .. code-block:: json

      {
        "status": "healthy"
      }

Database Health Check
~~~~~~~~~~~~~~~~~~~~~

.. http:get:: /health/db

   Returns the health status of the database connection and lists available collections.

   **Example Request**:

   .. code-block:: http

      GET /health/db HTTP/1.1
      Host: localhost:8000

   **Example Response**:

   .. code-block:: json

      {
        "db": "pdf_extraction",
        "collections": ["extraction_results", "benchmarks"]
      }

PDF Extraction Endpoints
------------------------

All extraction endpoints accept a PDF file via multipart/form-data and return structured extraction results.

PyMuPDF Extraction
~~~~~~~~~~~~~~~~~

.. http:post:: /extract/pymupdf

   Extract text from PDF using PyMuPDF (fitz).

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
        - PDF file to extract text from

   **Example Request**:

   .. code-block:: http

      POST /api/v1/extract/pymupdf HTTP/1.1
      Host: localhost:8000
      Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

      ------WebKitFormBoundary7MA4YWxkTrZu0gW
      Content-Disposition: form-data; name="file"; filename="document.pdf"
      Content-Type: application/pdf

      [PDF file content]
      ------WebKitFormBoundary7MA4YWxkTrZu0gW--

   **Example Response**:

   .. code-block:: json

      {
        "status": "success",
        "tool": "pymupdf",
        "data": [
          {
            "type": "metadata",
            "content": "Title: Sample Document\nAuthor: John Doe"
          },
          {
            "type": "text",
            "content": "This is the extracted text from page 1..."
          }
        ],
        "text": null,
        "error": null
      }

PDFPlumber Extraction
~~~~~~~~~~~~~~~~~~~~~

.. http:post:: /extract/pdfplumber

   Extract text from PDF using pdfplumber. Excellent for table extraction.

   **Request Parameters**: Same as PyMuPDF extraction

   **Example Response**: Same structure as PyMuPDF extraction with ``tool`` set to ``"pdfplumber"``

PyPDF Extraction
~~~~~~~~~~~~~~~~

.. http:post:: /extract/pypdf

   Extract text from PDF using pypdf. Lightweight for simple text extraction.

   **Request Parameters**: Same as PyMuPDF extraction

   **Example Response**: Same structure as PyMuPDF extraction with ``tool`` set to ``"pypdf"``

PDFMiner Extraction
~~~~~~~~~~~~~~~~~~~

.. http:post:: /extract/pdfminer

   Extract text from PDF using pdfminer.six. Deep text analysis with position information.

   **Request Parameters**: Same as PyMuPDF extraction

   **Example Response**: Same structure as PyMuPDF extraction with ``tool`` set to ``"pdfminer"``

Benchmarking Endpoints
----------------------

Run Benchmark
~~~~~~~~~~~~

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

   .. code-block:: http

      POST /api/v1/benchmark HTTP/1.1
      Host: localhost:8000
      Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

      ------WebKitFormBoundary7MA4YWxkTrZu0gW
      Content-Disposition: form-data; name="file"; filename="document.pdf"
      Content-Type: application/pdf

      [PDF file content]
      ------WebKitFormBoundary7MA4YWxkTrZu0gW
      Content-Disposition: form-data; name="tools"

      ["pymupdf", "pdfplumber"]
      ------WebKitFormBoundary7MA4YWxkTrZu0gW--

   **Example Response**:

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

Error Responses
---------------

All endpoints may return error responses in the following format:

.. code-block:: json

   {
     "detail": "Error description message"
   }

Common HTTP Status Codes
------------------------

.. list-table:: HTTP Status Codes
   :header-rows: 1

   * - Status Code
     - Meaning
     - Description
   * - 200
     - OK
     - Request successful
   * - 400
     - Bad Request
     - Invalid request parameters
   * - 422
     - Unprocessable Entity
     - Validation error
   * - 500
     - Internal Server Error
     - Server-side error

Interactive Documentation
------------------------

The API also provides interactive documentation:

* **Swagger UI**: http://localhost:8000/docs
* **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to explore and test the API endpoints directly from your browser.
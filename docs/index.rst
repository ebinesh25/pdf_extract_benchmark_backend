PDF Extraction Backend Documentation
=====================================

Welcome to the PDF Extraction Backend documentation! This FastAPI application provides multiple PDF extraction tools with benchmarking capabilities.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   endpoints
   extraction
   benchmarking
   schemas
   examples

Features
--------

* Multiple PDF extraction tools (PyMuPDF, pdfplumber, pypdf, pdfminer)
* Benchmarking capabilities to compare extraction performance
* RESTful API with FastAPI
* Automatic API documentation with Swagger UI
* Structured data extraction (text, tables, metadata, images)

Quick Start
-----------

1. Install the package with documentation dependencies:

   .. code-block:: bash

      pip install -e ".[docs]"

2. Run the FastAPI server:

   .. code-block:: bash

      uvicorn app.main:app --reload

3. Access the interactive API documentation:

   * Swagger UI: http://localhost:8000/docs
   * ReDoc: http://localhost:8000/redoc

API Overview
------------

The API provides the following main endpoints:

* **PDF Extraction**: Extract content from PDF files using different tools
* **Benchmarking**: Compare performance of different extraction tools
* **Health Checks**: Monitor API and database status

Available Extraction Tools
---------------------------

.. list-table:: Supported PDF Extraction Tools
   :header-rows: 1

   * - Tool
     - Description
     - Best For
   * - PyMuPDF
     - Fast PDF processing with OCR support
     - General text extraction, images
   * - pdfplumber
     - Detailed layout analysis
     - Tables, structured data
   * - pypdf
     - Lightweight text extraction
     - Simple text extraction
   * - pdfminer
     - Deep text analysis with position info
     - Detailed text analysis

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
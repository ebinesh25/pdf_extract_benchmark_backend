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

   The batch processor uses the file handling utilities:

   .. literalinclude:: ../app/utils/file_handler.py
      :language: python
      :lines: 40-72
      :caption: File upload and validation implementation

Tool Comparison
~~~~~~~~~~~~~~~

Compare extraction results from different tools:

   .. literalinclude:: ../app/utils/benchmarking.py
      :language: python
      :lines: 61-77
      :caption: Accuracy calculation implementation

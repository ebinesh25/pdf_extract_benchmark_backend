Data Models and Schemas
=======================

This document provides detailed information about the data models and schemas used in the PDF Extraction Backend.

Overview
--------

The API uses Pydantic models for data validation and serialization. These models ensure type safety, provide automatic validation, and generate OpenAPI documentation.

Extraction Schemas
-----------------

ExtractionTool Enum
~~~~~~~~~~~~~~~~~~

.. py:class:: app.schemas.extraction.ExtractionTool

   Enumeration of supported PDF extraction tools.

   **Values**:
   
   * ``PYMUPDF``: PyMuPDF (fitz) extraction tool
   * ``PDFPLUMBER``: pdfplumber extraction tool
   * ``PYPDF``: pypdf extraction tool
   * ``PDFMINER``: pdfminer.six extraction tool

   **Example Usage**:

   .. code-block:: python

      from app.schemas.extraction import ExtractionTool
      
      tool = ExtractionTool.PYMUPDF
      print(tool.value)  # Output: "pymupdf"

   **Implementation**:

   The ExtractionTool enum is defined as:

   .. literalinclude:: ../app/schemas/extraction.py
      :language: python
      :lines: 10-16
      :caption: ExtractionTool enum definition

ExtractionContent Model
~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: app.schemas.extraction.ExtractionContent

   Represents individual content items extracted from a PDF.

   **Fields**:

   .. list-table:: ExtractionContent Fields
      :header-rows: 1

      * - Field
        - Type
        - Required
        - Description
      * - type
        - str
        - Yes
        - Type of content: text, table, metadata, or image
      * - content
        - str
        - Yes
        - The actual extracted content

   **Example**:

   .. code-block:: json

      {
        "type": "text",
        "content": "This is the extracted text from page 1..."
      }

   **Content Types**:

   * **text**: Plain text content from the document
   * **table**: Structured table data
   * **metadata**: Document metadata (title, author, etc.)
   * **image**: Information about extracted images

ExtractionResponse Model
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: app.schemas.extraction.ExtractionResponse

   Response model for PDF extraction endpoints.

   **Fields**:

   .. list-table:: ExtractionResponse Fields
      :header-rows: 1

      * - Field
        - Type
        - Required
        - Description
      * - status
        - str
        - Yes
        - Extraction status (success/error)
      * - tool
        - ExtractionTool
        - Yes
        - Extraction tool used
      * - data
        - List[ExtractionContent] | None
        - No
        - Structured extracted content
      * - text
        - str | None
        - No
        - Legacy text field for backward compatibility
      * - error
        - str | None
        - No
        - Error message if extraction failed

   **Success Response Example**:

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
          },
          {
            "type": "table",
            "content": "Table 1:\nName | Age | City\nJohn | 30 | NYC"
          }
        ],
        "text": null,
        "error": null
      }

   **Error Response Example**:

   .. code-block:: json

      {
        "status": "error",
        "tool": "pymupdf",
        "data": null,
        "text": null,
        "error": "PyMuPDF extraction failed: Invalid PDF file"
      }

ErrorResponse Model
~~~~~~~~~~~~~~~~~~~

.. py:class:: app.schemas.extraction.ErrorResponse

   Standard error response model.

   **Fields**:

   .. list-table:: ErrorResponse Fields
      :header-rows: 1

      * - Field
        - Type
        - Required
        - Description
      * - detail
        - str
        - Yes
        - Error message

   **Example**:

   .. code-block:: json

      {
        "detail": "Invalid file type. Allowed: .pdf"
      }

   **Implementation**:

   The ErrorResponse model is defined as:

   .. literalinclude:: ../app/schemas/extraction.py
      :language: python
      :lines: 67-77
      :caption: ErrorResponse model definition

Benchmarking Schemas
--------------------

BenchmarkResult Model
~~~~~~~~~~~~~~~~~~~~~

.. py:class:: app.schemas.benchmarking.BenchmarkResult

   Represents the result of benchmarking a single extraction tool.

   **Fields**:

   .. list-table:: BenchmarkResult Fields
      :header-rows: 1

      * - Field
        - Type
        - Required
        - Description
      * - tool
        - ExtractionTool
        - Yes
        - The extraction tool that was benchmarked
      * - execution_time_ms
        - float
        - Yes
        - Execution time in milliseconds
      * - accuracy_score
        - Optional[float]
        - No
        - Accuracy score (0-1) when ground truth is provided
      * - extracted_text_length
        - int
        - Yes
        - Length of extracted text in characters
      * - extracted_text
        - str | None
        - Yes
        - The actual extracted text content
      * - extracted_data
        - Optional[List[Dict[str, str]]]
        - No
        - Structured data (tables, metadata, etc.)
      * - error
        - Optional[str]
        - No
        - Error message if extraction failed
      * - cost_per_page
        - str
        - Yes
        - Processing cost per page
      * - features
        - List[str]
        - Yes
        - List of supported features

   **Example**:

   .. code-block:: json

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
      }

BenchmarkResponse Model
~~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: app.schemas.benchmarking.BenchmarkResponse

   Response model for benchmarking endpoints.

   **Fields**:

   .. list-table:: BenchmarkResponse Fields
      :header-rows: 1

      * - Field
        - Type
        - Required
        - Description
      * - filename
        - str
        - Yes
        - Name of the benchmarked file
      * - file_size_bytes
        - int
        - Yes
        - Size of the file in bytes
      * - results
        - List[BenchmarkResult]
        - Yes
        - Array of benchmark results for each tool

   **Example**:

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
          }
        ]
      }

Model Validation
---------------

Pydantic provides automatic validation for all models. Here are the validation rules:

ExtractionTool Validation
~~~~~~~~~~~~~~~~~~~~~~~~~

* Must be one of the predefined enum values
* Case-sensitive matching
* Automatically converted to lowercase strings

ExtractionContent Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **type**: Must be a non-empty string
* **content**: Must be a non-empty string
* Both fields are required

ExtractionResponse Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **status**: Must be a non-empty string
* **tool**: Must be a valid ExtractionTool enum value
* **data**: Must be null or a list of ExtractionContent objects
* **text**: Must be null or a string
* **error**: Must be null or a string

BenchmarkResult Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~

* **tool**: Must be a valid ExtractionTool enum value
* **execution_time_ms**: Must be a non-negative float
* **accuracy_score**: Must be null or a float between 0.0 and 1.0
* **extracted_text_length**: Must be a non-negative integer
* **extracted_text**: Must be null or a string
* **extracted_data**: Must be null or a list of dictionaries
* **error**: Must be null or a string
* **cost_per_page**: Must be a non-empty string
* **features**: Must be a list of strings

Custom Validation
~~~~~~~~~~~~~~~~~

The models include custom validation logic:

.. code-block:: python

   from pydantic import validator, Field
   
   class ExtractionResponse(BaseModel):
       # ... fields ...
       
       @validator('status')
       def validate_status(cls, v):
           if v not in ['success', 'error']:
               raise ValueError('Status must be either "success" or "error"')
           return v
       
       @validator('data')
       def validate_data_consistency(cls, v, values):
           if values.get('status') == 'success' and v is None:
               raise ValueError('Data must be provided when status is success')
           return v

Model Usage Examples
-------------------

Creating Model Instances
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from app.schemas.extraction import ExtractionResponse, ExtractionContent, ExtractionTool
   from app.schemas.benchmarking import BenchmarkResult, BenchmarkResponse

   # Create extraction content
   content = ExtractionContent(
       type="text",
       content="This is extracted text from the PDF."
   )

   # Create extraction response
   extraction_response = ExtractionResponse(
       status="success",
       tool=ExtractionTool.PYMUPDF,
       data=[content],
       text=None,
       error=None
   )

   # Create benchmark result
   benchmark_result = BenchmarkResult(
       tool=ExtractionTool.PYMUPDF,
       execution_time_ms=150.5,
       accuracy_score=0.95,
       extracted_text_length=2500,
       extracted_text="Extracted text content...",
       extracted_data=None,
       error=None,
       cost_per_page="Free",
       features=["text", "images", "metadata"]
   )

   # Create benchmark response
   benchmark_response = BenchmarkResponse(
       filename="document.pdf",
       file_size_bytes=1024000,
       results=[benchmark_result]
   )

Serializing and Deserializing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json

   # Serialize to JSON
   extraction_json = extraction_response.model_dump_json()
   print(extraction_json)

   # Deserialize from JSON
   extraction_data = json.loads(extraction_json)
   restored_response = ExtractionResponse(**extraction_data)

   # Convert to dictionary
   extraction_dict = extraction_response.model_dump()
   print(extraction_dict)

Validation with External Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pydantic import ValidationError

   try:
       # This will raise ValidationError due to missing required fields
       invalid_response = ExtractionResponse(
           status="success"
           # Missing required 'tool' field
       )
   except ValidationError as e:
       print(f"Validation error: {e}")

   try:
       # This will raise ValidationError due to invalid enum value
       invalid_content = ExtractionContent(
           type="invalid_type",  # Not a valid content type
           content="Some content"
       )
   except ValidationError as e:
       print(f"Validation error: {e}")

Model Extensions
---------------

Adding Custom Fields
~~~~~~~~~~~~~~~~~~~~~

You can extend the models for custom use cases:

.. code-block:: python

   from typing import Optional
   from pydantic import BaseModel
   from app.schemas.extraction import ExtractionResponse

   class ExtendedExtractionResponse(ExtractionResponse):
       """Extended extraction response with additional fields."""
       processing_time_ms: Optional[float] = None
       page_count: Optional[int] = None
       language_detected: Optional[str] = None
       confidence_score: Optional[float] = None

   # Usage
   extended_response = ExtendedExtractionResponse(
       status="success",
       tool=ExtractionTool.PYMUPDF,
       data=[content],
       text=None,
       error=None,
       processing_time_ms=150.5,
       page_count=10,
       language_detected="en",
       confidence_score=0.98
   )

Custom Validation Methods
~~~~~~~~~~~~~~~~~~~~~~~~~

Add custom validation logic:

.. code-block:: python

   from pydantic import validator

   class CustomExtractionResponse(ExtractionResponse):
       """Extraction response with custom validation."""
       
       @validator('data')
       def validate_content_types(cls, v):
           if v is not None:
               valid_types = {'text', 'table', 'metadata', 'image'}
               for item in v:
                   if item.type not in valid_types:
                       raise ValueError(f"Invalid content type: {item.type}")
           return v
       
       @validator('error')
       def validate_error_consistency(cls, v, values):
           if values.get('status') == 'error' and not v:
               raise ValueError("Error message must be provided when status is error")
           if values.get('status') == 'success' and v:
               raise ValueError("Error message should not be provided when status is success")
           return v

Model Configuration
------------------

JSON Schema Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

The models include JSON schema configuration for OpenAPI documentation:

.. code-block:: python

   class ExtractionResponse(BaseModel):
       # ... fields ...
       
       class Config:
           json_schema_extra = {
               "examples": [
                   {
                       "status": "success",
                       "tool": "pymupdf",
                       "data": [
                           {
                               "type": "text",
                               "content": "Sample extracted text..."
                           }
                       ],
                       "text": None,
                       "error": None
                   }
               ]
           }

Field Aliases
~~~~~~~~~~~~~

Use field aliases for API compatibility:

.. code-block:: python

   from pydantic import Field

   class AliasedExtractionResponse(BaseModel):
       """Extraction response with field aliases."""
       
       extraction_status: str = Field(..., alias="status")
       extraction_tool: ExtractionTool = Field(..., alias="tool")
       extracted_data: Optional[List[ExtractionContent]] = Field(None, alias="data")
       extracted_text: Optional[str] = Field(None, alias="text")
       error_message: Optional[str] = Field(None, alias="error")
       
       class Config:
           allow_population_by_field_name = True

   # Usage with aliases
   aliased_response = AliasedExtractionResponse(
       status="success",
       tool=ExtractionTool.PYMUPDF,
       data=[content],
       text=None,
       error=None
   )
   
   # Access by original field names
   print(aliased_response.extraction_status)
   print(aliased_response.extraction_tool)

Best Practices
--------------

Model Design Principles
~~~~~~~~~~~~~~~~~~~~~~~

1. **Explicit Field Types**: Always specify field types for better validation
2. **Required Fields**: Mark required fields explicitly
3. **Optional Fields**: Use Optional for nullable fields
4. **Default Values**: Provide sensible defaults where appropriate
5. **Validation**: Add custom validation for business logic
6. **Documentation**: Include field descriptions and examples

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from pydantic import ValidationError

   def safe_model_creation(model_class, **kwargs):
       """Safely create a model instance with error handling."""
       try:
           return model_class(**kwargs)
       except ValidationError as e:
           print(f"Validation failed: {e}")
           return None

   # Usage
   response = safe_model_creation(
       ExtractionResponse,
       status="success",
       tool=ExtractionTool.PYMUPDF,
       data=[content],
       text=None,
       error=None
   )

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Model Instantiation**: Pydantic models have some overhead for validation
2. **JSON Serialization**: Use ``model_dump_json()`` for direct JSON serialization
3. **Batch Processing**: Consider validation for batch operations
4. **Caching**: Cache validated model instances when possible

Testing Models
--------------

Unit Testing
~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from app.schemas.extraction import ExtractionResponse, ExtractionContent, ExtractionTool

   def test_extraction_response_success():
       """Test successful extraction response."""
       content = ExtractionContent(type="text", content="Sample text")
       response = ExtractionResponse(
           status="success",
           tool=ExtractionTool.PYMUPDF,
           data=[content],
           text=None,
           error=None
       )
       
       assert response.status == "success"
       assert response.tool == ExtractionTool.PYMUPDF
       assert len(response.data) == 1
       assert response.error is None

   def test_extraction_response_validation():
       """Test validation errors."""
       with pytest.raises(ValidationError):
           ExtractionResponse(
               status="invalid_status",  # Invalid status
               tool=ExtractionTool.PYMUPDF
           )

Integration Testing
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from fastapi.testclient import TestClient
   from app.main import app

   def test_extraction_endpoint_response_schema():
       """Test that extraction endpoint returns valid schema."""
       client = TestClient(app)
       
       with open('test_document.pdf', 'rb') as f:
           response = client.post(
               '/api/v1/extract/pymupdf',
               files={'file': ('test.pdf', f, 'application/pdf')}
           )
       
       assert response.status_code == 200
       
       # Validate response schema
       data = response.json()
       validated_response = ExtractionResponse(**data)
       
       assert validated_response.status in ['success', 'error']

For more information about using these models in API endpoints, see the :doc:`endpoints` documentation.
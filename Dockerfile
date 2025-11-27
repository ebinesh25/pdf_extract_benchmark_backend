FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF processing and OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    mesa-utils \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements
COPY pyproject.toml ./

# Install Python dependencies using pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Create upload directory
RUN mkdir -p temp_uploads

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

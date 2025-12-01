FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OCR + OpenGL
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    mesa-utils \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (for caching)
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir . gunicorn uvicorn

# Copy application code
COPY . .

# Create temp directory (Cloud Run allows ephemeral writes)
RUN mkdir -p /app/temp_uploads

# Cloud Run requires this
ENV PORT=8080

# Gunicorn command using UvicornWorker
CMD ["gunicorn", "app.main:app", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8080"]

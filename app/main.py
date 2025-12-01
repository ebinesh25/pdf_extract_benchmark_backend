from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import extraction

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="PDF extraction backend with multiple extraction tools",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(extraction.router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "description": "PDF extraction backend supporting multiple extraction tools",
        "docs": "/docs",
        "available_tools": ["pymupdf", "pdfplumber", "pypdf", "pdfminer"]
    }

@app.get("/models")
async def get_models():
    """Get available models."""
    return {"models": ["pymupdf", "pdfplumber", "pypdf", "pdfminer"]}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
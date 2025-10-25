"""FastAPI application for document generation."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

from ..models import GenerateDocumentRequest, GenerateDocumentResponse, TemplateInfo
from ..config import settings
from .document_service import DocumentService

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Create document service
document_service = DocumentService()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description,
        "endpoints": {
            "generate": "/api/generate",
            "templates": "/api/templates",
            "download": "/api/download/{filename}",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/templates", response_model=list[TemplateInfo])
async def list_templates():
    """List all available templates."""
    return document_service.list_templates()


@app.get("/api/templates/{template_name}/slides")
async def get_template_slide_types(template_name: str):
    """
    Get slide type information for a PowerPoint template.
    
    Returns metadata from slide notes including:
    - slide_type: Type identifier for the slide
    - description: Human-readable description
    - placeholders: Dictionary of field definitions with types
    """
    try:
        slide_types = document_service.get_template_slide_types(template_name)
        return {"template_name": template_name, "slide_types": slide_types}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading template: {str(e)}")


@app.post("/api/generate", response_model=GenerateDocumentResponse)
async def generate_document(request: GenerateDocumentRequest):
    """
    Generate a document from a template.
    
    - **template_name**: Name of the template (without extension)
    - **document_type**: Type of document (word, excel, or powerpoint)
    - **fields**: Dictionary of field names and values to populate
    - **return_type**: How to return the document (binary or download_link)
    """
    response, output_path = document_service.generate_document(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    # If binary return type, return the file directly
    if request.return_type == "binary" and output_path and output_path.exists():
        return FileResponse(
            path=output_path,
            filename=response.filename,
            media_type="application/octet-stream"
        )
    
    # Otherwise return the response with download link
    return response


@app.get("/api/download/{filename}")
async def download_document(filename: str):
    """Download a generated document."""
    file_path = settings.output_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type based on extension
    media_types = {
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }
    
    media_type = media_types.get(file_path.suffix, "application/octet-stream")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)

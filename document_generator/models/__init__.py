"""Data models for document generation requests and responses."""

from typing import Dict, Any, Optional, Literal, List
from pydantic import BaseModel, Field


class DocumentField(BaseModel):
    """A field to be filled in the document template."""
    name: str = Field(..., description="Field name in the template")
    value: Any = Field(..., description="Value to fill in the field")


class SlideSpec(BaseModel):
    """Specification for a single slide in a presentation."""
    slide_type: str = Field(..., description="Type of slide layout to use (matches slide_type in template metadata)")
    fields: Dict[str, Any] = Field(default_factory=dict, description="Fields to populate in this slide")


class GenerateDocumentRequest(BaseModel):
    """Request model for document generation."""
    template_name: str = Field(..., description="Name of the template to use")
    document_type: Literal["word", "excel", "powerpoint"] = Field(..., description="Type of document to generate")
    fields: Optional[Dict[str, Any]] = Field(None, description="Dictionary of field names and their values (for simple generation)")
    slides: Optional[List[SlideSpec]] = Field(None, description="List of slide specifications (for advanced PowerPoint generation)")
    return_type: Literal["binary", "download_link"] = Field(default="binary", description="How to return the document")


class GenerateDocumentResponse(BaseModel):
    """Response model for document generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    message: str = Field(..., description="Status message")
    document_id: Optional[str] = Field(None, description="ID of the generated document")
    download_url: Optional[str] = Field(None, description="Download URL if return_type is download_link")
    filename: Optional[str] = Field(None, description="Generated filename")


class TemplateInfo(BaseModel):
    """Information about an available template."""
    name: str = Field(..., description="Template name")
    document_type: Literal["word", "excel", "powerpoint"] = Field(..., description="Document type")
    description: Optional[str] = Field(None, description="Template description")
    fields: list[str] = Field(default_factory=list, description="List of available field names")

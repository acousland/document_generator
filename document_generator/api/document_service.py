"""Document service for managing document generation."""

from pathlib import Path
from typing import Dict, Any, Tuple, List
import uuid
from datetime import datetime

from ..generators import WordGenerator, ExcelGenerator, PowerPointGenerator
from ..generators.powerpoint_advanced_generator import PowerPointAdvancedGenerator
from ..models import GenerateDocumentRequest, GenerateDocumentResponse, TemplateInfo
from ..config import settings


class DocumentService:
    """Service for managing document generation."""
    
    def __init__(self):
        self.word_generator = WordGenerator()
        self.excel_generator = ExcelGenerator()
        self.powerpoint_generator = PowerPointGenerator()
        self.powerpoint_advanced_generator = PowerPointAdvancedGenerator()
        
        self.generators = {
            "word": self.word_generator,
            "excel": self.excel_generator,
            "powerpoint": self.powerpoint_generator,
        }
        
        self.extensions = {
            "word": ".docx",
            "excel": ".xlsx",
            "powerpoint": ".pptx",
        }
    
    def list_templates(self) -> list[TemplateInfo]:
        """List all available templates."""
        templates = []
        
        for doc_type, ext in self.extensions.items():
            template_files = list(settings.templates_dir.glob(f"*{ext}"))
            
            for template_file in template_files:
                try:
                    generator = self.generators.get(doc_type)
                    if not generator:
                        continue
                    
                    fields = generator.get_template_fields(template_file)
                    templates.append(TemplateInfo(
                        name=template_file.stem,
                        document_type=doc_type,
                        description=f"Template for {doc_type} documents",
                        fields=fields
                    ))
                except Exception:
                    # Silently skip templates that can't be read
                    # Don't log to avoid breaking MCP protocol
                    continue
        
        return templates
    
    def get_template_slide_types(self, template_name: str) -> List[Dict[str, Any]]:
        """
        Get slide type information for a PowerPoint template.
        Returns metadata from slide notes.
        """
        template_path = settings.templates_dir / f"{template_name}.pptx"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found")
        
        return self.powerpoint_advanced_generator.get_template_slide_types(template_path)
    
    def generate_document(self, request: GenerateDocumentRequest) -> Tuple[GenerateDocumentResponse, Path]:
        """
        Generate a document from a template.
        
        Returns:
            Tuple of (response model, path to generated file)
        """
        try:
            # Find the template
            template_ext = self.extensions[request.document_type]
            template_path = settings.templates_dir / f"{request.template_name}{template_ext}"
            
            if not template_path.exists():
                return GenerateDocumentResponse(
                    success=False,
                    message=f"Template '{request.template_name}' not found"
                ), None
            
            # Generate a unique filename
            document_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{request.template_name}_{timestamp}_{document_id[:8]}{template_ext}"
            output_path = settings.output_dir / output_filename
            
            # Generate the document
            generator = self.generators[request.document_type]
            
            # Use advanced generator for PowerPoint with slides specification
            if request.document_type == "powerpoint" and request.slides:
                self.powerpoint_advanced_generator.generate_from_slides(
                    template_path, 
                    [slide.dict() for slide in request.slides], 
                    output_path
                )
            else:
                # Use standard generation with fields
                if not request.fields:
                    return GenerateDocumentResponse(
                        success=False,
                        message="Either 'fields' or 'slides' must be provided"
                    ), None
                generator.generate(template_path, request.fields, output_path)
            
            # Prepare response
            response = GenerateDocumentResponse(
                success=True,
                message="Document generated successfully",
                document_id=document_id,
                filename=output_filename
            )
            
            # Add download URL if requested
            if request.return_type == "download_link":
                response.download_url = f"{settings.base_url}/api/download/{output_filename}"
            
            return response, output_path
            
        except Exception as e:
            return GenerateDocumentResponse(
                success=False,
                message=f"Error generating document: {str(e)}"
            ), None

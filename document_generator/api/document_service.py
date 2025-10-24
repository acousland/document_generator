"""Document service for managing document generation."""

from pathlib import Path
from typing import Dict, Any, Tuple
import uuid
from datetime import datetime

from ..generators import WordGenerator, ExcelGenerator, PowerPointGenerator
from ..models import GenerateDocumentRequest, GenerateDocumentResponse, TemplateInfo
from ..config import settings


class DocumentService:
    """Service for managing document generation."""
    
    def __init__(self):
        self.word_generator = WordGenerator()
        self.excel_generator = ExcelGenerator()
        self.powerpoint_generator = PowerPointGenerator()
        
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
                generator = self.generators[doc_type]
                try:
                    fields = generator.get_template_fields(template_file)
                    templates.append(TemplateInfo(
                        name=template_file.stem,
                        document_type=doc_type,
                        description=f"Template for {doc_type} documents",
                        fields=fields
                    ))
                except Exception as e:
                    print(f"Error reading template {template_file}: {e}")
        
        return templates
    
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

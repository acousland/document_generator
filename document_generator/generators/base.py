"""Base document generator interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class DocumentGenerator(ABC):
    """Abstract base class for document generators."""
    
    @abstractmethod
    def generate(self, template_path: Path, fields: Dict[str, Any], output_path: Path) -> Path:
        """
        Generate a document from a template.
        
        Args:
            template_path: Path to the template file
            fields: Dictionary of field names and values
            output_path: Path where the generated document should be saved
            
        Returns:
            Path to the generated document
        """
        pass
    
    @abstractmethod
    def get_template_fields(self, template_path: Path) -> list[str]:
        """
        Extract field names from a template.
        
        Args:
            template_path: Path to the template file
            
        Returns:
            List of field names found in the template
        """
        pass

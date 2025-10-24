"""Configuration settings for the document generator."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_title: str = "Document Generator API"
    api_description: str = "API for generating Microsoft Office documents from templates"
    api_version: str = "0.1.0"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Paths
    templates_dir: Path = Path(__file__).parent.parent / "templates"
    output_dir: Path = Path(__file__).parent.parent / "generated_documents"
    
    # File serving
    base_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist
settings.templates_dir.mkdir(parents=True, exist_ok=True)
settings.output_dir.mkdir(parents=True, exist_ok=True)

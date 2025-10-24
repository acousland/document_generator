"""Tests for data models."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_generator.models import (
    GenerateDocumentRequest,
    GenerateDocumentResponse,
    TemplateInfo
)


def test_generate_document_request_creation():
    """Test creating a GenerateDocumentRequest."""
    request = GenerateDocumentRequest(
        template_name="test",
        document_type="word",
        fields={"name": "John", "date": "2024-01-01"},
        return_type="binary"
    )
    assert request.template_name == "test"
    assert request.document_type == "word"
    assert request.fields["name"] == "John"
    assert request.return_type == "binary"


def test_generate_document_request_default_return_type():
    """Test default return_type in GenerateDocumentRequest."""
    request = GenerateDocumentRequest(
        template_name="test",
        document_type="excel",
        fields={"value": "100"}
    )
    assert request.return_type == "binary"


def test_generate_document_response_creation():
    """Test creating a GenerateDocumentResponse."""
    response = GenerateDocumentResponse(
        success=True,
        message="Success",
        document_id="123",
        download_url="http://example.com/doc.docx",
        filename="test.docx"
    )
    assert response.success is True
    assert response.message == "Success"
    assert response.document_id == "123"
    assert response.download_url == "http://example.com/doc.docx"
    assert response.filename == "test.docx"


def test_template_info_creation():
    """Test creating a TemplateInfo."""
    info = TemplateInfo(
        name="letter",
        document_type="word",
        description="A letter template",
        fields=["name", "date", "body"]
    )
    assert info.name == "letter"
    assert info.document_type == "word"
    assert info.description == "A letter template"
    assert len(info.fields) == 3
    assert "name" in info.fields


def test_template_info_default_fields():
    """Test default empty fields list in TemplateInfo."""
    info = TemplateInfo(
        name="test",
        document_type="powerpoint"
    )
    assert info.fields == []

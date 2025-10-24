"""Tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_generator.api.main import app
from document_generator.config import settings


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_templates(client):
    """Test listing templates."""
    response = client.get("/api/templates")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_generate_document_missing_template(client):
    """Test generating a document with a missing template."""
    request_data = {
        "template_name": "nonexistent",
        "document_type": "word",
        "fields": {"test": "value"},
        "return_type": "download_link"
    }
    response = client.post("/api/generate", json=request_data)
    assert response.status_code == 400


def test_download_nonexistent_file(client):
    """Test downloading a file that doesn't exist."""
    response = client.get("/api/download/nonexistent.docx")
    assert response.status_code == 404

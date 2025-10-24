"""Tests for document generators."""

import pytest
from pathlib import Path
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_generator.generators import WordGenerator, ExcelGenerator, PowerPointGenerator


def test_word_generator_instantiation():
    """Test that WordGenerator can be instantiated."""
    generator = WordGenerator()
    assert generator is not None


def test_excel_generator_instantiation():
    """Test that ExcelGenerator can be instantiated."""
    generator = ExcelGenerator()
    assert generator is not None


def test_powerpoint_generator_instantiation():
    """Test that PowerPointGenerator can be instantiated."""
    generator = PowerPointGenerator()
    assert generator is not None


# Additional tests would require actual template files
# These would be integration tests run after templates are created

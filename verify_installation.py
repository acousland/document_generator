#!/usr/bin/env python3
"""
Installation verification script for Document Generator.

This script checks if all dependencies are installed and the system is properly configured.
"""

import sys
from pathlib import Path


def print_header(text):
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print('=' * 60)


def check_python_version():
    """Check Python version."""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True


def check_dependencies():
    """Check if required dependencies are installed."""
    print_header("Dependency Check")
    
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("pydantic", "Data validation"),
        ("pydantic_settings", "Settings management"),
        ("docx", "Word document processing"),
        ("openpyxl", "Excel document processing"),
        ("pptx", "PowerPoint document processing"),
        ("mcp", "Model Context Protocol"),
    ]
    
    all_installed = True
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {module_name:20s} - {description}")
        except ImportError:
            print(f"❌ {module_name:20s} - {description} (NOT INSTALLED)")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Some dependencies are missing.")
        print("   Run: pip install -r requirements.txt")
    
    return all_installed


def check_directory_structure():
    """Check if required directories exist."""
    print_header("Directory Structure Check")
    
    base_dir = Path(__file__).parent
    required_dirs = [
        ("templates", "Template storage directory"),
        ("document_generator", "Main package directory"),
        ("document_generator/api", "API module"),
        ("document_generator/generators", "Generator modules"),
        ("document_generator/mcp_server", "MCP server module"),
        ("examples", "Example scripts"),
        ("tests", "Test suite"),
    ]
    
    all_exist = True
    for dir_path, description in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✅ {dir_path:30s} - {description}")
        else:
            print(f"❌ {dir_path:30s} - {description} (MISSING)")
            all_exist = False
    
    return all_exist


def check_configuration():
    """Check configuration."""
    print_header("Configuration Check")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from document_generator.config import settings
        
        print(f"✅ Configuration loaded successfully")
        print(f"   Templates directory: {settings.templates_dir}")
        print(f"   Output directory: {settings.output_dir}")
        print(f"   API port: {settings.port}")
        print(f"   Base URL: {settings.base_url}")
        
        # Check if directories are writable
        try:
            settings.templates_dir.mkdir(parents=True, exist_ok=True)
            settings.output_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Directories are writable")
        except Exception as e:
            print(f"❌ Directory permission error: {e}")
            return False
        
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False


def check_templates():
    """Check if templates exist."""
    print_header("Template Check")
    
    base_dir = Path(__file__).parent
    templates_dir = base_dir / "templates"
    
    if not templates_dir.exists():
        print("⚠️  Templates directory not found")
        print("   Run: python examples/create_templates.py")
        return False
    
    template_files = list(templates_dir.glob("*.*"))
    if not template_files:
        print("⚠️  No templates found")
        print("   Run: python examples/create_templates.py")
        return False
    
    print(f"✅ Found {len(template_files)} template(s):")
    for template in template_files:
        print(f"   - {template.name}")
    
    return True


def check_api_imports():
    """Check if API can be imported."""
    print_header("API Import Check")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from document_generator.api.main import app
        print("✅ FastAPI application imported successfully")
        
        from document_generator.api.document_service import DocumentService
        print("✅ Document service imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ API import failed: {e}")
        return False


def check_mcp_imports():
    """Check if MCP server can be imported."""
    print_header("MCP Server Import Check")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from document_generator.mcp_server.server import DocumentGeneratorMCPServer
        print("✅ MCP server imported successfully")
        return True
    except ImportError as e:
        print(f"❌ MCP server import failed: {e}")
        return False


def print_summary(checks):
    """Print summary of all checks."""
    print_header("Summary")
    
    passed = sum(1 for result in checks.values() if result)
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n✅ All checks passed! The system is ready to use.")
        print("\nNext steps:")
        print("  1. Start the API server:")
        print("     ./run_api.sh")
        print("     or")
        print("     python -m document_generator.api.main")
        print("\n  2. Visit http://localhost:8000/docs for API documentation")
        print("\n  3. Try the examples:")
        print("     python examples/api_example.py")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Create templates: python examples/create_templates.py")
        print("  - Check Python version: python --version (requires 3.9+)")


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print("  Document Generator Installation Verification")
    print("=" * 60)
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Directory Structure": check_directory_structure(),
        "Configuration": check_configuration(),
        "Templates": check_templates(),
        "API Imports": check_api_imports(),
        "MCP Imports": check_mcp_imports(),
    }
    
    print_summary(checks)
    
    # Return exit code
    if all(checks.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

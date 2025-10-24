#!/bin/bash
# Script to run the Document Generator API server

echo "Starting Document Generator API server..."
echo "=========================================="
echo ""

# Check if required packages are installed
python3 -c "import fastapi" 2>/dev/null || {
    echo "Error: Required packages not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
}

# Create template and output directories if they don't exist
mkdir -p templates
mkdir -p generated_documents

echo "Server starting at http://localhost:8000"
echo "API documentation will be available at:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""

# Run the server
python3 -m document_generator.api.main

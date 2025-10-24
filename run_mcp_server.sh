#!/bin/bash
# Script to run the Document Generator MCP server

echo "Starting Document Generator MCP server..."
echo "=========================================="
echo ""

# Check if required packages are installed
python3 -c "import mcp" 2>/dev/null || {
    echo "Error: Required packages not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
}

# Create template and output directories if they don't exist
mkdir -p templates
mkdir -p generated_documents

echo "MCP server starting (stdio mode)..."
echo ""

# Run the MCP server
python3 -m document_generator.mcp_server.server

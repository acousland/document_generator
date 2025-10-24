# Quick Start Guide

Get up and running with the Document Generator in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/acousland/document_generator.git
cd document_generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or for development with testing tools:

```bash
pip install -r requirements-dev.txt
```

### 3. Create Example Templates

Run the template creation script:

```bash
python examples/create_templates.py
```

This creates three example templates in the `templates/` directory:
- `letter.docx` - A business letter template
- `report.xlsx` - A monthly report template
- `presentation.pptx` - A presentation template

## Running the API Server

### Option 1: Using the Shell Script

```bash
./run_api.sh
```

### Option 2: Direct Python Command

```bash
python -m document_generator.api.main
```

### Option 3: Using Uvicorn

```bash
uvicorn document_generator.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

## Your First Document Generation

### Using cURL

Generate a Word document:

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_name": "letter",
    "document_type": "word",
    "fields": {
      "date": "January 15, 2024",
      "recipient_name": "John Doe",
      "body_text": "This is a test letter generated through the API.",
      "sender_name": "Jane Smith",
      "sender_title": "Manager",
      "company_name": "Acme Corporation",
      "phone_number": "+1-555-0123"
    },
    "return_type": "download_link"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Document generated successfully",
  "document_id": "abc123...",
  "filename": "letter_20240115_120000_abc12345.docx",
  "download_url": "http://localhost:8000/api/download/letter_20240115_120000_abc12345.docx"
}
```

Download the document:
```bash
curl -O http://localhost:8000/api/download/letter_20240115_120000_abc12345.docx
```

### Using Python

Run the example script:

```bash
python examples/api_example.py
```

This will:
1. List all available templates
2. Generate a Word document
3. Generate an Excel document
4. Generate a PowerPoint document
5. Show you how to download them

### Using the Interactive API Docs

1. Open http://localhost:8000/docs in your browser
2. Click on "POST /api/generate"
3. Click "Try it out"
4. Edit the request body
5. Click "Execute"
6. See the response and download link

## Running the MCP Server

### Start the MCP Server

```bash
./run_mcp_server.sh
```

Or directly:

```bash
python -m document_generator.mcp_server.server
```

### Configure for Claude Desktop

Add to your Claude Desktop configuration file:

**macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "document-generator": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/path/to/document_generator"
    }
  }
}
```

Restart Claude Desktop, and you'll have access to document generation tools!

## Using Docker

### Quick Start with Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker Directly

```bash
# Build
docker build -t document-generator .

# Run
docker run -d -p 8000:8000 \
  -v $(pwd)/templates:/app/templates \
  -v $(pwd)/generated_documents:/app/generated_documents \
  document-generator

# Check status
docker ps

# View logs
docker logs -f <container-id>
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=document_generator --cov-report=html
```

View coverage report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## API Endpoints Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/templates` | List all templates |
| POST | `/api/generate` | Generate a document |
| GET | `/api/download/{filename}` | Download a document |

## MCP Tools Quick Reference

| Tool | Description |
|------|-------------|
| `list_templates` | List all available templates |
| `get_template_info` | Get details about a template |
| `generate_document` | Generate a document |

## Template Syntax

Templates use `{{field_name}}` placeholders:

**Word (.docx):**
```
Dear {{recipient_name}},

{{body_text}}

Sincerely,
{{sender_name}}
```

**Excel (.xlsx):**
```
| Field | Value |
|-------|-------|
| Date  | {{date}} |
| Total | {{total}} |
```

**PowerPoint (.pptx):**
```
Slide Title: {{title}}
Content: {{content}}
```

## Common Operations

### List Templates

```bash
curl http://localhost:8000/api/templates
```

### Generate with Binary Response

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{...fields...}' \
  --output document.docx
```

### Check API Health

```bash
curl http://localhost:8000/health
```

## Next Steps

1. **Create Custom Templates** - Add your own templates to the `templates/` directory
2. **Integrate with Your App** - Use the API in your application
3. **Deploy to Production** - See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options
4. **Extend Functionality** - See [ARCHITECTURE.md](ARCHITECTURE.md) for extension points

## Troubleshooting

### Port Already in Use

Change the port:
```bash
python -m document_generator.api.main --port 8001
```

Or set environment variable:
```bash
PORT=8001 python -m document_generator.api.main
```

### Templates Not Found

Ensure templates are in the correct directory:
```bash
ls -la templates/
```

Create example templates if missing:
```bash
python examples/create_templates.py
```

### Module Import Errors

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

### Permission Denied

Make scripts executable:
```bash
chmod +x run_api.sh run_mcp_server.sh
```

## Getting Help

- **Documentation:** See [README.md](README.md) for full documentation
- **Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **Deployment:** See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides
- **Issues:** Open an issue on GitHub
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

## What's Next?

Try generating documents with your own data:

1. Create a custom template
2. Call the API with your data
3. Get your generated document instantly!

**Example:**
```python
import requests

response = requests.post('http://localhost:8000/api/generate', json={
    "template_name": "your_template",
    "document_type": "word",
    "fields": {
        "field1": "value1",
        "field2": "value2"
    }
})

print(response.json())
```

Happy document generating! 🚀

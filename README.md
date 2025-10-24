# Document Generator API & MCP Server

A powerful API and MCP (Model Context Protocol) server for generating Microsoft Office documents (Word, Excel, PowerPoint) from templates. This tool allows agents and applications to connect, specify a template, provide field values, and receive generated documents either as binary objects or download links.

## Features

- 🚀 **FastAPI REST API** - High-performance async API for document generation
- 🤖 **MCP Server** - Model Context Protocol server for AI agent integration
- 📄 **Word Documents** - Generate .docx files from templates
- 📊 **Excel Spreadsheets** - Generate .xlsx files from templates
- 📽️ **PowerPoint Presentations** - Generate .pptx files from templates
- 🔄 **Template Management** - List and manage document templates
- ⬇️ **Flexible Output** - Return documents as binary data or download links
- 🔍 **Field Discovery** - Automatically extract template field names

## Installation

### Requirements

- Python 3.9 or higher
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

### 1. Create Example Templates

First, create some example templates to work with:

```bash
python examples/create_templates.py
```

This creates three sample templates:
- `templates/letter.docx` - A letter template with placeholders
- `templates/report.xlsx` - An Excel report template
- `templates/presentation.pptx` - A PowerPoint presentation template

### 2. Start the API Server

```bash
python -m document_generator.api.main
```

Or using uvicorn directly:

```bash
uvicorn document_generator.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 3. Test the API

View the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Or run the example script:

```bash
python examples/api_example.py
```

## API Usage

### List Available Templates

```bash
curl http://localhost:8000/api/templates
```

Response:
```json
[
  {
    "name": "letter",
    "document_type": "word",
    "description": "Template for word documents",
    "fields": ["date", "recipient_name", "body_text", "sender_name", "sender_title", "company_name", "phone_number"]
  }
]
```

### Generate a Document (Download Link)

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_name": "letter",
    "document_type": "word",
    "fields": {
      "date": "2024-01-15",
      "recipient_name": "John Doe",
      "body_text": "This is a test letter.",
      "sender_name": "Jane Smith",
      "sender_title": "Manager",
      "company_name": "Acme Corp",
      "phone_number": "+1-555-0123"
    },
    "return_type": "download_link"
  }'
```

Response:
```json
{
  "success": true,
  "message": "Document generated successfully",
  "document_id": "abc123...",
  "filename": "letter_20240115_120000_abc12345.docx",
  "download_url": "http://localhost:8000/api/download/letter_20240115_120000_abc12345.docx"
}
```

### Generate a Document (Binary)

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_name": "letter",
    "document_type": "word",
    "fields": {
      "date": "2024-01-15",
      "recipient_name": "John Doe"
    },
    "return_type": "binary"
  }' \
  --output generated_letter.docx
```

### Download a Generated Document

```bash
curl -O http://localhost:8000/api/download/letter_20240115_120000_abc12345.docx
```

## MCP Server Usage

### Start the MCP Server

```bash
python -m document_generator.mcp_server.server
```

The MCP server communicates via stdio and provides the following tools:

### Available MCP Tools

1. **list_templates** - List all available templates
2. **get_template_info** - Get detailed information about a specific template
3. **generate_document** - Generate a document from a template

### MCP Tool Examples

**list_templates:**
```json
{
  "name": "list_templates",
  "arguments": {}
}
```

**get_template_info:**
```json
{
  "name": "get_template_info",
  "arguments": {
    "template_name": "letter",
    "document_type": "word"
  }
}
```

**generate_document:**
```json
{
  "name": "generate_document",
  "arguments": {
    "template_name": "letter",
    "document_type": "word",
    "fields": {
      "date": "2024-01-15",
      "recipient_name": "John Doe",
      "body_text": "Hello, this is a test."
    },
    "return_type": "download_link"
  }
}
```

## Creating Custom Templates

Templates use `{{field_name}}` as placeholders that will be replaced with actual values.

### Word Templates (.docx)

1. Create a Word document
2. Add placeholders like `{{field_name}}` wherever you want dynamic content
3. Save as a .docx file in the `templates/` directory

Example:
```
Dear {{recipient_name}},

{{body_text}}

Sincerely,
{{sender_name}}
```

### Excel Templates (.xlsx)

1. Create an Excel spreadsheet
2. Add placeholders like `{{field_name}}` in cells
3. Save as a .xlsx file in the `templates/` directory

Example:
| Report Date | {{report_date}} |
| Department  | {{department}}  |
| Revenue     | {{revenue}}     |

### PowerPoint Templates (.pptx)

1. Create a PowerPoint presentation
2. Add placeholders like `{{field_name}}` in text boxes and shapes
3. Save as a .pptx file in the `templates/` directory

## Configuration

Configuration can be set via environment variables or a `.env` file:

```env
# API Settings
API_TITLE=Document Generator API
API_VERSION=0.1.0

# Server Settings
HOST=0.0.0.0
PORT=8000

# Base URL for download links
BASE_URL=http://localhost:8000
```

## Project Structure

```
document_generator/
├── document_generator/
│   ├── __init__.py
│   ├── config.py                  # Configuration settings
│   ├── models/                    # Data models
│   │   └── __init__.py
│   ├── generators/                # Document generators
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── word_generator.py
│   │   ├── excel_generator.py
│   │   └── powerpoint_generator.py
│   ├── api/                       # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── document_service.py
│   └── mcp_server/                # MCP server
│       ├── __init__.py
│       └── server.py
├── templates/                     # Document templates
├── examples/                      # Example scripts
│   ├── create_templates.py
│   └── api_example.py
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/templates` | List all templates |
| POST | `/api/generate` | Generate a document |
| GET | `/api/download/{filename}` | Download a generated document |

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Style

The project follows Python best practices and PEP 8 style guidelines.

## Use Cases

- **Automated Report Generation** - Generate periodic reports from data
- **Document Templating** - Create personalized documents at scale
- **AI Agent Integration** - Allow AI agents to create documents
- **Workflow Automation** - Integrate with business process automation
- **Mass Mailings** - Generate personalized letters or documents
- **Data Export** - Export data to formatted Office documents

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For questions or issues, please open an issue on the GitHub repository.
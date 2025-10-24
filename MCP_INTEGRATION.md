# MCP (Model Context Protocol) Integration Guide

Complete guide for integrating the Document Generator with MCP-compatible AI agents and applications.

## What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs. It enables AI agents to:

- Discover and use tools
- Access resources
- Execute actions in a standardized way

The Document Generator MCP server exposes document generation capabilities as MCP tools that AI agents can discover and use.

## Architecture

```
┌─────────────────────┐
│   AI Agent          │
│  (Claude Desktop,   │
│   Custom App, etc.) │
└──────────┬──────────┘
           │ MCP Protocol
           │ (JSON-RPC over stdio)
           ▼
┌─────────────────────┐
│ Document Generator  │
│    MCP Server       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Document Service   │
│   & Generators      │
└─────────────────────┘
```

## Available MCP Tools

### 1. list_templates

**Description:** Lists all available document templates with their metadata.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {}
}
```

**Example Request:**
```json
{
  "name": "list_templates",
  "arguments": {}
}
```

**Example Response:**
```json
[
  {
    "name": "letter",
    "type": "word",
    "description": "Template for word documents",
    "fields": ["date", "recipient_name", "body_text", "sender_name"]
  },
  {
    "name": "report",
    "type": "excel",
    "description": "Template for excel documents",
    "fields": ["report_date", "department", "total_sales"]
  }
]
```

### 2. get_template_info

**Description:** Get detailed information about a specific template.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "template_name": {
      "type": "string",
      "description": "Name of the template"
    },
    "document_type": {
      "type": "string",
      "enum": ["word", "excel", "powerpoint"],
      "description": "Type of document"
    }
  },
  "required": ["template_name", "document_type"]
}
```

**Example Request:**
```json
{
  "name": "get_template_info",
  "arguments": {
    "template_name": "letter",
    "document_type": "word"
  }
}
```

**Example Response:**
```json
{
  "name": "letter",
  "type": "word",
  "description": "Template for word documents",
  "fields": ["date", "recipient_name", "body_text", "sender_name", "sender_title", "company_name", "phone_number"]
}
```

### 3. generate_document

**Description:** Generate a document from a template with specified field values.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "template_name": {
      "type": "string",
      "description": "Name of the template (without extension)"
    },
    "document_type": {
      "type": "string",
      "enum": ["word", "excel", "powerpoint"],
      "description": "Type of document to generate"
    },
    "fields": {
      "type": "object",
      "description": "Dictionary of field names and values"
    },
    "return_type": {
      "type": "string",
      "enum": ["binary", "download_link"],
      "description": "How to return the document",
      "default": "download_link"
    }
  },
  "required": ["template_name", "document_type", "fields"]
}
```

**Example Request:**
```json
{
  "name": "generate_document",
  "arguments": {
    "template_name": "letter",
    "document_type": "word",
    "fields": {
      "date": "January 15, 2024",
      "recipient_name": "John Doe",
      "body_text": "This is an example letter.",
      "sender_name": "Jane Smith",
      "sender_title": "Manager",
      "company_name": "Acme Corp",
      "phone_number": "+1-555-0123"
    },
    "return_type": "download_link"
  }
}
```

**Example Response:**
```json
{
  "success": true,
  "message": "Document generated successfully",
  "document_id": "abc123-def456-ghi789",
  "filename": "letter_20240115_120000_abc12345.docx",
  "download_url": "http://localhost:8000/api/download/letter_20240115_120000_abc12345.docx",
  "file_path": "/path/to/generated_documents/letter_20240115_120000_abc12345.docx"
}
```

## Integration Methods

### 1. Claude Desktop

Claude Desktop supports MCP servers out of the box.

**Configuration File Location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "document-generator": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/full/path/to/document_generator"
    }
  }
}
```

**Using Specific Python Version:**
```json
{
  "mcpServers": {
    "document-generator": {
      "command": "/usr/bin/python3.11",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/full/path/to/document_generator"
    }
  }
}
```

**Using Virtual Environment:**
```json
{
  "mcpServers": {
    "document-generator": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/full/path/to/document_generator"
    }
  }
}
```

**Windows Configuration:**
```json
{
  "mcpServers": {
    "document-generator": {
      "command": "python.exe",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "C:\\Users\\YourName\\document_generator"
    }
  }
}
```

**Verification:**
1. Save the configuration file
2. Restart Claude Desktop
3. Start a new conversation
4. The document generation tools should be available

### 2. Custom Python Application

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_document_generator():
    """Example of using the Document Generator MCP server."""
    
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "document_generator.mcp_server.server"],
        cwd="/path/to/document_generator"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools])
            
            # List templates
            result = await session.call_tool("list_templates", {})
            templates = json.loads(result.content[0].text)
            print("Templates:", templates)
            
            # Generate a document
            result = await session.call_tool("generate_document", {
                "template_name": "letter",
                "document_type": "word",
                "fields": {
                    "date": "2024-01-15",
                    "recipient_name": "John Doe",
                    "body_text": "Test letter",
                    "sender_name": "Jane Smith"
                },
                "return_type": "download_link"
            })
            
            response = json.loads(result.content[0].text)
            print("Generated document:", response)

if __name__ == "__main__":
    asyncio.run(use_document_generator())
```

### 3. Node.js Application

```javascript
const { spawn } = require('child_process');
const readline = require('readline');

class DocumentGeneratorClient {
  constructor() {
    this.process = spawn('python', [
      '-m', 
      'document_generator.mcp_server.server'
    ], {
      cwd: '/path/to/document_generator',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    this.rl = readline.createInterface({
      input: this.process.stdout
    });
  }
  
  async callTool(name, arguments) {
    return new Promise((resolve, reject) => {
      const request = {
        jsonrpc: '2.0',
        id: Date.now(),
        method: 'tools/call',
        params: { name, arguments }
      };
      
      this.process.stdin.write(JSON.stringify(request) + '\n');
      
      this.rl.once('line', (line) => {
        const response = JSON.parse(line);
        if (response.error) {
          reject(response.error);
        } else {
          resolve(response.result);
        }
      });
    });
  }
  
  async generateDocument(templateName, documentType, fields) {
    return await this.callTool('generate_document', {
      template_name: templateName,
      document_type: documentType,
      fields: fields,
      return_type: 'download_link'
    });
  }
}

// Usage
async function main() {
  const client = new DocumentGeneratorClient();
  
  const result = await client.generateDocument('letter', 'word', {
    date: '2024-01-15',
    recipient_name: 'John Doe',
    body_text: 'Hello from Node.js!',
    sender_name: 'Jane Smith'
  });
  
  console.log('Generated:', result);
}

main().catch(console.error);
```

## Use Cases

### 1. AI-Assisted Document Creation

**Scenario:** User asks Claude to create a business letter.

**Claude's Workflow:**
1. Use `list_templates` to find available letter templates
2. Ask user for necessary information
3. Use `generate_document` with filled fields
4. Provide download link to user

**Example Conversation:**
```
User: "Create a business letter to John Doe from Acme Corp."

Claude: I'll help you create a business letter. Let me gather the information...
        [Uses list_templates to find letter template]
        [Asks user for missing fields]
        [Uses generate_document with filled data]
        
        I've generated your letter. You can download it here: [download link]
```

### 2. Batch Document Generation

**Scenario:** Generate multiple reports from data.

```python
async def generate_monthly_reports(data_list):
    """Generate reports for multiple departments."""
    for department_data in data_list:
        result = await session.call_tool("generate_document", {
            "template_name": "report",
            "document_type": "excel",
            "fields": department_data,
            "return_type": "download_link"
        })
        print(f"Generated report: {result['filename']}")
```

### 3. Automated Presentation Creation

**Scenario:** Create presentation from meeting notes.

```python
async def create_presentation(meeting_notes):
    """Convert meeting notes to presentation."""
    # Extract key points from notes (AI processing)
    fields = extract_key_points(meeting_notes)
    
    # Generate presentation
    result = await session.call_tool("generate_document", {
        "template_name": "presentation",
        "document_type": "powerpoint",
        "fields": fields,
        "return_type": "download_link"
    })
    
    return result['download_url']
```

## Best Practices

### 1. Error Handling

```python
async def safe_document_generation(template, doc_type, fields):
    """Generate document with error handling."""
    try:
        # First, check template exists
        templates = await session.call_tool("list_templates", {})
        template_list = json.loads(templates.content[0].text)
        
        if not any(t['name'] == template for t in template_list):
            return {"error": f"Template '{template}' not found"}
        
        # Generate document
        result = await session.call_tool("generate_document", {
            "template_name": template,
            "document_type": doc_type,
            "fields": fields
        })
        
        return json.loads(result.content[0].text)
        
    except Exception as e:
        return {"error": str(e)}
```

### 2. Field Validation

```python
async def validate_and_generate(template_name, doc_type, fields):
    """Validate fields before generation."""
    # Get template info
    info = await session.call_tool("get_template_info", {
        "template_name": template_name,
        "document_type": doc_type
    })
    
    template_info = json.loads(info.content[0].text)
    required_fields = template_info['fields']
    
    # Check all required fields are present
    missing_fields = [f for f in required_fields if f not in fields]
    if missing_fields:
        return {"error": f"Missing fields: {missing_fields}"}
    
    # Generate document
    return await session.call_tool("generate_document", {
        "template_name": template_name,
        "document_type": doc_type,
        "fields": fields
    })
```

### 3. Resource Cleanup

```python
async def generate_and_cleanup(template, doc_type, fields):
    """Generate document and cleanup old files."""
    result = await session.call_tool("generate_document", {
        "template_name": template,
        "document_type": doc_type,
        "fields": fields
    })
    
    # Schedule cleanup of old files
    cleanup_old_documents(days=7)
    
    return result
```

## Troubleshooting MCP Integration

### Server Not Starting

**Check:**
1. Python path is correct
2. Dependencies are installed
3. Working directory is correct

**Debug:**
```bash
# Test server manually
python -m document_generator.mcp_server.server
# Should wait for input
```

### Tools Not Available

**Check:**
1. Configuration file syntax is valid JSON
2. Application has been restarted
3. Server starts without errors

**Debug:**
```json
// Add logging to config
{
  "mcpServers": {
    "document-generator": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/path/to/document_generator",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Communication Errors

**Check:**
1. stdio pipes are not blocked
2. No print statements in server code
3. JSON-RPC format is correct

## Security Considerations

### 1. Path Security
- Server only accesses templates and output directories
- No arbitrary file system access
- Sandboxed execution

### 2. Input Validation
- All inputs validated by Pydantic models
- Field values sanitized
- Template names validated

### 3. Access Control
- Consider adding authentication
- Rate limiting for production
- Audit logging

## Advanced Configuration

### Multiple Environments

```json
{
  "mcpServers": {
    "document-generator-dev": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/path/to/dev/document_generator",
      "env": {
        "BASE_URL": "http://localhost:8000"
      }
    },
    "document-generator-prod": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/path/to/prod/document_generator",
      "env": {
        "BASE_URL": "https://docs.example.com"
      }
    }
  }
}
```

### Custom Environment Variables

```json
{
  "mcpServers": {
    "document-generator": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/path/to/document_generator",
      "env": {
        "TEMPLATES_DIR": "/custom/templates",
        "OUTPUT_DIR": "/custom/output",
        "BASE_URL": "https://example.com"
      }
    }
  }
}
```

## Support

For MCP integration issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review MCP documentation: https://modelcontextprotocol.io
3. Open an issue on GitHub

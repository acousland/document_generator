# Claude Desktop MCP Server Setup - Complete ✅

## What Was Done

### 1. Python 3.11 Installation
- Installed Python 3.11 via Homebrew (`/opt/homebrew/bin/python3.11`)
- Created new virtual environment: `venv_py311`
- This allows the MCP server to run (requires Python 3.10+)

### 2. Dependencies Installed
- All packages from `requirements.txt` 
- **MCP (Model Context Protocol)** package (v1.19.0)
- All document generation libraries (python-docx, openpyxl, python-pptx, etc.)

### 3. Claude Desktop Configuration Updated
**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Configuration:**
```json
"document-generator": {
  "command": "/Users/acousland/Documents/Code/document_generator/venv_py311/bin/python",
  "args": ["-m", "document_generator.mcp_server.server"],
  "cwd": "/Users/acousland/Documents/Code/document_generator"
}
```

## How to Use

### Step 1: Restart Claude Desktop
1. Close Claude Desktop completely
2. Reopen Claude Desktop
3. Start a new conversation

### Step 2: Available Tools
Once Claude Desktop connects to the MCP server, you'll have access to three tools:

#### 1. **list_templates**
Lists all available document templates with their fields.

**Example:**
```
Claude: "What templates are available?"
→ Returns list of templates (letter, report, presentation, FHO_presentation, etc.)
```

#### 2. **get_template_info**
Get detailed information about a specific template.

**Example:**
```
Claude: "Show me the fields in the FHO_presentation template"
→ Returns: template name, type, description, and required fields
```

#### 3. **generate_document**
Generate a document from a template with your data.

**Example:**
```
Claude: "Generate a presentation using the FHO_presentation template with these details: [your data]"
→ Generates the document and provides a download link
```

## Virtual Environments

You now have two virtual environments:

### `venv` (Python 3.9) - Keep for reference
- Used for FastAPI server
- Located at: `/Users/acousland/Documents/Code/document_generator/venv`
- Command: `source venv/bin/activate`

### `venv_py311` (Python 3.11) - Use for MCP
- Used for MCP server integration with Claude Desktop
- Located at: `/Users/acousland/Documents/Code/document_generator/venv_py311`
- Command: `source venv_py311/bin/activate`

## Verification

### Check MCP Server Status
```bash
cd /Users/acousland/Documents/Code/document_generator
source venv_py311/bin/activate
python -m document_generator.mcp_server.server
# This will wait for input from Claude Desktop
```

### Check Python Version
```bash
source venv_py311/bin/activate
python --version
# Should output: Python 3.11.14
```

### Check MCP Package
```bash
source venv_py311/bin/activate
pip show mcp
# Should show: mcp version 1.19.0
```

## Templates Available

1. **letter.docx** - Letter template with recipient, sender, and body fields
2. **report.xlsx** - Monthly report template with metrics and notes
3. **presentation.pptx** - 3-slide presentation template
4. **FHO_presentation.pptx** - Your custom presentation template

## Troubleshooting

### Claude Desktop Tools Not Showing
1. Verify the config file is valid JSON
2. Check that the Python path exists: `/Users/acousland/Documents/Code/document_generator/venv_py311/bin/python`
3. Restart Claude Desktop completely
4. Open the Developer Menu to check for errors

### MCP Server Won't Start
```bash
# Test the server manually
source venv_py311/bin/activate
python -m document_generator.mcp_server.server
```

### Commands Not Found
- Make sure you're using the correct virtual environment: `venv_py311`
- Run: `source venv_py311/bin/activate`

## Next Steps

- Use Claude Desktop to generate documents from templates
- Ask Claude to generate the FHO_presentation with your data
- Download generated documents from the provided links

Enjoy! 🎉

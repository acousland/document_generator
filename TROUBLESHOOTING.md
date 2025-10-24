# Troubleshooting Guide

Common issues and solutions for the Document Generator.

## Installation Issues

### Problem: pip install fails with timeout

**Symptoms:**
```
ReadTimeoutError: HTTPSConnectionPool(host='pypi.org', port=443): Read timed out.
```

**Solutions:**
1. Increase timeout:
   ```bash
   pip install --default-timeout=200 -r requirements.txt
   ```

2. Use a different mirror:
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

3. Install packages individually:
   ```bash
   pip install fastapi uvicorn python-docx openpyxl python-pptx
   ```

### Problem: ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Check Python version:
   ```bash
   python --version  # Should be 3.9+
   ```

3. Use virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Problem: Permission denied when installing

**Symptoms:**
```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Solutions:**
1. Use user installation:
   ```bash
   pip install --user -r requirements.txt
   ```

2. Use virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Server Issues

### Problem: Port already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
1. Change port:
   ```bash
   PORT=8001 python -m document_generator.api.main
   ```

2. Kill process using port:
   ```bash
   # Find process
   lsof -i :8000  # macOS/Linux
   netstat -ano | findstr :8000  # Windows
   
   # Kill process
   kill -9 <PID>  # macOS/Linux
   taskkill /PID <PID> /F  # Windows
   ```

3. Use different port in code:
   ```python
   # Edit document_generator/config.py
   port: int = 8001
   ```

### Problem: Server starts but endpoints return 404

**Symptoms:**
```
curl http://localhost:8000/api/templates
{"detail":"Not Found"}
```

**Solutions:**
1. Check you're on the correct URL:
   ```bash
   curl http://localhost:8000/  # Root endpoint
   ```

2. Verify server is running:
   ```bash
   curl http://localhost:8000/health
   ```

3. Check logs for errors:
   ```bash
   # Look for startup errors in terminal
   ```

### Problem: Server crashes on startup

**Symptoms:**
```
ImportError: cannot import name 'BaseSettings'
```

**Solutions:**
1. Install missing dependencies:
   ```bash
   pip install pydantic-settings
   ```

2. Update all dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## Template Issues

### Problem: Template not found

**Symptoms:**
```json
{
  "success": false,
  "message": "Template 'letter' not found"
}
```

**Solutions:**
1. Check template exists:
   ```bash
   ls templates/
   ```

2. Create example templates:
   ```bash
   python examples/create_templates.py
   ```

3. Verify template name (without extension):
   ```bash
   # If file is letter.docx, use "letter" as template_name
   ```

4. Check templates directory path:
   ```bash
   # Should be in project root
   pwd
   ls templates/
   ```

### Problem: Fields not being replaced

**Symptoms:**
Generated document still shows `{{field_name}}` instead of values.

**Solutions:**
1. Check field names match exactly:
   ```bash
   # Case-sensitive: {{Name}} != {{name}}
   ```

2. Verify placeholder syntax:
   ```
   Correct: {{field_name}}
   Incorrect: {field_name} or [[field_name]]
   ```

3. Check for extra spaces:
   ```
   Correct: {{field_name}}
   Incorrect: {{ field_name }}
   ```

4. List template fields:
   ```bash
   curl http://localhost:8000/api/templates
   ```

### Problem: Generated document is corrupted

**Symptoms:**
- Document won't open
- Error message about corrupted file

**Solutions:**
1. Check template file is valid:
   ```bash
   # Open template in Office application
   # Verify it opens correctly
   ```

2. Ensure field values don't contain special characters:
   ```python
   # Escape special characters if needed
   import html
   value = html.escape(value)
   ```

3. Verify file permissions:
   ```bash
   ls -la templates/
   ls -la generated_documents/
   ```

## API Issues

### Problem: 422 Unprocessable Entity

**Symptoms:**
```json
{
  "detail": [
    {
      "loc": ["body", "document_type"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```

**Solutions:**
1. Check valid values:
   - `document_type`: "word", "excel", or "powerpoint"
   - `return_type`: "binary" or "download_link"

2. Verify request body structure:
   ```json
   {
     "template_name": "letter",
     "document_type": "word",
     "fields": {},
     "return_type": "binary"
   }
   ```

3. Check content type:
   ```bash
   curl -H "Content-Type: application/json" ...
   ```

### Problem: Binary download is empty

**Symptoms:**
- File downloads but is 0 bytes
- File is corrupted

**Solutions:**
1. Use `return_type: "download_link"` instead:
   ```json
   {
     "return_type": "download_link"
   }
   ```

2. Check file was generated:
   ```bash
   ls -lh generated_documents/
   ```

3. Use proper download method:
   ```bash
   curl -O http://localhost:8000/api/download/filename.docx
   ```

### Problem: CORS errors in browser

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solutions:**
1. Add CORS middleware in `document_generator/api/main.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. Use proxy in development

## Docker Issues

### Problem: Docker build fails

**Symptoms:**
```
ERROR: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete
```

**Solutions:**
1. Check Dockerfile syntax:
   ```bash
   docker build --no-cache -t document-generator .
   ```

2. Build with verbose output:
   ```bash
   docker build --progress=plain -t document-generator .
   ```

3. Check network connectivity:
   ```bash
   docker build --network=host -t document-generator .
   ```

### Problem: Container exits immediately

**Symptoms:**
```
docker ps  # Shows no running containers
```

**Solutions:**
1. Check logs:
   ```bash
   docker logs <container-id>
   ```

2. Run in foreground:
   ```bash
   docker run -p 8000:8000 document-generator
   ```

3. Check for missing files:
   ```bash
   docker run -it document-generator ls /app
   ```

### Problem: Cannot access container

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8000
```

**Solutions:**
1. Check port mapping:
   ```bash
   docker ps  # Look at PORTS column
   ```

2. Verify container is running:
   ```bash
   docker ps -a
   ```

3. Check firewall:
   ```bash
   # Allow port 8000
   ```

## MCP Server Issues

### Problem: MCP server not responding

**Symptoms:**
- No output from MCP server
- Claude Desktop can't connect

**Solutions:**
1. Check server is running:
   ```bash
   python -m document_generator.mcp_server.server
   # Should start and wait for input
   ```

2. Verify configuration:
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

3. Check Python path:
   ```bash
   which python  # Use full path in config
   ```

4. Restart Claude Desktop after config changes

### Problem: MCP tools not available

**Symptoms:**
- Claude Desktop doesn't show document generation tools

**Solutions:**
1. Check config file location:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Validate JSON syntax:
   ```bash
   python -m json.tool < claude_desktop_config.json
   ```

3. Check server logs in Claude Desktop

## Performance Issues

### Problem: Slow document generation

**Symptoms:**
- Generation takes > 5 seconds
- Timeouts on large documents

**Solutions:**
1. Optimize template:
   - Reduce file size
   - Remove unnecessary formatting

2. Increase timeout:
   ```python
   # In client code
   timeout = 300  # 5 minutes
   ```

3. Monitor resource usage:
   ```bash
   top  # Check CPU/memory
   ```

### Problem: High memory usage

**Symptoms:**
- Server uses excessive RAM
- Out of memory errors

**Solutions:**
1. Limit concurrent requests:
   ```python
   # Add rate limiting
   ```

2. Clear generated documents:
   ```bash
   # Add cleanup script
   find generated_documents/ -mtime +7 -delete
   ```

3. Use pagination for template lists

## Testing Issues

### Problem: Tests fail to run

**Symptoms:**
```
ModuleNotFoundError: No module named 'pytest'
```

**Solutions:**
1. Install test dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run from project root:
   ```bash
   cd /path/to/document_generator
   pytest
   ```

### Problem: Test failures

**Symptoms:**
```
FAILED tests/test_api.py::test_generate_document
```

**Solutions:**
1. Check if server is running:
   ```bash
   # Stop server before running tests
   ```

2. Clear test files:
   ```bash
   rm -rf generated_documents/*
   ```

3. Run with verbose output:
   ```bash
   pytest -v -s
   ```

## File Permission Issues

### Problem: Permission denied writing files

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'generated_documents/file.docx'
```

**Solutions:**
1. Check directory permissions:
   ```bash
   ls -la generated_documents/
   ```

2. Create directory if missing:
   ```bash
   mkdir -p generated_documents
   chmod 755 generated_documents
   ```

3. Fix ownership:
   ```bash
   chown -R $USER:$USER generated_documents
   ```

## Logging and Debugging

### Enable Debug Logging

```python
# In document_generator/config.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Application Logs

```bash
# When running directly
python -m document_generator.api.main 2>&1 | tee app.log

# With Docker
docker logs -f <container-id>

# With systemd
journalctl -u document-generator -f
```

### Test Individual Components

```python
# Test generator
from document_generator.generators import WordGenerator
gen = WordGenerator()
gen.generate(template_path, fields, output_path)

# Test service
from document_generator.api.document_service import DocumentService
service = DocumentService()
templates = service.list_templates()
```

## Getting More Help

If you're still experiencing issues:

1. **Check Documentation:**
   - [README.md](README.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)
   - [DEPLOYMENT.md](DEPLOYMENT.md)

2. **Search Issues:**
   - GitHub Issues: Look for similar problems

3. **Create Issue:**
   - Include error messages
   - Include steps to reproduce
   - Include environment details:
     ```bash
     python --version
     pip list | grep -E "(fastapi|uvicorn|docx|openpyxl|pptx)"
     uname -a  # OS information
     ```

4. **Ask for Help:**
   - Open a GitHub issue
   - Provide minimal reproduction example
   - Include relevant logs

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing package | `pip install -r requirements.txt` |
| `FileNotFoundError` | Missing template | Create template or check path |
| `PermissionError` | No write access | Fix directory permissions |
| `ConnectionRefusedError` | Server not running | Start the server |
| `422 Unprocessable Entity` | Invalid request | Check request format |
| `404 Not Found` | Wrong endpoint | Verify URL |
| `500 Internal Server Error` | Server error | Check logs |

"""MCP Server for document generation."""

import asyncio
import json
from typing import Any
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from ..api.document_service import DocumentService
from ..models import GenerateDocumentRequest, TemplateInfo
from ..config import settings


class DocumentGeneratorMCPServer:
    """MCP Server for document generation."""
    
    def __init__(self):
        self.server = Server("document-generator")
        self.document_service = DocumentService()
        self.setup_tools()
    
    def setup_tools(self):
        """Set up MCP tools."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="list_templates",
                    description="List all available document templates",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    }
                ),
                Tool(
                    name="get_template_info",
                    description="Get detailed information about a specific template",
                    inputSchema={
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
                ),
                Tool(
                    name="generate_document",
                    description="Generate a document from a template with specified fields",
                    inputSchema={
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
                                "description": "Dictionary of field names and values to populate in the template"
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
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            
            if name == "list_templates":
                templates = self.document_service.list_templates()
                result = [
                    {
                        "name": t.name,
                        "type": t.document_type,
                        "description": t.description,
                        "fields": t.fields
                    }
                    for t in templates
                ]
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            
            elif name == "get_template_info":
                template_name = arguments.get("template_name")
                document_type = arguments.get("document_type")
                
                templates = self.document_service.list_templates()
                template = next(
                    (t for t in templates if t.name == template_name and t.document_type == document_type),
                    None
                )
                
                if not template:
                    return [TextContent(
                        type="text",
                        text=json.dumps({"error": f"Template '{template_name}' of type '{document_type}' not found"})
                    )]
                
                result = {
                    "name": template.name,
                    "type": template.document_type,
                    "description": template.description,
                    "fields": template.fields
                }
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            
            elif name == "generate_document":
                # Create request object
                request = GenerateDocumentRequest(
                    template_name=arguments.get("template_name"),
                    document_type=arguments.get("document_type"),
                    fields=arguments.get("fields", {}),
                    return_type=arguments.get("return_type", "download_link")
                )
                
                # Generate document
                response, output_path = self.document_service.generate_document(request)
                
                result = {
                    "success": response.success,
                    "message": response.message,
                    "document_id": response.document_id,
                    "filename": response.filename,
                    "download_url": response.download_url,
                }
                
                if output_path:
                    result["file_path"] = str(output_path)
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            
            else:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"})
                )]
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the MCP server."""
    server = DocumentGeneratorMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

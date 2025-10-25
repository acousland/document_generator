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
                    name="get_powerpoint_slide_types",
                    description="Get available slide types from a PowerPoint template. Each slide type is a reusable layout that can be used zero, one, or multiple times when composing a presentation. Slide types can be used in any order you choose - you're not limited to the order they appear in the template.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "template_name": {
                                "type": "string",
                                "description": "Name of the PowerPoint template (without .pptx extension)"
                            }
                        },
                        "required": ["template_name"]
                    }
                ),
                Tool(
                    name="generate_document",
                    description="Generate a document from a template. For PowerPoint: compose a custom presentation by selecting which slide types to use and in what order. You can use any slide type multiple times, skip slide types you don't need, and arrange them however makes sense for the content. Think of slide types as building blocks you can mix and match.",
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
                                "description": "Dictionary of field names and values (for simple generation)"
                            },
                            "slides": {
                                "type": "array",
                                "description": "Array of slide specifications for PowerPoint (advanced composition mode). Each item specifies which slide_type to use and what content to put in it. You choose: which types, how many of each, and in what order. For example: [title_page, content, content, content, two_column, closing] uses 'content' three times in a row.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "slide_type": {
                                            "type": "string",
                                            "description": "Type of slide to use"
                                        },
                                        "fields": {
                                            "type": "object",
                                            "description": "Fields to populate in this slide"
                                        }
                                    },
                                    "required": ["slide_type", "fields"]
                                }
                            },
                            "return_type": {
                                "type": "string",
                                "enum": ["binary", "download_link"],
                                "description": "How to return the document",
                                "default": "download_link"
                            }
                        },
                        "required": ["template_name", "document_type"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            try:
                return await _handle_tool(name, arguments)
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Tool execution failed: {str(e)}"})
                )]
        
        async def _handle_tool(name: str, arguments: Any) -> list[TextContent]:
            """Internal handler for tools to allow try-catch wrapper."""
            
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
            
            elif name == "get_powerpoint_slide_types":
                template_name = arguments.get("template_name")
                
                try:
                    slide_types = self.document_service.get_template_slide_types(template_name)
                    result = {
                        "template_name": template_name,
                        "slide_types": slide_types
                    }
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                except FileNotFoundError:
                    return [TextContent(
                        type="text",
                        text=json.dumps({"error": f"Template '{template_name}.pptx' not found"})
                    )]
                except Exception as e:
                    return [TextContent(
                        type="text",
                        text=json.dumps({"error": f"Error reading template: {str(e)}"})
                    )]
            
            elif name == "generate_document":
                # Create request object
                from ..models import SlideSpec
                
                slides_data = arguments.get("slides")
                slides = None
                if slides_data:
                    slides = [SlideSpec(**slide) for slide in slides_data]
                
                request = GenerateDocumentRequest(
                    template_name=arguments.get("template_name"),
                    document_type=arguments.get("document_type"),
                    fields=arguments.get("fields"),
                    slides=slides,
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

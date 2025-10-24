"""Example of how to interact with the MCP server programmatically.

This example demonstrates how an MCP client would interact with the document
generator MCP server.
"""

import json


def example_mcp_requests():
    """
    Examples of MCP tool calls that can be sent to the document generator MCP server.
    
    Note: These are examples of the JSON payloads that would be sent via the MCP protocol.
    In a real implementation, these would be sent through the MCP client library.
    """
    
    print("Example MCP Tool Calls")
    print("=" * 60)
    
    # Example 1: List all templates
    list_templates_request = {
        "name": "list_templates",
        "arguments": {}
    }
    print("\n1. List Templates Request:")
    print(json.dumps(list_templates_request, indent=2))
    
    # Example 2: Get specific template info
    get_template_info_request = {
        "name": "get_template_info",
        "arguments": {
            "template_name": "letter",
            "document_type": "word"
        }
    }
    print("\n2. Get Template Info Request:")
    print(json.dumps(get_template_info_request, indent=2))
    
    # Example 3: Generate a Word document
    generate_word_request = {
        "name": "generate_document",
        "arguments": {
            "template_name": "letter",
            "document_type": "word",
            "fields": {
                "date": "2024-01-15",
                "recipient_name": "John Doe",
                "body_text": "This letter was generated through the MCP server.",
                "sender_name": "Jane Smith",
                "sender_title": "Manager",
                "company_name": "Acme Corporation",
                "phone_number": "+1-555-0123"
            },
            "return_type": "download_link"
        }
    }
    print("\n3. Generate Word Document Request:")
    print(json.dumps(generate_word_request, indent=2))
    
    # Example 4: Generate an Excel document
    generate_excel_request = {
        "name": "generate_document",
        "arguments": {
            "template_name": "report",
            "document_type": "excel",
            "fields": {
                "report_date": "2024-01-31",
                "department": "Sales",
                "total_sales": "150",
                "new_customers": "25",
                "revenue": "$75,000",
                "notes": "Excellent performance this month."
            },
            "return_type": "download_link"
        }
    }
    print("\n4. Generate Excel Document Request:")
    print(json.dumps(generate_excel_request, indent=2))
    
    # Example 5: Generate a PowerPoint document
    generate_ppt_request = {
        "name": "generate_document",
        "arguments": {
            "template_name": "presentation",
            "document_type": "powerpoint",
            "fields": {
                "presentation_title": "Q1 2024 Results",
                "presenter_name": "Jane Smith",
                "date": "January 31, 2024",
                "slide_title": "Key Achievements",
                "bullet_1": "Exceeded sales targets by 20%",
                "bullet_2": "Acquired 25 new customers",
                "bullet_3": "Launched 3 new products",
                "summary": "Outstanding quarter with record performance."
            },
            "return_type": "download_link"
        }
    }
    print("\n5. Generate PowerPoint Document Request:")
    print(json.dumps(generate_ppt_request, indent=2))
    
    print("\n" + "=" * 60)
    print("\nHow to use with Claude Desktop or other MCP clients:")
    print("\n1. Add this configuration to your MCP client settings:")
    print("""
{
  "mcpServers": {
    "document-generator": {
      "command": "python",
      "args": ["-m", "document_generator.mcp_server.server"],
      "cwd": "/path/to/document_generator"
    }
  }
}
""")
    print("\n2. The MCP client will be able to use these tools:")
    print("   - list_templates: List all available templates")
    print("   - get_template_info: Get details about a specific template")
    print("   - generate_document: Generate a document from a template")
    
    print("\n3. AI agents can then use these tools to generate documents")
    print("   based on user requests, automatically filling in fields.")


if __name__ == "__main__":
    example_mcp_requests()

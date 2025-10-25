"""Example of using the advanced PowerPoint generator with metadata-driven slides."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_generator.generators.powerpoint_advanced_generator import PowerPointAdvancedGenerator


def example_get_slide_types():
    """Example: Get available slide types from a template."""
    print("=" * 70)
    print("EXAMPLE 1: Get Slide Types from Template")
    print("=" * 70)
    
    generator = PowerPointAdvancedGenerator()
    template_path = Path("templates/advanced_presentation.pptx")
    
    slide_types = generator.get_template_slide_types(template_path)
    
    print(f"\nTemplate: {template_path.name}")
    print(f"Found {len(slide_types)} slide types:\n")
    
    for slide_info in slide_types:
        print(f"📊 Slide Type: '{slide_info['slide_type']}'")
        print(f"   Description: {slide_info['description']}")
        print(f"   Placeholders:")
        for field_name, field_info in slide_info['placeholders'].items():
            field_type = field_info.get('type', 'text')
            field_desc = field_info.get('description', '')
            print(f"     - {field_name} ({field_type}): {field_desc}")
        print()


def example_generate_presentation():
    """Example: Generate a presentation by composing slides."""
    print("=" * 70)
    print("EXAMPLE 2: Generate Presentation from Slides")
    print("=" * 70)
    
    generator = PowerPointAdvancedGenerator()
    template_path = Path("templates/advanced_presentation.pptx")
    output_path = Path("generated_documents/my_presentation.pptx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Define the slides to include
    slides_data = [
        {
            "slide_type": "title_page",
            "fields": {
                "title": "Q4 Business Review",
                "subtitle": "October 25, 2025",
                "presenter": "Jane Smith, CEO"
            }
        },
        {
            "slide_type": "section_break",
            "fields": {
                "section_title": "Executive Summary"
            }
        },
        {
            "slide_type": "content",
            "fields": {
                "heading": "Key Achievements",
                "body": "This quarter we achieved significant growth across all business units.",
                "bullet_points": [
                    "Revenue increased 25% YoY",
                    "Launched 3 new products",
                    "Expanded to 5 new markets",
                    "Customer satisfaction at all-time high"
                ]
            }
        },
        {
            "slide_type": "two_column",
            "fields": {
                "heading": "Opportunities & Challenges",
                "left_heading": "Opportunities",
                "left_content": "• Growing market demand\n• Strategic partnerships\n• Technology innovations\n• Emerging markets",
                "right_heading": "Challenges",
                "right_content": "• Competitive pressure\n• Supply chain issues\n• Talent acquisition\n• Regulatory changes"
            }
        },
        {
            "slide_type": "section_break",
            "fields": {
                "section_title": "Financial Performance"
            }
        },
        {
            "slide_type": "content",
            "fields": {
                "heading": "Revenue & Profit",
                "body": "Strong financial performance across all metrics.",
                "bullet_points": [
                    "Revenue: $50M (↑25%)",
                    "Gross Margin: 65%",
                    "Operating Income: $15M",
                    "Net Profit Margin: 22%"
                ]
            }
        },
        {
            "slide_type": "closing",
            "fields": {
                "closing_message": "Thank You!",
                "contact_info": "jane.smith@company.com | (555) 123-4567"
            }
        }
    ]
    
    # Generate the presentation
    print(f"\n📝 Generating presentation with {len(slides_data)} slides...")
    result_path = generator.generate_from_slides(template_path, slides_data, output_path)
    
    print(f"✅ Presentation generated successfully!")
    print(f"📄 Output: {result_path}")
    print(f"📊 Total slides: {len(slides_data)}")


def example_mcp_usage():
    """Example: How this would be used via MCP."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: MCP Usage Pattern")
    print("=" * 70)
    
    print("""
In Claude Desktop, you would interact like this:

USER: "What slide types are available in advanced_presentation?"

CLAUDE uses tool: get_powerpoint_slide_types
  Arguments: {"template_name": "advanced_presentation"}
  
Returns:
  - title_page: Main title slide
  - section_break: Section divider
  - content: Heading, body, and bullet points
  - two_column: Side-by-side content
  - closing: Closing message and contact

---

USER: "Create a Q4 review presentation with a title page, overview, 
      and closing slide"

CLAUDE uses tool: generate_document
  Arguments: {
    "template_name": "advanced_presentation",
    "document_type": "powerpoint",
    "slides": [
      {
        "slide_type": "title_page",
        "fields": {
          "title": "Q4 Review",
          "subtitle": "October 2025",
          "presenter": "Your Name"
        }
      },
      {
        "slide_type": "content",
        "fields": {
          "heading": "Overview",
          "body": "Key highlights from Q4...",
          "bullet_points": ["Point 1", "Point 2", "Point 3"]
        }
      },
      {
        "slide_type": "closing",
        "fields": {
          "closing_message": "Thank You!",
          "contact_info": "email@company.com"
        }
      }
    ]
  }

Returns: Download link to generated presentation!
""")


if __name__ == "__main__":
    # Run examples
    example_get_slide_types()
    print("\n")
    example_generate_presentation()
    example_mcp_usage()

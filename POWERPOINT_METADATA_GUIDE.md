# Metadata-Driven PowerPoint Generation Guide

## Overview

The advanced PowerPoint generator uses **metadata in slide notes** to create flexible, composable presentations. Each slide in your template contains JSON metadata describing its type and placeholders.

## How It Works

### 1. Template Structure

Each slide in your template has **metadata in the Notes section** (not visible in slide show):

⚠️ **Important Note About Quotes**: PowerPoint automatically converts straight quotes (`"`) to smart/curly quotes (`"` and `"`). The system handles this automatically, so your JSON will work even if PowerPoint changes the quote style.

```json
{
  "slide_type": "content",
  "description": "Standard content slide",
  "placeholders": {
    "heading": {
      "type": "text",
      "description": "Slide heading"
    },
    "body": {
      "type": "paragraph",
      "description": "Main content"
    },
    "bullet_points": {
      "type": "list",
      "description": "Key points"
    }
  }
}
```

### 2. Field Types Supported

- **text**: Single line text
- **paragraph**: Multi-line text
- **list**: Array of bullet points
- **table**: 2D array of data (coming soon)
- **image**: Image insertion (coming soon)
- **number**: Formatted numbers (coming soon)
- **date**: Formatted dates (coming soon)

### 3. Creating a Template

#### Option A: Use PowerPoint + Manual JSON

1. Create slides in PowerPoint
2. Add placeholders like `{{field_name}}`
3. Click "Notes" button at bottom
4. Paste JSON metadata for each slide

#### Option B: Use Python Script

```python
from examples.create_advanced_template import create_advanced_presentation_template
create_advanced_presentation_template()
```

## Using via MCP/Claude Desktop

### Key Concept: Slide Types are Building Blocks

Think of slide types as **LEGO blocks** - you can:
- ✅ Use any slide type multiple times (e.g., 5 "content" slides in a row)
- ✅ Skip slide types you don't need (template has "closing"? Don't use it if you don't want it)
- ✅ Arrange them in any order (not limited to template order)
- ✅ Mix and match based on your content needs

The template order doesn't matter - it's just a library of available layouts!

### Step 1: Discover Available Slide Types

**Claude Desktop Interaction:**
```
You: "What slide types are in advanced_presentation?"

Claude uses: get_powerpoint_slide_types
Arguments: {"template_name": "advanced_presentation"}

Returns:
- title_page: Title, subtitle, presenter
- section_break: Section heading
- content: Heading, body, bullet points
- two_column: Side-by-side content
- closing: Closing message and contact
```

### Step 2: Generate a Presentation

**Claude Desktop Interaction:**
```
You: "Create a Q4 review presentation with:
     - Title page
     - 3 slides about different achievements
     - A comparison slide
     - 2 more content slides about plans
     - Closing"

Claude thinks: "I need title_page (once), content (5 times!), 
                 two_column (once), closing (once)"

Claude uses: generate_document
Arguments: {
  "template_name": "advanced_presentation",
  "document_type": "powerpoint",
  "slides": [
    {"slide_type": "title_page", "fields": {...}},
    {"slide_type": "content", "fields": {"heading": "Achievement 1", ...}},
    {"slide_type": "content", "fields": {"heading": "Achievement 2", ...}},
    {"slide_type": "content", "fields": {"heading": "Achievement 3", ...}},
    {"slide_type": "two_column", "fields": {"heading": "Pros vs Cons", ...}},
    {"slide_type": "content", "fields": {"heading": "Q1 Plans", ...}},
    {"slide_type": "content", "fields": {"heading": "Q2 Plans", ...}},
    {"slide_type": "closing", "fields": {...}}
  ]
}

Notice: "content" was used 5 times! "section_break" wasn't used at all!
```

### Example: Flexible Composition

### Example: Flexible Composition

```
User: "Make a 10-slide deck about our product"

Template has: title_page, section_break, content, two_column, closing

Claude can create:
- title_page (1x)
- content (7x) - reusing this layout 7 times!
- two_column (1x)  
- closing (1x)
= 10 slides total

Claude skipped "section_break" completely because it wasn't needed.
```

**Another Example:**
```
User: "Create a comparison-heavy presentation"

Claude can create:
- title_page (1x)
- two_column (5x) - using comparison layout 5 times!
- closing (1x)
= 7 slides total
```

**Old Approach:**
```
You: "Create a presentation with title, content, and closing slides"

Claude uses: generate_document
Arguments: {
  "template_name": "advanced_presentation",
  "document_type": "powerpoint",
  "slides": [
    {
      "slide_type": "title_page",
      "fields": {
        "title": "Q4 Business Review",
        "subtitle": "October 2025",
        "presenter": "Jane Smith"
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
        "body": "This quarter showed strong growth",
        "bullet_points": [
          "Revenue up 25%",
          "3 new products launched",
          "Customer satisfaction high"
        ]
      }
    },
    {
      "slide_type": "closing",
      "fields": {
        "closing_message": "Thank You!",
        "contact_info": "jane@company.com"
      }
    }
  ]
}

Returns: Download link to presentation!
```

## Creating Your Own FHO Template

### Step 1: Design Slides in PowerPoint

1. Create each slide layout you want
2. Use `{{placeholder_name}}` for dynamic content
3. Style everything (fonts, colors, positions)

### Step 2: Add Metadata to Each Slide

For each slide:

1. Click "Notes" at bottom of PowerPoint
2. Add JSON metadata:

```json
{
  "slide_type": "financial_summary",
  "description": "Financial results slide",
  "placeholders": {
    "quarter": {"type": "text", "description": "Quarter name"},
    "revenue": {"type": "number", "description": "Total revenue"},
    "highlights": {"type": "list", "description": "Key metrics"}
  }
}
```

### Step 3: Save Template

Save as `FHO_presentation.pptx` in `templates/` folder.

### Step 4: Test It

```python
# Get slide types
from document_generator.generators.powerpoint_advanced_generator import PowerPointAdvancedGenerator

generator = PowerPointAdvancedGenerator()
slide_types = generator.get_template_slide_types("templates/FHO_presentation.pptx")

for slide in slide_types:
    print(f"{slide['slide_type']}: {slide['description']}")
```

## Example Metadata for Common Slides

### Title Slide
```json
{
  "slide_type": "title",
  "description": "Main title slide",
  "placeholders": {
    "title": {"type": "text", "description": "Presentation title"},
    "subtitle": {"type": "text", "description": "Subtitle or date"},
    "presenter": {"type": "text", "description": "Presenter name"}
  }
}
```

### Data Slide
```json
{
  "slide_type": "metrics",
  "description": "Key metrics slide",
  "placeholders": {
    "heading": {"type": "text", "description": "Section heading"},
    "metric1": {"type": "number", "description": "First metric"},
    "metric2": {"type": "number", "description": "Second metric"},
    "notes": {"type": "paragraph", "description": "Additional notes"}
  }
}
```

### Comparison Slide
```json
{
  "slide_type": "comparison",
  "description": "Side-by-side comparison",
  "placeholders": {
    "title": {"type": "text", "description": "Slide title"},
    "left_heading": {"type": "text", "description": "Left column heading"},
    "left_content": {"type": "list", "description": "Left column points"},
    "right_heading": {"type": "text", "description": "Right column heading"},
    "right_content": {"type": "list", "description": "Right column points"}
  }
}
```

## API Endpoints

### Get Slide Types
```
GET /api/templates/{template_name}/slides

Response:
{
  "template_name": "advanced_presentation",
  "slide_types": [...]
}
```

### Generate Presentation
```
POST /api/generate
{
  "template_name": "advanced_presentation",
  "document_type": "powerpoint",
  "slides": [...]
}
```

## Tips for Template Design

1. **Keep it simple**: Start with 3-5 slide types
2. **Be consistent**: Use same placeholder naming pattern
3. **Test early**: Generate a sample deck to verify
4. **Document**: Use clear descriptions in metadata
5. **Version**: Keep template in version control

## Troubleshooting

**Slide type not found:**
- Check spelling in metadata `slide_type` field
- Verify metadata is valid JSON
- Use `get_powerpoint_slide_types` to list available types

**Fields not populated:**
- Check placeholder spelling: `{{field_name}}`
- Ensure field names match metadata exactly
- Verify field is in correct slide type

**Bullet points not working:**
- Use array of strings: `["Point 1", "Point 2"]`
- Ensure field type is "list" in metadata
- Check placeholder is in a text box

## Next Steps

1. Create your FHO template with metadata
2. Test it with the example script
3. Restart Claude Desktop
4. Ask Claude to generate presentations!

The system will understand your template structure automatically. 🎉

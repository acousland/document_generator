"""Example script demonstrating API usage."""

import requests
import json


# API base URL
BASE_URL = "http://localhost:8000"


def list_templates():
    """List all available templates."""
    response = requests.get(f"{BASE_URL}/api/templates")
    print("Available Templates:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


def generate_word_document():
    """Generate a Word document."""
    request_data = {
        "template_name": "letter",
        "document_type": "word",
        "fields": {
            "date": "2024-01-15",
            "recipient_name": "John Doe",
            "body_text": "This is an example letter generated from a template using our document generation API.",
            "sender_name": "Jane Smith",
            "sender_title": "Manager",
            "company_name": "Acme Corporation",
            "phone_number": "+1-555-0123"
        },
        "return_type": "download_link"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate", json=request_data)
    print("\nGenerated Word Document:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


def generate_excel_document():
    """Generate an Excel document."""
    request_data = {
        "template_name": "report",
        "document_type": "excel",
        "fields": {
            "report_date": "2024-01-31",
            "department": "Sales",
            "total_sales": "150",
            "new_customers": "25",
            "revenue": "$75,000",
            "notes": "Excellent performance this month. Sales exceeded targets by 20%."
        },
        "return_type": "download_link"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate", json=request_data)
    print("\nGenerated Excel Document:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


def generate_powerpoint_document():
    """Generate a PowerPoint document."""
    request_data = {
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
            "summary": "Outstanding quarter with record-breaking performance across all metrics."
        },
        "return_type": "download_link"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate", json=request_data)
    print("\nGenerated PowerPoint Document:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


def download_document(filename):
    """Download a generated document."""
    response = requests.get(f"{BASE_URL}/api/download/{filename}")
    if response.status_code == 200:
        with open(f"downloaded_{filename}", "wb") as f:
            f.write(response.content)
        print(f"\nDocument downloaded: downloaded_{filename}")
    else:
        print(f"\nError downloading document: {response.status_code}")


if __name__ == "__main__":
    print("Document Generator API Examples\n")
    print("=" * 50)
    
    # List templates
    templates = list_templates()
    
    print("\n" + "=" * 50)
    
    # Generate documents
    word_result = generate_word_document()
    excel_result = generate_excel_document()
    ppt_result = generate_powerpoint_document()
    
    print("\n" + "=" * 50)
    print("\nTo download a document, use:")
    if word_result.get("filename"):
        print(f"  curl -O {BASE_URL}/api/download/{word_result['filename']}")

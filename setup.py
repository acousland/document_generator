from setuptools import setup, find_packages

setup(
    name="document_generator",
    version="0.1.0",
    description="API & MCP server for generating Microsoft Office documents from templates",
    author="acousland",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "python-multipart>=0.0.6",
        "python-docx>=1.1.0",
        "openpyxl>=3.1.2",
        "python-pptx>=0.6.23",
        "pydantic>=2.5.0",
        "aiofiles>=23.2.1",
        "jinja2>=3.1.2",
        "mcp>=0.9.0",
    ],
    python_requires=">=3.9",
)

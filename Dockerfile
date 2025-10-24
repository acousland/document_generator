FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY document_generator/ ./document_generator/
COPY setup.py .
COPY pyproject.toml .

# Install the package
RUN pip install -e .

# Create directories for templates and generated documents
RUN mkdir -p /app/templates /app/generated_documents

# Expose the API port
EXPOSE 8000

# Run the API server
CMD ["python", "-m", "document_generator.api.main"]

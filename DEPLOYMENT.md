# Deployment Guide

This guide covers different deployment options for the Document Generator API & MCP Server.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)

## Local Development

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create example templates:**
   ```bash
   python examples/create_templates.py
   ```

3. **Start the API server:**
   ```bash
   ./run_api.sh
   ```
   Or manually:
   ```bash
   python -m document_generator.api.main
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running the MCP Server

```bash
./run_mcp_server.sh
```

Or manually:
```bash
python -m document_generator.mcp_server.server
```

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and start:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop:**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t document-generator .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v $(pwd)/templates:/app/templates \
     -v $(pwd)/generated_documents:/app/generated_documents \
     -e BASE_URL=http://your-domain.com \
     --name document-generator \
     document-generator
   ```

3. **Check logs:**
   ```bash
   docker logs -f document-generator
   ```

## Cloud Deployment

### AWS Elastic Container Service (ECS)

1. **Build and push to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com
   docker build -t document-generator .
   docker tag document-generator:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/document-generator:latest
   docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/document-generator:latest
   ```

2. **Create ECS Task Definition** with:
   - Container port: 8000
   - Environment variables for configuration
   - EFS volume for templates and generated documents

3. **Create ECS Service** with:
   - Load balancer for HTTPS traffic
   - Auto-scaling configuration
   - Health checks on `/health` endpoint

### Google Cloud Run

1. **Build and deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/your-project-id/document-generator
   gcloud run deploy document-generator \
     --image gcr.io/your-project-id/document-generator \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8000
   ```

2. **Configure Cloud Storage** for templates and generated documents

### Azure Container Instances

1. **Build and push to ACR:**
   ```bash
   az acr build --registry your-registry --image document-generator .
   ```

2. **Deploy to ACI:**
   ```bash
   az container create \
     --resource-group your-resource-group \
     --name document-generator \
     --image your-registry.azurecr.io/document-generator \
     --dns-name-label document-generator \
     --ports 8000
   ```

### Kubernetes

1. **Create deployment.yaml:**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: document-generator
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: document-generator
     template:
       metadata:
         labels:
           app: document-generator
       spec:
         containers:
         - name: document-generator
           image: document-generator:latest
           ports:
           - containerPort: 8000
           env:
           - name: BASE_URL
             value: "https://your-domain.com"
           volumeMounts:
           - name: templates
             mountPath: /app/templates
           - name: generated-docs
             mountPath: /app/generated_documents
         volumes:
         - name: templates
           persistentVolumeClaim:
             claimName: templates-pvc
         - name: generated-docs
           persistentVolumeClaim:
             claimName: generated-docs-pvc
   ```

2. **Apply:**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

## Production Considerations

### Security

1. **Use HTTPS:**
   - Configure SSL/TLS certificates
   - Use a reverse proxy (nginx, Caddy) or cloud load balancer

2. **Authentication:**
   - Add API key authentication
   - Implement OAuth 2.0 for user authentication
   - Use JWT tokens for session management

3. **Rate Limiting:**
   - Implement rate limiting to prevent abuse
   - Use services like Cloudflare or AWS WAF

### Performance

1. **Horizontal Scaling:**
   - Deploy multiple instances
   - Use a load balancer

2. **Caching:**
   - Cache generated documents for repeated requests
   - Use Redis for caching

3. **Storage:**
   - Use object storage (S3, GCS, Azure Blob) for generated documents
   - Set up automatic cleanup of old documents

### Monitoring

1. **Health Checks:**
   - Use the `/health` endpoint
   - Monitor response times

2. **Logging:**
   - Centralize logs (CloudWatch, Stackdriver, ELK)
   - Monitor error rates

3. **Metrics:**
   - Track document generation rates
   - Monitor storage usage
   - Set up alerts for failures

### Environment Variables

Set these in production:

```bash
# API Configuration
API_TITLE=Document Generator API
API_VERSION=0.1.0

# Server
HOST=0.0.0.0
PORT=8000

# URLs
BASE_URL=https://your-domain.com

# Storage (if using cloud storage)
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1

# Authentication (if implemented)
API_KEY_ENABLED=true
JWT_SECRET=your-secret-key
```

### Backup and Recovery

1. **Templates:**
   - Keep templates in version control
   - Back up to multiple locations

2. **Generated Documents:**
   - Implement retention policies
   - Regular backups to object storage

### Scaling

The application is stateless and can be easily scaled horizontally:

- Use container orchestration (Kubernetes, ECS)
- Shared storage for templates and generated documents
- Load balancer for traffic distribution

### Database (Optional Enhancement)

Consider adding a database for:
- Document generation history
- User management
- Template metadata
- Analytics

Recommended databases:
- PostgreSQL for relational data
- MongoDB for document-based storage

## Support

For deployment issues, please open an issue on GitHub.

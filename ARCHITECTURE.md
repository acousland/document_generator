# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Clients                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   cURL   │  │  Python  │  │   Web    │  │MCP Client│    │
│  │          │  │  Client  │  │ Browser  │  │ (AI Agent│    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        │ HTTP/REST   │ HTTP/REST   │ HTTP/REST   │ MCP/stdio
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   FastAPI    │  │   FastAPI    │  │  MCP Server  │
│   Server     │  │   Server     │  │              │
│   Instance   │  │   Instance   │  │   (stdio)    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Document        │
              │  Service         │
              │  (Business Logic)│
              └─────────┬────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│     Word     │ │    Excel     │ │  PowerPoint  │
│  Generator   │ │  Generator   │ │  Generator   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │               │               │
       └───────────────┴───────────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │  Template Storage   │
            │   & File System     │
            └─────────────────────┘
```

## Component Description

### 1. API Layer (FastAPI)

**File:** `document_generator/api/main.py`

- RESTful API endpoints
- Request validation using Pydantic
- OpenAPI/Swagger documentation
- Async request handling
- CORS support (configurable)

**Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/templates` - List templates
- `POST /api/generate` - Generate documents
- `GET /api/download/{filename}` - Download files

### 2. MCP Server Layer

**File:** `document_generator/mcp_server/server.py`

- Model Context Protocol implementation
- stdio-based communication
- Tool definitions for AI agents
- JSON-based request/response

**Tools:**
- `list_templates` - Discover available templates
- `get_template_info` - Get template metadata
- `generate_document` - Create documents

### 3. Service Layer

**File:** `document_generator/api/document_service.py`

- Business logic orchestration
- Template management
- Document generation coordination
- File naming and storage

**Responsibilities:**
- Validate template existence
- Route to appropriate generator
- Manage file paths
- Generate unique IDs

### 4. Generator Layer

**Files:**
- `document_generator/generators/word_generator.py`
- `document_generator/generators/excel_generator.py`
- `document_generator/generators/powerpoint_generator.py`

**Responsibilities:**
- Load template files
- Parse placeholder syntax (`{{field_name}}`)
- Replace placeholders with values
- Save generated documents

### 5. Data Models

**File:** `document_generator/models/__init__.py`

- Request/Response schemas
- Data validation
- Type safety
- API contracts

**Models:**
- `GenerateDocumentRequest`
- `GenerateDocumentResponse`
- `TemplateInfo`

## Data Flow

### Document Generation Flow

```
1. Client Request
   │
   ▼
2. API/MCP Endpoint
   │ (validates request)
   ▼
3. Document Service
   │ (finds template)
   │ (selects generator)
   ▼
4. Generator (Word/Excel/PowerPoint)
   │ (loads template)
   │ (replaces placeholders)
   │ (saves document)
   ▼
5. Response
   │ (returns binary OR)
   │ (returns download link)
   ▼
6. Client receives document
```

### Template Discovery Flow

```
1. Client Request
   │
   ▼
2. API/MCP Endpoint
   │
   ▼
3. Document Service
   │ (scans template directory)
   │
   ├──▶ Word Generator
   │    (extracts fields)
   │
   ├──▶ Excel Generator
   │    (extracts fields)
   │
   └──▶ PowerPoint Generator
        (extracts fields)
   │
   ▼
4. Response
   │ (returns template list)
   │ (with field names)
   ▼
5. Client receives template info
```

## Design Patterns

### 1. Strategy Pattern
- **Usage:** Different generators for different document types
- **Benefit:** Easy to add new document formats

### 2. Template Method Pattern
- **Usage:** Base generator class with common operations
- **Benefit:** Consistent interface across generators

### 3. Factory Pattern
- **Usage:** Generator selection in DocumentService
- **Benefit:** Centralized creation logic

### 4. Dependency Injection
- **Usage:** Configuration via Settings class
- **Benefit:** Easy testing and configuration

## Scalability Considerations

### Horizontal Scaling
- Stateless design
- No session storage
- Shared file system or object storage
- Load balancer distribution

### Vertical Scaling
- Async I/O for concurrent requests
- Efficient memory usage
- Streaming for large files

### Storage Strategy
- Local filesystem for development
- Object storage (S3, GCS) for production
- CDN for download acceleration
- Automatic cleanup policies

## Security Architecture

### Input Validation
- Pydantic models for type checking
- Request size limits
- Filename sanitization

### File Operations
- Sandboxed template directory
- Generated files in separate directory
- No arbitrary file access

### API Security (Future)
- API key authentication
- Rate limiting
- HTTPS enforcement
- CORS configuration

## Extension Points

### Adding New Document Types
1. Create new generator class inheriting from `DocumentGenerator`
2. Implement `generate()` and `get_template_fields()` methods
3. Add to `DocumentService.generators` dict
4. Add file extension to `DocumentService.extensions` dict

### Adding Authentication
1. Create authentication middleware
2. Add to FastAPI app
3. Protect endpoints as needed

### Adding Database
1. Create models for templates, documents, users
2. Add database configuration
3. Modify DocumentService to use database
4. Add migration scripts

### Adding Caching
1. Add Redis configuration
2. Cache template metadata
3. Cache generated documents (with TTL)
4. Invalidate on template changes

## Testing Strategy

### Unit Tests
- Generator functions
- Model validation
- Service logic

### Integration Tests
- API endpoints
- MCP tools
- End-to-end generation

### Performance Tests
- Concurrent requests
- Large document generation
- Memory usage

## Monitoring & Observability

### Metrics to Track
- Document generation rate
- Error rate by document type
- Response times
- Storage usage
- Template access patterns

### Logging Strategy
- Request/response logging
- Error tracking
- Performance monitoring
- Audit trails

### Health Checks
- `/health` endpoint
- Template directory accessibility
- Storage capacity
- Service dependencies

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| API Framework | FastAPI | High performance, async, auto-docs |
| MCP Protocol | mcp library | Standard for AI agent integration |
| Word Processing | python-docx | Mature, well-documented |
| Excel Processing | openpyxl | Full XLSX support |
| PowerPoint Processing | python-pptx | Complete PPTX functionality |
| Validation | Pydantic | Type safety, data validation |
| Configuration | pydantic-settings | Environment-based config |
| Testing | pytest | Standard Python testing framework |

## Future Enhancements

### Planned Features
- PDF generation support
- Template versioning
- Batch document generation
- Webhook notifications
- Template preview API
- Custom styling per generation
- Variable fonts and images
- Conditional content blocks
- Data source integration (databases, APIs)
- Template marketplace

### Performance Improvements
- Document generation queue
- Worker pool for parallel processing
- Caching layer
- CDN integration
- Background job processing

### Security Enhancements
- OAuth 2.0 integration
- Role-based access control
- Encrypted document storage
- Audit logging
- API rate limiting per user

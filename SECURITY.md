# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please email the maintainers directly rather than opening a public issue.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

## Security Best Practices

### Dependency Management

This project uses the following approach for dependency security:

1. **Automated Scanning**: Dependencies are checked against the GitHub Advisory Database
2. **Version Pinning**: We use minimum version requirements (>=) to allow security updates
3. **Regular Updates**: Dependencies are reviewed and updated regularly

### Current Security Measures

#### Input Validation
- All API inputs are validated using Pydantic models
- Template names are sanitized to prevent path traversal
- Field values are validated before processing
- File extensions are restricted to known document types

#### File System Security
- Templates are isolated to a specific directory
- Generated documents are stored in a separate directory
- No arbitrary file system access is permitted
- Path traversal attempts are blocked

#### API Security
- Request size limits (configurable)
- Content-Type validation
- CORS can be configured for production
- Health check endpoint for monitoring

### Production Recommendations

For production deployments, we recommend:

1. **HTTPS Only**: Always use HTTPS in production
2. **Authentication**: Implement API key or OAuth 2.0 authentication
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Network Security**: Use firewalls and security groups
5. **Monitoring**: Implement logging and alerting
6. **Regular Updates**: Keep dependencies up to date

### Known Security Considerations

#### File Upload
Currently, templates must be pre-loaded on the server. Future versions may support template upload, which will require additional validation:
- File type verification
- Virus scanning
- Size limits
- Content validation

#### Authentication
The current version does not include authentication. For production use:
- Add API key authentication
- Implement user management
- Use JWT tokens for sessions
- Configure RBAC (Role-Based Access Control)

### Dependency Vulnerabilities

#### Resolved Vulnerabilities

**FastAPI < 0.109.1**
- Issue: Content-Type Header ReDoS vulnerability
- Resolution: Updated to fastapi>=0.109.1
- Impact: DoS attack via malicious Content-Type headers
- Status: ✅ Resolved

**python-multipart < 0.0.18**
- Issue: DoS via deformation multipart/form-data boundary
- Resolution: Updated to python-multipart>=0.0.18
- Impact: DoS attack via malicious multipart data
- Status: ✅ Resolved

**python-multipart <= 0.0.6**
- Issue: Content-Type Header ReDoS vulnerability
- Resolution: Updated to python-multipart>=0.0.18
- Impact: DoS attack via malicious Content-Type headers
- Status: ✅ Resolved

### Security Headers

For production deployments, configure your reverse proxy (nginx, Apache, etc.) to add security headers:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

### Docker Security

When using Docker:

1. **Non-root User**: Run containers as non-root user
2. **Read-only Filesystem**: Use read-only root filesystem where possible
3. **Resource Limits**: Set CPU and memory limits
4. **Network Isolation**: Use Docker networks for isolation
5. **Image Scanning**: Scan images for vulnerabilities

Example Docker run with security options:
```bash
docker run -d \
  --read-only \
  --tmpfs /tmp \
  --user 1000:1000 \
  --memory="512m" \
  --cpus="1.0" \
  -p 8000:8000 \
  document-generator
```

### MCP Server Security

The MCP server communicates via stdio and:
- Only accepts commands from the parent process
- Validates all tool inputs
- Sandboxes file operations
- Does not expose network services directly

### Environment Variables

Sensitive configuration should use environment variables:
- Never commit secrets to version control
- Use `.env` files locally (add to .gitignore)
- Use secret management services in production
- Rotate credentials regularly

### Audit Logging

For production, implement audit logging:
- Log all document generation requests
- Track API usage patterns
- Monitor for suspicious activity
- Retain logs according to compliance requirements

## Vulnerability Disclosure Timeline

We aim to:
1. Acknowledge receipt within 48 hours
2. Provide an initial assessment within 7 days
3. Release a fix within 30 days
4. Publicly disclose after fix is available

## Security Updates

Security updates will be announced via:
- GitHub Security Advisories
- Release notes
- CHANGELOG.md

## Compliance

This project does not currently implement specific compliance frameworks (SOC2, HIPAA, etc.). 

For compliance-required deployments:
- Implement audit logging
- Add user authentication and authorization
- Configure data retention policies
- Enable encryption at rest and in transit
- Implement backup and disaster recovery

## Security Checklist for Production

- [ ] HTTPS enabled with valid certificate
- [ ] Authentication implemented
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Security headers added
- [ ] Logging and monitoring enabled
- [ ] Regular security updates scheduled
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan documented
- [ ] Secrets management configured
- [ ] Network security configured (firewall, security groups)
- [ ] Regular security audits scheduled

## Contact

For security concerns, please contact the maintainers through GitHub issues (for non-sensitive matters) or via the repository's security policy.

## Acknowledgments

We use the following tools and databases for security:
- GitHub Advisory Database
- Dependabot (if enabled)
- Manual security reviews
- Community contributions

## Updates

This security policy is reviewed and updated regularly. Last updated: 2024.

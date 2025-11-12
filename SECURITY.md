# Security Documentation

## Overview

This document outlines the security architecture, vulnerabilities, and mitigation strategies for the 3D Print MVP platform. This platform exposes your local machine through multiple middleware components, making security **critical**.

## Security Threat Model

### Attack Surface

1. **Web APIs** - FastAPI (port 8000) and Medusa.js (port 9000) expose endpoints
2. **Database** - PostgreSQL (port 5432) contains sensitive user and order data
3. **Cache/Queue** - Redis (port 6379) handles job queues and sessions
4. **Physical Hardware** - Bambu Lab 3D printers (MQTT) controllable via API
5. **Cloud Storage** - Cloudflare R2 credentials enable file access
6. **Admin Interfaces** - Medusa Admin (port 7001), Flower (port 5555), PgAdmin (port 5050)

### Critical Vulnerabilities (Pre-Hardening)

| Vulnerability | Severity | Impact |
|--------------|----------|--------|
| **Permissive CORS (`*`)** | 🔴 CRITICAL | Any website can make authenticated requests, enabling CSRF attacks |
| **No API Authentication** | 🔴 CRITICAL | Anonymous users can access endpoints, create jobs, control printers |
| **Network Binding (`0.0.0.0`)** | 🔴 HIGH | All services accessible from any machine on network |
| **Plaintext Credentials** | 🔴 HIGH | `.env` file contains R2 keys, printer access codes, JWT secrets |
| **No Rate Limiting** | 🟡 MEDIUM | APIs vulnerable to brute force and DoS attacks |
| **No Input Validation** | 🟡 MEDIUM | File uploads lack size/format validation |
| **Default Passwords** | 🟡 MEDIUM | PostgreSQL, MinIO, PgAdmin use weak defaults |
| **No TLS/SSL** | 🟡 MEDIUM | All traffic sent in plaintext over HTTP |

## Security Hardening Implementation

### 1. CORS Configuration

**Before (INSECURE):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows ANY website to make requests
    allow_credentials=True,
)
```

**After (SECURE):**
```python
# Load from environment with strict defaults
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Only whitelisted origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Explicit methods only
    allow_headers=["Content-Type", "Authorization"],  # Explicit headers
    max_age=600,  # Cache preflight requests for 10 minutes
)
```

**Configuration:**
```bash
# .env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 2. JWT Authentication Middleware

All API endpoints now require valid JWT tokens issued by Medusa.js backend.

**Implementation:**
```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token from Medusa.js"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Protected endpoint example
@app.get("/jobs/{job_id}", dependencies=[Depends(verify_token)])
async def get_job(job_id: int):
    # Endpoint logic
```

**Public Endpoints (No Auth Required):**
- `GET /` - Health check
- `GET /health` - System status

**Protected Endpoints (Auth Required):**
- All `/jobs/*` endpoints
- All `/manufacturing/*` endpoints
- All `/quota/*` endpoints
- `GET /stats/dashboard` (admin only)

### 3. Rate Limiting

Implemented using Redis-backed rate limiting to prevent abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Endpoint-specific limits
@app.post("/jobs/create")
@limiter.limit("10/minute")  # Max 10 job creation requests per minute
async def create_job():
    pass

@app.post("/manufacturing/create")
@limiter.limit("5/minute")  # Max 5 manufacturing jobs per minute
async def create_manufacturing_job():
    pass

@app.get("/stats/dashboard")
@limiter.limit("30/minute")  # Admin dashboard
async def get_dashboard_stats():
    pass
```

### 4. Input Validation & File Upload Security

**File Upload Limits:**
```python
from fastapi import UploadFile, File, HTTPException
from typing import List

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB per image
MAX_FILES = 50  # Maximum 50 images per scan
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

async def validate_upload_files(files: List[UploadFile]):
    """Validate file uploads for security"""
    if len(files) > MAX_FILES:
        raise HTTPException(400, f"Maximum {MAX_FILES} files allowed")

    for file in files:
        # Check extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"File type {ext} not allowed")

        # Check MIME type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(400, f"MIME type {file.content_type} not allowed")

        # Check file size
        file.file.seek(0, 2)  # Seek to end
        size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        if size > MAX_FILE_SIZE:
            raise HTTPException(400, f"File {file.filename} exceeds {MAX_FILE_SIZE/1024/1024}MB limit")

    return True
```

### 5. Network Binding Security

**Development Mode (localhost only):**
```yaml
# docker-compose.yml
services:
  api:
    ports:
      - "127.0.0.1:8000:8000"  # Only accessible from localhost

  postgres:
    ports:
      - "127.0.0.1:5432:5432"  # Database not accessible from network

  redis:
    ports:
      - "127.0.0.1:6379:6379"  # Redis not accessible from network
```

**Production Mode (reverse proxy):**
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. Secrets Management

**Environment Variable Encryption:**
```bash
# Use git-crypt or sops for .env encryption
# Install git-crypt
sudo apt-get install git-crypt

# Initialize encryption
cd /home/user/3d-print-mvp
git-crypt init

# Create .gitattributes
echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes
echo ".env.production filter=git-crypt diff=git-crypt" >> .gitattributes

# Export key for team members
git-crypt export-key /secure/location/git-crypt-key
```

**Strong Secret Generation:**
```bash
# Generate strong JWT secret
openssl rand -hex 32

# Generate cookie secret
openssl rand -hex 32

# Generate database password
openssl rand -base64 32
```

### 7. Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "yourdomain.com"])
```

### 8. Bambu Lab Printer Security

**Network Isolation:**
```bash
# Printers should be on isolated VLAN
# Firewall rules (iptables example):

# Allow API server to access printers only
iptables -A OUTPUT -p tcp -d 192.168.1.100 -m owner --uid-owner api-user -j ACCEPT
iptables -A OUTPUT -p tcp -d 192.168.1.101 -m owner --uid-owner api-user -j ACCEPT

# Block all other access to printer network
iptables -A OUTPUT -p tcp -d 192.168.1.0/24 -j DROP
```

**Access Control:**
```python
# Require admin role for printer control
async def require_admin(token_payload: dict = Depends(verify_token)):
    if token_payload.get("role") != "admin":
        raise HTTPException(403, "Admin access required")

@app.post("/manufacturing/create", dependencies=[Depends(require_admin)])
async def create_manufacturing_job():
    # Only admins can create manufacturing jobs
```

**Printer Access Code Rotation:**
```python
# Rotate Bambu Lab access codes monthly
# Store in encrypted secrets manager, not .env
from cryptography.fernet import Fernet

def get_printer_access_code(printer_id: str) -> str:
    """Retrieve encrypted printer access code"""
    key = os.getenv("ENCRYPTION_KEY").encode()
    fernet = Fernet(key)
    encrypted_code = os.getenv(f"BAMBU_{printer_id}_ACCESS_CODE").encode()
    return fernet.decrypt(encrypted_code).decode()
```

### 9. Audit Logging

All sensitive operations are logged:

```python
from enum import Enum
from datetime import datetime

class AuditAction(str, Enum):
    JOB_CREATED = "job_created"
    JOB_CANCELLED = "job_cancelled"
    MANUFACTURING_STARTED = "manufacturing_started"
    PRINTER_CONTROLLED = "printer_controlled"
    FILE_UPLOADED = "file_uploaded"
    FILE_DOWNLOADED = "file_downloaded"
    ADMIN_ACCESS = "admin_access"

async def log_audit_event(
    user_id: str,
    action: AuditAction,
    details: dict,
    ip_address: str,
    user_agent: str
):
    """Log security-relevant events"""
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        timestamp=datetime.utcnow()
    )
    db.add(audit_log)
    await db.commit()

    # Also log to external SIEM if configured
    if SENTRY_DSN:
        sentry_sdk.capture_message(f"Audit: {action}", level="info", extra=details)
```

### 10. Database Security

**PostgreSQL Hardening:**
```sql
-- Create read-only user for analytics
CREATE USER analytics_readonly WITH PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE rd_platform TO analytics_readonly;
GRANT USAGE ON SCHEMA public TO analytics_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytics_readonly;

-- Create application user with limited privileges
CREATE USER api_user WITH PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE rd_platform TO api_user;
GRANT USAGE, CREATE ON SCHEMA public TO api_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO api_user;

-- Enable row-level security
ALTER TABLE processing_jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_jobs_isolation ON processing_jobs
    FOR ALL
    TO api_user
    USING (user_id = current_setting('app.current_user_id')::TEXT);
```

**Redis Security:**
```conf
# redis.conf
requirepass your_strong_redis_password_here
bind 127.0.0.1
protected-mode yes
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## Security Checklist

### Pre-Deployment

- [ ] Change all default passwords (PostgreSQL, Redis, MinIO, PgAdmin)
- [ ] Generate strong JWT_SECRET and COOKIE_SECRET (32+ characters)
- [ ] Rotate Bambu Lab printer access codes
- [ ] Configure ALLOWED_ORIGINS for production domain
- [ ] Enable git-crypt or sops for .env encryption
- [ ] Review and limit database user privileges
- [ ] Enable Redis password authentication
- [ ] Configure firewall rules for printer network isolation
- [ ] Set up TLS/SSL certificates (Let's Encrypt)
- [ ] Enable Sentry error tracking with proper DSN
- [ ] Configure backup strategy for PostgreSQL
- [ ] Set up monitoring and alerting (Prometheus/Grafana)

### Runtime Monitoring

- [ ] Monitor audit logs for suspicious activity
- [ ] Track rate limit violations
- [ ] Alert on failed authentication attempts (>5/minute)
- [ ] Monitor printer access patterns
- [ ] Track file upload sizes and frequencies
- [ ] Monitor database connection pool exhaustion
- [ ] Alert on API error rates >1%
- [ ] Track job queue depth (alert if >1000)

### Regular Maintenance

- [ ] Rotate JWT secrets every 90 days
- [ ] Rotate database passwords every 90 days
- [ ] Rotate Cloudflare R2 access keys every 90 days
- [ ] Update dependencies monthly (npm audit, pip-audit)
- [ ] Review audit logs weekly
- [ ] Test backup restoration monthly
- [ ] Review firewall rules monthly
- [ ] Conduct security assessment quarterly

## Incident Response

### Suspected Compromise

1. **Immediate Actions:**
   ```bash
   # Stop all services
   docker-compose down

   # Block all external access
   sudo iptables -A INPUT -j DROP

   # Preserve logs
   docker-compose logs > incident-$(date +%Y%m%d-%H%M%S).log
   ```

2. **Investigation:**
   - Review audit logs in database
   - Check Sentry error logs
   - Examine nginx access logs
   - Review system auth logs: `sudo grep -i "failed\|error" /var/log/auth.log`

3. **Recovery:**
   - Rotate all secrets (JWT, database, R2, printer codes)
   - Restore from known-good backup
   - Update firewall rules
   - Re-deploy with hardened configuration

4. **Post-Incident:**
   - Document timeline and root cause
   - Implement additional controls
   - Update incident response plan

## Compliance Considerations

### PCI DSS (If Processing Payments)

- ✅ Stripe handles PCI compliance (SAQ A)
- ✅ No credit card data stored locally
- ⚠️ Ensure TLS 1.2+ for all payment communications
- ⚠️ Regularly update Stripe SDK

### GDPR (If Serving EU Customers)

- ⚠️ Implement data retention policies
- ⚠️ Add user data export functionality
- ⚠️ Add user data deletion (right to be forgotten)
- ⚠️ Cookie consent banner on frontend
- ⚠️ Privacy policy and terms of service

### Data Retention

```python
# Implement automated data cleanup
from datetime import timedelta

async def cleanup_old_data():
    """Delete old data per retention policy"""
    retention_days = 90
    cutoff = datetime.utcnow() - timedelta(days=retention_days)

    # Delete old processing jobs
    await db.execute(
        delete(ProcessingJob).where(
            ProcessingJob.created_at < cutoff,
            ProcessingJob.status.in_(["completed", "failed", "cancelled"])
        )
    )

    # Delete old audit logs (keep 1 year)
    audit_cutoff = datetime.utcnow() - timedelta(days=365)
    await db.execute(
        delete(AuditLog).where(AuditLog.timestamp < audit_cutoff)
    )

    await db.commit()
```

## Security Testing

### Automated Scanning

```bash
# Dependency vulnerabilities
npm audit --production
pip-audit

# SAST (Static Application Security Testing)
bandit -r backend/processing-api/
eslint frontend/storefront/src --ext .ts,.tsx

# Container scanning
docker scan processing-api:latest
trivy image processing-api:latest

# Secrets detection
trufflehog --regex --entropy=True .
```

### Manual Testing

```bash
# Test CORS policy
curl -H "Origin: https://evil.com" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://localhost:8000/jobs/create

# Test authentication
curl -X POST http://localhost:8000/jobs/create \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
# Should return 401 Unauthorized

# Test rate limiting
for i in {1..20}; do
  curl http://localhost:8000/jobs/create
done
# Should see 429 Too Many Requests after limit

# Test input validation
curl -X POST http://localhost:8000/jobs/create \
     -F "file=@/etc/passwd"
# Should reject non-image files
```

## Contact

For security issues, contact:
- Email: security@yourdomain.com
- PGP Key: [Your PGP public key]

**DO NOT** disclose security vulnerabilities in public GitHub issues.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Medusa.js Security](https://docs.medusajs.com/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)
- [Redis Security](https://redis.io/topics/security)
- [Bambu Lab API Security](https://github.com/Doridian/OpenBambuAPI)

---

**Last Updated:** 2025-11-12
**Version:** 1.0.0
**Status:** ✅ Hardened

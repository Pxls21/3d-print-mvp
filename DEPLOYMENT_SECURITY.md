# Deployment Security Checklist

## Overview

This document provides a step-by-step security checklist for deploying the 3D Print MVP platform safely. Follow these steps **in order** before exposing your system to production traffic.

## Pre-Deployment Security Checklist

### 1. Secrets & Credentials (CRITICAL)

- [ ] **Generate strong JWT_SECRET**
  ```bash
  openssl rand -hex 32
  # Add to .env: JWT_SECRET=<generated_value>
  ```

- [ ] **Generate strong COOKIE_SECRET**
  ```bash
  openssl rand -hex 32
  # Add to .env: COOKIE_SECRET=<generated_value>
  ```

- [ ] **Change PostgreSQL password**
  ```bash
  openssl rand -base64 32
  # Add to .env: POSTGRES_PASSWORD=<generated_value>
  # Update DATABASE_URL with new password
  ```

- [ ] **Change Redis password**
  ```bash
  openssl rand -hex 24
  # Add to .env: REDIS_PASSWORD=<generated_value>
  # Update REDIS_URL with new password
  ```

- [ ] **Update all development tool passwords**
  - [ ] PGADMIN_PASSWORD
  - [ ] MINIO_ROOT_PASSWORD
  - [ ] FLOWER_PASSWORD

- [ ] **Verify .env is in .gitignore** (should already be there)
  ```bash
  grep -q "^\.env$" .gitignore && echo "✓ .env is ignored" || echo "✗ Add .env to .gitignore"
  ```

### 2. CORS & Network Security

- [ ] **Configure ALLOWED_ORIGINS for your domain**
  ```bash
  # In .env:
  ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
  ADMIN_CORS=https://admin.yourdomain.com
  ```

- [ ] **Never use wildcard (*) in production**
  ```bash
  # BAD (development only):
  ALLOWED_ORIGINS=*

  # GOOD (production):
  ALLOWED_ORIGINS=https://yourdomain.com
  ```

- [ ] **Verify localhost bindings in docker-compose.yml**
  ```bash
  # All services should bind to 127.0.0.1 for local-only access:
  # - "127.0.0.1:8000:8000"  # Processing API
  # - "127.0.0.1:9000:9000"  # Medusa backend
  # - "127.0.0.1:5432:5432"  # PostgreSQL
  # - "127.0.0.1:6379:6379"  # Redis
  # - "127.0.0.1:3000:3000"  # Frontend (use reverse proxy)
  ```

### 3. TLS/SSL Configuration

- [ ] **Obtain SSL certificate**
  - Option 1: Let's Encrypt (free, recommended)
    ```bash
    sudo apt-get install certbot python3-certbot-nginx
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```
  - Option 2: Commercial certificate provider

- [ ] **Configure reverse proxy (nginx recommended)**
  ```bash
  # Install nginx
  sudo apt-get install nginx

  # Copy template configuration
  sudo cp /path/to/nginx.conf /etc/nginx/sites-available/3d-print-mvp
  sudo ln -s /etc/nginx/sites-available/3d-print-mvp /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl reload nginx
  ```

- [ ] **Enable HSTS after SSL is working**
  ```bash
  # In .env:
  ENABLE_HSTS=true
  HSTS_MAX_AGE=31536000
  ```

- [ ] **Test SSL configuration**
  ```bash
  # Use SSL Labs test
  # https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
  ```

### 4. Database Security

- [ ] **Create dedicated database user (not postgres)**
  ```sql
  CREATE USER api_user WITH PASSWORD 'strong_password_here';
  GRANT CONNECT ON DATABASE rd_platform TO api_user;
  GRANT USAGE, CREATE ON SCHEMA public TO api_user;
  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO api_user;
  ```

- [ ] **Enable row-level security for multi-tenancy**
  ```sql
  ALTER TABLE processing_jobs ENABLE ROW LEVEL SECURITY;
  CREATE POLICY user_jobs_isolation ON processing_jobs
      FOR ALL TO api_user
      USING (user_id = current_setting('app.current_user_id')::TEXT);
  ```

- [ ] **Set up automated backups**
  ```bash
  # Daily PostgreSQL backups
  sudo crontab -e
  # Add: 0 2 * * * pg_dump rd_platform > /backups/rd_platform_$(date +\%Y\%m\%d).sql
  ```

- [ ] **Configure backup retention** (30 days recommended)

### 5. Bambu Lab Printer Security

- [ ] **Isolate printers on dedicated VLAN**
  - Recommended subnet: 192.168.100.0/24
  - Printer 1: 192.168.100.10
  - Printer 2: 192.168.100.11

- [ ] **Configure firewall rules** (iptables example)
  ```bash
  # Allow API server to access printers only
  sudo iptables -A OUTPUT -p tcp -d 192.168.100.10 -m owner --uid-owner api-user -j ACCEPT
  sudo iptables -A OUTPUT -p tcp -d 192.168.100.11 -m owner --uid-owner api-user -j ACCEPT

  # Block all other access to printer network
  sudo iptables -A OUTPUT -p tcp -d 192.168.100.0/24 -j DROP

  # Save rules
  sudo iptables-save > /etc/iptables/rules.v4
  ```

- [ ] **Rotate printer access codes**
  - Initial setup: Obtain from printer settings
  - Schedule: Monthly rotation recommended
  - Update .env after each rotation

- [ ] **Never expose printer IPs to internet**

### 6. Rate Limiting & DDoS Protection

- [ ] **Configure rate limiting**
  ```bash
  # In .env:
  RATE_LIMIT_ENABLED=true
  RATE_LIMIT_REQUESTS=100
  RATE_LIMIT_WINDOW=60
  ```

- [ ] **Set up Cloudflare (recommended)**
  - Free tier provides DDoS protection
  - Add your domain to Cloudflare
  - Enable "Under Attack" mode if needed

- [ ] **Configure nginx rate limiting** (additional layer)
  ```nginx
  limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

  location /api/ {
      limit_req zone=api burst=20 nodelay;
  }
  ```

### 7. Monitoring & Alerting

- [ ] **Set up Sentry error tracking**
  ```bash
  # Create Sentry account at sentry.io
  # Add to .env:
  SENTRY_DSN=https://your_sentry_dsn@sentry.io/project_id
  ```

- [ ] **Configure log aggregation** (optional but recommended)
  - Option 1: ELK Stack (Elasticsearch, Logstash, Kibana)
  - Option 2: Grafana + Loki
  - Option 3: Cloud service (Datadog, New Relic)

- [ ] **Set up uptime monitoring**
  - Option 1: UptimeRobot (free)
  - Option 2: Pingdom
  - Option 3: StatusCake

- [ ] **Configure alerts**
  - [ ] API error rate > 1%
  - [ ] Database connection failures
  - [ ] Redis connection failures
  - [ ] Disk usage > 80%
  - [ ] Failed authentication attempts > 5/min

### 8. File Upload Security

- [ ] **Verify file upload limits**
  ```bash
  # In .env:
  MAX_FILE_SIZE=10485760        # 10MB per file
  MAX_FILES_PER_REQUEST=50       # Max 50 files per upload
  ```

- [ ] **Configure nginx client_max_body_size**
  ```nginx
  http {
      client_max_body_size 500M;  # Match total upload limit
  }
  ```

- [ ] **Enable virus scanning** (optional but recommended)
  ```bash
  sudo apt-get install clamav clamav-daemon
  sudo systemctl enable clamav-daemon
  ```

### 9. API Authentication Testing

- [ ] **Test JWT authentication**
  ```bash
  # Should fail without token
  curl -X POST http://localhost:8000/jobs/create \
       -H "Content-Type: application/json" \
       -d '{"user_id": "test"}'
  # Expected: 401 Unauthorized

  # Should succeed with valid token
  curl -X POST http://localhost:8000/jobs/create \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer YOUR_VALID_JWT" \
       -d '{"user_id": "test", ...}'
  # Expected: 200 OK
  ```

- [ ] **Test CORS policy**
  ```bash
  # From unauthorized origin (should fail)
  curl -H "Origin: https://evil.com" \
       -H "Access-Control-Request-Method: POST" \
       -X OPTIONS http://localhost:8000/jobs/create
  # Expected: No CORS headers in response

  # From authorized origin (should succeed)
  curl -H "Origin: https://yourdomain.com" \
       -H "Access-Control-Request-Method: POST" \
       -X OPTIONS http://localhost:8000/jobs/create
  # Expected: CORS headers present
  ```

- [ ] **Test rate limiting**
  ```bash
  # Exceed rate limit
  for i in {1..110}; do
      curl http://localhost:8000/jobs/create
  done
  # Expected: 429 Too Many Requests after limit
  ```

### 10. Security Scanning

- [ ] **Run dependency vulnerability scan**
  ```bash
  # Python dependencies
  cd backend/processing-api
  pip install pip-audit
  pip-audit

  # Node.js dependencies
  cd backend/medusa
  npm audit --production

  # Fix vulnerabilities
  pip-audit --fix  # Python
  npm audit fix    # Node.js
  ```

- [ ] **Run container security scan**
  ```bash
  docker scan rd-platform-processing-api:latest
  docker scan rd-platform-medusa:latest
  ```

- [ ] **Run SAST (Static Application Security Testing)**
  ```bash
  # Python
  pip install bandit
  bandit -r backend/processing-api/

  # JavaScript/TypeScript
  npm install -g eslint
  eslint backend/medusa/src --ext .ts,.js
  ```

- [ ] **Check for exposed secrets**
  ```bash
  # Install trufflehog
  pip install trufflehog

  # Scan repository
  trufflehog --regex --entropy=True .
  ```

## Post-Deployment Monitoring

### Daily Tasks

- [ ] Review error logs in Sentry
- [ ] Check API error rates
- [ ] Monitor disk usage
- [ ] Verify backup completion

### Weekly Tasks

- [ ] Review audit logs for suspicious activity
- [ ] Check rate limit violations
- [ ] Review failed authentication attempts
- [ ] Update dependencies (security patches)

### Monthly Tasks

- [ ] Rotate sensitive credentials
- [ ] Review and update firewall rules
- [ ] Test backup restoration
- [ ] Conduct security assessment
- [ ] Review access logs

### Quarterly Tasks

- [ ] Rotate all secrets (JWT, database, etc.)
- [ ] Penetration testing
- [ ] Security training for team
- [ ] Disaster recovery drill

## Incident Response Plan

### If Breach Suspected

1. **Immediate Actions**
   ```bash
   # Stop all services
   docker-compose down

   # Block all external access
   sudo iptables -A INPUT -j DROP

   # Preserve logs
   docker-compose logs > incident-$(date +%Y%m%d-%H%M%S).log
   cp /var/log/nginx/access.log /incident/nginx-access-$(date +%Y%m%d).log
   ```

2. **Investigation**
   - Review audit logs in database
   - Check Sentry error logs
   - Examine nginx access logs
   - Review system auth logs: `sudo grep -i "failed\|error" /var/log/auth.log`

3. **Recovery**
   - Rotate all secrets (JWT, database, R2, printer codes)
   - Restore from known-good backup
   - Update firewall rules
   - Re-deploy with hardened configuration

4. **Post-Incident**
   - Document timeline and root cause
   - Implement additional controls
   - Update incident response plan
   - Notify affected users (if required)

## Production Deployment Checklist Summary

Before going live:

- [x] ✓ Security middleware implemented (CORS, rate limiting, headers)
- [x] ✓ JWT authentication on all protected endpoints
- [x] ✓ Audit logging for sensitive operations
- [x] ✓ Input validation and file upload limits
- [x] ✓ Network bindings secured (localhost only)
- [x] ✓ Docker services with secure defaults
- [ ] Generate strong secrets (JWT, database, Redis)
- [ ] Configure ALLOWED_ORIGINS for your domain
- [ ] Set up TLS/SSL certificates
- [ ] Configure reverse proxy (nginx)
- [ ] Set up database backups
- [ ] Configure firewall for printer isolation
- [ ] Set up monitoring (Sentry, uptime)
- [ ] Test all security implementations
- [ ] Run vulnerability scans
- [ ] Review and test incident response plan

## Support & Resources

- **Security Documentation**: See `SECURITY.md` for detailed information
- **Environment Configuration**: See `.env.example` for all settings
- **Docker Configuration**: See `docker/docker-compose.yml` for service setup

## Compliance Considerations

### PCI DSS (If Processing Payments)
- ✅ Stripe handles PCI compliance (SAQ A)
- ✅ No credit card data stored locally
- ⚠️ Ensure TLS 1.2+ for all payment communications

### GDPR (If Serving EU Customers)
- ⚠️ Implement data retention policies
- ⚠️ Add user data export functionality
- ⚠️ Add user data deletion (right to be forgotten)
- ⚠️ Cookie consent banner on frontend
- ⚠️ Privacy policy and terms of service

## Emergency Contacts

- Security Team: security@yourdomain.com
- On-Call Engineer: oncall@yourdomain.com
- Hosting Provider Support: [your provider]
- Cloudflare Support: [if applicable]

---

**Last Updated**: 2025-11-12
**Version**: 1.0.0
**Review**: Quarterly

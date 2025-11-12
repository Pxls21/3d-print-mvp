# 🚀 Quick Start Guide - Local Development

Get your development environment running in **5 minutes**.

## Prerequisites

- Docker & Docker Compose installed
- OpenSSL (for generating secrets)
- Git

## Step 1: Clone & Navigate

```bash
cd /home/user/3d-print-mvp
```

## Step 2: Create Environment File (2 minutes)

```bash
# Copy the template
cp .env.example .env
```

## Step 3: Generate Required Secrets (2 minutes)

```bash
# Generate JWT secret
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env

# Generate Cookie secret
echo "COOKIE_SECRET=$(openssl rand -hex 32)" >> .env
```

**That's the minimum!** The rest has secure defaults for local development.

## Step 4: Start Development Environment (1 minute)

```bash
# Start core services only
docker-compose -f docker/docker-compose.yml up

# OR start with dev tools (MinIO, PgAdmin, Flower)
docker-compose -f docker/docker-compose.yml --profile dev-tools up
```

## Step 5: Access Your Services

Once running, access at:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Customer-facing storefront |
| **API (FastAPI)** | http://localhost:8000 | Processing orchestration |
| **Medusa API** | http://localhost:9000 | E-commerce backend |
| **Admin Panel** | http://localhost:7001 | Medusa admin dashboard |
| **API Docs** | http://localhost:8000/docs | FastAPI interactive docs |

### Dev Tools (--profile dev-tools only)

| Service | URL | Credentials |
|---------|-----|-------------|
| **PgAdmin** | http://localhost:5050 | admin@localhost.local / ChangeMePgAdmin123! |
| **Flower** | http://localhost:5555 | admin / ChangeMeFlower123! |
| **MinIO Console** | http://localhost:9001 | minioadmin / ChangeMeMinio123! |

## Step 6: Initialize Database (First Run)

```bash
# Medusa migrations (run once)
docker exec -it rd-platform-medusa npm run migration:run

# Processing API will auto-create tables via SQLAlchemy
```

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are already in use
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :9000

# Stop conflicting services or change ports in docker-compose.yml
```

### Database Connection Issues

```bash
# Check PostgreSQL logs
docker logs rd-platform-postgres

# Verify password in .env matches docker-compose
grep POSTGRES_PASSWORD .env
```

### Redis Connection Issues

```bash
# Check Redis logs
docker logs rd-platform-redis

# Verify Redis password
grep REDIS_PASSWORD .env
```

### Permission Errors

```bash
# Fix file permissions
chmod +x scripts/*

# Reset Docker volumes (WARNING: deletes data)
docker-compose -f docker/docker-compose.yml down -v
```

## Development Workflow

### Making Changes

```bash
# Code changes are hot-reloaded automatically
# - FastAPI: uvicorn --reload
# - Next.js: next dev
# - Medusa: npm run dev

# View logs
docker-compose -f docker/docker-compose.yml logs -f [service-name]
```

### Running Tests

```bash
# FastAPI tests
docker exec -it rd-platform-processing-api pytest

# Frontend tests
docker exec -it rd-platform-storefront npm test
```

### Accessing Database

```bash
# Via PgAdmin (dev-tools): http://localhost:5050

# Via psql
docker exec -it rd-platform-postgres psql -U postgres -d rd_platform

# Common queries
\dt           # List tables
\d+ users     # Describe users table
SELECT * FROM processing_jobs LIMIT 10;
```

### Accessing Redis

```bash
# Connect to Redis CLI
docker exec -it rd-platform-redis redis-cli -a ChangeMeRedis123!

# Common commands
KEYS *               # List all keys
GET key_name         # Get value
FLUSHALL             # Clear all data (careful!)
```

## Optional Configuration

### Configure Cloudflare R2 (for file uploads)

```bash
# Add to .env:
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=rd-platform
```

### Configure Stripe (for payments)

```bash
# Add to .env:
STRIPE_SECRET_KEY=sk_test_your_test_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_test_key
NEXT_PUBLIC_STRIPE_KEY=pk_test_your_test_key
```

### Configure Sentry (for error tracking)

```bash
# Add to .env:
SENTRY_DSN=https://your_dsn@sentry.io/project_id
```

### Configure Bambu Lab Printers (for FDM manufacturing)

```bash
# Add to .env:
BAMBU_1_IP=192.168.1.100
BAMBU_1_ACCESS_CODE=your_8_digit_code
BAMBU_1_SERIAL=your_printer_serial
```

## Stopping Services

```bash
# Stop all services
docker-compose -f docker/docker-compose.yml down

# Stop and remove volumes (deletes all data!)
docker-compose -f docker/docker-compose.yml down -v
```

## Next Steps

1. **Review Security**: Read `SECURITY.md` for production security considerations
2. **Deployment**: See `DEPLOYMENT_SECURITY.md` before deploying
3. **Architecture**: Check `PRODUCTION_STACK.md` for technology decisions
4. **API Documentation**: Visit http://localhost:8000/docs for interactive API docs

## Common Issues & Solutions

### "Port already in use"
Change port binding in `docker/docker-compose.yml` from `127.0.0.1:PORT:PORT` to `127.0.0.1:NEW_PORT:PORT`

### "Cannot connect to database"
1. Check `.env` file has correct `POSTGRES_PASSWORD`
2. Verify docker-compose.yml uses same password
3. Check logs: `docker logs rd-platform-postgres`

### "JWT authentication fails"
1. Verify `JWT_SECRET` is set in `.env`
2. Restart services after changing `.env`
3. Check both Medusa and Processing API use same `JWT_SECRET`

### "Files won't upload"
1. Start with `--profile dev-tools` to enable MinIO
2. OR configure Cloudflare R2 credentials in `.env`
3. Check file upload limits in `.env` (MAX_FILE_SIZE, MAX_FILES_PER_REQUEST)

### "Rate limiting blocks requests"
Temporarily disable in `.env`:
```bash
RATE_LIMIT_ENABLED=false
```

## Getting Help

- **Security Issues**: See `SECURITY.md`
- **Deployment**: See `DEPLOYMENT_SECURITY.md`
- **Architecture**: See `PRODUCTION_STACK.md`
- **Main README**: See `README.md`

---

**Development ready!** Start coding and all changes hot-reload automatically. 🎉

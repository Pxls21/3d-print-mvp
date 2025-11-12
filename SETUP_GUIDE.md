# R&D Platform - Setup Guide

Complete guide to set up and run the R&D Manufacturing Platform locally.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Configuration](#configuration)
- [Running the Platform](#running-the-platform)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

```bash
# System requirements
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Git
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

# Optional (for local development)
- NVIDIA GPU with CUDA support (for processing pipeline)
- OctoPrint-enabled 3D printers (for FDM integration)
```

### Check Installations

```bash
python --version  # Should be 3.10+
node --version    # Should be 18+
docker --version
docker-compose --version
git --version
```

---

## Project Structure

```
3d-print-mvp/
├── backend/
│   ├── medusa/                 # Medusa.js e-commerce platform
│   ├── processing-api/         # FastAPI processing orchestration
│   │   ├── main.py            # Main API
│   │   ├── models.py          # Database models
│   │   ├── database.py        # DB connection
│   │   ├── requirements.txt   # Python deps
│   │   └── Dockerfile
│   └── manufacturing/         # Manufacturing services
│       ├── octoprint_service.py    # FDM integration
│       └── workflow_manager.py     # Workflow management
├── frontend/
│   └── storefront/            # Next.js user interface
├── services/
│   ├── file-upload/           # Cloudflare R2 integration
│   │   └── r2_service.py
│   └── job-queue/             # Redis queue management
├── docker/
│   └── docker-compose.yml     # Local dev environment
├── config/                    # Configuration files
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
├── .env.example              # Environment template
└── README.md
```

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Pxls21/3d-print-mvp.git
cd 3d-print-mvp
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

### 3. Start Services with Docker

```bash
cd docker
docker-compose up -d
```

### 4. Access Services

```
✅ Processing API:     http://localhost:8000/docs
✅ Medusa Admin:       http://localhost:7001
✅ Medusa API:         http://localhost:9000
✅ Storefront:         http://localhost:3000
✅ Flower (Celery):    http://localhost:5555
✅ PgAdmin:            http://localhost:5050  (optional)
```

---

## Detailed Setup

### Option 1: Docker (Recommended for Development)

```bash
# Start all services
cd docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Option 2: Manual Setup (Advanced)

#### 1. PostgreSQL Setup

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib  # Ubuntu/Debian
brew install postgresql                         # macOS

# Start PostgreSQL
sudo systemctl start postgresql

# Create database
createdb rd_platform

# Or use Docker
docker run -d \
  --name rd-platform-postgres \
  -e POSTGRES_DB=rd_platform \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15-alpine
```

#### 2. Redis Setup

```bash
# Install Redis
sudo apt install redis-server  # Ubuntu/Debian
brew install redis             # macOS

# Start Redis
sudo systemctl start redis

# Or use Docker
docker run -d \
  --name rd-platform-redis \
  -p 6379:6379 \
  redis:7-alpine
```

#### 3. Backend Setup (Processing API)

```bash
cd backend/processing-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Run API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. Medusa.js Setup

```bash
cd backend/medusa

# Install dependencies
npm install
# or
pnpm install

# Run migrations
npx medusa migrations run

# Seed database (optional)
npm run seed

# Start Medusa
npm run dev
```

#### 5. Frontend Setup (Storefront)

```bash
cd frontend/storefront

# Install dependencies
npm install
# or
pnpm install

# Run development server
npm run dev
```

---

## Configuration

### Environment Variables

Edit `.env` file with your configuration:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rd_platform

# Redis
REDIS_URL=redis://localhost:6379

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=rd-platform

# Stripe
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx

# OctoPrint (FDM Printers)
OCTOPRINT_1_URL=http://192.168.1.100
OCTOPRINT_1_API_KEY=your_api_key
OCTOPRINT_1_NAME=Prusa i3 MK3S
```

### Cloudflare R2 Setup

1. Sign up for Cloudflare (free tier available)
2. Go to R2 Object Storage
3. Create a bucket named `rd-platform`
4. Generate API tokens:
   - Account ID
   - Access Key ID
   - Secret Access Key
5. Add to `.env`

### Stripe Setup

1. Sign up for Stripe (test mode)
2. Get API keys from Dashboard
3. Add to `.env`

### OctoPrint Setup (Optional - for FDM)

1. Install OctoPrint on your 3D printer
2. Get API key from Settings → API
3. Add printer details to `.env`

---

## Running the Platform

### Development Mode

```bash
# Start all services
docker-compose up -d

# Or start individually:

# Processing API
cd backend/processing-api
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Medusa
cd backend/medusa
npm run dev

# Storefront
cd frontend/storefront
npm run dev

# Celery Worker
cd backend/processing-api
celery -A celery_worker worker --loglevel=info
```

### Production Mode

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## Development Workflow

### Database Migrations

```bash
# Create migration
cd backend/processing-api
alembic revision --autogenerate -m "Description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Adding New API Endpoints

1. Edit `backend/processing-api/main.py`
2. Add route with type hints
3. Test at http://localhost:8000/docs

### Adding Manufacturing Methods

1. Edit `backend/manufacturing/workflow_manager.py`
2. Define workflow stages
3. Implement handler class
4. Update API routes

### Testing

```bash
# Run tests
cd backend/processing-api
pytest

# With coverage
pytest --cov=. --cov-report=html
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### Database Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U postgres -d rd_platform
```

#### Docker Issues

```bash
# Remove all containers
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache

# View logs
docker-compose logs -f <service_name>
```

#### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Restart Redis
sudo systemctl restart redis
```

### Debug Mode

```bash
# Enable SQL logging
export SQL_ECHO=true

# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Useful Commands

```bash
# View all running containers
docker ps

# Exec into container
docker exec -it rd-platform-processing-api bash

# View database
docker exec -it rd-platform-postgres psql -U postgres -d rd_platform

# View Redis
docker exec -it rd-platform-redis redis-cli
```

---

## Next Steps

1. **Configure GPU Processing Server** (see GPU_SETUP.md)
   - Install COLMAP
   - Install Point2CAD
   - Set up processing pipeline

2. **Set up Manufacturing Integration**
   - Configure OctoPrint for FDM
   - Set up SLS printer integration
   - Configure CFC/CNC workflows

3. **Deploy to Production** (see DEPLOYMENT.md)
   - Set up hosting (Railway, VPS)
   - Configure domain and SSL
   - Set up monitoring (Sentry)

4. **Customize Platform**
   - Add your branding
   - Configure pricing tiers
   - Customize email templates

---

## Support

- Documentation: `/docs` directory
- Issues: [GitHub Issues](https://github.com/Pxls21/3d-print-mvp/issues)
- Architecture: See `PRODUCTION_STACK.md`

---

## Development Team

- **Processing Pipeline**: GPU-intensive (COLMAP + Point2CAD) - Handle with desktop Claude Code
- **Platform Backend**: FastAPI, Medusa.js, PostgreSQL, Redis - Built with web Claude Code
- **Manufacturing**: OctoPrint, workflow management - Built with web Claude Code
- **Frontend**: Next.js storefront - Built with web Claude Code

---

**Happy Building! 🚀**

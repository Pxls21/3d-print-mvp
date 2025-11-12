# 🚀 Quick Start Guide - R&D Manufacturing Platform

## Overview

This guide covers setting up the complete scan-to-manufacturing platform with COLMAP + Point2CAD processing and FDM/SLS/CFC/CNC integration.

**What you're building**: An R&D platform where users scan prototypes (20-50 photos) and get manufactured parts via FDM, SLS, CFC, or CNC.

---

## Step 1: Upload to Repository

### 1.1 Create GitHub Repository

```bash
# On your local machine
cd ~/projects
mkdir 3d-print-mvp
cd 3d-print-mvp

# Initialize git
git init
git branch -M main

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.env.production

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
data/
outputs/
test_data/
*.glb
*.stl
*.ply
models/

# Logs
logs/
*.log

# Dependencies
node_modules/
package-lock.json

# Docker
.dockerignore
EOF

# Create README
cat > README.md << 'EOF'
# 3D Print MVP - Photos to STL Service

Production-ready AI service to convert photos into 3D printable files.

## Setup

1. See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for complete project details
2. See [QUICK_START.md](QUICK_START.md) for setup instructions
3. See [tasks/](tasks/) for development tasks
4. See [.claude/skills/](.claude/skills/) for AI-assisted development

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Security](docs/SECURITY.md)
- [Deployment](docs/DEPLOYMENT.md)
- [API Reference](docs/API.md)

## License

MIT - See LICENSE file
EOF

# Create GitHub repo and push
gh repo create 3d-print-mvp --private --source=. --remote=origin
git add .
git commit -m "Initial project structure"
git push -u origin main
```

### 1.2 Copy Documentation Files

Copy all the files I created into your repository:

```
3d-print-mvp/
├── README.md                      ← Main readme
├── PROJECT_OVERVIEW.md            ← Business overview
├── QUICK_START.md                 ← This file
├── TROUBLESHOOTING.md             ← Common issues
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── SECURITY.md
│   └── API.md
├── tasks/
│   ├── TASKS.md                   ← Complete task list
│   ├── PHASE_1.md
│   ├── PHASE_2.md
│   ├── PHASE_3.md
│   ├── PHASE_4.md
│   └── PHASE_5.md
├── .claude/
│   └── skills/
│       ├── README.md
│       ├── trellis-expert.md
│       ├── medusa-ecommerce.md
│       ├── security-expert.md
│       └── testing-expert.md
└── scripts/
    ├── setup.sh
    ├── deploy.sh
    └── test.sh
```

---

## Step 2: Claude Code Web Setup

### 2.1 Access Claude Code

1. Go to https://claude.ai/code
2. Sign in with your account
3. Create new project: "3D Print MVP"

### 2.2 Load Repository

In Claude Code chat:

```
I need you to help me set up a production-ready 3D printing service project. 

The repository is at: https://github.com/YOUR_USERNAME/3d-print-mvp

Please:
1. Review the PROJECT_OVERVIEW.md to understand the project
2. Review tasks/TASKS.md for implementation tasks
3. Load the Claude skills from .claude/skills/
4. Help me create the initial project structure
```

### 2.3 Create Project Structure

Ask Claude Code to create:

```
Please create the following directory structure:

backend/
├── core/
│   ├── __init__.py
│   ├── trellis_pipeline.py
│   ├── freecad_processor.py
│   └── config.py
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   └── middleware/
├── models/
│   ├── __init__.py
│   └── database.py
├── services/
│   ├── __init__.py
│   ├── processing.py
│   ├── storage.py
│   └── security.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── tests/
    ├── test_trellis.py
    ├── test_freecad.py
    └── test_api.py

medusa-backend/
├── src/
│   ├── modules/
│   │   └── 3d-processing/
│   ├── api/
│   └── subscribers/
└── medusa-config.js

frontend/
├── src/
│   ├── components/
│   │   ├── ImageUploader.tsx
│   │   ├── JobStatus.tsx
│   │   └── AdminDashboard.tsx
│   ├── pages/
│   ├── lib/
│   └── styles/
└── package.json

docker/
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── docker-compose.prod.yml

scripts/
├── setup.sh
├── deploy.sh
└── test.sh
```

### 2.4 Initialize Configuration Files

Ask Claude Code to create:

```
Create the following configuration files:

1. backend/requirements.txt with:
   - TRELLIS dependencies
   - FastAPI
   - SQLAlchemy
   - Security libraries

2. frontend/package.json with:
   - Next.js 14
   - React 18
   - Medusa storefront dependencies

3. .env.example with all required environment variables

4. docker-compose.yml for local development

5. README.md with setup instructions
```

---

## Step 3: Local Development on Fedora

### 3.1 Clone Repository

```bash
# On your Fedora system
cd ~/projects
git clone https://github.com/YOUR_USERNAME/3d-print-mvp.git
cd 3d-print-mvp
```

### 3.2 Install System Dependencies

```bash
# Update system
sudo dnf update -y

# Install Python 3.10
sudo dnf install python3.10 python3.10-devel -y

# Install Node.js 18
sudo dnf install nodejs -y
# Or use nvm:
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
# nvm install 18

# Install Docker
sudo dnf install docker docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install NVIDIA drivers (if not already)
sudo dnf install nvidia-driver nvidia-settings -y

# Install CUDA 11.8
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora37/x86_64/cuda-fedora37.repo
sudo dnf install cuda-11-8 -y

# Install FreeCAD
sudo dnf install freecad freecad-python3 -y
```

### 3.3 Setup Python Environment

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install Python dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Install TRELLIS
cd ~/projects
git clone --recurse-submodules https://github.com/microsoft/TRELLIS.git
cd TRELLIS
pip install -e .
```

### 3.4 Setup Environment Variables

```bash
cd ~/projects/3d-print-mvp

# Copy example env
cp .env.example .env

# Edit with your values
nano .env

# Required variables:
# DATABASE_URL=postgresql://user:pass@localhost:5432/print3d
# REDIS_URL=redis://localhost:6379
# RUNPOD_API_KEY=your_key_here
# STRIPE_SECRET_KEY=your_key_here
```

### 3.5 Test TRELLIS Locally

```bash
# Activate environment
source venv/bin/activate

# Run test script
cd backend
python tests/test_trellis.py

# Expected output:
# ✅ TRELLIS loaded successfully
# ✅ GPU detected: NVIDIA GeForce RTX 3090 (24GB)
# ✅ Test image processed in 18.3 seconds
# ✅ Output saved to: outputs/test_output.glb
```

---

## Step 4: Development Workflow

### 4.1 Daily Workflow

```bash
# Start work
cd ~/projects/3d-print-mvp
source venv/bin/activate

# Pull latest changes
git pull origin main

# Work on current task (see tasks/TASKS.md)
# Example: Working on TASK_002
cd backend/core
code trellis_pipeline.py

# Run tests
pytest tests/

# Commit changes
git add .
git commit -m "feat: Implement TRELLIS single-image processing (TASK_002)"
git push origin main
```

### 4.2 Using Claude Code During Development

**When stuck**, ask Claude Code:

```
I'm working on TASK_002 (TRELLIS Integration).

Using the TRELLIS expert skill, help me:
1. Implement multi-image processing
2. Optimize VRAM usage
3. Handle errors gracefully

Current code:
[paste your code]

Error message:
[paste error if any]
```

### 4.3 Using Archon MCP

```bash
# Index project
archon index-dir ~/projects/3d-print-mvp

# Query documentation
archon query "TRELLIS multi-image API example"

# Track tasks
archon create-task "TASK_002" "TRELLIS Integration"
archon update-task "TASK_002" --status "in-progress"
archon complete-task "TASK_002"
```

---

## Step 5: Testing

### 5.1 Unit Tests

```bash
# Run all tests
pytest backend/tests/

# Run specific test
pytest backend/tests/test_trellis.py -v

# With coverage
pytest --cov=backend tests/
```

### 5.2 Integration Tests

```bash
# Start services
docker-compose up -d

# Run integration tests
pytest backend/tests/integration/

# Stop services
docker-compose down
```

### 5.3 Manual Testing

```bash
# Test TRELLIS pipeline
python backend/core/trellis_pipeline.py --image test_data/sample.jpg

# Test FreeCAD validation
python backend/core/freecad_processor.py --input outputs/test.glb

# Test full pipeline
python scripts/test_pipeline.py
```

---

## Step 6: Deployment Preparation

### 6.1 Build Docker Images

```bash
# Build backend
docker build -f docker/Dockerfile.backend -t 3d-print-backend:v1 .

# Build frontend
docker build -f docker/Dockerfile.frontend -t 3d-print-frontend:v1 .

# Test locally
docker-compose -f docker-compose.prod.yml up
```

### 6.2 Push to Registry

```bash
# Login to registry
docker login

# Tag images
docker tag 3d-print-backend:v1 yourusername/3d-print-backend:v1
docker tag 3d-print-frontend:v1 yourusername/3d-print-frontend:v1

# Push
docker push yourusername/3d-print-backend:v1
docker push yourusername/3d-print-frontend:v1
```

### 6.3 Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up
```

---

## Step 7: Monitoring

### 7.1 Check System Status

```bash
# Check Docker containers
docker ps

# Check logs
docker-compose logs -f backend

# Check GPU usage
nvidia-smi

# Check disk space
df -h
```

### 7.2 Monitor Application

```bash
# API health check
curl http://localhost:8000/health

# Check job status
curl http://localhost:8000/api/v1/jobs/{job_id}

# View metrics
curl http://localhost:8000/metrics
```

---

## Step 8: Common Commands

### Development

```bash
# Start dev environment
docker-compose up -d

# Restart service
docker-compose restart backend

# View logs
docker-compose logs -f backend

# Run tests
pytest backend/tests/

# Format code
black backend/
```

### Database

```bash
# Access database
docker-compose exec postgres psql -U postgres -d print3d

# Run migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "Add new field"
```

### Git

```bash
# Create feature branch
git checkout -b feature/task-002-trellis

# Commit work
git add .
git commit -m "feat: Add TRELLIS integration"

# Push and create PR
git push origin feature/task-002-trellis
gh pr create
```

---

## Troubleshooting

### GPU Not Detected

```bash
# Check NVIDIA driver
nvidia-smi

# Check CUDA
nvcc --version

# Reinstall CUDA if needed
sudo dnf remove cuda-*
sudo dnf install cuda-11-8
```

### TRELLIS Not Loading

```bash
# Check Python environment
which python
python --version

# Reinstall TRELLIS
pip uninstall trellis
cd ~/projects/TRELLIS
pip install -e .

# Test import
python -c "from trellis.pipelines import TrellisImageTo3DPipeline; print('OK')"
```

### Docker Issues

```bash
# Reset Docker
docker system prune -a

# Rebuild images
docker-compose build --no-cache

# Check Docker daemon
sudo systemctl status docker
```

---

## Next Steps

1. ✅ Complete TASK_001 (Environment setup)
2. ✅ Test TRELLIS locally
3. ✅ Verify GPU works
4. → Begin TASK_002 (TRELLIS integration)
5. → Follow tasks/ directory for remaining work

---

## Resources

- **Documentation**: See `/docs` directory
- **Tasks**: See `/tasks` directory
- **Skills**: See `/.claude/skills` directory
- **Examples**: See `/examples` directory (will be created)

---

## Support

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review relevant skill file in `.claude/skills/`
3. Ask Claude Code with context
4. Check GitHub Issues
5. Review TRELLIS/Medusa documentation

---

**You're ready to start building! 🚀**

Begin with TASK_001 in the tasks/ directory.

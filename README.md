# 🚀 3D Print MVP - Photos to CAD Service

**Transform multi-angle photos into precision 3D models using professional photogrammetry**

Built with COLMAP + Point2CAD + DeepCAD + Medusa.js

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Development Timeline](#development-timeline)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This is a **production-ready MVP** for a professional photogrammetry service that converts multi-angle photos into precision CAD files. The service offers three subscription tiers with quota-based access:

| Tier | Monthly Quota | Processing Time | Price/Month | Rate Limit |
|------|---------------|-----------------|-------------|------------|
| **Starter** | 50 models | 15-20 min/model | £29 | 5 models/day |
| **Professional** | 200 models | 15-20 min/model | £99 | 25 models/day |
| **Enterprise** | 1000 models | 15-20 min/model | £399 | Unlimited |

**All tiers require 20-50 multi-angle photos per model for manufacturing-grade precision**

### Key Differentiators

✅ **Manufacturing precision** (traditional photogrammetry, not AI hallucination)
✅ **Parametric CAD output** (STEP files for editing, not just meshes)
✅ **Quota-based pricing** (predictable costs, scalable usage)
✅ **Production-ready infrastructure** (not a prototype)
✅ **Zero-trust security** (encrypted, monitored, audited)
✅ **Permissive licensed stack** (Apache 2.0 / BSD / MIT)

---

## ⚡ Features

### User Features
- 📸 **Drag-and-drop image upload**
- 🎨 **Three quality tiers**
- ⏱️ **Real-time processing status**
- 📥 **Instant STL download**
- 💳 **Stripe payment integration**
- 🔐 **Secure file storage**
- 📊 **Usage dashboard**

### Admin Features
- 📈 **Real-time monitoring dashboard**
- 👥 **User management**
- 💰 **Revenue analytics**
- 🛠️ **Job queue management**
- ⚠️ **Error tracking (Sentry)**
- 📊 **Cost tracking**

### Technical Features
- 🚀 **Serverless GPU processing** (RunPod)
- 🔒 **Zero-trust security architecture**
- 📦 **Encrypted file storage**
- 🌊 **Rate limiting & DDoS protection**
- 🎯 **Invisible STL watermarking**
- 📝 **Comprehensive audit logging**

---

## 🏗️ Technology Stack

### Photogrammetry Pipeline
| Component | Technology | Purpose | License |
|-----------|------------|---------|---------|
| **Structure from Motion** | [COLMAP](https://github.com/colmap/colmap) | Multi-view photogrammetry | BSD 3-Clause ✅ |
| **CAD Reconstruction** | [Point2CAD](https://github.com/prs-eth/point2cad) | Point cloud → parametric CAD | Apache 2.0 ✅ |
| **Design Refinement** | [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) | CAD sequence optimization | MIT ✅ |
| **GPU Processing** | RunPod Serverless | Pay-per-use GPU compute | Commercial |

### E-commerce Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| **E-commerce** | [Medusa.js](https://medusajs.com) | Orders, payments, subscriptions |
| **Processing API** | FastAPI | Job orchestration |
| **Database** | PostgreSQL | Data persistence |
| **Cache/Queue** | Redis | Job queue & caching |
| **Storage** | Cloudflare R2 | S3-compatible file storage |

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Storefront** | Next.js 14 | User interface |
| **Admin** | Medusa Admin | Management dashboard |
| **Hosting** | Vercel | Edge deployment |

### Infrastructure
| Component | Service | Cost |
|-----------|---------|------|
| **API Hosting** | Railway | ~$50/month |
| **GPU Processing** | RunPod | ~$50-200/month (pay-per-use) |
| **CDN** | Cloudflare | Free |
| **Monitoring** | Sentry | Free tier |

---

## 🚀 Quick Start

### Prerequisites

```bash
# System requirements
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- NVIDIA GPU with 24GB VRAM (for local dev)
- Git
```

### Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/3d-print-mvp.git
cd 3d-print-mvp

# 2. Run automated setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Start development environment
docker-compose up -d

# Services will be available at:
# - Frontend: http://localhost:3000
# - Medusa Admin: http://localhost:7001
# - Processing API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit with your credentials
nano .env
```

Required variables:
- `DATABASE_URL` - PostgreSQL connection string
- `RUNPOD_API_KEY` - RunPod API key
- `RUNPOD_ENDPOINT_ID` - RunPod serverless endpoint
- `STRIPE_SECRET_KEY` - Stripe secret key
- `CLOUDFLARE_R2_ACCESS_KEY` - R2 access key
- `ENCRYPTION_KEY` - Master encryption key

---

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture & design decisions |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide |
| [SECURITY.md](docs/SECURITY.md) | Security implementation & best practices |
| [API.md](docs/API.md) | API reference & examples |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues & solutions |

### Development Tasks

Detailed implementation tasks are in `/tasks`:

- [PHASE_1.md](tasks/PHASE_1.md) - Foundation & local development (Weeks 1-2)
- [PHASE_2.md](tasks/PHASE_2.md) - GPU processing service (Weeks 3-4)
- [PHASE_3.md](tasks/PHASE_3.md) - Frontend development (Weeks 5-6)
- [PHASE_4.md](tasks/PHASE_4.md) - Testing & optimization (Weeks 7-8)
- [PHASE_5.md](tasks/PHASE_5.md) - Launch & monitoring (Week 9+)

### Claude Code Skills

AI-assisted development skills are in `/.claude/skills`:

- [trellis-expert.md](.claude/skills/trellis-expert.md) - TRELLIS API expertise
- [medusa-ecommerce.md](.claude/skills/medusa-ecommerce.md) - Medusa.js patterns
- [security-expert.md](.claude/skills/security-expert.md) - Security best practices
- [testing-expert.md](.claude/skills/testing-expert.md) - Testing strategies

---

## ⏱️ Development Timeline

**Total: 8-12 weeks to production MVP**

```
Week 1-2:  Foundation (TRELLIS, FreeCAD, local testing)
Week 3-4:  GPU Service (RunPod, Docker, processing API)
Week 5-6:  Frontend (Next.js, Medusa, user interface)
Week 7-8:  Testing (E2E tests, performance, security)
Week 9+:   Launch (Beta testing, monitoring, iteration)
```

### Milestones

- ✅ **Week 2**: Working TRELLIS pipeline locally
- ✅ **Week 4**: Serverless GPU processing deployed
- ✅ **Week 6**: User-facing storefront live
- ✅ **Week 8**: Production-ready system
- 🎯 **Week 9**: Soft launch with beta users
- 🚀 **Week 10**: Public launch

---

## 🏛️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                   USER JOURNEY                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. User uploads 20-50 multi-angle photos              │
│  2. Selects subscription tier (checks quota)           │
│  3. Job submitted to processing queue                  │
│  4. RunPod processes with COLMAP photogrammetry        │
│  5. Point2CAD extracts parametric CAD                  │
│  6. DeepCAD optimizes design (optional)                │
│  7. User downloads STEP + STL files                    │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 TECHNICAL ARCHITECTURE                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Frontend (Next.js)                                    │
│    ↓                                                   │
│  Medusa.js Backend (Subscriptions & Quotas)            │
│    ↓                                                   │
│  Processing API (FastAPI)                              │
│    ↓                                                   │
│  RunPod Serverless (GPU)                               │
│    ├─ COLMAP (Structure from Motion)                  │
│    ├─ Point2CAD (Point Cloud → CAD)                   │
│    └─ DeepCAD (CAD Refinement)                        │
│    ↓                                                   │
│  Cloudflare R2 (File storage)                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed diagrams.

---

## 💰 Cost Breakdown

### Development Costs

```
Phase 1-2: $0 (local development)
Phase 3-4: $100 (RunPod testing)
Phase 5:   $150 (beta infrastructure)

Total Development: ~$250
```

### Monthly Operating Costs

```
Fixed Costs:
- Railway (Medusa + API):  $50/month
- Cloudflare R2:            $25/month (more storage for multi-image)
- Monitoring (Sentry):      $0 (free tier)
Subtotal:                   $75/month

Variable Costs (per model):
- RunPod GPU (15-20 min):  $0.40-0.53/model
  (A40 @ $0.00044/sec × 900-1200 seconds)

Example at 100 models/month (conservative):
- Fixed:                   $75
- GPU (avg $0.46/model):   $46
Total:                     $121/month

Revenue scenarios:
- 10 Starter subs:         £290/month
- 5 Professional subs:     £495/month
- 2 Enterprise subs:       £798/month
Margin: 85-90%
```

---

## 🔐 Security Features

- 🔒 **End-to-end encryption** (files encrypted at rest and in transit)
- 🎯 **Invisible watermarking** (prove STL ownership)
- 🚨 **Rate limiting** (prevent abuse)
- 👁️ **Audit logging** (all actions tracked)
- 🛡️ **DDoS protection** (Cloudflare)
- 🔑 **API authentication** (JWT tokens)
- 📝 **Input validation** (prevent injection attacks)
- 🏢 **SOC 2 compliance** (RunPod certified)

See [SECURITY.md](docs/SECURITY.md) for complete security architecture.

---

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run specific test suites
npm run test:unit          # Unit tests
npm run test:integration   # Integration tests
npm run test:e2e           # End-to-end tests
npm run test:security      # Security tests

# Performance benchmarking
npm run benchmark
```

### Test Coverage Goals

- Unit tests: >80%
- Integration tests: >70%
- E2E tests: Critical paths covered
- Security tests: OWASP Top 10 covered

---

## 📊 Monitoring & Observability

### Metrics Dashboard

Access at: `http://admin.yourdomain.com/metrics`

Key metrics:
- **Success rate** (target: >95%)
- **Average processing time** (target: <3 minutes)
- **GPU cost per job**
- **Revenue per user**
- **Conversion rate**

### Error Tracking

Sentry integration provides:
- Real-time error notifications
- Stack traces
- User context
- Performance monitoring

---

## 🤝 Contributing

This is a private project, but contributions are welcome from team members.

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature"`
3. Push branch: `git push origin feature/your-feature`
4. Open pull request

### Commit Message Convention

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
chore: Update dependencies
```

---

## 📄 License

**MIT License** - see [LICENSE](LICENSE) file for details

### Third-Party Licenses

**All core components have commercial-friendly licenses:**

- **COLMAP**: BSD 3-Clause (ETH Zurich & UNC Chapel Hill)
- **Point2CAD**: Apache 2.0 (prs-eth - changed from CC-BY-NC in March 2024)
- **DeepCAD**: MIT License (Rundi Wu)
- **Medusa.js**: MIT License
- **Next.js**: MIT License

**Commercial Use**: ✅ Fully permitted with no restrictions or revenue limits

---

## 🆘 Support

### Documentation
- [Project Overview](PROJECT_OVERVIEW.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING.md)

### Contact
- **Email**: support@yourdomain.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/3d-print-mvp/issues)

### Useful Links
- [COLMAP Repository](https://github.com/colmap/colmap)
- [Point2CAD Repository](https://github.com/prs-eth/point2cad)
- [DeepCAD Repository](https://github.com/ChrisWu1997/DeepCAD)
- [Medusa.js Docs](https://docs.medusajs.com)
- [RunPod Docs](https://docs.runpod.io)

---

## 🎯 Roadmap

### Phase 1: MVP (Current)
- ✅ Multi-image photogrammetry (COLMAP)
- ✅ Parametric CAD output (Point2CAD)
- ✅ Three subscription tiers
- ✅ Quota/rate limit management
- ✅ Stripe subscription payments
- ✅ Basic admin dashboard

### Phase 2: Enhancement (Month 3-6)
- 🔄 CAD refinement optimization (DeepCAD tuning)
- 🔄 Advanced mesh repair pipeline
- 🔄 MiCADangelo integration (when released)
- 🔄 Mobile app for photo capture
- 🔄 API marketplace

### Phase 3: Scale (Month 6-12)
- 🔄 White-label solutions
- 🔄 Enterprise features
- 🔄 Advanced CAD editing tools
- 🔄 International expansion
- 🔄 Batch processing

---

## 🌟 Acknowledgments

Built with these amazing open-source projects:

- [COLMAP](https://github.com/colmap/colmap) by ETH Zurich & UNC Chapel Hill
- [Point2CAD](https://github.com/prs-eth/point2cad) by PRS Lab, ETH Zurich
- [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) by Rundi Wu
- [Medusa.js](https://medusajs.com) by Medusa team
- [RunPod](https://runpod.io) for serverless GPU infrastructure

---

**Made with ❤️ for the 3D printing community**

*Last updated: November 2025*

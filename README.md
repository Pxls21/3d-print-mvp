# 🚀 R&D Platform - Scan to Manufacturing Service

**Transform multi-angle photos into manufactured prototypes using professional photogrammetry**

**Your complete rapid prototyping solution:** Scan → Process → Manufacture with FDM, SLS, CFC, and CNC

Built with COLMAP + Point2CAD + Medusa.js

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

This is an **R&D platform** that enables rapid prototyping from concept to finished part. Users scan prototypes with a smartphone camera, and our platform handles everything from 3D reconstruction to manufacturing with FDM, SLS, CFC printers, and CNC machines.

### Manufacturing Methods Available

| Method | Use Case | Turnaround | Quality | Best For |
|--------|----------|------------|---------|----------|
| **FDM** | Quick prototypes | Same day | Prototype | Form/fit testing, visual mockups |
| **SLS** | Functional parts | 1-2 days | Functional | Engineering validation, assembly testing |
| **CFC** | End-use parts | 2-3 days | Production | Fiber-reinforced components, final products |
| **CNC** | Precision parts | 1-2 days | Precision | Machined components, tight tolerances |

**All scans require 20-50 multi-angle photos for manufacturing-grade precision**

### Complete Workflow

```
1. Scan your prototype with phone camera (20-50 images)
2. Upload to platform → COLMAP + Point2CAD processing (8-14 min)
3. Review 3D preview and get AI manufacturing recommendations
4. Choose method: FDM (fast) → SLS (functional) → CFC (end-use) → CNC (precision)
5. Receive manufactured part
```

### Key Differentiators

✅ **One scan, multiple manufacturing options** (FDM/SLS/CFC/CNC from single scan)
✅ **Manufacturing precision** (traditional photogrammetry, not AI hallucination)
✅ **Parametric CAD output** (STEP files for CNC/CFC, STL for FDM/SLS)
✅ **AI manufacturing recommendations** (platform suggests optimal method)
✅ **Integrated workflow** (from scan to finished part in one platform)
✅ **R&D focused** (rapid iteration and prototyping)
✅ **Permissive licensed stack** (Apache 2.0 / BSD / MIT)

---

## ⚡ Features

### User Features
- 📸 **Multi-image upload** (20-50 photos from smartphone)
- 🤖 **AI manufacturing recommendations** (platform suggests optimal method)
- 🎨 **3D preview** (inspect before manufacturing)
- 🏭 **Multiple manufacturing methods** (FDM/SLS/CFC/CNC)
- ⏱️ **Real-time processing status** (track scan → manufacture)
- 📥 **STEP + STL download** (editable CAD for CNC/CFC, printable STL for FDM/SLS)
- 💳 **Flexible pricing** (pay per scan or subscription)
- 📊 **Project dashboard** (track all prototypes)

### Manufacturing Integration
- 🖨️ **FDM auto-queue** (ready STL sent directly to printer)
- 🔬 **SLS with cleanup** (automated post-processing workflow)
- 💪 **CFC with fiber planning** (STEP export for manual refinement)
- ⚙️ **CNC with CAM** (STEP + toolpath planning assistance)
- 📏 **Dimensional analysis** (automatic measurement and tolerance checking)
- 🎯 **Printability validation** (pre-flight checks before manufacturing)

### Admin Features
- 📈 **Real-time monitoring dashboard**
- 🏭 **Machine status tracking** (FDM/SLS/CFC/CNC availability)
- 👥 **User & project management**
- 💰 **Revenue analytics by manufacturing method**
- 🛠️ **Job queue management across all machines**
- ⚠️ **Error tracking (Sentry)**
- 📊 **Manufacturing cost tracking**

### Technical Features
- 🚀 **Serverless GPU processing** (RunPod)
- 🔒 **Zero-trust security architecture**
- 📦 **Encrypted file storage**
- 🌊 **Rate limiting & DDoS protection**
- 🎯 **Invisible STL watermarking**
- 📝 **Comprehensive audit logging**

---

## 🏗️ Technology Stack

### Photogrammetry Pipeline (Manufacturing-Grade)
| Component | Technology | Purpose | License | Processing Time |
|-----------|------------|---------|---------|-----------------|
| **Structure from Motion** | [COLMAP](https://github.com/colmap/colmap) | Multi-view photogrammetry (20-50 images) | BSD 3-Clause ✅ | 5-8 min |
| **CAD Reconstruction** | [Point2CAD](https://github.com/prs-eth/point2cad) | Point cloud → parametric CAD (STEP) | Apache 2.0 ✅ | 3-5 min |
| **GPU Infrastructure** | NVIDIA RTX 3090 (24GB VRAM) | Local processing (50-80 scans/day) | Hardware | **Total: 8-14 min** |

**Why this stack?**
- ✅ **COLMAP over Meshroom**: Faster (30-50%), better CLI automation, BSD license
- ✅ **Manufacturing precision**: Traditional photogrammetry, not AI hallucination
- ✅ **Dual output**: STL for FDM/SLS (auto-ready), STEP for CNC/CFC (manual refinement)
- ✅ **RTX 3090 capacity**: 4-6 scans/hour, 50-80 scans/day at 50% utilization

### Platform Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| **E-commerce & Billing** | [Medusa.js](https://medusajs.com) | Orders, payments, project management |
| **Processing API** | FastAPI | Job orchestration & manufacturing queue |
| **Database** | PostgreSQL | Projects, scans, manufacturing jobs |
| **Cache/Queue** | Redis | Job queue & real-time status |
| **Storage** | Cloudflare R2 | Multi-image uploads, STEP/STL storage |

### Manufacturing Integration
| Machine Type | Interface | Automation Level |
|--------------|-----------|------------------|
| **FDM Printers** | OctoPrint API | Fully automated (STL → print) |
| **SLS Printers** | Custom integration | Semi-automated (STL + post-processing) |
| **CFC Printers** | Manual + STEP export | Manual fiber planning required |
| **CNC Machines** | Custom CAM interface | Manual toolpath planning required |

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Storefront** | Next.js 14 | User interface |
| **Admin** | Medusa Admin | Management dashboard |
| **Hosting** | Vercel | Edge deployment |

### Infrastructure
| Component | Service | Cost | Purpose |
|-----------|---------|------|---------|
| **GPU Processing** | Local RTX 3090 | Hardware cost | COLMAP + Point2CAD processing |
| **API Hosting** | Railway / VPS | ~$50/month | FastAPI + Medusa.js |
| **Storage** | Cloudflare R2 | ~$25/month | Multi-image uploads, outputs |
| **CDN** | Cloudflare | Free | Asset delivery |
| **Monitoring** | Sentry | Free tier | Error tracking |
| **Manufacturing Queue** | Self-hosted | Included | OctoPrint + custom interfaces |

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

### Complete User Journey (Scan to Manufactured Part)

```
┌────────────────────────────────────────────────────────────┐
│                   USER WORKFLOW                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. User scans prototype (phone camera, 20-50 images)     │
│  2. Upload to platform → Processing queue                 │
│  3. COLMAP reconstruction (5-8 min on RTX 3090)           │
│  4. Point2CAD CAD extraction (3-5 min)                    │
│  5. Preview 3D model + get AI recommendations             │
│  6. User chooses manufacturing method:                    │
│     ├─ FDM: Auto-queue STL → OctoPrint                   │
│     ├─ SLS: Queue STL → Manual post-processing            │
│     ├─ CFC: Export STEP → User refines → Queue            │
│     └─ CNC: Export STEP → User plans CAM → Queue          │
│  7. Part manufactured and delivered                        │
│                                                            │
│  Total Time:                                               │
│  - Scanning: 5-10 min (user)                              │
│  - Processing: 8-14 min (automated)                       │
│  - FDM: 4-8 hours (same day)                              │
│  - SLS: 1-2 days                                           │
│  - CFC: 2-3 days (with user CAD work)                     │
│  - CNC: 1-2 days (with user CAM work)                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Technical Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   PLATFORM STACK                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Frontend (Next.js 14)                                     │
│    - Multi-image upload (20-50 photos)                    │
│    - 3D preview (Three.js)                                │
│    - Manufacturing method selection                        │
│    - Project dashboard                                     │
│         ↓                                                  │
│  Platform Backend (Medusa.js + FastAPI)                   │
│    - Project & scan management                             │
│    - Manufacturing queue orchestration                     │
│    - Billing & payments                                    │
│    - Machine availability tracking                         │
│         ↓                                                  │
│  Processing Server (RTX 3090)                              │
│    ├─ COLMAP (Structure from Motion)    [5-8 min]        │
│    ├─ Point2CAD (CAD Reconstruction)    [3-5 min]        │
│    ├─ Mesh validation & repair                            │
│    └─ Dual export: STL (FDM/SLS) + STEP (CFC/CNC)        │
│         ↓                                                  │
│  Manufacturing Integration                                 │
│    ├─ FDM: OctoPrint API → Auto-queue                    │
│    ├─ SLS: Custom queue + workflow                        │
│    ├─ CFC: STEP export → Manual refinement                │
│    └─ CNC: STEP export → CAM planning                     │
│         ↓                                                  │
│  File Storage (Cloudflare R2)                              │
│    - Multi-image uploads                                   │
│    - STEP files (for CFC/CNC)                             │
│    - STL files (for FDM/SLS)                              │
│    - Manufacturing outputs                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed diagrams.

---

## 💰 Pricing & Business Model

### Subscription Options

**Choose your plan**: Scan processing only, or scan + materials bundle

#### Option A: Scan Processing Only

| Tier | Monthly Quota | What's Included | Price/Month | Overage Rate | Rate Limit |
|------|---------------|-----------------|-------------|--------------|------------|
| **Starter** | 50 scans | COLMAP + Point2CAD processing (STEP + STL) | £29 | £0.60/scan | 5/day |
| **Professional** | 200 scans | COLMAP + Point2CAD processing (STEP + STL) | £99 | £0.50/scan | 25/day |
| **Enterprise** | 1000 scans | COLMAP + Point2CAD processing (STEP + STL) | £399 | £0.40/scan | Unlimited |

**Then buy materials separately as needed**

#### Option B: Scan + Materials Bundle (Best Value)

| Tier | Scan Quota | Materials Included | Price/Month | Savings |
|------|------------|-------------------|-------------|---------|
| **Starter + Materials** | 50 scans | 2kg filament OR 1kg PA12 powder/month | £49 | ~£20/month |
| **Professional + Materials** | 200 scans | 8kg filament OR 4kg PA12 OR 1x CF spool/month | £169 | ~£80/month |
| **Enterprise + Materials** | 1000 scans | 20kg filament OR 10kg PA12 OR 3x CF spools/month | £599 | ~£250/month |

**Bundle benefits**: Lower effective material cost + guaranteed allocation + tier discounts on additional purchases

---

### Material Shop (Separate Purchase)

**Users buy spools in advance, no subscription needed if you have CAD files ready**

| Material Type | Use With | Price | Yields (approx) | Tier Discount |
|---------------|----------|-------|-----------------|---------------|
| **Standard Filament (1kg)** | FDM | £20-30 | 5-10 small parts | 10% Pro, 15% Ent |
| **PA12 Nylon Powder (2kg)** | SLS | £60-80 | 8-12 functional parts | 10% Pro, 15% Ent |
| **Carbon Fiber Spool (500m)** | CFC | £150 | 3-5 composite parts | 10% Pro, 15% Ent |
| **Standard Spool + CF Bundle** | CFC | £180 | 3-5 composite parts | 10% Pro, 15% Ent |
| **CNC Material Stock** | CNC | Variable | Custom quote | 10% Pro, 15% Ent |

**How it works**:
1. **Scan** → Upload photos → Process to STL/STEP (uses subscription quota)
2. **Buy Materials** → Purchase spools based on what you need
3. **Queue Print** → FDM auto-queues, SLS/CFC/CNC scheduled
4. **Collect** → Pick up finished parts

**Alternative**: Already have CAD files? Skip step 1, buy materials, and just print!

### Cost Structure (per scan)

```
Processing Costs:
- GPU time (8-14 min on RTX 3090):  Amortized hardware cost
- Storage (300MB avg):               $0.01
- API/infrastructure:                $0.02
Total Processing:                    ~$0.05/scan

Manufacturing Costs (your estimates):
- FDM material + time:               ~$X
- SLS material + time:               ~$3X
- CFC material + time + labor:       ~$8X
- CNC material + time + labor:       ~$10X

Platform Margins:
- FDM tier: 40-50% margin
- SLS tier: 45-55% margin
- CFC/CNC tier: 35-45% margin (includes consultation)
```

### Revenue Model

```
Monthly Projections (50% capacity):
- 25 scans/day × 22 working days = 550 scans/month

Conservative mix:
- 60% FDM (330 scans):        £XXXk
- 30% SLS (165 scans):        £XXXk
- 10% CFC/CNC (55 scans):     £XXXk
Total Monthly Revenue:         £XXk/month

Costs:
- Fixed infrastructure:        £75
- Processing (550 scans):      £27
- Manufacturing materials:     £XXk
- Labor (monitoring):          £XXk
Total Monthly Costs:           £XXk

Net Monthly Profit:            £XXk (XX% margin)
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

### Phase 1: MVP - Core Scanning & FDM (Months 1-3)
- ✅ COLMAP + Point2CAD pipeline (8-14 min processing)
- ✅ Multi-image upload (20-50 photos)
- ✅ Dual output: STL (FDM) + STEP (CNC/CFC)
- ✅ FDM integration via OctoPrint
- ✅ Basic 3D preview and project dashboard
- ✅ Payment & project management (Medusa.js)
- 🎯 **Launch**: FDM-only prototyping service

### Phase 2: Add SLS & Manufacturing Intelligence (Months 3-6)
- 🔄 SLS printer integration + post-processing workflow
- 🔄 AI manufacturing recommendations (geometry analysis)
- 🔄 Dimensional analysis & tolerance checking
- 🔄 Advanced mesh repair pipeline
- 🔄 Mobile app for guided photo capture
- 🔄 Manufacturing queue dashboard
- 🎯 **Launch**: FDM + SLS service tiers

### Phase 3: CFC & CNC Integration (Months 6-9)
- 🔄 CFC printer integration with fiber path planning assistance
- 🔄 CNC machine integration with CAM workflow
- 🔄 STEP file editing guidance for users
- 🔄 Material selection recommendations
- 🔄 Advanced CAD refinement tools
- 🔄 Batch processing for repeat orders
- 🎯 **Launch**: Full manufacturing suite (FDM/SLS/CFC/CNC)

### Phase 4: Scale & Advanced Features (Months 9-12)
- 🔄 Multi-scanner setup (handle multiple RTX 3090s)
- 🔄 Advanced quality prediction ML model
- 🔄 White-label solutions for other R&D facilities
- 🔄 API marketplace for third-party integrations
- 🔄 Design optimization suggestions
- 🔄 International facility partnerships
- 🎯 **Goal**: 500+ scans/month, 85%+ automation

### Future Enhancements (Year 2+)
- MiCADangelo integration (when available November 2025+)
- In-browser STEP editor for CFC/CNC refinement
- AR preview for scale validation
- Automated fiber orientation for CFC
- Generative design suggestions
- Multi-material recommendations

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

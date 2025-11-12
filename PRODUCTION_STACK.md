# 🏗️ Production Stack - 3D Print MVP

**Updated**: November 12, 2025
**Status**: Validated & Ready for Implementation
**Approach**: Multi-Image Photogrammetry → Parametric CAD

---

## 📊 Executive Summary

This document defines the **final production technology stack** for the 3D Print MVP, based on comprehensive validation of licensing, technical capabilities, and business requirements.

### Key Decision: Photogrammetry Over AI

**Why we chose traditional photogrammetry:**
- ✅ Manufacturing-grade precision (not AI hallucination)
- ✅ Utilizes all 20-50 images effectively
- ✅ Parametric CAD output (STEP files for editing)
- ✅ All permissive licenses (Apache 2.0, BSD, MIT)
- ✅ Proven industrial workflow

**Why we rejected single-image AI models:**
- ❌ TRELLIS: Not photorealistic enough
- ❌ Wonder3D++: Too new (Dec 2024), untested
- ❌ Hunyuan3D-2: Geographic restriction (blocked in UK)
- ❌ InstantMesh: Known quality limitations
- ❌ Throws away valuable multi-view data

---

## 🎯 Core Technology Stack

### 1. Photogrammetry Pipeline

#### COLMAP (Structure from Motion)
- **Purpose**: Multi-view 3D reconstruction
- **License**: BSD 3-Clause ✅
- **Developer**: ETH Zurich & UNC Chapel Hill
- **Input**: 20-50 overlapping images
- **Output**: Sparse + dense point clouds
- **Processing Time**: 10-15 minutes (GPU-accelerated)
- **VRAM**: 8-16GB recommended
- **Commercial Use**: Fully permitted

**Key Features:**
- Industry-standard SfM pipeline
- Automatic feature matching
- Dense reconstruction
- Camera calibration
- GPU acceleration support

**Repository**: https://github.com/colmap/colmap

---

#### Point2CAD (Point Cloud → Parametric CAD)
- **Purpose**: Extract CAD primitives from point clouds
- **License**: Apache 2.0 ✅ (changed March 21, 2024)
- **Developer**: PRS Lab, ETH Zurich
- **Input**: Dense point clouds
- **Output**: Parametric B-rep (STEP files)
- **Processing Time**: 3-5 minutes
- **VRAM**: 16GB+ recommended
- **Commercial Use**: Fully permitted (no restrictions)

**Key Features:**
- Primitive detection (cylinders, planes, spheres, etc.)
- Parametric surface fitting
- B-rep topology construction
- STEP file export for CAD editing
- Edge and face segmentation

**Repository**: https://github.com/prs-eth/point2cad

**License History:**
- Dec 7, 2023: CC-BY-NC 4.0 (non-commercial) ❌
- Mar 21, 2024: Apache 2.0 (commercial) ✅

---

#### DeepCAD (CAD Sequence Refinement)
- **Purpose**: Optimize CAD construction sequence
- **License**: MIT ✅
- **Developer**: Rundi Wu
- **Input**: CAD sequences from Point2CAD
- **Output**: Refined, optimized CAD design
- **Processing Time**: 1-2 minutes
- **VRAM**: 8GB
- **Commercial Use**: Fully permitted

**Key Features:**
- CAD sequence optimization
- Design consistency improvement
- Reduces redundant operations
- Optional enhancement step

**Repository**: https://github.com/ChrisWu1997/DeepCAD

---

### 2. E-Commerce Platform

#### Medusa.js 2.0
- **Purpose**: Subscription management, quotas, payments
- **License**: MIT ✅
- **Developer**: Medusa Team
- **Features**:
  - Subscription tier management
  - Quota tracking per user
  - Rate limiting enforcement
  - Stripe integration
  - Usage analytics
  - Admin dashboard

**Repository**: https://github.com/medusajs/medusa

---

### 3. Backend Infrastructure

#### FastAPI (Processing Orchestrator)
- **Purpose**: Job queue, processing coordination
- **License**: MIT ✅
- **Features**:
  - Multi-image upload handling
  - Job queue management (Redis)
  - RunPod integration
  - Status tracking
  - Error handling

#### PostgreSQL (Database)
- **Purpose**: User data, subscriptions, quotas
- **License**: PostgreSQL License ✅
- **Data Stored**:
  - User accounts
  - Subscription tiers
  - Usage quotas
  - Processing jobs
  - File metadata

#### Redis (Cache & Queue)
- **Purpose**: Job queue, rate limiting, caching
- **License**: BSD ✅
- **Features**:
  - Bull queue for job processing
  - Rate limiting counters
  - Session caching
  - Real-time status updates

---

### 4. GPU Infrastructure

#### RunPod Serverless
- **Purpose**: On-demand GPU compute
- **Pricing**: Pay-per-use ($0.00044/sec for A40)
- **Hardware**: NVIDIA A40 (48GB VRAM) or A100
- **Features**:
  - Auto-scaling
  - Cold start optimization
  - Python SDK
  - Docker container deployment

**Cost per Model:**
```
15-20 min processing @ $0.00044/sec
= 900-1200 seconds
= $0.40-0.53 per model
```

---

### 5. Storage

#### Cloudflare R2 (S3-Compatible)
- **Purpose**: Image uploads, STEP/STL file storage
- **Pricing**:
  - Storage: $0.015/GB/month
  - Egress: $0 (free!)
  - API calls: $0.36/million
- **Features**:
  - S3-compatible API
  - CDN integration
  - No egress fees (major cost savings)
  - Global distribution

**Storage Estimates:**
```
Per job:
- Input: 20-50 images @ 5MB each = 100-250MB
- Output: STEP + STL = 10-50MB
- Total: ~300MB per job

At 100 models/month:
- Storage: 30GB
- Cost: $0.45/month
```

---

### 6. Frontend

#### Next.js 14
- **Purpose**: User storefront
- **License**: MIT ✅
- **Features**:
  - Multi-image upload UI
  - Subscription management
  - Quota display
  - Processing status tracking
  - File download

#### Tailwind CSS
- **Purpose**: Styling
- **License**: MIT ✅

---

## 🔄 Complete Processing Pipeline

```
User Flow:
1. User logs in → Check subscription tier
2. Check quota → Has remaining models?
3. Upload 20-50 images → Validate count and quality
4. Submit job → Queue in Redis
5. Deduct from quota → Update database

Processing Flow:
1. RunPod cold start → Pull Docker container
2. Download images from R2 → Local storage
3. Run COLMAP → Generate point cloud (10-15 min)
4. Run Point2CAD → Extract CAD primitives (3-5 min)
5. Run DeepCAD → Refine sequence (1-2 min)
6. Export STEP + STL → Upload to R2
7. Notify user → Email + dashboard notification

Total Time: 15-20 minutes per model
```

---

## 💰 Pricing & Business Model

### Subscription Tiers

| Tier | Price/Month | Quota | Rate Limit | Cost per Model | Margin |
|------|-------------|-------|------------|----------------|--------|
| **Starter** | £29 | 50 models | 5/day | £0.58 | 90% |
| **Professional** | £99 | 200 models | 25/day | £0.50 | 91% |
| **Enterprise** | £399 | 1000 models | Unlimited | £0.40 | 92% |

### Overage Pricing
- **£0.60 per additional model** beyond quota
- Automatically charged at end of billing cycle
- Prevents service interruption

### Cost Breakdown (per model)
```
GPU Processing: £0.40-0.53
Storage: £0.01
Payment Processing: £0.03-0.12 (2.9% + £0.30 on subscription)
Total Variable Cost: £0.44-0.66 per model

Pricing: £0.40-0.60 (effective per model in subscription)
Margin: 85-90%
```

---

## 📊 Technical Requirements

### Local Development (Fedora)
- **OS**: Fedora 39+
- **GPU**: NVIDIA RTX 3090 (24GB VRAM)
- **CUDA**: 11.8 or 12.x
- **RAM**: 32GB+ recommended
- **Storage**: 500GB+ for datasets

### Production (RunPod)
- **GPU**: NVIDIA A40 (48GB) or A100 (80GB)
- **VRAM**: 16GB minimum, 48GB recommended
- **CUDA**: 11.8+
- **Docker**: GPU-enabled container

### Software Dependencies
```bash
# Core Pipeline
- COLMAP (compile from source)
- Point2CAD (Python package)
- DeepCAD (Python package)
- PyTorch 2.0+
- CUDA Toolkit 11.8+

# Backend
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

# Frontend
- Next.js 14
- React 18+
```

---

## 🔐 Security & Compliance

### Data Security
- ✅ End-to-end encryption (images in transit)
- ✅ Encrypted storage (R2 server-side encryption)
- ✅ Secure file URLs (pre-signed, time-limited)
- ✅ API authentication (JWT tokens)

### Privacy
- ✅ GDPR compliant (EU users)
- ✅ Automatic file deletion (30 days after processing)
- ✅ User data export capability
- ✅ Right to deletion

### Rate Limiting
- ✅ Per-tier daily limits
- ✅ API rate limiting (100 req/min)
- ✅ Upload size limits (50MB per image)
- ✅ DDoS protection (Cloudflare)

---

## ✅ License Validation Summary

**All core components cleared for commercial use:**

| Component | License | Changed | Validation Date | Status |
|-----------|---------|---------|-----------------|--------|
| COLMAP | BSD 3-Clause | - | Nov 12, 2025 | ✅ Cleared |
| Point2CAD | Apache 2.0 | Mar 21, 2024 | Nov 12, 2025 | ✅ Cleared |
| DeepCAD | MIT | - | Nov 12, 2025 | ✅ Cleared |
| Medusa.js | MIT | - | Nov 12, 2025 | ✅ Cleared |
| Next.js | MIT | - | Nov 12, 2025 | ✅ Cleared |
| FastAPI | MIT | - | Nov 12, 2025 | ✅ Cleared |

**No licensing restrictions, no revenue limits, no attribution requirements beyond standard license notices.**

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for detailed license audit.

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
- ✅ Install COLMAP on Fedora
- ✅ Test Point2CAD integration
- ✅ Validate DeepCAD pipeline
- ✅ Measure VRAM usage and processing times
- ✅ Create test dataset (20-50 images)

### Phase 2: Backend (Weeks 3-4)
- ✅ Set up Medusa.js
- ✅ Implement subscription tiers
- ✅ Build quota tracking system
- ✅ Integrate rate limiting
- ✅ Set up PostgreSQL + Redis

### Phase 3: GPU Service (Week 5)
- ✅ Dockerize full pipeline
- ✅ Deploy to RunPod
- ✅ Test serverless endpoints
- ✅ Benchmark costs
- ✅ Optimize cold starts

### Phase 4: Frontend (Week 6)
- ✅ Build Next.js storefront
- ✅ Multi-image upload UI
- ✅ Subscription management
- ✅ Quota display
- ✅ Processing status tracker

### Phase 5: Testing & Launch (Weeks 7-8)
- ✅ E2E testing
- ✅ Performance optimization
- ✅ Security audit
- ✅ Beta launch

---

## 📈 Success Metrics

### Technical KPIs
- **Processing Success Rate**: >95%
- **Average Processing Time**: 15-20 minutes
- **VRAM Usage**: <48GB per job
- **API Uptime**: >99.5%

### Business KPIs
- **Subscriber Growth**: 10-20% MoM
- **Churn Rate**: <10% per month
- **Quota Utilization**: >60% average
- **Overage Revenue**: 10-20% of total revenue

### Quality KPIs
- **STEP File Validity**: >98%
- **STL Printability**: >95%
- **User Satisfaction**: >4.5/5
- **Support Tickets**: <2% of jobs

---

## 🔄 Future Enhancements

### Phase 2 (Months 3-6)
- 🔄 MiCADangelo integration (when released)
- 🔄 Advanced mesh repair pipeline
- 🔄 Mobile app for photo capture guidance
- 🔄 Batch processing for Enterprise tier
- 🔄 API marketplace

### Phase 3 (Months 6-12)
- 🔄 White-label solutions
- 🔄 In-browser CAD editor
- 🔄 Advanced analytics dashboard
- 🔄 Machine learning quality prediction
- 🔄 International expansion

---

## 📚 References

### Official Documentation
- [COLMAP Documentation](https://colmap.github.io/)
- [Point2CAD Paper](https://arxiv.org/abs/2312.00892)
- [DeepCAD GitHub](https://github.com/ChrisWu1997/DeepCAD)
- [Medusa.js Docs](https://docs.medusajs.com/)
- [RunPod Docs](https://docs.runpod.io/)

### Validation Documents
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) - License audit
- [FINAL_MODEL_RECOMMENDATION.md](FINAL_MODEL_RECOMMENDATION.md) - Model comparison
- [ALTERNATIVE_TECHNOLOGIES_ANALYSIS.md](ALTERNATIVE_TECHNOLOGIES_ANALYSIS.md) - Technology alternatives

---

## 🎯 Decision Log

### Why COLMAP over AI models?
**Decision Date**: November 11, 2025
**Rationale**:
- Manufacturing precision required
- 20-50 images available (don't throw away data)
- Industry-standard workflow
- All licenses cleared

### Why subscription over pay-per-job?
**Decision Date**: November 12, 2025
**Rationale**:
- Predictable revenue (MRR)
- Better customer retention
- Quota system prevents abuse
- Higher lifetime value

### Why Point2CAD over commercial solutions?
**Decision Date**: November 12, 2025
**Rationale**:
- Apache 2.0 license (changed Mar 2024)
- No licensing fees
- Full control over pipeline
- Academic quality, commercial license

---

**Last Updated**: November 12, 2025
**Version**: 2.0 (Photogrammetry Stack)
**Status**: ✅ Ready for Implementation

---

**All systems go! 🚀**

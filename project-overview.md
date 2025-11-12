# 🎯 R&D Platform - Project Overview

## Executive Summary

**Project**: Scan-to-Manufacturing R&D Platform
**Target Launch**: 8-12 weeks from start (FDM tier), 6-9 months for full suite
**Technology**: COLMAP + Point2CAD + RTX 3090 + FDM/SLS/CFC/CNC Integration
**Market**: Product developers, engineers, R&D teams, manufacturers
**Business Model**: Pay-per-scan with manufacturing (£X-£10X per scan) + subscription discounts

---

## The Problem

Rapid prototyping from concept to physical part is fragmented and slow:
- ❌ **Disconnected workflows**: Scan → CAD → Manufacturing are separate services
- ❌ **Limited method selection**: Most facilities offer only one manufacturing method
- ❌ **Expensive 3D scanning**: Professional scanners cost £300-£3000
- ❌ **Manual CAD work**: Hours of modeling for simple prototypes
- ❌ **Slow iteration**: Days-weeks between design changes and physical testing

**Result**: R&D teams waste time and money on fragmented prototyping workflows

---

## Our Solution

**Complete scan-to-manufacturing platform: One scan → Multiple manufacturing options → Finished parts**

### Integrated Manufacturing Methods

| Method | Turnaround | Automation | Best For | Ready State |
|--------|------------|------------|----------|-------------|
| **FDM** | Same day | Fully automated | Quick prototypes | STL → Auto-queue |
| **SLS** | 1-2 days | Semi-automated | Functional testing | STL + post-process |
| **CFC** | 2-3 days | Manual refinement | End-use parts | STEP + fiber planning |
| **CNC** | 1-2 days | Manual refinement | Precision parts | STEP + CAM planning |

**Single scan (20-50 photos) → All manufacturing options available**

### Platform Workflow

```
1. SCAN (5-10 min)
   └─ User captures prototype with phone camera (20-50 images)

2. PROCESS (8-14 min automated)
   ├─ COLMAP photogrammetry (5-8 min)
   ├─ Point2CAD CAD reconstruction (3-5 min)
   └─ Dual output: STL (FDM/SLS) + STEP (CFC/CNC)

3. REVIEW & SELECT
   ├─ 3D preview in browser
   ├─ AI manufacturing recommendations
   ├─ Dimensional analysis & tolerance check
   └─ Choose manufacturing method

4. MANUFACTURE
   ├─ FDM: Auto-queue → Same day delivery
   ├─ SLS: Queue → 1-2 days
   ├─ CFC: Export STEP → User refines → 2-3 days
   └─ CNC: Export STEP → User CAM plans → 1-2 days
```

### Key Innovation

**One Platform, Complete Workflow**:
1. ✅ **Single scan, multiple outputs**: FDM/SLS get ready STL, CFC/CNC get editable STEP
2. ✅ **AI manufacturing recommendations**: Platform analyzes geometry and suggests optimal method
3. ✅ **Integrated queue management**: All machines managed from one dashboard
4. ✅ **Flexible pricing**: Pay per scan + manufacturing, or subscription for discounts
5. ✅ **Traditional photogrammetry**: Manufacturing-grade precision, not AI hallucination

**Result**: R&D teams iterate 10x faster with complete scan-to-part workflow

---

## Technical Architecture

### Core Pipeline

```
20-50 Photos → COLMAP → Point Cloud → Point2CAD → STEP + STL → Manufacturing
   User         5-8 min   Sparse+Dense   3-5 min      Dual Output   Method Choice
```

### Why This Stack?

#### COLMAP (ETH Zurich & UNC Chapel Hill)
- **Input**: 20-50 multi-angle photos from smartphone
- **Output**: Dense point clouds via Structure-from-Motion
- **Speed**: 5-8 minutes on RTX 3090 (24GB VRAM)
- **License**: BSD 3-Clause (commercial friendly)
- **Quality**: Industry-standard photogrammetry
- **Why over Meshroom**: 30-50% faster, better CLI automation, preferred for production

#### Point2CAD (PRS Lab, ETH Zurich)
- **Input**: Dense point clouds from COLMAP
- **Output**: Parametric CAD (B-rep) as STEP files
- **Speed**: 3-5 minutes on RTX 3090
- **License**: Apache 2.0 (changed March 2024 - verified ✅)
- **Quality**: Manufacturing-grade CAD primitives
- **Output**: Editable STEP for CFC/CNC, convertible to STL for FDM/SLS

#### Local GPU Infrastructure (RTX 3090)
- **VRAM**: 24GB (sufficient for all processing)
- **Capacity**: 4-6 scans/hour, 50-80 scans/day at 50% utilization
- **Cost**: One-time hardware investment, amortized per scan
- **Reliability**: Local control, no cloud dependencies
- **Why local over RunPod**: Lower long-term costs, data privacy, instant availability

#### Medusa.js (Platform Management)
- **Purpose**: Project management, billing, user accounts
- **Flexibility**: Fully customizable for manufacturing workflows
- **License**: MIT
- **Features**: Order management, payment processing, admin dashboard

#### Manufacturing Queue Management
- **FDM**: Bambu Lab MQTT API integration (fully automated)
- **SLS**: Custom queue with post-processing workflow
- **CFC**: Manual queue with STEP file export and consultation
- **CNC**: Manual queue with CAM planning assistance

### System Diagram

```
┌─────────────────────────────────────────────────────┐
│  User uploads 20-50 photos via Next.js storefront  │
│           ↓                                         │
│  Medusa.js checks quota & subscription status       │
│           ↓                                         │
│  FastAPI queues job & triggers RunPod               │
│           ↓                                         │
│  RunPod GPU:                                        │
│    1. COLMAP (Structure from Motion)                │
│    2. Point2CAD (Point Cloud → CAD)                 │
│    3. DeepCAD (Refinement)                          │
│           ↓                                         │
│  User downloads STEP + STL from Cloudflare R2       │
│           ↓                                         │
│  Quota decremented, usage tracked                   │
└─────────────────────────────────────────────────────┘
```

---

## Market Opportunity

### Target Markets

**Primary (R&D Facilities & Product Development)**:
- Engineering teams needing rapid prototyping
- Product development companies
- Manufacturing R&D departments
- Industrial design studios
- Startups building physical products

**Secondary**:
- Educational institutions (engineering programs)
- Maker spaces and tech hubs
- Independent inventors and entrepreneurs
- Small manufacturing businesses

### Market Size & Positioning

- **Addressable Market**: $2B+ (rapid prototyping & manufacturing services)
- **Our Niche**: Integrated scan-to-manufacturing platform
- **Competitive Advantage**:
  - Single scan → multiple manufacturing options (vs fragmented workflows)
  - 10x faster iteration (vs traditional CAD + separate manufacturing)
  - 60-80% cost savings (vs outsourced scanning + separate manufacturing)

### Revenue Projections

**Year 1 (Conservative - FDM focus)**:
```
Capacity: 50-80 scans/day @ 50% = 25-40 scans/day
Monthly: 25 scans/day × 22 days = 550 scans/month

Month 1-3 (Ramp-up, 30% capacity):
  165 scans/month @ £X avg = £XXk/month

Month 4-6 (Growth, 50% capacity):
  275 scans/month @ £X avg = £XXk/month

Month 7-9 (Stable, 70% capacity):
  385 scans/month @ £X avg = £XXk/month

Month 10-12 (Add SLS, 80% capacity):
  440 scans/month @ £1.5X avg = £XXk/month

Year 1 Total: £XX-XXk MRR growth
```

**Year 2 (Add CFC/CNC)**:
```
Full suite operational (FDM/SLS/CFC/CNC)
Capacity: 80% utilization = 440 scans/month

Revenue mix:
- 60% FDM:      264 scans @ £X    = £XXk
- 25% SLS:      110 scans @ £3X   = £XXk
- 10% CFC:      44 scans  @ £10X  = £XXk
- 5% CNC:       22 scans  @ £12X  = £XXk
Total Monthly Revenue: £XXk/month → £XXXk ARR

Margin: 45-55% (including manufacturing costs)
```

**Key Metrics**:
- Average Transaction Value (ATV): £X-£10X per scan+manufacturing
- Customer Acquisition Cost (CAC): £100-200
- Repeat Rate: 40-60% (R&D teams iterate frequently)
- Payback Period: 2-4 scans

---

## Competitive Analysis

### Direct Competitors

| Service | Price | Time | Quality | Limitations |
|---------|-------|------|---------|-------------|
| **Professional Photogrammetry** | £50-200 | Days | Excellent | Expensive, slow |
| **3D Scanning Services** | £100+ | Hours | Good | Requires equipment |
| **Meshy.ai** | $20 | 5min | Good | Limited control |
| **Our Service** | £2-25 | 90s-15min | Good-Excellent | None |

### Competitive Advantages

1. **Price**: 80% cheaper than alternatives
2. **Speed**: 10x faster than manual photogrammetry
3. **Accessibility**: Works from smartphone photos
4. **Quality Tiers**: Choose speed vs quality
5. **Progressive Enhancement**: Start cheap, upgrade if needed

---

## Business Model

### Revenue Streams

**1. Scan + Manufacturing (Primary)**
- **FDM Tier**: £X per scan+print (same day turnaround)
- **SLS Tier**: £3X per scan+print (1-2 day turnaround)
- **CFC Tier**: £10X per scan+STEP export+consultation (2-3 day turnaround)
- **CNC Tier**: £12X per scan+STEP export+CAM assistance (1-2 day turnaround)

**2. Subscription Discounts (Secondary)**
- **Monthly Plan**: 20% discount on all scans (£XX/month minimum)
- **Annual Plan**: 35% discount on all scans (£XXX/year minimum)
- **Enterprise**: Custom pricing for high-volume R&D teams

**3. Additional Services (Future)**
- Design iteration packages (multiple scans of same prototype)
- CAD refinement service (human-in-the-loop for CFC/CNC)
- Rush processing (premium for faster turnaround)
- Material consultation and recommendations

### Cost Structure

**Fixed Costs** (~£100/month):
- API Hosting (Railway/VPS): £50/month
- Storage (Cloudflare R2): £30/month (multi-image + outputs)
- Monitoring & Analytics: £20/month
- Software licenses: Included (all open-source)

**Variable Costs per Scan**:
- Processing (GPU amortization): ~£0.05/scan (RTX 3090)
- Storage (300MB per scan): ~£0.01/scan
- Payment processing: 2.9% + £0.30
- **Manufacturing costs** (estimated, you'll need to refine):
  - FDM material + time: £Y
  - SLS material + time: £3Y
  - CFC material + time + consultation: £8Y
  - CNC material + time + CAM: £10Y

**Total Variable Cost**: £0.06 (processing) + Manufacturing + Payment fees

**Example P&L** (Conservative: 20 subscribers):
```
Revenue (10 Starter + 5 Pro + 2 Enterprise):
  10 × £29  = £290
   5 × £99  = £495
   2 × £399 = £798
  Total     = £1,583/month

Costs:
  Fixed              = £75
  Processing (avg 150 models) = £69
  Payment fees       = £49
  Total costs        = £193

Net Profit: £1,390/month (88% margin)
```

**Growth Scenario** (50 subscribers):
```
Revenue: £3,965/month
Costs: £415/month
Net Profit: £3,550/month (89% margin)
```

---

## Go-to-Market Strategy

### Phase 1: Soft Launch (Month 1-2)
- 🎯 Target: 50 beta users
- 📢 Channels: Reddit (r/3Dprinting), Product Hunt
- 💰 Offer: 50% discount for early adopters
- 📊 Goal: Validate product-market fit

### Phase 2: Public Launch (Month 3-6)
- 🎯 Target: 500 active users
- 📢 Channels: Social media, SEO, content marketing
- 💰 Pricing: Full price with free tier
- 📊 Goal: Achieve £4K MRR

### Phase 3: Scale (Month 6-12)
- 🎯 Target: 2,000+ users
- 📢 Channels: Partnerships, affiliates, paid ads
- 💰 Strategy: Upsell to subscriptions
- 📊 Goal: £20K+ MRR

---

## Development Timeline

### 8-Week MVP Development

**Weeks 1-2: Foundation**
- ✅ TRELLIS integration on RTX 3090
- ✅ FreeCAD STL validation
- ✅ Medusa.js backend setup

**Weeks 3-4: GPU Service**
- 🔨 Docker containerization
- 🔨 RunPod serverless deployment
- 🔨 FastAPI job orchestration

**Weeks 5-6: Frontend**
- 🎨 Next.js storefront
- 🎨 Upload interface
- 🎨 Job status tracking
- 🎨 Admin dashboard

**Weeks 7-8: Testing & Launch**
- 🧪 End-to-end testing
- 🧪 Performance optimization
- 🧪 Security audit
- 🚀 Beta deployment

### Post-Launch Roadmap

**Month 3-6: Enhancement**
- Multi-image optimization (gsplat integration)
- Custom rendering (SUAPP-style)
- Mobile app
- API marketplace

**Month 6-12: Scale**
- White-label solutions
- Enterprise features
- Advanced CAD integration
- International expansion

---

## Team & Resources

### Required Skills

**Development** (You):
- ✅ Python (TRELLIS, FastAPI)
- ✅ Node.js (Medusa.js)
- ✅ React/Next.js
- ✅ Docker/DevOps

**Tools**:
- ✅ Claude Code (AI-assisted development)
- ✅ Archon MCP (project management)
- ✅ RTX 3090 (local testing)
- ✅ GitHub (version control)

### External Services

- **Funding**: Prince's Trust (apply for startup grant)
- **Mentorship**: Technical advisor (optional)
- **Legal**: Terms of service, privacy policy
- **Accounting**: Revenue tracking

---

## Key Metrics (KPIs)

### Technical
- ✅ Success rate: >95%
- ✅ Avg processing time: <3 minutes
- ✅ System uptime: >99.5%

### Business
- 📈 Monthly Active Users (MAU)
- 💰 Monthly Recurring Revenue (MRR)
- 🔄 Conversion rate (free → paid)
- 📊 Customer Acquisition Cost (CAC)
- ❤️ Net Promoter Score (NPS)

### Quality
- ⭐ User satisfaction: >4.5/5
- 🔁 Repeat usage: >20%
- 🐛 Bug rate: <1%
- 📧 Support response: <2 hours

---

## Risk Mitigation

### Technical Risks

**Risk**: TRELLIS quality issues  
**Mitigation**: Offer refunds, test extensively, maintain high standards

**Risk**: GPU costs higher than expected  
**Mitigation**: Start conservative, optimize models, pass costs to users

**Risk**: Security breach  
**Mitigation**: Zero-trust architecture, encryption, audit logging

### Business Risks

**Risk**: Low conversion rates  
**Mitigation**: A/B testing, user feedback, pricing experiments

**Risk**: Competition  
**Mitigation**: Focus on speed + price advantages, build brand loyalty

**Risk**: Regulatory issues  
**Mitigation**: Legal review, GDPR compliance, clear ToS

---

## Success Criteria

### MVP Success (Week 8)
- ✅ 50+ beta users
- ✅ 90%+ processing success rate
- ✅ <3 minute avg processing time
- ✅ Positive user feedback

### Launch Success (Month 3)
- 💰 £1,500+ MRR
- 👥 500+ registered users
- 📊 10%+ conversion rate
- ⭐ 4.5+ rating

### Growth Success (Month 12)
- 💰 £20K+ MRR
- 👥 5,000+ users
- 🌍 Multi-country presence
- 🏆 Market leader in niche

---

## Next Steps

### Immediate (This Week)
1. ✅ Review all documentation
2. ✅ Set up repository structure
3. ✅ Begin TASK_001 (Environment setup)
4. 📝 Apply to Prince's Trust

### Short-term (Month 1)
1. Complete Phase 1 tasks
2. Test TRELLIS pipeline thoroughly
3. Set up Medusa backend
4. Create landing page

### Medium-term (Month 2-3)
1. Deploy RunPod processing
2. Build user interface
3. Soft launch with beta users
4. Iterate based on feedback

---

## Contact & Resources

### Project Links
- **Repository**: [GitHub URL]
- **Demo**: [Demo URL when live]
- **Docs**: [Documentation site]

### Useful Resources
- [TRELLIS GitHub](https://github.com/microsoft/TRELLIS)
- [SuGaR GitHub](https://github.com/Anttwo/SuGaR)
- [Medusa Docs](https://docs.medusajs.com)
- [RunPod Docs](https://docs.runpod.io)

### Support
- **Email**: [Your email]
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

## Appendix

### Technology Licenses

**All core components validated for commercial use:**

| Technology | License | Commercial Use | Validation |
|-----------|---------|----------------|------------|
| COLMAP | BSD 3-Clause | ✅ Yes | Validated ✅ |
| Point2CAD | Apache 2.0 | ✅ Yes | Changed Mar 2024 ✅ |
| DeepCAD | MIT | ✅ Yes | Validated ✅ |
| Medusa.js | MIT | ✅ Yes | Validated ✅ |
| Next.js | MIT | ✅ Yes | Validated ✅ |

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for full license audit.

### Estimated Costs Summary

**Development**: £150 (8 weeks)
**Monthly Operating**: £65-250 (scales with usage)
**Marketing**: £200-500/month (optional)

**Total Year 1**: £1,500-4,000

---

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Status**: Pre-launch Development

---

*This project is designed to be production-ready from day one. No shortcuts, no technical debt, no placeholders.*

**Let's build something amazing! 🚀**

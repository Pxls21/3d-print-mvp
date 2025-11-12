# 🎯 3D Print MVP - Project Overview

## Executive Summary

**Project**: Professional Photogrammetry-to-CAD Service
**Target Launch**: 8-12 weeks from start
**Technology**: COLMAP + Point2CAD + DeepCAD + Medusa.js + RunPod
**Market**: Product designers, manufacturers, reverse engineering, 3D printing
**Business Model**: Quota-based SaaS (£29-£399/month subscriptions)

---

## The Problem

Creating 3D printable models from physical objects requires:
- ❌ Expensive 3D scanners (£300-£3000)
- ❌ Complex CAD software expertise
- ❌ Manual photogrammetry (hours of work)
- ❌ Professional service (£50-£200 per model)

**Result**: High barrier to entry for casual users

---

## Our Solution

**Turn multi-angle smartphone photos into parametric CAD files using professional photogrammetry**

### Three Subscription Tiers

| Tier | Monthly Quota | Processing Time | Price/Month | Rate Limit | Output |
|------|---------------|-----------------|-------------|------------|--------|
| **Starter** | 50 models | 15-20 min | £29 | 5/day | STEP + STL |
| **Professional** | 200 models | 15-20 min | £99 | 25/day | STEP + STL |
| **Enterprise** | 1000 models | 15-20 min | £399 | Unlimited | STEP + STL |

**All tiers require 20-50 multi-angle photos per model**

### Key Innovation

**Manufacturing-Grade Photogrammetry**:
1. Traditional photogrammetry (not AI hallucination)
2. Parametric CAD output (STEP files for editing)
3. Quota-based predictable pricing
4. Professional-grade accuracy for reverse engineering

**Result**: Predictable costs, scalable for businesses, manufacturing precision

---

## Technical Architecture

### Core Pipeline

```
20-50 Photos → COLMAP → Point Cloud → Point2CAD → DeepCAD → STEP + STL
               15-20 min  Sparse+Dense  CAD Primitives  Refinement  Download
```

### Why This Stack?

#### COLMAP (ETH Zurich & UNC Chapel Hill)
- **Input**: 20-50 multi-angle photos
- **Output**: Dense point clouds via Structure-from-Motion
- **Speed**: 10-15 minutes on GPU
- **License**: BSD 3-Clause (commercial friendly)
- **Quality**: Industry-standard photogrammetry

#### Point2CAD (PRS Lab, ETH Zurich)
- **Input**: Point clouds from COLMAP
- **Output**: Parametric CAD primitives (B-rep)
- **Speed**: 3-5 minutes
- **License**: Apache 2.0 (changed March 2024)
- **Quality**: Manufacturing-grade accuracy

#### DeepCAD (Optional Refinement)
- **Purpose**: Optimize CAD sequence
- **Speed**: 1-2 minutes
- **License**: MIT
- **Quality**: Improves design consistency

#### Medusa.js (E-commerce)
- **Purpose**: Subscriptions, quotas, usage tracking
- **Flexibility**: Fully customizable
- **License**: MIT
- **Ecosystem**: Rich plugin ecosystem

#### RunPod (GPU Cloud)
- **Model**: Serverless, pay-per-use
- **Cost**: $0.40-0.53 per model
- **Scale**: Auto-scaling
- **Hardware**: NVIDIA A40/A100 GPUs

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

**Primary**: 
- Hobbyist 3D printer owners (2M+ globally)
- Product designers and makers
- Educational institutions

**Secondary**:
- E-commerce sellers (product photos → 3D models)
- AR/VR content creators
- Game developers

### Market Size

- **Addressable Market**: $500M+ (3D printing services)
- **Our Niche**: Photo-to-STL automation
- **Competitive Advantage**: 10x faster, 80% cheaper

### Revenue Projections

**Year 1 (Conservative)**:
```
Month 1-3:   10 subscribers  → £500/month
Month 4-6:   30 subscribers  → £1,500/month
Month 7-9:   60 subscribers  → £3,000/month
Month 10-12: 100 subscribers → £5,000/month

Year 1 Total: £20-30K MRR growth
Average LTV: £600-1,200 per customer
```

**Year 2 (Growth)**:
```
500 subscribers → £25K/month → £300K ARR
Churn rate: <10%/month (target)
Margin: 85-90% (predictable costs)
```

**Key Metrics**:
- Customer Acquisition Cost (CAC): £50-100
- Lifetime Value (LTV): £600-1,200
- LTV:CAC Ratio: 6-12:1 (healthy)
- Payback Period: 2-3 months

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

**1. Subscription Tiers (Primary)**
- Starter: £29/month (50 models, 5/day rate limit)
- Professional: £99/month (200 models, 25/day rate limit)
- Enterprise: £399/month (1000 models, unlimited rate limit)

**2. Overage Charges (Secondary)**
- £0.60 per additional model beyond quota
- Automatically charged at end of billing cycle

**3. API Access (Future)**
- £149/month base + £0.40 per API call
- Enterprise custom pricing

### Cost Structure

**Fixed Costs** (~£75/month):
- Railway (API + Database): £50/month
- Cloudflare R2 (Storage): £25/month (multi-image storage)
- Monitoring (Sentry): £0 (free tier)

**Variable Costs**:
- RunPod GPU: £0.40-0.53 per model (15-20 min processing)
- Payment processing: 2.9% + £0.30 (monthly subscription)

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

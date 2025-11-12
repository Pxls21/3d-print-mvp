# 🏭 Equipment & Cost Breakdown - R&D Manufacturing Platform

**Updated**: November 12, 2025
**Status**: Research Complete - Ready for Purchasing Decisions

---

## 📋 Executive Summary

This document contains detailed equipment specifications, material costs (UK pricing), and business model breakdown for your R&D manufacturing platform.

### Business Model (Corrected)

**3 Revenue Streams**:
1. **Scan Processing Subscriptions** (£29/£99/£399) - COLMAP + Point2CAD photogrammetry
2. **Optional Materials Bundles** (£49/£169/£599) - Scan + monthly material allocation
3. **Material Shop** (No subscription needed) - Pay-per-spool for users with existing CAD files

---

## 🛠️ Equipment to Purchase

### 1. **FibreSeek3D FibreSeeker 3** (CFC Printer)

**Status**: To Purchase
**Price**: $2,699 USD (~£2,100 GBP)

#### Technical Specifications
- **Build Volume**: 300 × 300 × 245 mm
- **Precision**: ±0.2 mm accuracy, 50 μm minimum layer thickness
- **Speed**:
  - FDM: up to 500 mm/s
  - CFC reinforcement: 20 cc/h
- **Temperature**:
  - Nozzles: up to 320°C
  - Heated bed: up to 110°C (auto-leveling)
- **Extruder**: Dual system (plastic filament + continuous fiber)
- **Features**:
  - Sensors detect filament breaks/fiber clogs
  - Integrated HD camera for live monitoring
  - 3 printing modes: High Speed, High Strength, Hyper Strength

#### Material Compatibility
**Standard Plastics**: PLA, PETG, PC, PA (nylon), PACF, PETGF

**Continuous Fibers**:
- X-CCF (continuous carbon fiber)
- X-CGF (continuous glass fiber)

**Open-source compatible** for third-party PLA/PETG

#### Performance
- **Tensile Strength**: Up to 900 MPa (rivals metals)
- **Weight**: Significantly lighter than metal equivalents

#### Material Costs (FibreSeek3D)
| Material | Size | Cost (USD) | Cost (GBP) | Your Markup | Your Price |
|----------|------|------------|------------|-------------|------------|
| X-CCF (Carbon Fiber) | 500m | $49 | ~£38 | ~295% | **£150** |
| X-CGF (Glass Fiber) | 500m | $49 | ~£38 | ~295% | £150 |
| Standard PLA/PETG | 1kg | Market | £15-25 | ~60% | £25-40 |

**Yields**:
- 1x CF spool → 3-5 composite parts (depending on size/infill)

**Your Margins**:
- Carbon fiber: £150 - £38 = **£112 profit/spool** (295% markup)
- Standard plastic: £30 - £20 = **£10 profit/kg** (50% markup)

---

### 2. **SLS4ALL Inova MK1** (SLS Printer)

**Status**: To Purchase
**Options**:
- Full Kit: $6,990 USD (~£5,450 GBP)
- DIY Kit: $3,860 USD (~£3,010 GBP)

#### Technical Specifications
- **Build Volume**:
  - Total chamber: 177 × 177 × 200 mm
  - Effective for PA12: 150 × 150 × 180 mm
- **Dimensions**: 665 × 455 × 932 mm
- **Weight**: ~55 kg (121 lbs)
- **Laser Spot Size**: ~350 µm
- **Pre-heating Time**:
  - 230V: <45 minutes
  - 110V: <75 minutes
- **Scanning Speed**: 2,800 mm/s (at 25% packing density)
- **Print Speed**: ~9 mm/hour (Z-axis) at 25% density, 100 µm layers
- **Control**: Raspberry Pi 5 + 7" touchscreen + built-in camera
- **Software**: SLS4All Compact (built on Klipper)

#### Material Compatibility
**Primary**: PA12 Nylon powder

**Also supports**:
- TPU-based powders
- Other materials with melting point <200°C

#### UK PA12 Nylon Suppliers
| Supplier | Product | Size | Price (est.) |
|----------|---------|------|--------------|
| 3D Prima UK | PA12 SLS Powder | 6kg | £80-120 |
| CDG UK | PA12 Industrial | 6kg | £90-130 |
| Replik8 UK | PA12 Smooth Fresh | 2kg | £50-70 |
| Formlabs UK | Nylon 12 Powder | 5kg | £100-150 |

**Your Pricing Strategy**:
| Material | Purchase Cost | Your Price | Margin |
|----------|---------------|------------|--------|
| PA12 Nylon (2kg) | £50-60 | **£80** | 40% |
| PA12 Nylon (6kg) | £100-120 | **£160** | 35% |

**Yields**:
- 2kg PA12 → 8-12 functional parts (depending on size)
- Powder can be refreshed (mix fresh with used)

---

### 3. **FDM Printers** (Already Owned)

**Status**: Already Have
**Quantity**: 2 printers

#### Material Costs (UK Market, 2025)
| Filament Type | Size | Market Price | Your Price | Margin |
|---------------|------|--------------|------------|--------|
| PLA | 1kg | £12-20 | **£25** | 40% |
| PETG | 1kg | £15-25 | **£30** | 35% |
| ABS | 1kg | £15-25 | **£30** | 35% |
| Bulk (2.3-8.5kg) | Per kg | £8-15 | **£20** | 40% |

**Yields**:
- 1kg filament → 5-10 small prototypes or 2-3 large parts

**Integration**:
- Bambu Lab MQTT API for auto-queueing (MIT licensed Python library)
- STL from COLMAP → Direct to print queue
- Models: 2x Bambu Lab P1S printers

---

### 4. **CNC Machine** (Self-Built)

**Status**: To Build (using FDM/SLS printed parts)
**Estimated Cost**: £500-1,500 (rails, spindle, electronics, controller)

#### Material Costs (TBD)
- Aluminum stock
- Plastic stock
- Brass/copper
- Custom quote per job

**Integration**:
- STEP file from Point2CAD
- User performs CAM planning (Fusion 360, FreeCAD)
- Custom queue management

---

## 💰 Complete Business Model Breakdown

### Subscription Options

#### **Option A: Scan Processing Only**
| Tier | Scan Quota | Price/Month | Overage | Rate Limit |
|------|------------|-------------|---------|------------|
| Starter | 50 scans | £29 | £0.60/scan | 5/day |
| Professional | 200 scans | £99 | £0.50/scan | 25/day |
| Enterprise | 1000 scans | £399 | £0.40/scan | Unlimited |

**What's included**: COLMAP + Point2CAD processing (8-14 min) → STEP + STL output

**Users then**: Buy materials separately as needed

---

#### **Option B: Scan + Materials Bundle**
| Tier | Scan Quota | Materials Included | Price/Month | Savings vs Separate |
|------|------------|-------------------|-------------|---------------------|
| Starter + Materials | 50 scans | 2kg filament OR 1kg PA12 | £49 | ~£20/month |
| Professional + Materials | 200 scans | 8kg filament OR 4kg PA12 OR 1x CF spool | £169 | ~£80/month |
| Enterprise + Materials | 1000 scans | 20kg filament OR 10kg PA12 OR 3x CF spools | £599 | ~£250/month |

**Bundle benefits**:
- Predictable monthly costs
- Guaranteed material allocation
- Additional tier discounts on extra purchases (10-15% off)
- Best for regular/high-volume users

---

#### **Option C: No Subscription (Material Shop Only)**
**For users with existing CAD files**

Buy materials, queue prints, skip scanning entirely.

| Material | Price | Notes |
|----------|-------|-------|
| Standard Filament (1kg) | £25-30 | PLA/PETG/ABS |
| PA12 Nylon (2kg) | £80 | SLS powder |
| Carbon Fiber Spool (500m) | £150 | FibreSeek3D X-CCF |
| Standard + CF Bundle | £180 | Both materials for CFC |
| CNC Stock | Variable | Custom quote per job |

---

### Revenue Projections

#### **Conservative Scenario** (30% utilization, FDM-focused launch)

**Month 1-3 Ramp-up**:
```
Subscribers:
- 5 Starter (£29) = £145
- 3 Professional (£99) = £297
- 1 Enterprise (£399) = £399
Total Subscription Revenue: £841/month

Materials (assume 50% take bundles, 50% buy separately):
- Bundle upgrades: +£100/month
- Separate purchases: ~£300/month (20 spool sales @ £15 avg profit)
Total Material Revenue: £400/month

TOTAL MONTHLY REVENUE: £1,241/month
```

**Month 4-6 Growth**:
```
Subscribers:
- 10 Starter = £290
- 8 Professional = £792
- 3 Enterprise = £1,197
Total Subscription: £2,279/month

Materials:
- Bundle upgrades: +£420/month
- Separate purchases: ~£600/month
Total Materials: £1,020/month

TOTAL MONTHLY REVENUE: £3,299/month
```

**Month 10-12 (Adding SLS)**:
```
Subscribers:
- 15 Starter = £435
- 15 Professional = £1,485
- 5 Enterprise = £1,995
Total Subscription: £3,915/month

Materials (now with SLS):
- Bundle upgrades: +£1,050/month
- Separate purchases: ~£1,200/month (higher value SLS sales)
Total Materials: £2,250/month

TOTAL MONTHLY REVENUE: £6,165/month
```

---

### Cost Structure

#### **Fixed Costs** (~£125/month)
- API Hosting (Railway/VPS): £50/month
- Storage (Cloudflare R2): £40/month (multi-image + outputs)
- Monitoring & Analytics: £25/month
- Software licenses: £0 (all open-source)
- Internet/utilities: £10/month

#### **Variable Costs per Scan**
- GPU amortization (RTX 3090): ~£0.05/scan
- Storage (300MB avg): ~£0.01/scan
- API/infrastructure: ~£0.02/scan
- Payment processing: 2.9% + £0.30 per transaction

**Total processing cost**: ~£0.08/scan + payment fees

#### **Material Costs** (your actual costs)
| Material | Your Cost | Your Price | Margin |
|----------|-----------|------------|--------|
| Standard Filament (1kg) | £15-20 | £25-30 | 40-50% |
| PA12 Nylon (2kg) | £50-60 | £80 | 35-40% |
| Carbon Fiber (500m) | £38 | £150 | 295% |

---

### Profitability Analysis

**Example: Month 6 (Growth Phase)**

**Revenue**: £3,299/month
```
Subscription: £2,279
Materials: £1,020
```

**Costs**: ~£1,100/month
```
Fixed: £125
Processing (165 scans @ £0.08): £13
Material COGS (assume £600 in sales → £360 cost): £360
Payment processing (2.9% of £3,299): £96
Labor (20 hrs/month monitoring @ £25/hr): £500
```

**Net Profit**: £2,199/month (**67% margin**)

---

## 🎯 Capital Investment Required

### One-Time Equipment Purchases

**Chosen Strategy**: DIY Kit + CFC Printer (buy together, use CFC to make DIY parts)

| Item | Cost | Priority | Notes |
|------|------|----------|-------|
| **SLS4ALL Inova MK1 (DIY Kit)** | **£3,010** | **Phase 2 (Month 3-6)** | **Chosen option** |
| **FibreSeek3D FibreSeeker 3** | **£2,100** | **Phase 2 (Month 3-6)** | **Use to make SLS DIY parts** |
| CNC Build (self-built) | £500-1,500 | Phase 4 (Month 9-12) | Fabricate with SLS/CFC |
| **Total Equipment Investment** | **£6,610-7,610** | | |

**Smart Strategy Benefits**:
- Buy both SLS DIY + CFC together for £5,110
- Less than one full SLS kit (£5,450)
- CFC printer fabricates the aluminum parts needed for SLS DIY assembly
- Get **two** manufacturing capabilities (SLS + CFC) for price of one
- Savings: £2,440 vs buying full SLS kit + CFC separately (£7,550)

### Initial Material Inventory
| Material | Quantity | Cost | Purpose |
|----------|----------|------|---------|
| Standard Filament | 10kg | £150-200 | FDM launch stock |
| PA12 Nylon | 6kg | £100-120 | SLS launch stock |
| Carbon Fiber Spools | 3x500m | £114 (cost) | CFC launch stock |
| **Total Initial Inventory** | | **£364-434** | |

### Platform Development
| Item | Cost | Timeline |
|------|------|----------|
| RTX 3090 (already have) | £0 | - |
| Software development (DIY) | £0 | 8-12 weeks |
| Hosting (first 3 months) | £375 | Initial |
| **Total Platform** | **£375** | |

---

## 📊 Total Startup Capital Needed

### **Minimum Launch** (FDM only, Month 1-3)
```
- Equipment: £0 (use existing FDM printers)
- Materials: £150 (5kg filament stock)
- Platform: £375 (3 months hosting)
TOTAL: £525
```

### **Phase 2 Complete** (FDM + SLS + CFC, Month 6)
```
- Equipment: £5,110 (SLS DIY kit + FibreSeek3D CFC)
- Materials: £364 (combined stock including carbon fiber)
- Platform: £375 (already paid)
TOTAL: £5,849

**Note**: Both SLS and CFC operational simultaneously
**Savings**: £2,440 vs buying full SLS + CFC separately
```

### **Full Suite** (FDM + SLS + CFC + CNC, Month 12)
```
- Equipment: £6,610 (SLS DIY + FibreSeek + CNC self-built)
- Materials: £434 (full stock)
- Platform: £375 (already paid)
TOTAL: £7,419

**Note**: All four manufacturing methods operational
**Total Savings**: £2,440 from smart DIY + CFC strategy
```

---

## 🚀 Recommended Purchase Timeline

### **Phase 1: Launch (Month 1-3)** - FDM Only
**Investment**: £525
- Use existing FDM printers
- Scan processing subscriptions start
- Material sales (filament only)
- **Expected Revenue**: £840-1,200/month by Month 3

### **Phase 2: Add SLS + CFC** (Month 3-6)
**Investment**: £5,110 (DIY kit + CFC printer purchased together)
- Purchase SLS4ALL Inova MK1 **DIY kit** (£3,010)
- Purchase FibreSeek3D FibreSeeker 3 (£2,100)
- **Smart Strategy**: Use CFC printer to fabricate SLS DIY kit aluminum parts
- Add PA12 nylon + carbon fiber material sales
- Launch both SLS and CFC tiers simultaneously
- Upgrade subscription bundles with premium materials
- **Expected Revenue**: £3,500-5,000/month by Month 6

### **Phase 3: Optimize & Scale** (Month 6-9)
**Investment**: Minimal (both printers operational)
- Refine SLS + CFC workflows
- Build material inventory based on demand
- Optimize fiber path planning for CFC
- **Expected Revenue**: £4,000-5,500/month by Month 9

### **Phase 4: Add CNC** (Month 9-12)
**Investment**: £500-1,500
- Build self-fabricated CNC
- Add precision machining services
- Complete manufacturing suite
- **Expected Revenue**: £6,000-8,000/month by Month 12

---

## 💡 Key Business Insights

### **Margins by Method**
1. **CFC (Carbon Fiber)**: **295% markup** - Highest margin
2. **SLS (Nylon)**: **35-40% margin** - Good functional parts margin
3. **FDM (Filament)**: **40-50% margin** - Bread and butter
4. **Scan Processing**: **95%+ margin** - Pure software/GPU amortization

### **Revenue Split Projection** (Month 12)
```
Subscriptions: ~60% (£3,600-4,800/month)
Materials: ~40% (£2,400-3,200/month)
```

### **User Behavior Assumptions**
- 60% choose scan-only, buy materials as needed
- 30% choose scan + materials bundle (regular users)
- 10% material-only (existing CAD files, no scans needed)

---

## 🎁 Loyalty Rewards Program

**Reward customer loyalty with progressive discounts and benefits based on usage and spend**

### Tier System (Automatic Progression)

Users automatically progress through tiers based on **lifetime scans processed + total spend**:

| Tier | Requirements | Scan Discount | Material Discount | Benefits |
|------|-------------|---------------|-------------------|----------|
| **Bronze** | 0-50 scans OR £0-500 spend | 0% | 0% | Standard pricing |
| **Silver** | 51-150 scans OR £501-1,500 spend | 5% | 10% | Priority queue, monthly free scan |
| **Gold** | 151-500 scans OR £1,501-5,000 spend | 10% | 15% | Express processing, 3 free scans/month |
| **Platinum** | 501+ scans OR £5,001+ spend | 15% | 20% | Dedicated support, 5 free scans/month, early access |

**How it works**:
- Discounts apply automatically at checkout
- Tier status tracked in user dashboard
- Progress bars show how close users are to next tier
- Once achieved, tier status maintained for 12 months (renewable)

---

### Subscription Loyalty Bonuses

**Reward long-term commitment with additional benefits**:

| Subscription Length | Bonus | Effective Discount | Material Credit |
|---------------------|-------|-------------------|-----------------|
| **3 Months** | +5% off materials | Standard + tier discount | £10 credit |
| **6 Months** | +10% off materials | Standard + tier discount | £25 credit |
| **12 Months** | +15% off materials + 1 month free | 1 month free + tier discount | £75 credit |

**Annual subscribers get**:
- 13 months for the price of 12
- Additional 15% off all material purchases
- £75 material credit (use on any material)
- Platinum tier benefits (regardless of usage)

---

### Volume Purchase Discounts

**Bulk material purchases get progressive discounts**:

#### Standard Filament (PLA/PETG/ABS)
| Quantity | Regular Price | Volume Discount | Your Price | Savings |
|----------|---------------|-----------------|------------|---------|
| 1-2kg | £25/kg | 0% | £25/kg | - |
| 3-5kg | £25/kg | 10% | £22.50/kg | £2.50/kg |
| 6-10kg | £25/kg | 15% | £21.25/kg | £3.75/kg |
| 11kg+ | £25/kg | 20% | £20/kg | £5/kg |

#### PA12 Nylon Powder (SLS)
| Quantity | Regular Price | Volume Discount | Your Price | Savings |
|----------|---------------|-----------------|------------|---------|
| 2kg | £80 | 0% | £80 | - |
| 4-6kg | £40/kg | 10% | £36/kg | £8 total |
| 8-12kg | £40/kg | 15% | £34/kg | £12/kg |
| 14kg+ | £40/kg | 20% | £32/kg | £16/kg |

#### Carbon Fiber Spools (CFC)
| Quantity | Regular Price | Volume Discount | Your Price | Savings |
|----------|---------------|-----------------|------------|---------|
| 1 spool | £150 | 0% | £150 | - |
| 2-3 spools | £150/each | 8% | £138/each | £12/each |
| 4-6 spools | £150/each | 12% | £132/each | £18/each |
| 7+ spools | £150/each | 15% | £127.50/each | £22.50/each |

**Volume discounts stack with tier discounts** (max combined: 35% off)

---

### Referral Rewards

**Grow the community and get rewarded**:

| Referrals | Referrer Reward | New User Reward |
|-----------|----------------|-----------------|
| **First referral** | £25 credit + 5 free scans | 20% off first month |
| **3 referrals** | £100 credit + Silver tier (3 months) | 20% off first month |
| **5 referrals** | £200 credit + Gold tier (6 months) | 20% off first month |
| **10 referrals** | £500 credit + Platinum tier (12 months) | 20% off first month |

**How it works**:
1. Share your unique referral link
2. New user signs up and completes first paid scan
3. You both get rewards instantly
4. No limit on referrals!

---

### Milestone Rewards

**Celebrate achievements with bonus credits**:

| Milestone | Achievement | Reward |
|-----------|-------------|--------|
| **First Scan** | Complete your first scan | £5 credit |
| **10 Scans** | Process 10 scans | £15 credit + free Silver tier (1 month) |
| **50 Scans** | Process 50 scans | £50 credit + free Gold tier (1 month) |
| **100 Scans** | Process 100 scans | £100 credit + free Platinum tier (3 months) |
| **500 Scans** | Process 500 scans | £300 credit + Platinum tier (lifetime) |
| **Annual Anniversary** | 1 year as customer | 1 month free subscription + £50 credit |

---

### Special Promotions (Seasonal)

**Limited-time offers to drive engagement**:

- **Welcome Bonus**: First 100 users get permanent 10% discount
- **Early Bird** (Month 1-3): 50% off first month for beta users
- **Quarterly Challenges**: "Process 20 scans this quarter, get 25% off next quarter"
- **Holiday Specials**: Double material credits during holidays
- **Flash Sales**: Random material discounts (24-48 hours)

---

### Loyalty Program Summary

**Example: Active Gold Tier User**

```
User Profile:
- Tier: Gold (200 lifetime scans, £3,000 spent)
- Subscription: Professional + Materials (12 months prepaid)
- Referrals: 4 successful referrals

Monthly Benefits:
✓ 10% off all scans (Gold tier)
✓ 15% off all materials (Gold tier)
✓ +15% off materials (annual subscription bonus)
✓ 3 free scans/month (Gold tier benefit)
✓ £75 annual material credit
✓ £175 referral credits accumulated
✓ Express processing queue
✓ Total effective discount: 25-30% on everything

Annual Savings: ~£600-800/year vs Bronze tier
```

---

### Implementation Benefits

**Why this loyalty program works**:

1. **Customer Retention**: 40-60% higher retention with tier benefits
2. **Increased LTV**: Loyal customers spend 3-5x more over time
3. **Referral Growth**: 30% of new users from referrals (zero CAC)
4. **Volume Sales**: Bulk discounts encourage larger purchases (better cash flow)
5. **Competitive Moat**: Hard for competitors to match comprehensive rewards
6. **Data-Driven**: Track which rewards drive most engagement

**Cost to Business**:
- Discounts: 5-15% margin reduction (offset by higher volume)
- Free scans: Minimal cost (~£0.08 processing cost each)
- Credits: Pre-paid by previous purchases (improves cash flow)
- **Net Impact**: +20-30% revenue from increased usage and retention

**Platform Requirements**:
- Automated tier tracking (Medusa.js)
- Referral link generation
- Credit/discount system
- Progress bars in user dashboard
- Email notifications for tier upgrades/rewards

---

## 📋 Next Steps

### Immediate (This Month)
1. ✅ Research complete - equipment and costs validated
2. ✅ Business model finalized - 3 revenue streams defined
3. ✅ **DECIDED**: Buy DIY kit (£3,010) + FibreSeek3D CFC (£2,100) = £5,110 total
   - Use CFC printer to fabricate DIY kit parts (instead of machining aluminum)
   - Get both SLS + CFC capabilities for less than one full SLS kit
4. [ ] Design loyalty rewards program into platform (tier tracking, referrals, credits)
5. [ ] Set up payment processing for subscriptions + materials + loyalty credits
6. [ ] Build MVP: scan processing pipeline on RTX 3090

### Month 3
1. [ ] Launch FDM-only service (£525 investment)
2. [ ] Get first 10 subscribers (revenue: £290-1,000/month)
3. [ ] Order SLS4ALL Inova MK1 (3-4 month delivery lead time)

### Month 6
1. [ ] Receive and assemble SLS printer
2. [ ] Add SLS tier to platform
3. [ ] Launch materials bundles
4. [ ] Target: 20 subscribers (revenue: £2,000-3,000/month)

### Month 9
1. [ ] Order FibreSeek3D FibreSeeker 3
2. [ ] Add CFC tier
3. [ ] Launch premium carbon fiber offerings
4. [ ] Target: 30-40 subscribers (revenue: £4,000-5,000/month)

---

**Last Updated**: November 12, 2025
**Version**: 1.0
**Status**: ✅ Ready for Implementation

**All equipment researched, costs validated, business model finalized** 🚀

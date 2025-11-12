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
- OctoPrint API for auto-queueing
- STL from COLMAP → Direct to print queue

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
| Item | Cost | Priority |
|------|------|----------|
| FibreSeek3D FibreSeeker 3 | £2,100 | Phase 1 (Month 6-9) |
| SLS4ALL Inova MK1 (Full Kit) | £5,450 | Phase 1 (Month 3-6) |
| SLS4ALL Inova MK1 (DIY Kit) | £3,010 | Alternative (save £2,440) |
| CNC Build (self-built) | £500-1,500 | Phase 2 (Month 9-12) |
| **Total (Full Kit path)** | **£8,050-9,050** | |
| **Total (DIY path)** | **£6,610-7,610** | |

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

### **Phase 1 Complete** (FDM + SLS, Month 6)
```
- Equipment: £3,010 (SLS DIY kit)
- Materials: £364 (combined stock)
- Platform: £375 (already paid)
TOTAL: £3,749
```

### **Full Suite** (FDM + SLS + CFC + CNC, Month 12)
```
- Equipment: £7,610 (SLS DIY + FibreSeek + CNC)
- Materials: £434 (full stock)
- Platform: £375 (already paid)
TOTAL: £8,419
```

---

## 🚀 Recommended Purchase Timeline

### **Phase 1: Launch (Month 1-3)** - FDM Only
**Investment**: £525
- Use existing FDM printers
- Scan processing subscriptions start
- Material sales (filament only)
- **Expected Revenue**: £840-1,200/month by Month 3

### **Phase 2: Add SLS** (Month 3-6)
**Investment**: £3,010 (DIY kit) or £5,450 (full kit)
- Purchase SLS4ALL Inova MK1
- Add PA12 nylon material sales
- Upgrade subscription bundles
- **Expected Revenue**: £2,500-3,500/month by Month 6

### **Phase 3: Add CFC** (Month 6-9)
**Investment**: £2,100
- Purchase FibreSeek3D FibreSeeker 3
- Add carbon fiber composite sales
- Premium tier becomes viable
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

## 📋 Next Steps

### Immediate (This Month)
1. ✅ Research complete - equipment and costs validated
2. ✅ Business model finalized - 3 revenue streams defined
3. [ ] Decide: DIY kit (£3,010) vs Full kit (£5,450) for SLS?
4. [ ] Set up payment processing for subscriptions + materials
5. [ ] Build MVP: scan processing pipeline on RTX 3090

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

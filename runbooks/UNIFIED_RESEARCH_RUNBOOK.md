# Unified Prospect Research Runbook

Takes a lead as input. Outputs a research profile with scoring, qualification, and outreach strategy.

**Feeds into:** [UNIFIED_OUTREACH_SEQUENCE.md](UNIFIED_OUTREACH_SEQUENCE.md)

**Combines:** LEADGEN3 weighted scoring (R1) + PROSPECT-ANALYSIS deep dive (R2) + RUNBOOK prospect research (R3)

---

## Inputs

```
- Contact Name
- Contact Email
- Contact Title
- Contact LinkedIn
- Company Name
- Company Website
- Industry
- Team Size
- HQ Location
- Source (ad, organic, referral, Sales Nav, etc.)
- Any initial context
```

---

## Phase 1: Quick Score (5 min)

Before doing any deep research, score the lead on available data. This determines whether to invest in a full deep dive.

### 1.1 - Weighted Scoring (/100)

Score each dimension using whatever data is available (Airtable fields, LinkedIn, website scan):

| Dimension | Weight | What to Score | Score /100 |
|-----------|--------|---------------|------------|
| **Company Fit** | 25% | Cross-border ops? Multi-currency? Multi-entity? Revenue $5M-$500M? Industry match? | |
| **Contact Access** | 20% | Decision maker (CFO/VP Finance/Treasurer)? Influencer? Wrong level? | |
| **Opportunity Quality** | 20% | Stated pain? Growth signals? Trigger events? Timing? | |
| **Competitive Position** | 15% | Treasury incumbent? Airwallex/Wise/Stripe? Banks only? Empty landscape? | |
| **Outreach Readiness** | 20% | Personalization anchors available? Multiple angles? Research depth possible? | |

**Weighted total = (Company Fit x 0.25) + (Contact Access x 0.20) + (Opportunity Quality x 0.20) + (Competitive Position x 0.15) + (Outreach Readiness x 0.20)**

### 1.2 - Classification

| Score | Priority | Action |
|-------|----------|--------|
| 70+ | **P1 - HIGH** | Full deep dive (Phase 2). Full escalation sequence (SDR + AE + Founder). |
| 50-69 | **P2 - MEDIUM** | Full deep dive (Phase 2). Standard sequence (SDR + AE only). |
| 35-49 | **P3 - NURTURE** | Skip deep dive. Light-touch SDR sequence only. Revisit if trigger event occurs. |
| <35 | **P4 - DISQUALIFY** | No outreach. Close lead. Document reason. |

**If P3 or P4: STOP HERE.** Do not invest in Phase 2 research.

---

## Phase 2: Deep Dive (30-45 min)

For P1 and P2 leads only. Do actual web research using WebSearch and WebFetch.

### 2.1 - Company Research

**Website Analysis:**
- Fetch homepage, /about, /services, /products
- What they do (one line)
- Business model (SaaS, services, marketplace, lending, etc.)
- Target customers
- Products/services offered
- Look for: cross-border operations, multi-currency mentions, international clients/suppliers, payment flows, treasury needs

**Web Search (run these 3 searches):**
1. `"[Company Name]" [country]` - basic info
2. `"[Company Name]" funding OR revenue OR growth OR expansion` - growth signals
3. `"[Company Name]" cross-border OR international OR payments OR currency` - Finmo-relevant signals

**Business Registry (if applicable):**
- Australia: ABN Lookup (abr.business.gov.au)
- Singapore: ACRA BizFile
- Philippines: SEC
- India: MCA

**Extract:**
- Recent news, funding, partnerships, expansion
- Revenue/growth trajectory
- Countries of operation and currencies
- Existing payment/treasury providers (Airwallex, Wise, Stripe, banks)

### 2.2 - Contact Research

**LinkedIn Profile:**
- Current title, tenure, career history
- Education, certifications
- Cross-border or payments/treasury experience

**Decision Authority:**
- Founder/CEO = decision maker
- CFO/VP Finance/Treasurer = economic buyer
- Director/Manager Finance = influencer/champion
- Other = may need to find the right person

**Career Pattern:**
- Finance/treasury background? (ideal)
- Operations/tech background? (needs different framing)
- Cross-border experience in career? (understands the problem)

**Venture Map (if multi-venture founder):**
- Map ALL connected ventures
- Which venture has strongest Finmo fit?
- The sign-up company may not be the best target

### 2.3 - Finmo Fit Assessment (/27)

Score each dimension 0-3 (0 = No need, 1 = Weak, 2 = Clear need, 3 = Strong/urgent):

| Dimension | Score (0-3) | Notes |
|-----------|-------------|-------|
| Cross-border payments | | Do they move money internationally? |
| Multi-currency | | 2+ currencies? |
| AR/AP | | Invoice clients or pay vendors? |
| Multi-entity | | Multiple legal entities? |
| Treasury visibility | | Need consolidated view across accounts? |
| Collections | | Receive international payments? |
| Payouts | | Pay international suppliers/partners? |
| Volume potential | | Estimated monthly volume? |
| Decision maker | | Is our contact the buyer? |

**Scoring:**
- 18+ = High priority (confirms P1/P2)
- 10-17 = Medium (may adjust classification)
- <10 = Low (consider downgrading to P3)

### 2.4 - Decision Maker Map

| Name | Title | Buying Role | Personalization Anchor | Priority |
|------|-------|-------------|----------------------|----------|
| | | Economic Buyer | | 1 |
| | | Executive Sponsor | | 2 |
| | | Champion/End User | | 3 |
| | | Technical Evaluator | | 4 |

**Buying roles:**
- **Economic Buyer:** Signs the check. Usually CFO/VP Finance/Treasurer.
- **Executive Sponsor:** CEO/MD who approves strategic spend.
- **Champion:** Daily user who will push internally. Usually Finance Manager/Controller.
- **Technical Evaluator:** CTO/IT who validates integration/security.

### 2.5 - BANT/MEDDIC Quick Assessment

| Dimension | Rating (A/B/C) | Evidence | Confidence |
|-----------|----------------|----------|------------|
| **Budget** | | Revenue, funding, investor pressure? | |
| **Authority** | | Is contact the buyer? | |
| **Need** | | Stated pain or structural need? | |
| **Timeline** | | Trigger event? Active search? | |

| Dimension | Rating (A/B/C) | Evidence |
|-----------|----------------|----------|
| **Metrics** | | What would they measure? (FX savings, time saved, visibility) |
| **Economic Buyer** | | Who signs? |
| **Decision Criteria** | | What matters to them? |
| **Decision Process** | | Who else is involved? |
| **Identify Pain** | | Confirmed or inferred? |
| **Champion** | | Who pushes internally? |

### 2.6 - Competitive Landscape

| Category | Current Solution | Confidence | Switching Cost |
|----------|-----------------|-----------|----------------|
| Banking | | | |
| Treasury/Cash Mgmt | | | |
| Payments | | | |
| Accounting/ERP | | | |
| FX | | | |

---

## Phase 3: Research Output

Compile everything into the research profile:

```markdown
# Prospect Research: [Contact Name] / [Company Name]

## Quick Score
- **Score:** X/100 (PX classification)
- **Finmo Fit:** X/27
- **Go/No-Go:** [Pursue / Nurture / Disqualify]

## Executive Summary
[3-5 sentences: Who they are, why they're a fit, what's the angle, what's the risk, what's the recommended action. This should be the ONLY thing a busy AE needs to read.]

## Company Profile
[From 2.1]

## Contact Profile & Decision Maker Map
[From 2.2 + 2.4]

## Fit Assessment
- **Finmo Fit:** X/27
- **BANT:** X
- **MEDDIC Completeness:** X%

## Angles & Personalization
- **Primary angle:** [The ONE strongest angle]
- **Secondary angle:** [Backup]
- **Personalization anchors:** [3-5 specific details for content creation]
- **Competitors detected:** [If any]

## Red Flags
- [Risk 1]
- [Risk 2]

## Recommended Outreach Strategy
- **Sequence tier:** [Full escalation (SDR+AE+Founder) / Standard (SDR+AE) / Light-touch (SDR only)]
- **Starting framework:** [C3 Discovery / C4 Direct / C5 Founder]
- **Primary channel:** [Email / LinkedIn / WhatsApp]
- **Expected timeline:** [X months to meeting/deal]
```

---

## Finmo Capabilities Reference

| Capability | What It Does |
|------------|-------------|
| Connected Dashboard | Unified view across all banks, accounts, entities |
| Cash Visibility | Real-time aggregated balances across entities, currencies |
| Cash Forecasting | AI-powered forecasting, scenario modeling, surplus/shortfall alerts |
| AR/AP Automation | Invoice tracking, payment execution, approval workflows, maker-checker |
| Multi-Entity Hierarchy | Parent-child org structure, role-based access, consolidated view, single login |
| Global Payments | Collections in 30+ currencies, payouts to 180+ countries |
| Currency Accounts | Local accounts to receive payments in foreign currencies |
| FX | Real-time rates, hedging strategies |
| Working Capital | Idle cash investment, liquidity management |
| Security | SOC 2 Type II, ISO 27001, PCI-DSS |

---

## APAC Market Context

When researching APAC prospects, consider these structural tailwinds (from APAC_TREASURY_MARKET_THESIS.md):

1. **Friendshoring/Supply Chain Diversification** - $235B FDI into ASEAN (2024), outpacing China
2. **Data Center Infrastructure Boom** - $50B+ investment wave across MY, SG, ID, TH
3. **EV Supply Chain Transition** - New supplier ecosystems across TH, ID, MY
4. **Agricultural/Commodity Supply Chain** - Millions of smallholders, ESG mandates
5. **Semiconductor Packaging** - $20B+ in Penang/Kulim, Singapore
6. **Conglomerate Treasury Modernization** - S/4HANA migrations = natural entry point

Use these to inform outreach angles when the prospect operates in affected industries.

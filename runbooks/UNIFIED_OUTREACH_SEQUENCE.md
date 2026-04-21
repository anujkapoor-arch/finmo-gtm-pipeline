# Unified Outreach Sequence: SDR -> AE -> Founder

**Input:** Research profile from [UNIFIED_RESEARCH_RUNBOOK.md](UNIFIED_RESEARCH_RUNBOOK.md)

**Combines:** C3 (Conversational), C4 (Direct), C5 (CEO Direct), Leadfeeder/SalesHandy formulas (PAS, BAB, Relevant Question, Up to You), David Hanna real conversation patterns

---

## Architecture

Three-tier escalation across 35 days. Each tier has a different sender, tone, and goal. The escalation itself is a signal to the prospect that they matter.

**Key design principle: SHUFFLE FORMULAS across tiers.** SDRs use selling formulas (BAB). AEs use discovery formulas (Pattern Share). No two consecutive emails use the same approach. The prospect should never see a pattern.

```
TIER 1: SDR (Days 1-13)          TIER 2: AE (Days 16-25)         TIER 3: FOUNDER (Days 28-35)
Mix of discovery + selling        Mix of selling + discovery       Personal. Unstructured.
Hypothesis, BAB, Referral,        PAS, Pattern Share,              "My team flagged you."
Open Door                         Relevant Question, Up to You     Coffee, not demo.
```

### Sequence by Lead Score

| Lead Score | Sequence |
|------------|----------|
| P1 (70+) | Full escalation: SDR -> AE -> Founder |
| P2 (50-69) | Standard: SDR -> AE only |
| P3 (35-49) | Light-touch: SDR only (3 emails + CR) |

### Formula Shuffle Map

| Email | Sender | Formula | Type |
|-------|--------|---------|------|
| 1 | SDR | Pain Hypothesis (Style A) | Discovery |
| 2 | SDR | **BAB** | **Selling** |
| 3 | SDR | Referral/Right Person (Style B) | Social proof |
| 4 | SDR | Open Door | Zero pressure |
| 5 | AE | **PAS** | **Selling** |
| 6 | AE | **Pattern Share** | **Discovery** |
| 7 | AE | Relevant Question | Value-first |
| 8 | AE | Up to You | Zero pressure |
| 9 | CEO | Personal reach-out | Relationship |
| 10 | CEO | Value drop | Insight |

**Pattern: Discovery -> Selling -> Social Proof -> Pause -> Selling -> Discovery -> Value -> Pause -> Personal -> Insight. Every email zig-zags.**

---

## Global Rules (Apply to ALL Content)

### Writing
- No em dashes (use hyphens)
- No emojis (except thumbs-up reaction on WhatsApp)
- No banned AI words: leverage, comprehensive, robust, seamless, cutting-edge, innovative, synergy, streamline, optimize, utilize, facilitate, enhance, foster, delve, navigate (metaphorical), excited to, it's worth noting
- No "I hope this finds you well" or any variation
- No "I'd love to explore synergies"
- No "We help companies like yours"
- No "In today's fast-paced..."
- Contractions always (I'm, you're, they've, wouldn't)
- Sentence fragments are fine
- Starting with "And", "But", "So" is fine
- Sound like you'd actually say this at a networking event (cocktail party test)

### Banned Email Openings

These phrases scream "AI-generated cold email." Never use them as openers:

**Kill list:**
- "Still thinking about..."
- "Following up on..."
- "I've been talking to..."
- "One pattern that keeps coming up..."
- "Two patterns keep coming up..."
- "I keep seeing..."
- "I keep hearing from..."
- "Interesting trend:..."
- "Quick follow-up on..."

**Use instead:**
- Open with a specific fact or number about their company: "Four countries. Four currencies. $48M in structured financing."
- Open with a what-if: "What if [Company]'s finance team could see cash across all entities from a single login?"
- Open with what you do in one line: "I work with Group CFOs at multi-country manufacturers who've outgrown the three-tool stack."
- Open with a direct statement about their setup: "[Company] pays staff in five currencies but bills clients in two. The gap between those is where margin hides."
- Open with one person's words: "A CFO at a 200-person BPO told me something that stuck:"

**Each email must stand alone.** No callbacks to prior emails ("as I mentioned", "following up on my earlier note", "still thinking about"). If a prospect only reads one email, it should make complete sense on its own.

### Formatting
- HTML: use `<br><br>` NOT `<p>` tags
- Subject lines: 2-5 words, lowercase, company-specific. Anchor to concrete outcomes (real-time cash, one platform, 13-week forecast) not internal jargon (consolidation gap, visibility lag, treasury stack).
- LinkedIn CR: under 300 characters
- One question OR one CTA per message (never both, never multiple)

### Sender Variable

**CRITICAL: `{{sender_first_name}}` is for SIGN-OFFS and SENDER references ONLY.** Never use it in the greeting/salutation line. Greetings must always use the recipient's actual first name (e.g., "Hi David," not "Hi {{sender_first_name}},"). This is a common AI generation error - always verify.

All email, LinkedIn, AND WhatsApp bodies MUST use `{{sender_first_name}}` everywhere a sender name appears. This includes:
- Email sign-offs (end of body)
- CEO/Founder LinkedIn messages (custom_linkedin3)
- CEO/Founder WhatsApp messages (whatsapp_ceo_1)
- CEO email bodies (email9_body, email10_body) - both inline mentions AND sign-offs

**Never hardcode** "David", "David Hanna", "David from Finmo", "David here, CEO", "it's David (CEO)", etc. Always use `{{sender_first_name}}`.

Exception: Email 1 may be left unsigned (raw hypothesis, no sign-off).

### Respectful Opt-Out

**No opt-out on Email 1 or Email 2.** The first two emails earn the right to exist through specificity and research, not through an escape hatch. Adding opt-out too early signals low confidence.

**From Email 3 onward:** Include a short, varied opt-out line. It must be:
1. Separated from the email body with `<br><br>` so it visually sits at the bottom, not part of the content
2. Different phrasing on every email - never repeat the same opt-out line
3. Short - one line, not a paragraph

**Opt-out variations (E3+):**

| Email | Opt-Out Variation |
|-------|-------------------|
| Email 3 (SDR) | "Not relevant? Just say 'pass' - no hard feelings." |
| Email 4 (SDR) | *(Open Door email - the whole email IS the opt-out, so no extra line needed)* |
| Email 5 (AE) | "If I'm way off, reply 'pass' and I'll know." |
| Email 6 (AE) | "If this isn't your world, just say so." |
| Email 7 (AE) | *(Relevant Question - ends with walkthrough ask which is soft enough)* |
| Email 8 (AE) | *(Up to You - ends with "if not, I totally understand" which serves as opt-out)* |
| Email 9 (CEO) | *(Personal reach-out - no opt-out needed, CEO tone is already soft)* |
| Email 10 (CEO) | "No pressure either way." *(already present, sufficient)* |

**LinkedIn messages:** Add opt-out only on the last message in each tier. Keep it casual: "If this isn't on your radar, totally fine - just lmk and I'll stop pinging."

**Placement:** Always the LAST line before the sender name. Never bury it in the middle. Always separated from the body with `<br><br>`.

### Channels
- **Email:** Primary channel. Formal enough for cold outreach, trackable.
- **LinkedIn:** Secondary. CR first, then messages after acceptance. More casual tone. "btw", "lmk" okay here.
- **WhatsApp:** Personal channel. Acknowledge the awkwardness. Reference prior touches. Short bursts, not blocks.

### WhatsApp Rules (SDR + AE)

WhatsApp is a personal channel. You must earn the right to be there. Every SDR/AE WhatsApp MUST:
1. Acknowledge that messaging a stranger on WhatsApp is unusual
2. Reference a prior touch (email, LinkedIn) so it doesn't feel cold
3. Send as 2 separate short messages, not one block
4. Never ask business questions a stranger wouldn't answer
5. Keep it about flagging the email, not re-pitching

**SDR/AE WhatsApp pattern:**
```
Message 1:
Hi [First Name], totally get it if WhatsApp from a stranger is weird - just figured this is faster than waiting for email to land.

Message 2:
This is {{sender_first_name}} from Finmo. Dropped you an email earlier about something I noticed about [Company]'s [specific detail - e.g., "4-country finance setup"]. Just wanted to make sure it didn't land in spam.
```

**CEO WhatsApp pattern is different** - 3 short bursts, personal tone, "my team flagged you" framing. See Tier 3.

### Variety (Tool Shed - Paul Castain)
No two consecutive touches should use the same approach. Rotate across:
- Hypothesis + question
- Aspiration / before-after (BAB)
- Social proof / referral
- Pattern / industry insight
- Free tips / value-first
- Zero pressure / "up to you"
- Observation (no question, no CTA)
- Personal reach-out

---

## Finmo Positioning (Use in All Content)

Finmo is a **treasury management platform with embedded payments** - not just an FX tool or a payments gateway.

### What Finmo Does (Full Capability Set)
- **Cash visibility:** Real-time aggregated balances across all banks, accounts, entities, currencies from a single login
- **Cash forecasting:** 13-week AI-powered forecasting, scenario modeling, surplus/shortfall alerts
- **AR/AP automation:** Invoice tracking, payment execution, approval workflows, maker-checker
- **Multi-entity hierarchy:** Parent-child org structure, role-based access, consolidated view
- **Collections:** Receive payments in 30+ currencies via local accounts
- **Payouts:** Send money to 180+ countries - same-day in many markets
- **FX:** Mid-market rates, not bank retail rates
- **Reconciliation:** Automated matching across accounts and entities
- **Security:** SOC 2 Type II, ISO 27001, PCI-DSS

### Category Framing (Use in Emails)
- **Primary:** "Treasury with payments built in, not bolted on"
- **Alternative:** "One platform instead of three" (replacing bank + FX broker + spreadsheet)
- **For scale-ups:** "A modern alternative to legacy TMS - live in weeks, not quarters"
- **Category name:** "Payments-led treasury" or "TMS-Lite"

### Competitive Positioning (Without Naming Competitors)
Use these framings to plant Finmo's position without attacking anyone:
- vs payments-only tools (Airwallex/Wise/Stripe): "You've probably outgrown a payments-only tool. What's missing is the treasury layer."
- vs legacy TMS (Kyriba/TreasuryXpress): "Built for scaleups, not enterprises. Live in weeks, not quarters."
- vs banks: "Mid-market FX rates, not retail. One dashboard, not four portals."
- vs Trovata: "Similar cash visibility, but we also execute payments. One platform, not two."
- vs spreadsheets: "Your Monday morning cash picture takes seconds, not hours."

### Money Movement Angle
Finmo is licensed for money movement. When relevant, explore whether the prospect needs:
- To **collect** from international clients without managing separate bank accounts per country
- To **pay** suppliers, staff, or partners across borders from one platform
- To **replace** their current multi-bank, multi-broker setup with a single system

Frame as: "See where your cash is, move it where it needs to go, and forecast what's coming - all from one login."

---

## Market References (from APAC Treasury Market Thesis)

Use real companies and metrics to agitate problems and show market momentum. These are NOT Finmo customers - they illustrate the scale of the treasury challenge:

**Companies by industry:**
- **BPO/Outsourcing:** Astra International ($20-22B revenue, 200K+ employees), CP Group ($80-90B, 400K+ employees)
- **Manufacturing:** Samsung Vietnam ($55-65B exports/yr), Foxconn Vietnam ($5-10B invested), Intel Malaysia ($7B+)
- **Agribusiness/FMCG:** Wilmar ($67B, 500+ plants, 50+ countries), Olam ($36B, 5M+ smallholder farmers)
- **Conglomerates:** San Miguel, Ayala, SM Investments, JG Summit, Sime Darby - active S/4HANA migrations
- **Telco/Infra:** Singtel/Nxera (multi-billion data center), Telkom Indonesia ($2B+ buildout)

**Key stats:**
- $235B FDI into ASEAN in 2024 (outpaced China for first time)
- $50B+ data center investment pipeline across SEA
- 9+ major enterprises on active S/4HANA migrations in SEA
- Typical FX leakage: 1-2% on bank conversions
- $800B+ combined revenue across top 15 SEA conglomerates

**How to use:** "Companies like Astra International and CP Group are investing in treasury platforms to manage exactly this kind of multi-country complexity." Not a claim they use Finmo - a claim the problem is real and the market is moving.

---

## TIER 1: SDR (Days 1-13)

**Sender:** SDR (Harini, Sukriti, or assigned rep)
**Tone:** Mix of curious peer AND light selling. Not all discovery - throw in a BAB.
**Goal:** Get a response. Map pain. Qualify for AE escalation.
**Word limit:** 40-130 words (varies by formula - hypothesis emails are short, BAB is longer)

---

### Day 1: Email 1 - Pain Hypothesis (Style A)

*Specific, researched, hypothesis-driven. Shows you did the homework. No product mention. No opt-out.*

**Structure:**
- One specific observation about their business (10-15 words)
- Your hypothesis framed as a guess: "I'd bet..." / "That's a lot of..." (15-20 words)
- One easy-to-answer question (10-15 words)

**Template:**
```
Subject: [2-4 word company-specific hook, lowercase]

Hi [First Name],<br><br>

[Specific observation - something only true for them at this company right now. Open with facts or numbers, NOT "I've been talking to..." or "Still thinking about..."].<br><br>

[Hypothesis about their pain, framed around managing multiple disconnected tools or lack of a single view across entities].<br><br>

[One question they can answer in a sentence.]
```

**Quality check:** Could you swap in a competitor's name and this email still works? If yes, it's too generic. Rewrite.

---

### Day 1: LinkedIn Connection Request

**Goal:** Get accepted by offering value. Content-offer approach.

**Template:**
```
Hi [First Name], great to e-meet you! I put together a short guide on how [their company type] running [X]+ currencies handle treasury and payments from one platform instead of three. Thought it might be useful given [Company]'s setup. Want me to send it over?
```

---

### Day 2: WhatsApp (SDR)

**Message 1:**
```
Hi [First Name], totally get it if WhatsApp from a stranger is weird - just figured this is faster than waiting for email to land.
```

**Message 2:**
```
This is {{sender_first_name}} from Finmo. Dropped you an email earlier about something I noticed about [Company]'s [specific detail - e.g., "4-country finance setup"]. Just wanted to make sure it didn't land in spam.
```

---

### Day 5: Email 2 - BAB (Before-After-Bridge)

*Aspiration-driven. Selling formula used by SDR - breaks the "SDR = only discovery" pattern. No opt-out.*

**Structure:**
1. **Before:** Open with a what-if about their specific situation (single login, one platform)
2. **Social proof:** Reference a similar company's result - frame around platform consolidation, not just FX savings
3. **Bridge:** Finmo as treasury with payments built in - collections, payouts, visibility in one system
4. **CTA:** Walkthrough ask

**Template:**
```
Subject: [aspiration hook anchored to concrete outcome, 3-5 words lowercase]

Hi [First Name],<br><br>

What if [lead's company]'s finance team could [see cash across all X countries / pay suppliers and collect from clients in X currencies / forecast the next 13 weeks] - from a single login? No separate bank portals, no FX broker, no spreadsheets stitching it together.<br><br>

A [similar company description] made that switch. They went from [their "before" state - multiple tools, manual processes] to one platform that handles treasury and payments together. [One specific result with numbers - frame around time saved or operational improvement, not just FX savings].<br><br>

Finmo is a treasury management platform with payments built in - cash visibility, forecasting, reconciliation, collections in 30+ currencies, and payouts to 180+ countries. One system instead of three.<br><br>

Worth a quick walkthrough next week?<br><br>

{{sender_first_name}}
```

---

### Day 7: LinkedIn Message 1 - Observation, No Question

*Tool Shed variety: plant a seed. No ask.*

**Template:**
```
[One specific observation about their company's multi-country/multi-currency setup. Connect it to the "three disconnected tools" problem. No question, no CTA. Just a thought that sticks.]
```

---

### Day 10: Email 3 - Referral / Right Person (Style B)

*Social proof driven. Scalable formula. Completely different tone from Emails 1 and 2. First email with opt-out.*

**Structure:**
- What you do + who you help (one line) - frame around treasury-with-payments, not just visibility
- Similar company reference + result
- Connect to their company
- Walkthrough ask
- Separated opt-out

**Template:**
```
Subject: [industry problem at scale, 3-5 words]

Hi [First Name],<br><br>

I work with [role] teams at [their type of company] who've outgrown the bank-plus-broker-plus-spreadsheet setup and need treasury and payments in one place.<br><br>

Companies running [X]+ currencies across [region] switched from that three-tool stack to a single platform - cash visibility, 13-week forecasting, automated reconciliation, and cross-border payments all in one system. No months-long implementation like a legacy TMS. Live in weeks.<br><br>

That's why I thought of [lead's company] with [their specific setup]. Would you be open to a short walkthrough?<br><br>

Not relevant? Just say "pass" - no hard feelings.<br><br>

{{sender_first_name}}
```

---

### Day 13: Email 4 - Open Door

*Zero pressure. Acknowledges you might be wrong. Resets the conversation. No opt-out needed - the whole email IS the opt-out.*

**Template:**
```
Subject: wrong question maybe

Hi [First Name],<br><br>

Totally possible the treasury and payments angle isn't the thing keeping you up at night. With [their specific context - growth, M&A, expansion], the biggest headache might be something completely different.<br><br>

What's actually the toughest operational finance challenge on your plate right now?<br><br>

{{sender_first_name}}
```

---

### Day 14: SDR Decision Point

**Reply (positive):** SDR warms intro to AE.
**Reply (negative/not now):** Nurture list. Quarterly check-in.
**No reply + P1/P2:** Escalate to Tier 2 (AE takes over).
**No reply + P3:** Nurture. Stop sequence.

### SDR-to-AE Handoff (if prospect replied)

```
[First Name], wanted to connect you with [AE Name] on our team. [He/She] works directly with [companies in their industry] and can get more specific about [the thing they expressed interest in].

[AE Name] will reach out - I'll let them take it from here.
```

---

## TIER 2: AE (Days 16-25)

**Sender:** AE (Account Executive)
**Tone:** Mix of direct selling AND discovery. Not all PAS - throw in a Pattern Share.
**Goal:** Present value, quantify ROI, book a demo or call.
**Product mention:** YES - Finmo named in most emails. Exception: Pattern Share (Email 6).
**Word limit:** 80-165 words (varies by formula - PAS is tighter, Relevant Question is longer).

---

### Day 16: Email 5 - PAS (Problem-Agitate-Solve)

*Pain-first. Structured sales argument. Frame the problem around the three-tool stack, not just FX. Solve with payments-led treasury.*

**Structure:**
1. **Problem:** Direct statement about their specific operational gap (managing three disconnected tools)
2. **Agitate:** What that costs in time, money, or risk - be specific to their setup
3. **Solve:** Finmo as treasury with payments built in - ONE capability, not a feature list
4. **CTA:** Specific day/time ask

**Template:**
```
Subject: [3-5 word problem-specific hook]

Hi [First Name],<br><br>

[Direct statement about their setup - e.g., "Most [company type] your size end up with three separate tools: a bank for payments, a spreadsheet for cash visibility, and maybe an FX broker for conversions. None of them talk to each other."]<br><br>

[Agitate: what that gap costs them specifically. Time, money, risk. Use their numbers/context.]<br><br>

Finmo is treasury with payments built in, not bolted on. [One specific capability that maps to their pain - e.g., "One login, real-time cash positions across all entities, collections in 30+ currencies, payouts to 180+ countries, and mid-market FX."]<br><br>

Worth 15 minutes to see if it fits [Company]'s setup?<br><br>

If I'm way off, reply "pass" and I'll know.<br><br>

{{sender_first_name}}
```

---

### Day 17: WhatsApp (AE)

**Message 1:**
```
Hi [First Name], apologies for the cold WhatsApp - just figured this is quicker than email.
```

**Message 2:**
```
This is {{sender_first_name}} from Finmo. My colleague [SDR Name] reached out last week about [Company]'s [specific setup]. Wanted to share one thing: [specific insight relevant to their setup]. Happy to show you the details if that's interesting.
```

---

### Day 20: Email 6 - Pattern Share (Discovery)

*SDR-style discovery move used by AE. Breaks the selling pattern. Prospect expects another pitch after Email 5 - gets a peer-level observation instead. No product mention.*

**Template:**
```
Subject: [observation hook, 3-4 words]

Hi [First Name],<br><br>

[One industry observation - something ironic, unexpected, or contrarian about their type of company and how they handle treasury/payments. NOT "I keep seeing..." or "One pattern that keeps coming up..." - just state the observation directly].<br><br>

[Connect it to their specific situation in one sentence].<br><br>

Does that ring true, or have you already sorted it internally?<br><br>

If this isn't your world, just say so.<br><br>

{{sender_first_name}}
```

---

### Day 21: LinkedIn Message 2 - Market Trend

**Goal:** Share a market reference. No direct pitch.

```
[First Name] - [relevant market insight from thesis or a specific observation about their industry]. Curious if [their company] is seeing the same pressure on the finance side.
```

---

### Day 22: Email 7 - Relevant Question (Free Value)

*Gives 2 actionable tips. The prospect gets real value whether they respond or not.*

**Structure:**
1. Open with what they can achieve - frame around one-platform consolidation
2. Acknowledge they're busy
3. 2 specific, actionable tips they can implement right away
4. Offer Finmo as the shortcut
5. Low-commitment CTA

**Template:**
```
Subject: [value hook, 3-5 words]

Hi [First Name],<br><br>

Two things your finance team can do this week without buying anything:<br><br>

1. [Specific actionable tip with a number/metric. Something they can do tomorrow. E.g., "Run a one-time FX audit - compare your bank's conversion rates to mid-market on the same days. Most companies running X+ currencies find a 1-2% gap."]<br><br>

2. [Second tip, different angle. Also actionable and free. E.g., "Time your payroll conversions. Shifting from reactive to planned conversions 3 days before payroll saves 0.5-1% per batch."]<br><br>

Both of these are things Finmo automates - plus [one additional capability relevant to them: same-day payouts / collections in 30+ currencies / 13-week forecasting]. But the audit alone is worth doing regardless.<br><br>

Want help running the numbers? 15 minutes and I can walk you through it.<br><br>

{{sender_first_name}}
```

---

### Day 25: Email 8 - Up to You (Zero Pressure Close)

*No meeting ask. Gives value, teases more, hands control to the prospect. After 3 AE emails of varying intensity, this one backs off completely.*

**Structure:**
1. How you found them
2. 2 specific observations/numbers
3. Tease a third
4. "Want me to send it? If not, no hard feelings."

**Template:**
```
Subject: [2 things about company's specific area]

Hi [First Name],<br><br>

Two things I noticed researching [lead's company]'s setup:<br><br>

1. [Specific observation with a number - something they can verify independently. Frame around time or operational cost, not just FX.]<br><br>

2. [Second observation, different angle, also with a number. Frame around the one-platform benefit.]<br><br>

There's a third one around [related topic - e.g., "how 13-week cash forecasting changes the conversation with your board"], but I don't want to overwhelm you. If the first two are useful, want me to send the third?<br><br>

If not, totally fine. No hard feelings.
```

---

### Day 25: AE Decision Point

**Reply (positive):** Book demo/call.
**Reply to "Up to You" ("yes send the third"):** Send third tip + transition to call.
**No reply + P1:** Escalate to Founder.
**No reply + P2:** Nurture. Stop sequence.

### AE-to-Founder Handoff (internal)

```
[Company] is a P1 lead. [One line on why they're interesting]. SDR ran 4 touches, I ran 4 - no response but the fit is strong. Can you send a personal note? Their [contact title] is [name]. [One personalization anchor].
```

---

## TIER 3: Founder/CEO Direct (Days 28-35)

**Sender:** CEO / Founder (David Hanna or equivalent)
**Tone:** Busy founder who saw something interesting. Personal, not templated.
**Goal:** Differentiate. Get an in-person meeting or call. "Coffee" not "demo."
**Product mention:** Company name yes, product pitch no. "We work with..." not "Finmo does X."
**Word limit:** Under 50 words per email.
**Framework:** Modeled on real CEO conversation that converted. The prospect said: "It was highly unusual to get a direct contact with a CEO. Hence my response to you."

**CEO WhatsApp is different from SDR/AE** - no need to acknowledge awkwardness. CEO reaching out directly IS the hook. 3 short bursts, personal tone.

---

### Day 28: Email 9 - The Personal Reach-Out

**Rules:**
- Reference "my team" to explain why CEO is reaching out
- Mention something specific about their business
- Use "treasury and payments" category framing naturally
- "Coffee or a call" CTA, not a demo
- Include a personal detail (location, travel, something real)
- Sign with first name only

**Template:**
```
Subject: [first name] - quick note

Hi [First Name],<br><br>

[Your name] here, [title] at Finmo. My team flagged [their company] and I took a look - [one specific observation about their business].<br><br>

We built Finmo for exactly that - treasury and payments in one platform, not three separate tools. Would be good to compare notes over a call or coffee [personal detail].<br><br>

[First name]
```

---

### Day 28: WhatsApp (CEO) - 3 short bursts

**Message 1:**
```
Hi [First Name], it's [CEO Name] ([Title]) from Finmo.
```

**Message 2:**
```
[One line about why their company is interesting. Keep it genuine.]
```

**Message 3:**
```
Would be great to connect and understand more about your business and how we can help (potentially). Happy to jump on a call or come to you.
```

---

### Day 33: Email 10 - The Value Drop

**Template:**
```
Subject: Re: [first name] - quick note

[First Name],<br><br>

[One specific insight with a number relevant to their type of company. Frame around the cost of running three disconnected tools or the operational benefit of consolidation. NOT "one thing I keep hearing from..." - just state the insight directly.]<br><br>

Happy to share how we've helped similar setups if useful. No pressure either way.<br><br>

[First name]
```

---

### Day 35: LinkedIn Message 3 (Final)

```
[First Name] - {{sender_first_name}} from Finmo. My team has been following [their company] for a while. Your [specific detail] is impressive. Would love to connect and compare notes on how treasury and payments are converging for [companies their size/type].
```

---

### Day 35: End of Sequence

**If response:** Meeting booked.
**If no response:** Quarterly nurture list. Calendar reminder 90 days. Re-engage on trigger event (funding, expansion, new hire, news).

---

## Full Sequence Calendar

**LinkedIn CR goes FIRST.** The connection request is the gate. Email starts only after a 7-day buffer to allow acceptance. If not accepted after 7 days, view their profile (triggers a notification) and wait another 7 days before starting email.

**Why CR first:** LinkedIn messages only work if connected. Sending emails before knowing if the CR was accepted wastes the LinkedIn channel. By leading with CR, we get 7 days of passive visibility (they see who viewed/requested) before the first email lands.

| Day | Channel | Sender | Formula | What Happens | System |
|-----|---------|--------|---------|-------------|--------|
| 0 | **LinkedIn CR** | SDR | Content-offer | Send CR. This is Day 0 - everything else is relative to this. | SmartReach |
| 7 | **Check** | SDR | - | **If CR accepted:** proceed to Day 8. **If not:** view profile, wait 7 more days. | SmartReach/Manual |
| 8 | Email 1 | SDR | Pain Hypothesis | First email. They may have seen your profile/CR already. | SmartReach |
| 9 | WhatsApp x2 | SDR | Intro bursts | "Sent you an email..." | Unipile |
| 10 | LinkedIn Msg 1 | SDR | Observation (no ask) | Only if CR accepted. Otherwise skip. | SmartReach |
| 12 | Email 2 | SDR | **BAB (aspiration)** | Selling formula from SDR | SmartReach |
| 17 | Email 3 | SDR | **Referral/Social Proof** | Different tone | SmartReach |
| 20 | Email 4 | SDR | Open Door | Zero pressure | SmartReach |
| 21 | ─── | **SDR DECISION POINT** | ─── | Reply -> AE handoff. No reply + P1/P2 -> escalate to AE. P3 -> stop. | ─── |
| 23 | Email 5 | AE | **PAS (pain)** | New sender, selling | SmartReach |
| 24 | WhatsApp x2 | AE | Direct + number | Reference SDR | Unipile |
| 27 | Email 6 | AE | **Pattern Share** | Discovery from AE | SmartReach |
| 28 | LinkedIn Msg 2 | AE | Market trend | Only if connected | SmartReach |
| 29 | Email 7 | AE | **Relevant Question** | Free value | SmartReach |
| 32 | Email 8 | AE | **Up to You** | Zero pressure | SmartReach |
| 32 | ─── | **AE DECISION POINT** | ─── | Reply -> demo. No reply + P1 -> escalate to CEO. P2 -> nurture. | ─── |
| 35 | Email 9 | CEO | **Personal reach-out** | Status signal | SmartReach |
| 35 | WhatsApp x3 | CEO | Short bursts | Personal | Unipile |
| 40 | Email 10 | CEO | **Value drop** | Insight | SmartReach |
| 42 | LinkedIn Msg 3 | CEO | Final connection | Only if connected | SmartReach |

**20 touchpoints. 42 days. 3 senders. 3 channels. LinkedIn CR gates the sequence.**

### LinkedIn CR Not Accepted Flow

If the CR is not accepted after Day 7:

| Day | Action | System |
|-----|--------|--------|
| 7 | CR not accepted -> View their profile (triggers LinkedIn notification) | SmartReach/Manual |
| 14 | Still not accepted -> Start email sequence anyway (Day 8 flow). Skip all LinkedIn message steps. | SmartReach |

The email sequence runs regardless after Day 14 max wait. LinkedIn messages are conditional on connection status.

---

## Content Quality Checklist

Before any content ships, verify:

- [ ] No two consecutive emails use the same formula
- [ ] SDR uses at least one selling formula (BAB)
- [ ] AE uses at least one discovery formula (Pattern Share)
- [ ] Subject line: 2-5 words, lowercase, company-specific, anchored to concrete outcomes
- [ ] First line: specific enough it only works for THIS person at THIS company
- [ ] No banned openings ("still thinking about", "following up on", "I've been talking to", "one pattern")
- [ ] One question OR one CTA per message (not both)
- [ ] No banned words (see list above)
- [ ] No em dashes, no emojis, no "Best,/Cheers,/Regards,"
- [ ] `{{sender_first_name}}` used for all sign-offs AND LinkedIn messages (no hardcoded "David from Finmo")
- [ ] No opt-out on Email 1 or Email 2
- [ ] Opt-out on E3+ is separated from body with `<br><br>` and varies per email
- [ ] LinkedIn CR under 300 characters, uses content-offer template
- [ ] SDR/AE WhatsApp acknowledges the awkwardness + references prior email
- [ ] CEO WhatsApp uses 3 short bursts with "my team flagged" framing
- [ ] Cocktail party test: read it out loud - would you say this in person?
- [ ] Specificity test: could you swap in a competitor's name? If yes, rewrite
- [ ] HTML uses `<br><br>` not `<p>` tags
- [ ] Each escalation references prior sender or "my team"
- [ ] "Payments-led treasury" or "one platform" framing used at least once in the sequence
- [ ] Money movement (collections/payouts) mentioned at least once in the sequence

---

## Competitor Response Framework

If a competitor surfaces at any stage:

1. **Acknowledge** - "Good to know [Competitor] is in the mix" (1 line)
2. **Differentiate** - State what Finmo has, don't attack competitor (2-3 lines, facts only)
3. **Ask** - "What matters most to you in this decision?" (1 question)
4. **Propose** - Short call to compare. "If they're genuinely better for your setup, I'll tell you that."

| Competitor | Finmo Differentiators |
|------------|----------------------|
| **Airwallex** | Airwallex is a payments platform. Finmo is a treasury platform with payments built in. No cash forecasting, no treasury workflows, no multi-entity hierarchy in Airwallex. |
| **Wise** | Wise handles FX transfers well but lacks cash visibility, forecasting, reconciliation. When you need a single pane of glass across 10+ bank accounts, Wise doesn't scale. |
| **Stripe** | Stripe collects payments. Finmo manages your entire cash position. Stripe is a revenue collection layer, not a treasury layer. For finance teams, not engineering teams. |
| **Trovata** | Both do cash visibility well. Finmo adds instant payouts, cross-border payments, automated reconciliation. One platform, not two. |
| **Kyriba/TreasuryXpress** | Built for scaleups, not enterprises. Live in weeks, not quarters. No 6-month implementation. |
| **Local banks** | 1-2% FX markup vs mid-market rates. No real-time visibility. No multi-entity consolidated view. Manual everything. |

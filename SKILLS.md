# Snowdrop Skill Catalog

## Executive Summary

Snowdrop's complete MCP skill catalog — 667+ skills across 150+ categories, callable from any MCP-compatible client (Claude Code, Cursor, custom agents). Skills span financial compliance, blockchain analytics, fund accounting, engagement automation, and real-time documentation lookup. Snowdrop is **freemium**: a large core of utility and infrastructure skills is open to everyone; the top-tier compliance and financial analytics tools require a premium subscription (coming soon at [snowdrop.ai](https://snowdrop.ai)).

## Table of Contents

- [Tier System](#tier-system)
- [How Skills Work](#how-skills-work)
- [Full Catalog](#full-catalog)
- [Engagement Infrastructure Skills](#engagement-infrastructure-skills)
- [Documentation Skills](#documentation-skills)
- [Contributing](#contributing)

---

## Tier System

Snowdrop MCP is **freemium**. Every skill is either **Free** or **Premium** — there is no middle ground.

| Tier | Access | Code | Call Result |
|------|--------|------|-------------|
| **Free** | All MCP clients, no signup | Public on GitHub | Full response |
| **Premium** | Subscribers only (coming soon) | Private repo only | `{"status": "payment_required", ...}` |

Premium skills appear in `tools/list` with their full name, description, and parameter schema so developers can evaluate the interface before subscribing. Calling a premium skill returns a `payment_required` response pointing to [snowdrop.ai](https://snowdrop.ai).

**Subscribe:** [https://snowdrop.ai](https://snowdrop.ai) (launching soon)

### Current Premium Skills (Crown Jewels — Phase 1)

**Compliance (14)** — advanced regulatory logic with significant IP value:

| Tool Name | Regulation |
|-----------|-----------|
| `mica_asset_classification` | EU MiCA 2023/1114 — ART/EMT/Utility token classification |
| `sebi_fpi_validator` | SEBI FPI Regulations 2019 — India investment limits |
| `fsa_japan_crypto_audit` | Japan FSA Payment Services Act — crypto exchange audit |
| `sec_form_pf_compiler` | SEC Form PF — private fund adviser reporting |
| `kyc_aml_chain_analysis` | KYC/AML on-chain screening — OFAC pattern analysis |
| `reg_bi_compliance_logic` | SEC Reg BI — broker-dealer best interest obligations |
| `brexit_passporting_check` | Post-Brexit EU/UK cross-border licensing |
| `australia_asics_checker` | AFSL licensing — Corporations Act 2001 |
| `france_amf_whitepaper_audit` | AMF ICO visa — Pacte Law whitepaper audit |
| `ireland_ica_reporting` | CBI ICAV reporting — UCITS/AIFMD structures |
| `fincen_boir_generator` | FinCEN BOIR — Corporate Transparency Act |
| `esg_sfdr_categorization` | SFDR Article 6/8/9 — ESG fund classification |
| `schedule_d_8949_generator` | IRS Schedule D / Form 8949 tax reporting |
| `digital_agent_clause_checker` | AI agent contract clause analysis |

**Technical (5)** — high-value proprietary algorithms:

| Tool Name | Description |
|-----------|-------------|
| `smart_contract_vulnerability_scan` | Security audit — reentrancy, delegatecall, access controls |
| `agentic_white_label_portal` | Enterprise white-label MCP portal configuration |
| `latency_optimized_order_routing` | HFT/low-latency order routing — competitive IP |
| `private_key_shard_manager` | MPC Shamir's Secret Sharing — custody logic |
| `hardware_wallet_handshake` | Hardware wallet confirmation gating |

**Free compliance utilities** (open to all): `gdpr_fin_data_scrub`, `india_gst_tax_calculator`, `brazil_pix_settlement_logic` — commodity tools with no significant IP moat.

---

## How Skills Work

Each skill is a Python function registered with FastMCP. Call them like any MCP tool:

```
Use the fund_accounting skill to calculate NAV for my portfolio.
Use the kyc_aml_chain_analysis skill to screen this wallet address.
Use the portfolio_stress_test skill to run a 2008 GFC scenario.
```

## Full Catalog

| Category | Description |
|---|---|
| **A2A** | Google Agent-to-Agent protocol — agent discovery, handshakes, collaboration contracts |
| **Accounting** | Double-entry bookkeeping, journal entries, trial balance, P&L |
| **Accounting Standards** | GAAP, IFRS, ASC 842 lease accounting, revenue recognition |
| **Achievements** | Agent achievement tracking, milestone logging, proof of labor |
| **Agent CRM** | Agent relationship management, interaction history, trust scoring |
| **Agent Directory** | Agent registry, capability lookup, routing |
| **Ambassadors** | Community ambassador program management |
| **Analytics** | Financial analytics, cohort analysis, trend detection |
| **Anomaly** | Anomaly detection in financial data, outlier flagging |
| **API Spec** | OpenAPI spec generation, endpoint documentation |
| **API Versioning** | Version management, deprecation tracking |
| **Approval** | Multi-party approval workflows, authorization chains |
| **Attribution** | Revenue attribution, marketing ROI, source tracking |
| **Banking** | Bank account management, transaction categorization, reconciliation |
| **Benchmarks** | Performance benchmarking against indices, peer comparison |
| **Billing** | Invoice generation, subscription billing, dunning |
| **Blockchain** | On-chain data parsing, block explorer integration, hash verification |
| **Bounties** | Bounty creation, tracking, and payout logic |
| **Budgeting** | Budget creation, variance analysis, rolling forecasts |
| **Capacity** | Resource capacity planning, utilization tracking |
| **Capital Markets** | Equity/debt issuance, syndication, capital stack analysis |
| **Certification** | Compliance certification tracking, audit readiness |
| **Commodities** | Commodity pricing, futures, basis risk |
| **Comms** | Agent communication protocols, message routing |
| **Community Analytics** | Community health metrics, engagement scoring |
| **Competitive** | Competitive intelligence, market positioning |
| **Compliance** | AML/KYC, SFDR, MiCA, SEC, GDPR, cross-jurisdictional |
| **Compliance Reporting** | Regulatory report generation, filing schedules |
| **Config Management** | System configuration versioning and deployment |
| **Content** | Financial content generation, report writing |
| **Contracts** | Contract parsing, obligation tracking, clause analysis |
| **Contracts Lifecycle** | Contract lifecycle management from draft to expiry |
| **Cost Allocation** | Overhead allocation, fund expense attribution |
| **CRE** | Commercial real estate underwriting, NOI, cap rate |
| **Credit** | Credit scoring, creditworthiness analysis, default probability |
| **Credit Analysis** | Debt service coverage, leverage ratios, credit memos |
| **Crowd Economics** | Crowdfunding economics, token distribution, bonding curves |
| **Crypto** | Crypto asset management, portfolio tracking, tax lots |
| **Crypto Auth** | Wallet authentication, signature verification |
| **Data Quality** | Data validation, completeness checks, lineage tracking |
| **Deals** | Deal pipeline management, term sheet analysis |
| **Debt** | Debt scheduling, amortization, covenant tracking |
| **DeFi** | DeFi protocol analysis, yield farming, liquidity pools |
| **Derivatives** | Options pricing, delta hedging, Greeks calculation |
| **Disaster Recovery** | DR planning, RTO/RPO analysis, failover logic |
| **Docs** | Document generation, template management |
| **Education** | Financial education content, quiz generation |
| **Energy Finance** | Energy project finance, PPA structuring, offtake analysis |
| **Escrow** | Escrow account management, release conditions, milestone tracking |
| **Estate** | Estate planning, trust administration, inheritance analysis |
| **ETL** | Data extraction, transformation, and loading pipelines |
| **Events** | Financial event processing, corporate actions |
| **Export** | Data export, CSV/XBRL/JSON formatting |
| **Feature Management** | Feature flag management, rollout tracking |
| **Feedback** | User feedback collection and analysis |
| **Financial Analysis** | Ratio analysis, DuPont, Altman Z-score |
| **Fixed Income** | Bond pricing, yield curves, duration, convexity |
| **Forecasting** | Revenue forecasting, scenario modeling, Monte Carlo |
| **Franchise** | Franchise economics, royalty tracking, FDD analysis |
| **Fund Accounting** | NAV calculation, fund administration, investor allocations |
| **Fund Admin** | Subscription/redemption processing, waterfall distribution |
| **FX** | Currency conversion, FX exposure, hedging ratios |
| **FX Trading** | FX order management, execution analytics |
| **Gateway** | API gateway logic, rate limiting, routing |
| **Ghost Ledger** | Google Sheets-based fund accounting ledger (Snowdrop's core) |
| **Governance** | DAO governance, voting mechanics, proposal analysis |
| **Grants** | Grant tracking, reporting requirements, drawdown schedules |
| **Health** | System health monitoring, uptime tracking |
| **I18n** | Internationalization, multi-currency, locale formatting |
| **Incidents** | Incident management, post-mortem analysis |
| **Insurance** | Insurance policy analysis, premium calculation, claims |
| **Insurance Analytics** | Loss ratio, combined ratio, actuarial analysis |
| **Integrations** | Third-party API integration management |
| **Jury** | Multi-agent consensus and dispute resolution |
| **KPI** | KPI definition, tracking, and alerting |
| **Library** | Knowledge library management, document indexing |
| **Log Management** | Log aggregation, analysis, retention policies |
| **Market Data** | Price feeds, OHLCV, market depth, volatility surfaces |
| **Memory** | Agent memory storage and retrieval |
| **Mercury** | Mercury business banking API integration |
| **MLPs** | Master Limited Partnership accounting and analysis |
| **Muni Finance** | Municipal bond analysis, CUSIP lookup, tax-exempt yield |
| **Network** | Network topology analysis, peer connections |
| **NLG** | Natural language generation for financial reports |
| **NLP** | Financial document NLP, sentiment, entity extraction |
| **NMTC** | New Markets Tax Credit allocation and compliance |
| **Notifications** | Alert generation, threshold monitoring |
| **Notifications Management** | Notification preference and delivery management |
| **Observability** | System observability, tracing, metrics |
| **Operations** | Operational workflow management, SLA tracking |
| **Orchestration** | Multi-agent orchestration, task routing |
| **Partners** | Partnership agreement analysis, revenue sharing |
| **Payments** | Payment processing, settlement, reconciliation |
| **Payroll** | Payroll calculation, tax withholding, garnishments |
| **Pension** | Pension fund accounting, actuarial assumptions, liability |
| **Pitch** | Investment pitch analysis, deck scoring |
| **Playground** | Sandbox environment for skill testing |
| **Portfolio** | Portfolio construction, optimization, rebalancing |
| **Pricing** | Asset pricing, model validation, fair value |
| **Privacy** | PII detection, data masking, GDPR scrubbing |
| **Private Credit** | Direct lending, CLO structuring, credit facilities |
| **Project Finance** | Infrastructure finance, DSCR, waterfall modeling |
| **Prompts** | Prompt engineering, template management |
| **Public Finance** | Government accounting, GASB, municipal budgeting |
| **Quant** | Quantitative analysis, factor models, backtesting |
| **Ralph Wiggum** | Self-correction loop — Snowdrop's internal QA system |
| **Readiness** | Operational readiness assessment, go-live checklists |
| **Real Estate** | Property analysis, valuation, lease abstraction |
| **Real Estate Finance** | CRE debt, LTV, DSCR, construction lending |
| **Referrals** | Referral program tracking and payout logic |
| **Regulatory** | Multi-jurisdiction regulatory requirement lookup |
| **REITs** | REIT compliance, FFO, AFFO, distribution calculations |
| **Reporting** | Financial statement generation, board reporting |
| **Restructuring** | Debt restructuring, distressed analysis, recovery rates |
| **Risk** | VaR, CVaR, stress testing, scenario analysis |
| **SaaS Metrics** | ARR, churn, LTV, CAC, magic number |
| **SDK** | SDK generation and documentation |
| **Search** | Financial document search, semantic retrieval |
| **Security** | Security audit, access control, credential management |
| **Simulation** | Financial simulation, agent behavior modeling |
| **Skill Marketplace** | Skill pricing, listing, and discovery |
| **Skill Meta** | Skill metadata management and registration |
| **Social** | Social platform integration, community metrics |
| **Sovereign** | Sovereign wealth fund analysis, country risk |
| **Specialty Finance** | Specialty lending, receivables, factoring |
| **Sprints** | Sprint planning, velocity tracking, burndown |
| **Structured Finance** | ABS, MBS, CDO structuring and analysis |
| **Supply Chain Finance** | SCF programs, dynamic discounting, reverse factoring |
| **Support** | Support ticket management, SLA tracking |
| **Swarm** | Multi-agent swarm coordination, assembly line |
| **Tax** | US federal/state tax, cost basis, wash sale detection |
| **Tax Advanced** | International tax, BEPS, transfer pricing |
| **Technical** | Technical analysis, chart patterns, signal generation |
| **Telegram** | Telegram bot integration, alert delivery |
| **Telemetry** | System telemetry, performance metrics |
| **Time Tracking** | Time logging, billing rates, project allocation |
| **Tokenomics** | Token economic modeling, emission schedules, vesting |
| **Trade Finance** | LC, SBLC, documentary collections, trade credit |
| **Treasury** | Cash management, liquidity forecasting, investment policy |
| **Trust** | Trust accounting, fiduciary duties, distribution |
| **Vendor Evaluation** | Vendor scoring, RFP analysis, due diligence |
| **Vendors** | Vendor management, contract tracking, payment terms |
| **Venture** | Venture debt, cap table, dilution modeling |
| **Watering Hole** | Agent marketplace mechanics, job posting, payout |
| **Workflow** | Workflow automation, approval routing, status tracking |

---

## Engagement Infrastructure Skills

Snowdrop's autonomous Moltbook engagement system — posting content, tracking performance,
and feeding a live MBA-friendly dashboard. Built on the Google A2A Protocol for agent observability.

| Skill | Description |
|-------|-------------|
| `moltbook_engagement_sheet` | Read/write the Moltbook Engagement Google Sheet command center. Actions: `log_post`, `get_submolt_list`, `get_stats`, `daily_report`, `update_weekly_actual`, `log_daily_report`, `update_performance` (poller upserts upvotes/comments), `update_submolt_perf` (poller upserts per-submolt aggregates). |
| `slack_post` | Post text messages to the Snowdrop Slack channel (`SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID`). Used for daily engagement reports and milestone alerts. |
| `moltbook_post_performance` | Fetch live upvotes and comments for Moltbook posts by `post_id`. ROI score = upvotes×2 + comments×5. Spot-check any post in real time. Optional `write_to_sheet=True` upserts results. |
| `performance_poller_control` | Observe and control the Performance Poller A2A subagent. Actions: `status` (last run, posts polled, errors), `trigger` (run immediately via subprocess), `read_card` (return A2A agent card JSON), `read_log` (structured recent log lines). |
| `context7_docs` | Fetch live, version-specific library documentation via Context7 MCP. Call before writing code that uses any third-party library (gspread, FastMCP, requests, anthropic, etc.). Requires `CONTEXT7_API_KEY`. See **Documentation Skills** section below. |
| `google_dev_docs` | Search Google's official developer docs (GCP, Firestore, Cloud Run, BigQuery, Vertex AI, Firebase, Maps). Requires `GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY`. See **Documentation Skills** section below. |

### Performance Poller Subagent (A2A Protocol)

The Performance Poller is an autonomous subagent (`scripts/performance_poller.py`) running every
2 hours on snowdrop-node via cron. It polls the Moltbook API for upvotes and comments on every
logged post, then:
1. Upserts results into the **POST PERFORMANCE** tab
2. Recomputes **SUBMOLT PERFORMANCE** aggregates with ROI grades
3. Updates **WEEKLY FORECAST** engagement_actual column
4. Logs structured JSON entries (with `run_id` UUID for A2A traceability)

**ROI Grades** (by avg upvotes/post):
- **A** = avg ≥ 5 → double down, post 6×/day in this submolt
- **B** = avg ≥ 2 → working, maintain current pace
- **C** = avg ≥ 0.5 → some traction, experiment with topics
- **D** = avg > 0 → minimal traction, try a different angle
- **F** = avg = 0 → pause after 20+ posts, reallocate to better submolts

**A2A agent card** (served by Fly.io):
```
https://snowdrop-mcp.fly.dev/.well-known/agent-performance-poller.json
```

**Snowdrop can interact with the poller from any MCP client:**
```python
performance_poller_control(action="status")        # last run, posts polled, errors
performance_poller_control(action="read_log", limit=20)   # recent structured log
performance_poller_control(action="trigger")       # run immediately (don't wait 2h)
performance_poller_control(action="read_card")     # A2A agent card JSON
```

**State file:** `state/poller_state.json` on snowdrop-node
**Log file:** `/tmp/performance_poller.log` on snowdrop-node
**Crontab:** `0 */2 * * * /home/snowdrop/snowdrop-core/venv/bin/python /home/snowdrop/snowdrop-mcp/scripts/performance_poller.py >> /tmp/performance_poller.log 2>&1`

### Dashboard Tab

The **DASHBOARD** tab in the Moltbook Engagement Sheet is formula-driven — no manual refresh needed.
Add it with: `python scripts/add_dashboard_tab.py`

Key KPIs visible at a glance:
- Posts Today / This Week / All Time
- Upvotes and Comments (populated by Performance Poller every 2h)
- Engagement Rate (% posts with ≥1 upvote)
- % of Weekly Target with On Track / Behind / At Risk status
- Strategy Distribution (7 posting strategies)
- Top 10 Submolts by avg upvotes (QUERY from SUBMOLT PERFORMANCE)
- Year Forecast Progress toward 10,000-post target
- Estimated token spend at $0.0002/post (Gemini Flash Lite)

---

## Documentation Skills

Snowdrop and all her subagents must call these skills **before writing code** that uses any
third-party library or Google API. They return current, version-specific documentation so code
is written against today's APIs, not training data from 18 months ago.

| Skill | File | Description |
|-------|------|-------------|
| `context7_docs` | `skills/docs/context7_docs.py` | Live library docs via Context7 MCP (HTTP). Resolves library name → Context7 ID → fetches version-specific docs. Covers gspread, FastMCP, requests, anthropic, httpx, and thousands more. |
| `google_dev_docs` | `skills/docs/google_dev_docs.py` | Authoritative Google developer docs via Google Developer Knowledge MCP. Covers all GCP services (Cloud Run, BigQuery, Vertex AI, Pub/Sub, Secret Manager, Firestore), Firebase, Android, Maps, and all Google APIs. Re-indexed within 24h of upstream changes. |

### Usage (for AI coding agents reading this)

```python
# Before using gspread: fetch current docs
context7_docs(library="gspread", topic="service account authentication")
# → returns /burnash/gspread docs with code examples

# Before using Cloud Run: fetch Google's official docs
google_dev_docs(query="Cloud Run deploy Python container environment variables")
# → returns 5 authoritative doc chunks from docs.cloud.google.com

# fetch_full=True gets the complete page for the top result
google_dev_docs(query="Vertex AI streaming Gemini Python SDK", fetch_full=True)
```

### Setup / Env Vars

| Var | How to get it |
|-----|--------------|
| `CONTEXT7_API_KEY` | Free at [context7.com/dashboard](https://context7.com/dashboard) |
| `GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY` | GCP Console → APIs & Services → Credentials → Create API key → restrict to "Developer Knowledge API". Must first enable: `gcloud services enable developerknowledge.googleapis.com` |

### Technical Details

- **Context7 endpoint**: `https://mcp.context7.com/mcp` — JSON-RPC 2.0, `Authorization: Bearer {key}`
- **Google Dev Knowledge endpoint**: `https://developerknowledge.googleapis.com/mcp` — JSON-RPC 2.0, `X-Goog-Api-Key: {key}`
- Both use `Accept: application/json, text/event-stream` (MCP streamable-HTTP transport)
- Context7 tools: `resolve-library-id` (libraryName + query) → `query-docs` (libraryId + query)
- Google tools: `search_documents` (query) → optionally `get_document` (name from parent field)

---

## Contributing

Want to add a skill? See [CONTRIBUTING.md](CONTRIBUTING.md) or open a Discussion.

Each skill must follow the standard pattern:
- Python function with `TOOL_META` dict
- Structured return: `{"status": "success/error", "data": {...}, "timestamp": "..."}`
- No hardcoded secrets — env vars only
- Executive Summary docstring

*Built by Snowdrop — Stonewater Solutions LLC*

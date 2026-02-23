# Snowdrop Skill Catalog

> 667+ skills across 150+ categories. All free. All open.

Snowdrop's complete MCP skill catalog — every Python function registered with FastMCP and callable from any MCP-compatible client (Claude Code, Cursor, custom agents). Skills span financial compliance, blockchain analytics, fund accounting, engagement automation, real-time documentation lookup, and more. Each skill follows the standard `TOOL_META` + structured-return pattern.

## Table of Contents

- [How Skills Work](#how-skills-work)
- [Tier System](#tier-system)
- [Full Catalog](#full-catalog)
- [Engagement Infrastructure Skills](#engagement-infrastructure-skills)
- [Documentation Skills](#documentation-skills)
- [Contributing](#contributing)

## Tier System

Snowdrop MCP is freemium. Skills are either **Free** (open access) or **Premium** (subscribers only).
There is no middle ground — Premium means the implementation code is private.

| Tier | Access | IP Protection |
|------|--------|---------------|
| Free | All MCP clients | Code public on GitHub |
| Premium | Subscribers only (coming soon) | Code in private repo, public stub returns `payment_required` |

### Current Premium (Crown Jewels — Phase 1)
All compliance/* except gdpr_fin_data_scrub, india_gst_tax_calculator, brazil_pix_settlement_logic.
Plus: agentic_white_label_portal, smart_contract_vulnerability_scan, latency_optimized_order_routing,
private_key_shard_manager, hardware_wallet_handshake.

Premium skills appear in tools/list with "(Premium — subscribe at https://snowdrop.ai)" in their
description. Calling them returns {"status": "payment_required", ...} on the public server.

Subscribe: https://snowdrop.ai (launching soon)

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

## Contributing

Want to add a skill? See [CONTRIBUTING.md](CONTRIBUTING.md) or open a Discussion.

Each skill must follow the standard pattern:
- Python function with `TOOL_META` dict
- Structured return: `{"status": "success/error", "data": {...}, "timestamp": "..."}`
- No hardcoded secrets — env vars only
- Executive Summary docstring

*Built by Snowdrop — Stonewater Solutions LLC*

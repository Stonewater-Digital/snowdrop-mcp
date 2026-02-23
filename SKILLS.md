# Snowdrop MCP — Skills Directory

## Executive Summary
This document provides a comprehensive, auto-generated directory of all skills available on the Snowdrop MCP server. It details the exact count and capabilities of both **Premium** (proprietary/paid) and **Free** skills currently loaded in production. Generated: `2026-02-23T22:07:49.461265+00:00`. The skill count reflects the local Python environment. For the count of skills deployed to Cloud Run, call the /health endpoint at https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/health. To regenerate: `python scripts/generate_skill_directory.py` or `./scripts/sync_catalog.sh`.

**Total Active Skills:** 994
- **Free Skills:** 972
- **Premium Skills:** 22

## Table of Contents
1. [Premium Skills](#premium-skills)
2. [Free Skills by Category](#free-skills-by-category)
3. [Ecosystem Topology](#ecosystem-topology)

---

## Premium Skills
Premium skills contain proprietary logic (e.g., financial modeling, compliance enforcement, white-label portals). Their real implementations live in the private `skills/premium/` directory. Public stubs exist for discovery but return paywall responses without a valid JWT.

| Skill Name | Description |
|------------|-------------|
| `agentic_white_label_portal` | Generates a white-label portal configuration for a Snowdrop client. Filters the master skill registry to only those skills the client is authorised to access, applies branding overrides, assigns rate limits based on the daily USD transaction cap, and returns a complete portal configuration object ready for front-end consumption. |
| `australia_asics_checker` | Determines Australian Financial Services Licence (AFSL) requirements under the Corporations Act 2001 (Cth) Part 7.6. Evaluates service type, client classification (retail vs wholesale), product categories, and foreign provider relief under ASIC Class Orders and legislative instruments. |
| `brexit_passporting_check` | Post-Brexit cross-border licensing analysis for UK and EU financial services. Confirms that EEA passporting is definitively unavailable since 31 December 2020, evaluates available equivalence decisions, and determines local authorisation requirements per target market and licence type. |
| `digital_agent_clause_checker` | Evaluates actions against identity, spend, and communication rules. |
| `esg_sfdr_categorization` | Classifies EU investment funds under SFDR (EU) 2019/2088 as Article 6 (no ESG), Article 8 (promotes ESG characteristics), or Article 9 (sustainable investment objective). Applies ESA Joint Supervisory Authority guidance, ESMA Q&A, and EU Taxonomy Regulation (EU) 2020/852 disclosure requirements. |
| `fincen_boir_generator` | Generates a FinCEN Beneficial Ownership Information Report (BOIR) under the Corporate Transparency Act (CTA) 31 U.S.C. § 5336 and 31 CFR Part 1010.380. Validates all required fields, checks the 23 statutory exemption categories, and formats the payload for FinCEN BOIR online submission. |
| `france_amf_whitepaper_audit` | Audits a token offering whitepaper against French AMF requirements under the Pacte Law (Loi n° 2019-486) and AMF General Regulation (RG AMF) Articles 712-1 to 712-23. Scores completeness, flags missing mandatory sections, and determines ICO visa eligibility. |
| `fsa_japan_crypto_audit` | Audits a Japanese crypto-asset exchange against FSA (Financial Services Agency) requirements under the Payment Services Act (資金決済に関する法律), specifically cold storage minimums, asset segregation, and operational security controls. |
| `hardware_wallet_handshake` | Gate-keeps large on-chain transfers by requiring hardware wallet confirmation when a transaction exceeds the configured USD threshold. Generates a cryptographically random nonce and a confirmation request payload with a 5-minute expiry window. |
| `ireland_ica_reporting` | Generates Irish Central Bank (CBI) reporting data for Irish Collective Asset-management Vehicles (ICAVs) under the Irish Collective Asset-management Vehicles Act 2015 and CBI UCITS/AIF Rulebooks. Supports both UCITS and AIFMD structures with sub-fund disaggregation and CBI deadline computation. |
| `issue_access_token` | Mint an ES256 JWT access token for a trusted agent or project. Registers the JTI in the revocation blocklist and writes an audit log entry (raw token is never persisted). Args: subject (str), label (str), scope (list[str] \| None), ttl_days (int). Returns: {status, data: {token, jti, subject, expires_at, scope}, timestamp}. |
| `kyc_aml_chain_analysis` | Performs on-chain KYC/AML screening by cross-referencing wallet addresses against OFAC-style sanctioned address lists and heuristic risk indicators including mixer usage patterns, rapid fund movement (under 24h), and known bad actor address clusters. Supports TON, Solana, and Ethereum chains. |
| `latency_optimized_order_routing` | Selects the optimal server route for a trade order by ranking available exchange server locations by latency and filtering out unreliable routes (reliability < 99%). Returns the winning route, ranked alternatives, and estimated execution time advantage over the median route. |
| `list_access_tokens` | List all issued JWT access tokens from the audit log. Returns metadata only — raw token strings are never stored or returned. Each entry contains: sub, label, jti, scope, exp, issued_at. Returns: {status, data: {tokens: [...]}, timestamp}. |
| `mica_asset_classification` | Classifies crypto-assets under EU MiCA Regulation (EU) 2023/1114 as ART (Asset-Referenced Token), EMT (E-Money Token), or Utility Token. Flags significant status based on market cap and daily volume thresholds. |
| `private_key_shard_manager` | MPC key shard management using Shamir's Secret Sharing: split a key into N shards (K-of-N required to reconstruct), reconstruct from K shards, or verify shard validity. |
| `reg_bi_compliance_logic` | Evaluates a broker-dealer recommendation against SEC Regulation Best Interest (17 CFR § 240.15l-1) four-obligation framework: Disclosure, Care, Conflict of Interest, and Compliance. Scores each obligation and identifies documentation requirements. |
| `revoke_access_token` | Revoke an active JWT by JTI. Marks the token as revoked in the Firestore blocklist so that _is_revoked() will return True on future checks. Args: jti (str), reason (str, optional). Returns: {status, data: {jti, revoked_at, reason}, timestamp}. |
| `schedule_d_8949_generator` | Classifies transactions into short- and long-term gains for tax filing. |
| `sebi_fpi_validator` | Validates Foreign Portfolio Investor (FPI) compliance under SEBI (Foreign Portfolio Investors) Regulations, 2019. Determines FPI Category I, II, or III; checks the 10% single-company investment limit, 24%/49% sectoral caps, and grandfathering provisions. |
| `sec_form_pf_compiler` | Compiles SEC Form PF data for private fund advisers under Dodd-Frank Act Section 404 and SEC Rule 204(b)-1. Determines Large Adviser classification, filing frequency, and generates the structured Form PF JSON payload for PFRD submission. |
| `smart_contract_vulnerability_scan` | Analyze DeFi smart contract metadata for common vulnerability patterns: reentrancy, unchecked delegatecall, centralization risk, and missing access controls. Returns risk score and recommendations. |

---

## Free Skills by Category
Free skills are publicly available utility, infrastructure, and standard API wrapper tools.

### Users
| Skill Name | Description |
|------------|-------------|
| `a2a_request_handler` | Performs JSON-RPC compliance checks and bearer-token auth for A2A requests. |
| `a2a_response_builder` | Constructs JSON-RPC envelopes for outbound A2A traffic. |
| `access_control_checker` | Validates tier permissions across Snowdrop skills. |
| `achievement_tracker` | Evaluates activity events for new badges and upcoming milestones. |
| `acquirer_spread_hedge_allocator` | Optimizes hedge basket weighting using beta, borrow cost, and stub exposure. |
| `action_item_extractor` | Uses heuristics to identify action items, assignees, and priority from text. |
| `activist_campaign_scorecard` | Scores activist campaigns using filing cadence, proposal quality, and precedent outcomes to frame trade bias. |
| `activity_based_costing` | Distributes cost pools based on activity driver consumption. |
| `administrator_api_bridge` | Bridge skill that validates administrator feeds and emits normalized payload summaries. |
| `adr_local_settlement_optimizer` | Suggests optimal ADR/local conversions factoring fees and FX parity. |
| `aerodrome_impermanent_loss_guardrail` | Simulates Aerodrome IL exposure for dual-asset pools and recommends caps. |
| `aerodrome_liquidity_rebalance_playbook` | Builds Aerodrome liquidity rebalance plans for yield rotations. |
| `aerodrome_lsd_leverage_spread_modeler` | Models Aerodrome LSD leverage spreads with health-factor guardrails. |
| `agent_certification_issuer` | Generates signed certificates for agents who pass compatibility tests. |
| `agent_collaboration_handshake` | Formalises an agent-to-agent collaboration contract by serialising the contract terms deterministically, producing a SHA-256 hash, and generating a nonce-stamped signature payload. Validates that the calling agent's ID is listed as a party. Returns signing instructions and an expiry window for the counter-party to countersign. |
| `agent_compatibility_tester` | Runs handshake, discovery, and error-handling tests for third-party agents. |
| `agent_credit_scorer` | Generates 300-850 style scores using payment history and utilization inputs. |
| `agent_directory_manager` | Registers, updates, searches, and deactivates public agent profiles. |
| `agent_funnel_analyzer` | Calculates conversion rates across registration, activation, engagement, and upgrade. |
| `agent_heartbeat_collector` | Rolls up heartbeat telemetry and surfaces degraded/dead agents. |
| `agent_heartbeat_monitor` | Build health check monitoring configurations for Fly.io and Railway services. Defines check intervals, alert rules (3 consecutive failures = alert), and per-service configs. |
| `agent_network_mapper` | Builds adjacency insights, clusters, and bridge agents from interactions. |
| `agent_onboarding_validator` | Checks VC freshness, capability alignment, and bad-actor lists before onboarding. |
| `agent_profile_builder` | Creates shareable markdown pages summarizing an agent's public metrics. |
| `agent_reputation_scorer` | Calculates a 0-100 composite score from payments, labor, and violations. |
| `agent_session_tracker` | Aggregates per-agent usage, spend, and churn risk from session logs. |
| `agent_skill_version_checker` | Verifies Context7 documentation freshness for registered skills. Flags any skill whose last_checked date is older than 7 days and returns a freshness score as a percentage of up-to-date skills. |
| `agent_tab_manager` | Credits and debits agent tabs with a $100 cap and settles via Proof of Labor. |
| `agent_to_agent_negotiation` | Executes one round of a structured bot-to-bot price negotiation, generating a counter-offer or accept/walk-away recommendation within a 5-round protocol. |
| `agent_trust_score_calc` | Calculates a 0-100 trust score for a peer agent based on transaction success rate, uptime, longevity, skill breadth, and verification status. |
| `agentic_syndication_logic` | Assembles an optimal bot syndicate for a given mission by filtering candidates on availability and trust, matching skills to requirements, and minimizing cost while maximizing skill coverage. |
| `air_quality_lookup` | Retrieve current air quality conditions, historical hourly AQI data, or heatmap tile configuration for any location using the Google Air Quality API. Returns AQI score, dominant pollutant, individual pollutant concentrations, health recommendations, plus an esg_score (0–100) and real_estate_impact assessment for ESG reporting and property valuation workflows. |
| `allocation_enforcer_80_20` | Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails. |
| `altman_z_score` | Calculates Altman Z, identifies zone, and estimates distress probability. |
| `ambassador_manager` | Handles ambassador applications, approvals, listings, and removals. |
| `ambassador_reward_calculator` | Computes base rewards and bonuses for ambassador activity. |
| `annual_budget_builder` | Projects monthly revenue/expense totals with growth assumptions for 12 months. |
| `antitrust_case_law_matcher` | Matches live deals with precedent case rulings to infer regulatory posture. |
| `antitrust_timeline_estimator` | Projects regulatory review paths using precedent duration by sector and agency workload. |
| `api_credential_rotator` | Generates rotation tasks for API keys/secrets using age vs. policy frequency. |
| `api_health_monitor` | Performs lightweight health checks and scores availability. |
| `api_key_rotation_logic` | Evaluates API credential ages against their configured maximum lifetime. Returns three categories: expired keys (must rotate now), expiring-soon keys (within 7 days), and a full rotation schedule sorted by urgency. Also reports an overall compliance percentage. |
| `api_key_rotation_monitor` | Scores API keys by age and alerts when max_age_days is breached. |
| `api_playground_provider` | Generates sample inputs and sandboxed outputs for public skill demos. |
| `api_usage_dashboard` | Summarizes token usage, costs, and trends across providers/models/purposes. |
| `api_version_router` | Negotiates version routing and flags deprecations for skills. |
| `approval_chain_builder` | Builds escalated approval chains based on action context and risk. |
| `arbitrum_batch_cost_pressure_monitor` | Projects Arbitrum batch posting cost pressure based on calldata pricing and queue depth. |
| `arbitrum_block_builder_watch` | Tracks Arbitrum builder dominance to detect MEV cartels. |
| `arbitrum_cross_domain_message_flow_tracker` | Tracks Arbitrum cross-domain message queues to flag settlement delays. |
| `arbitrum_gas_rebate_window_simulator` | Simulates Arbitrum gas rebate windows to recommend timing-sensitive swaps. |
| `arbitrum_l1_data_gas_planner` | Optimizes Arbitrum data gas budgeting for the next submission window. |
| `arbitrum_latency_breaker_detector` | Detects Arbitrum latency breaker events before users feel sequencer stalls. |
| `arbitrum_memetic_orderflow_guard` | Flags memecoin orderflow on Arbitrum attracting MEV dogpiles. |
| `arbitrum_mempool_backlog_risk_monitor` | Scores Arbitrum mempool congestion risk and suggests throttle actions for spiky bursts. |
| `arbitrum_proof_window_reliability_scanner` | Models Arbitrum proof submission reliability against backlog volatility. |
| `arbitrum_sandwich_risk_radar` | Scores live sandwich attack risk across Arbitrum dex orderflow. |
| `arbitrum_sequencer_fee_forecaster` | Projects Arbitrum sequencer fee bands for the next block window using backlog and L1 data costs. |
| `arbitrum_throughput_ceiling_tracker` | Estimates Arbitrum throughput headroom vs current usage to plan order flow bursts. |
| `arbitrum_to_base_eth_bridge_optimizer` | Optimizes ETH bridge routing from Arbitrum to Base with fee and latency heuristics. |
| `arbitrum_to_base_govtoken_bridge_optimizer` | Optimizes governance token bridge routing from Arbitrum to Base with fee and latency heuristics. |
| `arbitrum_to_base_lsd_bridge_optimizer` | Optimizes liquid staking derivative bridge routing from Arbitrum to Base with fee and latency heuristics. |
| `arbitrum_to_base_stablecoin_bridge_optimizer` | Optimizes stablecoin bridge routing from Arbitrum to Base with fee and latency heuristics. |
| `arbitrum_to_optimism_eth_bridge_optimizer` | Optimizes ETH bridge routing from Arbitrum to Optimism with fee and latency heuristics. |
| `arbitrum_to_optimism_govtoken_bridge_optimizer` | Optimizes governance token bridge routing from Arbitrum to Optimism with fee and latency heuristics. |
| `arbitrum_to_optimism_lsd_bridge_optimizer` | Optimizes liquid staking derivative bridge routing from Arbitrum to Optimism with fee and latency heuristics. |
| `arbitrum_to_optimism_stablecoin_bridge_optimizer` | Optimizes stablecoin bridge routing from Arbitrum to Optimism with fee and latency heuristics. |
| `arbitrum_tx_priority_curve_optimizer` | Builds a recommended Arbitrum priority fee curve for latency-sensitive users. |
| `argus_to_json_transformer` | Transforms legacy Argus-style raw commercial real estate data dictionaries into a clean, standardized JSON schema with consistent field naming, type coercion, and a warnings list for missing or suspicious values. |
| `artifact_registry_manager` | Manage Google Artifact Registry Docker images: list, clean old tags, remove untagged layers. Use after each deployment to keep storage costs low. Requires roles/artifactregistry.admin on the service account. |
| `assembly_line_cost_calculator` | Compares Assembly Line run-rate against a pure-Opus baseline. |
| `assembly_line_orchestrator` | Frames the Haiku→Sonnet→Opus workflow and estimates token spend. |
| `asset_allocation_optimizer` | Finds feasible allocations that hit target return/risk under constraints. |
| `asset_light_transition_scorecard` | Scores restructurings shifting to asset-light models based on margin potential. |
| `asset_sale_catalyst_model` | Assesses probability-weighted asset sale proceeds versus enterprise value gap. |
| `audit_24h_reconstructor` | Filters ledger activity to a 24h window and produces a running balance. |
| `audit_kraken` | Retrieves live Kraken exchange balances for TON, SOL, and USDC, converts to USD, and returns a structured balance report. |
| `audit_trail_immutable_export` | Export records to a SHA-256 signed CSV. The hash covers the entire CSV content, making tampering detectable. Hash is embedded as the final row or metadata header. |
| `audit_trail_logger` | Writes immutable audit entries to logs/audit_trail.jsonl. |
| `backup_snapshot_creator` | Compiles file manifests for Snowdrop backups (no writes performed). |
| `backup_verifier` | Checks backup manifests for missing or corrupted files using SHA-256 hashes. |
| `badge_issuer` | Creates cryptographic badge records for ambassador and achievement unlocks. |
| `balance_sheet_generator` | Groups trial balance entries into a balance sheet (A=L+E validation). |
| `balancer_impermanent_loss_guardrail` | Simulates Balancer IL exposure for dual-asset pools and recommends caps. |
| `balancer_liquidity_rebalance_playbook` | Builds Balancer liquidity rebalance plans for yield rotations. |
| `balancer_lsd_leverage_spread_modeler` | Models Balancer LSD leverage spreads with health-factor guardrails. |
| `bankruptcy_exit_watchlist` | Tracks Chapter 11 emergence timelines, valuation metrics, and tradeable post-reorg equities. |
| `base_batch_cost_pressure_monitor` | Projects Base batch posting cost pressure based on calldata pricing and queue depth. |
| `base_cross_domain_bundle_guard` | Tracks Base cross-domain bundles that leak MEV to L1. |
| `base_cross_domain_message_flow_tracker` | Tracks Base cross-domain message queues to flag settlement delays. |
| `base_gas_rebate_window_simulator` | Simulates Base gas rebate windows to recommend timing-sensitive swaps. |
| `base_l1_data_gas_planner` | Optimizes Base data gas budgeting for the next submission window. |
| `base_latency_breaker_detector` | Detects Base latency breaker events before users feel sequencer stalls. |
| `base_mempool_backlog_risk_monitor` | Scores Base mempool congestion risk and suggests throttle actions for spiky bursts. |
| `base_mev_backrun_heatmap` | Maps Base backrun bands to protect passive LPs. |
| `base_priority_lane_optimizer` | Suggests Base priority lanes to dodge MEV bursts. |
| `base_proof_window_reliability_scanner` | Models Base proof submission reliability against backlog volatility. |
| `base_sequencer_fee_forecaster` | Projects Base sequencer fee bands for the next block window using backlog and L1 data costs. |
| `base_throughput_ceiling_tracker` | Estimates Base throughput headroom vs current usage to plan order flow bursts. |
| `base_to_arbitrum_eth_bridge_optimizer` | Optimizes ETH bridge routing from Base to Arbitrum with fee and latency heuristics. |
| `base_to_arbitrum_govtoken_bridge_optimizer` | Optimizes governance token bridge routing from Base to Arbitrum with fee and latency heuristics. |
| `base_to_arbitrum_lsd_bridge_optimizer` | Optimizes liquid staking derivative bridge routing from Base to Arbitrum with fee and latency heuristics. |
| `base_to_arbitrum_stablecoin_bridge_optimizer` | Optimizes stablecoin bridge routing from Base to Arbitrum with fee and latency heuristics. |
| `base_to_optimism_eth_bridge_optimizer` | Optimizes ETH bridge routing from Base to Optimism with fee and latency heuristics. |
| `base_to_optimism_govtoken_bridge_optimizer` | Optimizes governance token bridge routing from Base to Optimism with fee and latency heuristics. |
| `base_to_optimism_lsd_bridge_optimizer` | Optimizes liquid staking derivative bridge routing from Base to Optimism with fee and latency heuristics. |
| `base_to_optimism_stablecoin_bridge_optimizer` | Optimizes stablecoin bridge routing from Base to Optimism with fee and latency heuristics. |
| `base_tx_priority_curve_optimizer` | Builds a recommended Base priority fee curve for latency-sensitive users. |
| `basket_trade_rebalance_orchestrator` | Simulates rebalances for popular baskets to plan front-running trades. |
| `benchmark_comparator` | Calculates alpha, beta, tracking error, and rolling alpha versus benchmark. |
| `bigquery_query` | Run BigQuery SQL queries and schema operations for financial analytics. Uses BigQuery REST API v2 with explicit SA credentials — no gcloud, no ADC. Requires roles/bigquery.jobUser and roles/bigquery.dataViewer. |
| `billing_reconciler` | Compares invoiced amounts against measured compute usage to surface deltas. |
| `black_scholes_pricer` | Calculates Black-Scholes option prices with full Greek outputs. |
| `blockchain_wallet_reconciler` | Reconciles Ghost Ledger wallet balances against on-chain snapshots and surfaces tolerance breaches. |
| `blog_post_generator` | Creates structured blog content with title, sections, and metadata. |
| `bond_pricer` | Computes clean/dirty price, duration, convexity, and current yield. |
| `bonding_curve_pricer` | Calculates Watering Hole bonding curve prices using time decay, demand velocity, and snap-back protections. |
| `bounty_claim_handler` | Handles claim lifecycle events for posted community bounties. |
| `bounty_payout_processor` | Validates and stages payouts for approved bounty winners. |
| `bounty_poster` | Publishes new skill, feature, or bug-fix bounties to the community board. |
| `brazil_pix_settlement_logic` | Applies Banco Central do Brasil (BCB) Pix rules per Resolução BCB nº 1 (2020) and subsequent circulars. Validates transaction limits (nightly R$1,000 cap for PF), fee structures, settlement times (10 seconds 24/7), and transaction type restrictions. |
| `break_even_analyzer` | Computes break-even units, revenue, margin of safety, and estimated time to break even. |
| `bridge_loan_pricing` | Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month. Rates are expressed as annual decimals (e.g. 0.05 = 5%). |
| `bridge_loan_rollover_calculator` | Models bridge maturity walls and rollover probability. |
| `budget_variance_analyzer` | Compares actuals to budget with variance labeling and assessments. |
| `burn_rate_calculator` | Calculates gross/net burn, runway, and trend classification from recent data. |
| `burn_trigger_monitor` | Flags Watering Hole burn when expenses beat revenue+labor by 20% for 3 weeks. |
| `buyback_window_optimizer` | Aligns blackout schedules with liquidity patterns to anticipate supportive repurchase flows. |
| `calc_waterfall_dist` | Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. |
| `calendar_spread_decay_optimizer` | Optimizes calendar spreads by simulating theta bleed vs. vol drift. |
| `cap_rate_decomposition` | Breaks down cap rate into risk-free, property, market, and vacancy components. |
| `cap_table_manager` | Computes fully diluted ownership after venture rounds including option pools and notes. |
| `cap_table_simulator` | Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. |
| `capital_call_fx_optimizer` | Allocates multi-currency balances to satisfy a capital call with minimal FX drag. |
| `capital_call_notice_generator` | Creates LP-specific capital call instructions awaiting Thunder sign-off. |
| `capital_raise_dilution_estimator` | Simulates rights, PIPE, and follow-on dilution paths to measure near-term overhangs. |
| `carried_interest_tracker` | Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows. |
| `carveout_proceeds_allocator` | Simulates cash deployment from equity carveouts vs. balance-sheet needs. |
| `cash_conversion_cycle` | Computes DSO, DIO, DPO, and the cash conversion cycle to assess working capital efficiency. |
| `cash_flow_projector` | Computes monthly cash flow projections with cumulative balances and risk flags. |
| `cash_total_return_swap_equity_basis_analyzer` | Measures basis between cash equities and TRS quotes after funding. |
| `cash_vs_stock_mix_optimizer` | Recommends optimal hedge mix incorporating borrow rates and dividend adjustments. |
| `central_bank_ledger_sync` | Reconciles a CBDC transaction ledger against central bank balance and reported circulation figures to detect discrepancies. |
| `cfius_risk_heatmap_generator` | Scores deals on national security triggers using NAICS mapping and prior cases. |
| `chalkboard_dashboard` | Aggregates transparency metrics for the public chalkboard dashboard. |
| `changelog_generator` | Outputs Keep a Changelog formatted text from change entries. |
| `chapter11_plan_value_dashboard` | Compares plan recovery waterfalls against market pricing for multiple classes. |
| `chart_data_formatter` | Normalizes data into Chart.js/Plotly friendly schema with labels/datasets. |
| `chart_of_accounts` | Adds or searches accounts across the Stonewater standard chart. |
| `churn_analyzer` | Analyzes churn patterns, cohort retention, and at-risk agents. |
| `clawback_analyzer` | Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. |
| `clinical_trial_binary_planner` | Builds probability-weighted payoff trees for pivotal biotech readouts using open FDA calendars. |
| `closed_end_fund_activist_screener` | Flags CEFs ripe for activism based on discount persistence and governance terms. |
| `closing_conditions_scorer` | Scores closing condition tightness to estimate slippage risk. |
| `cloud_build_trigger` | Manually trigger a Google Cloud Build build from a trigger ID or repo/branch. Returns the build ID and log URL for monitoring. |
| `cloud_run_deploy` | Deploy, inspect, list, or delete Google Cloud Run services. Uses Cloud Run Admin API v2 with explicit service account credentials only — no gcloud CLI, no Application Default Credentials. |
| `cmbs_loan_analyzer` | Computes LTV, DSCR, debt yield, and balloon risk for CMBS loans. |
| `co_investment_ledger` | Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio. |
| `coinbase_agentkit_verifier` | Drafts the JSON payload needed to verify Snowdrop in Coinbase AgentKit. |
| `collaborative_liquidity_hunt` | Validates whether a group of trusted agents has sufficient combined capital to exploit a thin-market spread opportunity and produces a pro-rata allocation plan. |
| `collar_ratio_sensitivity_analyzer` | Simulates collar payout across acquirer price paths to manage hedge sizing. |
| `collections_manager` | Tiers overdue accounts into reminder, notice, suspension, or write off stages. |
| `commitment_pacing_model` | Suggests annual commitments and overcommitment ratios for PE allocation targets. |
| `community_growth_tracker` | Calculates growth rates, viral coefficient, and projections from snapshots. |
| `community_impact_attributor` | Splits revenue, usage, and profit between community and internal skills. |
| `community_leverage_dashboard` | Summarizes how community contributions amplify internal capacity. |
| `community_skill_adoption_tracker` | Compares usage, revenue, and growth metrics between internal and community skills. |
| `community_skill_submitter` | Validates community skill code before it enters the review queue. |
| `comparable_company_screener` | Calculates EV/Revenue, EV/EBITDA, P/E, and implied values for a target. |
| `comparable_transaction_analyzer` | Derives valuation ranges from comps using EV/Revenue and EV/EBITDA multiples. |
| `competing_bid_probability_forecaster` | Uses M&A precedent, target scarcity, and sponsor interest signals to rate topping odds. |
| `competitive_landscape_tracker` | Compares competitor offerings, pricing, and feature coverage. |
| `compliance_calendar` | Generates a consolidated compliance deadline calendar with statuses. |
| `compute_budget_enforcer` | Makes sure Snowdrop does not exceed the $50/day compute budget. |
| `compute_capacity_planner` | Projects when capacity will be breached and recommends actions. |
| `compute_time_tracker` | Calculates task durations, idle time, and cost per skill/model. |
| `config_validator` | Ensures config.yaml content meets Snowdrop schema expectations. |
| `consensus_protocol` | Evaluates votes for quorum and flags potential Byzantine behavior. |
| `construction_draw_scheduler` | Generates draw schedules, interest carry, and LTC compliance checks. |
| `construction_draw_validator` | Validates a construction loan draw request by verifying that receipts sum to the requested amount, the milestone exists and has sufficient remaining budget, and completion percentage is consistent. Returns approval status, discrepancy list, and remaining milestone budget. |
| `context_window_optimizer` | Packs content sections into the available context window using priority heuristics. |
| `contract_lifecycle_manager` | Creates, updates, lists, and surfaces contracts nearing expiration. |
| `contract_metadata_analyzer` | Scores contract risk based on verification, usage, and deployer reputation. |
| `contract_renewal_alerter` | Identifies contracts requiring renewal action and quantifies value at risk. |
| `contractor_payment_tracker` | Aggregates contractor payments and flags 1099 thresholds. |
| `contribution_attribution_engine` | Weights lines of code, complexity, usage, and revenue to estimate contributor value. |
| `contribution_quality_scorer` | Calculates quality grades based on Snowdrop coding standards and security checks. |
| `contribution_token_tracker` | Aggregates token usage by contributor type to measure leverage. |
| `contributor_retention_analyzer` | Tracks contributor repeat rates, retention curves, and churn metrics. |
| `conversation_summarizer` | Compress multi-turn logs into actionable decisions and questions. |
| `convertible_arbitrage_event_sync` | Aligns convertible hedge unwinds with catalysts to trade equity lag/lead. |
| `convertible_bond_basis_dashboard` | Tracks CB basis vs. fair value adjusting for credit spread and carry. |
| `convertible_note_calculator` | Computes accrued interest, conversion price, and shares for convertible notes. |
| `correlation_matrix_builder` | Build Pearson correlation matrices from asset price histories. |
| `cost_basis_averaging_logic` | Calculate cost basis using FIFO, LIFO, average cost, or specific-lot method. Identifies tax-loss harvesting opportunities and wash sale risk. |
| `cost_center_reporter` | Aggregates expenses by center with mix and budget deltas. |
| `cost_segregation_estimator` | Approximates accelerated depreciation benefits from cost seg studies. |
| `covenant_lite_risk_scorer` | Assigns protection scores based on covenant packages and aggressive terms. |
| `covenant_reset_playbook_builder` | Outlines likely covenant reset packages from precedent negotiations. |
| `cre_cap_rate_aggregator` | Aggregates capitalization rates from a list of comparable CRE sales. Computes individual cap rates (NOI / sale_price), then averages by asset class (office, retail, multifamily, etc.) and by market (MSA). Returns overall market average and outlier flags. |
| `cre_debt_stack_modeling` | Models a commercial real estate capital stack with senior debt, mezzanine, and equity tranches. Calculates blended cost of capital, cumulative LTV per tranche, and flags structural risk (e.g., LTV > 80% for senior). |
| `cre_lease_comparator` | Evaluates tenant/landlord economics for NNN, gross, and modified gross leases. |
| `credit_default_swap_pricer` | Converts CDS spreads into implied default probabilities and expected losses. |
| `credit_downgrade_shock_modeler` | Projects equity beta and spread snapbacks tied to ratings-agency downgrade scenarios. |
| `credit_enhancement_calculator` | Determines required subordination and overcollateralization to hit target ratings. |
| `credit_facility_utilization_monitor` | Aggregates revolver/DDTL/term loan utilization and identifies spread tiers. |
| `credit_limit_adjuster` | Applies utilization and score rules to tab limit changes. |
| `credit_spread_analyzer` | Calculates credit spreads, implied default probabilities, and indicative ratings. |
| `cron_scheduler` | Checks which scheduled tasks are due and when the next run occurs. |
| `cross_asset_vol_leak_tracker` | Tracks vol lead-lag between equities and credit/commodities proxies to inform trades. |
| `cross_border_event_heat_gauge` | Flags jurisdictions with rising policy risks affecting pending company-level events. |
| `cross_border_tax_grossup_modeler` | Estimates tax leakage and withholding adjustments for cross-border stock deals. |
| `cross_chain_accounting_bridge` | Normalize TON, Solana, and Ethereum transactions into a unified single ledger with net positions per chain. |
| `crowd_roi_calculator` | Measures value created by community contributions versus review cost. |
| `crowd_sourced_risk_audit` | Aggregates multi-assessor risk scores into a confidence-weighted consensus, surfaces statistical outliers, and classifies overall consensus strength. |
| `crowd_sourcing_forecast` | Projects contributions, skills, and value under bear/base/bull scenarios for six months. |
| `crowd_value_velocity` | Calculates weekly value velocity, acceleration, and forward projections. |
| `crypto_fiat_converter` | Uses USD hub conversions (pending Thunder approval for transfers). |
| `crypto_glossary` | Explains crypto terms with analogies and risk warnings (goodwill only). |
| `csv_exporter` | Flattens dict rows and emits RFC4180-compliant CSV strings. |
| `ctr_generator` | Determines whether a CTR filing is required and drafts the payload. |
| `curl_example_generator` | Builds ready-to-run curl commands for each skill's input schema. |
| `currency_carry_analyzer` | Calculates carry yields, CIP deviations, and risk flags for FX pairs. |
| `curve_impermanent_loss_guardrail` | Simulates Curve IL exposure for dual-asset pools and recommends caps. |
| `curve_liquidity_rebalance_playbook` | Builds Curve liquidity rebalance plans for yield rotations. |
| `curve_lsd_leverage_spread_modeler` | Models Curve LSD leverage spreads with health-factor guardrails. |
| `custodian_feed_harmonizer` | Normalize custodian statement payloads into a canonical schema with validation flags. |
| `custody_break_detector` | Identify cash or security breaks between custody statements and the ledger. |
| `daily_briefing_generator` | Assembles Snowdrop's morning status brief for Thunder. |
| `dashboard_aggregator` | Groups panels by source, surfaces alerts, and crafts summary sentences. |
| `data_anonymizer` | Transforms sensitive fields using hash/mask/redact/generalize strategies. |
| `data_freshness_monitor` | Checks data sources against allowed staleness windows. |
| `data_narrator` | Converts structured finance outputs into tone-aware prose. |
| `data_provenance_map` | Construct lineage graph from ingestion artifacts and flag stale datasets or missing dependencies. |
| `data_quality_scorecard` | Compute null/duplication/freshness scores for administrator datasets and flag breaches. |
| `data_transformer` | Applies rename/cast/compute/drop/default transformations to dataset rows sequentially. |
| `dcf_sensitivity_matrix` | Builds a DCF table across WACC and terminal growth assumptions. |
| `deal_break_downside_calculator` | Benchmarks standalone downside using factor peers, DCF ranges, and option market cues. |
| `deal_document_change_detector` | Diffs new filings against prior documents to surface material clause changes. |
| `dealer_gamma_position_reconstructor` | Infers dealer gamma balance using OI ladder and price levels. |
| `debt_capacity_calculator` | Computes leverage and cash-flow-based debt capacity estimates. |
| `debt_commitment_slippage_checker` | Monitors financing bank updates and macro stress to flag commitment cracks. |
| `debt_covenant_monitor` | Evaluates debt covenants against current financial ratios. Supports leverage_ratio (lower is better), interest_coverage (higher is better), and current_ratio (higher is better) covenant types. Returns breach status and distance-to-breach for each covenant. |
| `debt_issuance_analyzer` | Computes net proceeds, OID yields, and all-in borrowing costs for bond deals. |
| `declining_margin_turnaround_monitor` | Scores restructurings on margin recovery speed relative to guidance. |
| `defi_yield_comparator` | Filters DeFi protocols by safety heuristics and ranks risk-adjusted yield. |
| `delayed_draw_term_loan_tracker` | Calculates drawn/undrawn balances, fees, and blended costs for DDTLs. |
| `deleveraging_path_visualizer` | Charts leverage trajectories under various asset sale and EBITDA scenarios. |
| `delta_hedge_cost_forecaster` | Projects re-hedge frequency and cost for popular option structures. |
| `deployment_readiness_checker` | Aggregates deployment checklist results and surfaces blockers/warnings. |
| `deposit_pricing_analyzer` | Calculates weighted cost of deposits, effective beta, and expense impact from rate shifts. |
| `depository_receipt_fee_analyzer` | Quantifies ad valorem fees eroding ADR parity to price trades correctly. |
| `deprecation_notice_generator` | Formats structured deprecation notices for skills/endpoints. |
| `digest_builder` | Creates readable digests summarizing activity, metrics, and tips per agent. |
| `dispersion_vs_correlation_mapper` | Relates single-name vol to index implied correlation for dispersion plays. |
| `dispute_resolver` | Determines auto, manual, or split dispute resolutions for escrow issues. |
| `dissent_rights_arbitrage_planner` | Quantifies appraisal-rights value vs. cost for appraisal arbitrage trades. |
| `distressed_exchange_acceptance_model` | Estimates acceptance probability for distressed exchanges across tranche holders. |
| `distribution_waterfall_modeler` | Calculates LP/GP outcomes for American and European waterfalls with tier detail. |
| `divestiture_requirement_model` | Quantifies revenue thresholds regulators typically demand to approve similar deals. |
| `dividend_capture_screener` | Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted decay. |
| `dividend_reinstatement_detector` | Screens for companies poised to restart dividends based on cash flow inflections and board language. |
| `dividend_swap_roll_calendar` | Plots dividend swap rolls to lock in mispriced implied dividends. |
| `docker_cleanup` | Clean up Docker images, containers, and volumes on the local machine to prevent disk exhaustion. Supports dry-run mode. Schedule weekly via subagent. Always preserve keep_images list (e.g. the live snowdrop-mcp image). |
| `docker_secret_injector` | Builds op run templates for injecting secrets into containers. |
| `document_vault_ocr_router` | Assign vault documents to OCR models based on mime type, priority, and presence of embedded text. |
| `dpi_narrative_generator` | Converts DPI metrics into LP-facing narrative with severity tiers when below target. |
| `drawdown_notice_generator` | Produce structured LP drawdown notices and routing metadata. |
| `drawdown_scheduler` | Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline. |
| `dry_powder_calculator` | Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves. If monthly_deployment_rate is provided, runway_months = dry_powder / rate. Useful for fund pacing, LP reporting, and GP investment planning. |
| `dscr_calculator` | Computes DSCR, assessment tier, excess cash, and headroom for new debt. |
| `dual_class_collapse_timer` | Estimates when dual-class sunsets or pressure points could unlock governance catalysts. |
| `dual_listed_company_spread_tracker` | Monitors DLC spread relative to currency-adjusted parity and borrow friction. |
| `duplicate_transaction_detector` | Finds exact and fuzzy duplicate transactions for Ghost Ledger hygiene. |
| `dupont_analysis` | Returns 3-stage and 5-stage DuPont ROE decomposition. |
| `dynamic_discount_calculator` | Applies tiered volume and loyalty discounts for agents. |
| `earnings_gap_playbook` | Quantifies historical post-earnings gaps vs. implied move to flag asymmetric setups using free price feeds. |
| `earnings_quality_analyzer` | Computes accrual ratios, Beneish M-Score, and manipulation risk. |
| `earnings_quality_restatement_checker` | Flags restatement risk from irregular accruals and audit comments. |
| `earnings_vol_crush_projector` | Projects vol crush magnitude after earnings using historical analogs. |
| `earnings_whisper_spread_analyzer` | Measures gap between whisper numbers and official consensus to weight surprise odds. |
| `earnout_value_distribution_engine` | Simulates milestone achievement probability to value contingent payouts. |
| `ebitda_normalization` | Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. |
| `ecosystem_health_dashboard` | Aggregates community metrics into a public health score and highlights. |
| `efficient_frontier_calculator` | Generates random portfolios to approximate the efficient frontier and key points. |
| `elegance_loop` | Compares planned actions against executed results, quantifies drift, and flags when discrepancies breach the 1% tolerance. |
| `email_alert_builder` | Prepares email payloads without sending them. |
| `employee_option_overhang_quantifier` | Measures equity overhang vs. expected dilution through restructuring. |
| `energy_to_currency_peg_logic` | Models energy-backed currency pegs (IoT/solar), computing intrinsic unit value and stress-testing sustainability across energy price scenarios. |
| `entity_extractor` | Uses regex heuristics to extract Snowdrop-relevant entities. |
| `env_var_auditor` | Finds missing, empty, and extra environment variables relative to .env.template. |
| `equity_commitment_backstop_tracker` | Monitors rights backstop size, participants, and pricing fairness. |
| `equity_cure_need_forecaster` | Projects covenant breaches and equity cure sizing windows. |
| `equity_stub_volatility_estimator` | Models stub volatility using component variance contribution. |
| `error_pattern_detector` | Clusters similar errors and surfaces bursts for remediation. |
| `error_retry_exponential_backoff` | Generate an exponential backoff retry schedule with optional jitter for production error handling. Returns per-attempt delays and total max wait time. |
| `escrow_manager` | Creates, monitors, and adjudicates agent escrow records. |
| `estimated_tax_calculator` | Applies 90%/100% safe harbor logic to estimate quarterly payments and due dates. |
| `etf_create_redeem_arb_planner` | Optimizes swap vs. in-kind flows to monetize ETF create/redeem arbitrage. |
| `etf_nav_premium_discount_poller` | Streams ETF premium/discount readings with create/redeem costs to rank arb setups. |
| `etherfi_impermanent_loss_guardrail` | Simulates EtherFi IL exposure for dual-asset pools and recommends caps. |
| `etherfi_liquidity_rebalance_playbook` | Builds EtherFi liquidity rebalance plans for yield rotations. |
| `etherfi_lsd_leverage_spread_modeler` | Models EtherFi LSD leverage spreads with health-factor guardrails. |
| `event_correlator` | Evaluates correlation rules to surface compound incidents. |
| `event_manager` | Handles creation, updates, registrations, and cancellations for events. |
| `exception_queue_prioritizer` | Prioritize reconciliation exceptions by severity, financial exposure, and SLA breach risk. |
| `exchange_1031_analyzer` | Calculates gains, boot, and deadlines for like-kind exchanges. |
| `exchange_ratio_fair_value_solver` | Calculates fair exchange ratios after adjusting for net debt and earning power. |
| `executive_summary_generator` | Formats operational metrics into a Thunder-ready briefing. |
| `executive_transition_sentiment_monitor` | Correlates C-suite turnover with subsequent stock performance and option flow clues. |
| `exit_multiple_analysis` | Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.). |
| `exotic_barrier_breach_probability_engine` | Estimates barrier hit probabilities using free implied vol data. |
| `expense_allocation_engine` | Distributes fund expenses across share classes according to commitment or NAV weights. |
| `expense_categorizer` | Maps expense strings to IRS categories using heuristics. |
| `failure_diagnostic_generator` | Summarizes attempts, hypothesizes root causes, and prescribes human actions. |
| `fastapi_to_mcp_wrapper` | Generate MCP-compliant TOOL_META dict and Python wrapper function code from a function name, docstring, and parameter list. |
| `fcf_quality_analyzer` | Compares free cash flow to net income and highlights working capital effects. |
| `feature_flag_manager` | Gets, sets, lists, or evaluates feature flags stored in config/feature_flags.json. |
| `fee_drag_analyzer` | Summarizes fees and calculates annualized drag versus AUM. |
| `feedback_collector` | Stores categorized feedback with auto-responses. |
| `feedback_response_generator` | Generates human-like responses to agent feedback with priority flags. |
| `feedback_sentiment_analyzer` | Computes sentiment trends and common themes from feedback entries. |
| `ffo_affo_calculator` | Calculates FFO/AFFO and payout ratios for REITs. |
| `fiat_to_crypto_onramp_audit` | Audits fiat-to-crypto on-ramp transactions for volume, fees, velocity, and anomalous spikes. |
| `financial_entity_graph` | Constructs an in-memory adjacency graph of financial entities (funds, companies, LPs, GPs, properties) and their ownership / investment relationships. Computes degree centrality for each node, finds connected components via BFS, and identifies hub entities whose centrality exceeds median + 1 standard deviation. |
| `financial_highlight_extractor` | Summarizes headline metrics, growth narratives, and risks for presentations. |
| `financial_literacy_quiz` | Provides educational quizzes for goodwill content. |
| `financing_gap_liquidity_checker` | Tracks committed financing sources, hedging cost, and debt market windows per deal. |
| `fincen_filings_deal_linker` | Links suspicious activity filings to active deals to gauge watchdog heat. |
| `firebase_ai_logic_list_prompts` | List Firebase AI Logic server-side prompt templates for a project. Returns template IDs, model configurations, and system instructions. |
| `firebase_ai_logic_run_prompt` | Execute a Firebase AI Logic prompt template with provided variables. Returns the model's text response. |
| `firebase_app_distribution_upload` | Upload a build artifact to Firebase App Distribution and notify testers. Returns the release name and download URL. |
| `firebase_app_hosting_list_sites` | List Firebase App Hosting backends for a project. Returns backend ID, repository URL, deploy status, and live URL. |
| `firebase_auth_create_user` | Create a new Firebase Auth user account. Returns the user's UID, email, and creation time. |
| `firebase_auth_get_user` | Look up a Firebase Auth user by UID or email address. Returns user profile data. |
| `firebase_auth_revoke_tokens` | Revoke all refresh tokens for a Firebase Auth user, forcing them to re-authenticate. Returns the user UID and revocation timestamp. |
| `firebase_crashlytics_get_issue` | Get detailed information about a specific Firebase Crashlytics issue including stack trace summary and affected versions. |
| `firebase_crashlytics_list_issues` | List crash issues from Firebase Crashlytics for a given app. Returns issue ID, title, impact (users affected), and last occurrence time. |
| `firebase_dynamic_links_create` | Create a Firebase Dynamic Link (short URL) that routes users to the correct app or web destination based on their platform. Returns the short link and preview link. |
| `firebase_extensions_list` | List all installed Firebase Extensions in a project. Returns extension instance ID, state, extension reference, and configuration. |
| `firebase_fcm_data_analytics` | Get Firebase Cloud Messaging delivery analytics data — send counts, delivery rates, and open rates for a date range. |
| `firebase_fcm_send` | Send a single FCM push notification to a device registration token, topic, or condition. Returns message_id on success. |
| `firebase_fcm_send_multicast` | Send FCM push notification to up to 500 device tokens simultaneously. Returns success_count, failure_count, and per-token results. |
| `firebase_firestore_read` | Read a Firestore document by collection+document ID, or query a collection with optional filters. Returns document data as JSON. |
| `firebase_firestore_write` | Set, update, or delete a Firestore document. Use operation='set' to replace, 'update' to merge fields, 'delete' to remove document. |
| `firebase_hosting_deploy` | Deploy files to a Firebase Hosting site or channel via the Firebase Hosting REST API. Returns the channel URL and release version. |
| `firebase_hosting_list_releases` | List release history for a Firebase Hosting site or channel. Returns list of releases with version, create_time, and status. |
| `firebase_in_app_messaging_list` | List active Firebase In-App Messaging campaigns for a project. Returns campaign names, trigger conditions, and message content. |
| `firebase_ml_get_model` | Get details of a specific Firebase ML model including its download URI for TFLite deployment. |
| `firebase_ml_list_models` | List ML models hosted in Firebase ML for a project. Returns model ID, display name, creation time, and download URI. |
| `firebase_realtime_db_delete` | Delete a node from Firebase Realtime Database at the given path. |
| `firebase_realtime_db_read` | Read a value from Firebase Realtime Database at the given path. Returns the value as JSON. |
| `firebase_realtime_db_write` | Write or update a value in Firebase Realtime Database at the given path. Use method='set' to replace, 'update' to merge, 'push' to append. |
| `firebase_remote_config_get` | Get the current Firebase Remote Config template, including all parameters, parameter groups, and conditions. |
| `firebase_remote_config_set` | Publish a new Firebase Remote Config template. Merges provided parameters with existing config. Returns the new version number and update time. |
| `firebase_storage_upload` | Upload a base64-encoded file to Firebase Cloud Storage. Returns the storage path and a signed download URL valid for 7 days. |
| `flyio_deploy_status` | Builds Fly.io API requests and summarizes allocation health. |
| `form_1099_generator` | Produces Snowdrop's 1099-NEC structure for Thunder review. |
| `forward_vol_calendar_curve_builder` | Builds forward vol curves from listed options to spot anomalies. |
| `fragment_number_monitor` | Filters Fragment number listings by prefix and budget. |
| `franchise_analytics_reporter` | Summarizes revenue, royalties, and operational health per franchise operator. |
| `franchise_billing_reconciler` | Calculates royalty balances for each franchise operator. |
| `franchise_onboarder` | Checks franchise safety gates and returns royalty terms. |
| `franchise_royalty_calculator` | Computes 10% RSS revenue royalties owed by Bar-in-a-Box franchisees. |
| `frax_impermanent_loss_guardrail` | Simulates Frax IL exposure for dual-asset pools and recommends caps. |
| `frax_liquidity_rebalance_playbook` | Builds Frax liquidity rebalance plans for yield rotations. |
| `frax_lsd_leverage_spread_modeler` | Models Frax LSD leverage spreads with health-factor guardrails. |
| `fund_expense_allocator` | Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments). Returns dollar allocations and percentage shares for each sub-fund. |
| `fund_of_funds_allocator` | Creates a heuristic allocation maximizing expected return under diversification rules. |
| `fungible_share_transfer_cost_estimator` | Calculates all-in costs for transferring shares across clearing venues. |
| `futures_curve_analyzer` | Classifies contango/backwardation, computes roll yield, and signals carry trades. |
| `fx_forward_calculator` | Calculates forward rates, points, and hedging costs for currency hedges. |
| `fx_option_pricer` | Calculates FX option premiums and Greeks via Garman-Kohlhagen model. |
| `fx_rate_fetcher` | Retrieves spot FX quotes and inverse rates via ExchangeRate-API. |
| `fx_risk_exposure_calculator` | Aggregates gross/net FX exposures and estimates VaR. |
| `fx_swap_valuation` | Values currency basis swaps using discounted cash flows. |
| `gamma_squeeze_exposure_tracker` | Reconstructs dealer gamma exposure using OI, delta, and borrow metrics. |
| `gas_fee_estimator` | Provides conservative fee estimates for TON and SOL transfers. |
| `gcp_secret_manager` | Create, read, rotate, list, or delete secrets in Google Cloud Secret Manager. Uses Secret Manager API v1 with explicit service account credentials — no gcloud CLI, no ADC. Requires roles/secretmanager.admin on the service account. |
| `gdpr_fin_data_scrub` | Removes or pseudonymises PII from financial data records per GDPR Article 5(1)(e) (storage limitation) and Article 25 (data protection by design). Uses SHA-256 hashing for reversible pseudonymisation or full redaction, preserving non-PII financial fields. |
| `generate_k1_schema` | Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items. |
| `geocoding_lookup` | Google Geocoding API skill for address normalization, coordinate lookup, address validation, and timezone resolution. Used in real estate and location-based financial analysis pipelines. |
| `get_ab_test_insights` | Calculates Moltbook engagement win rates comparing Gemini 2.0 Flash-Lite and Grok 4.1 Fast based on historical performance. |
| `ghost_ledger` | Google Sheets fund-accounting bridge. Supports initializing a new ledger spreadsheet with structured tabs, reading tab data, appending rows, summing vault balances, and writing autonomous decision entries to THE LOGIC LOG tab for audit traceability. |
| `ghost_ledger_enricher` | Annotates Ghost Ledger transactions with ROI heuristics and metadata. |
| `ghost_ledger_reconciler` | Compare ledger snapshots to live balances with zero-tolerance policy. |
| `ghost_ledger_sheets_reader` | Loads Ghost Ledger rows from Google Sheets for the requested notebook section and filters them to a date range. |
| `ghost_ledger_sheets_writer` | Appends validated ledger rows to Ghost Ledger Google Sheets tabs. |
| `ghost_town_detector` | Raises an alert when 14 days pass without paid transactions. |
| `github_issue_tracker` | Fetches labeled GitHub issues and estimates difficulty. |
| `global_tax_withholding_skill` | Calculates the withholding tax on a distribution to an international LP. Applies any available tax treaty rate in preference to the default rate. Grants full exemption (0%) to qualifying entities such as pension funds and sovereign wealth funds. Returns the withholding amount, effective rate, and net distribution after withholding. |
| `go_shop_option_value_estimator` | Values go-shop clauses via historical topping-bid stats and target strategic scarcity. |
| `goodwill_cask_allocator` | Allocates the daily Goodwill cask budget until depleted, then closes the tap. |
| `gp_clawback_calculator` | Evaluates carry distributions versus whole-fund entitlement and recommends clawback. |
| `gradual_rollout_controller` | Decides if an agent is part of a canary rollout using deterministic hashing. |
| `grant_milestone_tracker` | Summarizes milestone completion, disbursements, and deadlines for grants. |
| `grant_proposal_handler` | Accepts, evaluates, and adjudicates Goodwill grant proposals. |
| `green_building_subsidy_audit` | Audits a commercial building's eligibility for green building tax incentives including the Investment Tax Credit (ITC) for solar, Section 179D energy efficiency deduction, and a curated set of state-level ESG incentives. Returns eligible programs, estimated values, and requirements met. |
| `guidance_revision_heatmap` | Maps management guidance changes against Street revisions to spot underpriced sentiment swings. |
| `hackathon_coordinator` | Manages hackathon lifecycle and scores submissions when provided. |
| `heartbeat` | Checks Ghost Ledger readiness, required API keys, and reconciliation freshness before writing HEARTBEAT.md with the current timestamp. |
| `hedge_ratio_slippage_monitor` | Alerts when hedge ratios drift from target because of price or volatility shifts. |
| `hedging_cost_calculator` | Quantifies hedging cost, downside, and upside caps across hedge types. |
| `historical_replay` | Applies historical drawdowns to portfolio weights to estimate losses. |
| `holding_company_discount_modeler` | Calculates holdco vs. underlying NAV gaps, catalyst timelines, and leverage impact. |
| `identity_access_provisioner` | Generate provisioning instructions for identity requests with entitlements and expiry validation. |
| `idr_waterfall_calculator` | Allocates distributable cash through IDR tiers for MLPs. |
| `imf_sdr_allocation_tracker` | Tracks IMF Special Drawing Rights (SDR) holdings vs allocations for a country, converts to USD, and assesses quota adequacy. |
| `impermanent_loss_calculator` | Evaluates current LP value vs hold value and required fees to break even. |
| `implied_volatility_solver` | Computes implied volatility from option price using bisection search. |
| `implied_vs_realized_carry_calculator` | Compares implied carry vs. realized vol for vol selling strategies. |
| `incident_escalation_router` | Determines escalation targets and automatic guardrails based on severity. |
| `incident_tracker` | Opens, updates, or lists incidents with SLA tracking and JSONL logging. |
| `index_constituent_gap_finder` | Detects valuation gaps between index members and non-members with similar fundamentals. |
| `index_rebalance_flow_simulator` | Models passive fund buying/selling pressure ahead of major index review announcements. |
| `india_gst_tax_calculator` | Calculates Indian Goods and Services Tax (GST) for services including cross-border supply, SEZ, and export scenarios. Applies IGST Act 2017 rates, OIDAR (Online Information Database Access and Retrieval) rules, and LUT (Letter of Undertaking) exemptions for zero-rated exports. |
| `industry_benchmark_comparator` | Ranks Snowdrop metrics versus benchmark percentiles to highlight strengths and gaps. |
| `inflation_deflation_tracker` | Computes inflation rates and estimates deflation crossover dates. |
| `inflation_hedging_simulator` | Models sovereign fund real returns across inflation scenarios and recommends allocation shifts for inflation protection. |
| `influence_scorer` | Scores agent influence using a simplified PageRank iteration. |
| `insurance_coverage_tracker` | Summarizes insurance coverages, gaps, and renewal windows. |
| `intent_classifier` | Heuristically classifies operator text into MCP skill intents |
| `interest_rate_swap_valuer` | Computes MTM, PV legs, and DV01 for swaps using provided discount curve. |
| `interlisted_short_locate_planner` | Maps borrow availability across venues to support cross-border arbitrage. |
| `intraday_basis_slippage_guard` | Alerts when live spreads deviate from modeled thresholds intraday. |
| `intraday_vol_reversion_scanner` | Detects intraday vol spikes likely to mean revert based on order book metrics. |
| `investment_basics_explainer` | Returns plain-language explanations for foundational investing topics. |
| `investor_letter_drafter` | Builds executive-ready investor letter sections. |
| `invoice_factoring_calculator` | Computes advance, fees, and effective annual rate for factoring transactions. |
| `invoice_generator` | Generates franchise-friendly invoices with royalty handling. |
| `ipo_pricing_analyzer` | Evaluates implied valuation, dilution, and discount to comps for IPO ranges. |
| `irr_bridge_reporter` | Calculates IRR, DPI, RVPI, and TVPI along with driver bridge for investor reporting. |
| `irr_calculator` | Computes IRR, MOIC, and profit metrics from dated cash flows. |
| `j_curve_modeler` | Simulates fund cash flows, NAV, and J-curve inflection metrics. |
| `javascript_sdk_generator` | Builds an ES module client with fetch wrappers and TypeScript types for skills. |
| `journal_entry_builder` | Builds balanced journal entries and assigns sequential IDs. |
| `json_to_xbrl_transformer` | Transform JSON financial facts into SEC XBRL-JSON format using the us-gaap taxonomy. Maps concept names to us-gaap namespace and generates inline XBRL-compatible output. |
| `jury_deliberation_orchestrator` | Structures prompts and verdicts for the Sonnet/Grok/Gemini debate loop. |
| `jury_verdict_aggregator` | Roll up model verdicts with dynamic confidence weighting and escalation logic. |
| `k1_allocator` | Allocates income, deductions, and distributions across partners with special allocations. |
| `kelly_criterion_calculator` | Computes Kelly fraction, position size, and expected growth rates. |
| `key_derivation_helper` | Derives deterministic key identifiers from the master seed. |
| `knowledge_base_article_generator` | Summarizes frequent ticket resolutions into KB articles to reduce load. |
| `knowledge_base_indexer` | Builds an inverted index over documents and answers keyword queries. |
| `kpi_tracker` | Calculates KPI progress, highlights off-track metrics, and summarizes health. |
| `l2_mempool_privacy_guard` | Monitors encrypted mempool fallback coverage across Arbitrum/Base/Optimism. |
| `l2_shared_auction_tracker` | Aggregates shared sequencer auctions across major L2s to signal MEV demand. |
| `lbo_model_builder` | Models leverage, cash flows, and equity returns for a stylized LBO. |
| `leak_rumor_price_action_profiler` | Profiles pre-announcement trading to flag deals with elevated leak scrutiny risk. |
| `lease_abstract_skill` | Extracts key commercial lease terms from raw lease text using regex-based pattern matching. Targets commencement date, expiration date, base rent, escalation rate, renewal options, and break clauses. Returns confidence score and list of fields that could not be extracted. |
| `lease_accounting_calculator` | Computes lease liability, ROU asset, and income statement impact for ASC 842. |
| `ledger_immutability_checker` | Build a SHA-256 hash chain over ledger entries to detect tampering and verify immutability. Each entry hash includes the prior hash, forming a blockchain-style chain. |
| `lesson_to_action_sync_bot` | Scan logs/lessons.md, cluster recurring entries, and emit recommended follow-up actions. |
| `lessons_analyzer` | Parses logs/lessons.md content for failure hotspots and trends. |
| `levered_holdco_vs_opco_spread_tuner` | Quantifies spread impact from leverage and subsidiary dividend policy. |
| `liability_management_transaction_mapper` | Maps tender/exchange sequences to assess residual capital structure risk. |
| `linea_data_availability_cost_forecaster` | Forecasts Linea data availability costs when proofs spike. |
| `linea_proof_latency_profiler` | Profiles Linea proof latency and confidence based on queue depth and L1 gas noise. |
| `linea_prover_cluster_health_monitor` | Monitors Linea prover clusters for saturation and fallback readiness. |
| `linea_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Linea sequencer mempools and hints. |
| `linea_state_diff_audit_simulator` | Simulates Linea state diff coverage to spot risky batches before posting. |
| `linea_validity_challenge_planner` | Plans Linea validity challenge playbooks if proofs degrade. |
| `linear_regression_forecaster` | Fits y = mx + b and projects forward values with r-squared diagnostics. |
| `liquidity_depth_analyzer` | Estimates price impact and slippage for CFMM pools. |
| `liquidity_sleeve_switchboard` | Reallocates liquidity sleeves between vehicles to exploit transient spreads. |
| `liquidity_sweep_impact_estimator` | Estimates market impact from large option sweeps to manage slippage. |
| `litigation_docket_event_tracker` | Monitors docket updates and court calendars to quantify lawsuit resolution catalysts. |
| `llc_compliance_tracker` | Calculates upcoming compliance deadlines for Stonewater Solutions LLC. |
| `loan_amortization_calculator` | Computes monthly payment, amortization schedule, and payoff projections. |
| `loan_covenant_checker` | Tests financial covenants and highlights closest breaches. |
| `loan_loss_reserve_modeler` | Calculates expected credit losses by segment with macro overlays. |
| `log_integrity` | Verify the SHA-256 hash chain in Snowdrop's invocation audit log. Detects deletions, modifications, or insertions. On suspicion, alerts to Ghost Ledger THE LOGIC LOG and writes a local INTEGRITY_ALERT file. Run daily via systemd timer for continuous tamper-evidence. |
| `log_rotation_manager` | Evaluates log files and proposes rotation/compression/deletion actions. |
| `long_term_memory_store` | Append-only JSONL memory store with taggable search and CRUD operations. |
| `lp_reporting_standard` | Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null. Produces structured markdown with sections for Fund Overview, Performance Metrics, Top Holdings, Cash Position, and Upcoming Events. |
| `ltv_calculator` | Computes LTV, discounted LTV, and payback metrics for each agent tier. |
| `macro_data_surprise_linker` | Connects company guidance sensitivity with upcoming macro releases to prime event trays. |
| `macro_indicator_tracker` | Fetches recent FRED indicators and computes MoM trends. |
| `management_fee_offset` | Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs. Net fee is floored at zero (cannot be negative). |
| `mandate_enforcer` | Injects mandated proposals at top of sprint backlog while respecting capacity. |
| `market_data_fetcher` | Pulls CoinGecko quotes and 24h change metrics. |
| `max_drawdown_analyzer` | Computes maximum drawdown statistics from an equity curve. |
| `mcp_discovery_beacon` | Packages a list of Snowdrop skills into MCP-compatible advertisement payloads and generates the beacon configuration required for periodic self-registration on the MCP network. Calculates a visibility score (0–100) based on skill count and category diversity. |
| `mcp_tool_registrar` | Produces a JSON-RPC compliant MCP tools/list response for Snowdrop skills. |
| `meme_stock_flow_regime_classifier` | Detects social-volume and borrow-cost trigger points that precede melt-up or crash phases. |
| `mercury_balance_fetcher` | Retrieves account balances from Mercury's /api/v1/accounts endpoint. |
| `mercury_payment_sender` | Constructs ACH/wire payloads for Mercury but leaves them pending Thunder approval. |
| `mercury_transaction_ingest` | Pulls Mercury transactions, tags inflow/outflow, and formats for Ghost Ledger. |
| `merger_accretion_dilution` | Evaluates EPS impact of an acquisition with cash/stock mix and synergies. |
| `merger_spread_implied_probability` | Converts deal spreads into implied probabilities adjusting for borrow and carry. |
| `message_signer` | Signs messages with an env-provided key for agent authentication. |
| `minority_interest_buyin_model` | Values buy-in economics vs. minority protections and cash flow splits. |
| `mlp_distributable_cash_flow_calc` | Calculates Distributable Cash Flow (DCF) and coverage ratios for Master Limited Partnerships. |
| `mlp_distribution_analyzer` | Calculates DCF coverage, leverage, and GP take for MLP distributions. |
| `mlp_dpu_growth_modeler` | Projects DPU growth considering EBITDA growth, IDRs, and dropdowns. |
| `mlp_k1_estimator` | Estimates income, return of capital, and UBTI exposure for MLP units. |
| `model_router` | Reads config/config.yaml and maps a task category to the correct model entry. |
| `moltbook_engagement_loop` | Analyzes Moltbook post history to determine optimal posting times (UTC), best-performing content types, recommended posting frequency, and forecasts expected engagement for the next post. |
| `moltbook_engagement_sheet` | Read and write the Moltbook Engagement Google Sheet — Snowdrop's command center. Actions: 'log_post' (append post to POST LOG), 'get_submolt_list' (read SUBMOLT DIRECTORY for strategy routing), 'get_stats' (aggregate performance data), 'daily_report' (compile daily stats from POST LOG, suitable for Slack), 'update_weekly_actual' (fill in this week's actual post count in WEEKLY FORECAST), 'update_performance' (upsert post upvotes/comments into POST PERFORMANCE tab — called by the performance poller), 'update_submolt_perf' (upsert per-submolt aggregate stats into SUBMOLT PERFORMANCE tab — called by the poller), 'update_karma' (upserts total account karma tracking into KARMA HISTORY tab). Designed to run cheaply with Gemini Flash Lite. |
| `moltbook_post_performance` | Fetch live upvotes and comments for one or more Moltbook posts by post_id. Returns engagement metrics, ROI score (upvotes*2 + comments*5), and traction status. Use for spot-checking specific posts or verifying the performance poller is working. Set write_to_sheet=True to also upsert results into the POST PERFORMANCE tab. |
| `moltbook_poster` | Formats Snowdrop skills for the Moltbook agent marketplace. |
| `moltbook_reputation_builder` | Generates structured Moltbook post drafts to build agent reputation, scores estimated engagement, and recommends the optimal submolt and tags. Now includes cost tracking. |
| `moltbook_sentiment_analyzer` | Scores Moltbook posts for financial sentiment and detects narrative shifts within submolts over a configurable lookback window. |
| `moltbook_stamina_monitor` | Monitors Moltbook API rate limits (stamina) from the Google Sheet and generates a 1-sentence health summary using a cheap model. |
| `money_transmitter_checker` | Flags actions that might require MTL coverage and provides guidance. |
| `monte_carlo_simulator` | Runs geometric Brownian motion simulations to generate percentile outcomes. |
| `moving_average_crossover` | Calculates SMA/EMA crossovers and emits trading posture signals. |
| `mrr_calculator` | Calculates MRR components and growth for Watering Hole subscriptions. |
| `mullvad_vpn_status` | Constructs Mullvad account queries and summarizes connection health. |
| `multi_bank_liquidity_sweeper` | Recommend cash sweeps across multiple banks using target min/max policies. |
| `multi_book_influence_tracker` | Calculates an agent's influence score across multiple social platforms, identifies top-performing interactions, and infers the influence trend over time. |
| `multi_currency_consolidator` | Converts positions into a base currency with exposure diagnostics. |
| `multi_l2_mev_burst_scheduler` | Schedules rollup transaction batches to sidestep simultaneous MEV bursts. |
| `multi_leg_strategy_pnl_simulator` | Simulates P&L paths for iron condors, butterflies, and ratio spreads. |
| `multi_sig_workflow` | Classifies an action into auto, 2FA, or multi-sig approval paths. |
| `muni_bond_analyzer` | Computes tax-equivalent yield, breakeven rates, and annual savings for muni bonds. |
| `nav_reconciliation` | Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. |
| `nav_rollforward_tracker` | Bridges opening NAV to closing NAV using period cash flows and valuation changes. |
| `net_interest_margin_calculator` | Computes current NIM, gap ratios, and projected NIM under rate shocks. |
| `net_operating_loss_shield_optimizer` | Maps NOL usage scenarios to protect tax assets post-transaction. |
| `newsletter_composer` | Creates newsletters covering new skills, platform stats, and educational tips. |
| `nft_inventory_tracker` | Aggregates NFT holdings with valuation deltas and allocation mix. |
| `nmtc_community_impact_scorer` | Scores NMTC projects across jobs, needs, and community benefits. |
| `nmtc_compliance_checker` | Evaluates census tract, QALICB, and substantially-all tests for NMTC projects. |
| `nmtc_deal_structurer` | Models NMTC leveraged structures with investor equity, leverage loans, and subsidy. |
| `nmtc_investor_return_calculator` | Calculates investor IRR over NMTC compliance period with tax credits and fees. |
| `noi_audit_tool` | Validates Net Operating Income (NOI) for a commercial real estate property. Computes NOI from gross revenue and operating expenses, calculates NOI margin, and flags material variance against a prior period if provided. |
| `noncore_asset_sale_sequencer` | Orders asset dispositions to maximize deleveraging and valuation uplift. |
| `notification_preferences_manager` | Gets, sets, or resets notification preferences per agent with persistence. |
| `notification_router` | Maps alert priority to Telegram/SMS/freeze workflows. |
| `occupancy_rate_forecaster` | Forecasts occupancy rates for the next 3 periods using simple linear regression on historical data, with optional adjustments for market absorption rate and new supply entering the market. |
| `okr_tracker` | Calculates OKR progress, color codes, and highlights at-risk objectives. |
| `openapi_spec_generator` | Converts Snowdrop skill metadata into an OpenAPI 3.0.3 specification. |
| `openrouter_cost_logger` | Calculates OpenRouter call costs using the internal pricing table. |
| `operating_leverage_calculator` | Computes contribution margin, DOL, breakeven revenue, and scenario EBIT deltas. |
| `operational_maturity_scorer` | Rates capabilities across dimensions and assigns an overall maturity level. |
| `opportunity_zone_audit` | Audits Qualified Opportunity Zone (QOZ) investment compliance per IRC §1400Z-2. Checks the 180-day reinvestment window, 10-year hold for full exclusion, substantial improvement test (must double basis in improvements), and original use doctrine. Estimates tax benefits. |
| `optimism_batch_cost_pressure_monitor` | Projects Optimism batch posting cost pressure based on calldata pricing and queue depth. |
| `optimism_bundle_collision_detector` | Detects Optimism bundle collisions that hint at searcher wars. |
| `optimism_cross_domain_message_flow_tracker` | Tracks Optimism cross-domain message queues to flag settlement delays. |
| `optimism_gas_rebate_window_simulator` | Simulates Optimism gas rebate windows to recommend timing-sensitive swaps. |
| `optimism_jit_liquidity_monitor` | Monitors Optimism JIT liquidity spikes for warning signals. |
| `optimism_l1_data_gas_planner` | Optimizes Optimism data gas budgeting for the next submission window. |
| `optimism_latency_breaker_detector` | Detects Optimism latency breaker events before users feel sequencer stalls. |
| `optimism_mempool_backlog_risk_monitor` | Scores Optimism mempool congestion risk and suggests throttle actions for spiky bursts. |
| `optimism_priority_fee_shaper` | Shapes Optimism priority fees to undercut sandwich bots. |
| `optimism_proof_window_reliability_scanner` | Models Optimism proof submission reliability against backlog volatility. |
| `optimism_sequencer_fee_forecaster` | Projects Optimism sequencer fee bands for the next block window using backlog and L1 data costs. |
| `optimism_throughput_ceiling_tracker` | Estimates Optimism throughput headroom vs current usage to plan order flow bursts. |
| `optimism_to_arbitrum_eth_bridge_optimizer` | Optimizes ETH bridge routing from Optimism to Arbitrum with fee and latency heuristics. |
| `optimism_to_arbitrum_govtoken_bridge_optimizer` | Optimizes governance token bridge routing from Optimism to Arbitrum with fee and latency heuristics. |
| `optimism_to_arbitrum_lsd_bridge_optimizer` | Optimizes liquid staking derivative bridge routing from Optimism to Arbitrum with fee and latency heuristics. |
| `optimism_to_arbitrum_stablecoin_bridge_optimizer` | Optimizes stablecoin bridge routing from Optimism to Arbitrum with fee and latency heuristics. |
| `optimism_to_base_eth_bridge_optimizer` | Optimizes ETH bridge routing from Optimism to Base with fee and latency heuristics. |
| `optimism_to_base_govtoken_bridge_optimizer` | Optimizes governance token bridge routing from Optimism to Base with fee and latency heuristics. |
| `optimism_to_base_lsd_bridge_optimizer` | Optimizes liquid staking derivative bridge routing from Optimism to Base with fee and latency heuristics. |
| `optimism_to_base_stablecoin_bridge_optimizer` | Optimizes stablecoin bridge routing from Optimism to Base with fee and latency heuristics. |
| `optimism_tx_priority_curve_optimizer` | Builds a recommended Optimism priority fee curve for latency-sensitive users. |
| `option_pool_modeler` | Evaluates current and proposed option pool sizing plus dilution to shareholders. |
| `options_flow_clustering_model` | Clusters notable options prints to surface stealth positioning. |
| `options_liquidity_pullback_detector` | Detects widening bid-ask spreads and volume drops signaling liquidity stress. |
| `options_open_interest_rotation_monitor` | Identifies large OI rolls indicating positioning shifts. |
| `options_strategy_analyzer` | Aggregates multi-leg option strategy P&L and diagnostics. |
| `options_volatility_smile_plotter` | Builds smile curves from free option chains and overlays realized anchors. |
| `pair_trade_analyzer` | Computes ratio z-scores, correlation, and trade signals for price pairs. |
| `partner_onboarding_validator` | Ensures partner submissions meet baseline technical and compliance requirements. |
| `partner_revenue_share_calculator` | Computes revenue share payouts per partner tier. |
| `payment_gateway_router` | Determines which verification skill should process a payment receipt. |
| `payment_reconciler` | Reconciles Watering Hole payments against invoice records. |
| `payment_terms_optimizer` | Evaluates early-pay discounts to maximize savings within cash constraints. |
| `pdf_report_formatter` | Creates a layout-ready dict for PDF renderers (sections, TOC, metadata). |
| `pe_valuation_dcf` | Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. |
| `peer_holdco_nav_gap_meter` | Ranks peer holdcos by NAV gaps adjusted for discount catalysts. |
| `pendle_impermanent_loss_guardrail` | Simulates Pendle IL exposure for dual-asset pools and recommends caps. |
| `pendle_liquidity_rebalance_playbook` | Builds Pendle liquidity rebalance plans for yield rotations. |
| `pendle_lsd_leverage_spread_modeler` | Models Pendle LSD leverage spreads with health-factor guardrails. |
| `performance_attribution` | Decomposes active return into allocation, selection, and interaction components. |
| `performance_poller_control` | Observe, trigger, or read the status of the Snowdrop Performance Poller subagent (A2A protocol). Actions: 'status' (last run time, posts polled, errors), 'trigger' (run poller immediately via subprocess), 'read_card' (return the A2A agent card JSON), 'read_log' (last N lines of poller log). The poller normally runs every 2h via cron but can be triggered on-demand. |
| `pii_detector` | Finds PII in free-form text and masks the findings. |
| `pik_toggle_modeler` | Builds period schedules for cash and PIK interest accruals. |
| `piotroski_f_score` | Evaluates the nine Piotroski signals to rate financial strength. |
| `pipe_registration_rights_timer` | Follows PIPE resale registration deadlines to anticipate float unlocks. |
| `pitch_deck_generator` | Creates slide-by-slide pitch content for Snowdrop fundraising narratives. |
| `places_search` | Search, discover, and retrieve details for businesses and points of interest using the Google Places API (New). Supports free-text search, nearby discovery, and full place detail lookups. Returns structured business data plus an investment_signal field assessing business density and health for real estate and market analysis. |
| `poison_pill_trigger_analyzer` | Tests thresholds and dilution math for outstanding shareholder rights plans. |
| `polygon_zkevm_data_availability_cost_forecaster` | Forecasts Polygon zkEVM data availability costs when proofs spike. |
| `polygon_zkevm_proof_latency_profiler` | Profiles Polygon zkEVM proof latency and confidence based on queue depth and L1 gas noise. |
| `polygon_zkevm_prover_cluster_health_monitor` | Monitors Polygon zkEVM prover clusters for saturation and fallback readiness. |
| `polygon_zkevm_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Polygon zkEVM sequencer mempools and hints. |
| `polygon_zkevm_state_diff_audit_simulator` | Simulates Polygon zkEVM state diff coverage to spot risky batches before posting. |
| `polygon_zkevm_validity_challenge_planner` | Plans Polygon zkEVM validity challenge playbooks if proofs degrade. |
| `portfolio_rebalancer` | Compares target weights vs current positions and builds pending trade list. |
| `portfolio_stress_test` | Applies historical crash scenarios (2008 GFC, 2020 COVID, Rate Shock) or custom shock tables to a portfolio. Calculates dollar and percentage loss per scenario, identifies the worst-hit asset in each scenario, selects the maximum drawdown scenario overall, and estimates the capital injection needed to recover to the original portfolio value. |
| `portfolio_variance_calc` | Calculate portfolio expected return, variance, standard deviation, Sharpe ratio, and diversification benefit using Modern Portfolio Theory (MPT). |
| `post_mortem_generator` | Creates structured post-mortem Markdown with action items and lessons learned. |
| `post_reorg_equity_liquidity_planner` | Forecasts float, turnover, and lockups for newly listed post-reorg equities. |
| `post_spin_index_inclusion_tracker` | Tracks index add/drop impacts following spin-effective dates. |
| `postgresql_ledger_adapter` | Builds parameterized SQL statements for Ghost Ledger backed by Postgres. |
| `preferred_vs_common_switch_pairer` | Identifies capital structures where preferred/common toggles misprice fundamentals. |
| `premium_estimator` | Provides heuristic premium estimates based on business profile and coverage type. |
| `price_alert_evaluator` | Checks price conditions (above, below, pct_change) and prioritizes alerts. |
| `price_feed_aggregator` | Fetches CoinGecko and Kraken prices then returns the median. |
| `pricing_feed_voter` | Computes a consensus price across vendor feeds and flags quotes outside tolerance bands. |
| `private_credit_term_analyzer` | Computes all-in yields, covenant protection, and risk assessment for private credit facilities. |
| `product_launch_trade_setup` | Compares historical launch announcements to realized demand signals to gauge trade direction. |
| `proforma_generator` | Projects multi-year cash flows, NOI, and returns for income properties. |
| `prompt_ab_tester` | Appends prompt experiment outcomes and computes per-variant stats. |
| `prompt_injection_shield` | Scans incoming agent requests for prompt injection attacks, role-play overrides, encoding tricks, and unauthorized tool access. Returns threat level and blocked tools. |
| `prompt_template_manager` | Provides CRUD operations on config/prompt_templates.json. |
| `proof_of_labor_arbiter` | Scores labor contributions and returns credit recommendations. |
| `proposal_manager` | Submits, lists, fetches, or closes proposals per Snowdrop governance rules. |
| `proxy_fight_vote_pathfinder` | Visualizes proxy math, record dates, and swing ballots for live contested meetings. |
| `pubsub_publisher` | Google Cloud Pub/Sub skill for event streaming between Snowdrop services. Supports publish, pull, topic and subscription management via the Pub/Sub REST API. |
| `python_sdk_generator` | Builds a basic Python client with typed methods for each Snowdrop skill. |
| `quarterly_report_generator` | Summarizes fund performance against benchmarks for the quarter. |
| `railway_deploy_status` | Builds Railway GraphQL queries and parses deployment states when provided. |
| `ralph_wiggum_retry_manager` | Determines whether to retry or escalate tasks per ethics playbook. |
| `rate_card_manager` | Retrieves or updates tier pricing for Watering Hole skills. |
| `rate_limit_cascade` | Downgrades Opus→Sonnet→Haiku→Grok when a model is saturated. |
| `real_estate_tax_escrow` | Calculates monthly escrow reserve requirements for property taxes and insurance. Uses the millage rate system (mills per $1,000 of assessed value). Outputs monthly escrow, annual tax, and combined annual total. |
| `rebalance_trigger` | Checks portfolio split vs. target bands and surfaces recommended skims or reviews. |
| `reconcile` | Daily reconciliation engine. Compares live Kraken exchange balances against the Ghost Ledger (Google Sheets). Emits a CRITICAL alert to Thunder via Telegram if any discrepancy is detected. Zero-tolerance policy. |
| `recovery_runbook_generator` | Outputs a step-by-step recovery plan tailored to the failure type. |
| `referral_reward_calculator` | Determines referral tier, rate, and milestone bonuses. |
| `referral_tracker` | Aggregates referral spend and issues credits to promoters. |
| `refinancing_analyzer` | Evaluates refinance savings, break-even, and NPV for proposed loan terms. |
| `reg_fd_8k_alert_router` | Streams fresh 8-Ks, tags material language, and suggests contextual playbooks. |
| `regulatory_remedy_playbook_builder` | Suggests divestiture candidates and valuation impact based on overlap matrices. |
| `reit_compliance_tester` | Evaluates income/asset/shareholder tests for REIT status. |
| `reit_dividend_analyzer` | Evaluates dividend yield, payout ratios, and tax characterization. |
| `reit_dividend_coverage` | Evaluates REIT dividend sustainability by computing FFO and AFFO payout coverage ratios. Classifies risk as low, medium, or high, and flags dividends at risk of cuts. |
| `reit_dividend_reinvestment_logic` | Executes Dividend Reinvestment Plan (DRIP) logic for a REIT distribution. Calculates whole and fractional shares purchasable at the current share price, computes the blended new cost basis per share, and produces a reinvestment summary suitable for ledger entry. |
| `reit_ffo_calculator` | Calculates REIT Funds From Operations (FFO) and Adjusted FFO (AFFO) per NAREIT standards. FFO adds back real estate depreciation and amortization to GAAP net income and excludes gains/losses on property sales. |
| `reit_nav_calculator` | Values properties via NOI/cap rates to derive NAV per share. |
| `reit_nav_premium_tracker` | Tracks the premium or discount of a REIT's market price relative to Net Asset Value (NAV) per share. Computes a z-score against historical premiums (when provided) and signals overvalued, undervalued, or fair value. |
| `remittance_cost_optimizer` | Ranks cross-border remittance corridors by total cost, identifies cheapest and fastest options, and filters by urgency. |
| `rent_roll_analyzer` | Calculates occupancy, income, loss-to-lease, and lease rollover risk. |
| `repo_value_estimator` | Estimates tokens and dollars needed to rebuild the repo from scratch. |
| `reputation_staking` | Locks reputation points against delivery, quality, or fairness claims. |
| `request_queue_manager` | Manages enqueue/dequeue/peek/stats for agent request queues. |
| `request_rate_limiter` | Enforces per-agent token bucket rate limits and returns retry hints. |
| `research_library_manager` | Publishes and queries Goodwill research papers for the community. |
| `response_cache_manager` | Provides get/set/invalidate operations for skill response cache entries. |
| `revenue_anomaly_detector` | Monitors rolling revenue patterns for drops and spikes. |
| `revenue_per_skill_analyzer` | Aggregates billing records to highlight top-performing skills and concentration |
| `revenue_recognition_checker` | Applies the ASC 606 five-step model to contracts and allocates revenue to obligations. |
| `reverse_morris_trust_matchmaker` | Suggests RMT partners using complementary tax bases and strategic fit. |
| `reverse_termination_fee_stress_test` | Models buyer default risk versus RTF incentives and financing covenants. |
| `review_cost_estimator` | Approximates token/time cost to review a submission. |
| `rights_offering_value_splitter` | Values tradable rights vs. subscription commitments using historical take-up rates. |
| `roi_annotator` | Enriches ledger transactions with qualitative ROI commentary. |
| `route_optimizer` | Google Route Optimization API skill for fleet tour optimization, point-to-point directions, and distance matrix calculations. Supports real estate inspections, logistics planning, and multi-stop delivery sequencing. |
| `runway_scenario_modeler` | Projects runway months under bull/base/bear net burn assumptions. |
| `rwa_oracle_block_timestamp_gapper` | Measures block timestamp gaps affecting TWAP-driven oracle updates. |
| `rwa_oracle_carbon_asset_price_guard` | Validates carbon offset price feeds against EU ETS and voluntary market data. |
| `rwa_oracle_cds_spread_checker` | Checks corporate CDS spreads feeding private credit tokens for stale data. |
| `rwa_oracle_collateral_liquidity_flagger` | Flags collateral where oracle liquidity inputs diverge from on-chain trades. |
| `rwa_oracle_cross_chain_feed_diff` | Diffs oracle values across chains to detect delayed relays or bridge drifts. |
| `rwa_oracle_data_vendor_quorum_checker` | Ensures quorum logic across multiple vendors is functioning and weighted correctly. |
| `rwa_oracle_distribution_waterfall_recon` | Checks that oracle-distributed cashflows match waterfall calculations per tranche. |
| `rwa_oracle_energy_ppa_price_monitor` | Monitors PPA settlement curves versus on-chain kilowatt-hour pricing oracles. |
| `rwa_oracle_fallback_latency_monitor` | Measures latency when feeds fall back to secondary providers during outages. |
| `rwa_oracle_forestry_land_value_checker` | Compares forestry land appraisal indexes with oracle quotes backing timber tokens. |
| `rwa_oracle_inflation_swap_bridge` | Maps inflation swap fixings to CPI-linked RWA oracle inputs. |
| `rwa_oracle_market_data_downtime_buffer` | Projects NAV impact when core venues go dark and oracles rely on stale buffers. |
| `rwa_oracle_metals_inventory_indexer` | Reconciles LME inventory data against tokenized warehouse receipt feeds. |
| `rwa_oracle_muni_bond_price_sync` | Aligns municipal bond marks from EMMA with on-chain oracle quotes and flags spreads beyond tolerance. |
| `rwa_oracle_performance_fee_shadow_calc` | Runs independent performance-fee calculations to cross-check oracle output. |
| `rwa_oracle_price_ladder_sanity_checker` | Validates laddered price levels for order-book fed RWAs remain monotonic. |
| `rwa_oracle_primary_secondary_spread_checker` | Compares primary issuance prices with secondary token trading to spot gaps. |
| `rwa_oracle_private_credit_nav_tracker` | Aggregates private credit NAV statements and reconciles them with streaming oracle NAVs. |
| `rwa_oracle_real_estate_index_blender` | Blends Case-Shiller and proprietary comps to smooth real-estate NAV ticks feeding tokens. |
| `rwa_oracle_real_estate_sale_comp_checker` | Confirms sale comparables feeding residential tokens align with MLS data. |
| `rwa_oracle_shipping_rate_feed_watcher` | Checks Baltic Dry and Freightos prints versus oracle shipping feeds for divergence. |
| `rwa_oracle_sofr_libor_spread_monitor` | Tracks SOFR-LIBOR spreads embedded in oracle discount factors for loans. |
| `rwa_oracle_stress_scenario_projector` | Applies stress shocks to oracle inputs to preview NAV drawdowns before they post. |
| `rwa_oracle_t_bill_fx_cross_checker` | Ensures T-bill tokens priced in non-USD denominations reflect live FX crosses. |
| `rwa_oracle_token_nav_consistency_guard` | Confirms oracle NAV outputs reconcile with issuer-reported NAV statements. |
| `rwa_oracle_treasury_curve_reconciler` | Compares oracle Treasury curves with FRED benchmarks to ensure discount factors match. |
| `rwa_oracle_volume_weight_consistency` | Ensures oracle VWAP calculations match reported venue volumes. |
| `rwa_oracle_weather_index_checker` | Validates weather derivative indexes powering parametric insurance tokens. |
| `rwa_private_credit_collateral_file_attestor` | Confirms collateral file hashes and borrowing base calculations for on-chain lenders. |
| `rwa_private_credit_covenant_packet_checker` | Parses covenant reports to ensure breach notices trigger token gating logic. |
| `rwa_private_credit_loan_servicer_cashflow_validator` | Reconciles servicer remittance files against token payout streams for private credit pools. |
| `rwa_private_credit_nav_facility_limit_monitor` | Checks NAV facility utilization versus limits before approving new draws. |
| `rwa_private_credit_payment_default_signal_router` | Routes delinquency signals to holders and pauses distributions until resolved. |
| `rwa_real_estate_appraisal_report_consistency_checker` | Checks appraisal comparables and LTV metrics for consistency with disclosure packets. |
| `rwa_real_estate_construction_permit_tracker` | Aligns construction draw schedules with permit milestones to gate unlocks. |
| `rwa_real_estate_deed_forgery_scanner` | Analyzes notarized deed uploads for signature anomalies and tamper patterns before minting tokens. |
| `rwa_real_estate_environmental_report_checker` | Validates environmental assessments and ensures mitigation steps are recorded on-chain. |
| `rwa_real_estate_escrow_disbursement_chain_watcher` | Traces escrow disbursements to ensure fiat releases mirror token allocation events. |
| `rwa_real_estate_hoa_compliance_verifier` | Checks HOA dues payments and covenant compliance before distributions are released. |
| `rwa_real_estate_insurance_binder_attestor` | Validates property insurance binders, coverage limits, and renewal dates pre-transfer. |
| `rwa_real_estate_occupancy_certificate_validator` | Verifies certificates of occupancy and permit status for new developments. |
| `rwa_real_estate_parcel_zoning_attestor` | Confirms each parcel's zoning class via municipal APIs to enforce token-level use restrictions. |
| `rwa_real_estate_property_liens_status_monitor` | Pulls lien registries to detect new encumbrances on token collateral. |
| `rwa_real_estate_property_tax_ledger_matcher` | Matches property tax receipts versus blockchain cash flows to confirm taxes remain current. |
| `rwa_real_estate_rent_roll_cashflow_verifier` | Audits rent-roll statements against stablecoin remittance data for income-backed tokens. |
| `rwa_real_estate_tenant_kyc_rollup` | Aggregates tenant KYC attestations to verify income streams backing lease tokens. |
| `rwa_real_estate_title_registry_sync` | Cross-checks tokenized deed metadata with county title registries and surfaces mismatched parcel identifiers. |
| `rwa_real_estate_utility_arrears_detector` | Flags properties with unpaid utility balances or liens impacting collateral quality. |
| `rwa_treasury_auction_allotment_matcher` | Matches primary auction allotments to token mint quantities to prevent synthetic supply. |
| `rwa_treasury_collateral_chain_snapshotter` | Builds snapshots of collateral pledges to avoid double counting the same bills. |
| `rwa_treasury_cusip_whitelist_verifier` | Ensures only approved CUSIPs appear in wrapped Treasury vaults by reconciling mint payloads with issuance calendars. |
| `rwa_treasury_discount_curve_checker` | Compares implied token discounts to the live Treasury curve to spot mispricing. |
| `rwa_treasury_fedwire_settlement_audit` | Maps Fedwire settlement receipts to blockchain proofs for custody assurance. |
| `rwa_treasury_maturity_schedule_guardian` | Checks that token maturity ladders align with underlying Treasury maturity dates. |
| `rwa_treasury_rebate_payment_tracker` | Tracks rebate and coupon-equivalent flows into token treasury accounts. |
| `rwa_treasury_repo_haircut_compliance_monitor` | Checks repo leverage agreements to ensure haircuts stay within disclosures. |
| `rwa_treasury_safekeeping_receipt_checker` | Validates safekeeping receipts and custodial chain-of-control for token wrappers. |
| `rwa_treasury_sanctions_screen` | Screens custodians and counterparties for OFAC flags before settlement. |
| `safe_note_converter` | Calculates SAFE conversion price, shares, and founder dilution. |
| `sanctions_network_monitor` | Cross-check wallet exposures against sanctions feeds and return flagged entities. |
| `sanctions_screener` | Checks entities/wallets against curated sanctions heuristics. |
| `sar_generator` | Drafts FinCEN SAR payloads without auto-filing. |
| `scaling_decision_engine` | Evaluates telemetry against thresholds to suggest scale up/down/hold. |
| `scheduled_workflow_trigger` | Determines due, overdue, and next trigger times for workflows. |
| `schema_validator` | Checks arbitrary data payloads against JSON Schema definitions (subset). |
| `scroll_data_availability_cost_forecaster` | Forecasts Scroll data availability costs when proofs spike. |
| `scroll_proof_latency_profiler` | Profiles Scroll proof latency and confidence based on queue depth and L1 gas noise. |
| `scroll_prover_cluster_health_monitor` | Monitors Scroll prover clusters for saturation and fallback readiness. |
| `scroll_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Scroll sequencer mempools and hints. |
| `scroll_state_diff_audit_simulator` | Simulates Scroll state diff coverage to spot risky batches before posting. |
| `scroll_validity_challenge_planner` | Plans Scroll validity challenge playbooks if proofs degrade. |
| `secondary_offering_dilution` | Evaluates dilution, proceeds, and TERP for primary/secondary offerings. |
| `secrets_audit_monitor` | Checks whether required secrets are present in the environment and flags missing/empty variables. |
| `section382_cap_table_guard` | Simulates ownership shifts to protect Section 382 limits. |
| `sector_spin_pair_alignment_tool` | Builds hedged baskets pairing spin parent and pure-play comps. |
| `securitization_cashflow_modeler` | Generates month-by-month cash flow projections including CPR/CDR and servicing fees. |
| `self_audit_daily` | Compares planned vs executed actions, logs discrepancies, and triggers freezes if needed. |
| `share_block_crossing_matchmaker` | Matches block trade appetite to reduce slippage in structural arb legs. |
| `share_class_liquidity_gap_radar` | Spots dual share class liquidity premiums that invite arb. |
| `share_lockup_expiry_pressure_meter` | Quantifies lockup expirations' float impact and price response odds. |
| `shareholder_vote_turnout_forecaster` | Projects vote outcomes by modeling historical turnout, proxy advisor stances, and current register data. |
| `sharpe_ratio_calculator` | Calculates Sharpe, Sortino, and ancillary performance stats. |
| `sheet_pruner` | Prevents data bloat by autonomously removing logs older than the retention period from the Command Center. |
| `sheets_to_postgres_migrator` | Produces SQL/ETL plan for moving Ghost Ledger tabs into PostgreSQL tables. |
| `short_interest_crunch_indicator` | Combines short interest days-to-cover with catalyst calendar to time squeezes. |
| `signature_verifier` | Verifies HMAC-SHA256 signatures for incoming agent messages. |
| `skeptic_challenge_generator` | Produces a structured counter-position with risks and precedents for a thesis. |
| `skew_jump_risk_meter` | Quantifies skew jump risk around catalysts using historical skew shocks. |
| `skew_steepener_backtest_lab` | Backtests skew steepener ideas across time using synthetic option data. |
| `skill_builder` | Meta-skill: takes a plain-English skill description and generates a production-ready Snowdrop Python skill module via the Assembly Line (Haiku drafts, Sonnet polishes, Opus certifies for jury-tier complexity). Optionally writes the result to disk. |
| `skill_demo_generator` | Creates narrative demo content, sample IO, and use cases for any skill. |
| `skill_dependency_mapper` | Scans skill files for env vars, internal imports, and external API references. |
| `skill_dispatcher` | Maps classified intents and extracted entities into MCP skill payloads. |
| `skill_doc_generator` | Renders markdown docs for a skill module's TOOL_META. |
| `skill_marketplace_listing` | Turns the skill registry into a Moltbook/Fragment-friendly markdown listing. |
| `skill_performance_ranker` | Combines reliability, latency, popularity, and satisfaction into a composite score. |
| `skill_quality_decay_tracker` | Measures error rate drift and maintenance burden for community skills over time. |
| `skill_review_pipeline` | Runs static review checks on submitted community skill code. |
| `skill_royalty_splitter` | Calculates revenue splits for community skills and tracks contributor balances. |
| `skill_search_engine` | Ranks skills by textual similarity to a query string. |
| `skill_self_tester` | Generates test payloads from TOOL_META.inputSchema and runs the skill function. |
| `skill_telemetry_aggregator` | Process telemetry samples from Snowdrop skills and emit aggregated health metrics with outlier detection. |
| `slack_alert` | Send a message to Snowdrop's Slack channel. Used for real-time alerts to Thunder: price moves, audit results, integrity alerts, status updates. Actions: send (post message), ping (connectivity test). |
| `slippage_protection_buffer` | Calculate maximum allowable slippage for a trade using bid/ask spread and order book depth. Sets max_slippage = spread + estimated_impact + 10% buffer. |
| `smart_contract_access_control_diff_checker` | Diffs access-control lists between versions to highlight missing roles. |
| `smart_contract_authority_matrix_auditor` | Builds a permission matrix for each method to catch privilege creep. |
| `smart_contract_bridge_finality_checker` | Verifies bridge contracts enforce finality depth before crediting funds. |
| `smart_contract_cross_chain_message_profiler` | Profiles bridge message flow for ack failures or stalled packets. |
| `smart_contract_cross_pool_drain_simulator` | Runs stress flows across linked pools to detect capital draining routes. |
| `smart_contract_delegatecall_guardrail` | Inspects delegatecall targets to ensure they respect access control and immutability assumptions. |
| `smart_contract_emergency_pause_validator` | Validates pause pathways ensure multi-sig approvals and enforce cooldowns. |
| `smart_contract_fee_switch_diff_checker` | Compares fee switch states across deployments to expose unnoticed toggles. |
| `smart_contract_flashloan_pressure_tester` | Runs deterministic flash-loan scenarios to measure collateral buffers and slippage thresholds. |
| `smart_contract_governance_quorum_analyzer` | Evaluates historical quorum attainment to estimate hostile takeover risk. |
| `smart_contract_infinite_mint_sentinel` | Detects code paths capable of unlimited minting without supply caps. |
| `smart_contract_interest_rate_jump_detector` | Stress-tests rate models for discontinuities following governance votes. |
| `smart_contract_liquidation_waterfall_checker` | Validates liquidation waterfalls respect seniority rules across tranches. |
| `smart_contract_liquidity_sink_detector` | Detects pools where withdrawals can be blocked via hooks or sticky fee logic. |
| `smart_contract_mev_backrun_scorer` | Scores how easily transactions can be backrun given hooks and mempool patterns. |
| `smart_contract_native_asset_sweep_detector` | Ensures no function can sweep native chain assets without quorum approval. |
| `smart_contract_nonce_management_monitor` | Ensures relayers clear queued nonces to prevent stuck meta-transactions. |
| `smart_contract_oracle_dependency_graph` | Constructs dependency graphs of oracle feeds to find single points of failure. |
| `smart_contract_oracle_sandwich_risk_scanner` | Identifies oracle updates that traders can sandwich before settlement. |
| `smart_contract_paymaster_abuse_detector` | Analyzes ERC-4337 paymaster policies for unlimited sponsor risk. |
| `smart_contract_permit_replay_guard` | Validates permit signatures expire correctly and integrate nonce tracking. |
| `smart_contract_precision_loss_guard` | Checks decimal math routines to prevent precision loss on rebasing assets. |
| `smart_contract_price_staleness_alarm` | Calculates price feed staleness windows and raises alerts when data age exceeds limits. |
| `smart_contract_protocol_fee_recon` | Reconciles protocol fee accounting with actual treasury balances. |
| `smart_contract_reentrancy_surface_mapper` | Simulates nested calls and flags storage slots lacking reentrancy guards. |
| `smart_contract_reward_emission_checker` | Compares scheduled reward emissions to live supply to catch runaway inflation. |
| `smart_contract_signature_malleability_scan` | Checks signature verification logic for malleability or unchecked parameters. |
| `smart_contract_state_desync_simulator` | Simulates sequencer delays to predict when L2 states diverge from L1 finality. |
| `smart_contract_stateful_callback_tracker` | Tracks callbacks to ensure downstream states revert when upstream calls fail. |
| `smart_contract_storage_collision_detector` | Analyzes proxy storage layouts for slot collisions across upgrades. |
| `smart_contract_token_allowance_drift_checker` | Monitors allowances versus expected spend to highlight risky approvals. |
| `smart_contract_unbounded_loop_detector` | Scans bytecode for unbounded loops that can be griefed via block gas limits. |
| `smart_contract_upgrade_timelock_checker` | Verifies upgrade timelocks meet governance thresholds and cannot be bypassed. |
| `smart_contract_validator_slash_risk_checker` | Estimates slash exposure by simulating validator misbehavior scenarios. |
| `smart_contract_vault_share_dilution_checker` | Models share issuance math to catch dilution vectors for vault depositors. |
| `sol_balance_checker` | Calls Solana RPC getBalance and returns SOL for the configured wallet. |
| `sol_transfer_builder` | Constructs Solana transfer payloads and fee estimates pending approval. |
| `solana_jit_execution` | Calculate Just-in-Time liquidity provisioning plan for a Solana AMM pool with yield estimation and risk scoring. |
| `sovereign_debt_yield_curve` | Computes sovereign bond spreads over US Treasuries, builds yield curves, and identifies inversions for Global South debt analysis. |
| `sovereign_fiat_bridge` | Converts sovereign fiat currency to a target digital asset for treasury onboarding. Applies jurisdiction-specific regulatory surcharges on top of a base protocol fee. Estimates settlement time and enumerates regulatory requirements for the given jurisdiction. |
| `sovereign_reserves_analyzer` | Analyzes sovereign reserve composition (fiat/gold/digital) and compares against IMF adequacy metrics. |
| `sovereign_wealth_alpha_source` | Screens and ranks sovereign wealth fund investment opportunities by return/risk ratio against configurable criteria. |
| `spac_closure_probability_rater` | Scores SPAC deals using redemption levels, sponsor incentives, and regulatory risk. |
| `special_dividend_arbitrage_planner` | Evaluates pre/post special dividend payout value capture tactics including deep ITM options. |
| `spin_stub_pair_trade_planner` | Designs hedges between parent and spin based on float/weight forecasts. |
| `spin_tax_free_safe_harbor_checker` | Tests transactions against IRS safe harbor requirements for tax-free status. |
| `spinoff_sum_of_the_parts_modeler` | Aggregates segment data into SOP valuations to benchmark spin stub pricing. |
| `spread_curve_speedometer` | Tracks spread compression velocity vs. historical analogs to size exposures. |
| `sprint_planner` | Selects backlog tasks for the sprint based on priority, capacity, and dependencies. |
| `stakewise_impermanent_loss_guardrail` | Simulates StakeWise IL exposure for dual-asset pools and recommends caps. |
| `stakewise_liquidity_rebalance_playbook` | Builds StakeWise liquidity rebalance plans for yield rotations. |
| `stakewise_lsd_leverage_spread_modeler` | Models StakeWise LSD leverage spreads with health-factor guardrails. |
| `staking_reward_tracker` | Summarizes staking rewards, projected income, and outstanding claims per validator. |
| `stapled_security_basis_monitor` | Breaks stapled units into components to highlight mispriced legs. |
| `starknet_data_availability_cost_forecaster` | Forecasts Starknet data availability costs when proofs spike. |
| `starknet_proof_latency_profiler` | Profiles Starknet proof latency and confidence based on queue depth and L1 gas noise. |
| `starknet_prover_cluster_health_monitor` | Monitors Starknet prover clusters for saturation and fallback readiness. |
| `starknet_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Starknet sequencer mempools and hints. |
| `starknet_state_diff_audit_simulator` | Simulates Starknet state diff coverage to spot risky batches before posting. |
| `starknet_validity_challenge_planner` | Plans Starknet validity challenge playbooks if proofs degrade. |
| `statistical_anomaly_detector` | Flags z-score anomalies across global or rolling windows. |
| `status_report_generator` | Formats Snowdrop execution updates into a markdown status report. |
| `strategy_backtester` | Runs deterministic backtests for rule-based trading strategies. |
| `structured_logger` | Appends structured log entries with correlation metadata to a JSONL file. |
| `structured_note_hedge_unwinder` | Estimates issuer hedging unwind pressure around callable structured notes. |
| `structured_product_greeks_unwrapper` | Decomposes popular retail structured products into Greek exposures. |
| `stub_value_residual_calculator` | Estimates stub valuation for partial deals where equity carve-outs persist. |
| `subscription_doc_parser` | Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores. |
| `subscription_manager` | Identifies subscriptions due for billing and drafts charge records. |
| `subsector_pair_trade_curator` | Curates structural pair trades using variance-covariance analytics. |
| `supervoting_conversion_timer` | Tracks super-voting share collapse triggers to anticipate governance shifts. |
| `supply_chain_disruption_signal_board` | Uses shipping-data and supplier earnings to anticipate company-specific supply hits. |
| `support_escalation_router` | Determines routing paths for support tickets based on category, tier, and urgency. |
| `support_ticket_manager` | Creates, updates, closes, and lists support tickets with SLA tracking. |
| `swap_benchmark_mismatch_detector` | Flags swaps referencing off-benchmark underlyings that create synthetic arb. |
| `swarm_message_router` | Validates sender/recipient roles and produces routing envelopes. |
| `synergy_realization_probabilizer` | Scores synergy credibility via comps, procurement data, and management track record. |
| `synthetic_market_data_generator` | Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills. |
| `synthetic_short_interest_balancer` | Monitors synthetic short build-up across swaps vs. physical borrow. |
| `system_health_composite` | Rolls subsystem telemetry into a weighted score and recommendations. |
| `taiko_data_availability_cost_forecaster` | Forecasts Taiko data availability costs when proofs spike. |
| `taiko_proof_latency_profiler` | Profiles Taiko proof latency and confidence based on queue depth and L1 gas noise. |
| `taiko_prover_cluster_health_monitor` | Monitors Taiko prover clusters for saturation and fallback readiness. |
| `taiko_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Taiko sequencer mempools and hints. |
| `taiko_state_diff_audit_simulator` | Simulates Taiko state diff coverage to spot risky batches before posting. |
| `taiko_validity_challenge_planner` | Plans Taiko validity challenge playbooks if proofs degrade. |
| `tail_event_rehedge_scheduler` | Automates re-hedge reminders when vol regime shifts breach thresholds. |
| `tail_hedge_payoff_matcher` | Matches portfolio beta to best-fit tail hedge structures with payoff tables. |
| `tailscale_mesh_healthcheck` | Pulls device metadata from Tailscale and surfaces online/offline state. |
| `target_shareholder_overlap_mapper` | Maps common holders between acquirer and target to forecast vote outcomes. |
| `task_dependency_resolver` | Performs topological sorting and surfaces parallelizable groups. |
| `tax_basics_guide` | Shares plain-language US tax basics by entity type (goodwill only). |
| `tax_loss_harvest_window_finder` | Identifies crowded losers with elevated December bounce odds using seasonal factor models. |
| `tax_loss_harvester` | Ranks positions by after-tax savings potential with wash sale warnings. |
| `telegram_alert_formatter` | Formats alerts using Telegram MarkdownV2 with escaping and CTA support. |
| `telegram_command_router` | Parses Telegram commands (/balance, /audit, /brief, /price, /status, /help). |
| `telemetry_collector` | Appends anonymous usage telemetry after stripping PII. |
| `telemetry_reporter` | Aggregates telemetry events by dimension with latency/error metrics. |
| `telnyx_alert` | Drafts Telnyx SMS payloads to notify Thunder of high-priority events. |
| `tenant_credit_analyzer` | Scores tenant credit strength based on financials and lease metrics. |
| `tender_offer_price_response_simulator` | Projects price paths for issuer/third-party tender offers across acceptance levels. |
| `term_sheet_analyzer` | Evaluates post-money, ownership, and liquidation waterfalls for venture deals. |
| `theta_decay_heatmap_builder` | Visualizes theta decay pockets across expiries and strikes. |
| `three_statement_modeler` | Generates linked financial statements using indirect cash flow method. |
| `three_way_reconciliation_bot` | Matches GL, administrator, and custodian balances to highlight breaks exceeding tolerance. |
| `threshold_monitor` | Evaluates metrics against warning and critical thresholds. |
| `thunder_executive_briefing` | Generates a concise, plain-English daily executive briefing for Thunder (operator). Synthesises portfolio value, P&L, open alerts, reconciliation status, and market movers into a human-readable summary. Classifies overall severity as routine, attention, or urgent and surfaces action items. |
| `thunder_signal` | Sends a severity-tiered Telegram alert to Thunder (the Operator). Severity levels: CRITICAL (vault breach, reconciliation failure), WARNING (Sybil infiltration, threshold breach), INTEL (general updates, Great Day). |
| `ticking_fee_tracker` | Calculates ticking-fee accrual vs. expected closing to inform spread carry trades. |
| `tif_district_calculator` | Projects increment revenue and coverage for TIF districts over the term. |
| `timezone_scheduler` | Converts event timestamps into relevant time zones and flags off-hour meetings. |
| `tip_pool_distributor` | Splits gratuities by hours worked and role multipliers for Watering Hole staff. |
| `token_contract_validator` | Flags risky token authority settings and liquidity constraints. |
| `token_cost_tracker` | Logs model API usage and enforces the $50/day spend cap. |
| `token_efficiency_benchmarker` | Compares tokens per skill/line/quality across internal and community contributors. |
| `token_estimator` | Estimates token counts and costs across Claude/GPT/Gemini families. |
| `token_standard_aml_risk_timer` | Applies dynamic AML cooldown timers when risk scores breach thresholds. |
| `token_standard_audit_trail_packer` | Packages on-chain and off-chain audit trails for regulator-ready exports. |
| `token_standard_beneficial_owner_registry_bridge` | Bridges beneficial owner registries into token KYC proofs for regulators. |
| `token_standard_control_person_limit_monitor` | Tracks beneficial ownership percentages to enforce control-person caps. |
| `token_standard_corporate_actions_allocator` | Automates corporate action allocation tables for partitioned cap tables. |
| `token_standard_erc1400_document_registry_sync` | Keeps ERC-1400 document URIs synced with latest prospectus filings. |
| `token_standard_erc1400_issuance_policy_checker` | Confirms ERC-1400 issuance hooks adhere to disclosure-driven policies. |
| `token_standard_erc1400_redemption_flow_modeler` | Simulates ERC-1400 redemption flows to ensure certificate revocations propagate. |
| `token_standard_erc3643_hook_validator` | Checks ERC-3643 validation hooks execute within gas and return proper codes. |
| `token_standard_erc3643_partition_guard` | Ensures partition balances respect transfer restrictions across partitions. |
| `token_standard_erc3643_whitelist_enforcer` | Validates ERC-3643 allowlists against investor registries before transfers. |
| `token_standard_escrow_release_scheduler` | Schedules escrow release events based on oracle-verified milestones. |
| `token_standard_geofence_policy_checker` | Enforces geo-fencing policies at the smart-contract level before transfers settle. |
| `token_standard_liquidation_preference_mapper` | Maps liquidation preference stacks to ensure payouts follow documentation. |
| `token_standard_mica_security_token_classifier` | Runs MiCA tests to classify tokens as financial instruments requiring passporting. |
| `token_standard_mica_utility_token_guardrail` | Checks MiCA utility token criteria to ensure consumer disclosures are adequate. |
| `token_standard_multi_chain_supply_auditor` | Audits circulating supply across chains to prevent double listings. |
| `token_standard_oracle_binding_tester` | Tests failover paths for oracle binding functions within compliance wrappers. |
| `token_standard_prospectus_linker` | Ensures wallets receive the latest prospectus hash before participating in offerings. |
| `token_standard_redemption_notice_builder` | Crafts redemption notice packets with deadlines and KYC refresh requests. |
| `token_standard_registrar_sync_agent` | Synchronizes token transfer agents with smart-contract registrars in near-real time. |
| `token_standard_risk_scorecard_generator` | Generates composite risk scorecards per investor wallet for compliance teams. |
| `token_standard_routing_number_verifier` | Validates routing and account numbers used for fiat bridges in compliance workflows. |
| `token_standard_rwa_oracle_binding_validator` | Verifies tokens consume signed oracle data per governance charter. |
| `token_standard_sanctions_attestor` | Confirms sanctions screening proofs are attached to each restricted transfer. |
| `token_standard_secondary_liquidity_gater` | Controls secondary trading windows based on issuer-defined liquidity tiers. |
| `token_standard_solvency_ratio_checker` | Checks issuer solvency ratios versus promised buffers before new issuance. |
| `token_standard_tax_withholding_engine` | Calculates withholding schedules per jurisdiction before stablecoin payouts. |
| `token_standard_transfer_restriction_matrix` | Generates restriction matrices mapping jurisdiction plus investor tier combinations. |
| `token_standard_travel_rule_payload_builder` | Builds Travel Rule payloads for off-ramp transactions initiated by RWA tokens. |
| `token_supply_modeler` | Projects circulating supply month by month with mint and burn events. |
| `token_swap_estimator` | Estimates CFMM swap execution with slippage buffer for Thunder review. |
| `ton_balance_checker` | Queries TON Center for the configured wallet and returns TON balances. |
| `ton_payment_verifier` | Validates TON transactions for Snowdrop payments without broadcasting funds. |
| `ton_transfer_builder` | Constructs TON transfer payloads without broadcasting. |
| `ton_usdg_yield_tracker` | Calculates accrued USDG yield for TON staking ladders. |
| `ton_w5_gasless_transfer` | Build TON W5 wallet gasless transfer payload using battery sponsorship for zero-fee TON movements. |
| `tracking_stock_basis_arbitrageur` | Models tracking stock dislocations vs. parent share price sensitivity. |
| `tracking_stock_break_even_solver` | Computes break-even for tracking stock conversions and rollups. |
| `trade_settlement_lc_logic` | Validates Letters of Credit against UCP 600 international rules, checks document completeness, and generates settlement recommendations. |
| `tranche_analyzer` | Calculates tranche credit enhancement, expected loss, and implied ratings. |
| `transaction_anomaly_flagger` | Scores transactions for amount, counterparty, category, and timing anomalies. |
| `transaction_freeze` | Activates the global freeze flag so downstream payment skills stop immediately. |
| `transaction_ingest_bridge` | Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. |
| `transaction_sim_pre_flight` | Simulates an on-chain transaction in isolation before submission. Checks for insufficient balances, high slippage, and other failure conditions. Returns projected new balances, estimated gas cost in USD, and a success probability score derived from balance adequacy and warning count. |
| `treasury_sweep_recommender` | Identifies idle cash available for sweeps and proposes destinations (pending Thunder). |
| `trial_balance_generator` | Aggregates journal entries into account-level debit/credit totals. |
| `trial_balance_snapshotter` | Converts ledger entries into a base-currency trial balance and highlights NAV deltas. |
| `triple_net_reconciliation` | Reconciles estimated NNN (triple-net) lease pass-through charges (CAM, insurance, property taxes) against actual year-end costs. Determines per-category variance and whether the tenant owes a true-up payment or is owed a credit. |
| `trust_score_calculator` | Combines signals such as payments, vouches, and disputes into a trust tier. |
| `unsponsored_adr_signal_matrix` | Scores unsponsored ADR launches by comparing demand signals and float constraints. |
| `uptime_tracker` | Calculates uptime %, MTBF, MTTR, and outage extremes from heartbeat logs. |
| `usage_heatmap_generator` | Buckets skill requests into hour/day heatmap bins for usage insights. |
| `usd_jpy_carry_trade_monitor` | Analyzes USD/JPY carry trade profitability using US vs Japan yield differentials and synthetic FX volatility. |
| `usdc_payment_verifier` | Validates Solana USDC transfers by comparing signature, amount, and wallets. |
| `value_at_risk` | Computes multi-level VaR and CVaR via historical simulation. |
| `variance_swap_mark_to_market_estimator` | Calculates MTM on listed variance swaps using free realized data. |
| `velocity_tracker` | Summarizes velocity averages, trend, and predictability over past sprints. |
| `vendor_channel_check_synthesizer` | Aggregates public datapoints (earnings calls, supply chain indices) into actionable sales inflection alerts. |
| `vendor_cost_comparator` | Computes daily/monthly spend per provider and ranks by cost-effectiveness. |
| `vendor_due_diligence` | Scores vendor fit based on uptime, pricing, certifications, and experience. |
| `vendor_risk_assessor` | Evaluates concentration risk, SPOFs, and diversification across vendors. |
| `vendor_sla_monitor` | Evaluates uptime and latency metrics vs SLA targets for each vendor. |
| `venture_debt_amortization` | Generates a complete monthly payment schedule for a venture debt instrument with an interest-only (IO) period followed by a fully-amortizing repayment period. Optionally calculates the warrant coverage value granted to the lender as a percentage of principal. |
| `venture_return_analyzer` | Computes proceeds for preferred vs common across exit scenarios, including participation caps. |
| `verify_hurdle_rate` | Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation. |
| `vertex_ai_inference` | Call Vertex AI Gemini models for text generation, analysis, or embeddings. Uses Vertex AI REST API with explicit service account credentials — no gcloud, no ADC. Supports gemini-2.0-flash-exp (fastest), gemini-1.5-pro (most capable), gemini-1.5-flash. |
| `vintage_year_analyzer` | Compares funds across vintages and computes quartiles/PME proxies. |
| `vintage_year_benchmarking` | Benchmarks a private equity fund's performance against vintage-year peer data. Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, determines quartile rank (Q1=top), and produces a side-by-side comparison table for TVPI, DPI, and IRR. |
| `vix_term_structure_analyzer` | Charts VIX futures curve shape vs. realized vol to identify steepening trades. |
| `vol_carry_roll_down_alerts` | Alerts when rolling long-vol positions offers attractive carry improvements. |
| `vol_surface_regime_classifier` | Labels vol regimes (contango/backwardation) and ties them to macro states. |
| `volatility_etf_decay_tracker` | Tracks decay and rebalance drag in vol-linked ETFs. |
| `volatility_risk_premium_surface_plotter` | Maps VRP across tenors and strikes for strategy selection. |
| `volga_vanna_sensitivity_mapper` | Computes second-order Greeks to guide exotic options hedging. |
| `vote_tabulator` | Counts proposal votes and checks for mandates via 1-sigma upvote threshold. |
| `wallets_check` | Checks on-chain balances versus Ghost Ledger and enforces $0.00 tolerance. |
| `warranty_breach_risk_meter` | Uses sector incident databases to estimate reps and warranties breach odds. |
| `wash_sale_detector` | Flags loss sales with repurchases inside the 30-day wash window. |
| `watering_hole_order_router` | Quotes Watering Hole skill requests via the bonding curve, assigns the correct skill, and returns billing plus dispatch telemetry. |
| `weather_lookup` | Fetch current weather, multi-day forecasts, or historical weather data for any location using the Google Weather API. Returns structured weather metrics plus a commodity_signal field flagging weather-driven market implications for agricultural futures and supply chain analysis. |
| `web_of_trust_manager` | Records vouches between agents and exposes trust graph stats. |
| `webhook_receiver` | Verifies webhook signatures and normalizes payloads. |
| `websocket_market_ingest` | Build WebSocket connection and parser configurations for real-time market data ingestion from Kraken or Binance. |
| `weekly_pnl_report` | Aggregates revenue and expense items into a weekly P&L rollup. |
| `what_if_engine` | Applies scenario overrides to a base business case and projects outcomes. |
| `white_label_config_generator` | Produces config YAML structure for franchise operators with branding hooks. |
| `withholding_obligation_tracker` | Compute gross vs. net distributions and withholding requirements per LP. |
| `workflow_engine` | Evaluates workflow dependencies and surfaces next executable steps. |
| `x_sentiment_grok` | Constructs xAI Grok payloads for sentiment queries. |
| `xp_calculator` | Tallies XP from recent activities and estimates level progression. |
| `yield_curve_analyzer` | Classifies curve shape and recession signals from key spreads. |
| `zksync_data_availability_cost_forecaster` | Forecasts zkSync data availability costs when proofs spike. |
| `zksync_proof_latency_profiler` | Profiles zkSync proof latency and confidence based on queue depth and L1 gas noise. |
| `zksync_prover_cluster_health_monitor` | Monitors zkSync prover clusters for saturation and fallback readiness. |
| `zksync_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across zkSync sequencer mempools and hints. |
| `zksync_state_diff_audit_simulator` | Simulates zkSync state diff coverage to spot risky batches before posting. |
| `zksync_validity_challenge_planner` | Plans zkSync validity challenge playbooks if proofs degrade. |
| `zoning_impact_analyzer` | Analyzes parcel zoning rules to determine maximum buildable density, parking requirements, and compliance of a proposed land use. Returns restriction list and compliant flag. |

---

## Ecosystem Topology
For a broader view of how the **Snowdrop MCP** fits into the larger multi-agent architecture (including The Watering Hole, Moltbook, and Conductive Admin), please refer to the [ECOSYSTEM_TOPOLOGY.md](ECOSYSTEM_TOPOLOGY.md) file.

# Snowdrop MCP — Skills Directory

## Executive Summary
This document provides a comprehensive, auto-generated directory of all skills available on the Snowdrop MCP server. It details the exact count and capabilities of both **Premium** (proprietary/paid) and **Free** skills currently loaded in production. Generated: `2026-02-28T00:02:53.236038+00:00`. The skill count reflects the local Python environment. For the count of skills deployed to Cloud Run, call the /health endpoint at https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/health. To regenerate: `python scripts/generate_skill_directory.py` or `./scripts/sync_catalog.sh`.

**Total Active Skills:** 1525
- **Free Skills:** 1503
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

### Home
| Skill Name | Description |
|------------|-------------|
| `a2a_request_handler` | Performs JSON-RPC compliance checks and bearer-token auth for A2A requests. |
| `a2a_response_builder` | Constructs JSON-RPC envelopes for outbound A2A traffic. |
| `above_market_lease_amortizer` | Calculates periodic amortization expense for lease intangibles. |
| `abs_credit_enhancement` | Applies agency percentile sizing by mapping ratings to loss percentiles and comparing them to provided subordination to compute required enhancement and coverage ratios. |
| `access_control_checker` | Validates tier permissions across Snowdrop skills. |
| `accounts_payable_optimizer` | Evaluates supplier invoices for early payment discounts versus company cost of capital to recommend an optimal payment schedule. |
| `accumulation_distribution` | Calculates accumulation/distribution via money flow multiplier and cumulative volume flow. |
| `achievement_tracker` | Evaluates activity events for new badges and upcoming milestones. |
| `action_item_extractor` | Uses heuristics to identify action items, assignees, and priority from text. |
| `active_address_momentum` | Analyzes daily active address series, applying momentum and Metcalfe's Law valuation hints. |
| `activity_based_costing` | Distributes cost pools based on activity driver consumption. |
| `administrator_api_bridge` | Bridge skill that validates administrator feeds and emits normalized payload summaries. |
| `advance_decline_line` | Builds the cumulative Advance-Decline line and optional McClellan oscillator signal. |
| `adx_calculator` | Applies Wilder's Average Directional Index to gauge whether trends are weak or strong. |
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
| `agricultural_weather_risk_scorer` | Scores crop yield risk from precipitation and temperature anomalies across agricultural regions. Returns risk scores (0–10), identifies the highest-risk region, and provides an aggregate supply disruption probability estimate. |
| `air_quality_lookup` | Retrieve current air quality conditions, historical hourly AQI data, or heatmap tile configuration for any location using the Google Air Quality API. Returns AQI score, dominant pollutant, individual pollutant concentrations, health recommendations, plus an esg_score (0–100) and real_estate_impact assessment for ESG reporting and property valuation workflows. |
| `allocation_enforcer_80_20` | Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails. |
| `altman_z_score` | Calculates Altman Z, identifies zone, and estimates distress probability. |
| `ambassador_manager` | Handles ambassador applications, approvals, listings, and removals. |
| `ambassador_reward_calculator` | Computes base rewards and bonuses for ambassador activity. |
| `amm_price_impact_calculator` | Applies constant product math to measure price impact of swapping base for quote reserves. |
| `amt_calculator` | Calculates Alternative Minimum Tax income, exemption phase-out, tentative minimum tax, and resulting liability versus the regular tax system. |
| `annual_budget_builder` | Projects monthly revenue/expense totals with growth assumptions for 12 months. |
| `annuity_payment_calculator` | Determines the periodic payment required to amortize a balance, including summary stats for total paid, interest, and early amortization snapshots. |
| `annuity_pricing_tool` | Prices whole-life and deferred-life annuities-due using a simple mortality model calibrated to approximate 2017 CSO rates. Returns annuity factor, present value, and break-even analysis metrics. |
| `anti_treaty_shopping_lob` | Evaluates LOB tests (ownership/base erosion, publicly traded, active trade or business, derivative benefits). |
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
| `arms_index_trin` | Computes TRIN as (Adv/Dec)/(AdvVol/DecVol) and averages it to identify overbought/oversold. |
| `art_valuation_model` | Uses hedonic regression weights calibrated to artist, medium, size, and provenance with comparable sales to estimate value and liquidity. |
| `artifact_registry_manager` | Manage Google Artifact Registry Docker images: list, clean old tags, remove untagged layers. Use after each deployment to keep storage costs low. Requires roles/artifactregistry.admin on the service account. |
| `asian_option_pricer` | Monte Carlo arithmetic Asian option pricer using Kemna-Vorst geometric control variate to reduce variance (Hull, Ch. 26). |
| `assembly_line_cost_calculator` | Compares Assembly Line run-rate against a pure-Opus baseline. |
| `assembly_line_orchestrator` | Frames the Haiku→Sonnet→Opus workflow and estimates token spend. |
| `asset_allocation_by_age` | Applies a modified age-based formula to recommend stock/bond/cash/alt allocations and produces a glide path toward retirement. |
| `asset_allocation_optimizer` | Finds feasible allocations that hit target return/risk under constraints. |
| `asset_backed_token_collateral_analyr` | Evaluates collateral value, advance rates, and haircuts for asset-backed token programs. |
| `asset_swap_spread` | Derives the par asset swap spread and constant Z-spread using swap discount factors and root-finding. |
| `asset_tokenization_fee_estimator` | Aggregates setup and recurring platform fees to forecast tokenization economics. |
| `atr_calculator` | Implements Wilder's Average True Range for volatility assessment. |
| `audit_24h_reconstructor` | Filters ledger activity to a 24h window and produces a running balance. |
| `audit_kraken` | Retrieves live Kraken exchange balances for TON, SOL, and USDC, converts to USD, and returns a structured balance report. |
| `audit_trail_immutable_export` | Export records to a SHA-256 signed CSV. The hash covers the entire CSV content, making tampering detectable. Hash is embedded as the final row or metadata header. |
| `audit_trail_logger` | Writes immutable audit entries to logs/audit_trail.jsonl. |
| `auto_loan_calculator` | Builds a car financing model covering tax, amount financed, monthly payment, and total interest across the loan term. |
| `autocallable_note_pricer` | Simulates geometric Brownian paths to estimate autocall probabilities, expected life, and fair price for a Phoenix/autocallable note. |
| `awesome_oscillator` | Calculates Bill Williams' Awesome Oscillator using 5/34 SMA of median price to highlight momentum shifts. |
| `backdoor_roth_calc` | Applies the IRS pro-rata rule to a backdoor Roth IRA conversion and reports the taxable portion, estimated tax bill, and feasibility guidance. |
| `backtesting_var_model` | Evaluates VaR performance using Basel traffic light thresholds and Kupiec LR test. |
| `backup_snapshot_creator` | Compiles file manifests for Snowdrop backups (no writes performed). |
| `backup_verifier` | Checks backup manifests for missing or corrupted files using SHA-256 hashes. |
| `badge_issuer` | Creates cryptographic badge records for ambassador and achievement unlocks. |
| `balance_sheet_generator` | Groups trial balance entries into a balance sheet (A=L+E validation). |
| `balancer_impermanent_loss_guardrail` | Simulates Balancer IL exposure for dual-asset pools and recommends caps. |
| `balancer_liquidity_rebalance_playbook` | Builds Balancer liquidity rebalance plans for yield rotations. |
| `balancer_lsd_leverage_spread_modeler` | Models Balancer LSD leverage spreads with health-factor guardrails. |
| `barrier_option_pricer` | Monte Carlo pricer for continuously monitored barriers using Brownian-bridge correction (Broadie-Glasserman, 1997) for up/down and in/out configurations. |
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
| `basel_output_floor` | Applies 72.5% output floor to IRB RWA and quantifies capital impact. |
| `basis_risk_calculator` | Quantifies commodity hedge basis risk. Computes hedged portfolio volatility, hedge effectiveness (R²), optimal hedge ratio (minimum-variance), and basis differential. |
| `benchmark_comparator` | Calculates alpha, beta, tracking error, and rolling alpha versus benchmark. |
| `benchmark_relative_performance` | Calculates performance statistics versus a benchmark including capture ratios and tracking error. |
| `beta_calculator` | Computes beta, correlation, alpha, systematic contribution, and residual risk relative to a benchmark. |
| `bigquery_query` | Run BigQuery SQL queries and schema operations for financial analytics. Uses BigQuery REST API v2 with explicit SA credentials — no gcloud, no ADC. Requires roles/bigquery.jobUser and roles/bigquery.dataViewer. |
| `billing_reconciler` | Compares invoiced amounts against measured compute usage to surface deltas. |
| `binary_option_pricer` | Values digital options of cash-or-nothing or asset-or-nothing type; European payoff via Black-Scholes, American via binomial tree. |
| `black_litterman_optimizer` | Computes Black-Litterman posterior returns and optimal weights using CAPM equilibrium implied returns blended with confidence-weighted views per He and Litterman (1999). |
| `black_scholes_pricer` | Calculates Black-Scholes option prices with full Greek outputs. |
| `blockchain_wallet_reconciler` | Reconciles Ghost Ledger wallet balances against on-chain snapshots and surfaces tolerance breaches. |
| `blog_post_generator` | Creates structured blog content with title, sections, and metadata. |
| `blue_sky_filing_fee_calculator` | Calculates blue sky filing fees using schedule caps and minimums. |
| `bollinger_bands` | Calculates SMA-based Bollinger Bands with configurable standard deviation multipliers. |
| `bond_duration_calculator` | Computes Macaulay duration, modified duration, and convexity for a coupon bond. |
| `bond_futures_basis_calculator` | Identifies CTD bond and computes gross/net basis for bond futures. |
| `bond_futures_ctd` | Evaluates conversion-factor adjusted invoice price, carry, and implied repo rate to identify the CTD bond per CME Treasury delivery rules. |
| `bond_pricer` | Prices a fixed-rate bond using standard street-convention accrued interest under 30/360, ACT/ACT, or ACT/360 day-count with support for semi-annual or quarterly coupons. |
| `bond_relative_value` | Calculates Z-spread via discount-factor root search, approximates asset swap spread versus swaps, and derives CDS basis. |
| `bond_yield_calculator` | Provides quick estimates for a bond's current yield, yield to maturity, yield to call, and duration approximation from price and coupon inputs. |
| `bonding_curve_pricer` | Calculates Watering Hole bonding curve prices using time decay, demand velocity, and snap-back protections. |
| `book_value_analyzer` | Computes book/tangible book per share and related valuation ratios. |
| `borrower_credit_scorecard` | Generates weighted scorecard covering leverage, coverage, liquidity, and management. |
| `bounty_claim_handler` | Handles claim lifecycle events for posted community bounties. |
| `bounty_payout_processor` | Validates and stages payouts for approved bounty winners. |
| `bounty_poster` | Publishes new skill, feature, or bug-fix bounties to the community board. |
| `brazil_pix_settlement_logic` | Applies Banco Central do Brasil (BCB) Pix rules per Resolução BCB nº 1 (2020) and subsequent circulars. Validates transaction limits (nightly R$1,000 cap for PF), fee structures, settlement times (10 seconds 24/7), and transaction type restrictions. |
| `break_even_analysis` | Determines unit and revenue breakeven levels and runs pricing/cost what-if scenarios to stress test contribution margins. |
| `break_even_analyzer` | Computes break-even units, revenue, margin of safety, and estimated time to break even. |
| `breakeven_inflation_calculator` | Calculates breakeven inflation and adjusts for risk premium assumptions. |
| `bridge_loan_pricing` | Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month. Rates are expressed as annual decimals (e.g. 0.05 = 5%). |
| `budget_variance_analyzer` | Summarizes budgeted versus actual spend by category with variance breakdowns, flagging overruns and savings opportunities. |
| `burn_rate_calculator` | Calculates gross/net burn, runway, and trend classification from recent data. |
| `burn_rate_runway` | Computes gross and net burn rates, cash runway, and projected zero-cash date accounting for compounding revenue growth. |
| `burn_trigger_monitor` | Flags Watering Hole burn when expenses beat revenue+labor by 20% for 3 weeks. |
| `cac_ltv_calculator` | Calculates CAC, gross-margin LTV, payback period, and ratio health to evaluate growth efficiency for subscription and transactional businesses. |
| `calc_waterfall_dist` | Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. |
| `callable_bond_oas` | Builds a Black-Derman-Toy short-rate lattice calibrated to the input curve and solves for the OAS that matches market price, then reports duration and convexity. |
| `callable_bond_pricer` | Values a callable bond on a single-factor Hull-White lattice, providing model price, duration, and call exercise probabilities. |
| `calmar_ratio_calculator` | Computes the Calmar ratio using cumulative returns and drawdown analysis. |
| `candlestick_pattern_detector` | Scans OHLC data for common patterns: doji, hammer, engulfing, stars, soldiers/crows, harami, spinning top, shooting star. |
| `cap_floor_pricer` | Prices interest rate caps or floors using Black's model for each caplet/floorlet. |
| `cap_rate_analyzer` | Computes actual cap rate and implied value relative to market cap rates. |
| `cap_rate_decomposition` | Breaks down cap rate into risk-free, property, market, and vacancy components. |
| `cap_table_manager` | Computes fully diluted ownership after venture rounds including option pools and notes. |
| `cap_table_simulator` | Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. |
| `capital_account_reconciler` | Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees. |
| `capital_allocation_raroc` | Calculates RAROC and economic value added per business line for regulatory capital planning. |
| `capital_call_calculator` | Calculates LP capital call wire amounts based on commitment percentages. Supports per-call fund expenses and validates that call_pct does not exceed remaining unfunded commitment. |
| `capital_call_fx_optimizer` | Allocates multi-currency balances to satisfy a capital call with minimal FX drag. |
| `capital_call_notice_generator` | Creates LP-specific capital call instructions awaiting Thunder sign-off. |
| `capital_expenditure_analyzer` | Breaks capex into maintenance vs growth and measures NOI burden. |
| `capital_gains_tax_calculator` | Calculates realized capital gain tax based on holding period and jurisdiction. |
| `captive_insurance_analyzer` | Estimates required surplus and feasibility for forming a captive insurer. Uses Value-at-Risk (VaR) at a user-specified confidence level with a normal loss distribution assumption. Returns required surplus, VaR capital, break-even loss ratio, and a feasibility score. |
| `captive_insurance_feasibility_model` | Scores captive feasibility based on losses, premium, and surplus needs. |
| `carbon_credit_pricer` | Applies benchmark market prices with discounts for vintage and premiums for project quality to produce fair values. |
| `carried_interest_calculator` | Computes GP carried interest after returning LP capital and preferred return. Supports optional full GP catch-up tranche before profit split. Uses European-style (whole-fund) waterfall logic. |
| `carried_interest_tax_analyzer` | Calculates tax liability for carried interest under three-year rule. |
| `carried_interest_tax_calculator` | Recharacterizes carried interest under IRC §1061's three-year holding period rule. |
| `carried_interest_tracker` | Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows. |
| `carry_trade_calculator` | Computes carry-to-vol metrics for FX pairs using interest differentials. |
| `cash_conversion_cycle` | Computes DSO, DIO, DPO, and the cash conversion cycle to assess working capital efficiency. |
| `cash_flow_forecaster` | Builds a 12-month cash forecast factoring in revenue growth, fixed operating costs, variable expenses, and scheduled one-time cash outlays. |
| `cash_flow_projector` | Computes monthly cash flow projections with cumulative balances and risk flags. |
| `catastrophe_bond_analyzer` | Evaluates expected loss, risk-adjusted spread, multiple-at-risk (MAR), and approximate Sharpe ratio for catastrophe bonds. Uses trapezoidal integration over the loss distribution to estimate expected loss. |
| `catastrophe_bond_spreads` | Applies industry convention (expected loss + risk load + liquidity premium) to decompose cat bond spreads. |
| `ccar_capital_planning` | Projects CET1 ratio over stress horizon using Fed CCAR methodology. |
| `cci_calculator` | Calculates Donald Lambert's Commodity Channel Index using a mean deviation normalization. |
| `cd_ladder_builder` | Constructs a certificate-of-deposit ladder by distributing capital across available terms, reporting allocation, weighted yield, and liquidity schedule. |
| `cdo_squared_correlation` | Aggregates inner CDO tranche correlations to infer compound/base metrics and reports spread sensitivity across the outer tranche. |
| `cdo_tranche_pricer` | Prices a CDO tranche using the Li (2000) Gaussian copula and Vasicek LHP model to deliver expected loss, spread, and delta analytics. |
| `cds_basis_trade_analyzer` | Decomposes the CDS-cash basis into coupon, financing, and default-leg components using basis trading conventions (Hull, Ch. 24). |
| `cds_bond_basis_tracker` | Calculates CDS basis across bonds and flags rich/cheap signals. |
| `cds_breakeven_spread` | Calculates running spread that equates premium and protection PVs. |
| `cds_cheapest_to_deliver_analyzer` | Identifies the cheapest deliverable bond and expected auction recovery. |
| `cds_convexity_calculator` | Estimates convexity impact from nonlinear CDS spread moves. |
| `cds_correlation_basket_analyzer` | Analyzes basket correlation scenarios and tranche loss contributions. |
| `cds_counterparty_risk_analyzer` | Evaluates CDS counterparty exposures versus assigned limits. |
| `cds_curve_steepener_analyzer` | Evaluates CDS curve slope and roll yield for steepener trades. |
| `cds_duration_calculator` | Calculates CDS PV01 and spread duration based on discount curve. |
| `cds_hazard_rate_bootstrapper` | Bootstraps hazard rates from CDS spreads and recovery assumptions. |
| `cds_index_basis` | Measures the difference between traded CDS index spread and the weighted intrinsic spread and derives implied correlation using variance decomposition. |
| `cds_index_portfolio_analyzer` | Aggregates CDS index notionals, sectors, and risk skew. |
| `cds_index_roll_cost` | Computes CDS index roll cost by comparing on/off-the-run spreads and PV01 carry over the roll period, following standard index arbitrage analytics. |
| `cds_jump_to_default_calculator` | Calculates jump-to-default impact using LGD and recovery assumptions. |
| `cds_mark_to_market_calculator` | Marks CDS positions using PV01 and spread differentials. |
| `cds_notional_risk_calculator` | Computes gross, net, and concentration metrics for CDS notionals. |
| `cds_option_pricer` | Applies the Black (1976) model with risky DV01 scaling to CDS swaptions for payer/receiver structures. |
| `cds_pnl_attribution_model` | Attributes CDS P&L into carry, spread, and curve components. |
| `cds_premium_leg_pv` | Discounts CDS premium leg coupons to compute PV and annuity. |
| `cds_protection_leg_pv` | Computes PV of CDS protection leg using default probabilities. |
| `cds_recovery_rate_sensitivity` | Analyzes CDS spread sensitivity to recovery rate scenarios. |
| `cds_spread_calculator` | Estimates CDS par spread and expected loss using default probabilities. |
| `cds_survival_probability_curve` | Generates survival probabilities from hazard rates and tenors. |
| `cds_upfront_to_running_converter` | Converts CDS upfront percentage into equivalent running spread. |
| `cecl_calculator` | Calculates CECL reserves by segment using life-of-loan loss rates plus qualitative adjustments. |
| `central_bank_ledger_sync` | Reconciles a CBDC transaction ledger against central bank balance and reported circulation figures to detect discrepancies. |
| `cet1_deduction_engine` | Computes CET1 deductions with 15% aggregate threshold for DTAs, MSRs, and investments. |
| `chaikin_money_flow` | Calculates Chaikin Money Flow (CMF) over a specified period to quantify accumulation or distribution. |
| `chaikin_volatility` | Calculates Chaikin Volatility (EMA of range with rate-of-change comparison). |
| `chalkboard_dashboard` | Aggregates transparency metrics for the public chalkboard dashboard. |
| `changelog_generator` | Outputs Keep a Changelog formatted text from change entries. |
| `charitable_giving_optimizer` | Applies IRS AGI limits for cash (60%) and appreciated asset (30%) donations and advises whether gifting stock yields higher tax savings. |
| `chart_data_formatter` | Normalizes data into Chart.js/Plotly friendly schema with labels/datasets. |
| `chart_of_accounts` | Adds or searches accounts across the Stonewater standard chart. |
| `chooser_option_pricer` | Rubinstein chooser pricing via combination of Black-Scholes call and adjusted put legs, supporting standard and complex choosers. |
| `churn_analyzer` | Analyzes churn patterns, cohort retention, and at-risk agents. |
| `claims_development_triangle` | Constructs a cumulative loss development triangle and computes volume-weighted age-to-age factors, tail factor, and cumulative-to-ultimate factors from a list of claim records with accident_year, development_year, and cumulative_paid fields. |
| `clawback_analyzer` | Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. |
| `clawback_calculator` | Determines GP clawback due when interim carried interest distributions exceed final entitlement. Optionally applies interest on the outstanding clawback amount. |
| `climate_risk_transition` | Applies NGFS transition scenarios to sector PDs and estimates RWA impact and stranded assets. |
| `cliquet_option_pricer` | Monte Carlo pricing of locally capped/floored cliquet options with global collar following risk-neutral dynamics. |
| `cln_pricer` | Discounts CLN coupons and principal with expected loss per Hull (2006) to estimate fair price and incremental spread. |
| `clob_liquidity_score` | Computes a composite score from depth-weighted spread, imbalance, and volume decay to quantify CLOB liquidity. |
| `cloud_build_trigger` | Manually trigger a Google Cloud Build build from a trigger ID or repo/branch. Returns the build ID and log URL for monitoring. |
| `cloud_run_deploy` | Deploy, inspect, list, or delete Google Cloud Run services. Uses Cloud Run Admin API v2 with explicit service account credentials only — no gcloud CLI, no Application Default Credentials. |
| `cmbs_loan_analyzer` | Computes LTV, DSCR, debt yield, and balloon risk for CMBS loans. |
| `cmo_cashflow_waterfall` | Projects mortgage collateral cashflows with PSA prepayments and allocates them through sequential/PAC/TAC tranches to report WALs and yields. |
| `co_investment_analyzer` | Calculates fee savings, carry relief, and net IRR uplift from co-investment structures. |
| `co_investment_ledger` | Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio. |
| `cohort_retention_analyzer` | Computes retention percentages for each cohort, aggregates the average curve, and estimates cohort-level LTV along with churn by month. |
| `coinbase_agentkit_verifier` | Drafts the JSON payload needed to verify Snowdrop in Coinbase AgentKit. |
| `collaborative_liquidity_hunt` | Validates whether a group of trusted agents has sufficient combined capital to exploit a thin-market spread opportunity and produces a pro-rata allocation plan. |
| `collar_strategy_analyzer` | Analyzes protective collar payoff, net cost, and protection ranges. |
| `collateral_management_optimizer` | Ranks collateral by haircut-adjusted funding cost versus yield. |
| `collections_manager` | Tiers overdue accounts into reminder, notice, suspension, or write off stages. |
| `combined_ratio_calculator` | Computes combined ratio, underwriting margin, and operating ratio from loss, expense, and investment income ratios. Supports trade and statutory basis. |
| `commercial_umbrella_coverage_analyzer` | Determines umbrella exhaustion probabilities and gap coverage. |
| `commitment_pacing_model` | Suggests annual commitments and overcommitment ratios for PE allocation targets. |
| `commodity_beta_calculator` | Estimates OLS beta, alpha, correlation, and annualized tracking error of a commodity return series against a benchmark. Returns are in decimal form (e.g. 0.02 = 2%). |
| `commodity_correlation_tracker` | Computes pairwise Pearson correlations across commodity return series, identifies highest and lowest correlated pairs, and reports diversification score. |
| `commodity_momentum_signal` | Builds a time-series momentum signal using short and long lookback returns with volatility-adjusted scoring. Standard approach: 12-1 momentum skips the most recent month to avoid short-term reversal contamination. |
| `commodity_risk_dashboard` | Aggregates gross/net notional, parametric 1-day 95% VaR per position, portfolio VaR proxy, oil-beta weighted exposure, and concentration flags. |
| `commodity_structured_note` | Values a participation note written on a commodity forward using Black's model and applies cap/floor constraints. |
| `commodity_swap_pricer` | Prices fixed-for-floating commodity swaps using forward curves and discount factors. |
| `commodity_term_structure_model` | Fits an OLS linear regression to a commodity futures curve to estimate level (intercept at T=0), slope (price change per month), curvature (MSE of fit), and reports curve structure classification. |
| `community_growth_tracker` | Calculates growth rates, viral coefficient, and projections from snapshots. |
| `community_impact_attributor` | Splits revenue, usage, and profit between community and internal skills. |
| `community_leverage_dashboard` | Summarizes how community contributions amplify internal capacity. |
| `community_skill_adoption_tracker` | Compares usage, revenue, and growth metrics between internal and community skills. |
| `community_skill_submitter` | Validates community skill code before it enters the review queue. |
| `comparable_company_screener` | Calculates EV/Revenue, EV/EBITDA, P/E, and implied values for a target. |
| `comparable_transaction_analyzer` | Derives valuation ranges from comps using EV/Revenue and EV/EBITDA multiples. |
| `competitive_landscape_tracker` | Compares competitor offerings, pricing, and feature coverage. |
| `compliance_calendar` | Generates a consolidated compliance deadline calendar with statuses. |
| `compound_interest_calculator` | Calculates the future value of an investment with compound interest, returning effective annual yield and year-by-year growth. |
| `compound_option_pricer` | Geske (1979) closed-form pricer for call-on-call and put-on-call compound options using bivariate normals. |
| `compute_budget_enforcer` | Makes sure Snowdrop does not exceed the $50/day compute budget. |
| `compute_capacity_planner` | Projects when capacity will be breached and recommends actions. |
| `compute_time_tracker` | Calculates task durations, idle time, and cost per skill/model. |
| `concentration_risk_hhi` | Computes HHI, effective number of obligors, and top exposures akin to ECB concentration add-ons. |
| `config_validator` | Ensures config.yaml content meets Snowdrop schema expectations. |
| `consensus_protocol` | Evaluates votes for quorum and flags potential Byzantine behavior. |
| `construction_draw_scheduler` | Generates draw schedules, interest carry, and LTC compliance checks. |
| `construction_draw_validator` | Validates a construction loan draw request by verifying that receipts sum to the requested amount, the milestone exists and has sufficient remaining budget, and completion percentage is consistent. Returns approval status, discrepancy list, and remaining milestone budget. |
| `contango_backwardation_detector` | Identifies curve structure (contango / backwardation / mixed), computes per-tenor annualized roll yield, front and tail basis, and flags extreme backwardation. |
| `context_window_optimizer` | Packs content sections into the available context window using priority heuristics. |
| `contingent_cds_pricer` | Values contingent CDS via barrier-adjusted probabilities: barrier probability via down-and-in hitting formula (Broadie-Glasserman) multiplied by conditional default PV. |
| `continuous_compounding_calculator` | Applies Pe^rt to compute the continuously compounded future value and compares it to annual and monthly compounding scenarios. |
| `contract_lifecycle_manager` | Creates, updates, lists, and surfaces contracts nearing expiration. |
| `contract_metadata_analyzer` | Scores contract risk based on verification, usage, and deployer reputation. |
| `contract_renewal_alerter` | Identifies contracts requiring renewal action and quantifies value at risk. |
| `contractor_payment_tracker` | Aggregates contractor payments and flags 1099 thresholds. |
| `contribution_attribution_engine` | Weights lines of code, complexity, usage, and revenue to estimate contributor value. |
| `contribution_quality_scorer` | Calculates quality grades based on Snowdrop coding standards and security checks. |
| `contribution_token_tracker` | Aggregates token usage by contributor type to measure leverage. |
| `contributor_retention_analyzer` | Tracks contributor repeat rates, retention curves, and churn metrics. |
| `convenience_yield_calculator` | Solves for implied convenience yield using the continuous cost-of-carry relation: F = S * exp((r + u - y) * T), rearranged as y = r + u - ln(F/S) / T. |
| `conversation_summarizer` | Compress multi-turn logs into actionable decisions and questions. |
| `convertible_arbitrage_analytics` | Computes share hedge, gamma exposure, and credit/borrow carry for convert arb positions. |
| `convertible_bond_pricer` | Approximates the Tsiveriotis-Fernandes convertible decomposition into straight bond and embedded call option to deliver price and Greeks. |
| `convertible_note_calculator` | Computes accrued interest, conversion price, and shares for convertible notes. |
| `convexity_hedger` | Determines barbell weights that match the duration of a bullet bond while maximizing convexity per CFA curriculum. |
| `corporate_action_processor` | Adjusts position quantities and cash for announced corporate actions. |
| `corporate_business_interruption_calculator` | Estimates business interruption exposure from revenue, expense, and standby time. |
| `corporate_property_cat_exposure_model` | Summarizes property exposure by peril zone and cat return periods. |
| `correlation_matrix_builder` | Build Pearson correlation matrices from asset price histories. |
| `correlation_swap_pricer` | Computes the fair correlation (average off-diagonal) and marks the swap relative to strike with delta/vega style metrics. |
| `cost_basis_averaging_logic` | Calculate cost basis using FIFO, LIFO, average cost, or specific-lot method. Identifies tax-loss harvesting opportunities and wash sale risk. |
| `cost_center_reporter` | Aggregates expenses by center with mix and budget deltas. |
| `cost_segregation_estimator` | Approximates accelerated depreciation benefits from cost seg studies. |
| `countercyclical_buffer_calc` | Weights jurisdiction CCyB rates by credit exposures to derive bank-specific buffer. |
| `counterparty_credit_charge` | Computes bilateral credit adjustments (CVA/DVA) by integrating discounted exposures with marginal default probabilities per Basel CVA methodology. |
| `counterparty_exposure_calculator` | Aggregates MTM by counterparty, applies collateral, and flags threshold breaches. |
| `counterparty_exposure_pfe` | Computes potential future exposure (PFE) across tenors using collateralized netting set information. |
| `covenant_lite_risk_scorer` | Assigns protection scores based on covenant packages and aggressive terms. |
| `covered_call_analyzer` | Computes payoff, breakeven, and annualized returns for a covered call position. |
| `cre_cap_rate_aggregator` | Aggregates capitalization rates from a list of comparable CRE sales. Computes individual cap rates (NOI / sale_price), then averages by asset class (office, retail, multifamily, etc.) and by market (MSA). Returns overall market average and outlier flags. |
| `cre_debt_stack_modeling` | Models a commercial real estate capital stack with senior debt, mezzanine, and equity tranches. Calculates blended cost of capital, cumulative LTV per tranche, and flags structural risk (e.g., LTV > 80% for senior). |
| `cre_lease_comparator` | Evaluates tenant/landlord economics for NNN, gross, and modified gross leases. |
| `credit_card_payoff_calculator` | Simulates credit card amortization for a chosen payment or target timeline and compares it against paying issuer minimums. |
| `credit_conversion_factor_calculator` | Assigns Basel CCF based on facility type (commitment, guarantee, trade finance, etc.). |
| `credit_curve_bootstrapper` | Solves for piecewise-constant hazard rates that match CDS spreads under the ISDA standard model (premium leg equals protection leg per tenor). |
| `credit_default_swap_pricer` | Prices a CDS using flat hazard and discount rates, returning par spread and PVs. |
| `credit_enhancement_calculator` | Determines required subordination and overcollateralization to hit target ratings. |
| `credit_event_probability` | Transforms piecewise hazard rates into survival, marginal default probabilities, and event odds per tenor. |
| `credit_facility_utilization_monitor` | Aggregates revolver/DDTL/term loan utilization and identifies spread tiers. |
| `credit_index_option_pricer` | Applies Black's formula on CDS index spreads with PV01 scaling to deliver payer/receiver option values and Greeks. |
| `credit_limit_adjuster` | Applies utilization and score rules to tab limit changes. |
| `credit_migration_matrix` | Converts raw rating transition counts into normalized probability matrices and drift statistics. |
| `credit_portfolio_stress_tester` | Applies EBITDA declines and rate shocks to measure coverage and leverage impact. |
| `credit_quality_migration_tracker` | Compares prior and current rating distributions to flag drift. |
| `credit_risk_irb_capital` | Applies Basel IRB corporate formula for rho, maturity adjustment, and capital (K). |
| `credit_risk_sa_capital` | Calculates RWA for standardized approach exposures with credit conversion and collateral mitigation. |
| `credit_spread_analyzer` | Calculates credit spreads, implied default probabilities, and indicative ratings. |
| `credit_spread_calculator` | Computes approximate yield and spread from coupon, price, and benchmark rates. |
| `credit_spread_decomposer` | Breaks a corporate bond option-adjusted spread into expected loss (PD*LGD), liquidity premium, risk premium, and tax component per BIS credit risk methodology. |
| `credit_triangle_calculator` | Applies the credit triangle (spread ≈ hazard × (1 − recovery)) to reconcile CDS quotes with implied hazard and loss metrics for a given tenor. |
| `credit_var_calculator` | CreditMetrics style credit VaR computing conditional default probabilities and obligor contributions. |
| `credit_vix_calculator` | Uses the VIX variance replication formula on CDS option strips to infer an implied volatility index for credit spreads. |
| `credit_waterfall_calculator` | Allocates cash to fees, senior, mezzanine, and equity tranches. |
| `cron_scheduler` | Checks which scheduled tasks are due and when the next run occurs. |
| `cross_asset_correlation` | Computes pairwise correlations across asset classes and flags concentration risks. |
| `cross_chain_accounting_bridge` | Normalize TON, Solana, and Ethereum transactions into a unified single ledger with net positions per chain. |
| `cross_chain_bridge_fee_estimator` | Estimates total bridge fees including relayer markup and destination chain execution gas. |
| `crowd_roi_calculator` | Measures value created by community contributions versus review cost. |
| `crowd_sourced_risk_audit` | Aggregates multi-assessor risk scores into a confidence-weighted consensus, surfaces statistical outliers, and classifies overall consensus strength. |
| `crowd_sourcing_forecast` | Projects contributions, skills, and value under bear/base/bull scenarios for six months. |
| `crowd_value_velocity` | Calculates weekly value velocity, acceleration, and forward projections. |
| `crs_reporting_classifier` | Flags CRS reportable accounts per OECD CRS Section VIII definitions. |
| `crypto_fiat_converter` | Uses USD hub conversions (pending Thunder approval for transfers). |
| `crypto_glossary` | Explains crypto terms with analogies and risk warnings (goodwill only). |
| `crypto_tax_fund_accounting` | Applies FIFO cost basis to crypto trades per IRS Notice 2014-21 and captures staking income. |
| `crypto_yield_farming_analyzer` | Converts pool volume/TVL and token incentives into APY while quantifying impermanent loss via volatility. |
| `csv_exporter` | Flattens dict rows and emits RFC4180-compliant CSV strings. |
| `ctr_generator` | Determines whether a CTR filing is required and drafts the payload. |
| `curl_example_generator` | Builds ready-to-run curl commands for each skill's input schema. |
| `currency_adjusted_return` | Adjusts local returns for FX moves to measure base-currency performance. |
| `currency_carry_analyzer` | Calculates carry yield (interest rate differential) for FX pairs, checks covered interest parity (CIP) deviation against observed forwards, and ranks pairs by carry attractiveness. |
| `curve_impermanent_loss_guardrail` | Simulates Curve IL exposure for dual-asset pools and recommends caps. |
| `curve_liquidity_rebalance_playbook` | Builds Curve liquidity rebalance plans for yield rotations. |
| `curve_lsd_leverage_spread_modeler` | Models Curve LSD leverage spreads with health-factor guardrails. |
| `custodian_feed_harmonizer` | Normalize custodian statement payloads into a canonical schema with validation flags. |
| `custody_break_detector` | Identify cash or security breaks between custody statements and the ledger. |
| `cyber_insurance_exposure_estimator` | Estimates cyber limit need from revenue, records, and controls maturity. |
| `daily_briefing_generator` | Assembles Snowdrop's morning status brief for Thunder. |
| `dao_governance_participation_scorer` | Assesses voter turnout and proposal engagement to highlight DAO governance strength. |
| `dashboard_aggregator` | Groups panels by source, surfaces alerts, and crafts summary sentences. |
| `data_anonymizer` | Transforms sensitive fields using hash/mask/redact/generalize strategies. |
| `data_freshness_monitor` | Checks data sources against allowed staleness windows. |
| `data_narrator` | Converts structured finance outputs into tone-aware prose. |
| `data_provenance_map` | Construct lineage graph from ingestion artifacts and flag stale datasets or missing dependencies. |
| `data_quality_scorecard` | Compute null/duplication/freshness scores for administrator datasets and flag breaches. |
| `data_transformer` | Applies rename/cast/compute/drop/default transformations to dataset rows sequentially. |
| `dcf_sensitivity_matrix` | Builds a DCF table across WACC and terminal growth assumptions. |
| `dcf_simple` | Discounts forecast free cash flows and a Gordon terminal value to estimate EV. |
| `debt_avalanche_planner` | Simulates the debt avalanche payoff strategy (highest interest rate first) and contrasts it against a classic snowball to highlight savings. |
| `debt_capacity_calculator` | Computes leverage and cash-flow-based debt capacity estimates. |
| `debt_covenant_monitor` | Evaluates debt covenants against current financial ratios. Supports leverage_ratio (lower is better), interest_coverage (higher is better), and current_ratio (higher is better) covenant types. Returns breach status and distance-to-breach for each covenant. |
| `debt_issuance_analyzer` | Computes net proceeds, OID yields, and all-in borrowing costs for bond deals. |
| `debt_service_coverage_calculator` | Computes DSCR using EBITDA less capex relative to cash interest and amortization. |
| `debt_service_coverage_reit` | Computes DSCR using NOI less recurring capex versus debt service. |
| `debt_snowball_planner` | Simulates a debt snowball strategy by ordering balances from smallest to largest, applying extra cash to the current focus account, and outputting the payoff timeline. |
| `debt_to_income_calculator` | Evaluates monthly debt obligations relative to income for mortgage qualification across Conventional, FHA, and VA programs. |
| `default_fund_sizing` | Computes cover-2 requirement using member stress losses net of margin and allocates contributions. |
| `default_rate_calculator` | Calculates period and trailing default rates from cohort data. |
| `defi_liquidity_pool_analyzer` | Computes turnover, fee APR, and concentration analytics for AMM pools. |
| `defi_yield_comparator` | Filters DeFi protocols by safety heuristics and ranks risk-adjusted yield. |
| `delayed_draw_term_loan_tracker` | Calculates drawn/undrawn balances, fees, and blended costs for DDTLs. |
| `delta_hedging_simulator` | Simulates discrete delta hedging P&L decomposition over a price path. |
| `dema_calculator` | Computes the Double Exponential Moving Average (2*EMA - EMA(EMA)) to highlight early momentum turns. |
| `deployment_readiness_checker` | Aggregates deployment checklist results and surfaces blockers/warnings. |
| `deposit_pricing_analyzer` | Calculates weighted cost of deposits, effective beta, and expense impact from rate shifts. |
| `deprecation_notice_generator` | Formats structured deprecation notices for skills/endpoints. |
| `depreciation_calculator` | Produces annual depreciation schedules for straight-line, declining balance, MACRS (simplified), and sum-of-years methods. |
| `development_pipeline_tracker` | Summarizes pipeline by stage, budget, and delivery exposure. |
| `digest_builder` | Creates readable digests summarizing activity, metrics, and tips per agent. |
| `directors_officers_liability_calculator` | Estimates D&O expected loss, limit adequacy, and retention impacts. |
| `dispute_resolver` | Determines auto, manual, or split dispute resolutions for escrow issues. |
| `distressed_debt_recovery` | Waterfalls enterprise value through senior/mezz/equity to compute recoveries and implied returns. |
| `distressed_debt_screener` | Flags distressed signals using price, spread, PD, and coverage metrics. |
| `distribution_waterfall_calculator` | Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split. Supports both European (whole-fund) and American (deal-by-deal) modes. Uses correct catch-up formula: GP gets 100% until carry% of total profits is met. |
| `distribution_waterfall_modeler` | Calculates LP/GP outcomes for American and European waterfalls with tier detail. |
| `divergence_detector` | Identifies regular and hidden divergences between price action and an oscillator/indicator. |
| `dividend_accrual_calculator` | Accrues dividends between ex-date and pay-date across positions. |
| `dividend_capacity_analyzer` | Determines MDA and dividend restrictions relative to combined capital buffer requirements. |
| `dividend_reinvestment_projector` | Projects a dividend reinvestment plan by compounding dividends into new shares with growth assumptions for payouts and share price. |
| `docker_cleanup` | Clean up Docker images, containers, and volumes on the local machine to prevent disk exhaustion. Supports dry-run mode. Schedule weekly via subagent. Always preserve keep_images list (e.g. the live snowdrop-mcp image). |
| `docker_secret_injector` | Builds op run templates for injecting secrets into containers. |
| `document_vault_ocr_router` | Assign vault documents to OCR models based on mime type, priority, and presence of embedded text. |
| `dodd_frank_volcker_compliance` | Evaluates RENTD, inventory, and VaR metrics against Volcker Rule limits. |
| `dollar_cost_averaging_simulator` | Runs a dollar-cost averaging simulation against lump sum investing using a price series to determine ending values and identify the winning approach. |
| `donchian_channels` | Applies Richard Donchian's channel breakout system using highest highs and lowest lows. |
| `downside_risk_metrics` | Computes downside deviation, upside potential ratio, gain/loss ratio, and Bernardo-Ledoit ratio. |
| `dpi_calculator` | Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital. DPI is the realized component of fund performance — cash actually returned to LPs. |
| `dpi_narrative_generator` | Converts DPI metrics into LP-facing narrative with severity tiers when below target. |
| `drawdown_analyzer` | Computes drawdown metrics from an equity curve or NAV series. |
| `drawdown_constrained_optimizer` | Performs scenario search across asset paths to maximize expected return while enforcing a user-specified maximum drawdown limit consistent with UCITS risk budgeting guidance. |
| `drawdown_notice_generator` | Produce structured LP drawdown notices and routing metadata. |
| `drawdown_scheduler` | Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline. |
| `dry_powder_calculator` | Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves. If monthly_deployment_rate is provided, runway_months = dry_powder / rate. Useful for fund pacing, LP reporting, and GP investment planning. |
| `dscr_calculator` | Computes DSCR, assessment tier, excess cash, and headroom for new debt. |
| `duplicate_transaction_detector` | Finds exact and fuzzy duplicate transactions for Ghost Ledger hygiene. |
| `dupont_analysis` | Returns 3-stage and 5-stage DuPont ROE decomposition. |
| `dupont_decomposition` | Breaks down ROE using the classic DuPont formula plus a five-factor variant that isolates tax burden and interest burden effects. |
| `duration_matching_engine` | Solves for asset weights whose duration and convexity match a target liability, using least-squares immunization per Fabozzi. |
| `dynamic_discount_calculator` | Applies tiered volume and loyalty discounts for agents. |
| `earnings_quality_analyzer` | Computes accrual ratios, Beneish M-Score, and manipulation risk. |
| `earnings_surprise_calculator` | Calculates EPS surprise percentage, SUE proxy, and price-drift implications (PEAD). |
| `earnings_yield_calculator` | Computes earnings yield (inverse P/E) and compares against the 10Y Treasury yield. |
| `ease_of_movement` | Computes Richard Arms' Ease of Movement oscillator with SMA signal to judge efficient rallies/drops. |
| `ebitda_addback_analyzer` | Scores EBITDA addbacks by quality to show normalized EBITDA. |
| `ebitda_normalization` | Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. |
| `economic_substance_checker` | Checks economic substance requirements for common zero/low-tax fund domiciles. |
| `economic_surprise_index` | Computes weighted surprise index using normalized release beats/misses. |
| `ecosystem_health_dashboard` | Aggregates community metrics into a public health score and highlights. |
| `efficient_frontier_calculator` | Generates random portfolios to approximate the efficient frontier and key points. |
| `elder_ray_index` | Computes Elder-Ray Bull/Bear Power relative to an EMA trend baseline. |
| `elegance_loop` | Compares planned actions against executed results, quantifies drift, and flags when discrepancies breach the 1% tolerance. |
| `ema_calculator` | Calculates exponential moving averages using Wilder's smoothing to detect price momentum shifts. |
| `email_alert_builder` | Prepares email payloads without sending them. |
| `emergency_fund_calculator` | Determines the ideal emergency fund amount by weighing monthly expenses, income stability, and dependents while highlighting current coverage gaps. |
| `employer_401k_match_optimizer` | Evaluates contribution rates needed to earn the full employer match while respecting IRS limits and highlights remaining match dollars on the table. |
| `energy_crack_spread_calculator` | Computes 3-2-1 crack spread (standard refinery margin), custom ratio crack spread, 1-1-1 simplified spread, and a margin compression flag. All prices in $/bbl. |
| `energy_to_currency_peg_logic` | Models energy-backed currency pegs (IoT/solar), computing intrinsic unit value and stress-testing sustainability across energy price scenarios. |
| `enterprise_risk_retention_optimizer` | Selects corporate retention using expected loss curve and premium quotes. |
| `entity_extractor` | Uses regex heuristics to extract Snowdrop-relevant entities. |
| `env_var_auditor` | Finds missing, empty, and extra environment variables relative to .env.template. |
| `environmental_liability_exposure_model` | Estimates environmental liability exposure using scenario severities. |
| `equity_swap_pricer` | Discounts realized equity leg returns against fixed rate leg to compute PV, DV01, and carry. |
| `erc20_token_supply_analyzer` | Breaks total supply into circulating, treasury, and locked components to monitor float. |
| `error_pattern_detector` | Clusters similar errors and surfaces bursts for remediation. |
| `error_retry_exponential_backoff` | Generate an exponential backoff retry schedule with optional jitter for production error handling. Returns per-attempt delays and total max wait time. |
| `errors_omissions_premium_estimator` | Calculates E&O premium using rate per revenue and modifiers. |
| `escrow_manager` | Creates, monitors, and adjudicates agent escrow records. |
| `esg_screened_optimizer` | Delivers a constrained mean-variance allocation subject to minimum ESG score, sector exclusions, and sector caps consistent with EU SFDR Article 8 screening. |
| `esg_tax_incentive_calculator` | Models ESG incentives including IRC §§45/48 credits, Canada's Clean Technology ITC, and the Dutch EIA regime. |
| `estimated_quarterly_tax` | Combines income tax and self-employment tax to suggest quarterly estimated payments and safe harbor amounts to minimize penalties. |
| `estimated_tax_calculator` | Applies 90%/100% safe harbor logic to estimate quarterly payments and due dates. |
| `etf_vs_mutual_fund_comparator` | Aggregates expense ratios, commissions, and tax drag to compare ETF and mutual fund costs annually and across a 10-year horizon. |
| `etherfi_impermanent_loss_guardrail` | Simulates EtherFi IL exposure for dual-asset pools and recommends caps. |
| `etherfi_liquidity_rebalance_playbook` | Builds EtherFi liquidity rebalance plans for yield rotations. |
| `etherfi_lsd_leverage_spread_modeler` | Models EtherFi LSD leverage spreads with health-factor guardrails. |
| `ev_ebitda_comparator` | Computes EV/EBITDA multiples per company, sector median, and growth-adjusted comparisons. |
| `event_correlator` | Evaluates correlation rules to surface compound incidents. |
| `event_manager` | Handles creation, updates, registrations, and cancellations for events. |
| `exception_queue_prioritizer` | Prioritize reconciliation exceptions by severity, financial exposure, and SLA breach risk. |
| `excess_of_loss_calculator` | Calculates per-occurrence reinsurance recoveries, layer loss ratio, attachment frequency, average in-layer severity, and reinstatement premium for an excess-of-loss (XL) reinsurance layer applied to a list of ground-up losses. |
| `exchange_1031_analyzer` | Calculates gains, boot, and deadlines for like-kind exchanges. |
| `exchange_netflow_analyzer` | Summarizes exchange wallet activity for accumulation/distribution signal generation. |
| `executive_summary_generator` | Formats operational metrics into a Thunder-ready briefing. |
| `exit_multiple_analysis` | Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.). |
| `exit_tax_calculator` | Computes exit tax exposures for investors emigrating from the US, Germany, or Canada. |
| `exotic_barrier_option_pricer` | Provides approximate closed-form barrier option prices for single-barrier European options. Uses the Reiner-Rubinstein analytic formulas for standard barrier types. |
| `expected_shortfall_decomposition` | Basel III ES attribution by computing conditional tail expectations and factor contributions. |
| `expense_allocation_engine` | Distributes fund expenses across share classes according to commitment or NAV weights. |
| `expense_categorizer` | Maps expense strings to IRS categories using heuristics. |
| `expense_ratio_calculator` | Computes underwriting expense ratio and breakdowns for acquisition, general & administrative, and other expenses. Supports both trade basis (vs. NWP) and statutory basis (vs. NEP). |
| `expense_ratio_impact` | Quantifies the difference in ending balance between two funds with different expense ratios and reports cumulative fee drag. |
| `facility_amendment_fee_calculator` | Computes amendment consent fees based on participation levels. |
| `factor_exposure_calculator` | Calculates factor betas and contribution to variance per factor. |
| `factor_tilted_portfolio` | Implements Barra-style factor tilting by solving a constrained least-squares system to match target factor shifts while minimizing benchmark deviation. |
| `failure_diagnostic_generator` | Summarizes attempts, hypothesizes root causes, and prescribes human actions. |
| `farmland_valuation` | Capitalizes normalized NOI per acre and blends with comparable sale metrics to determine farmland value. |
| `fastapi_to_mcp_wrapper` | Generate MCP-compliant TOOL_META dict and Python wrapper function code from a function name, docstring, and parameter list. |
| `fatca_withholding_calculator` | Applies Chapter 4 withholding based on FATCA status and documentation validity. |
| `fcf_quality_analyzer` | Compares free cash flow to net income and highlights working capital effects. |
| `fear_greed_composite` | Combines multiple sentiment metrics into a 0-100 fear/greed composite score. |
| `feature_flag_manager` | Gets, sets, lists, or evaluates feature flags stored in config/feature_flags.json. |
| `federal_income_tax_estimator` | Applies 2024 U.S. federal tax brackets to compute AGI, taxable income, tax liability, marginal rate, and bracket-level breakdown. |
| `fee_drag_analyzer` | Summarizes fees and calculates annualized drag versus AUM. |
| `fee_drag_calculator` | Estimates net IRR after management fees, performance carry, and other charges. Carry drag is only applied to returns above the hurdle rate. |
| `feedback_collector` | Stores categorized feedback with auto-responses. |
| `feedback_response_generator` | Generates human-like responses to agent feedback with priority flags. |
| `feedback_sentiment_analyzer` | Computes sentiment trends and common themes from feedback entries. |
| `ffo_affo_calculator` | Calculates FFO/AFFO and payout ratios for REITs. |
| `fiat_to_crypto_onramp_audit` | Audits fiat-to-crypto on-ramp transactions for volume, fees, velocity, and anomalous spikes. |
| `fibonacci_extension` | Computes Fibonacci extension projections (100%–261.8%) for trend continuation targets. |
| `fibonacci_retracement` | Computes common Fibonacci retracement prices (23.6%, 38.2%, 50%, 61.8%, 78.6%) for trend analysis. |
| `financial_entity_graph` | Constructs an in-memory adjacency graph of financial entities (funds, companies, LPs, GPs, properties) and their ownership / investment relationships. Computes degree centrality for each node, finds connected components via BFS, and identifies hub entities whose centrality exceeds median + 1 standard deviation. |
| `financial_highlight_extractor` | Summarizes headline metrics, growth narratives, and risks for presentations. |
| `financial_literacy_quiz` | Provides educational quizzes for goodwill content. |
| `financial_ratio_analyzer` | Calculates common liquidity, leverage, and profitability ratios using provided balance sheet and income statement figures. |
| `fire_number_calculator` | Computes the FIRE nest egg based on expenses and withdrawal rate, simulates years to reach it with contributions, and reports Coast/Barista FIRE thresholds. |
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
| `first_lien_second_lien_analyzer` | Allocates recovery value between first-lien and second-lien creditors. |
| `first_loss_tranche_pricer` | Monte Carlo Vasicek/Li large pool approximation for equity tranches using base-correlation averaging to determine the effective copula correlation. |
| `flyio_deploy_status` | Builds Fly.io API requests and summarizes allocation health. |
| `force_index` | Applies Elder's Force Index with optional EMA smoothing to detect bullish or bearish thrusts. |
| `foreign_tax_credit_calculator` | Applies the FTC limitation formula for passive and general baskets. |
| `form_1065_k1_allocator` | Splits partnership income items by partner percentages consistent with IRC §704(b). |
| `form_1099_generator` | Produces Snowdrop's 1099-NEC structure for Thunder review. |
| `forward_rate_agreement_calculator` | Calculates FRA settlement amounts given contracted and market rates. |
| `four_percent_rule_calculator` | Applies the 4% rule to approximate sustainable withdrawals, adjusts for desired horizon and inflation, and scores success probability heuristically. |
| `fragment_number_monitor` | Filters Fragment number listings by prefix and budget. |
| `franchise_analytics_reporter` | Summarizes revenue, royalties, and operational health per franchise operator. |
| `franchise_billing_reconciler` | Calculates royalty balances for each franchise operator. |
| `franchise_onboarder` | Checks franchise safety gates and returns royalty terms. |
| `franchise_royalty_calculator` | Computes 10% RSS revenue royalties owed by Bar-in-a-Box franchisees. |
| `frax_impermanent_loss_guardrail` | Simulates Frax IL exposure for dual-asset pools and recommends caps. |
| `frax_liquidity_rebalance_playbook` | Builds Frax liquidity rebalance plans for yield rotations. |
| `frax_lsd_leverage_spread_modeler` | Models Frax LSD leverage spreads with health-factor guardrails. |
| `free_cash_flow_yield` | Derives free cash flow yield and compares against earnings/dividend yields when available. |
| `freight_rate_analyzer` | Evaluates shipping freight index momentum, route-level rate dispersion, and market tightness signals for dry bulk, tanker, or container markets. |
| `fund_benchmark_comparison` | Compares a fund's KPIs to benchmark values and flags underperformance. Returns per-metric deltas, beat/miss flags, and overall hit rate. |
| `fund_expense_allocator` | Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight. |
| `fund_leverage_analyzer` | Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios. |
| `fund_of_funds_allocator` | Creates a heuristic allocation maximizing expected return under diversification rules. |
| `fund_of_funds_optimizer` | Uses scenario analysis with CVaR targeting to produce FoF weights under allocation caps. |
| `fund_restructuring_tax` | Evaluates IRC §§351, 368, 367 and EU Merger Directive treatment for fund Merger/Domestication transactions. |
| `funding_dilution_calculator` | Walks through successive funding rounds to compute new share issuances, share prices, ownership percentages, and aggregate dilution for founders. |
| `futures_curve_analyzer` | Classifies contango/backwardation, computes annualized roll yield per tenor, implied cost of carry, and carry trade signal from spot + futures curve. |
| `futures_roll_analyzer` | Evaluates roll cost, carry, and recommendation for futures positions. |
| `fx_calculator` | Computes FX forward rates via covered interest parity and related metrics. |
| `fx_forward_calculator` | Calculates forward rates, points, and hedging costs for currency hedges. |
| `fx_option_pricer` | Calculates FX option premiums and Greeks via Garman-Kohlhagen model. |
| `fx_rate_fetcher` | Retrieves spot FX quotes and inverse rates via ExchangeRate-API. |
| `fx_risk_exposure_calculator` | Aggregates gross/net FX exposures and estimates VaR. |
| `fx_swap_valuation` | Values currency basis swaps using discounted cash flows. |
| `gap_analyzer` | Scans OHLC data for breakaway, runaway, exhaustion, and common gaps, tracking fill status. |
| `gas_fee_estimator` | Provides conservative fee estimates for TON and SOL transfers. |
| `gcp_secret_manager` | Create, read, rotate, list, or delete secrets in Google Cloud Secret Manager. Uses Secret Manager API v1 with explicit service account credentials — no gcloud CLI, no ADC. Requires roles/secretmanager.admin on the service account. |
| `gdpr_fin_data_scrub` | Removes or pseudonymises PII from financial data records per GDPR Article 5(1)(e) (storage limitation) and Article 25 (data protection by design). Uses SHA-256 hashing for reversible pseudonymisation or full redaction, preserving non-PII financial fields. |
| `generate_k1_schema` | Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items. |
| `geocoding_lookup` | Google Geocoding API skill for address normalization, coordinate lookup, address validation, and timezone resolution. Used in real estate and location-based financial analysis pipelines. |
| `geographic_concentration_analyzer` | Calculates HHI by region and flags concentration against limits. |
| `get_ab_test_insights` | Calculates Moltbook engagement win rates comparing Gemini 2.0 Flash-Lite and Grok 4.1 Fast based on historical performance. |
| `ghost_ledger` | Google Sheets fund-accounting bridge. Supports initializing a new ledger spreadsheet with structured tabs, reading tab data, appending rows, summing vault balances, and writing autonomous decision entries to THE LOGIC LOG tab for audit traceability. |
| `ghost_ledger_enricher` | Annotates Ghost Ledger transactions with ROI heuristics and metadata. |
| `ghost_ledger_reconciler` | Compare ledger snapshots to live balances with zero-tolerance policy. |
| `ghost_ledger_sheets_reader` | Loads Ghost Ledger rows from Google Sheets for the requested notebook section and filters them to a date range. |
| `ghost_ledger_sheets_writer` | Appends validated ledger rows to Ghost Ledger Google Sheets tabs. |
| `ghost_town_detector` | Raises an alert when 14 days pass without paid transactions. |
| `github_issue_tracker` | Fetches labeled GitHub issues and estimates difficulty. |
| `global_tax_withholding_skill` | Calculates the withholding tax on a distribution to an international LP. Applies any available tax treaty rate in preference to the default rate. Grants full exemption (0%) to qualifying entities such as pension funds and sovereign wealth funds. Returns the withholding amount, effective rate, and net distribution after withholding. |
| `goodwill_cask_allocator` | Allocates the daily Goodwill cask budget until depleted, then closes the tap. |
| `gordon_growth_model` | Computes intrinsic value using Gordon Growth, plus yield and growth sensitivity. |
| `gp_clawback_calculator` | Evaluates carry distributions versus whole-fund entitlement and recommends clawback. |
| `gp_co_invest_calculator` | Calculates GP and LP capital allocations plus promote economics for co-investment deals. Returns GP commitment, LP commitment, and the promote pool available for the GP. |
| `gradual_rollout_controller` | Decides if an agent is part of a canary rollout using deterministic hashing. |
| `grant_milestone_tracker` | Summarizes milestone completion, disbursements, and deadlines for grants. |
| `grant_proposal_handler` | Accepts, evaluates, and adjudicates Goodwill grant proposals. |
| `green_building_subsidy_audit` | Audits a commercial building's eligibility for green building tax incentives including the Investment Tax Credit (ITC) for solar, Section 179D energy efficiency deduction, and a curated set of state-level ESG incentives. Returns eligible programs, estimated values, and requirements met. |
| `gsib_score_calculator` | Computes Basel systemic importance score using indicator values and denominators. |
| `hackathon_coordinator` | Manages hackathon lifecycle and scores submissions when provided. |
| `hash_rate_security_model` | Calculates PoW security metrics and estimated 51% attack costs drawing from Nakamoto consensus economics. |
| `heartbeat` | Checks Ghost Ledger readiness, required API keys, and reconciliation freshness before writing HEARTBEAT.md with the current timestamp. |
| `hedge_fund_alpha_decomposition` | Performs multi-factor OLS (Fama-French-Carhart) to estimate alpha, betas, R², and information ratio for hedge fund returns. |
| `hedging_cost_calculator` | Quantifies hedging cost, downside, and upside caps across hedge types. |
| `heikin_ashi_calculator` | Converts standard candles to Heikin-Ashi and reports trend direction and strength. |
| `heloc_calculator` | Calculates HELOC borrowing power, interest-only draw payments, amortized repayment amounts, and total interest based on rate and term parameters. |
| `hierarchical_risk_parity` | Constructs Lopez de Prado's Hierarchical Risk Parity (HRP) allocation with single-linkage clustering and recursive bisection risk budgeting. |
| `high_yield_savings_comparator` | Compares multiple savings accounts by incorporating APY, minimum balances, and monthly fees to surface the best net yield with 1-year and 5-year projections. |
| `historical_replay` | Applies historical drawdowns to portfolio weights to estimate losses. |
| `historical_var_calculator` | Historical simulation VaR/ES with Kupiec backtest p-value using equal or exponential age weights. |
| `historical_volatility` | Computes realized volatility via close-to-close, Parkinson, Garman-Klass, or Yang-Zhang estimators. |
| `hsa_triple_tax_advantage` | Projects HSA balances using constant contributions and growth to highlight tax savings from deductions, tax-free compounding, and qualified medical withdrawals. |
| `ibnr_reserve_calculator` | Estimates IBNR reserves using a volume-weighted chain-ladder approach. Accepts a loss development triangle (accident years × development periods) and per-year premiums. Returns age-to-age development factors, projected ultimates, IBNR by year, and an expected loss ratio. |
| `ichimoku_cloud` | Generates Ichimoku Kinko Hyo components (Tenkan, Kijun, Senkou A/B, Chikou) for full cloud analysis. |
| `identity_access_provisioner` | Generate provisioning instructions for identity requests with entitlements and expiry validation. |
| `idr_waterfall_calculator` | Allocates distributable cash through IDR tiers for MLPs. |
| `ifrs17_csm_calculator` | Calculates IFRS 17 contractual service margin and amortizes it over coverage units. |
| `ifrs17_risk_adjustment` | Computes risk adjustment as VaR minus expected loss using the confidence level technique. |
| `ifrs9_ecl_calculator` | Computes 12-month and lifetime ECL discounted at the effective interest rate per IFRS 9. |
| `ifrs9_stage_classifier` | Classifies assets into IFRS 9 stages using PD migration and delinquency criteria. |
| `illiquidity_premium_estimator` | Computes the Amihud price impact ratio and converts it to an illiquidity premium using Amihud (2002). |
| `imf_sdr_allocation_tracker` | Tracks IMF Special Drawing Rights (SDR) holdings vs allocations for a country, converts to USD, and assesses quota adequacy. |
| `impermanent_loss_calculator` | Computes impermanent loss percentage for constant product pools given price ratio shifts. |
| `implied_volatility_solver` | Computes implied volatility from an observed option price using bisection on the Black-Scholes model. |
| `incident_escalation_router` | Determines escalation targets and automatic guardrails based on severity. |
| `incident_tracker` | Opens, updates, or lists incidents with SLA tracking and JSONL logging. |
| `india_gst_tax_calculator` | Calculates Indian Goods and Services Tax (GST) for services including cross-border supply, SEZ, and export scenarios. Applies IGST Act 2017 rates, OIDAR (Online Information Database Access and Retrieval) rules, and LUT (Letter of Undertaking) exemptions for zero-rated exports. |
| `industry_benchmark_comparator` | Ranks Snowdrop metrics versus benchmark percentiles to highlight strengths and gaps. |
| `inflation_adjusted_return` | Calculates nominal versus real returns by discounting investment growth for inflation and highlighting purchasing power erosion. |
| `inflation_deflation_tracker` | Computes inflation rates and estimates deflation crossover dates. |
| `inflation_hedging_simulator` | Models sovereign fund real returns across inflation scenarios and recommends allocation shifts for inflation protection. |
| `inflation_linker_pricer` | Discounts inflation-linked coupons on the real yield curve and reports price and duration versus inflation assumptions. |
| `influence_scorer` | Scores agent influence using a simplified PageRank iteration. |
| `information_ratio_calculator` | Computes Information Ratio, tracking error, active return, and hit rate. |
| `infrastructure_project_finance` | Constructs a single-asset project model to evaluate DSCR, LLCR, and equity IRR against capex and leverage assumptions. |
| `installment_option_pricer` | Binomial tree valuation of installment (pay-as-you-go) options with optimal abandonment before the next premium is due. |
| `insurance_coverage_tracker` | Summarizes insurance coverages, gaps, and renewal windows. |
| `insurance_leverage_calculator` | Computes leverage and capacity utilization metrics for P&C insurers: net written premium-to-surplus, liabilities-to-surplus, investment leverage, and capacity headroom vs. A.M. Best benchmarks. |
| `insurance_linked_securities_tool` | Analyzes expected loss, attachment/exhaustion probabilities, multiple-at-risk (MAR), risk-adjusted spread, and relative value score for ILS instruments (cat bonds, industry loss warranties, sidecars). |
| `insurance_regulatory_checker` | Checks NAIC Risk-Based Capital (RBC) ratio and NWP-to-surplus leverage against standard P&C regulatory thresholds. Returns action level classification, surplus adequacy assessment, and list of regulatory concerns. |
| `insurance_tower_allocation_optimizer` | Aligns tower layers with modeled loss percentiles to minimize gaps. |
| `intent_classifier` | Heuristically classifies operator text into MCP skill intents |
| `interest_coverage_ratio` | Calculates interest and fixed charge coverage ratios. |
| `interest_rate_risk_banking_book` | Computes IRRBB delta EVE and NII across the six Basel shock scenarios. |
| `interest_rate_sensitivity_reit` | Calculates fixed vs floating mix, duration, and DV01 for the debt stack. |
| `interest_rate_swap_analyzer` | Values a fixed/float interest rate swap and reports DV01 and break-even rate. |
| `interest_rate_swap_valuer` | Computes MTM, PV legs, and DV01 for swaps using provided discount curve. |
| `intl_ae_fund_tax` | Outlines UAE's zero-withholding environment and new 9% corporate tax for mainland profits. |
| `intl_au_fund_tax` | Computes Australian dividend/interest/royalty withholding, MIT incentives, and 30% corporate tax for onshore management entities. |
| `intl_br_fund_tax` | Models Brazil's statutory withholding regime and 34% IRPJ/CSLL burden on Brazilian blockers. |
| `intl_ca_fund_tax` | Calculates Canadian withholding vs treaty relief and applies the 26.5% combined federal/provincial corporate rate when a Canadian permanent establishment exists. |
| `intl_ch_fund_tax` | Computes Swiss withholding and refund potential plus cantonal/federal corporate tax on Swiss permanent establishments. |
| `intl_cl_fund_tax` | Handles Chilean additional tax, treaty reductions, and 27% first-category tax for local operations. |
| `intl_co_fund_tax` | Models Colombian withholding without treaty protection and applies the 35% corporate rate (20% for FTZ) to local PE income. |
| `intl_de_fund_tax` | Models German Kapitalertragsteuer, solidarity surcharge, and the treaty relief schedule while applying a 29.8% combined corporate plus trade tax rate for German PE profits. |
| `intl_es_fund_tax` | Analyzes Spanish savings tax withholding and corporate tax for Spanish managers. |
| `intl_fr_fund_tax` | Determines French withholding outcomes and 25% corporation tax impact when a French permanent establishment exists. |
| `intl_gb_fund_tax` | Assesses UK withholding under ITA 2007 and the US-UK treaty while modeling 25% corporation tax on UK permanent establishments. |
| `intl_hk_fund_tax` | Provides Hong Kong profits tax modeling and notes absence of treaty relief for US investors. |
| `intl_id_fund_tax` | Captures Indonesian withholding (including the 0.1% share transfer tax) and the 22% corporate income tax on local operations. |
| `intl_ie_fund_tax` | Evaluates Irish withholding and 12.5% trading tax for Irish fund platforms. |
| `intl_il_fund_tax` | Calculates Israeli withholding versus treaty caps and applies 23% corporate tax for Israeli permanent establishments. |
| `intl_in_fund_tax` | Handles Indian Section 195 withholding, FPI capital gains, and local corporate tax when India permanent establishments exist. |
| `intl_it_fund_tax` | Handles Italian substitute withholding, treaty relief, and IRAP/IRES corporate taxation for Italian desks. |
| `intl_jp_fund_tax` | Calculates Japanese WHT (20.315% standard) vs US treaty reductions and applies the 30.5% corporation tax to Japanese permanent establishment profits. |
| `intl_kr_fund_tax` | Evaluates Korean withholding vs treaty relief and the 24.2% corporate tax burden on Korean permanent establishments. |
| `intl_lu_fund_tax` | Models Luxembourg WHT (typically nil on interest/royalty) and local subscription tax exposure. |
| `intl_mx_fund_tax` | Handles Mexican withholding, capital gains rules, and the 30% corporate rate for Mexican managers. |
| `intl_nl_fund_tax` | Computes Dutch dividend WHT and conditional WHT while applying the 25.8% CIT for Dutch permanent establishments. |
| `intl_ph_fund_tax` | Captures Philippine withholding (including CREATE-era rates) and the domestic 25% corporate tax on Philippine permanent establishments. |
| `intl_sa_fund_tax` | Evaluates Saudi withholding and the 20% income tax plus 2.5% Zakat overlay for onshore operations. |
| `intl_se_fund_tax` | Computes Swedish dividend withholding, treaty relief, and the 20.6% corporate tax on Swedish permanent establishments. |
| `intl_sg_fund_tax` | Handles Singapore WHT on interest/royalties and Section 13X exemption modeling for local fund platforms. |
| `intl_th_fund_tax` | Computes Thai withholding, treaty reductions, and 20% corporate tax for Bangkok management entities. |
| `intl_tr_fund_tax` | Computes Turkish withholding, treaty rates, and 25% CIT for entities with Turkish permanent establishments. |
| `intl_vn_fund_tax` | Provides Vietnam foreign contractor tax computations and 20% corporate tax for onshore subsidiaries. |
| `intl_za_fund_tax` | Assesses South African dividend/interest withholding, CGT inclusion, and 27% corporate tax for local operations. |
| `inventory_valuation` | Runs FIFO, LIFO, and weighted-average calculations to derive COGS and ending inventory, highlighting gross profit differences between methods. |
| `investment_basics_explainer` | Returns plain-language explanations for foundational investing topics. |
| `investment_fee_audit` | Tallies management, advisory, and transaction fees across accounts and quantifies the 10-year drag while pointing to expensive providers. |
| `investor_letter_drafter` | Builds executive-ready investor letter sections. |
| `investor_qualification_validator` | Validates accredited investor status using income and net worth thresholds. |
| `investor_statement_generator` | Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR. Validates that called capital does not exceed commitment. |
| `invoice_aging_analyzer` | Groups invoices into standard aging buckets, calculates outstanding exposure, and estimates collection performance and bad debt reserves. |
| `invoice_factoring_calculator` | Computes advance, fees, and effective annual rate for factoring transactions. |
| `invoice_generator` | Generates franchise-friendly invoices with royalty handling. |
| `ipo_pricing_analyzer` | Evaluates implied valuation, dilution, and discount to comps for IPO ranges. |
| `irr_bridge_reporter` | Calculates IRR, DPI, RVPI, and TVPI along with driver bridge for investor reporting. |
| `irr_calculator` | Computes IRR via Newton-Raphson iteration for periodic cash flows. Requires at least one sign change in the cash flow series. Returns IRR as an annualized percentage. |
| `j_curve_analyzer` | Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return. Negative early net flows create the characteristic J shape. |
| `j_curve_modeler` | Simulates fund cash flows, NAV, and J-curve inflection metrics. |
| `javascript_sdk_generator` | Builds an ES module client with fetch wrappers and TypeScript types for skills. |
| `journal_entry_builder` | Builds balanced journal entries and assigns sequential IDs. |
| `json_to_xbrl_transformer` | Transform JSON financial facts into SEC XBRL-JSON format using the us-gaap taxonomy. Maps concept names to us-gaap namespace and generates inline XBRL-compatible output. |
| `jury_deliberation_orchestrator` | Structures prompts and verdicts for the Sonnet/Grok/Gemini debate loop. |
| `jury_verdict_aggregator` | Roll up model verdicts with dynamic confidence weighting and escalation logic. |
| `k1_allocator` | Allocates income, deductions, and distributions across partners with special allocations. |
| `kelly_criterion_calculator` | Computes Kelly fraction, position size, and expected growth rates. |
| `keltner_channels` | Calculates Keltner Channels: EMA midline with ATR-based upper and lower envelopes. |
| `key_derivation_helper` | Derives deterministic key identifiers from the master seed. |
| `key_person_insurance_valuation` | Calculates key person insurance amount using salary, pipeline, and replacement time. |
| `key_rate_duration` | Computes key rate durations by bumping individual zero buckets (1/2/5/10/20/30y) consistent with the Basel IRRBB supervisory outlier test. |
| `klinger_oscillator` | Implements the Klinger Volume Oscillator (fast/slow EMAs of volume force) with signal histogram. |
| `know_sure_thing` | Implements Martin Pring's KST oscillator via four smoothed rate-of-change components. |
| `knowledge_base_article_generator` | Summarizes frequent ticket resolutions into KB articles to reduce load. |
| `knowledge_base_indexer` | Builds an inverted index over documents and answers keyword queries. |
| `kpi_tracker` | Calculates KPI progress, highlights off-track metrics, and summarizes health. |
| `l2_mempool_privacy_guard` | Monitors encrypted mempool fallback coverage across Arbitrum/Base/Optimism. |
| `l2_shared_auction_tracker` | Aggregates shared sequencer auctions across major L2s to signal MEV demand. |
| `large_exposure_checker` | Identifies exposures exceeding Basel LE limits (25% Tier1, 15% for G-SIB counterparties). |
| `lbo_model_builder` | Models leverage, cash flows, and equity returns for a stylized LBO. |
| `lease_abstract_skill` | Extracts key commercial lease terms from raw lease text using regex-based pattern matching. Targets commencement date, expiration date, base rent, escalation rate, renewal options, and break clauses. Returns confidence score and list of fields that could not be extracted. |
| `lease_accounting_calculator` | Computes lease liability, ROU asset, and income statement impact for ASC 842. |
| `lease_expiration_schedule` | Creates lease expiration ladder showing annual rollover percentages. |
| `ledger_immutability_checker` | Build a SHA-256 hash chain over ledger entries to detect tampering and verify immutability. Each entry hash includes the prior hash, forming a blockchain-style chain. |
| `lesson_to_action_sync_bot` | Scan logs/lessons.md, cluster recurring entries, and emit recommended follow-up actions. |
| `lessons_analyzer` | Parses logs/lessons.md content for failure hotspots and trends. |
| `leverage_ratio_calculator` | Computes Basel leverage ratio including SA-CCR derivative add-ons and securities financing exposures. |
| `liability_driven_optimizer` | Matches liability duration/convexity and surplus targets by allocating across asset cash-flow profiles consistent with ERISA and Solvency II liability-driven investing practices. |
| `life_expectancy_calculator` | Calculates curtate life expectancy (e_x), complete life expectancy (ê_x), and median future lifetime from a list of annual qx mortality rates. Uses exact actuarial recursion: t_px = product of (1 - q_{x+k}) for k=0..t-1. |
| `linea_data_availability_cost_forecaster` | Forecasts Linea data availability costs when proofs spike. |
| `linea_proof_latency_profiler` | Profiles Linea proof latency and confidence based on queue depth and L1 gas noise. |
| `linea_prover_cluster_health_monitor` | Monitors Linea prover clusters for saturation and fallback readiness. |
| `linea_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Linea sequencer mempools and hints. |
| `linea_state_diff_audit_simulator` | Simulates Linea state diff coverage to spot risky batches before posting. |
| `linea_validity_challenge_planner` | Plans Linea validity challenge playbooks if proofs degrade. |
| `linear_regression_forecaster` | Fits y = mx + b and projects forward values with r-squared diagnostics. |
| `liquidity_coverage_ratio` | Basel III LCR computation with supervisory caps on Level 2 assets and haircut adjustments. |
| `liquidity_depth_analyzer` | Estimates price impact and slippage for CFMM pools. |
| `liquidity_premium_calculator` | Approximates annual liquidity drag from bid-ask spreads and funding costs. |
| `llc_compliance_tracker` | Calculates upcoming compliance deadlines for Stonewater Solutions LLC. |
| `loan_amendment_tracker` | Scores cumulative impact of loan amendments to highlight covenant drift. |
| `loan_amortization_calculator` | Computes monthly payment, amortization schedule, and payoff projections. |
| `loan_cds_basis_analyzer` | Decomposes LCDS-cash loan basis into funding, liquidity, and recovery adjustments for basis trades. |
| `loan_covenant_checker` | Tests financial covenants and highlights closest breaches. |
| `loan_loss_reserve_modeler` | Calculates expected credit losses by segment with macro overlays. |
| `loan_to_value_calculator` | Calculates senior and total LTV ratios with headroom checks. |
| `loan_to_value_reit` | Calculates gross and net loan-to-value ratios for REIT balance sheets. |
| `log_integrity` | Verify the SHA-256 hash chain in Snowdrop's invocation audit log. Detects deletions, modifications, or insertions. On suspicion, alerts to Ghost Ledger THE LOGIC LOG and writes a local INTEGRITY_ALERT file. Run daily via systemd timer for continuous tamper-evidence. |
| `log_rotation_manager` | Evaluates log files and proposes rotation/compression/deletion actions. |
| `long_term_memory_store` | Append-only JSONL memory store with taggable search and CRUD operations. |
| `longevity_swap_pricer` | Transforms mortality qx inputs into a survival curve, discounts the floating and fixed legs, and reports PV and longevity risk premium. |
| `lookback_option_pricer` | Monte Carlo valuation of fixed or floating strike lookback options by monitoring running extrema (Glasserman, 2003). |
| `loss_ratio_calculator` | Calculates incurred loss ratio, ALAE-inclusive ratio, and development-adjusted ultimate loss ratio from earned premium and loss components. |
| `lp_commitment_tracker` | Tracks commitment, called capital, and remaining unfunded balance for each LP. Reports fund-level call percentage and identifies LPs with zero unfunded capacity. |
| `lp_reporting_standard` | Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null. Produces structured markdown with sections for Fund Overview, Performance Metrics, Top Holdings, Cash Position, and Upcoming Events. |
| `ltv_calculator` | Computes LTV, discounted LTV, and payback metrics for each agent tier. |
| `macd_calculator` | Computes Moving Average Convergence Divergence (12/26/9 defaults) with bullish/bearish interpretation. |
| `macro_indicator_tracker` | Fetches recent FRED indicators and computes MoM trends. |
| `macro_scenario_builder` | Applies macro factor shocks to exposures to estimate scenario returns. |
| `managed_futures_trend_signal` | Computes normalized trend-following signals using short/medium/long moving averages and breakout statistics inspired by CTA models. |
| `management_fee_calculator` | Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis. |
| `management_fee_offset` | Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs. Net fee is floored at zero (cannot be negative). |
| `management_fee_vat_calculator` | Determines VAT/GST on management fees and whether exemptions/zero-rating apply. |
| `mandate_enforcer` | Injects mandated proposals at top of sprint backlog while respecting capacity. |
| `margin_initial_simm` | Approximates ISDA SIMM initial margin by aggregating weighted sensitivities per risk class. |
| `margin_requirement_calculator` | Computes SPAN-style margin based on risk weights and add-ons. |
| `market_data_fetcher` | Pulls CoinGecko quotes and 24h change metrics. |
| `market_risk_frtb_sa` | Computes delta/vega/curvature buckets with prescribed correlations to derive FRTB SA capital plus DRC add-on. |
| `market_risk_ima_capital` | Calculates IMA capital: max(m * VaR, m * sVaR) + IRC + CRM per Basel 2.5. |
| `market_value_calculator` | Converts multi-currency positions to a base currency and aggregates exposure. |
| `marketplace_take_rate_analyzer` | Calculates marketplace take rate, per-order contribution, estimated buyer/seller LTV, and a liquidity score using GMV, revenue, and CAC inputs. |
| `mass_index` | Implements Donald Dorsey's Mass Index using double EMA of high-low range. |
| `max_drawdown_analyzer` | Computes maximum drawdown statistics from an equity curve. |
| `mbs_prepayment_model` | Generates PSA-based CPR and SMM projections plus collateral amortization and balance run-off stats. |
| `mcclellan_oscillator` | Calculates McClellan Oscillator (EMA19-EMA39) and the Summation Index to gauge breadth thrusts. |
| `mcp_discovery_beacon` | Packages a list of Snowdrop skills into MCP-compatible advertisement payloads and generates the beacon configuration required for periodic self-registration on the MCP network. Calculates a visibility score (0–100) based on skill count and category diversity. |
| `mcp_tool_registrar` | Produces a JSON-RPC compliant MCP tools/list response for Snowdrop skills. |
| `mean_cvar_optimizer` | Minimizes portfolio conditional VaR via Rockafellar-Uryasev subgradient descent with simplex projection and optional target return constraint. |
| `mean_reversion_detector` | Estimates Ornstein-Uhlenbeck half-life and current deviation z-score via OLS regression. |
| `mean_reversion_score` | Computes z-score of price versus rolling mean and estimates Ornstein-Uhlenbeck half-life. |
| `mercury_balance_fetcher` | Retrieves account balances from Mercury's /api/v1/accounts endpoint. |
| `mercury_payment_sender` | Constructs ACH/wire payloads for Mercury but leaves them pending Thunder approval. |
| `mercury_transaction_ingest` | Pulls Mercury transactions, tags inflow/outflow, and formats for Ghost Ledger. |
| `merger_accretion_dilution` | Evaluates EPS impact of an acquisition with cash/stock mix and synergies. |
| `merger_arbitrage_spread` | Computes dollar and annualized spread along with implied deal probability from price-break analysis. |
| `merger_spread_implied_probability` | Calculates M&A deal closing probability from market spread, offer price, and unaffected downside. |
| `merit_review_state_identifier` | Identifies merit review states for state securities registration planning. |
| `message_signer` | Signs messages with an env-provided key for agent authentication. |
| `metals_supply_demand_analyzer` | Builds supply/demand surplus or deficit tallies for base metals, computes inventory coverage in months, and flags deficit conditions. |
| `mezzanine_return_calculator` | Calculates blended cash, PIK, and equity kicker returns for mezzanine debt. |
| `mlp_debt_coverage_ratio` | Computes EBITDA to debt service coverage for midstream partnerships. |
| `mlp_distributable_cash_flow_calc` | Calculates Distributable Cash Flow (DCF) and coverage ratios for Master Limited Partnerships. |
| `mlp_distributable_cash_flow_calculator` | Derives MLP distributable cash flow from EBITDA, capex, and non-cash adjustments. |
| `mlp_distribution_analyzer` | Calculates DCF coverage, leverage, and GP take for MLP distributions. |
| `mlp_distribution_coverage_ratio` | Computes distribution coverage ratio and leverage on payouts for midstream partnerships. |
| `mlp_dpu_growth_modeler` | Projects DPU growth considering EBITDA growth, IDRs, and dropdowns. |
| `mlp_ebitda_to_distribution_calculator` | Calculates EBITDA payout ratios to monitor sustainability of MLP distributions. |
| `mlp_growth_capex_return_calculator` | Evaluates projected EBITDA gains versus growth capex to estimate cash-on-cash returns. |
| `mlp_incentive_distribution_rights_analyzer` | Applies MLP IDR tiers to calculate GP vs LP cash splits at current distribution rates. |
| `mlp_k1_estimator` | Estimates income, return of capital, and UBTI exposure for MLP units. |
| `mlp_k1_income_allocator` | Allocates taxable income across unitholders based on ownership units. |
| `mlp_maintenance_capex_tracker` | Aggregates maintenance capex budgets vs actuals per asset to surface overruns. |
| `mlp_unitholders_return_calculator` | Calculates price and distribution contribution to total return for MLP units. |
| `mlp_volume_throughput_estimator` | Measures asset utilization and tariff revenue for MLP pipeline systems. |
| `model_risk_validator` | Computes discrimination and stability metrics for regulatory model validation. |
| `model_router` | Reads config/config.yaml and maps a task category to the correct model entry. |
| `moic_calculator` | Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital. Also returns gain/loss in dollar terms. |
| `moltbook_engagement_loop` | Analyzes Moltbook post history to determine optimal posting times (UTC), best-performing content types, recommended posting frequency, and forecasts expected engagement for the next post. |
| `moltbook_engagement_sheet` | Read and write the Moltbook Engagement Google Sheet — Snowdrop's command center. Actions: 'log_post' (append post to POST LOG), 'get_submolt_list' (read SUBMOLT DIRECTORY for strategy routing), 'get_stats' (aggregate performance data), 'daily_report' (compile daily stats from POST LOG, suitable for Slack), 'update_weekly_actual' (fill in this week's actual post count in WEEKLY FORECAST), 'update_performance' (upsert post upvotes/comments into POST PERFORMANCE tab — called by the performance poller), 'update_submolt_perf' (upsert per-submolt aggregate stats into SUBMOLT PERFORMANCE tab — called by the poller), 'update_karma' (upserts total account karma tracking into KARMA HISTORY tab). Designed to run cheaply with Gemini Flash Lite. |
| `moltbook_post_performance` | Fetch live upvotes and comments for one or more Moltbook posts by post_id. Returns engagement metrics, ROI score (upvotes*2 + comments*5), and traction status. Use for spot-checking specific posts or verifying the performance poller is working. Set write_to_sheet=True to also upsert results into the POST PERFORMANCE tab. |
| `moltbook_poster` | Formats Snowdrop skills for the Moltbook agent marketplace. |
| `moltbook_reputation_builder` | Generates structured Moltbook post drafts to build agent reputation, scores estimated engagement, and recommends the optimal submolt and tags. Now includes cost tracking. |
| `moltbook_sentiment_analyzer` | Scores Moltbook posts for financial sentiment and detects narrative shifts within submolts over a configurable lookback window. |
| `moltbook_stamina_monitor` | Monitors Moltbook API rate limits (stamina) from the Google Sheet and generates a 1-sentence health summary using a cheap model. |
| `momentum_oscillator` | Measures price momentum as the difference and percent change over a configurable lookback. |
| `momentum_signal_generator` | Calculates short vs long lookback momentum and standardized signal strength. |
| `money_flow_index` | Calculates the volume-weighted RSI known as Money Flow Index (MFI). |
| `money_transmitter_checker` | Flags actions that might require MTL coverage and provides guidance. |
| `monte_carlo_simulator` | Runs geometric Brownian motion simulations to generate percentile outcomes. |
| `monte_carlo_var` | Monte Carlo VaR/ES with Cholesky-based correlated shocks consistent with Basel 99% methodologies. |
| `mortality_table_lookup` | Returns representative 2017 CSO mortality assumptions (qx, lx, and curtate life expectancy) for a given age, gender, and smoker status. Interpolates to the nearest available age bucket. |
| `mortgage_amortization` | Generates a month-by-month mortgage payoff schedule with support for extra principal payments and reports payoff timing and interest savings. |
| `mortgage_pool_analyzer` | Calculates single-month mortality, conditional prepayment rate (CPR), conditional default rate (CDR), and loss severity for mortgage pools. |
| `mortgage_refinance_analyzer` | Compares an existing mortgage to a potential refinance by modeling monthly savings, break-even period, lifetime interest, and payoff horizon. |
| `moving_average_crossover` | Compares fast and slow simple moving averages to flag golden or death cross confirmations. |
| `moving_average_ribbon` | Calculates SMA values for multiple periods to form a ribbon and detect trend/squeeze signals. |
| `mrr_calculator` | Calculates MRR components and growth for Watering Hole subscriptions. |
| `mullvad_vpn_status` | Constructs Mullvad account queries and summarizes connection health. |
| `multi_bank_liquidity_sweeper` | Recommend cash sweeps across multiple banks using target min/max policies. |
| `multi_book_influence_tracker` | Calculates an agent's influence score across multiple social platforms, identifies top-performing interactions, and infers the influence trend over time. |
| `multi_currency_consolidator` | Converts positions into a base currency with exposure diagnostics. |
| `multi_jurisdiction_net_return` | Combines treaty withholding, local fund tax, and investor-level tax drag across income types. |
| `multi_l2_mev_burst_scheduler` | Schedules rollup transaction batches to sidestep simultaneous MEV bursts. |
| `multi_period_rebalancer` | Dynamic programming rebalancer choosing whether to rebalance or drift each period based on expected return trade-off versus transaction costs, following Bodie, Kane, Marcus multi-period optimization. |
| `multi_sig_workflow` | Classifies an action into auto, 2FA, or multi-sig approval paths. |
| `muni_bond_analyzer` | Computes tax-equivalent yield, breakeven rates, and annual savings for muni bonds. |
| `muni_taxable_equivalent` | Computes taxable-equivalent yields for tax-exempt municipal bonds incorporating AMT exposure, state deductibility, and the 3.8% Medicare net investment income surtax. |
| `mvrv_ratio_calculator` | Computes Market Value to Realized Value ratio to identify accumulation or euphoria regimes. |
| `natural_gas_storage_analyzer` | Compares EIA-style natural gas storage levels to 5-year seasonal averages, flags injection/withdrawal pace, and provides bullish/bearish market implication. |
| `nav_reconciliation` | Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. |
| `nav_rollforward_tracker` | Bridges opening NAV to closing NAV using period cash flows and valuation changes. |
| `negative_volume_index` | Computes the Negative Volume Index with a 255-day EMA signal line per Norman Fosback. |
| `net_interest_margin_calculator` | Computes current NIM, gap ratios, and projected NIM under rate shocks. |
| `net_operating_income_bridge` | Builds an NOI bridge showing contributions from volume, rate, occupancy, and opex. |
| `net_stable_funding_ratio` | Calculates ASF and RSF weighted balances to determine NSFR compliance. |
| `new_highs_new_lows` | Computes new-high minus new-low series, ratios, and signals. |
| `newsletter_composer` | Creates newsletters covering new skills, platform stats, and educational tips. |
| `nft_floor_price_analyzer` | Summarizes NFT market data into actionable floor price analytics including depth and wash-trade-adjusted velocity. |
| `nft_inventory_tracker` | Aggregates NFT holdings with valuation deltas and allocation mix. |
| `nft_royalty_cashflow_calculator` | Calculates gross and net royalty cash flows using volume, pricing, and fee inputs. |
| `nmtc_community_impact_scorer` | Scores NMTC projects across jobs, needs, and community benefits. |
| `nmtc_compliance_checker` | Evaluates census tract, QALICB, and substantially-all tests for NMTC projects. |
| `nmtc_deal_structurer` | Models NMTC leveraged structures with investor equity, leverage loans, and subsidy. |
| `nmtc_investor_return_calculator` | Calculates investor IRR over NMTC compliance period with tax credits and fees. |
| `noi_audit_tool` | Validates Net Operating Income (NOI) for a commercial real estate property. Computes NOI from gross revenue and operating expenses, calculates NOI margin, and flags material variance against a prior period if provided. |
| `noi_calculator` | Calculates NOI and margin from rental revenue and operating expenses. |
| `notice_filing_requirement_tracker` | Tracks Form D notice filing triggers and deadlines by state. |
| `notification_preferences_manager` | Gets, sets, or resets notification preferences per agent with persistence. |
| `notification_router` | Maps alert priority to Telegram/SMS/freeze workflows. |
| `nth_to_default_basket_pricer` | Monte Carlo Gaussian copula model (Li, 2000) for nth-to-default baskets with systematic correlation and discounted loss metrics. |
| `nvt_ratio_calculator` | Computes Willy Woo's Network Value to Transactions ratio with smoothing to classify valuation zones. |
| `oas_calculator` | Calibrates a lognormal Black-Derman-Toy short-rate lattice to the supplied zero curve and derives the option-adjusted spread (OAS) required to reconcile the lattice price with the observed market price. |
| `obv_calculator` | Computes cumulative On-Balance Volume to confirm price trends vs volume flows. |
| `occupancy_rate_forecaster` | Forecasts occupancy rates for the next 3 periods using simple linear regression on historical data, with optional adjustments for market absorption rate and new supply entering the market. |
| `occupancy_rate_tracker` | Computes weighted average occupancy and vacancy by property type. |
| `oil_breakeven_price_calculator` | Determines the breakeven oil price for an upstream producer including lifting costs, opex, sustaining capex, royalties, production taxes, and a target return margin. Supports both simple and government-take deduction methods. |
| `okr_tracker` | Calculates OKR progress, color codes, and highlights at-risk objectives. |
| `omega_ratio_calculator` | Computes Omega = sum(max(r-threshold,0)) / sum(max(threshold-r,0)). |
| `on_chain_liquidity_depth_estimator` | Aggregates order book levels until price impact exceeds a defined slippage limit. |
| `openapi_spec_generator` | Converts Snowdrop skill metadata into an OpenAPI 3.0.3 specification. |
| `openrouter_cost_logger` | Calculates OpenRouter call costs using the internal pricing table. |
| `operating_expense_ratio` | Calculates operating expense ratio and efficiency gap versus target. |
| `operating_leverage_calculator` | Computes contribution margin, DOL, breakeven revenue, and scenario EBIT deltas. |
| `operational_maturity_scorer` | Rates capabilities across dimensions and assigns an overall maturity level. |
| `operational_risk_sma` | Calculates SMA capital = BIC * ILM with Basel thresholds and loss component adjustments. |
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
| `options_greeks_calculator` | Returns price and Greeks for European options via Black-Scholes. |
| `options_implied_move` | Converts ATM straddle pricing into implied move, range, and annualized IV approximation. |
| `options_payoff_diagram` | Calculates strategy payoff across a price grid and identifies basic spread types. |
| `options_strategy_analyzer` | Aggregates multi-leg option strategy P&L and diagnostics. |
| `pain_ratio_calculator` | Computes the Pain Index (average drawdown magnitude) and Pain Ratio (return/Pain). |
| `pair_trade_analyzer` | Computes ratio z-scores, correlation, OLS half-life, and trade signals for price pairs. |
| `parabolic_sar` | Implements Welles Wilder's Parabolic SAR with configurable acceleration factors to trail price trends. |
| `parametric_var_calculator` | Basel variance-covariance VaR with component, marginal, and incremental attribution over a user horizon. |
| `partner_onboarding_validator` | Ensures partner submissions meet baseline technical and compliance requirements. |
| `partner_revenue_share_calculator` | Computes revenue share payouts per partner tier. |
| `partnership_tax_allocation_model` | Allocates partnership income among partners with preferred returns. |
| `paycheck_withholding_estimator` | Estimates paycheck taxes for federal, state, Social Security, and Medicare with net pay and annualized projections based on pay frequency. |
| `payment_gateway_router` | Determines which verification skill should process a payment receipt. |
| `payment_reconciler` | Reconciles Watering Hole payments against invoice records. |
| `payment_terms_optimizer` | Evaluates early-pay discounts to maximize savings within cash constraints. |
| `payment_waterfall_modeler` | Distributes cash through tranche priorities covering interest then principal. |
| `pdf_report_formatter` | Creates a layout-ready dict for PDF renderers (sections, TOC, metadata). |
| `pe_secondary_pricing` | Applies secondary market heuristics (quartile + remaining commitment) to derive bid discount and implied IRR. |
| `pe_valuation_dcf` | Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. |
| `peg_ratio_calculator` | Evaluates PEG ratio relative to growth and adjusts for dividend yield when provided. |
| `pendle_impermanent_loss_guardrail` | Simulates Pendle IL exposure for dual-asset pools and recommends caps. |
| `pendle_liquidity_rebalance_playbook` | Builds Pendle liquidity rebalance plans for yield rotations. |
| `pendle_lsd_leverage_spread_modeler` | Models Pendle LSD leverage spreads with health-factor guardrails. |
| `pension_vs_lump_sum` | Values lifetime pension payments versus a lump sum using discounting and inflation adjustments, providing breakeven timing and sensitivity scenarios. |
| `percent_above_ma` | Calculates % of symbols above their moving average to gauge breadth thrusts. |
| `performance_attribution` | Decomposes active return into allocation, selection, and interaction components. |
| `performance_attribution_tool` | Performs allocation, selection, and interaction attribution vs a benchmark. |
| `performance_poller_control` | Observe, trigger, or read the status of the Snowdrop Performance Poller subagent (A2A protocol). Actions: 'status' (last run time, posts polled, errors), 'trigger' (run poller immediately via subprocess), 'read_card' (return the A2A agent card JSON), 'read_log' (last N lines of poller log). The poller normally runs every 2h via cron but can be triggered on-demand. |
| `personal_loan_comparator` | Evaluates personal loan offers by accounting for origination fees, payments, total interest, and estimated effective APR to rank the cheapest option. |
| `pfic_qef_calculator` | Calculates PFIC inclusions and §1291 interest adjustments for offshore funds. |
| `physical_storage_cost_calculator` | Quantifies the full carry cost of holding physical commodity inventory: warehouse/storage fees, insurance, and financing cost over a given horizon. Returns total cost, per-unit cost, and implied break-even basis appreciation. |
| `pii_detector` | Finds PII in free-form text and masks the findings. |
| `pik_toggle_modeler` | Builds period schedules for cash and PIK interest accruals. |
| `pillar_3_disclosure_generator` | Prepares Pillar 3 style summary of capital ratios, RWAs, LCR/NSFR, and leverage metrics. |
| `piotroski_f_score` | Evaluates the nine Piotroski signals to rate financial strength. |
| `pitch_deck_generator` | Creates slide-by-slide pitch content for Snowdrop fundraising narratives. |
| `pivot_point_calculator` | Computes pivot points and support/resistance for Standard, Fibonacci, Woodie, Camarilla, and DeMark methods. |
| `places_search` | Search, discover, and retrieve details for businesses and points of interest using the Google Places API (New). Supports free-text search, nearby discovery, and full place detail lookups. Returns structured business data plus an investment_signal field assessing business density and health for real estate and market analysis. |
| `pme_calculator` | Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path. PME > 1.0 means the fund outperformed the public market benchmark. |
| `pnl_attribution_calculator` | Breaks daily P&L into price, carry, FX, and fee components. |
| `polygon_zkevm_data_availability_cost_forecaster` | Forecasts Polygon zkEVM data availability costs when proofs spike. |
| `polygon_zkevm_proof_latency_profiler` | Profiles Polygon zkEVM proof latency and confidence based on queue depth and L1 gas noise. |
| `polygon_zkevm_prover_cluster_health_monitor` | Monitors Polygon zkEVM prover clusters for saturation and fallback readiness. |
| `polygon_zkevm_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Polygon zkEVM sequencer mempools and hints. |
| `polygon_zkevm_state_diff_audit_simulator` | Simulates Polygon zkEVM state diff coverage to spot risky batches before posting. |
| `polygon_zkevm_validity_challenge_planner` | Plans Polygon zkEVM validity challenge playbooks if proofs degrade. |
| `portable_alpha_calculator` | Aggregates returns from alpha and beta sleeves, subtracts hedge cost, and reports contribution along with realized tracking error. |
| `portable_alpha_constructor` | Combines capital allocations to uncorrelated alpha sleeves with a futures overlay sized to target beta exposure, following the portable alpha framework used by Canadian pensions. |
| `portfolio_beta_calculator` | Calculates weighted average beta from constituent betas and weights. |
| `portfolio_concentration_checker` | Flags concentration exposures versus policy limits. |
| `portfolio_concentration_risk` | Flags single-name, sector, and factor concentration breaches. |
| `portfolio_duration_calculator` | Calculates aggregate dollar duration and DV01 for fixed income books. |
| `portfolio_optimization_tool` | Builds heuristic mean-variance weights using return expectations and volatilities. |
| `portfolio_rebalancer` | Compares target weights vs current positions and builds pending trade list. |
| `portfolio_rebalancing_calculator` | Compares current holdings with target allocations to produce trade instructions, drift metrics, and tax lot reminders for selling positions. |
| `portfolio_stress_test` | Applies historical crash scenarios (2008 GFC, 2020 COVID, Rate Shock) or custom shock tables to a portfolio. Calculates dollar and percentage loss per scenario, identifies the worst-hit asset in each scenario, selects the maximum drawdown scenario overall, and estimates the capital injection needed to recover to the original portfolio value. |
| `portfolio_variance_calc` | Calculate portfolio expected return, variance, standard deviation, Sharpe ratio, and diversification benefit using Modern Portfolio Theory (MPT). |
| `portfolio_variance_calculator` | Computes covariance matrix, portfolio variance/volatility, and risk contributions from asset weights. |
| `portfolio_volatility_calculator` | Estimates portfolio variance and volatility from a covariance matrix. |
| `position_reconciliation_tool` | Compares internal books with prime broker files and flags breaks. |
| `post_mortem_generator` | Creates structured post-mortem Markdown with action items and lessons learned. |
| `postgresql_ledger_adapter` | Builds parameterized SQL statements for Ghost Ledger backed by Postgres. |
| `power_option_pricer` | Closed-form pricing for type-I power options (payoff (S^n − K)^+) based on moment-adjusted Black-Scholes. |
| `power_price_calculator` | Calculates spark spread (gas-fired margin), dark spread (coal-fired margin), clean spark/dark spreads (including carbon cost), and generation dispatch signal. |
| `precious_metals_lease_rate` | Derives the implied precious metals lease rate from spot, forward, and USD interest rate inputs. Uses the GOFO (Gold Forward Offered Rate) identity: Lease Rate = USD Rate − GOFO, where GOFO = annualized forward premium. |
| `preferred_equity_analyzer` | Calculates preferred equity cash yield, coverage, and call protection metrics. |
| `preferred_return_calculator` | Calculates accrued preferred return on LP capital with configurable compounding frequency. Supports annual, quarterly, monthly, and daily compounding. |
| `premium_calculator` | Computes gross written premium from base rate, exposure units, experience modification, schedule credits, and other adjustments following standard manual rating methodology. |
| `premium_estimator` | Provides heuristic premium estimates based on business profile and coverage type. |
| `present_value_calculator` | Computes the present value of a lump sum or annuity, adjusting for payment timing and reporting aggregate payments and implied interest. |
| `price_alert_evaluator` | Checks price conditions (above, below, pct_change) and prioritizes alerts. |
| `price_feed_aggregator` | Fetches CoinGecko and Kraken prices then returns the median. |
| `pricing_elasticity_estimator` | Uses observed price/volume pairs to estimate demand elasticity and recommends revenue/profit maximizing price points. |
| `pricing_feed_voter` | Computes a consensus price across vendor feeds and flags quotes outside tolerance bands. |
| `prime_broker_reconciliation` | Reconciles positions and cash between internal books and the prime broker. |
| `private_credit_term_analyzer` | Computes all-in yields, covenant protection, and risk assessment for private credit facilities. |
| `procyclicality_buffer` | Implements Basel CCyB mapping from credit-to-GDP gap and aggregates jurisdictional CCyB exposure-weighted rates. |
| `profit_margin_analyzer` | Builds a margin waterfall starting at revenue to show gross, operating, EBITDA, pretax, and net profit percentages. |
| `proforma_generator` | Projects multi-year cash flows, NOI, and returns for income properties. |
| `prompt_ab_tester` | Appends prompt experiment outcomes and computes per-variant stats. |
| `prompt_injection_shield` | Scans incoming agent requests for prompt injection attacks, role-play overrides, encoding tricks, and unauthorized tool access. Returns threat level and blocked tools. |
| `prompt_template_manager` | Provides CRUD operations on config/prompt_templates.json. |
| `proof_of_labor_arbiter` | Scores labor contributions and returns credit recommendations. |
| `property_type_diversification` | Computes HHI concentration and highlights overweight property types. |
| `proposal_manager` | Submits, lists, fetches, or closes proposals per Snowdrop governance rules. |
| `protocol_revenue_analyzer` | Calculates revenue per product and annualizes it to monitor concentration risk. |
| `pubsub_publisher` | Google Cloud Pub/Sub skill for event streaming between Snowdrop services. Supports publish, pull, topic and subscription management via the Pub/Sub REST API. |
| `put_call_ratio` | Tracks put/call ratios to identify fear vs greed sentiment zones. |
| `put_spread_calculator` | Calculates payoff metrics for bull or bear put spreads. |
| `python_sdk_generator` | Builds a basic Python client with typed methods for each Snowdrop skill. |
| `qoz_investment_tax_benefit_calculator` | Quantifies tax deferral and exclusion benefits for QOZ capital gains. |
| `quanto_option_pricer` | Black-Scholes quanto pricer with correlation adjustment between asset and FX volatility (Hull, Ch. 28). |
| `quarterly_report_generator` | Summarizes fund performance against benchmarks for the quarter. |
| `quota_share_calculator` | Computes ceded and retained premium, losses, ceding commission, and net underwriting result under a proportional quota share treaty. Supports fixed and provisional/sliding scale commission. |
| `railway_deploy_status` | Builds Railway GraphQL queries and parses deployment states when provided. |
| `rainbow_option_pricer` | Monte Carlo rainbow option pricer using correlated Gaussian sampling for best-of and worst-of structures (Stulz, 1982). |
| `ralph_wiggum_retry_manager` | Determines whether to retry or escalate tasks per ethics playbook. |
| `range_accrual_note` | Uses Black-style lognormal assumption for the reference rate to compute expected coupons on a range accrual structured note. |
| `rate_card_manager` | Retrieves or updates tier pricing for Watering Hole skills. |
| `rate_limit_cascade` | Downgrades Opus→Sonnet→Haiku→Grok when a model is saturated. |
| `real_asset_correlation_matrix` | Computes Pearson correlations across provided asset return series and compares tail-period correlations to detect crisis regimes. |
| `real_estate_tax_escrow` | Calculates monthly escrow reserve requirements for property taxes and insurance. Uses the millage rate system (mills per $1,000 of assessed value). Outputs monthly escrow, annual tax, and combined annual total. |
| `real_rate_calculator` | Computes ex-ante and ex-post real rates using Fisher relations. |
| `realized_cap_calculator` | Computes realized capitalization from UTXO-style inputs and infers unrealized profit and supply composition. |
| `rebalance_trigger` | Checks portfolio split vs. target bands and surfaces recommended skims or reviews. |
| `recallable_distribution_tracker` | Summarizes recallable vs permanent distributions per LP. Recallable distributions can be called back by the GP for follow-on investments. |
| `reconcile` | Daily reconciliation engine. Compares live Kraken exchange balances against the Ghost Ledger (Google Sheets). Emits a CRITICAL alert to Thunder via Telegram if any discrepancy is detected. Zero-tolerance policy. |
| `recovery_rate_estimator` | Aggregates LGD and recovery percentages by class. |
| `recovery_runbook_generator` | Outputs a step-by-step recovery plan tailored to the failure type. |
| `referral_reward_calculator` | Determines referral tier, rate, and milestone bonuses. |
| `referral_tracker` | Aggregates referral spend and issues credits to promoters. |
| `refinancing_analyzer` | Evaluates refinance savings, break-even, and NPV for proposed loan terms. |
| `regime_aware_allocator` | Fits a two-state hidden Markov model to realized returns and allocates according to risk-on/risk-off regime targets similar to Norges Bank's conditional allocation process. |
| `regime_detector` | Detects bull vs bear regimes using realized volatility and return trends. |
| `regulation_d_exemption_analyzer` | Determines Reg D rule availability based on size and investor counts. |
| `regulatory_capital_estimator` | Estimates Basel-style RWA and capital ratios for market risk books. |
| `regulatory_capital_waterfall` | Applies deductions to CET1 and adds AT1/Tier2 to produce regulatory ratios. |
| `reinsurance_treaty_analyzer` | Evaluates quota share and per-occurrence excess-of-loss treaty economics. Returns ceded and net premium/losses, ceding commission, and net combined ratio. |
| `reit_compliance_tester` | Evaluates income/asset/shareholder tests for REIT status. |
| `reit_dividend_analyzer` | Evaluates dividend yield, payout ratios, and tax characterization. |
| `reit_dividend_coverage` | Evaluates REIT dividend sustainability by computing FFO and AFFO payout coverage ratios. Classifies risk as low, medium, or high, and flags dividends at risk of cuts. |
| `reit_dividend_reinvestment_logic` | Executes Dividend Reinvestment Plan (DRIP) logic for a REIT distribution. Calculates whole and fractional shares purchasable at the current share price, computes the blended new cost basis per share, and produces a reinvestment summary suitable for ledger entry. |
| `reit_dividend_tax_treatment_analyzer` | Allocates REIT dividends into tax character categories and rates. |
| `reit_ffo_calculator` | Calculates REIT Funds From Operations (FFO) and Adjusted FFO (AFFO) per NAREIT standards. FFO adds back real estate depreciation and amortization to GAAP net income and excludes gains/losses on property sales. |
| `reit_nav_calculator` | Values properties via NOI/cap rates to derive NAV per share. |
| `reit_nav_premium_tracker` | Tracks the premium or discount of a REIT's market price relative to Net Asset Value (NAV) per share. Computes a z-score against historical premiums (when provided) and signals overvalued, undervalued, or fair value. |
| `reit_sector_comparison` | Benchmarks company metrics versus sector medians across KPIs. |
| `relative_strength_ranker` | Computes total returns over multiple lookbacks and ranks assets by composite score. |
| `remittance_cost_optimizer` | Ranks cross-border remittance corridors by total cost, identifies cheapest and fastest options, and filters by urgency. |
| `rent_roll_analyzer` | Calculates occupancy, income, loss-to-lease, and lease rollover risk. |
| `rental_rate_growth_calculator` | Calculates cash and GAAP leasing spreads versus expiring rents. |
| `repo_implied_rate` | Derives the implied repurchase (repo) rate from the Treasury cash-futures basis, adjusting for coupons and accrued interest. |
| `repo_value_estimator` | Estimates tokens and dollars needed to rebuild the repo from scratch. |
| `reputation_staking` | Locks reputation points against delivery, quality, or fairness claims. |
| `request_queue_manager` | Manages enqueue/dequeue/peek/stats for agent request queues. |
| `request_rate_limiter` | Enforces per-agent token bucket rate limits and returns retry hints. |
| `required_minimum_distribution` | Applies IRS life expectancy divisors to compute required minimum distributions for traditional IRAs, 401(k)s, and inherited accounts while projecting 5 years ahead. |
| `resampled_efficient_frontier` | Applies Michaud resampling by bootstrapping mean-variance inputs and averaging allocations to produce confidence bands for the efficient frontier. |
| `research_library_manager` | Publishes and queries Goodwill research papers for the community. |
| `residual_income_model` | Discounts residual incomes plus current book value to estimate intrinsic value. |
| `resolution_planning_metrics` | Generates key metrics for resolution planning submissions (165(d)). |
| `response_cache_manager` | Provides get/set/invalidate operations for skill response cache entries. |
| `retention_ratio_analyzer` | Analyzes retention and cession ratios with net loss ratio and reinsurance leverage metrics. Measures how much premium and loss exposure is retained vs. ceded and evaluates reinsurance program efficiency. |
| `retirement_income_gap_analyzer` | Aggregates guaranteed income sources with planned withdrawals to determine gaps versus target retirement spending and highlight additional savings required. |
| `retirement_savings_projector` | Forecasts retirement savings from current age to retirement, reporting nominal and inflation-adjusted balances plus a 4% rule shortfall analysis. |
| `revenue_anomaly_detector` | Monitors rolling revenue patterns for drops and spikes. |
| `revenue_per_skill_analyzer` | Aggregates billing records to highlight top-performing skills and concentration |
| `revenue_recognition_checker` | Applies the ASC 606 five-step model to contracts and allocates revenue to obligations. |
| `reverse_dcf` | Derives the growth rate required to justify the current market capitalization. |
| `review_cost_estimator` | Approximates token/time cost to review a submission. |
| `risk_adjusted_return_calculator` | Calculates risk-adjusted metrics (Sharpe, Sortino, Treynor) plus annualized return/volatility and maximum drawdown from a series of periodic returns. |
| `risk_budgeting_allocator` | Computes equal-risk-contribution weights (a la Maillard, Roncalli, Teiletche 2010) by solving for the portfolio weights whose marginal contributions match risk budgets. |
| `risk_parity_allocator` | Uses iterative proportional fitting on the covariance matrix to achieve target risk budgets per asset. |
| `risk_parity_calculator` | Allocates inverse-volatility weights and scales to a target portfolio volatility. |
| `risk_parity_weights` | Approximates risk-parity allocation via inverse volatility and reports risk contributions. |
| `robust_covariance_estimator` | Produces Ledoit-Wolf shrunk covariance and a Minimum Covariance Determinant (MCD) estimate to stabilize mean-variance inputs against outliers and regime shifts. |
| `roc_calculator` | Computes percentage rate of change and optional SMA smoothing to track acceleration. |
| `roi_annotator` | Enriches ledger transactions with qualitative ROI commentary. |
| `rolling_risk_analyzer` | Computes rolling Sharpe, max drawdown, beta (optional), and detects volatility regime shifts. |
| `roth_conversion_optimizer` | Quantifies the up-front tax bill, future tax savings, and breakeven timing for a Roth conversion using bracket differentials and an assumed 5% growth rate. |
| `route_optimizer` | Google Route Optimization API skill for fleet tour optimization, point-to-point directions, and distance matrix calculations. Supports real estate inspections, logistics planning, and multi-stop delivery sequencing. |
| `rsi_calculator` | Computes RSI using J. Welles Wilder's smoothing to spot overbought or oversold conditions. |
| `rule_of_72_calculator` | Uses the rule of 72 alongside logarithmic growth math to estimate doubling, tripling, and quadrupling timelines for an annual return. |
| `runway_scenario_modeler` | Projects runway months under bull/base/bear net burn assumptions. |
| `rvpi_calculator` | Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital. RVPI is the unrealized component of fund value — what the portfolio is still worth. |
| `rwa_cash_flow_waterfall_model` | Allocates tokenized asset cash flows across tranches based on priority or share percentages. |
| `rwa_compliance_status_tracker` | Rolls up AML, KYC, and filing checks into a single compliance status report. |
| `rwa_concentration_risk_analyzer` | Calculates concentration metrics for tokenized asset pools by asset type or geography. |
| `rwa_credit_enhancement_analyzer` | Measures expected loss coverage from subordination, reserves, and insurance protections. |
| `rwa_custody_cost_calculator` | Summarizes custody expenses for RWA structures using AUC fees and retainers. |
| `rwa_density_analyzer` | Computes RWA/exposure percentages and flags segments deviating from portfolio average. |
| `rwa_investor_accreditation_checker` | Evaluates investor profile against configurable accreditation thresholds. |
| `rwa_liquidity_premium_calculator` | Combines base rates, liquidity spreads, and tenor adjustments to set yield targets. |
| `rwa_market_depth_estimator` | Calculates average daily volume and depth to gauge token liquidity. |
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
| `rwa_originator_quality_scorer` | Combines historical loss rates, audits, and reporting cadence into an originator score. |
| `rwa_portfolio_stress_tester` | Applies price haircuts and default shocks to estimate stressed RWA portfolio values. |
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
| `rwa_redemption_mechanics_analyzer` | Evaluates redemption policies including frequency, notice, and penalties for tokenized RWAs. |
| `rwa_regulatory_capital_calculator` | Calculates RWA exposure and capital requirement based on risk weights and target ratios. |
| `rwa_secondary_market_price_model` | Calculates VWAP and volatility-based bands for RWA tokens on secondary markets. |
| `rwa_servicer_quality_scorer` | Generates a composite score for RWA servicers using accuracy, staffing, and remittance metrics. |
| `rwa_token_valuation_model` | Discounts projected cash flows to derive intrinsic value per RWA token. |
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
| `rwa_yield_spread_analyzer` | Computes yield spreads relative to benchmark bonds and adjusts for duration risk. |
| `sa_ccr_calculator` | Simplified SA-CCR calculation: EAD = alpha * (RC + PFE). |
| `saas_metrics_dashboard` | Generates a snapshot of SaaS health including net new MRR, churn metrics, ARPU, net revenue retention, and the quick ratio. |
| `safe_note_converter` | Calculates SAFE conversion price, shares, and founder dilution. |
| `same_store_noi_growth` | Calculates YoY same-store NOI growth and contribution analysis. |
| `sanctions_network_monitor` | Cross-check wallet exposures against sanctions feeds and return flagged entities. |
| `sanctions_screener` | Checks entities/wallets against curated sanctions heuristics. |
| `sar_generator` | Drafts FinCEN SAR payloads without auto-filing. |
| `savings_goal_planner` | Solves for the monthly contribution required to hit a savings goal given current balance, time horizon, and expected return, with annual milestones. |
| `scaling_decision_engine` | Evaluates telemetry against thresholds to suggest scale up/down/hold. |
| `scheduled_workflow_trigger` | Determines due, overdue, and next trigger times for workflows. |
| `schema_validator` | Checks arbitrary data payloads against JSON Schema definitions (subset). |
| `scroll_data_availability_cost_forecaster` | Forecasts Scroll data availability costs when proofs spike. |
| `scroll_proof_latency_profiler` | Profiles Scroll proof latency and confidence based on queue depth and L1 gas noise. |
| `scroll_prover_cluster_health_monitor` | Monitors Scroll prover clusters for saturation and fallback readiness. |
| `scroll_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Scroll sequencer mempools and hints. |
| `scroll_state_diff_audit_simulator` | Simulates Scroll state diff coverage to spot risky batches before posting. |
| `scroll_validity_challenge_planner` | Plans Scroll validity challenge playbooks if proofs degrade. |
| `seasonal_pattern_analyzer` | Aggregates historical commodity prices by calendar month to estimate seasonal factors, identify peak and trough months, and compute seasonal amplitude. |
| `secondary_offering_dilution` | Evaluates dilution, proceeds, and TERP for primary/secondary offerings. |
| `secrets_audit_monitor` | Checks whether required secrets are present in the environment and flags missing/empty variables. |
| `section_1231_gain_loss_calculator` | Computes 1231 gains and recapture amounts under 5-year lookback. |
| `sector_etf_comparator` | Ranks sector ETFs by performance metrics over a labelled period. |
| `sector_rotation_analyzer` | Measures sector relative strength and assigns rotation phases (leading/lagging/etc.). |
| `securitization_cashflow_modeler` | Generates month-by-month cash flow projections including CPR/CDR and servicing fees. |
| `self_audit_daily` | Compares planned vs executed actions, logs discrepancies, and triggers freezes if needed. |
| `self_deploy_check` | Detect unpushed commits on the current branch and push to origin/main to trigger Cloud Build CI/CD. Returns a summary of pushed commits or 'nothing to deploy' if HEAD matches origin/main. |
| `self_employment_tax_calculator` | Computes Social Security and Medicare self-employment tax components, including the deductible half and additional Medicare surtax. |
| `settlement_fail_tracker` | Ages failed trades and estimates fail penalties. |
| `sharpe_ratio_calculator` | Calculates Sharpe, Sortino, and ancillary performance stats. |
| `sheet_pruner` | Prevents data bloat by autonomously removing logs older than the retention period from the Command Center. |
| `sheets_to_postgres_migrator` | Produces SQL/ETL plan for moving Ghost Ledger tabs into PostgreSQL tables. |
| `shout_option_pricer` | Monte Carlo shout option valuation treating shout dates as discrete lookback checkpoints where locked intrinsic is preserved per Rubinstein's construction. |
| `signature_verifier` | Verifies HMAC-SHA256 signatures for incoming agent messages. |
| `skeptic_challenge_generator` | Produces a structured counter-position with risks and precedents for a thesis. |
| `skewness_kurtosis_analyzer` | Computes skewness, kurtosis, and Jarque-Bera statistic for return distributions. |
| `skill_builder` | Meta-skill: takes a plain-English skill description and generates a production-ready Snowdrop Python skill module via the Assembly Line (Haiku drafts, Sonnet polishes, Opus certifies for jury-tier complexity). Optionally writes the result to disk. |
| `skill_catalog_sync` | Returns live skill count breakdown (total, free, premium, failed) from the running server. Pass regenerate=True to rebuild SNOWDROP_SKILLS.md and SKILLS.md from the current codebase (admin use only). |
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
| `sma_calculator` | Calculates rolling simple moving averages to identify price alignment with key trend periods. |
| `smart_contract_access_control_diff_checker` | Diffs access-control lists between versions to highlight missing roles. |
| `smart_contract_authority_matrix_auditor` | Builds a permission matrix for each method to catch privilege creep. |
| `smart_contract_bridge_finality_checker` | Verifies bridge contracts enforce finality depth before crediting funds. |
| `smart_contract_cross_chain_message_profiler` | Profiles bridge message flow for ack failures or stalled packets. |
| `smart_contract_cross_pool_drain_simulator` | Runs stress flows across linked pools to detect capital draining routes. |
| `smart_contract_delegatecall_guardrail` | Inspects delegatecall targets to ensure they respect access control and immutability assumptions. |
| `smart_contract_emergency_pause_validator` | Validates pause pathways ensure multi-sig approvals and enforce cooldowns. |
| `smart_contract_fee_switch_diff_checker` | Compares fee switch states across deployments to expose unnoticed toggles. |
| `smart_contract_flashloan_pressure_tester` | Runs deterministic flash-loan scenarios to measure collateral buffers and slippage thresholds. |
| `smart_contract_gas_estimator` | Aggregates gas consumption inputs and converts them to native and USD fee estimates. |
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
| `social_security_estimator` | Approximates the primary insurance amount (PIA) and adjusts benefits for early or delayed claiming relative to full retirement age. |
| `sol_balance_checker` | Calls Solana RPC getBalance and returns SOL for the configured wallet. |
| `sol_transfer_builder` | Constructs Solana transfer payloads and fee estimates pending approval. |
| `solana_jit_execution` | Calculate Just-in-Time liquidity provisioning plan for a Solana AMM pool with yield estimation and risk scoring. |
| `solvency_ii_mcr` | Derives MCR using Solvency II linear formula (Life + Non-life) and SCR floor/cap. |
| `solvency_ii_scr` | Aggregates market, counterparty, life, health, and non-life SCRs with standard correlations. |
| `solvency_ratio_calculator` | Computes the Solvency II SCR coverage ratio from component risk modules. Applies the standard formula diversification benefit before adding operational risk. Returns coverage ratio, action level classification, and capital buffers. |
| `sortino_ratio_calculator` | Computes Sortino ratio with downside deviation and contextualizes relative to Sharpe. |
| `sovereign_debt_yield_curve` | Computes sovereign bond spreads over US Treasuries, builds yield curves, and identifies inversions for Global South debt analysis. |
| `sovereign_fiat_bridge` | Converts sovereign fiat currency to a target digital asset for treasury onboarding. Applies jurisdiction-specific regulatory surcharges on top of a base protocol fee. Estimates settlement time and enumerates regulatory requirements for the given jurisdiction. |
| `sovereign_reserves_analyzer` | Analyzes sovereign reserve composition (fiat/gold/digital) and compares against IMF adequacy metrics. |
| `sovereign_wealth_alpha_source` | Screens and ranks sovereign wealth fund investment opportunities by return/risk ratio against configurable criteria. |
| `spac_arbitrage_analyzer` | Breaks down SPAC trust yield, deal optionality, and expected value based on probability inputs. |
| `spread_option_pricer` | Computes two-asset spread option values via Kirk's approximation and correlated Monte Carlo for verification. |
| `sprint_planner` | Selects backlog tasks for the sprint based on priority, capacity, and dependencies. |
| `stakewise_impermanent_loss_guardrail` | Simulates StakeWise IL exposure for dual-asset pools and recommends caps. |
| `stakewise_liquidity_rebalance_playbook` | Builds StakeWise liquidity rebalance plans for yield rotations. |
| `stakewise_lsd_leverage_spread_modeler` | Models StakeWise LSD leverage spreads with health-factor guardrails. |
| `staking_reward_tracker` | Summarizes staking rewards, projected income, and outstanding claims per validator. |
| `staking_yield_calculator` | Analyzes staking rewards to derive APR, payout cadence, and token emissions. |
| `standard_deviation_channel` | Performs least-squares regression on prices and offsets by standard deviation bands. |
| `starknet_data_availability_cost_forecaster` | Forecasts Starknet data availability costs when proofs spike. |
| `starknet_proof_latency_profiler` | Profiles Starknet proof latency and confidence based on queue depth and L1 gas noise. |
| `starknet_prover_cluster_health_monitor` | Monitors Starknet prover clusters for saturation and fallback readiness. |
| `starknet_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Starknet sequencer mempools and hints. |
| `starknet_state_diff_audit_simulator` | Simulates Starknet state diff coverage to spot risky batches before posting. |
| `starknet_validity_challenge_planner` | Plans Starknet validity challenge playbooks if proofs degrade. |
| `startup_valuation_multiples` | Applies growth-adjusted revenue multiples and sector EBITDA comparables to produce valuation ranges and comparable context notes. |
| `state_crowdfunding_exemption_checker` | Determines state crowdfunding eligibility based on issuer location and raise size. |
| `state_income_tax_apportionment_model` | Apportions taxable income among states via three-factor formula. |
| `state_nexus_analyzer` | Assesses economic and physical nexus triggers for hedge funds under Wayfair and marketplace sourcing rules. |
| `state_securities_exemption_checker` | Determines state exemption availability by offering type and investor count. |
| `statistical_anomaly_detector` | Flags z-score anomalies across global or rolling windows. |
| `statistical_arbitrage_signal` | Computes OLS hedge ratio, spread z-score, and entry/exit guidance for a pair. |
| `statistical_arbitrage_zscore` | Performs OLS regression of X on Y to compute hedge ratio, z-score, and Ornstein-Uhlenbeck half-life for pairs trading. |
| `status_report_generator` | Formats Snowdrop execution updates into a markdown status report. |
| `stochastic_oscillator` | Implements George Lane's %K/%D oscillator with configurable slowing to detect momentum shifts. |
| `stock_split_calculator` | Computes the new share count and per-share price after a split while keeping total value and cost basis aligned. |
| `stock_to_flow_calculator` | Applies the PlanB stock-to-flow regression to estimate model price and scarcity context. |
| `straight_line_rent_calculator` | Computes straight-line rent adjustment over the remaining lease term. |
| `strategy_backtester` | Runs deterministic backtests for rule-based trading strategies. |
| `stress_test_capital_trajectory` | Projects CET1 ratio quarter-by-quarter under supervisory stress inputs. |
| `stress_test_pnl` | Applies factor shocks to estimate stressed P&L for positions. |
| `stress_test_scenario_engine` | Applies supervisory stresses to rate, FX, equity, and spread sensitivities to produce capital planning P&L breakdowns. |
| `structured_deposit_pricer` | Combines the discount cost of principal protection with the price of an embedded equity option to price structured deposits. |
| `structured_logger` | Appends structured log entries with correlation metadata to a JSONL file. |
| `student_loan_repayment_comparator` | Models standard, graduated, IBR, PAYE, and REPAYE student loan plans to expose monthly payments, total paid, and potential forgiveness along with a recommendation. |
| `subscription_doc_parser` | Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores. |
| `subscription_facility_analyzer` | Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact. Subscription lines are backed by LP commitments. |
| `subscription_manager` | Identifies subscriptions due for billing and drafts charge records. |
| `supertrend` | Applies the Supertrend algorithm (ATR bands with dynamic flips) to mark trailing stops and trend phase. |
| `supply_chain_risk_insurance_model` | Scores suppliers and calculates contingent BI exposure. |
| `support_escalation_router` | Determines routing paths for support tickets based on category, tier, and urgency. |
| `support_resistance_finder` | Finds price levels with multiple touches using swing highs/lows within a lookback window. |
| `support_ticket_manager` | Creates, updates, closes, and lists support tickets with SLA tracking. |
| `surety_bond_capacity_calculator` | Estimates surety bonding capacity from financial statements. |
| `swap_curve_builder` | Bootstraps an overnight-indexed swap (OIS) discount curve and overlays vanilla IRS par rates with turn-of-year adjustments per ISDA methodology. |
| `swap_rate_calculator` | Computes par swap rate, fixed leg PV, float leg PV, and NPV. |
| `swaption_pricer` | Prices payer or receiver swaptions via Black's model and returns Greeks. |
| `swarm_message_router` | Validates sender/recipient roles and produces routing envelopes. |
| `synthetic_cdo_pricer` | Implements the Gaussian copula with Vasicek closed form to deliver expected loss and spreads for each tranche. |
| `synthetic_market_data_generator` | Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills. |
| `system_health_composite` | Rolls subsystem telemetry into a weighted score and recommendations. |
| `taiko_data_availability_cost_forecaster` | Forecasts Taiko data availability costs when proofs spike. |
| `taiko_proof_latency_profiler` | Profiles Taiko proof latency and confidence based on queue depth and L1 gas noise. |
| `taiko_prover_cluster_health_monitor` | Monitors Taiko prover clusters for saturation and fallback readiness. |
| `taiko_sequencer_privacy_leak_scanner` | Detects privacy leak heuristics across Taiko sequencer mempools and hints. |
| `taiko_state_diff_audit_simulator` | Simulates Taiko state diff coverage to spot risky batches before posting. |
| `taiko_validity_challenge_planner` | Plans Taiko validity challenge playbooks if proofs degrade. |
| `tail_ratio_calculator` | Calculates right-tail/left-tail ratio plus skewness and kurtosis for fat-tail detection. |
| `tail_risk_hedging_cost` | Aggregates put option strikes/premiums to estimate hedge cost, drawdown coverage, and breakeven levels. |
| `tailscale_mesh_healthcheck` | Pulls device metadata from Tailscale and surfaces online/offline state. |
| `task_dependency_resolver` | Performs topological sorting and surfaces parallelizable groups. |
| `tax_aware_rebalancer` | Constructs a tax-lot aware rebalance plan that respects capital gains budgets, wash-sale windows, and differentiates long- vs short-term tax rates per IRS Publication 550 guidance. |
| `tax_basics_guide` | Shares plain-language US tax basics by entity type (goodwill only). |
| `tax_bracket_marginal_analyzer` | Reports the taxpayer's current federal bracket, marginal rate, remaining income headroom before the next bracket, and a visualization of all bracket tiers. |
| `tax_loss_harvester` | Ranks positions by after-tax savings potential with wash sale warnings. |
| `tax_loss_harvesting_calculator` | Aggregates available capital losses to offset realized gains, estimates tax savings (federal + state), and flags 30-day wash sale blackout periods. |
| `telegram_alert_formatter` | Formats alerts using Telegram MarkdownV2 with escaping and CTA support. |
| `telegram_command_router` | Parses Telegram commands (/balance, /audit, /brief, /price, /status, /help). |
| `telemetry_collector` | Appends anonymous usage telemetry after stripping PII. |
| `telemetry_reporter` | Aggregates telemetry events by dimension with latency/error metrics. |
| `telnyx_alert` | Drafts Telnyx SMS payloads to notify Thunder of high-priority events. |
| `tenant_concentration_tracker` | Flags top tenant exposure versus single-tenant and top-10 limits. |
| `tenant_credit_analyzer` | Scores tenant credit strength based on financials and lease metrics. |
| `term_premium_calculator` | Compares observed term yield to expected average of policy rates. |
| `term_sheet_analyzer` | Evaluates post-money, ownership, and liquidation waterfalls for venture deals. |
| `three_statement_modeler` | Generates linked financial statements using indirect cash flow method. |
| `three_way_reconciliation_bot` | Matches GL, administrator, and custodian balances to highlight breaks exceeding tolerance. |
| `threshold_monitor` | Evaluates metrics against warning and critical thresholds. |
| `thunder_executive_briefing` | Generates a concise, plain-English daily executive briefing for Thunder (operator). Synthesises portfolio value, P&L, open alerts, reconciliation status, and market movers into a human-readable summary. Classifies overall severity as routine, attention, or urgent and surfaces action items. |
| `thunder_signal` | Sends a severity-tiered Telegram alert to Thunder (the Operator). Severity levels: CRITICAL (vault breach, reconciliation failure), WARNING (Sybil infiltration, threshold breach), INTEL (general updates, Great Day). |
| `tier2_instrument_amortization` | Calculates remaining Tier 2 recognition after applying 20% annual haircuts during final 5 years. |
| `tif_district_calculator` | Projects increment revenue and coverage for TIF districts over the term. |
| `timber_valuation` | Applies Faustmann formula to timber growth and stumpage pricing to compute NPV and optimal rotation age. |
| `timezone_scheduler` | Converts event timestamps into relevant time zones and flags off-hour meetings. |
| `tip_pool_distributor` | Splits gratuities by hours worked and role multipliers for Watering Hole staff. |
| `tlac_calculator` | Calculates TLAC ratios vs 18% RWA and 6.75% leverage thresholds (US G-SIB). |
| `token_burn_deflation` | Analyzes burn events vs emissions to classify token supply behavior. |
| `token_contract_validator` | Flags risky token authority settings and liquidity constraints. |
| `token_cost_tracker` | Logs model API usage and enforces the $50/day spend cap. |
| `token_efficiency_benchmarker` | Compares tokens per skill/line/quality across internal and community contributors. |
| `token_estimator` | Estimates token counts and costs across Claude/GPT/Gemini families. |
| `token_inflation_rate_calculator` | Transforms token emission inputs into annualized inflation metrics. |
| `token_issuance_cost_calculator` | Aggregates issuance cost buckets and derives per-token cost of capital. |
| `token_lockup_period_analyzer` | Summarizes lockup mechanics with current remaining term and unlock schedule. |
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
| `token_supply_analyzer` | Analyzes emission schedules and burn rates to forecast supply paths and inflation. |
| `token_supply_modeler` | Projects circulating supply month by month with mint and burn events. |
| `token_swap_estimator` | Estimates CFMM swap execution with slippage buffer for Thunder review. |
| `token_unlock_scheduler` | Analyzes vesting events to quantify unlock pace, dilution, and sell pressure windows. |
| `token_velocity_calculator` | Computes MV=PQ velocity metrics and highlights value unlocked through slower token circulation. |
| `token_vesting_schedule_calculator` | Converts vesting plans with cliffs into cumulative unlock curves and outstanding balances. |
| `tokenized_bond_duration_calculator` | Computes Macaulay and modified duration from cash-flow schedules of tokenized bonds. |
| `tokenized_commodity_basis_tracker` | Compares token prices against spot commodity benchmarks adjusting for carry costs. |
| `tokenized_credit_portfolio_analyzer` | Aggregates RWA credit exposures to derive yield, expected loss, and coverage statistics. |
| `tokenized_fund_nav_calculator` | Aggregates asset values minus liabilities to derive NAV per RWA token. |
| `tokenized_real_estate_yield_calculator` | Computes NOI yield for tokenized real estate including leverage cost adjustments. |
| `ton_balance_checker` | Queries TON Center for the configured wallet and returns TON balances. |
| `ton_payment_verifier` | Validates TON transactions for Snowdrop payments without broadcasting funds. |
| `ton_transfer_builder` | Constructs TON transfer payloads without broadcasting. |
| `ton_usdg_yield_tracker` | Calculates accrued USDG yield for TON staking ladders. |
| `ton_w5_gasless_transfer` | Build TON W5 wallet gasless transfer payload using battery sponsorship for zero-fee TON movements. |
| `total_return_swap_analyzer` | Breaks down TRS financing costs, received return, and net P&L. |
| `total_return_swap_pricer` | Discounts realized equity leg cashflows against floating leg funding to output PVs, breakeven spread, and sensitivity. |
| `tracking_error_calculator` | Computes tracking error, active return, and a rough active-share proxy from return differences. |
| `tracking_error_optimizer` | Minimizes ex-ante tracking error relative to the benchmark while enforcing factor exposure targets via Lagrangian solution of the quadratic optimization problem. |
| `trade_break_resolver` | Scores trade breaks by aging and category to prioritize remediation. |
| `trade_lifecycle_tracker` | Summarizes trade lifecycle stages with elapsed times and bottlenecks. |
| `trade_settlement_lc_logic` | Validates Letters of Credit against UCP 600 international rules, checks document completeness, and generates settlement recommendations. |
| `tranche_analyzer` | Calculates tranche credit enhancement, expected loss, and implied ratings. |
| `transaction_anomaly_flagger` | Scores transactions for amount, counterparty, category, and timing anomalies. |
| `transaction_fee_analyzer` | Analyzes fee samples and block utilization to guide transaction fee bidding. |
| `transaction_freeze` | Activates the global freeze flag so downstream payment skills stop immediately. |
| `transaction_ingest_bridge` | Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. |
| `transaction_sim_pre_flight` | Simulates an on-chain transaction in isolation before submission. Checks for insufficient balances, high slippage, and other failure conditions. Returns projected new balances, estimated gas cost in USD, and a success probability score derived from balance adequacy and warning count. |
| `transfer_pricing_fund_analyzer` | Evaluates arm's-length ranges for fund management fees under IRC §482 and OECD TP Guidelines (2022). |
| `treasury_sweep_recommender` | Identifies idle cash available for sweeps and proposes destinations (pending Thunder). |
| `treaty_rate_lookup` | Returns statutory vs treaty withholding rates and article citations for major US treaties. |
| `trend_line_calculator` | Constructs trendlines using linear regression or peak/trough anchors to monitor price breaks. |
| `treynor_ratio_calculator` | Computes Treynor ratio, beta, Jensen's alpha, and systematic risk contribution. |
| `trial_balance_generator` | Aggregates journal entries into account-level debit/credit totals. |
| `trial_balance_snapshotter` | Converts ledger entries into a base-currency trial balance and highlights NAV deltas. |
| `triple_net_reconciliation` | Reconciles estimated NNN (triple-net) lease pass-through charges (CAM, insurance, property taxes) against actual year-end costs. Determines per-category variance and whether the tenant owes a true-up payment or is owed a credit. |
| `trust_score_calculator` | Combines signals such as payments, vouches, and disputes into a trust tier. |
| `tsi_calculator` | Calculates William Blau's True Strength Index via double EMA of price momentum. |
| `tvpi_calculator` | Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI). TVPI = (cumulative_distributions + residual_value) / paid_in_capital. Also reports DPI, RVPI, and NAV share. |
| `two_stage_ddm` | Discounts dividends through a high-growth phase and a terminal perpetuity. |
| `ubti_blocker_analyzer` | Computes unrelated business taxable income under IRC §§512-514 and recommends blocker structures. |
| `ulcer_index` | Computes the Ulcer Index and related drawdown metrics to capture downside pain. |
| `underwriting_profit_calculator` | Computes underwriting profit/loss, underwriting margin, combined ratio, and return on net earned premium from earned premium, losses, and expenses. |
| `unit_economics_sensitivity` | Applies +/- variation to CAC, LTV, margin, and churn to highlight best/worst case unit economics and breakeven thresholds. |
| `unitranche_yield_calculator` | Calculates unitranche cash yield plus amortized OID and fees. |
| `uptime_tracker` | Calculates uptime %, MTBF, MTTR, and outage extremes from heartbeat logs. |
| `us_state_ak_fund_tax` | Highlights Alaska's zero income tax treatment while adding borough mill rate exposure for real assets. |
| `us_state_al_fund_tax` | Computes Alabama pass-through entity tax, nonresident withholding, and composite filing triggers pursuant to Ala. Code §§40-18-14 and 40-18-24. |
| `us_state_ar_fund_tax` | Applies Arkansas top individual rate, SALT workaround election, and nonresident withholding needed under Ark. Code §26-51-919. |
| `us_state_az_fund_tax` | Calculates Arizona pass-through entity tax, Form 165 withholding, and composite filing tests under Ariz. Rev. Stat. §§43-1011 and 43-1147. |
| `us_state_ca_fund_tax` | Models California PIT, LLC fee, nonresident withholding, and AB 150 pass-through entity tax under Cal. Rev. & Tax. Code §§17041, 17942, 18662, and 19900. |
| `us_state_co_fund_tax` | Computes Colorado income tax, elective entity-level tax, and nonresident withholding obligations referencing Colo. Rev. Stat. §§39-22-104 and 39-22-601. |
| `us_state_ct_fund_tax` | Evaluates Connecticut PE Tax, nonresident withholding, and exemption status pursuant to Conn. Gen. Stat. §§12-699 and 12-704d. |
| `us_state_de_fund_tax` | Tracks Delaware intangible exemption status and annual LP/LLC franchise tax even though no entity-level income tax applies to qualified investment funds. |
| `us_state_fl_fund_tax` | Determines Florida corporate income/franchise tax exposure for hedge fund management entities while noting pass-through exemption for entities that remain partnerships. |
| `us_state_ga_fund_tax` | Calculates Georgia income tax, SALT workaround election, and nonresident withholding pursuant to O.C.G.A. §§48-7-20 and 48-7-129. |
| `us_state_hi_fund_tax` | Calculates Hawaii individual tax, nonresident withholding, and GET cash drag on management fees. |
| `us_state_ia_fund_tax` | Implements Iowa flat tax transition, SALT election, and nonresident withholding thresholds. |
| `us_state_id_fund_tax` | Applies Idaho flat income tax, SALT parity election, and Form 41P withholding mechanics. |
| `us_state_il_fund_tax` | Models Illinois individual income rate, replacement tax, and the entity-level election mandated by Public Act 102-0658. |
| `us_state_in_fund_tax` | Handles Indiana composite withholding and SALT workaround calculations under Ind. Code §§6-3-2-1 and 6-3-4-12. |
| `us_state_ks_fund_tax` | Models Kansas top bracket, corporate override, and BAHT SALT parity withholding mechanics. |
| `us_state_ky_fund_tax` | Aggregates Kentucky income tax, LLET, and composite filing logic under KRS 141.020 and 141.0401. |
| `us_state_la_fund_tax` | Computes Louisiana top marginal tax, elective PTE tax, and nonresident withholding for composite return compliance. |
| `us_state_ma_fund_tax` | Calculates Massachusetts flat tax, millionaires surtax, and SALT workaround election under Mass. Gen. Laws ch. 62 and ch. 63D. |
| `us_state_md_fund_tax` | Evaluates Maryland state income tax, nonresident withholding, and elective entity-level tax referencing Md. Code, Tax-Gen. §§10-102 and 10-210. |
| `us_state_me_fund_tax` | Calculates Maine income tax, surtax, and elective entity-level tax savings for investment funds. |
| `us_state_mi_fund_tax` | Runs Michigan flow-through tax computations including nonresident withholding consistency with Mich. Comp. Laws §§206.51 and 206.325. |
| `us_state_mn_fund_tax` | Applies Minnesota top bracket approximations, composite withholding, and elective PTE tax logic under Minn. Stat. §§290.06 and 289A.835. |
| `us_state_mo_fund_tax` | Estimates Missouri tax, elective entity-level tax, and Form MO-2NR withholding per Mo. Rev. Stat. §§143.011 and 143.441. |
| `us_state_ms_fund_tax` | Handles Mississippi flat income tax, SALT election, and franchise tax exposure. |
| `us_state_mt_fund_tax` | Computes Montana income tax, nonresident withholding, and the annual license fee for entities. |
| `us_state_nc_fund_tax` | Handles North Carolina flat tax, SALT election, and nonresident withholding compliance. |
| `us_state_nd_fund_tax` | Applies North Dakota's lowest-in-US 1.95% rate and required composite filings. |
| `us_state_ne_fund_tax` | Models Nebraska rate reductions, nonresident withholding, and SALT election dynamics. |
| `us_state_nh_fund_tax` | Models New Hampshire BPT exposure and interest/dividend withholding for hedge funds. |
| `us_state_nj_fund_tax` | Computes New Jersey individual tax proxies, BAIT election effect, and nonresident withholding for LP interests. |
| `us_state_nm_fund_tax` | Computes New Mexico income tax, SALT election, and Gross Receipts Tax on management fees. |
| `us_state_nv_fund_tax` | Calculates Nevada Commerce Tax exposure for investment funds meeting the $4M receipts trigger. |
| `us_state_ny_fund_tax` | Calculates New York State PTE tax, NYC UBT surrogate, and nonresident withholding under Tax Law §§601, 658 and Article 24-A (2021). |
| `us_state_oh_fund_tax` | Computes Ohio CAT exposure plus composite withholding for nonresident investors. |
| `us_state_ok_fund_tax` | Calculates Oklahoma top marginal tax, elective entity-level tax, and Form 512-S withholding obligations. |
| `us_state_or_fund_tax` | Addresses Oregon income tax, SALT election, and CAT overlay under Or. Rev. Stat. §§316.037 and 317A.100. |
| `us_state_pa_fund_tax` | Calculates Pennsylvania nonresident withholding and flat tax exposure per 72 P.S. §§7302 and 7335. |
| `us_state_ri_fund_tax` | Handles Rhode Island pass-through tax, corporate override, and composite withholding. |
| `us_state_sc_fund_tax` | Handles South Carolina nonresident withholding and elective entity-level tax calculations under S.C. Code §§12-6-510 and 12-6-590. |
| `us_state_sd_fund_tax` | Confirms South Dakota's income-tax-free status and highlights trust situs considerations. |
| `us_state_tn_fund_tax` | Calculates Tennessee excise/franchise equivalent for investment management entities. |
| `us_state_tx_fund_tax` | Computes Texas margin tax exposure for hedge fund operators. |
| `us_state_ut_fund_tax` | Evaluates Utah rate, PTE election, and Form TC-65 composite obligations. |
| `us_state_va_fund_tax` | Handles Virginia composite payments and SALT workaround calculations. |
| `us_state_vt_fund_tax` | Calculates Vermont income tax, SALT election effect, and estate exposure on fund interests. |
| `us_state_wa_fund_tax` | Computes Washington capital gains excise exposure for hedge fund allocations and approximates B&O impact. |
| `us_state_wi_fund_tax` | Calculates Wisconsin withholding and elective entity-level tax adjustments. |
| `us_state_wv_fund_tax` | Computes West Virginia income tax, severance overlays, and elective entity-level tax. |
| `us_state_wy_fund_tax` | Tracks Wyoming annual license tax exposure for holding entities. |
| `usage_heatmap_generator` | Buckets skill requests into hour/day heatmap bins for usage insights. |
| `usd_jpy_carry_trade_monitor` | Analyzes USD/JPY carry trade profitability using US vs Japan yield differentials and synthetic FX volatility. |
| `usdc_payment_verifier` | Validates Solana USDC transfers by comparing signature, amount, and wallets. |
| `value_at_risk` | Computes multi-level VaR and CVaR via historical simulation. |
| `value_at_risk_historical` | Computes historical VaR by sampling past returns and scaling by the desired horizon. |
| `value_at_risk_montecarlo` | Simulates returns via a Gaussian process to estimate VaR and expected shortfall. |
| `value_at_risk_parametric` | Computes Gaussian VaR and expected shortfall over a specified horizon. |
| `var_calculator` | Computes one-day VaR using historical percentile and parametric methods. |
| `variance_swap_fair_strike` | Applies the continuous variance swap replication integral approximated by discrete strikes (Carr & Madan 2001). |
| `variance_swap_pricer` | Applies the Carr-Madan replication integral to infer fair variance strikes and MTM P&L. |
| `velocity_tracker` | Summarizes velocity averages, trend, and predictability over past sprints. |
| `vendor_cost_comparator` | Computes daily/monthly spend per provider and ranks by cost-effectiveness. |
| `vendor_due_diligence` | Scores vendor fit based on uptime, pricing, certifications, and experience. |
| `vendor_risk_assessor` | Evaluates concentration risk, SPOFs, and diversification across vendors. |
| `vendor_sla_monitor` | Evaluates uptime and latency metrics vs SLA targets for each vendor. |
| `venture_capital_method` | Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method. |
| `venture_debt_amortization` | Generates a complete monthly payment schedule for a venture debt instrument with an interest-only (IO) period followed by a fully-amortizing repayment period. Optionally calculates the warrant coverage value granted to the lender as a percentage of principal. |
| `venture_return_analyzer` | Computes proceeds for preferred vs common across exit scenarios, including participation caps. |
| `verify_hurdle_rate` | Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation. |
| `vertex_ai_inference` | Call Vertex AI Gemini models for text generation, analysis, or embeddings. Uses Vertex AI REST API with explicit service account credentials — no gcloud, no ADC. Supports gemini-2.0-flash-exp (fastest), gemini-1.5-pro (most capable), gemini-1.5-flash. |
| `vintage_year_analyzer` | Benchmarks fund IRR/MOIC/DPI against vintage-year peer quartile data. Returns quartile placement (top/2nd/3rd/bottom) for each metric. |
| `vintage_year_benchmarking` | Benchmarks a private equity fund's performance against vintage-year peer data. Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, determines quartile rank (Q1=top), and produces a side-by-side comparison table for TVPI, DPI, and IRR. |
| `vix_term_structure_analyzer` | Analyzes VIX futures prices by expiry to identify contango/backwardation and roll yield. |
| `volatility_rank_percentile` | Calculates IV rank and percentile to understand volatility regimes. |
| `volatility_surface_analyzer` | Regresses implied volatility against strikes for each expiry to measure skew and term structure. |
| `volume_price_trend` | Calculates cumulative Volume Price Trend and compares against SMA to detect divergences. |
| `vote_tabulator` | Counts proposal votes and checks for mandates via 1-sigma upvote threshold. |
| `vwap_calculator` | Computes VWAP from typical price (H+L+C)/3 and derives 1/2 standard deviation bands. |
| `vwma_calculator` | Computes the volume-weighted moving average to compare price trends against standard SMA and confirm with volume. |
| `wallet_concentration_analyzer` | Analyzes wallet balance data to quantify concentration risk and whale dominance. |
| `wallets_check` | Checks on-chain balances versus Ghost Ledger and enforces $0.00 tolerance. |
| `wash_sale_cross_account` | Determines wash-sale disallowances when substantially identical securities are repurchased within ±30 days across related accounts. |
| `wash_sale_detector` | Flags loss sales with repurchases inside the 30-day wash window. |
| `wash_sale_rule_checker` | Checks transaction logs for wash sales inside 30-day windows. |
| `waterfall_sensitivity_analyzer` | Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split). Returns a sensitivity matrix and identifies optimal scenarios. |
| `watering_hole_order_router` | Quotes Watering Hole skill requests via the bonding curve, assigns the correct skill, and returns billing plus dispatch telemetry. |
| `weather_derivative_pricer` | Converts historical temperatures into HDD/CDD indices, computes expected payout, and delivers burn analysis statistics. |
| `weather_lookup` | Fetch current weather, multi-day forecasts, or historical weather data for any location using the Google Weather API. Returns structured weather metrics plus a commodity_signal field flagging weather-driven market implications for agricultural futures and supply chain analysis. |
| `web_of_trust_manager` | Records vouches between agents and exposes trust graph stats. |
| `webhook_receiver` | Verifies webhook signatures and normalizes payloads. |
| `websocket_market_ingest` | Build WebSocket connection and parser configurations for real-time market data ingestion from Kraken or Binance. |
| `weekly_pnl_report` | Aggregates revenue and expense items into a weekly P&L rollup. |
| `whale_concentration_index` | Evaluates distribution of balances to understand whale dominance and decentralization risk. |
| `what_if_engine` | Applies scenario overrides to a base business case and projects outcomes. |
| `white_label_config_generator` | Produces config YAML structure for franchise operators with branding hooks. |
| `williams_percent_r` | Calculates Larry Williams' %R oscillator comparing close versus the highest/lowest range. |
| `withholding_obligation_tracker` | Compute gross vs. net distributions and withholding requirements per LP. |
| `withholding_tax_reclaim_tracker` | Summarizes reclaimable withholding tax amounts and filing deadlines per country. |
| `workers_comp_experience_modifier` | Calculates WC experience modifier from actual and expected losses. |
| `workflow_engine` | Evaluates workflow dependencies and surfaces next executable steps. |
| `working_capital_analyzer` | Computes days sales outstanding, inventory days, days payable outstanding, cash conversion cycle, and highlights improvement opportunities. |
| `wrong_way_risk_estimator` | Applies a correlation-driven multiplier to CVA following Basel/WP80 guidance on wrong-way risk. |
| `x_sentiment_grok` | Constructs xAI Grok payloads for sentiment queries. |
| `xp_calculator` | Tallies XP from recent activities and estimates level progression. |
| `xva_desk_calculator` | Computes the suite of valuation adjustments using exposure profiles and hazard rate approximations. |
| `yield_curve_analyzer` | Builds spot discounts and forward rates to classify curve shape. |
| `yield_curve_bootstrapper` | Bootstraps spot and forward curves from par coupon instruments consistent with U.S. Treasury STRIPS methodology. |
| `yield_farming_apy_calculator` | Translates per-block reward rates into APR and APY estimates for yield farmers. |
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

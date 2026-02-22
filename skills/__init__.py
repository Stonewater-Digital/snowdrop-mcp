"""
Executive Summary: Snowdrop skill package — central registry for all 105 MCP-compatible skills.

Table of Contents:
- SKILL_REGISTRY: Master dict mapping skill names to module paths.
- get_skill: Utility to dynamically import and return a skill callable.
"""
from typing import Any
import importlib

SKILL_REGISTRY: dict[str, str] = {
    # Core Infrastructure (5)
    "audit_kraken": "skills.audit_kraken",
    "ghost_ledger": "skills.ghost_ledger",
    "reconcile": "skills.reconcile",
    "skill_builder": "skills.skill_builder",
    "thunder_signal": "skills.thunder_signal",
    # Fund Accounting (20)
    "calc_waterfall_dist": "skills.fund_accounting.calc_waterfall_dist",
    "verify_hurdle_rate": "skills.fund_accounting.verify_hurdle_rate",
    "generate_k1_schema": "skills.fund_accounting.generate_k1_schema",
    "nav_reconciliation": "skills.fund_accounting.nav_reconciliation",
    "cap_table_simulator": "skills.fund_accounting.cap_table_simulator",
    "clawback_analyzer": "skills.fund_accounting.clawback_analyzer",
    "drawdown_scheduler": "skills.fund_accounting.drawdown_scheduler",
    "carried_interest_tracker": "skills.fund_accounting.carried_interest_tracker",
    "pe_valuation_dcf": "skills.fund_accounting.pe_valuation_dcf",
    "ebitda_normalization": "skills.fund_accounting.ebitda_normalization",
    "debt_covenant_monitor": "skills.fund_accounting.debt_covenant_monitor",
    "subscription_doc_parser": "skills.fund_accounting.subscription_doc_parser",
    "fund_expense_allocator": "skills.fund_accounting.fund_expense_allocator",
    "vintage_year_benchmarking": "skills.fund_accounting.vintage_year_benchmarking",
    "co_investment_ledger": "skills.fund_accounting.co_investment_ledger",
    "exit_multiple_analysis": "skills.fund_accounting.exit_multiple_analysis",
    "bridge_loan_pricing": "skills.fund_accounting.bridge_loan_pricing",
    "management_fee_offset": "skills.fund_accounting.management_fee_offset",
    "dry_powder_calculator": "skills.fund_accounting.dry_powder_calculator",
    "lp_reporting_standard": "skills.fund_accounting.lp_reporting_standard",
    # Real Estate & REITs (15)
    "reit_ffo_calculator": "skills.real_estate.reit_ffo_calculator",
    "noi_audit_tool": "skills.real_estate.noi_audit_tool",
    "cre_debt_stack_modeling": "skills.real_estate.cre_debt_stack_modeling",
    "argus_to_json_transformer": "skills.real_estate.argus_to_json_transformer",
    "zoning_impact_analyzer": "skills.real_estate.zoning_impact_analyzer",
    "triple_net_reconciliation": "skills.real_estate.triple_net_reconciliation",
    "reit_dividend_coverage": "skills.real_estate.reit_dividend_coverage",
    "occupancy_rate_forecaster": "skills.real_estate.occupancy_rate_forecaster",
    "cre_cap_rate_aggregator": "skills.real_estate.cre_cap_rate_aggregator",
    "real_estate_tax_escrow": "skills.real_estate.real_estate_tax_escrow",
    "construction_draw_validator": "skills.real_estate.construction_draw_validator",
    "lease_abstract_skill": "skills.real_estate.lease_abstract_skill",
    "opportunity_zone_audit": "skills.real_estate.opportunity_zone_audit",
    "reit_nav_premium_tracker": "skills.real_estate.reit_nav_premium_tracker",
    "green_building_subsidy_audit": "skills.real_estate.green_building_subsidy_audit",
    # Compliance & Regulation (15)
    "mica_asset_classification": "skills.compliance.mica_asset_classification",
    "sebi_fpi_validator": "skills.compliance.sebi_fpi_validator",
    "fsa_japan_crypto_audit": "skills.compliance.fsa_japan_crypto_audit",
    "sec_form_pf_compiler": "skills.compliance.sec_form_pf_compiler",
    "gdpr_fin_data_scrub": "skills.compliance.gdpr_fin_data_scrub",
    "kyc_aml_chain_analysis": "skills.compliance.kyc_aml_chain_analysis",
    "reg_bi_compliance_logic": "skills.compliance.reg_bi_compliance_logic",
    "brexit_passporting_check": "skills.compliance.brexit_passporting_check",
    "india_gst_tax_calculator": "skills.compliance.india_gst_tax_calculator",
    "brazil_pix_settlement_logic": "skills.compliance.brazil_pix_settlement_logic",
    "australia_asics_checker": "skills.compliance.australia_asics_checker",
    "france_amf_whitepaper_audit": "skills.compliance.france_amf_whitepaper_audit",
    "ireland_ica_reporting": "skills.compliance.ireland_ica_reporting",
    "fincen_boir_generator": "skills.compliance.fincen_boir_generator",
    "esg_sfdr_categorization": "skills.compliance.esg_sfdr_categorization",
    # Sovereign Wealth & Macro (10)
    "sovereign_reserves_analyzer": "skills.sovereign.sovereign_reserves_analyzer",
    "central_bank_ledger_sync": "skills.sovereign.central_bank_ledger_sync",
    "fiat_to_crypto_onramp_audit": "skills.sovereign.fiat_to_crypto_onramp_audit",
    "inflation_hedging_simulator": "skills.sovereign.inflation_hedging_simulator",
    "trade_settlement_lc_logic": "skills.sovereign.trade_settlement_lc_logic",
    "sovereign_debt_yield_curve": "skills.sovereign.sovereign_debt_yield_curve",
    "imf_sdr_allocation_tracker": "skills.sovereign.imf_sdr_allocation_tracker",
    "energy_to_currency_peg_logic": "skills.sovereign.energy_to_currency_peg_logic",
    "remittance_cost_optimizer": "skills.sovereign.remittance_cost_optimizer",
    "sovereign_wealth_alpha_source": "skills.sovereign.sovereign_wealth_alpha_source",
    # Agent Social & Crowd Intel (10)
    "moltbook_sentiment_analyzer": "skills.social.moltbook_sentiment_analyzer",
    "agent_trust_score_calc": "skills.social.agent_trust_score_calc",
    "collaborative_liquidity_hunt": "skills.social.collaborative_liquidity_hunt",
    "moltbook_reputation_builder": "skills.social.moltbook_reputation_builder",
    "agent_to_agent_negotiation": "skills.social.agent_to_agent_negotiation",
    "crowd_sourced_risk_audit": "skills.social.crowd_sourced_risk_audit",
    "multi_book_influence_tracker": "skills.social.multi_book_influence_tracker",
    "agentic_syndication_logic": "skills.social.agentic_syndication_logic",
    "prompt_injection_shield": "skills.social.prompt_injection_shield",
    "moltbook_engagement_loop": "skills.social.moltbook_engagement_loop",
    # Technical & Multi-Chain (30)
    "ton_w5_gasless_transfer": "skills.technical.ton_w5_gasless_transfer",
    "solana_jit_execution": "skills.technical.solana_jit_execution",
    "cross_chain_accounting_bridge": "skills.technical.cross_chain_accounting_bridge",
    "private_key_shard_manager": "skills.technical.private_key_shard_manager",
    "ledger_immutability_checker": "skills.technical.ledger_immutability_checker",
    "fastapi_to_mcp_wrapper": "skills.technical.fastapi_to_mcp_wrapper",
    "websocket_market_ingest": "skills.technical.websocket_market_ingest",
    "error_retry_exponential_backoff": "skills.technical.error_retry_exponential_backoff",
    "agent_heartbeat_monitor": "skills.technical.agent_heartbeat_monitor",
    "cost_basis_averaging_logic": "skills.technical.cost_basis_averaging_logic",
    "audit_trail_immutable_export": "skills.technical.audit_trail_immutable_export",
    "json_to_xbrl_transformer": "skills.technical.json_to_xbrl_transformer",
    "smart_contract_vulnerability_scan": "skills.technical.smart_contract_vulnerability_scan",
    "slippage_protection_buffer": "skills.technical.slippage_protection_buffer",
    "portfolio_variance_calc": "skills.technical.portfolio_variance_calc",
    "agent_skill_version_checker": "skills.technical.agent_skill_version_checker",
    "latency_optimized_order_routing": "skills.technical.latency_optimized_order_routing",
    "api_key_rotation_logic": "skills.technical.api_key_rotation_logic",
    "hardware_wallet_handshake": "skills.technical.hardware_wallet_handshake",
    "financial_entity_graph": "skills.technical.financial_entity_graph",
    "global_tax_withholding_skill": "skills.technical.global_tax_withholding_skill",
    "reit_dividend_reinvestment_logic": "skills.technical.reit_dividend_reinvestment_logic",
    "venture_debt_amortization": "skills.technical.venture_debt_amortization",
    "sovereign_fiat_bridge": "skills.technical.sovereign_fiat_bridge",
    "agentic_white_label_portal": "skills.technical.agentic_white_label_portal",
    "mcp_discovery_beacon": "skills.technical.mcp_discovery_beacon",
    "transaction_sim_pre_flight": "skills.technical.transaction_sim_pre_flight",
    "portfolio_stress_test": "skills.technical.portfolio_stress_test",
    "agent_collaboration_handshake": "skills.technical.agent_collaboration_handshake",
    "thunder_executive_briefing": "skills.technical.thunder_executive_briefing",
}


def get_skill(name: str) -> tuple[callable, dict]:
    """Dynamically import a skill and return its callable + TOOL_META.

    Args:
        name: The skill name (must be a key in SKILL_REGISTRY).

    Returns:
        Tuple of (skill_function, TOOL_META dict).

    Raises:
        KeyError: If skill name not found in registry.
        ImportError: If module cannot be imported.
        AttributeError: If module lacks expected attributes.
    """
    if name not in SKILL_REGISTRY:
        raise KeyError(f"Skill '{name}' not found in SKILL_REGISTRY. Available: {len(SKILL_REGISTRY)} skills.")
    module_path = SKILL_REGISTRY[name]
    module = importlib.import_module(module_path)
    fn = getattr(module, name)
    meta = getattr(module, "TOOL_META")
    return fn, meta


def list_skills() -> list[str]:
    """Return sorted list of all registered skill names."""
    return sorted(SKILL_REGISTRY.keys())

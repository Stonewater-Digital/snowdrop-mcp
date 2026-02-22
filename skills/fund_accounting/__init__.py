"""
Executive Summary: Fund accounting skill package exposing 10 MCP-compatible financial tools for PE/VC fund operations.

Table of Contents:
1. calc_waterfall_dist      — LP/GP waterfall distributions
2. verify_hurdle_rate       — Preferred return hurdle validation
3. generate_k1_schema       — IRS Schedule K-1 JSON schema generation
4. nav_reconciliation       — NAV per share calculation and reconciliation
5. cap_table_simulator      — Equity dilution modeling across funding rounds
6. clawback_analyzer        — GP clawback obligation analysis
7. drawdown_scheduler       — Capital call scheduling against unfunded commitment
8. carried_interest_tracker — Cumulative GP carry tracking
9. pe_valuation_dcf         — DCF enterprise valuation
10. ebitda_normalization     — EBITDA add-back normalization for M&A due diligence
"""
from .calc_waterfall_dist import calc_waterfall_dist, TOOL_META as WATERFALL_META
from .verify_hurdle_rate import verify_hurdle_rate, TOOL_META as HURDLE_META
from .generate_k1_schema import generate_k1_schema, TOOL_META as K1_META
from .nav_reconciliation import nav_reconciliation, TOOL_META as NAV_META
from .cap_table_simulator import cap_table_simulator, TOOL_META as CAPTABLE_META
from .clawback_analyzer import clawback_analyzer, TOOL_META as CLAWBACK_META
from .drawdown_scheduler import drawdown_scheduler, TOOL_META as DRAWDOWN_META
from .carried_interest_tracker import carried_interest_tracker, TOOL_META as CARRY_META
from .pe_valuation_dcf import pe_valuation_dcf, TOOL_META as DCF_META
from .ebitda_normalization import ebitda_normalization, TOOL_META as EBITDA_META

__all__ = [
    # Skill functions
    "calc_waterfall_dist",
    "verify_hurdle_rate",
    "generate_k1_schema",
    "nav_reconciliation",
    "cap_table_simulator",
    "clawback_analyzer",
    "drawdown_scheduler",
    "carried_interest_tracker",
    "pe_valuation_dcf",
    "ebitda_normalization",
    # TOOL_META dicts (for MCP server registration)
    "WATERFALL_META",
    "HURDLE_META",
    "K1_META",
    "NAV_META",
    "CAPTABLE_META",
    "CLAWBACK_META",
    "DRAWDOWN_META",
    "CARRY_META",
    "DCF_META",
    "EBITDA_META",
    # Aggregate list for MCP tools/list registration
    "ALL_TOOLS",
]

ALL_TOOLS: list[dict] = [
    WATERFALL_META,
    HURDLE_META,
    K1_META,
    NAV_META,
    CAPTABLE_META,
    CLAWBACK_META,
    DRAWDOWN_META,
    CARRY_META,
    DCF_META,
    EBITDA_META,
]

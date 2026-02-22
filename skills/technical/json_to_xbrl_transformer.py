"""
Executive Summary: Transform JSON financial data into SEC-compatible XBRL-JSON format using the us-gaap taxonomy namespace.
Inputs: financial_data (dict: entity_name, cik, period, facts)
Outputs: xbrl_json (dict), concepts_mapped (int), unmapped_fields (list), taxonomy_version (str)
MCP Tool Name: json_to_xbrl_transformer
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "json_to_xbrl_transformer",
    "description": "Transform JSON financial facts into SEC XBRL-JSON format using the us-gaap taxonomy. Maps concept names to us-gaap namespace and generates inline XBRL-compatible output.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "financial_data": {
                "type": "object",
                "description": "Financial data dict with: entity_name (str), cik (str), period (str, e.g. '2025-12-31'), facts (dict mapping concept name → numeric value).",
                "properties": {
                    "entity_name": {"type": "string"},
                    "cik": {"type": "string"},
                    "period": {"type": "string"},
                    "facts": {"type": "object"}
                },
                "required": ["entity_name", "cik", "period", "facts"]
            }
        },
        "required": ["financial_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "xbrl_json": {"type": "object"},
            "concepts_mapped": {"type": "integer"},
            "unmapped_fields": {"type": "array"},
            "taxonomy_version": {"type": "string"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["xbrl_json", "concepts_mapped", "unmapped_fields", "taxonomy_version", "status", "timestamp"]
    }
}

# XBRL taxonomy version
_TAXONOMY_VERSION = "us-gaap-2024"

# Mapping of common plain-English financial concept names to us-gaap XBRL element names
# Source: SEC EDGAR us-gaap taxonomy (2024 release)
_CONCEPT_MAP: dict[str, str] = {
    # Income Statement
    "Revenue": "us-gaap:Revenues",
    "Revenues": "us-gaap:Revenues",
    "NetRevenue": "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
    "GrossProfit": "us-gaap:GrossProfit",
    "OperatingIncome": "us-gaap:OperatingIncomeLoss",
    "OperatingExpenses": "us-gaap:OperatingExpenses",
    "EBITDA": "us-gaap:EarningsBeforeInterestTaxesDepreciationAndAmortization",
    "NetIncome": "us-gaap:NetIncomeLoss",
    "NetLoss": "us-gaap:NetIncomeLoss",
    "EPS": "us-gaap:EarningsPerShareBasic",
    "EPSBasic": "us-gaap:EarningsPerShareBasic",
    "EPSDiluted": "us-gaap:EarningsPerShareDiluted",
    "CostOfRevenue": "us-gaap:CostOfRevenue",
    "CostOfGoodsSold": "us-gaap:CostOfGoodsSold",
    "ResearchAndDevelopment": "us-gaap:ResearchAndDevelopmentExpense",
    "SalesGeneralAdministrative": "us-gaap:SellingGeneralAndAdministrativeExpense",
    "DepreciationAmortization": "us-gaap:DepreciationDepletionAndAmortization",
    "InterestExpense": "us-gaap:InterestExpense",
    "IncomeTaxExpense": "us-gaap:IncomeTaxExpenseBenefit",
    # Balance Sheet — Assets
    "TotalAssets": "us-gaap:Assets",
    "CurrentAssets": "us-gaap:AssetsCurrent",
    "CashAndEquivalents": "us-gaap:CashAndCashEquivalentsAtCarryingValue",
    "ShortTermInvestments": "us-gaap:ShortTermInvestments",
    "AccountsReceivable": "us-gaap:AccountsReceivableNetCurrent",
    "Inventory": "us-gaap:InventoryNet",
    "PrepaidExpenses": "us-gaap:PrepaidExpenseAndOtherAssetsCurrent",
    "NonCurrentAssets": "us-gaap:AssetsNoncurrent",
    "PropertyPlantEquipment": "us-gaap:PropertyPlantAndEquipmentNet",
    "Goodwill": "us-gaap:Goodwill",
    "IntangibleAssets": "us-gaap:IntangibleAssetsNetExcludingGoodwill",
    # Balance Sheet — Liabilities
    "TotalLiabilities": "us-gaap:Liabilities",
    "CurrentLiabilities": "us-gaap:LiabilitiesCurrent",
    "AccountsPayable": "us-gaap:AccountsPayableCurrent",
    "AccruedLiabilities": "us-gaap:AccruedLiabilitiesCurrent",
    "DeferredRevenue": "us-gaap:DeferredRevenueCurrent",
    "ShortTermDebt": "us-gaap:ShortTermBorrowings",
    "LongTermDebt": "us-gaap:LongTermDebt",
    "NonCurrentLiabilities": "us-gaap:LiabilitiesNoncurrent",
    # Balance Sheet — Equity
    "TotalEquity": "us-gaap:StockholdersEquity",
    "RetainedEarnings": "us-gaap:RetainedEarningsAccumulatedDeficit",
    "CommonStock": "us-gaap:CommonStockValue",
    "AdditionalPaidInCapital": "us-gaap:AdditionalPaidInCapital",
    "TreasuryStock": "us-gaap:TreasuryStockValue",
    # Cash Flow Statement
    "OperatingCashFlow": "us-gaap:NetCashProvidedByUsedInOperatingActivities",
    "InvestingCashFlow": "us-gaap:NetCashProvidedByUsedInInvestingActivities",
    "FinancingCashFlow": "us-gaap:NetCashProvidedByUsedInFinancingActivities",
    "CapitalExpenditures": "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
    "FreeCashFlow": "us-gaap:FreeCashFlow",
    # Shares
    "SharesOutstanding": "us-gaap:CommonStockSharesOutstanding",
    "SharesIssued": "us-gaap:CommonStockSharesIssued",
    "WeightedAvgShares": "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
    "WeightedAvgSharesDiluted": "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
}

# Unit mappings for common concept categories
_UNIT_MAP: dict[str, dict] = {
    "monetary": {"unit": "USD", "decimals": -3},
    "shares": {"unit": "shares", "decimals": 0},
    "per_share": {"unit": "USD/shares", "decimals": 2},
    "ratio": {"unit": "pure", "decimals": 4},
}

# Concepts that represent per-share values
_PER_SHARE_CONCEPTS = {
    "us-gaap:EarningsPerShareBasic",
    "us-gaap:EarningsPerShareDiluted",
}

# Concepts that represent share counts
_SHARE_CONCEPTS = {
    "us-gaap:CommonStockSharesOutstanding",
    "us-gaap:CommonStockSharesIssued",
    "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
    "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
}


def _classify_unit(concept_xbrl: str) -> dict:
    """Classify the unit type for a mapped XBRL concept.

    Args:
        concept_xbrl: The us-gaap XBRL concept name.

    Returns:
        Unit dict with 'unit' and 'decimals' keys.
    """
    if concept_xbrl in _PER_SHARE_CONCEPTS:
        return _UNIT_MAP["per_share"]
    if concept_xbrl in _SHARE_CONCEPTS:
        return _UNIT_MAP["shares"]
    return _UNIT_MAP["monetary"]


def _normalize_cik(cik: str) -> str:
    """Normalize a CIK to SEC's zero-padded 10-digit format.

    Args:
        cik: Raw CIK string (may be numeric or already padded).

    Returns:
        Zero-padded 10-digit CIK string.
    """
    digits = "".join(c for c in str(cik) if c.isdigit())
    return digits.zfill(10)


def json_to_xbrl_transformer(financial_data: dict) -> dict:
    """Transform JSON financial facts into SEC XBRL-JSON format.

    Maps plain-English concept names to us-gaap taxonomy element names and
    builds an XBRL-JSON structure compatible with the SEC's inline XBRL
    (iXBRL) and XBRL API endpoints. Unmapped concepts are returned separately.

    Args:
        financial_data: Dict with keys:
            - entity_name (str): Legal entity name.
            - cik (str): SEC Central Index Key.
            - period (str): Reporting period end date (YYYY-MM-DD).
            - facts (dict): Mapping of concept name (str) to numeric value.

    Returns:
        A dict with keys:
            - xbrl_json (dict): SEC XBRL-JSON format output.
            - concepts_mapped (int): Number of facts successfully mapped to us-gaap.
            - unmapped_fields (list): Concept names that had no mapping.
            - taxonomy_version (str): XBRL taxonomy version used.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        required = {"entity_name", "cik", "period", "facts"}
        missing = required - set(financial_data.keys())
        if missing:
            raise ValueError(f"financial_data missing required keys: {missing}.")

        entity_name = str(financial_data["entity_name"]).strip()
        cik_raw = str(financial_data["cik"]).strip()
        period = str(financial_data["period"]).strip()
        facts = financial_data["facts"]

        if not entity_name:
            raise ValueError("entity_name cannot be empty.")
        if not facts or not isinstance(facts, dict):
            raise ValueError("facts must be a non-empty dict.")

        # Validate period format (loose check)
        try:
            period_dt = datetime.strptime(period[:10], "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"period must be in YYYY-MM-DD format, got '{period}'.")

        cik_normalized = _normalize_cik(cik_raw)

        # Build XBRL-JSON facts
        xbrl_facts: dict[str, Any] = {}
        unmapped_fields: list[str] = []
        concepts_mapped = 0

        for concept_name, value in facts.items():
            xbrl_concept = _CONCEPT_MAP.get(concept_name)
            if xbrl_concept is None:
                unmapped_fields.append(concept_name)
                continue

            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                unmapped_fields.append(concept_name)
                logger.warning(f"json_to_xbrl_transformer: non-numeric value for '{concept_name}': {value}")
                continue

            unit_info = _classify_unit(xbrl_concept)
            namespace, local_name = xbrl_concept.split(":")

            if xbrl_concept not in xbrl_facts:
                xbrl_facts[xbrl_concept] = {
                    "label": local_name,
                    "description": f"SEC us-gaap concept: {local_name}",
                    "units": {unit_info["unit"]: []},
                }

            # Add the fact value with period context
            fact_entry = {
                "end": period,
                "val": numeric_value,
                "accn": f"0001{cik_normalized}-{period_dt.strftime('%y')}-000001",
                "fy": period_dt.year,
                "fp": "FY",
                "form": "10-K",
                "filed": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "frame": f"CY{period_dt.year}",
            }

            xbrl_facts[xbrl_concept]["units"][unit_info["unit"]].append(fact_entry)
            concepts_mapped += 1

        # Build top-level XBRL-JSON structure (SEC EDGAR companyfacts format)
        xbrl_json = {
            "cik": int(cik_normalized),
            "entityName": entity_name,
            "facts": {
                "us-gaap": xbrl_facts,
            },
            "taxonomy": {
                "namespace": "http://fasb.org/us-gaap/2024",
                "version": _TAXONOMY_VERSION,
                "prefix": "us-gaap",
            },
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "generator": "Snowdrop json_to_xbrl_transformer v1.0",
                "concepts_mapped": concepts_mapped,
                "concepts_total": len(facts),
                "unmapped_count": len(unmapped_fields),
                "period": period,
                "format": "XBRL-JSON (SEC EDGAR companyfacts)",
            },
        }

        return {
            "status": "success",
            "xbrl_json": xbrl_json,
            "concepts_mapped": concepts_mapped,
            "unmapped_fields": unmapped_fields,
            "taxonomy_version": _TAXONOMY_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"json_to_xbrl_transformer failed: {e}")
        _log_lesson(f"json_to_xbrl_transformer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "xbrl_json": {},
            "concepts_mapped": 0,
            "unmapped_fields": [],
            "taxonomy_version": _TAXONOMY_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")

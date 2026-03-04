"""Educational guide to fiscal policy fundamentals.

MCP Tool Name: fiscal_policy_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fiscal_policy_guide",
    "description": "Returns educational content on fiscal policy: taxation, government spending, deficits, and the multiplier effect.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def fiscal_policy_guide() -> dict[str, Any]:
    """Returns educational content on fiscal policy."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Fiscal policy refers to the government's use of taxation and spending to influence the economy. Unlike monetary policy (managed by the central bank), fiscal policy is determined by elected officials through legislation — Congress and the President in the U.S.",
                "key_concepts": [
                    "Fiscal policy directly affects aggregate demand through government spending and taxation",
                    "Expansionary fiscal policy increases spending or cuts taxes to stimulate growth",
                    "Contractionary fiscal policy decreases spending or raises taxes to cool overheating",
                    "Fiscal policy has political constraints that monetary policy does not",
                ],
                "taxation": {
                    "types": {
                        "income_tax": "Progressive tax on individual and corporate income. The largest source of federal revenue.",
                        "payroll_tax": "Social Security and Medicare taxes (FICA). Shared between employer and employee. Second largest revenue source.",
                        "capital_gains_tax": "Tax on profits from selling investments. Short-term (ordinary rates) vs long-term (preferential rates for assets held >1 year).",
                        "sales_tax": "State and local consumption tax. Regressive — takes a higher percentage of income from lower earners.",
                        "property_tax": "Tax on real estate value. Primary funding source for local governments and schools.",
                        "estate_tax": "Tax on the transfer of wealth at death. Applies above the exemption threshold.",
                    },
                    "stimulus_effect": "Tax cuts increase disposable income, encouraging consumer spending and business investment. The magnitude depends on who receives the cut (lower-income recipients tend to spend a higher proportion).",
                },
                "government_spending": {
                    "mandatory": "Spending required by law (Social Security, Medicare, Medicaid, interest on debt). ~65% of the federal budget. Grows automatically with eligible population.",
                    "discretionary": "Spending set through annual appropriations (defense, education, transportation, research). ~30% of the budget. Requires annual Congressional approval.",
                    "transfer_payments": "Payments to individuals without a corresponding exchange of goods/services (Social Security benefits, unemployment insurance, welfare). Redistribute income but do not directly purchase output.",
                    "direct_impact": "Government purchases of goods and services (infrastructure, military equipment, federal employee salaries) directly add to GDP.",
                },
                "deficit_and_debt": {
                    "budget_deficit": "When government spending exceeds revenue in a given year. Deficit = Spending - Revenue. Financed by issuing Treasury securities (borrowing).",
                    "budget_surplus": "When revenue exceeds spending. Surpluses can be used to pay down debt. The U.S. last had surpluses in 1998-2001.",
                    "national_debt": "The accumulated total of all past deficits minus surpluses. U.S. national debt exceeds $34 trillion.",
                    "debt_to_gdp": "The ratio of national debt to GDP. A key measure of fiscal sustainability. U.S. ratio is approximately 120%. Japan exceeds 250%.",
                    "crowding_out": "Theory that heavy government borrowing raises interest rates, making private borrowing more expensive and reducing private investment.",
                },
                "multiplier_effect": {
                    "definition": "The principle that a change in government spending or taxation produces a larger change in total economic output (GDP).",
                    "formula": "Spending Multiplier = 1 / (1 - MPC), where MPC = Marginal Propensity to Consume. If MPC = 0.8, multiplier = 5x.",
                    "spending_multiplier": "A $1 increase in government spending may increase GDP by $1.50-$2.00, as the money circulates through the economy. Higher during recessions, lower during expansions.",
                    "tax_multiplier": "A $1 tax cut increases GDP by less than a $1 spending increase, because some of the tax cut is saved rather than spent. Tax multiplier = -MPC / (1 - MPC).",
                    "leakages": "Saving, taxes, and imports reduce the multiplier effect. The actual multiplier is typically 1.0-2.0, not the theoretical maximum.",
                },
                "example": "During a recession, Congress passes a $500 billion stimulus package: $300B in direct spending (infrastructure, aid to states) and $200B in tax cuts. With a spending multiplier of 1.5 and a tax multiplier of 1.0, the estimated GDP impact is $300B * 1.5 + $200B * 1.0 = $650B.",
                "common_mistakes": [
                    "Assuming government spending is always stimulus (it depends on economic conditions and what is displaced)",
                    "Ignoring the time lag — fiscal policy takes months or years to design, pass, and implement",
                    "Confusing budget deficits with national debt (deficit is the annual flow, debt is the accumulated stock)",
                    "Applying the simplified multiplier formula without considering leakages and crowding out",
                    "Assuming fiscal and monetary policy always work in the same direction (they can conflict)",
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

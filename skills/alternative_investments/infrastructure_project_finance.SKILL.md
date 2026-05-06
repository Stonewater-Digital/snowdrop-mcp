---
skill: infrastructure_project_finance
category: alternative_investments
description: Constructs a single-asset project model to evaluate DSCR, LLCR, and equity IRR against capex and leverage assumptions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: capex, revenue_forecast, opex_forecast, debt_rate, debt_tenor_years, debt_ratio
---

# Infrastructure Project Finance

## Description
Constructs a single-asset project finance model to evaluate DSCR, loan life coverage ratio (LLCR), and equity IRR against capex and leverage assumptions. Supports renewable energy, toll roads, and other long-dated infrastructure assets. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `capex` | `number` | Yes | Total project capital expenditure (dollars). |
| `revenue_forecast` | `array` | Yes | Annual revenue projections for each operating year (dollars). |
| `opex_forecast` | `array` | Yes | Annual operating expense projections for each year (dollars). |
| `debt_rate` | `number` | Yes | Debt interest rate as a decimal (e.g. 0.05 for 5%). |
| `debt_tenor_years` | `integer` | Yes | Debt repayment tenor in years. |
| `debt_ratio` | `number` | Yes | Debt-to-total-capex ratio as a decimal (e.g. 0.70 for 70% leverage). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "infrastructure_project_finance",
  "arguments": {
    "capex": 200000000,
    "revenue_forecast": [18000000, 20000000, 22000000, 23000000, 24000000],
    "opex_forecast": [5000000, 5200000, 5400000, 5500000, 5600000],
    "debt_rate": 0.05,
    "debt_tenor_years": 15,
    "debt_ratio": 0.70
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "infrastructure_project_finance"`.

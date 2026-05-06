---
skill: carbon_credit_pricer
category: alternative_investments
description: Applies benchmark market prices with discounts for vintage and premiums for project quality to produce fair values. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: credit_type, vintage_year, project_type, market_prices, quality_score
---

# Carbon Credit Pricer

## Description
Applies benchmark market prices with discounts for vintage age and premiums for project quality to produce fair values for voluntary and compliance carbon credits. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `credit_type` | `string` | Yes | Credit type: "voluntary" or "compliance". |
| `vintage_year` | `integer` | Yes | Year the carbon reductions were generated (e.g. 2022). |
| `project_type` | `string` | Yes | Project category (e.g. "reforestation", "renewable_energy", "methane_capture"). |
| `market_prices` | `array` | Yes | List of recent benchmark market prices per tonne (dollars). |
| `quality_score` | `number` | Yes | Project quality score 0–100 based on certification and additionality. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "carbon_credit_pricer",
  "arguments": {
    "credit_type": "voluntary",
    "vintage_year": 2022,
    "project_type": "reforestation",
    "market_prices": [12.5, 14.0, 11.8, 13.2],
    "quality_score": 78.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carbon_credit_pricer"`.

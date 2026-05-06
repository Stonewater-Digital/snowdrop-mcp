---
skill: timber_valuation
category: alternative_investments
description: Applies Faustmann formula to timber growth and stumpage pricing to compute NPV and optimal rotation age. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: standing_volume, species_mix_factor, growth_rate, stumpage_price, discount_rate, harvest_cycle_years
---

# Timber Valuation

## Description
Applies the Faustmann formula to timber growth dynamics and current stumpage pricing to compute NPV per acre and optimal harvest rotation age. Used for timberland REIT valuation and institutional forestry investments. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `standing_volume` | `number` | Yes | Current standing timber volume (board feet or cubic meters per acre). |
| `species_mix_factor` | `number` | Yes | Blended species quality multiplier 0–2 (1.0 = average, higher = higher-value species mix). |
| `growth_rate` | `number` | Yes | Annual timber volume growth rate as a decimal (e.g. 0.04 for 4%). |
| `stumpage_price` | `number` | Yes | Current stumpage price per unit volume (dollars per board foot or MBF). |
| `discount_rate` | `number` | Yes | Discount rate for NPV calculation as a decimal (e.g. 0.06 for 6%). |
| `harvest_cycle_years` | `integer` | Yes | Planned harvest rotation cycle in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "timber_valuation",
  "arguments": {
    "standing_volume": 8000,
    "species_mix_factor": 1.2,
    "growth_rate": 0.035,
    "stumpage_price": 0.45,
    "discount_rate": 0.06,
    "harvest_cycle_years": 30
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "timber_valuation"`.

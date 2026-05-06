---
skill: farmland_valuation
category: alternative_investments
description: Capitalizes normalized NOI per acre and blends with comparable sale metrics to determine farmland value. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: acres, soil_quality_score, crop_yield_history, cap_rate, comparable_sales
---

# Farmland Valuation

## Description
Capitalizes normalized net operating income per acre using soil quality and historical crop yield, then blends with comparable land sale metrics to determine farmland fair value. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `acres` | `number` | Yes | Total farmland acreage being valued. |
| `soil_quality_score` | `number` | Yes | Soil productivity index 0–100 (NRCS/USDA scale). |
| `crop_yield_history` | `array` | Yes | Historical annual crop yields (bushels per acre or equivalent). |
| `cap_rate` | `number` | Yes | Capitalization rate as a decimal (e.g. 0.04 for 4%). |
| `comparable_sales` | `array` | Yes | List of comparable farmland sale prices per acre (dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "farmland_valuation",
  "arguments": {
    "acres": 500,
    "soil_quality_score": 72.0,
    "crop_yield_history": [185, 192, 178, 201, 196],
    "cap_rate": 0.04,
    "comparable_sales": [8500, 9200, 8800, 7900]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "farmland_valuation"`.

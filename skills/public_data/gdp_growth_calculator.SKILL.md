---
skill: gdp_growth_calculator
category: public_data
description: Calculate GDP growth rate between two periods. Returns percentage growth and context on real vs nominal GDP.
tier: free
inputs: gdp_current, gdp_previous
---

# Gdp Growth Calculator

## Description
Calculate GDP growth rate between two periods. Returns percentage growth and context on real vs nominal GDP.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gdp_current` | `number` | Yes | Current period GDP value (in any consistent unit). |
| `gdp_previous` | `number` | Yes | Previous period GDP value (in same unit as current). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gdp_growth_calculator",
  "arguments": {
    "gdp_current": 0,
    "gdp_previous": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gdp_growth_calculator"`.

---
skill: rental_rate_growth_calculator
category: reits
description: Calculates cash and GAAP leasing spreads versus expiring rents.
tier: free
inputs: expiring_rent_psf, new_rent_psf, market_rent_psf
---

# Rental Rate Growth Calculator

## Description
Calculates cash and GAAP leasing spreads versus expiring rents.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expiring_rent_psf` | `number` | Yes |  |
| `new_rent_psf` | `number` | Yes |  |
| `market_rent_psf` | `number` | Yes |  |
| `retained_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rental_rate_growth_calculator",
  "arguments": {
    "expiring_rent_psf": 0,
    "new_rent_psf": 0,
    "market_rent_psf": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rental_rate_growth_calculator"`.

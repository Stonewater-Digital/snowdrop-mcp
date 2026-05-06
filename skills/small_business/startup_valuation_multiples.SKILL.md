---
skill: startup_valuation_multiples
category: small_business
description: Applies growth-adjusted revenue multiples and sector EBITDA comparables to produce valuation ranges and comparable context notes.
tier: free
inputs: annual_revenue, ebitda, growth_rate, industry_sector, stage
---

# Startup Valuation Multiples

## Description
Applies growth-adjusted revenue multiples and sector EBITDA comparables to produce valuation ranges and comparable context notes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_revenue` | `number` | Yes | Latest annualized revenue run rate. |
| `ebitda` | `number` | Yes | Trailing twelve months EBITDA (can be negative). |
| `growth_rate` | `number` | Yes | Year-over-year revenue growth as decimal. |
| `industry_sector` | `string` | Yes | Sector label (saas, fintech, marketplace, consumer, hardware). |
| `stage` | `string` | Yes | seed, series_a, series_b, or growth. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "startup_valuation_multiples",
  "arguments": {
    "annual_revenue": 0,
    "ebitda": 0,
    "growth_rate": 0,
    "industry_sector": "<industry_sector>",
    "stage": "<stage>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "startup_valuation_multiples"`.

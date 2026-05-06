---
skill: vintage_year_analyzer
category: fund_accounting
description: Compares funds across vintages and computes quartiles/PME proxies. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: funds
---

# Vintage Year Analyzer

## Description
Compares funds across vintages and computes quartiles/PME proxies. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `funds` | `array` | Yes | List of fund performance objects, each with `name`, `vintage_year`, `net_irr`, `tvpi` (total value to paid-in), `dpi` (distributions to paid-in), and optionally `strategy` and `size`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vintage_year_analyzer",
  "arguments": {
    "funds": [
      {"name": "Snowdrop PE Fund I", "vintage_year": 2018, "net_irr": 0.21, "tvpi": 1.85, "dpi": 0.60, "strategy": "buyout", "size": 75000000},
      {"name": "Snowdrop PE Fund II", "vintage_year": 2021, "net_irr": 0.18, "tvpi": 1.42, "dpi": 0.18, "strategy": "growth", "size": 150000000},
      {"name": "Peer VC Fund 2018", "vintage_year": 2018, "net_irr": 0.16, "tvpi": 1.70, "dpi": 0.40, "strategy": "venture", "size": 50000000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vintage_year_analyzer"`.

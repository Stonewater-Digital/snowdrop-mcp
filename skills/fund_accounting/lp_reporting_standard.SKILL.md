---
skill: lp_reporting_standard
category: fund_accounting
description: Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null.
tier: premium
inputs: fund_data, quarter, year
---

# Lp Reporting Standard

## Description
Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null. Produces structured markdown with sections for Fund Overview, Performance Metrics, Top Holdings, Cash Position, and Upcoming Events. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_data` | `object` | Yes | ILPA v2 compliant fund data object with fields for fund overview, performance metrics, holdings, cash positions, and upcoming events. |
| `quarter` | `string` | Yes | Reporting quarter (e.g. `"Q4"`). |
| `year` | `number` | Yes | Reporting year (e.g. `2025`). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lp_reporting_standard",
  "arguments": {
    "fund_data": {
      "fund_name": "Snowdrop Growth Equity Fund II",
      "vintage_year": 2021,
      "total_commitments": 150000000,
      "nav": 138000000,
      "irr_net": 0.187,
      "tvpi": 1.42,
      "dpi": 0.18,
      "top_holdings": [{"company": "PortCo Alpha", "sector": "SaaS", "nav": 22000000}],
      "cash_position": 4500000,
      "upcoming_events": [{"event": "Capital call", "date": "2026-07-01", "amount": 8000000}]
    },
    "quarter": "Q1",
    "year": 2026
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lp_reporting_standard"`.

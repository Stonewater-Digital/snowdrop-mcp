---
skill: exit_multiple_analysis
category: fund_accounting
description: Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.).
tier: premium
inputs: exits
---

# Exit Multiple Analysis

## Description
Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.). Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exits` | `array` | Yes | List of realized exit objects, each with `company`, `sector`, `exit_type` (e.g. `"M&A"`, `"IPO"`, `"secondary"`, `"write-off"`), `cost_basis`, and `proceeds`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "exit_multiple_analysis",
  "arguments": {
    "exits": [
      {"company": "Acme Corp", "sector": "SaaS", "exit_type": "M&A", "cost_basis": 5000000, "proceeds": 18000000},
      {"company": "Beta Health", "sector": "Healthcare", "exit_type": "IPO", "cost_basis": 3000000, "proceeds": 12500000},
      {"company": "Gamma Retail", "sector": "Consumer", "exit_type": "write-off", "cost_basis": 2000000, "proceeds": 0}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exit_multiple_analysis"`.

---
skill: pme_calculator
category: fund_admin
description: Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path. PME > 1.0 means the fund outperformed the public market benchmark.
tier: premium
inputs: contributions, distributions, index_returns, residual_nav
---

# Pme Calculator

## Description
Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path. PME > 1.0 means the fund outperformed the public market benchmark. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| contributions | array | Yes | Ordered sequence of LP capital contributions per period (positive numbers, USD) |
| distributions | array | Yes | Ordered sequence of LP distributions per period, aligned to contributions (positive numbers, USD) |
| index_returns | array | Yes | Ordered sequence of benchmark index returns per period as decimals (e.g. 0.12 for 12%), aligned to contributions |
| residual_nav | number | No | Remaining NAV at end of the evaluation period added as a final distribution for PME computation (default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pme_calculator",
  "arguments": {
    "contributions": [10000000, 8000000, 6000000, 0, 0],
    "distributions": [0, 0, 2000000, 12000000, 22000000],
    "index_returns": [0.15, 0.08, -0.05, 0.22, 0.18],
    "residual_nav": 5000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pme_calculator"`.

---
skill: rwa_portfolio_stress_tester
category: rwa_tokenization
description: Applies price haircuts and default shocks to estimate stressed RWA portfolio values.
tier: free
inputs: portfolio_value, haircut_pct, default_rate_pct
---

# Rwa Portfolio Stress Tester

## Description
Applies price haircuts and default shocks to estimate stressed RWA portfolio values.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_value` | `number` | Yes | Current market value |
| `haircut_pct` | `number` | Yes | Market value haircut percent |
| `default_rate_pct` | `number` | Yes | Default rate applied to assets |
| `lgd_pct` | `number` | No | Loss given default percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_portfolio_stress_tester",
  "arguments": {
    "portfolio_value": 0,
    "haircut_pct": 0,
    "default_rate_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_portfolio_stress_tester"`.

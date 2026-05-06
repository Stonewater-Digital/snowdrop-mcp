---
skill: rwa_liquidity_premium_calculator
category: rwa_tokenization
description: Combines base rates, liquidity spreads, and tenor adjustments to set yield targets.
tier: free
inputs: base_rate_pct, illiquidity_spread_bps, tenor_years
---

# Rwa Liquidity Premium Calculator

## Description
Combines base rates, liquidity spreads, and tenor adjustments to set yield targets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_rate_pct` | `number` | Yes | Risk-free benchmark rate |
| `illiquidity_spread_bps` | `number` | Yes | Spread per 100 bps of illiquidity |
| `tenor_years` | `number` | Yes | Investment tenor in years |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_liquidity_premium_calculator",
  "arguments": {
    "base_rate_pct": 0,
    "illiquidity_spread_bps": 0,
    "tenor_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_liquidity_premium_calculator"`.

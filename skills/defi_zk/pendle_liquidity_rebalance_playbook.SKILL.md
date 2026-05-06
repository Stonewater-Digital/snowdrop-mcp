---
skill: pendle_liquidity_rebalance_playbook
category: defi_zk
description: Builds Pendle liquidity rebalance plans for yield rotations.
tier: free
inputs: principal_usd, base_yield_apr, volatility_score, lockup_days
---

# Pendle Liquidity Rebalance Playbook

## Description
Builds Pendle liquidity rebalance plans for yield rotations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal_usd` | `number` | Yes | Capital deployed into the strategy. |
| `base_yield_apr` | `number` | Yes | Observed APR from live dashboards. |
| `volatility_score` | `number` | Yes | 0-1 measure of pool volatility. |
| `lockup_days` | `number` | Yes | Expected lockup horizon in days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pendle_liquidity_rebalance_playbook",
  "arguments": {
    "principal_usd": 0,
    "base_yield_apr": 0,
    "volatility_score": 0,
    "lockup_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pendle_liquidity_rebalance_playbook"`.

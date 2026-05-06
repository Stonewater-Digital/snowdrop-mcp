---
skill: pendle_impermanent_loss_guardrail
category: defi_zk
description: Simulates Pendle IL exposure for dual-asset pools and recommends caps.
tier: free
inputs: principal_usd, base_yield_apr, volatility_score, lockup_days
---

# Pendle Impermanent Loss Guardrail

## Description
Simulates Pendle IL exposure for dual-asset pools and recommends caps.

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
  "tool": "pendle_impermanent_loss_guardrail",
  "arguments": {
    "principal_usd": 0,
    "base_yield_apr": 0,
    "volatility_score": 0,
    "lockup_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pendle_impermanent_loss_guardrail"`.

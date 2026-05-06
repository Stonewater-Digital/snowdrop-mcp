---
skill: sa_ccr_calculator
category: regulatory_capital
description: Simplified SA-CCR calculation: EAD = alpha * (RC + PFE).
tier: free
inputs: trades, collateral
---

# Sa Ccr Calculator

## Description
Simplified SA-CCR calculation: EAD = alpha * (RC + PFE).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trades` | `array` | Yes | Trades with MtM and add-on parameters. |
| `collateral` | `number` | Yes | Collateral held against the netting set. |
| `alpha_multiplier` | `number` | No | Basel alpha multiplier (default 1.4). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sa_ccr_calculator",
  "arguments": {
    "trades": [],
    "collateral": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sa_ccr_calculator"`.

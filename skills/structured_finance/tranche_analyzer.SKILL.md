---
skill: tranche_analyzer
category: structured_finance
description: Calculates tranche credit enhancement, expected loss, and implied ratings.
tier: free
inputs: total_pool, expected_loss_pct, loss_volatility, tranches
---

# Tranche Analyzer

## Description
Calculates tranche credit enhancement, expected loss, and implied ratings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_pool` | `number` | Yes |  |
| `expected_loss_pct` | `number` | Yes |  |
| `loss_volatility` | `number` | Yes |  |
| `tranches` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tranche_analyzer",
  "arguments": {
    "total_pool": 0,
    "expected_loss_pct": 0,
    "loss_volatility": 0,
    "tranches": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tranche_analyzer"`.

---
skill: sharpe_ratio_calculator
category: risk
description: Calculates Sharpe, Sortino, and ancillary performance stats.
tier: free
inputs: returns
---

# Sharpe Ratio Calculator

## Description
Calculates Sharpe, Sortino, and ancillary performance stats.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes |  |
| `risk_free_rate_annual` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sharpe_ratio_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sharpe_ratio_calculator"`.

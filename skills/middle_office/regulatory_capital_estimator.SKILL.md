---
skill: regulatory_capital_estimator
category: middle_office
description: Estimates Basel-style RWA and capital ratios for market risk books.
tier: free
inputs: positions, tier1_capital
---

# Regulatory Capital Estimator

## Description
Estimates Basel-style RWA and capital ratios for market risk books.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `tier1_capital` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "regulatory_capital_estimator",
  "arguments": {
    "positions": [],
    "tier1_capital": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "regulatory_capital_estimator"`.

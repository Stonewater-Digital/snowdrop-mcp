---
skill: deposit_pricing_analyzer
category: banking
description: Calculates weighted cost of deposits, effective beta, and expense impact from rate shifts.
tier: free
inputs: deposits, rate_change_bps
---

# Deposit Pricing Analyzer

## Description
Calculates weighted cost of deposits, effective beta, and expense impact from rate shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `deposits` | `array` | Yes |  |
| `rate_change_bps` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "deposit_pricing_analyzer",
  "arguments": {
    "deposits": [],
    "rate_change_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "deposit_pricing_analyzer"`.

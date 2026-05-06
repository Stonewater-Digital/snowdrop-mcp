---
skill: balance_optimization_calculator
category: credit
description: Suggest balance redistribution across credit cards to minimize interest while keeping per-card utilization below 30%.
tier: free
inputs: cards
---

# Balance Optimization Calculator

## Description
Suggest balance redistribution across credit cards to minimize interest while keeping per-card utilization below 30%.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cards` | `array` | Yes | List of credit cards. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "balance_optimization_calculator",
  "arguments": {
    "cards": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "balance_optimization_calculator"`.

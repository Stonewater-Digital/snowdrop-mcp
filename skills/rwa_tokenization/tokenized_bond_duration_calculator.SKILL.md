---
skill: tokenized_bond_duration_calculator
category: rwa_tokenization
description: Computes Macaulay and modified duration from cash-flow schedules of tokenized bonds.
tier: free
inputs: cash_flows, yield_pct
---

# Tokenized Bond Duration Calculator

## Description
Computes Macaulay and modified duration from cash-flow schedules of tokenized bonds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_flows` | `array` | Yes | Cash flow schedule for the bond |
| `yield_pct` | `number` | Yes | Yield to maturity percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tokenized_bond_duration_calculator",
  "arguments": {
    "cash_flows": [],
    "yield_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tokenized_bond_duration_calculator"`.

---
skill: carry_trade_calculator
category: quant
description: Computes carry-to-vol metrics for FX pairs using interest differentials.
tier: free
inputs: pairs
---

# Carry Trade Calculator

## Description
Computes carry-to-vol metrics for FX pairs using interest differentials.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pairs` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "carry_trade_calculator",
  "arguments": {
    "pairs": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carry_trade_calculator"`.

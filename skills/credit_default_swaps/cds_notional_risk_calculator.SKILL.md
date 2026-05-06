---
skill: cds_notional_risk_calculator
category: credit_default_swaps
description: Computes gross, net, and concentration metrics for CDS notionals.
tier: free
inputs: positions
---

# Cds Notional Risk Calculator

## Description
Computes gross, net, and concentration metrics for CDS notionals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_notional_risk_calculator",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_notional_risk_calculator"`.

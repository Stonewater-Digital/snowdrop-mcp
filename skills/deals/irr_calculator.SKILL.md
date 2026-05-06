---
skill: irr_calculator
category: deals
description: Computes IRR, MOIC, and profit metrics from dated cash flows.
tier: free
inputs: cash_flows
---

# Irr Calculator

## Description
Computes IRR, MOIC, and profit metrics from dated cash flows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_flows` | `array` | Yes | List of dicts with date (ISO) and amount (negative=outflow). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "irr_calculator",
  "arguments": {
    "cash_flows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "irr_calculator"`.

---
skill: default_fund_sizing
category: quantitative_risk
description: Computes cover-2 requirement using member stress losses net of margin and allocates contributions.
tier: free
inputs: clearing_members, margin_held
---

# Default Fund Sizing

## Description
Computes cover-2 requirement using member stress losses net of margin and allocates contributions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `clearing_members` | `array` | Yes | Members with stress loss estimates and current margin. |
| `margin_held` | `number` | Yes | Aggregate initial margin held by CCP. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "default_fund_sizing",
  "arguments": {
    "clearing_members": [],
    "margin_held": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "default_fund_sizing"`.

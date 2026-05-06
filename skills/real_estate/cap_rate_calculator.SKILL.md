---
skill: cap_rate_calculator
category: real_estate
description: Calculate capitalization rate (cap rate) from net operating income and property value. Cap rate = NOI / Property Value.
tier: free
inputs: net_operating_income, property_value
---

# Cap Rate Calculator

## Description
Calculate capitalization rate (cap rate) from net operating income and property value. Cap rate = NOI / Property Value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_operating_income` | `number` | Yes | Annual net operating income in USD. |
| `property_value` | `number` | Yes | Current property value or purchase price in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cap_rate_calculator",
  "arguments": {
    "net_operating_income": 0,
    "property_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_rate_calculator"`.

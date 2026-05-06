---
skill: unit_economics_analyzer
category: small_business
description: Analyze unit economics including gross margin, LTV:CAC ratio, and CAC payback period.
tier: free
inputs: price, cogs, cac, ltv
---

# Unit Economics Analyzer

## Description
Analyze unit economics including gross margin, LTV:CAC ratio, and CAC payback period.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price` | `number` | Yes | Revenue per unit/transaction. |
| `cogs` | `number` | Yes | Cost of goods sold per unit. |
| `cac` | `number` | Yes | Customer Acquisition Cost. |
| `ltv` | `number` | Yes | Customer Lifetime Value. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "unit_economics_analyzer",
  "arguments": {
    "price": 0,
    "cogs": 0,
    "cac": 0,
    "ltv": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "unit_economics_analyzer"`.

---
skill: gross_profit_margin_calculator
category: accounting
description: Calculates gross profit margin as a percentage, measuring the proportion of revenue retained after direct production costs.
tier: free
inputs: revenue, cogs
---

# Gross Profit Margin Calculator

## Description
Calculates gross profit margin as a percentage, measuring the proportion of revenue retained after direct production costs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue` | `number` | Yes | Total revenue. |
| `cogs` | `number` | Yes | Cost of goods sold. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gross_profit_margin_calculator",
  "arguments": {
    "revenue": 0,
    "cogs": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gross_profit_margin_calculator"`.

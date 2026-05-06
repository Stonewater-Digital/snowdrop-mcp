---
skill: return_on_assets_calculator
category: accounting
description: Calculates return on assets (ROA) as a percentage, measuring how efficiently a company uses its assets to generate profit.
tier: free
inputs: net_income, avg_total_assets
---

# Return On Assets Calculator

## Description
Calculates return on assets (ROA) as a percentage, measuring how efficiently a company uses its assets to generate profit.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income for the period. |
| `avg_total_assets` | `number` | Yes | Average total assets for the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "return_on_assets_calculator",
  "arguments": {
    "net_income": 0,
    "avg_total_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "return_on_assets_calculator"`.

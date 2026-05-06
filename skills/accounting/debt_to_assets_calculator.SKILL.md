---
skill: debt_to_assets_calculator
category: accounting
description: Calculates the debt-to-assets ratio, showing the proportion of total assets financed through debt.
tier: free
inputs: total_debt, total_assets
---

# Debt To Assets Calculator

## Description
Calculates the debt-to-assets ratio, showing the proportion of total assets financed through debt.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_debt` | `number` | Yes | Total debt (short-term + long-term). |
| `total_assets` | `number` | Yes | Total assets. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_to_assets_calculator",
  "arguments": {
    "total_debt": 0,
    "total_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_to_assets_calculator"`.

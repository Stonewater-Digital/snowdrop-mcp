---
skill: altman_z_score
category: financial_analysis
description: Calculates Altman Z, identifies zone, and estimates distress probability.
tier: free
inputs: working_capital, total_assets, retained_earnings, ebit, market_cap, total_liabilities, revenue
---

# Altman Z Score

## Description
Calculates Altman Z, identifies zone, and estimates distress probability.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `working_capital` | `number` | Yes |  |
| `total_assets` | `number` | Yes |  |
| `retained_earnings` | `number` | Yes |  |
| `ebit` | `number` | Yes |  |
| `market_cap` | `number` | Yes |  |
| `total_liabilities` | `number` | Yes |  |
| `revenue` | `number` | Yes |  |
| `model` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "altman_z_score",
  "arguments": {
    "working_capital": 0,
    "total_assets": 0,
    "retained_earnings": 0,
    "ebit": 0,
    "market_cap": 0,
    "total_liabilities": 0,
    "revenue": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "altman_z_score"`.

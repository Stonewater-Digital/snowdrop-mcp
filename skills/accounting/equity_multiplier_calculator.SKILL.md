---
skill: equity_multiplier_calculator
category: accounting
description: Calculates the equity multiplier (total assets / total equity), a measure of financial leverage used in DuPont analysis.
tier: free
inputs: total_assets, total_equity
---

# Equity Multiplier Calculator

## Description
Calculates the equity multiplier (total assets / total equity), a measure of financial leverage used in DuPont analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_assets` | `number` | Yes | Total assets. |
| `total_equity` | `number` | Yes | Total shareholders equity. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "equity_multiplier_calculator",
  "arguments": {
    "total_assets": 0,
    "total_equity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "equity_multiplier_calculator"`.

---
skill: current_ratio_calculator
category: accounting
description: Calculates the current ratio (current assets / current liabilities) and provides an interpretive assessment of liquidity strength.
tier: free
inputs: current_assets, current_liabilities
---

# Current Ratio Calculator

## Description
Calculates the current ratio (current assets / current liabilities) and provides an interpretive assessment of liquidity strength.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_assets` | `number` | Yes | Total current assets. |
| `current_liabilities` | `number` | Yes | Total current liabilities. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "current_ratio_calculator",
  "arguments": {
    "current_assets": 0,
    "current_liabilities": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "current_ratio_calculator"`.

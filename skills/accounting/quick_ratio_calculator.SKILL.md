---
skill: quick_ratio_calculator
category: accounting
description: Calculates the quick ratio (acid-test ratio) by excluding inventory from current assets, providing a stricter measure of short-term liquidity.
tier: free
inputs: current_assets, inventory, current_liabilities
---

# Quick Ratio Calculator

## Description
Calculates the quick ratio (acid-test ratio) by excluding inventory from current assets, providing a stricter measure of short-term liquidity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_assets` | `number` | Yes | Total current assets. |
| `inventory` | `number` | Yes | Inventory value to exclude from current assets. |
| `current_liabilities` | `number` | Yes | Total current liabilities. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "quick_ratio_calculator",
  "arguments": {
    "current_assets": 0,
    "inventory": 0,
    "current_liabilities": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "quick_ratio_calculator"`.

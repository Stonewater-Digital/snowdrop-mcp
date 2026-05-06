---
skill: working_capital_calculator
category: accounting
description: Calculates net working capital and the current ratio to assess short-term liquidity.
tier: free
inputs: current_assets, current_liabilities
---

# Working Capital Calculator

## Description
Calculates net working capital and the current ratio to assess short-term liquidity.

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
  "tool": "working_capital_calculator",
  "arguments": {
    "current_assets": 0,
    "current_liabilities": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "working_capital_calculator"`.

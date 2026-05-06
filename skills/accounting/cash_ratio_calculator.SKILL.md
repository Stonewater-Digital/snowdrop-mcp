---
skill: cash_ratio_calculator
category: accounting
description: Calculates the cash ratio using only cash and marketable securities, the most conservative short-term liquidity measure.
tier: free
inputs: cash, marketable_securities, current_liabilities
---

# Cash Ratio Calculator

## Description
Calculates the cash ratio using only cash and marketable securities, the most conservative short-term liquidity measure.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash` | `number` | Yes | Cash and cash equivalents. |
| `marketable_securities` | `number` | Yes | Short-term marketable securities. |
| `current_liabilities` | `number` | Yes | Total current liabilities. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cash_ratio_calculator",
  "arguments": {
    "cash": 0,
    "marketable_securities": 0,
    "current_liabilities": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_ratio_calculator"`.

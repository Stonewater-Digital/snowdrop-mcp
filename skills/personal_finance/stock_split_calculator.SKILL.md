---
skill: stock_split_calculator
category: personal_finance
description: Computes the new share count and per-share price after a split while keeping total value and cost basis aligned.
tier: free
inputs: pre_split_shares, pre_split_price, split_ratio
---

# Stock Split Calculator

## Description
Computes the new share count and per-share price after a split while keeping total value and cost basis aligned.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pre_split_shares` | `number` | Yes | Share count before the split. |
| `pre_split_price` | `number` | Yes | Share price before the split. |
| `split_ratio` | `string` | Yes | Split ratio formatted like '4:1' or '1:5'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "stock_split_calculator",
  "arguments": {
    "pre_split_shares": 0,
    "pre_split_price": 0,
    "split_ratio": "<split_ratio>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stock_split_calculator"`.

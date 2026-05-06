---
skill: transaction_fee_analyzer
category: blockchain_analytics
description: Analyzes fee samples and block utilization to guide transaction fee bidding.
tier: free
inputs: fees, block_utilization_pct
---

# Transaction Fee Analyzer

## Description
Analyzes fee samples and block utilization to guide transaction fee bidding.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fees` | `array` | Yes | List of fee datapoints {timestamp, fee_amount, gas_used, gas_price}. |
| `block_utilization_pct` | `number` | Yes | Current block utilization percentage (0-100). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transaction_fee_analyzer",
  "arguments": {
    "fees": [],
    "block_utilization_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transaction_fee_analyzer"`.

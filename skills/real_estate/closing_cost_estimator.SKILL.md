---
skill: closing_cost_estimator
category: real_estate
description: Estimate closing costs for a home purchase (2-5% of price). Itemizes title insurance, appraisal, origination fees, escrow, recording fees, and more.
tier: free
inputs: home_price
---

# Closing Cost Estimator

## Description
Estimate closing costs for a home purchase (2-5% of price). Itemizes title insurance, appraisal, origination fees, escrow, recording fees, and more.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `home_price` | `number` | Yes | Home purchase price in USD. |
| `location` | `string` | No | General location indicator affecting cost range: low, average, or high. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "closing_cost_estimator",
  "arguments": {
    "home_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "closing_cost_estimator"`.

---
skill: rebalance_trigger
category: fund_accounting
description: Checks portfolio split vs. target bands and surfaces recommended skims or reviews.
tier: premium
inputs: boring_value, thunder_value
---

# Rebalance Trigger

## Description
Checks portfolio split vs. target bands and surfaces recommended skims or reviews. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `boring_value` | `number` | Yes | Current market value of the "boring" (low-risk, income) sleeve of the portfolio in dollars. |
| `thunder_value` | `number` | Yes | Current market value of the "thunder" (high-conviction, growth) sleeve of the portfolio in dollars. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rebalance_trigger",
  "arguments": {
    "boring_value": 8200000,
    "thunder_value": 2100000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rebalance_trigger"`.

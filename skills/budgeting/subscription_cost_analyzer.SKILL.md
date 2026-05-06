---
skill: subscription_cost_analyzer
category: budgeting
description: Analyzes subscription costs: total monthly and annual spending, sorted by cost.
tier: free
inputs: subscriptions
---

# Subscription Cost Analyzer

## Description
Analyzes subscription costs: total monthly and annual spending, sorted by cost.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subscriptions` | `array` | Yes | List of subscriptions with name and monthly cost. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "subscription_cost_analyzer",
  "arguments": {
    "subscriptions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "subscription_cost_analyzer"`.

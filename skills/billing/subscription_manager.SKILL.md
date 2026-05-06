---
skill: subscription_manager
category: billing
description: Identifies subscriptions due for billing and drafts charge records.
tier: free
inputs: subscriptions, current_date
---

# Subscription Manager

## Description
Identifies subscriptions due for billing and drafts charge records.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subscriptions` | `array` | Yes |  |
| `current_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "subscription_manager",
  "arguments": {
    "subscriptions": [],
    "current_date": "<current_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "subscription_manager"`.

---
skill: rwa_private_credit_payment_default_signal_router
category: crypto_rwa
description: Routes delinquency signals to holders and pauses distributions until resolved.
tier: free
inputs: payload
---

# Rwa Private Credit Payment Default Signal Router

## Description
Routes delinquency signals to holders and pauses distributions until resolved.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_private_credit_payment_default_signal_router",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_private_credit_payment_default_signal_router"`.

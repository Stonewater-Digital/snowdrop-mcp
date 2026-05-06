---
skill: enterprise_risk_retention_optimizer
category: corporate_insurance
description: Selects corporate retention using expected loss curve and premium quotes.
tier: free
inputs: retention_options
---

# Enterprise Risk Retention Optimizer

## Description
Selects corporate retention using expected loss curve and premium quotes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `retention_options` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "enterprise_risk_retention_optimizer",
  "arguments": {
    "retention_options": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "enterprise_risk_retention_optimizer"`.

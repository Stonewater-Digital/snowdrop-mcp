---
skill: credit_limit_optimizer
category: credit
description: Calculate the ideal total credit limit to achieve a target utilization ratio based on income and existing limits.
tier: free
inputs: income, existing_limits
---

# Credit Limit Optimizer

## Description
Calculate the ideal total credit limit to achieve a target utilization ratio based on income and existing limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `income` | `number` | Yes | Annual gross income. |
| `existing_limits` | `array` | Yes | List of current credit limits. |
| `utilization_target` | `number` | No | Target utilization ratio as decimal (default 0.30). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_limit_optimizer",
  "arguments": {
    "income": 0,
    "existing_limits": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_limit_optimizer"`.

---
skill: review_cost_estimator
category: crowd_economics
description: Approximates token/time cost to review a submission.
tier: free
inputs: submission
---

# Review Cost Estimator

## Description
Approximates token/time cost to review a submission.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `submission` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "review_cost_estimator",
  "arguments": {
    "submission": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "review_cost_estimator"`.

---
skill: repo_value_estimator
category: crowd_economics
description: Estimates tokens and dollars needed to rebuild the repo from scratch.
tier: free
inputs: skills
---

# Repo Value Estimator

## Description
Estimates tokens and dollars needed to rebuild the repo from scratch.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes |  |
| `model_pricing` | `object` | No |  |
| `iterations_per_skill` | `number` | No |  |
| `actual_cost_paid` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "repo_value_estimator",
  "arguments": {
    "skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "repo_value_estimator"`.

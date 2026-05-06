---
skill: contribution_quality_scorer
category: crowd_economics
description: Calculates quality grades based on Snowdrop coding standards and security checks.
tier: free
inputs: submission
---

# Contribution Quality Scorer

## Description
Calculates quality grades based on Snowdrop coding standards and security checks.

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
  "tool": "contribution_quality_scorer",
  "arguments": {
    "submission": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contribution_quality_scorer"`.

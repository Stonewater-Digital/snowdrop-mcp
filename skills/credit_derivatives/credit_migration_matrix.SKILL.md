---
skill: credit_migration_matrix
category: credit_derivatives
description: Converts raw rating transition counts into normalized probability matrices and drift statistics.
tier: free
inputs: rating_transitions, rating_scale
---

# Credit Migration Matrix

## Description
Converts raw rating transition counts into normalized probability matrices and drift statistics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `rating_transitions` | `array` | Yes | List of records with 'from', 'to', and 'count' fields representing observed migrations. |
| `rating_scale` | `array` | Yes | Ordered ratings from highest quality to default (e.g., ['AAA',...,'D']). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_migration_matrix",
  "arguments": {
    "rating_transitions": [],
    "rating_scale": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_migration_matrix"`.

---
skill: credit_quality_migration_tracker
category: private_credit
description: Compares prior and current rating distributions to flag drift.
tier: free
inputs: prior_distribution, current_distribution
---

# Credit Quality Migration Tracker

## Description
Compares prior and current rating distributions to flag drift.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prior_distribution` | `object` | Yes |  |
| `current_distribution` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_quality_migration_tracker",
  "arguments": {
    "prior_distribution": {},
    "current_distribution": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_quality_migration_tracker"`.

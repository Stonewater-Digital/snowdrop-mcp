---
skill: contributor_retention_analyzer
category: crowd_economics
description: Tracks contributor repeat rates, retention curves, and churn metrics.
tier: free
inputs: contributions
---

# Contributor Retention Analyzer

## Description
Tracks contributor repeat rates, retention curves, and churn metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contributions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contributor_retention_analyzer",
  "arguments": {
    "contributions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contributor_retention_analyzer"`.

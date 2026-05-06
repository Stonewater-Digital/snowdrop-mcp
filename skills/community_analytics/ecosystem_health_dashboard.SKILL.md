---
skill: ecosystem_health_dashboard
category: community_analytics
description: Aggregates community metrics into a public health score and highlights.
tier: free
inputs: metrics
---

# Ecosystem Health Dashboard

## Description
Aggregates community metrics into a public health score and highlights.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `metrics` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ecosystem_health_dashboard",
  "arguments": {
    "metrics": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ecosystem_health_dashboard"`.

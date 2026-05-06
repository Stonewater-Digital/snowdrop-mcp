---
skill: data_freshness_monitor
category: data_quality
description: Checks data sources against allowed staleness windows.
tier: free
inputs: sources
---

# Data Freshness Monitor

## Description
Checks data sources against allowed staleness windows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sources` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "data_freshness_monitor",
  "arguments": {
    "sources": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "data_freshness_monitor"`.

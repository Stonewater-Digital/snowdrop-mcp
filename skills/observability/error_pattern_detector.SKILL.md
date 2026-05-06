---
skill: error_pattern_detector
category: observability
description: Clusters similar errors and surfaces bursts for remediation.
tier: free
inputs: errors
---

# Error Pattern Detector

## Description
Clusters similar errors and surfaces bursts for remediation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `errors` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "error_pattern_detector",
  "arguments": {
    "errors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "error_pattern_detector"`.

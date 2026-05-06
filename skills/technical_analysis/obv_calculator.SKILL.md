---
skill: obv_calculator
category: technical_analysis
description: Computes cumulative On-Balance Volume to confirm price trends vs volume flows.
tier: free
inputs: closes, volumes
---

# Obv Calculator

## Description
Computes cumulative On-Balance Volume to confirm price trends vs volume flows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | Closing prices (oldest first). |
| `volumes` | `array` | Yes | Volume per period aligned with closes. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "obv_calculator",
  "arguments": {
    "closes": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "obv_calculator"`.

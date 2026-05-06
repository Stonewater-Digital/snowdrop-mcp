---
skill: competitive_landscape_tracker
category: competitive
description: Compares competitor offerings, pricing, and feature coverage.
tier: free
inputs: competitors, snowdrop_services, snowdrop_pricing
---

# Competitive Landscape Tracker

## Description
Compares competitor offerings, pricing, and feature coverage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `competitors` | `array` | Yes |  |
| `snowdrop_services` | `array` | Yes |  |
| `snowdrop_pricing` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "competitive_landscape_tracker",
  "arguments": {
    "competitors": [],
    "snowdrop_services": [],
    "snowdrop_pricing": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "competitive_landscape_tracker"`.

---
skill: force_index_calculator
category: technical_analysis
description: Calculate the Force Index, which combines price change and volume to measure the strength of bulls and bears. Uses EMA smoothing.
tier: free
inputs: closes, volumes
---

# Force Index Calculator

## Description
Calculate the Force Index, which combines price change and volume to measure the strength of bulls and bears. Uses EMA smoothing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `volumes` | `array` | Yes | List of volume values (oldest to newest). |
| `period` | `integer` | No | EMA smoothing period for the Force Index. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "force_index_calculator",
  "arguments": {
    "closes": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "force_index_calculator"`.

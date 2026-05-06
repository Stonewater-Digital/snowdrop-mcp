---
skill: lot_size_calculator
category: fx
description: Convert a unit count into standard lots (100,000), mini lots (10,000), and micro lots (1,000).
tier: free
inputs: units
---

# Lot Size Calculator

## Description
Convert a unit count into standard lots (100,000), mini lots (10,000), and micro lots (1,000).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `units` | `integer` | Yes | Number of currency units. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lot_size_calculator",
  "arguments": {
    "units": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lot_size_calculator"`.

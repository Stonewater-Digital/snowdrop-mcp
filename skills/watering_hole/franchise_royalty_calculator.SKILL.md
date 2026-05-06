---
skill: franchise_royalty_calculator
category: watering_hole
description: Computes 10% RSS revenue royalties owed by Bar-in-a-Box franchisees.
tier: free
inputs: sub_bars
---

# Franchise Royalty Calculator

## Description
Computes 10% RSS revenue royalties owed by Bar-in-a-Box franchisees.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sub_bars` | `array` | Yes | Per-franchise revenue feed entries. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "franchise_royalty_calculator",
  "arguments": {
    "sub_bars": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "franchise_royalty_calculator"`.

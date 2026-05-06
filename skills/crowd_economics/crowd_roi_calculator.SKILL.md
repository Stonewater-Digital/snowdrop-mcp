---
skill: crowd_roi_calculator
category: crowd_economics
description: Measures value created by community contributions versus review cost.
tier: free
inputs: community_contributions
---

# Crowd Roi Calculator

## Description
Measures value created by community contributions versus review cost.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `community_contributions` | `array` | Yes |  |
| `token_price_per_mtok` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crowd_roi_calculator",
  "arguments": {
    "community_contributions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crowd_roi_calculator"`.

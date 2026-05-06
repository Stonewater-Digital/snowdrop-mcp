---
skill: large_exposure_checker
category: regulatory_capital
description: Identifies exposures exceeding Basel LE limits (25% Tier1, 15% for G-SIB counterparties).
tier: free
inputs: exposures, tier1_capital, is_gsib
---

# Large Exposure Checker

## Description
Identifies exposures exceeding Basel LE limits (25% Tier1, 15% for G-SIB counterparties).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | Counterparty exposure and group info. |
| `tier1_capital` | `number` | Yes | Tier 1 capital used for limit. |
| `is_gsib` | `boolean` | Yes | Whether firm is G-SIB (15% limit). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "large_exposure_checker",
  "arguments": {
    "exposures": [],
    "tier1_capital": 0,
    "is_gsib": false
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "large_exposure_checker"`.

---
skill: allocation_enforcer_80_20
category: fund_accounting
description: Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: positions, overrides
---

# Allocation Enforcer 80 20

## Description
Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes | List of current portfolio positions, each with asset identifier and current market value. |
| `overrides` | `object` | No | Optional map of asset identifiers to override allocation band labels (e.g. `{"AAPL": "boring"}`). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "allocation_enforcer_80_20",
  "arguments": {
    "positions": [
      {"asset": "SPY", "value": 8000000, "category": "boring"},
      {"asset": "BTC", "value": 2000000, "category": "thunder"}
    ],
    "overrides": null
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "allocation_enforcer_80_20"`.

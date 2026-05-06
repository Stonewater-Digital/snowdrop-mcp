---
skill: sovereign_wealth_alpha_source
category: sovereign
description: Screens and ranks sovereign wealth fund investment opportunities by return/risk ratio against configurable criteria.
tier: free
inputs: criteria, opportunities
---

# Sovereign Wealth Alpha Source

## Description
Screens and ranks sovereign wealth fund investment opportunities by return/risk ratio against configurable criteria.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `criteria` | `object` | Yes | Investment screening criteria |
| `opportunities` | `array` | Yes | Investment opportunities to evaluate |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sovereign_wealth_alpha_source",
  "arguments": {
    "criteria": {},
    "opportunities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sovereign_wealth_alpha_source"`.

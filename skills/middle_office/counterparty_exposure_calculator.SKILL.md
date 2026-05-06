---
skill: counterparty_exposure_calculator
category: middle_office
description: Aggregates MTM by counterparty, applies collateral, and flags threshold breaches.
tier: free
inputs: positions
---

# Counterparty Exposure Calculator

## Description
Aggregates MTM by counterparty, applies collateral, and flags threshold breaches.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "counterparty_exposure_calculator",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "counterparty_exposure_calculator"`.

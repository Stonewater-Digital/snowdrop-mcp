---
skill: interest_rate_sensitivity_reit
category: reits
description: Calculates fixed vs floating mix, duration, and DV01 for the debt stack.
tier: free
inputs: debt_instruments
---

# Interest Rate Sensitivity Reit

## Description
Calculates fixed vs floating mix, duration, and DV01 for the debt stack.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `debt_instruments` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "interest_rate_sensitivity_reit",
  "arguments": {
    "debt_instruments": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_rate_sensitivity_reit"`.

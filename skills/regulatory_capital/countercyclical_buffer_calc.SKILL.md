---
skill: countercyclical_buffer_calc
category: regulatory_capital
description: Weights jurisdiction CCyB rates by credit exposures to derive bank-specific buffer.
tier: free
inputs: exposures, risk_weighted_assets
---

# Countercyclical Buffer Calc

## Description
Weights jurisdiction CCyB rates by credit exposures to derive bank-specific buffer.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | Exposures with CCyB rate info. |
| `risk_weighted_assets` | `number` | Yes | Total RWA for translating rate to buffer amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "countercyclical_buffer_calc",
  "arguments": {
    "exposures": [],
    "risk_weighted_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "countercyclical_buffer_calc"`.

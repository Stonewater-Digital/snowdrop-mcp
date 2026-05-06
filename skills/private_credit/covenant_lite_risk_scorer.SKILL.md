---
skill: covenant_lite_risk_scorer
category: private_credit
description: Assigns protection scores based on covenant packages and aggressive terms.
tier: free
inputs: covenants_present, covenants_absent, has_equity_cure, portability, incremental_capacity_pct
---

# Covenant Lite Risk Scorer

## Description
Assigns protection scores based on covenant packages and aggressive terms.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `covenants_present` | `array` | Yes |  |
| `covenants_absent` | `array` | Yes |  |
| `has_equity_cure` | `boolean` | Yes |  |
| `portability` | `boolean` | Yes |  |
| `incremental_capacity_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "covenant_lite_risk_scorer",
  "arguments": {
    "covenants_present": [],
    "covenants_absent": [],
    "has_equity_cure": false,
    "portability": false,
    "incremental_capacity_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "covenant_lite_risk_scorer"`.

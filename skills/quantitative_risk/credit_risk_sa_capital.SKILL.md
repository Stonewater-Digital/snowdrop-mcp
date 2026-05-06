---
skill: credit_risk_sa_capital
category: quantitative_risk
description: Calculates RWA for standardized approach exposures with credit conversion and collateral mitigation.
tier: free
inputs: exposures
---

# Credit Risk Sa Capital

## Description
Calculates RWA for standardized approach exposures with credit conversion and collateral mitigation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | Exposure items with risk weight and credit conversion factors. |
| `capital_ratio_pct` | `number` | No | Regulatory capital ratio to apply (default 8%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_risk_sa_capital",
  "arguments": {
    "exposures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_risk_sa_capital"`.

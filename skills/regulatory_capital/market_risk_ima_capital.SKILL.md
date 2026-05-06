---
skill: market_risk_ima_capital
category: regulatory_capital
description: Calculates IMA capital: max(m * VaR, m * sVaR) + IRC + CRM per Basel 2.5.
tier: free
inputs: var_10day, stressed_var_10day, incremental_risk_charge, comprehensive_risk_measure
---

# Market Risk Ima Capital

## Description
Calculates IMA capital: max(m * VaR, m * sVaR) + IRC + CRM per Basel 2.5.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `var_10day` | `number` | Yes | 10-day VaR. |
| `stressed_var_10day` | `number` | Yes | 10-day stressed VaR. |
| `incremental_risk_charge` | `number` | Yes | IRC add-on. |
| `comprehensive_risk_measure` | `number` | Yes | CRM add-on. |
| `multiplier` | `number` | No | Regulatory VaR multiplier (default 3). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "market_risk_ima_capital",
  "arguments": {
    "var_10day": 0,
    "stressed_var_10day": 0,
    "incremental_risk_charge": 0,
    "comprehensive_risk_measure": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "market_risk_ima_capital"`.

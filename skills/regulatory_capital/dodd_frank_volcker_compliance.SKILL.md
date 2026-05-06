---
skill: dodd_frank_volcker_compliance
category: regulatory_capital
description: Evaluates RENTD, inventory, and VaR metrics against Volcker Rule limits.
tier: free
inputs: trading_desk_inventory, rentd_limit, rentd_usage, customer_flow_ratio, risk_limit, value_at_risk
---

# Dodd Frank Volcker Compliance

## Description
Evaluates RENTD, inventory, and VaR metrics against Volcker Rule limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trading_desk_inventory` | `number` | Yes | Current inventory (positive=long). |
| `rentd_limit` | `number` | Yes | Reasonably expected near term demand limit. |
| `rentd_usage` | `number` | Yes | Current RENTD usage. |
| `customer_flow_ratio` | `number` | Yes | Customer facing volumes / proprietary volumes. |
| `risk_limit` | `number` | Yes | Approved VaR limit. |
| `value_at_risk` | `number` | Yes | Current VaR metric. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dodd_frank_volcker_compliance",
  "arguments": {
    "trading_desk_inventory": 0,
    "rentd_limit": 0,
    "rentd_usage": 0,
    "customer_flow_ratio": 0,
    "risk_limit": 0,
    "value_at_risk": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dodd_frank_volcker_compliance"`.

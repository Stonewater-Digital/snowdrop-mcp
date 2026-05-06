---
skill: resolution_planning_metrics
category: regulatory_capital
description: Generates key metrics for resolution planning submissions (165(d)).
tier: free
inputs: critical_functions, qualified_financial_contracts, inter_affiliate_exposures, tlac_amount
---

# Resolution Planning Metrics

## Description
Generates key metrics for resolution planning submissions (165(d)).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `critical_functions` | `array` | Yes | Functions with revenue and substitutability inputs. |
| `qualified_financial_contracts` | `integer` | Yes | Count of QFCs. |
| `inter_affiliate_exposures` | `number` | Yes | Inter-affiliate exposures |
| `tlac_amount` | `number` | Yes | TLAC resources available. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "resolution_planning_metrics",
  "arguments": {
    "critical_functions": [],
    "qualified_financial_contracts": 0,
    "inter_affiliate_exposures": 0,
    "tlac_amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "resolution_planning_metrics"`.

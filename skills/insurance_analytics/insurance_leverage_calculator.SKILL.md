---
skill: insurance_leverage_calculator
category: insurance_analytics
description: Computes leverage and capacity utilization metrics for P&C insurers: net written premium-to-surplus, liabilities-to-surplus, investment leverage, and capacity headroom vs. A.M.
tier: free
inputs: net_written_premium, policyholder_surplus, total_liabilities, invested_assets
---

# Insurance Leverage Calculator

## Description
Computes leverage and capacity utilization metrics for P&C insurers: net written premium-to-surplus, liabilities-to-surplus, investment leverage, and capacity headroom vs. A.M. Best benchmarks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_written_premium` | `number` | Yes | Annual net written premium (after cessions). Must be >= 0. |
| `policyholder_surplus` | `number` | Yes | Statutory policyholder surplus (net assets). Must be > 0. |
| `total_liabilities` | `number` | Yes | Total statutory liabilities (loss reserves + unearned premium + other). Must be >= 0. |
| `invested_assets` | `number` | Yes | Total invested assets at market value. Must be >= 0. |
| `nwp_to_surplus_benchmark` | `number` | No | NWP-to-surplus ratio threshold above which capacity is flagged as stretched. A.M. Best guideline is 3.0x; default 3.0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "insurance_leverage_calculator",
  "arguments": {
    "net_written_premium": 0,
    "policyholder_surplus": 0,
    "total_liabilities": 0,
    "invested_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "insurance_leverage_calculator"`.

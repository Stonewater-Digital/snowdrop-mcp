---
skill: hierarchical_risk_parity
category: portfolio_construction
description: Constructs Lopez de Prado's Hierarchical Risk Parity (HRP) allocation with single-linkage clustering and recursive bisection risk budgeting.
tier: free
inputs: asset_returns
---

# Hierarchical Risk Parity

## Description
Constructs Lopez de Prado's Hierarchical Risk Parity (HRP) allocation with single-linkage clustering and recursive bisection risk budgeting.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_returns` | `object` | Yes | Dictionary of asset identifiers to historical return series (decimal). |
| `min_periods` | `integer` | No | Minimum observations required per asset (default 60). |
| `linkage` | `string` | No | Linkage criterion: single or average (default single). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hierarchical_risk_parity",
  "arguments": {
    "asset_returns": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hierarchical_risk_parity"`.

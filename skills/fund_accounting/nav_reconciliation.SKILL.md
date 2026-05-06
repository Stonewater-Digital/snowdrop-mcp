---
skill: nav_reconciliation
category: fund_accounting
description: Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: assets, liabilities, shares_outstanding, prior_nav_per_share
---

# Nav Reconciliation

## Description
Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. Computes current NAV/share from total assets minus liabilities divided by shares outstanding, then diffs against the prior period NAV to surface unexplained movements. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes | List of asset objects, each with `name` and `fair_value` fields. |
| `liabilities` | `number` | Yes | Total fund liabilities in dollars. |
| `shares_outstanding` | `number` | Yes | Total shares / units outstanding. |
| `prior_nav_per_share` | `number` | No | NAV per share from prior period for variance reconciliation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nav_reconciliation",
  "arguments": {
    "assets": [
      {"name": "Portfolio Co A", "fair_value": 8500000},
      {"name": "Cash", "fair_value": 1200000}
    ],
    "liabilities": 300000,
    "shares_outstanding": 1000000,
    "prior_nav_per_share": 9.25
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nav_reconciliation"`.

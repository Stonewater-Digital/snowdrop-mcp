---
skill: quota_share_calculator
category: insurance_analytics
description: Computes ceded and retained premium, losses, ceding commission, and net underwriting result under a proportional quota share treaty. Supports fixed and provisional/sliding scale commission.
tier: free
inputs: gross_premium, gross_loss, quota_pct, ceding_commission_pct
---

# Quota Share Calculator

## Description
Computes ceded and retained premium, losses, ceding commission, and net underwriting result under a proportional quota share treaty. Supports fixed and provisional/sliding scale commission.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_premium` | `number` | Yes | Gross written premium subject to the quota share. Must be > 0. |
| `gross_loss` | `number` | Yes | Gross incurred losses subject to cession. Must be >= 0. |
| `quota_pct` | `number` | Yes | Cession percentage (0–100). E.g., 30.0 = cedant cedes 30% of premium and losses. |
| `ceding_commission_pct` | `number` | Yes | Ceding commission as a percentage of ceded premium (0–100). Represents the reinsurer's contribution to the cedant's acquisition costs. |
| `gross_expenses` | `number` | No | Gross underwriting expenses (before ceding commission offset). Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "quota_share_calculator",
  "arguments": {
    "gross_premium": 0,
    "gross_loss": 0,
    "quota_pct": 0,
    "ceding_commission_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "quota_share_calculator"`.

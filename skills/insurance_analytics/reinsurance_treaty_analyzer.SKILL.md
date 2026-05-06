---
skill: reinsurance_treaty_analyzer
category: insurance_analytics
description: Evaluates quota share and per-occurrence excess-of-loss treaty economics. Returns ceded and net premium/losses, ceding commission, and net combined ratio.
tier: free
inputs: treaty_type, gross_premium, gross_loss
---

# Reinsurance Treaty Analyzer

## Description
Evaluates quota share and per-occurrence excess-of-loss treaty economics. Returns ceded and net premium/losses, ceding commission, and net combined ratio.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `treaty_type` | `string` | Yes | Type of reinsurance treaty structure. |
| `gross_premium` | `number` | Yes | Gross written premium before cession. Must be > 0. |
| `gross_loss` | `number` | Yes | Gross incurred loss for the period. Must be >= 0. |
| `gross_expenses` | `number` | No | Gross underwriting expenses for the period. Must be >= 0. |
| `cession_pct` | `number` | No | Cession percentage for quota share (0–100). Required for quota_share. |
| `retention` | `number` | No | Per-occurrence retention (attachment point) for XL. Required for excess_of_loss. |
| `limit` | `number` | No | XL layer limit (maximum reinsurer payment per occurrence). Required for excess_of_loss. |
| `ceding_commission_pct` | `number` | No | Ceding commission as % of ceded premium (quota share only). 0–100. |
| `xol_rate_on_line_pct` | `number` | No | XL rate-on-line as % of ceded limit (price paid for the XL layer). Required for excess_of_loss to compute ceded premium. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reinsurance_treaty_analyzer",
  "arguments": {
    "treaty_type": "<treaty_type>",
    "gross_premium": 0,
    "gross_loss": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reinsurance_treaty_analyzer"`.

---
skill: excess_of_loss_calculator
category: insurance_analytics
description: Calculates per-occurrence reinsurance recoveries, layer loss ratio, attachment frequency, average in-layer severity, and reinstatement premium for an excess-of-loss (XL) reinsurance layer applied to a list of ground-up losses.
tier: free
inputs: ground_up_losses, attachment, limit
---

# Excess Of Loss Calculator

## Description
Calculates per-occurrence reinsurance recoveries, layer loss ratio, attachment frequency, average in-layer severity, and reinstatement premium for an excess-of-loss (XL) reinsurance layer applied to a list of ground-up losses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ground_up_losses` | `array` | Yes | List of per-occurrence ground-up loss amounts (before retention). Each must be >= 0. |
| `attachment` | `number` | Yes | Per-occurrence retention / attachment point. Must be >= 0. |
| `limit` | `number` | Yes | XL layer limit — maximum reinsurer payment per occurrence. Must be > 0. |
| `original_premium` | `number` | No | Original subject premium used to compute layer loss ratio (recoveries / original_premium). If omitted, loss ratio is computed as recoveries / (limit × event_count). |
| `reinstatement_premium_pct` | `number` | No | Reinstatement premium rate as % of the original layer premium for each dollar of limit consumed. E.g., 100 = 100% pro-rata reinstatement. Must be >= 0. |
| `xol_rate_on_line_pct` | `number` | No | Original layer premium as % of the layer limit (rate on line). Used to compute reinstatement premium. Required if reinstatement_premium_pct > 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "excess_of_loss_calculator",
  "arguments": {
    "ground_up_losses": [],
    "attachment": 0,
    "limit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "excess_of_loss_calculator"`.

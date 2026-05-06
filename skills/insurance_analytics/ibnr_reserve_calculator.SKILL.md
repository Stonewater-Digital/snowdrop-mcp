---
skill: ibnr_reserve_calculator
category: insurance_analytics
description: Estimates IBNR reserves using a volume-weighted chain-ladder approach. Accepts a loss development triangle (accident years × development periods) and per-year premiums.
tier: free
inputs: loss_triangle, premium_by_year
---

# Ibnr Reserve Calculator

## Description
Estimates IBNR reserves using a volume-weighted chain-ladder approach. Accepts a loss development triangle (accident years × development periods) and per-year premiums. Returns age-to-age development factors, projected ultimates, IBNR by year, and an expected loss ratio.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loss_triangle` | `array` | Yes | Cumulative loss development triangle. Each row is one accident year (oldest first); each column is a development period (12 months, 24 months, …). Cells beyond the latest diagonal should be null/None. |
| `premium_by_year` | `array` | Yes | Earned premium for each accident year, in the same order as loss_triangle rows. Used to compute expected loss ratios. Must have the same length as loss_triangle. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ibnr_reserve_calculator",
  "arguments": {
    "loss_triangle": [],
    "premium_by_year": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ibnr_reserve_calculator"`.

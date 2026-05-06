---
skill: unit_economics_sensitivity
category: small_business
description: Applies +/- variation to CAC, LTV, margin, and churn to highlight best/worst case unit economics and breakeven thresholds.
tier: free
inputs: base_cac, base_ltv, base_margin, base_churn, variation_pct
---

# Unit Economics Sensitivity

## Description
Applies +/- variation to CAC, LTV, margin, and churn to highlight best/worst case unit economics and breakeven thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_cac` | `number` | Yes | Baseline customer acquisition cost. |
| `base_ltv` | `number` | Yes | Baseline lifetime value per customer. |
| `base_margin` | `number` | Yes | Gross margin percentage as decimal. |
| `base_churn` | `number` | Yes | Churn rate as decimal. |
| `variation_pct` | `number` | Yes | Sensitivity swing percentage (e.g., 0.2 for +/-20%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "unit_economics_sensitivity",
  "arguments": {
    "base_cac": 0,
    "base_ltv": 0,
    "base_margin": 0,
    "base_churn": 0,
    "variation_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "unit_economics_sensitivity"`.

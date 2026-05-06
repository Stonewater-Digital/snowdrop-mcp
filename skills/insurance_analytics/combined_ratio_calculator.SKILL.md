---
skill: combined_ratio_calculator
category: insurance_analytics
description: Computes combined ratio, underwriting margin, and operating ratio from loss, expense, and investment income ratios. Supports trade and statutory basis.
tier: free
inputs: loss_ratio_pct, expense_ratio_pct
---

# Combined Ratio Calculator

## Description
Computes combined ratio, underwriting margin, and operating ratio from loss, expense, and investment income ratios. Supports trade and statutory basis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loss_ratio_pct` | `number` | Yes | Incurred loss ratio as a percentage (e.g., 65.0 = 65%). Must be >= 0. |
| `expense_ratio_pct` | `number` | Yes | Underwriting expense ratio as a percentage (e.g., 30.0 = 30%). On trade basis: expenses / net written premium. Must be >= 0. |
| `policyholder_dividend_ratio_pct` | `number` | No | Policyholder dividends / earned premium %. Typically 0 for most commercial lines. |
| `investment_income_ratio_pct` | `number` | No | Net investment income / earned premium %. Used to compute operating ratio. Typical range 2–8%. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "combined_ratio_calculator",
  "arguments": {
    "loss_ratio_pct": 0,
    "expense_ratio_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "combined_ratio_calculator"`.

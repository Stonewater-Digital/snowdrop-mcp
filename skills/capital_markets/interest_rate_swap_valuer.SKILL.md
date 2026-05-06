---
skill: interest_rate_swap_valuer
category: capital_markets
description: Computes MTM, PV legs, and DV01 for swaps using provided discount curve.
tier: free
inputs: notional, fixed_rate, floating_rate_current, swap_tenor_remaining_years, position, discount_curve
---

# Interest Rate Swap Valuer

## Description
Computes mark-to-market value, present value of fixed and floating legs, and DV01 for a plain-vanilla interest rate swap using a user-supplied discount curve. Supports pay-fixed and receive-fixed positions across quarterly, semi-annual, and annual payment frequencies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes | Notional principal of the swap (dollars). |
| `fixed_rate` | `number` | Yes | Fixed leg coupon rate as a decimal (e.g. 0.035 for 3.5%). |
| `floating_rate_current` | `number` | Yes | Current floating reference rate as a decimal (e.g. 0.052 for 5.2%). |
| `swap_tenor_remaining_years` | `number` | Yes | Remaining term of the swap in years. |
| `position` | `string` | Yes | "pay_fixed" or "receive_fixed". |
| `discount_curve` | `array` | Yes | List of discount curve points, each with `tenor_years` and `rate` fields. |
| `payment_frequency` | `string` | No | "quarterly", "semi_annual", or "annual" (default: "semi_annual"). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "interest_rate_swap_valuer",
  "arguments": {
    "notional": 50000000,
    "fixed_rate": 0.035,
    "floating_rate_current": 0.052,
    "swap_tenor_remaining_years": 3.5,
    "position": "pay_fixed",
    "discount_curve": [
      {"tenor_years": 1, "rate": 0.048},
      {"tenor_years": 2, "rate": 0.050},
      {"tenor_years": 3, "rate": 0.051},
      {"tenor_years": 5, "rate": 0.053}
    ],
    "payment_frequency": "semi_annual"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_rate_swap_valuer"`.

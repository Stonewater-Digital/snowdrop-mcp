---
skill: interest_rate_swap_valuer
category: capital_markets
description: Computes MTM, PV legs, and DV01 for swaps using provided discount curve.
tier: free
inputs: notional, fixed_rate, floating_rate_current, swap_tenor_remaining_years, position, discount_curve
---

# Interest Rate Swap Valuer

## Description
Computes MTM, PV legs, and DV01 for swaps using provided discount curve.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `fixed_rate` | `number` | Yes |  |
| `floating_rate_current` | `number` | Yes |  |
| `swap_tenor_remaining_years` | `number` | Yes |  |
| `payment_frequency` | `string` | No |  |
| `position` | `string` | Yes |  |
| `discount_curve` | `array` | Yes |  |

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
    "notional": 0,
    "fixed_rate": 0,
    "floating_rate_current": 0,
    "swap_tenor_remaining_years": 0,
    "position": "<position>",
    "discount_curve": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_rate_swap_valuer"`.

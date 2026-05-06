---
skill: liability_driven_optimizer
category: portfolio_construction
description: Matches liability duration/convexity and surplus targets by allocating across asset cash-flow profiles consistent with ERISA and Solvency II liability-driven investing practices.
tier: free
inputs: asset_cashflows, liability_schedule, discount_rate
---

# Liability Driven Optimizer

## Description
Matches liability duration/convexity and surplus targets by allocating across asset cash-flow profiles consistent with ERISA and Solvency II liability-driven investing practices.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_cashflows` | `array` | Yes | List of asset dictionaries each containing name and future cash flows. |
| `liability_schedule` | `array` | Yes | Schedule of liability cash flows with time and amount. |
| `discount_rate` | `number` | Yes | Flat discount rate used for PV calculations (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "liability_driven_optimizer",
  "arguments": {
    "asset_cashflows": [],
    "liability_schedule": [],
    "discount_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "liability_driven_optimizer"`.

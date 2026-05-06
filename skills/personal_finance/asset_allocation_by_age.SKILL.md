---
skill: asset_allocation_by_age
category: personal_finance
description: Applies a modified age-based formula to recommend stock/bond/cash/alt allocations and produces a glide path toward retirement.
tier: free
inputs: age, risk_tolerance, retirement_age, portfolio_value
---

# Asset Allocation By Age

## Description
Applies a modified age-based formula to recommend stock/bond/cash/alt allocations and produces a glide path toward retirement.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `age` | `number` | Yes | Current age of the investor. |
| `risk_tolerance` | `string` | Yes | conservative, moderate, or aggressive. |
| `retirement_age` | `number` | Yes | Target retirement age. |
| `portfolio_value` | `number` | Yes | Total investable assets. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "asset_allocation_by_age",
  "arguments": {
    "age": 0,
    "risk_tolerance": "<risk_tolerance>",
    "retirement_age": 0,
    "portfolio_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_allocation_by_age"`.

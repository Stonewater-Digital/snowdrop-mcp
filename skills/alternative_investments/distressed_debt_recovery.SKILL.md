---
skill: distressed_debt_recovery
category: alternative_investments
description: Waterfalls enterprise value through senior/mezz/equity to compute recoveries and implied returns. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: face_value, purchase_price, enterprise_value, senior_debt, mezzanine_debt, equity_cushion
---

# Distressed Debt Recovery

## Description
Waterfalls enterprise value through senior, mezzanine, and equity tranches to compute recoveries by class and implied return at purchase price. Used for distressed debt underwriting and secondary market pricing. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes | Face value of the debt instrument being analyzed (dollars). |
| `purchase_price` | `number` | Yes | Price paid to acquire the debt (dollars, typically below par). |
| `enterprise_value` | `number` | Yes | Estimated reorganization or liquidation enterprise value (dollars). |
| `senior_debt` | `number` | Yes | Total senior secured debt outstanding (dollars). |
| `mezzanine_debt` | `number` | Yes | Total mezzanine or subordinated debt outstanding (dollars). |
| `equity_cushion` | `number` | Yes | Pre-distress equity value cushion below the subject debt (dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "distressed_debt_recovery",
  "arguments": {
    "face_value": 50000000,
    "purchase_price": 35000000,
    "enterprise_value": 90000000,
    "senior_debt": 60000000,
    "mezzanine_debt": 20000000,
    "equity_cushion": 5000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distressed_debt_recovery"`.

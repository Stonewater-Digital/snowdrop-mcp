---
skill: gift_tax_calculator
category: tax
description: Calculate gift tax liability considering the annual exclusion ($18,000 for 2024), prior gifts, and lifetime exemption ($13.61M for 2024). Tax rate is 40% on amounts exceeding lifetime exemption.
tier: free
inputs: gift_amount
---

# Gift Tax Calculator

## Description
Calculate gift tax liability considering the annual exclusion ($18,000 for 2024), prior gifts, and lifetime exemption ($13.61M for 2024). Tax rate is 40% on amounts exceeding lifetime exemption.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gift_amount` | `number` | Yes | Current gift amount in USD. |
| `prior_year_gifts` | `number` | No | Cumulative taxable gifts from prior years (already applied against lifetime exemption) in USD. |
| `annual_exclusion` | `number` | No | Annual gift tax exclusion amount. |
| `lifetime_exemption` | `number` | No | Unified lifetime gift/estate tax exemption. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gift_tax_calculator",
  "arguments": {
    "gift_amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gift_tax_calculator"`.

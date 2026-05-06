---
skill: fee_drag_calculator
category: fund_admin
description: Estimates net IRR after management fees, performance carry, and other charges. Carry drag is only applied to returns above the hurdle rate.
tier: premium
inputs: gross_irr_pct, management_fee_pct, carry_pct, hurdle_rate_pct, other_fees_bps
---

# Fee Drag Calculator

## Description
Estimates net IRR after management fees, performance carry, and other charges. Carry drag is only applied to returns above the hurdle rate. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| gross_irr_pct | number | Yes | Fund gross IRR before any fees or carry deductions (e.g. 18.5 for 18.5%) |
| management_fee_pct | number | Yes | Annual management fee as a percentage of committed or invested capital (e.g. 2.0 for 2%) |
| carry_pct | number | Yes | GP carried interest percentage applied to returns above the hurdle (e.g. 20.0 for 20%) |
| hurdle_rate_pct | number | No | Preferred return rate that must be cleared before carry applies (default: 8.0) |
| other_fees_bps | number | No | Other fund-level charges expressed in basis points (e.g. admin, audit, legal; default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fee_drag_calculator",
  "arguments": {
    "gross_irr_pct": 18.5,
    "management_fee_pct": 2.0,
    "carry_pct": 20.0,
    "hurdle_rate_pct": 8.0,
    "other_fees_bps": 25.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fee_drag_calculator"`.

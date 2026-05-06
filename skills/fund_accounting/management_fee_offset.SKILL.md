---
skill: management_fee_offset
category: fund_accounting
description: Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs.
tier: premium
inputs: none
---

# Management Fee Offset

## Description
Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs. Net fee is floored at zero (cannot be negative). (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "management_fee_offset",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "management_fee_offset"`.

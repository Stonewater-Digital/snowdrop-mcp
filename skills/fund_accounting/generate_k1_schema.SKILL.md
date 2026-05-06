---
skill: generate_k1_schema
category: fund_accounting
description: Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: partner_id, fund_id, tax_year, allocations
---

# Generate K1 Schema

## Description
Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items. Produces a machine-readable K-1 payload covering ordinary income, capital gains, Section 199A deductions, and other pass-through items for LP tax filing. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `partner_id` | `string` | Yes | Unique LP/partner identifier. |
| `fund_id` | `string` | Yes | Fund entity identifier. |
| `tax_year` | `integer` | Yes | Tax year for which K-1 is generated (e.g. 2024). |
| `allocations` | `object` | Yes | Dict of K-1 line items to amounts, e.g. `{"ordinary_income": 12500.00, "long_term_capital_gain": 45000.00}`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "generate_k1_schema",
  "arguments": {
    "partner_id": "LP-0042",
    "fund_id": "FUND-001",
    "tax_year": 2024,
    "allocations": {
      "ordinary_income": 12500.00,
      "long_term_capital_gain": 45000.00,
      "section_199a_deduction": 2500.00
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "generate_k1_schema"`.

---
skill: physical_storage_cost_calculator
category: commodities
description: Quantifies the full carry cost of holding physical commodity inventory: warehouse/storage fees, insurance, and financing cost over a given horizon. Returns total cost, per-unit cost, and implied break-even basis appreciation.
tier: free
inputs: inventory_units, unit_value, storage_fee_per_unit_month
---

# Physical Storage Cost Calculator

## Description
Quantifies the full carry cost of holding physical commodity inventory: warehouse/storage fees, insurance, and financing cost over a given horizon. Returns total cost, per-unit cost, and implied break-even basis appreciation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `inventory_units` | `number` | Yes | Number of units in inventory (must be > 0). |
| `unit_value` | `number` | Yes | Current market value per unit (must be > 0). |
| `storage_fee_per_unit_month` | `number` | Yes | Flat storage fee per unit per month in currency terms. |
| `insurance_pct_annual` | `number` | No | Annual insurance cost as % of inventory value. Defaults to 0.5%. |
| `financing_rate_pct_annual` | `number` | No | Annual financing (opportunity) cost as % of inventory value. Defaults to 6%. |
| `months` | `number` | No | Storage horizon in months (must be > 0). Defaults to 3. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "physical_storage_cost_calculator",
  "arguments": {
    "inventory_units": 0,
    "unit_value": 0,
    "storage_fee_per_unit_month": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "physical_storage_cost_calculator"`.

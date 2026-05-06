---
skill: roi_annotator
category: fund_accounting
description: Enriches ledger transactions with qualitative ROI commentary. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: transaction
---

# Roi Annotator

## Description
Enriches ledger transactions with qualitative ROI commentary. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transaction` | `object` | Yes | Ledger transaction object with fields including `id`, `date`, `amount`, `category`, `description`, and optionally `cost_basis` and `proceeds` for investment-type entries. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "roi_annotator",
  "arguments": {
    "transaction": {
      "id": "txn_20260101_001",
      "date": "2026-01-01",
      "amount": 3200000,
      "category": "distribution",
      "description": "Exit proceeds from Portfolio Co Gamma (M&A)",
      "cost_basis": 1500000,
      "proceeds": 4700000
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "roi_annotator"`.

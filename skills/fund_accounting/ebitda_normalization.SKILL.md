---
skill: ebitda_normalization
category: fund_accounting
description: Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: reported_ebitda, adjustments
---

# Ebitda Normalization

## Description
Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `reported_ebitda` | `number` | Yes | As-reported EBITDA figure from the target company's financials in dollars. |
| `adjustments` | `array` | Yes | List of adjustment objects, each with `description`, `category` (e.g. `"one_time"`, `"non_cash"`, `"run_rate"`), and `amount` (positive = add-back, negative = reduction). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ebitda_normalization",
  "arguments": {
    "reported_ebitda": 8500000,
    "adjustments": [
      {"description": "Founder salary above market", "category": "run_rate", "amount": 350000},
      {"description": "One-time restructuring charge", "category": "one_time", "amount": 600000},
      {"description": "Non-cash stock comp expense", "category": "non_cash", "amount": 200000},
      {"description": "Discontinued product line losses", "category": "one_time", "amount": 150000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ebitda_normalization"`.

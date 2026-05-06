---
skill: schedule_d_8949_generator
category: compliance
description: Classifies transactions into short- and long-term gains for tax filing. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: transactions
---

# Schedule D 8949 Generator

## Description
Classifies transactions into short- and long-term gains for tax filing. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transactions` | `array[object]` | Yes | List of capital asset transactions each with date acquired, date sold, proceeds, cost basis, and asset description for Schedule D/Form 8949 classification |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "schedule_d_8949_generator",
  "arguments": {
    "transactions": [
      {
        "asset": "BTC",
        "date_acquired": "2024-01-15",
        "date_sold": "2026-03-10",
        "proceeds": 95000.00,
        "cost_basis": 42000.00
      }
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "schedule_d_8949_generator"`.

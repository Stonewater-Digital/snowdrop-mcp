---
skill: recallable_distribution_tracker
category: fund_admin
description: Summarizes recallable vs permanent distributions per LP. Recallable distributions can be called back by the GP for follow-on investments.
tier: premium
inputs: distributions
---

# Recallable Distribution Tracker

## Description
Summarizes recallable vs permanent distributions per LP. Recallable distributions can be called back by the GP for follow-on investments. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| distributions | array | Yes | List of distribution event objects, each with `lp_name` (string), `amount` (number), `recallable` (boolean), and `date` (string ISO8601) fields |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recallable_distribution_tracker",
  "arguments": {
    "distributions": [
      {"lp_name": "Maple Leaf Pension", "amount": 500000, "recallable": true, "date": "2023-06-30"},
      {"lp_name": "Maple Leaf Pension", "amount": 1200000, "recallable": false, "date": "2024-03-15"},
      {"lp_name": "Sunrise Endowment", "amount": 300000, "recallable": true, "date": "2023-06-30"},
      {"lp_name": "Sunrise Endowment", "amount": 800000, "recallable": false, "date": "2024-03-15"}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recallable_distribution_tracker"`.

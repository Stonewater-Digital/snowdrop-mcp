---
skill: repo_implied_rate
category: fixed_income_analytics
description: Derives the implied repurchase (repo) rate from the Treasury cash-futures basis, adjusting for coupons and accrued interest. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Repo Implied Rate

## Description
Derives the implied repurchase (repo) rate from the Treasury cash-futures basis, adjusting for coupons and accrued interest. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "repo_implied_rate",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "repo_implied_rate"`.

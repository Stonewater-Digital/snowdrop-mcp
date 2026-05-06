---
skill: lp_commitment_tracker
category: fund_admin
description: Tracks commitment, called capital, and remaining unfunded balance for each LP. Reports fund-level call percentage and identifies LPs with zero unfunded capacity.
tier: premium
inputs: lp_positions
---

# Lp Commitment Tracker

## Description
Tracks commitment, called capital, and remaining unfunded balance for each LP. Reports fund-level call percentage and identifies LPs with zero unfunded capacity. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| lp_positions | array | Yes | List of LP position objects, each with `lp_name` (string), `commitment` (number), and `called` (number) representing total commitment and capital drawn to date |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lp_commitment_tracker",
  "arguments": {
    "lp_positions": [
      {"lp_name": "Midwest Teachers Retirement", "commitment": 25000000, "called": 18750000},
      {"lp_name": "Harbor View Endowment", "commitment": 10000000, "called": 7500000},
      {"lp_name": "Redwood Family Office", "commitment": 5000000, "called": 5000000},
      {"lp_name": "Apex Insurance Group", "commitment": 15000000, "called": 9000000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lp_commitment_tracker"`.

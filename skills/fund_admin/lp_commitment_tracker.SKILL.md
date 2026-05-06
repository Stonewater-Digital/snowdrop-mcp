---
skill: lp_commitment_tracker
category: fund_admin
description: Tracks commitment, called capital, and remaining unfunded balance for each LP. Reports fund-level call percentage and identifies LPs with zero unfunded capacity.
tier: premium
inputs: none
---

# Lp Commitment Tracker

## Description
Tracks commitment, called capital, and remaining unfunded balance for each LP. Reports fund-level call percentage and identifies LPs with zero unfunded capacity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "lp_commitment_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lp_commitment_tracker"`.

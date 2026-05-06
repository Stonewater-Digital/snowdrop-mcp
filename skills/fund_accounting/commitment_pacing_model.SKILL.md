---
skill: commitment_pacing_model
category: fund_accounting
description: Suggests annual commitments and overcommitment ratios for PE allocation targets. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Commitment Pacing Model

## Description
Suggests annual commitments and overcommitment ratios for PE allocation targets. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "commitment_pacing_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commitment_pacing_model"`.

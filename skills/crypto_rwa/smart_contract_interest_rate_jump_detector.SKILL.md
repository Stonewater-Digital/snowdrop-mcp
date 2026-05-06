---
skill: smart_contract_interest_rate_jump_detector
category: crypto_rwa
description: Stress-tests rate models for discontinuities following governance votes.
tier: free
inputs: none
---

# Smart Contract Interest Rate Jump Detector

## Description
Stress-tests rate models for discontinuities following governance votes.

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
  "tool": "smart_contract_interest_rate_jump_detector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_interest_rate_jump_detector"`.

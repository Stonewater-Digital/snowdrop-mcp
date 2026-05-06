---
skill: smart_contract_liquidity_sink_detector
category: crypto_rwa
description: Detects pools where withdrawals can be blocked via hooks or sticky fee logic.
tier: free
inputs: none
---

# Smart Contract Liquidity Sink Detector

## Description
Detects pools where withdrawals can be blocked via hooks or sticky fee logic.

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
  "tool": "smart_contract_liquidity_sink_detector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_liquidity_sink_detector"`.

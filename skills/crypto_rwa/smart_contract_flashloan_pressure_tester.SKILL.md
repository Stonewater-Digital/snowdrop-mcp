---
skill: smart_contract_flashloan_pressure_tester
category: crypto_rwa
description: Runs deterministic flash-loan scenarios to measure collateral buffers and slippage thresholds.
tier: free
inputs: none
---

# Smart Contract Flashloan Pressure Tester

## Description
Runs deterministic flash-loan scenarios to measure collateral buffers and slippage thresholds.

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
  "tool": "smart_contract_flashloan_pressure_tester",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_flashloan_pressure_tester"`.

---
skill: smart_contract_flashloan_pressure_tester
category: crypto_rwa
description: Runs deterministic flash-loan scenarios to measure collateral buffers and slippage thresholds.
tier: free
inputs: payload
---

# Smart Contract Flashloan Pressure Tester

## Description
Runs deterministic flash-loan scenarios to measure collateral buffers and slippage thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_flashloan_pressure_tester",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_flashloan_pressure_tester"`.

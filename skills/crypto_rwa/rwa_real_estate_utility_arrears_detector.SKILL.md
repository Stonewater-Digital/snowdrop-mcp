---
skill: rwa_real_estate_utility_arrears_detector
category: crypto_rwa
description: Flags properties with unpaid utility balances or liens impacting collateral quality.
tier: free
inputs: payload
---

# Rwa Real Estate Utility Arrears Detector

## Description
Flags properties with unpaid utility balances or liens impacting collateral quality.

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
  "tool": "rwa_real_estate_utility_arrears_detector",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_utility_arrears_detector"`.

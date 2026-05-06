---
skill: rwa_real_estate_utility_arrears_detector
category: crypto_rwa
description: Flags properties with unpaid utility balances or liens impacting collateral quality.
tier: free
inputs: none
---

# Rwa Real Estate Utility Arrears Detector

## Description
Flags properties with unpaid utility balances or liens impacting collateral quality.

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
  "tool": "rwa_real_estate_utility_arrears_detector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_utility_arrears_detector"`.

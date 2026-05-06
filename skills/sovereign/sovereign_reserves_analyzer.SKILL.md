---
skill: sovereign_reserves_analyzer
category: sovereign
description: Analyzes sovereign reserve composition (fiat/gold/digital) and compares against IMF adequacy metrics.
tier: free
inputs: reserves
---

# Sovereign Reserves Analyzer

## Description
Analyzes sovereign reserve composition (fiat/gold/digital) and compares against IMF adequacy metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `reserves` | `object` | Yes | Reserve holdings breakdown |
| `imports_monthly` | `number` | No | Monthly import bill in USD (optional) |
| `sdr_usd_rate` | `number` | No | SDR to USD conversion rate (default: 1.33) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sovereign_reserves_analyzer",
  "arguments": {
    "reserves": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sovereign_reserves_analyzer"`.

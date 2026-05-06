---
skill: exchange_netflow_analyzer
category: blockchain_analytics
description: Summarizes exchange wallet activity for accumulation/distribution signal generation.
tier: free
inputs: inflows, outflows
---

# Exchange Netflow Analyzer

## Description
Summarizes exchange wallet activity for accumulation/distribution signal generation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `inflows` | `array` | Yes | List of inflow records {timestamp, amount}. Amounts can be raw tokens. |
| `outflows` | `array` | Yes | List of outflow records {timestamp, amount}. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "exchange_netflow_analyzer",
  "arguments": {
    "inflows": [],
    "outflows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exchange_netflow_analyzer"`.

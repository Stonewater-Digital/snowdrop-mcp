---
skill: protocol_revenue_analyzer
category: smart_contracts
description: Calculates revenue per product and annualizes it to monitor concentration risk.
tier: free
inputs: fee_streams
---

# Protocol Revenue Analyzer

## Description
Calculates revenue per product and annualizes it to monitor concentration risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fee_streams` | `array` | Yes | Per-product fee streams. |
| `annualization_factor` | `number` | No | Multiplier to annualize the provided period |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "protocol_revenue_analyzer",
  "arguments": {
    "fee_streams": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "protocol_revenue_analyzer"`.

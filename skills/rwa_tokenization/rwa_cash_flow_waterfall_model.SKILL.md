---
skill: rwa_cash_flow_waterfall_model
category: rwa_tokenization
description: Allocates tokenized asset cash flows across tranches based on priority or share percentages.
tier: free
inputs: cash_flows, tranches
---

# Rwa Cash Flow Waterfall Model

## Description
Allocates tokenized asset cash flows across tranches based on priority or share percentages.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_flows` | `array` | Yes | Per-period available cash |
| `tranches` | `array` | Yes | Waterfall share percentages |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_cash_flow_waterfall_model",
  "arguments": {
    "cash_flows": [],
    "tranches": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_cash_flow_waterfall_model"`.

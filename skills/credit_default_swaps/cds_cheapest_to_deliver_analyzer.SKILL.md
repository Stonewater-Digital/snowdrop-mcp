---
skill: cds_cheapest_to_deliver_analyzer
category: credit_default_swaps
description: Identifies the cheapest deliverable bond and expected auction recovery.
tier: free
inputs: deliverables
---

# Cds Cheapest To Deliver Analyzer

## Description
Identifies the cheapest deliverable bond and expected auction recovery.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `deliverables` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_cheapest_to_deliver_analyzer",
  "arguments": {
    "deliverables": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_cheapest_to_deliver_analyzer"`.

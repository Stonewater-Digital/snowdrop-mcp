---
skill: sanctions_network_monitor
category: compliance
description: Cross-check wallet exposures against sanctions feeds and return flagged entities.
tier: free
inputs: exposures
---

# Sanctions Network Monitor

## Description
Cross-check wallet exposures against sanctions feeds and return flagged entities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | List of exposures containing address, chain, and amount_usd. |
| `chains` | `array` | No | Optional list of chains to query in the sanctions feed. |
| `sources` | `array` | No | Sanctions sources to query (e.g., ofac, fatf, sample). |
| `alert_threshold_usd` | `number` | No | Trigger Thunder escalation when flagged exposure exceeds this USD amount. |
| `notify_thunder` | `boolean` | No | Send Thunder alert when threshold breached. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sanctions_network_monitor",
  "arguments": {
    "exposures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sanctions_network_monitor"`.

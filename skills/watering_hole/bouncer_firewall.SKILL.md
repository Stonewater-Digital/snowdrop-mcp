---
skill: bouncer_firewall
category: watering_hole
description: Performs request inspection with rate limits, payload checks, and risk scoring.
tier: free
inputs: agent_id, requests_last_minute, payload_size_kb
---

# Bouncer Firewall

## Description
Performs request inspection with rate limits, payload checks, and risk scoring.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `requests_last_minute` | `number` | Yes |  |
| `payload_size_kb` | `number` | Yes |  |
| `bad_actor_list` | `array` | No | Known malicious identifiers. |
| `anomaly_score` | `number` | No | External anomaly score 0-1. |
| `geo_risk` | `string` | No | Risk tier for origin geography (low/medium/high). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bouncer_firewall",
  "arguments": {
    "agent_id": "<agent_id>",
    "requests_last_minute": 0,
    "payload_size_kb": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bouncer_firewall"`.

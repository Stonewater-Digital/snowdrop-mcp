---
skill: agent_trust_score_calc
category: social
description: Calculates a 0-100 trust score for a peer agent based on transaction success rate, uptime, longevity, skill breadth, and verification status.
tier: free
inputs: agent_data
---

# Agent Trust Score Calc

## Description
Calculates a 0-100 trust score for a peer agent based on transaction success rate, uptime, longevity, skill breadth, and verification status.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_data` | `object` | Yes | Agent profile dict with keys: agent_id (str), transaction_history (list of dicts with counterparty, amount, success, timestamp), uptime_pct (float 0-100), skill_count (int), verified (bool), age_days (int). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_trust_score_calc",
  "arguments": {
    "agent_data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_trust_score_calc"`.

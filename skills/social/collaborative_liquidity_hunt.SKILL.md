---
skill: collaborative_liquidity_hunt
category: social
description: Validates whether a group of trusted agents has sufficient combined capital to exploit a thin-market spread opportunity and produces a pro-rata allocation plan.
tier: free
inputs: opportunity, participants
---

# Collaborative Liquidity Hunt

## Description
Validates whether a group of trusted agents has sufficient combined capital to exploit a thin-market spread opportunity and produces a pro-rata allocation plan.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `opportunity` | `object` | Yes | Dict with keys: asset (str), market (str), current_spread_bps (float), estimated_size (float), min_participants (int). |
| `participants` | `array` | Yes | List of dicts with agent_id (str), available_capital (float), trust_score (float 0-100). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "collaborative_liquidity_hunt",
  "arguments": {
    "opportunity": {},
    "participants": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "collaborative_liquidity_hunt"`.

---
skill: rwa_redemption_mechanics_analyzer
category: rwa_tokenization
description: Evaluates redemption policies including frequency, notice, and penalties for tokenized RWAs.
tier: free
inputs: redemption_frequency_days, notice_period_days
---

# Rwa Redemption Mechanics Analyzer

## Description
Evaluates redemption policies including frequency, notice, and penalties for tokenized RWAs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `redemption_frequency_days` | `number` | Yes | How often redemptions are allowed |
| `notice_period_days` | `number` | Yes | Required notice before redemption |
| `penalty_pct` | `number` | No | Penalty percent for early exit |
| `liquidity_buffer_pct` | `number` | No | Portfolio liquidity buffer percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_redemption_mechanics_analyzer",
  "arguments": {
    "redemption_frequency_days": 0,
    "notice_period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_redemption_mechanics_analyzer"`.

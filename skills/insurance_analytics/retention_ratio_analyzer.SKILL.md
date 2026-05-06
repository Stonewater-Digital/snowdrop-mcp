---
skill: retention_ratio_analyzer
category: insurance_analytics
description: Analyzes retention and cession ratios with net loss ratio and reinsurance leverage metrics. Measures how much premium and loss exposure is retained vs.
tier: free
inputs: gross_written_premium, ceded_premium, gross_losses, ceded_losses
---

# Retention Ratio Analyzer

## Description
Analyzes retention and cession ratios with net loss ratio and reinsurance leverage metrics. Measures how much premium and loss exposure is retained vs. ceded and evaluates reinsurance program efficiency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_written_premium` | `number` | Yes | Total gross written premium before any cessions. Must be > 0. |
| `ceded_premium` | `number` | Yes | Premium ceded to reinsurers. Must be >= 0 and <= gross_written_premium. |
| `gross_losses` | `number` | Yes | Total gross incurred losses for the period. Must be >= 0. |
| `ceded_losses` | `number` | Yes | Losses recoverable from reinsurers. Must be >= 0 and <= gross_losses. |
| `ceding_commission` | `number` | No | Ceding commissions received from reinsurers (reduces net expenses). Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "retention_ratio_analyzer",
  "arguments": {
    "gross_written_premium": 0,
    "ceded_premium": 0,
    "gross_losses": 0,
    "ceded_losses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "retention_ratio_analyzer"`.

---
skill: net_operating_loss_shield_optimizer
category: advanced_equities_spinoffs_restructuring
description: Maps NOL usage scenarios to protect tax assets post-transaction.
tier: free
inputs: none
---

# Net Operating Loss Shield Optimizer

## Description
Maps NOL usage scenarios to protect tax assets post-transaction.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tickers` | `array` | No | Tickers or identifiers relevant to the analysis focus. |
| `lookback_days` | `integer` | No | Historical window (days) for synthetic / free-data calculations. |
| `analysis_notes` | `string` | No | Optional qualitative context to embed in the response. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_operating_loss_shield_optimizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_operating_loss_shield_optimizer"`.

---
skill: reg_fd_8k_alert_router
category: event_driven_trades
description: Streams fresh 8-Ks, tags material language, and suggests contextual playbooks.
tier: free
inputs: none
---

# Reg Fd 8k Alert Router

## Description
Streams fresh 8-Ks, tags material language, and suggests contextual playbooks.

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
  "tool": "reg_fd_8k_alert_router",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reg_fd_8k_alert_router"`.

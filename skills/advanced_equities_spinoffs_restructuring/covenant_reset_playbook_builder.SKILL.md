---
skill: covenant_reset_playbook_builder
category: advanced_equities_spinoffs_restructuring
description: Outlines likely covenant reset packages from precedent negotiations.
tier: free
inputs: none
---

# Covenant Reset Playbook Builder

## Description
Outlines likely covenant reset packages from precedent negotiations.

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
  "tool": "covenant_reset_playbook_builder",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "covenant_reset_playbook_builder"`.

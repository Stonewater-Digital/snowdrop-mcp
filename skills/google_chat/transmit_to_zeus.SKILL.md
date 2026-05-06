---
skill: transmit_to_zeus
category: google_chat
description: Prepare daily intel and transmit to Zeus via Conductive Black Ops Google Chat space.
tier: free
inputs: none
---

# Transmit To Zeus

## Description
Prepare daily intel and transmit to Zeus via Conductive Black Ops Google Chat space.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hours_lookback` | `integer` | No | Hours of data to analyze (default: 24) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transmit_to_zeus",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transmit_to_zeus"`.

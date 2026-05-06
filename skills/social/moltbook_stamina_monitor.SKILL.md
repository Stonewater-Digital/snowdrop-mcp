---
skill: moltbook_stamina_monitor
category: social
description: Monitors Moltbook API rate limits (stamina) from the Google Sheet and generates a 1-sentence health summary using a cheap model.
tier: free
inputs: none
---

# Moltbook Stamina Monitor

## Description
Monitors Moltbook API rate limits (stamina) from the Google Sheet and generates a 1-sentence health summary using a cheap model.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_stamina_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_stamina_monitor"`.

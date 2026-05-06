---
skill: agentic_white_label_portal
category: technical
description: Generates a white-label portal configuration for a Snowdrop client. Filters the master skill registry to only those skills the client is authorised to access, applies branding overrides, assigns rate limits based on the daily USD transaction cap, and returns a complete portal configuration object ready for front-end consumption.
tier: premium
inputs: none
---

# Agentic White Label Portal

## Description
Generates a white-label portal configuration for a Snowdrop client. Filters the master skill registry to only those skills the client is authorised to access, applies branding overrides, assigns rate limits based on the daily USD transaction cap, and returns a complete portal configuration object ready for front-end consumption. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "agentic_white_label_portal",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agentic_white_label_portal"`.

---
skill: pitch_deck_generator
category: investor_relations
description: Creates slide-by-slide pitch content for Snowdrop fundraising narratives. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Pitch Deck Generator

## Description
Creates slide-by-slide pitch content for Snowdrop fundraising narratives. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "pitch_deck_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pitch_deck_generator"`.

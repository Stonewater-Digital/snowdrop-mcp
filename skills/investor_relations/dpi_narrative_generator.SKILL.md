---
skill: dpi_narrative_generator
category: investor_relations
description: Converts DPI metrics into LP-facing narrative with severity tiers when below target. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Dpi Narrative Generator

## Description
Converts DPI metrics into LP-facing narrative with severity tiers when below target. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "dpi_narrative_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dpi_narrative_generator"`.

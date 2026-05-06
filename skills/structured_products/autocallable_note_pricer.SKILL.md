---
skill: autocallable_note_pricer
category: structured_products
description: Simulates geometric Brownian paths to estimate autocall probabilities, expected life, and fair price for a Phoenix/autocallable note. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Autocallable Note Pricer

## Description
Simulates geometric Brownian paths to estimate autocall probabilities, expected life, and fair price for a Phoenix/autocallable note. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "autocallable_note_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "autocallable_note_pricer"`.

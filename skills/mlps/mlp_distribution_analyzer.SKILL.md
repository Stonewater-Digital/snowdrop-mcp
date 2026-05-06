---
skill: mlp_distribution_analyzer
category: mlps
description: Calculates DCF coverage, leverage, and GP take for MLP distributions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Distribution Analyzer

## Description
Calculates DCF coverage, leverage, and GP take for MLP distributions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_distribution_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_distribution_analyzer"`.

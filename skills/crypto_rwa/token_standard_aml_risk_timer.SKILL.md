---
skill: token_standard_aml_risk_timer
category: crypto_rwa
description: Applies dynamic AML cooldown timers when risk scores breach thresholds.
tier: free
inputs: none
---

# Token Standard Aml Risk Timer

## Description
Applies dynamic AML cooldown timers when risk scores breach thresholds.

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
  "tool": "token_standard_aml_risk_timer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_aml_risk_timer"`.

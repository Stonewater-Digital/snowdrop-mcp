---
skill: token_standard_mica_utility_token_guardrail
category: crypto_rwa
description: Checks MiCA utility token criteria to ensure consumer disclosures are adequate.
tier: free
inputs: none
---

# Token Standard Mica Utility Token Guardrail

## Description
Checks MiCA utility token criteria to ensure consumer disclosures are adequate.

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
  "tool": "token_standard_mica_utility_token_guardrail",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_mica_utility_token_guardrail"`.

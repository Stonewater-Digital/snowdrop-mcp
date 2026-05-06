---
skill: sec_form_pf_compiler
category: compliance
description: Compiles SEC Form PF data for private fund advisers under Dodd-Frank Act Section 404 and SEC Rule 204(b)-1. Determines Large Adviser classification, filing frequency, and generates the structured Form PF JSON payload for PFRD submission.
tier: premium
inputs: none
---

# Sec Form Pf Compiler

## Description
Compiles SEC Form PF data for private fund advisers under Dodd-Frank Act Section 404 and SEC Rule 204(b)-1. Determines Large Adviser classification, filing frequency, and generates the structured Form PF JSON payload for PFRD submission. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "sec_form_pf_compiler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sec_form_pf_compiler"`.

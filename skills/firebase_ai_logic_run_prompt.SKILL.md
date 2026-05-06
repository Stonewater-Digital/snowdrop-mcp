---
skill: firebase_ai_logic_run_prompt
category: root
description: Execute a Firebase AI Logic prompt template with provided variables. Returns the model's text response.
tier: free
inputs: none
---

# Firebase Ai Logic Run Prompt

## Description
Execute a Firebase AI Logic prompt template with provided variables. Returns the model's text response.

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
  "tool": "firebase_ai_logic_run_prompt",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_ai_logic_run_prompt"`.

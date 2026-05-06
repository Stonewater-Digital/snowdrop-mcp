---
skill: fastapi_to_mcp_wrapper
category: technical
description: Generate MCP-compliant TOOL_META dict and Python wrapper function code from a function name, docstring, and parameter list.
tier: free
inputs: function_name, function_docstring, parameters, return_type
---

# Fastapi To Mcp Wrapper

## Description
Generate MCP-compliant TOOL_META dict and Python wrapper function code from a function name, docstring, and parameter list.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `function_name` | `string` | Yes | The snake_case name of the Python function to wrap. |
| `function_docstring` | `string` | Yes | The function's docstring describing what it does. |
| `parameters` | `array` | Yes | List of parameter dicts, each with: name, type, required (bool), description. |
| `return_type` | `string` | Yes | The Python return type annotation as a string (e.g. 'dict', 'list', 'str'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fastapi_to_mcp_wrapper",
  "arguments": {
    "function_name": "<function_name>",
    "function_docstring": "<function_docstring>",
    "parameters": [],
    "return_type": "<return_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fastapi_to_mcp_wrapper"`.

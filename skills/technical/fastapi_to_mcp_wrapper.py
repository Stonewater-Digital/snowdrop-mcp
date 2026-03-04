"""
Executive Summary: Generate MCP-compliant TOOL_META dicts and wrapper function code from Python function signatures and docstrings.
Inputs: function_name (str), function_docstring (str), parameters (list of dicts), return_type (str)
Outputs: tool_meta (dict), wrapper_code (str), registration_snippet (str)
MCP Tool Name: fastapi_to_mcp_wrapper
"""
import os
import logging
import textwrap
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fastapi_to_mcp_wrapper",
    "description": "Generate MCP-compliant TOOL_META dict and Python wrapper function code from a function name, docstring, and parameter list.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "function_name": {
                "type": "string",
                "description": "The snake_case name of the Python function to wrap."
            },
            "function_docstring": {
                "type": "string",
                "description": "The function's docstring describing what it does."
            },
            "parameters": {
                "type": "array",
                "description": "List of parameter dicts, each with: name, type, required (bool), description.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "required": {"type": "boolean"},
                        "description": {"type": "string"}
                    },
                    "required": ["name", "type", "required", "description"]
                }
            },
            "return_type": {
                "type": "string",
                "description": "The Python return type annotation as a string (e.g. 'dict', 'list', 'str')."
            }
        },
        "required": ["function_name", "function_docstring", "parameters", "return_type"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "tool_meta": {"type": "object"},
            "wrapper_code": {"type": "string"},
            "registration_snippet": {"type": "string"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["tool_meta", "wrapper_code", "registration_snippet", "status", "timestamp"]
    }
}

# Python type → JSON Schema type mapping
_PY_TO_JSON_TYPE: dict[str, str] = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
    "Any": "object",
    "None": "null",
    "bytes": "string",
}

# Return type → JSON Schema output property structure
_RETURN_SCHEMA_TEMPLATES: dict[str, dict] = {
    "dict": {"type": "object", "description": "Returned dict result."},
    "list": {"type": "array", "description": "Returned list result.", "items": {"type": "object"}},
    "str": {"type": "string", "description": "Returned string result."},
    "int": {"type": "integer", "description": "Returned integer result."},
    "float": {"type": "number", "description": "Returned float result."},
    "bool": {"type": "boolean", "description": "Returned boolean result."},
}


def _py_type_to_json(py_type: str) -> str:
    """Map a Python type annotation string to a JSON Schema type string.

    Args:
        py_type: Python type annotation (e.g. 'str', 'int', 'list').

    Returns:
        JSON Schema type string (e.g. 'string', 'integer', 'array').
    """
    clean = py_type.strip().split("[")[0].split("|")[0].strip()
    return _PY_TO_JSON_TYPE.get(clean, "string")


def _build_tool_meta(
    function_name: str,
    description: str,
    parameters: list[dict],
    return_type: str,
) -> dict:
    """Build an MCP-compliant TOOL_META dict.

    Args:
        function_name: Snake_case function name.
        description: Human-readable description of the function.
        parameters: List of parameter spec dicts.
        return_type: Python return type string.

    Returns:
        TOOL_META dict conforming to MCP tool registration format.
    """
    properties: dict[str, Any] = {}
    required: list[str] = []

    for param in parameters:
        json_type = _py_type_to_json(param["type"])
        prop: dict[str, Any] = {
            "type": json_type,
            "description": param.get("description", ""),
        }
        if json_type == "array":
            prop["items"] = {"type": "object"}
        properties[param["name"]] = prop
        if param.get("required", False):
            required.append(param["name"])

    # Build output schema
    output_template = _RETURN_SCHEMA_TEMPLATES.get(return_type.strip(), {"type": "object"})
    output_schema = {
        "type": "object",
        "properties": {
            "result": output_template,
            "status": {"type": "string", "enum": ["success", "error"]},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    }

    return {
        "name": function_name,
        "description": description.strip(),
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
        "outputSchema": output_schema,
    }


def _build_wrapper_code(
    function_name: str,
    description: str,
    parameters: list[dict],
    return_type: str,
) -> str:
    """Generate MCP-compliant wrapper function source code as a string.

    Args:
        function_name: Snake_case function name.
        description: Human-readable description.
        parameters: List of parameter spec dicts.
        return_type: Python return type string.

    Returns:
        Python source code string for the MCP wrapper function.
    """
    # Build parameter signature
    param_parts = []
    for p in parameters:
        py_type = p["type"]
        if p.get("required", False):
            param_parts.append(f"{p['name']}: {py_type}")
        else:
            default = '""' if py_type == "str" else ("None" if py_type in ("list", "dict") else "None")
            param_parts.append(f"{p['name']}: {py_type} = {default}")

    sig = ", ".join(param_parts)

    # Build kwargs pass-through
    kwarg_lines = "\n        ".join([f'"{p["name"]}": {p["name"]},' for p in parameters])

    code = textwrap.dedent(f'''
        def {function_name}({sig}) -> dict:
            """MCP wrapper: {description.strip()}

            This function is auto-generated by fastapi_to_mcp_wrapper.
            It wraps the underlying implementation and enforces MCP output schema.

            Returns:
                MCP-compliant dict with status, result, and timestamp fields.
            """
            import logging
            from datetime import datetime, timezone
            _logger = logging.getLogger("snowdrop.skills")

            try:
                kwargs = {{
                    {kwarg_lines}
                }}
                # Call the underlying implementation here:
                result = _impl_{function_name}(**kwargs)

                return {{
                    "status": "success",
                    "result": result,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }}
            except Exception as e:
                _logger.error(f"{function_name} failed: {{e}}")
                return {{
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }}
    ''').strip()

    return code


def _build_registration_snippet(function_name: str) -> str:
    """Generate the MCP tool registration snippet for mcp_server.py.

    Args:
        function_name: Snake_case function name.

    Returns:
        Python source code snippet for registering the tool with an MCP server.
    """
    snippet = textwrap.dedent(f'''
        # In your MCP server (e.g. mcp_server.py), add:
        from skills.technical.{function_name} import TOOL_META as {function_name.upper()}_META
        from skills.technical.{function_name} import {function_name}

        # Register via JSON-RPC tools/list response:
        REGISTERED_TOOLS["{function_name}"] = {{
            "meta": {function_name.upper()}_META,
            "handler": {function_name},
        }}

        # Handle tool/call:
        @app.post("/tools/call")
        async def call_tool(request: ToolCallRequest):
            if request.name == "{function_name}":
                result = {function_name}(**request.arguments)
                return {{"result": result}}
    ''').strip()

    return snippet


def fastapi_to_mcp_wrapper(
    function_name: str,
    function_docstring: str,
    parameters: list[dict],
    return_type: str,
) -> dict:
    """Generate MCP TOOL_META, wrapper code, and registration snippet for a Python function.

    Converts a Python function signature into all artifacts needed for MCP tool
    registration: a TOOL_META dict (with JSON Schema input/output), a wrapper
    function that enforces MCP output format, and a registration snippet for
    mcp_server.py integration.

    Args:
        function_name: The snake_case name of the target function.
        function_docstring: The function's docstring (used as MCP description).
        parameters: List of parameter dicts, each with: name, type, required (bool), description.
        return_type: Python return type annotation string (e.g. 'dict', 'list').

    Returns:
        A dict with keys:
            - tool_meta (dict): MCP-compliant TOOL_META dict.
            - wrapper_code (str): Generated Python wrapper function source code.
            - registration_snippet (str): MCP server registration code snippet.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not function_name:
            raise ValueError("function_name cannot be empty.")
        if not function_name.replace("_", "").isalnum():
            raise ValueError(f"function_name must be alphanumeric + underscores, got '{function_name}'.")
        if not isinstance(parameters, list):
            raise TypeError(f"parameters must be a list, got {type(parameters).__name__}.")

        # Validate each parameter entry
        required_param_fields = {"name", "type", "required", "description"}
        for idx, param in enumerate(parameters):
            missing = required_param_fields - set(param.keys())
            if missing:
                raise ValueError(f"Parameter at index {idx} missing fields: {missing}.")

        description = function_docstring.strip() or f"MCP tool wrapping {function_name}."

        tool_meta = _build_tool_meta(function_name, description, parameters, return_type)
        wrapper_code = _build_wrapper_code(function_name, description, parameters, return_type)
        registration_snippet = _build_registration_snippet(function_name)

        return {
            "status": "success",
            "tool_meta": tool_meta,
            "wrapper_code": wrapper_code,
            "registration_snippet": registration_snippet,
            "parameter_count": len(parameters),
            "return_type": return_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"fastapi_to_mcp_wrapper failed: {e}")
        _log_lesson(f"fastapi_to_mcp_wrapper: {e}")
        return {
            "status": "error",
            "error": str(e),
            "tool_meta": {},
            "wrapper_code": "",
            "registration_snippet": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")

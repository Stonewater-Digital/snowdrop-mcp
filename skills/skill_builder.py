"""
Executive Summary: Meta-skill that generates new Snowdrop skill Python modules via the Assembly Line (Haiku drafts, Sonnet polishes, Opus certifies).

Inputs: name (str), purpose (str), inputs (str), outputs (str), complexity (str: standard/jury),
        write_to_disk (bool, optional)
Outputs: dict with generated code (str), stages_completed (list), written_to (str or null)
MCP Tool Name: skill_builder
"""
import os
import ast
from typing import Any

from openai import OpenAI

from config.models import resolve_model
from skills.utils import log_lesson, get_iso_timestamp, logger

# --- MCP Tool Metadata ---
TOOL_META = {
    "name": "skill_builder",
    "description": (
        "Meta-skill: takes a plain-English skill description and generates a production-ready "
        "Snowdrop Python skill module via the Assembly Line (Haiku drafts, Sonnet polishes, "
        "Opus certifies for jury-tier complexity). Optionally writes the result to disk."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "snake_case module name for the new skill (e.g. 'fetch_price').",
            },
            "purpose": {
                "type": "string",
                "description": "One sentence describing what the skill does.",
            },
            "inputs": {
                "type": "string",
                "description": "Description of the skill's input parameters and their types.",
            },
            "outputs": {
                "type": "string",
                "description": "Description of what the skill returns.",
            },
            "complexity": {
                "type": "string",
                "enum": ["standard", "jury"],
                "default": "standard",
                "description": (
                    "Assembly line tier. 'standard' uses Haiku + Sonnet. "
                    "'jury' adds Opus final review."
                ),
            },
            "write_to_disk": {
                "type": "boolean",
                "default": False,
                "description": "If true, writes the generated code to skills/{name}.py.",
            },
        },
        "required": ["name", "purpose", "inputs", "outputs"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "stages_completed": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "written_to": {
                        "type": ["string", "null"],
                    },
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# --- Skill Template for LLM System Prompt ---
SKILL_TEMPLATE: str = '''
You are an expert Python developer building skills for Snowdrop — a Sovereign Financial Intelligence Agent.
Every skill you generate MUST follow this exact template:

```python
"""
Executive Summary: [One line — what this skill does]

Inputs: [List params with types]
Outputs: [Return type description]
MCP Tool Name: [snake_case name]
"""
import os
from typing import Any

from skills.utils import log_lesson, get_iso_timestamp, logger

# --- MCP Tool Metadata ---
TOOL_META = {
    "name": "skill_name_here",
    "description": "What this tool does",
    "inputSchema": {
        "type": "object",
        "properties": { },
        "required": [ ]
    },
    "outputSchema": {
        "type": "object",
        "properties": { },
        "required": [ ]
    }
}

def skill_name_here(**kwargs) -> dict:
    """Google-style docstring with Args and Returns sections."""
    try:
        # Implementation here
        result = {}  # Replace with actual logic
        return {
            "status": "success",
            "data": result,
            "timestamp": get_iso_timestamp()
        }
    except Exception as e:
        logger.error(f"skill_name_here failed: {e}")
        log_lesson(f"skill_name_here: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp()
        }
```

Rules:
1. Use Python 3.11+ type hints everywhere.
2. Google-style docstrings on all functions (Args, Returns, Raises sections).
3. All environment variables via os.getenv().
4. Never raise unhandled exceptions — always catch at the top-level function.
5. Always return {"status": "success"|"error", "data": ..., "timestamp": iso_str}.
6. TOOL_META must have accurate inputSchema and outputSchema.
7. log_lesson must always be present and called on errors.
8. Keep imports minimal — only what is strictly required.
9. The main function name must exactly match the TOOL_META "name" field.
'''.strip()


def _call_llm(client: OpenAI, model: str, system: str, user: str) -> str:
    """Call an LLM via OpenRouter and return the response content.

    Args:
        client: An initialized OpenAI client pointing at OpenRouter.
        model: The OpenRouter model identifier string.
        system: System prompt to set the LLM's role and constraints.
        user: User message containing the specific request.

    Returns:
        str: The raw text content of the model's response.

    Raises:
        RuntimeError: If the API call fails or returns empty content.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError(f"Empty response from model {model}")
    return content


def skill_builder(
    name: str,
    purpose: str,
    inputs: str,
    outputs: str,
    complexity: str = "standard",
    **kwargs: Any,
) -> dict:
    """Generate a new Snowdrop skill module via the Assembly Line pattern.

    Orchestrates a multi-stage LLM pipeline to produce a production-ready Python
    skill module from a plain-English description:

        Stage 1 (Draft)   — claude-haiku: fast initial code generation
        Stage 2 (Polish)  — claude-sonnet: refinement, correctness, docstrings
        Stage 3 (Certify) — claude-opus: architectural review (jury tier only)

    Optionally writes the final code to skills/{name}.py on disk.

    Args:
        name: snake_case module name for the new skill (e.g. "fetch_price").
        purpose: One-sentence description of what the skill does.
        inputs: Description of input parameters and their types.
        outputs: Description of what the skill returns.
        complexity: Assembly line tier — "standard" (Haiku + Sonnet) or
            "jury" (adds Opus certification). Defaults to "standard".
        **kwargs: Optional overrides:
            - write_to_disk (bool): If True, saves generated code to disk.

    Returns:
        dict: A result dict with the following shape on success::

            {
                "status": "success",
                "data": {
                    "code": "<generated Python source>",
                    "stages_completed": ["draft", "polish"],
                    "written_to": "skills/fetch_price.py"  # or null
                },
                "timestamp": "2026-02-19T00:00:00+00:00"
            }

        On error::

            {
                "status": "error",
                "error": "<error message>",
                "timestamp": "2026-02-19T00:00:00+00:00"
            }
    """
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")

        write_to_disk: bool = bool(kwargs.get("write_to_disk", False))

        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        user_request: str = (
            f"Generate a complete Snowdrop skill module with the following specification:\n\n"
            f"Name: {name}\n"
            f"Purpose: {purpose}\n"
            f"Inputs: {inputs}\n"
            f"Outputs: {outputs}\n\n"
            f"Follow the template exactly. The TOOL_META name must be '{name}' "
            f"and the main function must also be named '{name}'."
        )

        stages_completed: list[str] = []

        # --- Stage 1: Draft (Haiku) ---
        logger.info(f"skill_builder: Stage 1 Draft via {resolve_model('draft')}")
        draft_code = _call_llm(
            client=client,
            model=resolve_model("draft"),
            system=SKILL_TEMPLATE,
            user=user_request,
        )
        stages_completed.append("draft")
        logger.info(f"skill_builder: Draft complete ({len(draft_code)} chars)")

        # --- Stage 2: Polish (Sonnet) ---
        polish_prompt: str = (
            f"Here is a draft Snowdrop skill module:\n\n```python\n{draft_code}\n```\n\n"
            f"Please refine this code for production quality:\n"
            f"1. Ensure all type hints are accurate and complete (Python 3.11+)\n"
            f"2. Improve Google-style docstrings (Args, Returns, Raises sections)\n"
            f"3. Verify TOOL_META inputSchema and outputSchema are accurate\n"
            f"4. Ensure error handling is robust and _log_lesson is always called on errors\n"
            f"5. Remove any placeholder comments — replace with real implementation\n"
            f"6. Keep the same function signatures and template structure\n\n"
            f"Return only the final Python code, no explanation."
        )

        logger.info(f"skill_builder: Stage 2 Polish via {resolve_model('default')}")
        polished_code = _call_llm(
            client=client,
            model=resolve_model("default"),
            system=SKILL_TEMPLATE,
            user=polish_prompt,
        )
        stages_completed.append("polish")
        logger.info(f"skill_builder: Polish complete ({len(polished_code)} chars)")

        final_code: str = polished_code

        # --- Stage 3: Certify (Opus) — jury tier only ---
        if complexity == "jury":
            certify_prompt: str = (
                f"You are the CFO AI reviewing a new Snowdrop skill for architectural soundness.\n\n"
                f"```python\n{polished_code}\n```\n\n"
                f"Perform a final review:\n"
                f"1. Check for security issues (hardcoded secrets, unsafe eval, etc.)\n"
                f"2. Verify fund-safety: no irreversible actions without guard checks\n"
                f"3. Confirm the MCP tool schema accurately reflects behavior\n"
                f"4. Ensure idempotency where applicable\n"
                f"5. Make any final corrections needed\n\n"
                f"Return only the final certified Python code, no explanation."
            )

            logger.info(f"skill_builder: Stage 3 Certify via {resolve_model('certification')}")
            certified_code = _call_llm(
                client=client,
                model=resolve_model("certification"),
                system=SKILL_TEMPLATE,
                user=certify_prompt,
            )
            stages_completed.append("certify")
            final_code = certified_code
            logger.info(f"skill_builder: Certify complete ({len(final_code)} chars)")

        # --- Extract code block if LLM wrapped it in markdown ---
        if "```python" in final_code:
            start = final_code.index("```python") + len("```python")
            end = final_code.rindex("```")
            final_code = final_code[start:end].strip()

        # --- Optionally write to disk ---
        written_to: str | None = None
        if write_to_disk:
            # Validate AST before writing
            try:
                ast.parse(final_code)
            except SyntaxError as e:
                raise ValueError(f"Generated code failed syntax validation: {e}")

            output_path = f"skills/{name}.py"
            with open(output_path, "w") as f:
                f.write(final_code)
            written_to = output_path
            logger.info(f"skill_builder: wrote skill to {output_path}")

        return {
            "status": "success",
            "data": {
                "code": final_code,
                "stages_completed": stages_completed,
                "written_to": written_to,
            },
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"skill_builder failed: {e}")
        log_lesson(f"skill_builder: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }

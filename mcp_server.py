"""
Executive Summary: FastMCP server for Snowdrop that dynamically discovers and registers
all skills in the skills/ directory as MCP tools, exposing them via the Model Context
Protocol (tools/list and tools/call) to any MCP-compatible client.

Table of Contents:
    1. Imports and Logging Setup
    2. FastMCP Server Instance
    3. _discover_skills() — walks skills/ directory, imports modules, collects TOOL_META
    4. register_skills() — registers discovered callables with the FastMCP server
    5. main() — orchestrates discovery, registration, and server startup
    6. Entrypoint
"""

import functools
import importlib.util
import inspect
import logging
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# 1. Logging Setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger("snowdrop.mcp_server")

# ---------------------------------------------------------------------------
# 2. FastMCP Server Instance
# ---------------------------------------------------------------------------

mcp = FastMCP("Snowdrop")

# ---------------------------------------------------------------------------
# 3. Skill Discovery
# ---------------------------------------------------------------------------

# The skills/ directory is the same directory that contains this file.
_SKILLS_DIR: Path = Path(__file__).parent

# Filenames to exclude from discovery.
_EXCLUDED_FILES: frozenset[str] = frozenset({"__init__.py", "mcp_server.py"})


def _discover_skills() -> dict[str, dict[str, Any]]:
    """Walk the skills/ directory tree and collect modules that expose TOOL_META.

    For each .py file (excluding __init__.py and mcp_server.py) the function:
        - Imports the module dynamically via importlib.
        - Checks for a ``TOOL_META`` dict attribute on the module.
        - Looks for a callable on the module whose name matches
          ``TOOL_META["name"]``.
        - Adds a record to the result dict keyed by the tool name.

    Returns:
        A dict mapping tool name -> {
            "meta": TOOL_META dict,
            "callable": the skill function,
            "module_path": absolute path string of the source file,
        }.
        Broken or non-conforming modules are skipped with a logged warning.
    """
    discovered: dict[str, dict[str, Any]] = {}

    py_files = sorted(_SKILLS_DIR.rglob("*.py"))

    for py_file in py_files:
        if py_file.name in _EXCLUDED_FILES:
            continue

        module_path_str = str(py_file.resolve())

        # Build a unique module name based on the relative path inside skills/.
        rel = py_file.relative_to(_SKILLS_DIR)
        # Convert path segments to a dotted module name, e.g. fund_accounting/core.py
        # becomes skills.fund_accounting.core
        module_name = "skills." + ".".join(rel.with_suffix("").parts)

        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            if spec is None or spec.loader is None:
                logger.warning("Could not create module spec for %s — skipping.", py_file)
                continue

            module: ModuleType = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)  # type: ignore[union-attr]
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to import %s: %s — skipping.", py_file, exc)
            continue

        # Validate TOOL_META presence and structure.
        tool_meta = getattr(module, "TOOL_META", None)
        if not isinstance(tool_meta, dict):
            logger.debug("%s has no TOOL_META dict — skipping.", py_file)
            continue

        tool_name: str | None = tool_meta.get("name")
        if not tool_name:
            logger.warning("%s TOOL_META missing 'name' key — skipping.", py_file)
            continue

        # Find the callable on the module.
        fn: Callable[..., Any] | None = getattr(module, tool_name, None)
        if fn is None or not callable(fn):
            logger.warning(
                "%s TOOL_META['name'] = %r but no matching callable found — skipping.",
                py_file,
                tool_name,
            )
            continue

        discovered[tool_name] = {
            "meta": tool_meta,
            "callable": fn,
            "module_path": module_path_str,
        }
        logger.debug("Discovered skill '%s' from %s.", tool_name, py_file)

    return discovered


# ---------------------------------------------------------------------------
# 4. Skill Registration
# ---------------------------------------------------------------------------


def _strip_var_keyword(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Return a wrapper of fn with **kwargs removed from its signature.

    FastMCP 3.x rejects functions whose signature contains VAR_KEYWORD (**kwargs)
    parameters.  This helper creates a thin wrapper with an adjusted signature so
    FastMCP can inspect and register the tool correctly, while still forwarding all
    keyword arguments to the original implementation.
    """
    sig = inspect.signature(fn)
    has_var_keyword = any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
    )
    if not has_var_keyword:
        return fn

    explicit_params = [
        p
        for p in sig.parameters.values()
        if p.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
    ]
    new_sig = sig.replace(parameters=explicit_params)

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    wrapper.__signature__ = new_sig  # type: ignore[attr-defined]
    return wrapper


def register_skills(discovered: dict[str, dict[str, Any]]) -> None:
    """Register each discovered skill with the FastMCP server.

    Uses ``mcp.tool()`` as a regular function call (not a decorator) so that
    registration can be performed dynamically at runtime.

    Args:
        discovered: The dict returned by ``_discover_skills()``, mapping
            tool name -> {"meta": ..., "callable": ..., "module_path": ...}.
    """
    for tool_name, record in discovered.items():
        fn: Callable[..., Any] = record["callable"]
        description: str = record["meta"].get("description", "")

        try:
            registered_fn = _strip_var_keyword(fn)
            mcp.tool(name=tool_name, description=description)(registered_fn)
            logger.debug("Registered tool '%s'.", tool_name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to register tool '%s': %s — skipping.", tool_name, exc)


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Discover skills, register them as MCP tools, and start the server.

    Execution order:
        1. ``_discover_skills()`` walks the skills/ directory.
        2. ``register_skills()`` binds each callable to the FastMCP instance.
        3. ``mcp.run()`` starts the server; FastMCP automatically handles
           ``tools/list`` and ``tools/call`` per the MCP spec.
    """
    logger.info("Snowdrop MCP server starting — scanning %s for skills…", _SKILLS_DIR)

    discovered = _discover_skills()

    if not discovered:
        logger.warning("No skills discovered. Server will start with zero tools.")
    else:
        register_skills(discovered)
        logger.info(
            "Successfully registered %d skill(s): %s",
            len(discovered),
            ", ".join(sorted(discovered.keys())),
        )

    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)


# ---------------------------------------------------------------------------
# 6. Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

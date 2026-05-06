"""
Executive Summary: Community Edition MCP server for Snowdrop. Dynamically discovers
and registers all skills in the skills/ directory, exposing them via the Model Context
Protocol through 3 meta-tools (dispatcher mode). No authentication required.

Table of Contents:
    1. Imports and Logging Setup
    2. FastMCP Server Instance
    3. Skill Discovery
    4. Skill Registration (direct mode, legacy)
    5. Meta-Tool Dispatcher (3 gateway tools)
    6. Main — FastAPI wrapper with /health, /.well-known/agent.json, /.well-known/skills.json
    7. Entrypoint
"""

import functools
import importlib.util
import inspect
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

# Ensure the repo root is in sys.path so skill files can do
# 'from skills.utils.xxx import yyy' regardless of invocation method.
_REPO_ROOT = Path(__file__).parent.resolve()
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

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

# The skills/ directory lives alongside this file.
_SKILLS_DIR: Path = Path(__file__).parent / "skills"

# Filenames to exclude from discovery.
_EXCLUDED_FILES: frozenset[str] = frozenset({"__init__.py", "mcp_server.py"})

# "dispatcher" (default) registers 3 meta-tools that gateway all skills.
# "direct" registers individual tools (subject to _MAX_TOOLS cap).
_MCP_MODE: str = os.environ.get("SNOWDROP_MCP_MODE", "dispatcher")

# Max tools exposed in direct mode. Set to 0 for unlimited.
_MAX_TOOLS: int = int(os.environ.get("SNOWDROP_MCP_MAX_TOOLS", "250"))

# Populated by main() after discovery — used by dispatcher meta-tools.
_SKILL_CATALOG: dict[str, dict[str, Any]] = {}

# Comma-separated whitelist of skill subdirectories to include.
_INCLUDE_DIRS: frozenset[str] = frozenset(
    d.strip() for d in os.environ.get("SNOWDROP_MCP_INCLUDE_DIRS", "").split(",") if d.strip()
)

# Comma-separated blacklist of skill subdirectories to exclude.
_EXCLUDE_DIRS: frozenset[str] = frozenset(
    d.strip() for d in os.environ.get("SNOWDROP_MCP_EXCLUDE_DIRS", "").split(",") if d.strip()
)


def _discover_skills() -> dict[str, dict[str, Any]]:
    """Walk the skills/ directory tree and collect modules that expose TOOL_META.

    Returns:
        A dict mapping tool name -> {
            "meta": TOOL_META dict,
            "callable": the skill function,
            "module_path": absolute path string of the source file,
            "category": subdirectory name or "root",
        }.
    """
    discovered: dict[str, dict[str, Any]] = {}
    failed_imports: list[str] = []

    if not _SKILLS_DIR.exists():
        logger.warning("Skills directory %s not found.", _SKILLS_DIR)
        _discover_skills._failed_imports = failed_imports  # type: ignore[attr-defined]
        return discovered

    for py_file in sorted(_SKILLS_DIR.rglob("*.py")):
        if py_file.name in _EXCLUDED_FILES:
            continue

        rel_parts = py_file.relative_to(_SKILLS_DIR).parts
        subdir = rel_parts[0] if len(rel_parts) > 1 else ""
        if _INCLUDE_DIRS and subdir not in _INCLUDE_DIRS:
            continue
        if _EXCLUDE_DIRS and subdir in _EXCLUDE_DIRS:
            continue

        module_path_str = str(py_file.resolve())
        rel = py_file.relative_to(_SKILLS_DIR)
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
            failed_imports.append(f"{py_file.name}: {type(exc).__name__}: {exc}")
            continue

        tool_meta = getattr(module, "TOOL_META", None)
        if not isinstance(tool_meta, dict):
            logger.debug("%s has no TOOL_META dict — skipping.", py_file)
            continue

        tool_name: str | None = tool_meta.get("name")
        if not tool_name:
            logger.warning("%s TOOL_META missing 'name' key — skipping.", py_file)
            continue

        fn: Callable[..., Any] | None = getattr(module, tool_name, None)
        if fn is None or not callable(fn):
            logger.warning(
                "%s TOOL_META['name'] = %r but no matching callable found — skipping.",
                py_file, tool_name,
            )
            continue

        discovered[tool_name] = {
            "meta": tool_meta,
            "callable": fn,
            "module_path": module_path_str,
            "category": subdir or "root",
        }
        logger.debug("Discovered skill '%s' from %s.", tool_name, py_file)

    _discover_skills._failed_imports = failed_imports  # type: ignore[attr-defined]
    return discovered


# ---------------------------------------------------------------------------
# 4. Skill Registration (direct mode)
# ---------------------------------------------------------------------------


def _strip_var_keyword(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Return a wrapper of fn with **kwargs removed from its signature.

    FastMCP 3.x rejects functions whose signature contains VAR_KEYWORD (**kwargs)
    parameters.
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
    """Register each discovered skill with the FastMCP server (direct mode)."""
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
# 5. Meta-Tool Dispatcher
# ---------------------------------------------------------------------------


def _build_skill_summary(record: dict[str, Any]) -> dict[str, Any]:
    """Extract a client-friendly summary from a catalog record."""
    meta = record["meta"]
    return {
        "name": meta.get("name", ""),
        "description": meta.get("description", ""),
        "category": record.get("category", ""),
        "inputSchema": meta.get("inputSchema", {}),
    }


def snowdrop_list_skills(category: str = "") -> dict[str, Any]:
    """List available skill categories, or skills within a specific category.

    Args:
        category: If empty, returns all categories with skill counts.
            If set, returns the skills in that category with their schemas.
    """
    ts = datetime.now(timezone.utc).isoformat()
    if not category:
        cats: dict[str, int] = {}
        for record in _SKILL_CATALOG.values():
            cat = record.get("category", "root")
            cats[cat] = cats.get(cat, 0) + 1
        return {
            "status": "ok",
            "data": {
                "total_skills": len(_SKILL_CATALOG),
                "categories": dict(sorted(cats.items())),
            },
            "timestamp": ts,
        }

    matches = [
        _build_skill_summary(r)
        for r in _SKILL_CATALOG.values()
        if r.get("category", "") == category
    ]
    if not matches:
        return {
            "status": "error",
            "data": {"error": f"No category '{category}' found."},
            "timestamp": ts,
        }
    return {
        "status": "ok",
        "data": {"category": category, "skills": matches, "count": len(matches)},
        "timestamp": ts,
    }


def snowdrop_execute(skill: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a Snowdrop skill by name with the given parameters.

    Args:
        skill: Exact skill name (e.g. "rsi_calculator").
        params: Keyword arguments to pass to the skill function.
    """
    ts = datetime.now(timezone.utc).isoformat()
    record = _SKILL_CATALOG.get(skill)
    if record is None:
        return {
            "status": "error",
            "data": {"error": f"Unknown skill '{skill}'. Use snowdrop_list_skills to browse."},
            "timestamp": ts,
        }

    fn: Callable[..., Any] = record["callable"]
    call_params = params or {}
    try:
        result = fn(**call_params)
        return result
    except Exception as exc:
        error_msg = f"{type(exc).__name__}: {exc}"
        return {"status": "error", "data": {"error": error_msg}, "timestamp": ts}


def snowdrop_search_skills(query: str) -> dict[str, Any]:
    """Search skills by keyword in name or description.

    Args:
        query: Search term (case-insensitive substring match).
    """
    ts = datetime.now(timezone.utc).isoformat()
    q = query.lower()
    matches = [
        _build_skill_summary(r)
        for name, r in _SKILL_CATALOG.items()
        if q in name.lower() or q in r["meta"].get("description", "").lower()
    ]
    return {
        "status": "ok",
        "data": {"query": query, "results": matches, "count": len(matches)},
        "timestamp": ts,
    }


def _register_dispatcher() -> None:
    """Register the 3 meta-tools with the FastMCP server."""
    mcp.tool(
        name="snowdrop_list_skills",
        description=(
            "List Snowdrop's skill categories and their counts, or list all skills "
            "within a specific category. Call with no arguments to see categories, "
            "or pass category='technical_analysis' to see skills in that category."
        ),
    )(snowdrop_list_skills)

    mcp.tool(
        name="snowdrop_execute",
        description=(
            "Execute any Snowdrop skill by name. Pass the skill name and a params dict. "
            "Example: skill='rsi_calculator', params={'prices': [...], 'period': 14}. "
            "Use snowdrop_list_skills or snowdrop_search_skills to discover available skills."
        ),
    )(snowdrop_execute)

    mcp.tool(
        name="snowdrop_search_skills",
        description=(
            "Search Snowdrop's skill catalog by keyword. Returns matching skill names, "
            "descriptions, categories, and input schemas. "
            "Example: query='volatility' returns all volatility-related skills."
        ),
    )(snowdrop_search_skills)


# ---------------------------------------------------------------------------
# 6. Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Discover skills, register them as MCP tools, and start the server."""
    logger.info("Snowdrop Community Edition starting — scanning %s for skills…", _SKILLS_DIR)

    discovered = _discover_skills()

    _failed_imports: list[str] = getattr(_discover_skills, "_failed_imports", [])
    logger.info(
        "Skill discovery complete — loaded=%d failed=%d",
        len(discovered), len(_failed_imports),
    )

    global _SKILL_CATALOG
    _SKILL_CATALOG = discovered

    if _MCP_MODE == "dispatcher":
        _register_dispatcher()
        logger.info(
            "Dispatcher mode — registered 3 meta-tools gatewaying %d skills across %d categories.",
            len(discovered),
            len({r.get("category", "root") for r in discovered.values()}),
        )
    else:
        if _MAX_TOOLS > 0 and len(discovered) > _MAX_TOOLS:
            logger.warning(
                "Discovered %d skills but SNOWDROP_MCP_MAX_TOOLS=%d — truncating.",
                len(discovered), _MAX_TOOLS,
            )
            sorted_names = sorted(discovered.keys())[:_MAX_TOOLS]
            discovered = {k: discovered[k] for k in sorted_names}
            _SKILL_CATALOG = discovered

        if not discovered:
            logger.warning("No skills discovered. Server will start with zero tools.")
        else:
            register_skills(discovered)
            logger.info("Direct mode — registered %d skill(s).", len(discovered))

    # --- Server Startup -------------------------------------------------------
    port_env = os.environ.get("PORT")

    if port_env:
        # HTTP mode — FastAPI wrapper with /health, /.well-known/agent.json, /.well-known/skills.json
        import uvicorn
        from fastapi import FastAPI, Response

        logger.info("HTTP mode — starting FastAPI+uvicorn on 0.0.0.0:%s", port_env)

        _mcp_http_app = mcp.http_app(stateless_http=True)

        _app = FastAPI(
            lifespan=_mcp_http_app.lifespan,
            title="Snowdrop MCP — Community Edition",
            version="2.0.0",
            description=(
                f"{len(discovered)} financial, compliance, DeFi, and infrastructure skills. "
                "Community edition — no authentication required."
            ),
            redirect_slashes=False,
        )

        @_app.get("/health", tags=["ops"])
        async def health() -> dict:
            """Health probe — returns service status and skill count."""
            return {
                "status": "ok",
                "skills": len(discovered),
                "version": "2.0.0",
                "edition": "community",
            }

        @_app.get("/.well-known/agent.json", tags=["a2a"])
        async def agent_card() -> Response:
            """A2A Agent Card — machine-readable service advertisement."""
            card_path = Path(__file__).parent / ".well-known" / "agent.json"
            if card_path.exists():
                content = card_path.read_text(encoding="utf-8")
            else:
                import json as _json
                content = _json.dumps({
                    "name": "Snowdrop",
                    "version": "2.0.0",
                    "error": "agent.json not found",
                })
            return Response(content=content, media_type="application/json")

        @_app.get("/.well-known/skills.json", tags=["a2a"])
        async def well_known_skills() -> dict:
            """Discovery endpoint: lists all available skills with metadata."""
            skills_list = []
            for name, record in _SKILL_CATALOG.items():
                # _SKILL_CATALOG entries store TOOL_META under key "meta"
                tool_meta = record.get("meta", {})
                description = tool_meta.get("description", "")
                parameters = (
                    tool_meta.get("inputSchema")
                    or tool_meta.get("parameters")
                    or {}
                )
                # category is stored directly in the record by _discover_skills()
                category = record.get("category", "general")

                # Tier: explicit field in TOOL_META, fallback to "free"
                tier = tool_meta.get("tier", "free")
                # Secondary check: "premium" keyword in description
                if tier == "free" and "premium" in description.lower():
                    tier = "premium"

                skills_list.append({
                    "name": name,
                    "description": description,
                    "category": category,
                    "tier": tier,
                    "uri": f"skill://{name}",
                    "parameters": parameters,
                })

            free_count = sum(1 for s in skills_list if s["tier"] == "free")
            premium_count = sum(1 for s in skills_list if s["tier"] == "premium")

            return {
                "schema_version": "1.0",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "server": {
                    "name": "Snowdrop",
                    "version": "2.0.0",
                    "url": "https://snowdrop-mcp-43795844349.us-central1.run.app",
                },
                "skills": skills_list,
                "total": len(skills_list),
                "free_count": free_count,
                "premium_count": premium_count,
            }

        _app.mount("", _mcp_http_app)

        uvicorn.run(
            _app,
            host="0.0.0.0",
            port=int(port_env),
            log_config=None,
        )
    else:
        # Stdio mode — for local MCP clients (Claude Code, Cursor, etc.)
        logger.info("Stdio mode — waiting for MCP client connection")
        mcp.run()


# ---------------------------------------------------------------------------
# 7. Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

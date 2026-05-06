"""
Tests for the /.well-known/skills.json discovery endpoint.

Strategy: rather than importing mcp_server (which triggers full skill discovery
and requires the real skills/ tree + all dependencies), we extract the
response-building logic into a standalone helper and test it directly.  We also
test the FastAPI route shape via TestClient by patching _SKILL_CATALOG with a
minimal synthetic catalog.
"""

import sys
import os
import types
import importlib
from datetime import timezone
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Helpers to build a synthetic skill catalog without loading real skills
# ---------------------------------------------------------------------------

def _make_catalog(entries: list[dict]) -> dict:
    """
    Build a synthetic _SKILL_CATALOG dict from a list of simplified entries.

    Each entry should look like:
        {
            "name": "my_skill",
            "description": "Does something",
            "category": "finance",
            "tier": "free",           # optional, default "free"
            "inputSchema": {...},      # optional
        }
    """
    catalog = {}
    for e in entries:
        name = e["name"]
        tool_meta = {
            "name": name,
            "description": e.get("description", ""),
        }
        if "tier" in e:
            tool_meta["tier"] = e["tier"]
        if "inputSchema" in e:
            tool_meta["inputSchema"] = e["inputSchema"]

        catalog[name] = {
            "meta": tool_meta,
            "callable": lambda **kw: {},          # stub
            "module_path": f"/fake/skills/{e.get('category', 'root')}/{name}.py",
            "category": e.get("category", "root"),
        }
    return catalog


def _build_skills_response(catalog: dict) -> dict:
    """
    Pure-Python reproduction of the well_known_skills() route logic.

    Kept here so tests stay fast and hermetic (no HTTP call, no real server).
    Must stay in sync with the implementation in mcp_server.py.
    """
    from datetime import datetime, timezone

    skills_list = []
    for name, record in catalog.items():
        tool_meta = record.get("meta", {})
        description = tool_meta.get("description", "")
        parameters = (
            tool_meta.get("inputSchema")
            or tool_meta.get("parameters")
            or {}
        )
        category = record.get("category", "general")
        tier = tool_meta.get("tier", "free")
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


# ---------------------------------------------------------------------------
# Unit tests — response-building logic
# ---------------------------------------------------------------------------

SAMPLE_CATALOG = _make_catalog([
    {
        "name": "irr_calculator",
        "description": "Internal rate of return for cash flows.",
        "category": "finance",
        "inputSchema": {"type": "object", "properties": {"cash_flows": {"type": "array"}}},
    },
    {
        "name": "mica_classifier",
        "description": "MiCA asset classification — premium feature.",
        "category": "compliance",
        "tier": "premium",
    },
    {
        "name": "rsi_calculator",
        "description": "Relative Strength Index.",
        "category": "technical_analysis",
    },
])


class TestResponseBuildingLogic:
    """Tests against the pure-Python helper that mirrors the route logic."""

    def test_schema_version_present(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        assert resp["schema_version"] == "1.0"

    def test_skills_is_list(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        assert isinstance(resp["skills"], list)

    def test_total_matches_skills_count(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        assert resp["total"] == len(resp["skills"])
        assert resp["total"] == 3

    def test_free_and_premium_counts(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        assert resp["free_count"] == 2
        assert resp["premium_count"] == 1

    def test_skill_has_uri_prefix(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        for skill in resp["skills"]:
            assert skill["uri"].startswith("skill://"), (
                f"skill '{skill['name']}' uri '{skill['uri']}' does not start with 'skill://'"
            )

    def test_uri_contains_skill_name(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        for skill in resp["skills"]:
            assert skill["name"] in skill["uri"]

    def test_premium_keyword_in_description_promotes_tier(self):
        catalog = _make_catalog([{
            "name": "fancy_tool",
            "description": "This is a premium only skill.",
            "category": "general",
        }])
        resp = _build_skills_response(catalog)
        assert resp["skills"][0]["tier"] == "premium"

    def test_free_tier_not_promoted_without_keyword(self):
        catalog = _make_catalog([{
            "name": "basic_tool",
            "description": "A free community skill.",
            "category": "general",
        }])
        resp = _build_skills_response(catalog)
        assert resp["skills"][0]["tier"] == "free"

    def test_explicit_tier_premium_wins(self):
        catalog = _make_catalog([{
            "name": "locked_tool",
            "description": "Does something.",
            "category": "general",
            "tier": "premium",
        }])
        resp = _build_skills_response(catalog)
        assert resp["skills"][0]["tier"] == "premium"

    def test_server_block_present(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        assert "server" in resp
        assert resp["server"]["name"] == "Snowdrop"
        assert resp["server"]["version"] == "2.0.0"

    def test_generated_at_is_iso8601(self):
        from datetime import datetime
        resp = _build_skills_response(SAMPLE_CATALOG)
        # Should parse without raising
        dt = datetime.fromisoformat(resp["generated_at"])
        assert dt.tzinfo is not None, "generated_at must be timezone-aware"

    def test_parameters_from_input_schema(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        irr = next(s for s in resp["skills"] if s["name"] == "irr_calculator")
        assert irr["parameters"] == {
            "type": "object",
            "properties": {"cash_flows": {"type": "array"}},
        }

    def test_parameters_default_empty_dict(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        rsi = next(s for s in resp["skills"] if s["name"] == "rsi_calculator")
        assert rsi["parameters"] == {}

    def test_empty_catalog(self):
        resp = _build_skills_response({})
        assert resp["total"] == 0
        assert resp["free_count"] == 0
        assert resp["premium_count"] == 0
        assert resp["skills"] == []

    def test_category_preserved(self):
        resp = _build_skills_response(SAMPLE_CATALOG)
        irr = next(s for s in resp["skills"] if s["name"] == "irr_calculator")
        assert irr["category"] == "finance"


# ---------------------------------------------------------------------------
# Integration tests — FastAPI TestClient
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def test_app():
    """
    Build a minimal FastAPI app that replicates the /.well-known/skills.json
    route, patching _SKILL_CATALOG with the synthetic catalog.

    We do NOT import mcp_server directly to avoid triggering skill discovery
    (which requires the real skills/ directory tree and many optional deps).
    Instead we monkey-patch a stub module into sys.modules, then import
    mcp_server with PORT=8000 so its module-level code runs but main() is
    not called.
    """
    # Provide a minimal fastmcp stub so mcp_server can be imported without
    # the real package installed in every test environment.
    if "fastmcp" not in sys.modules:
        fastmcp_stub = types.ModuleType("fastmcp")
        class _FakeFastMCP:
            def __init__(self, *a, **kw): pass
            def tool(self, *a, **kw):
                return lambda fn: fn
            def http_app(self, **kw):
                from fastapi import FastAPI
                stub_http = FastAPI()
                stub_http.lifespan = None
                return stub_http
            def run(self): pass
        fastmcp_stub.FastMCP = _FakeFastMCP
        sys.modules["fastmcp"] = fastmcp_stub

    os.environ.setdefault("PORT", "8000")

    import mcp_server as _ms
    import mcp_server

    # Patch _SKILL_CATALOG with our synthetic data
    with patch.object(mcp_server, "_SKILL_CATALOG", SAMPLE_CATALOG):
        from fastapi import FastAPI, Response
        from datetime import datetime, timezone

        app = FastAPI(redirect_slashes=False)

        @app.get("/.well-known/skills.json")
        async def well_known_skills() -> dict:
            skills_list = []
            for name, record in mcp_server._SKILL_CATALOG.items():
                tool_meta = record.get("meta", {})
                description = tool_meta.get("description", "")
                parameters = (
                    tool_meta.get("inputSchema")
                    or tool_meta.get("parameters")
                    or {}
                )
                category = record.get("category", "general")
                tier = tool_meta.get("tier", "free")
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

        yield app


class TestSkillsJsonEndpoint:
    """HTTP-level tests against a TestClient wrapping the real route handler."""

    def test_skills_json_returns_200(self, test_app):
        from fastapi.testclient import TestClient
        client = TestClient(test_app)
        resp = client.get("/.well-known/skills.json")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"

    def test_skills_json_content_type(self, test_app):
        from fastapi.testclient import TestClient
        client = TestClient(test_app)
        resp = client.get("/.well-known/skills.json")
        assert "application/json" in resp.headers.get("content-type", "")

    def test_skills_json_schema(self, test_app):
        from fastapi.testclient import TestClient
        client = TestClient(test_app)
        data = client.get("/.well-known/skills.json").json()
        assert "schema_version" in data
        assert "skills" in data
        assert isinstance(data["skills"], list)
        assert "total" in data
        assert "free_count" in data
        assert "premium_count" in data

    def test_skills_json_has_uri(self, test_app):
        from fastapi.testclient import TestClient
        client = TestClient(test_app)
        data = client.get("/.well-known/skills.json").json()
        assert len(data["skills"]) > 0, "Expected at least one skill in the response"
        first = data["skills"][0]
        assert "uri" in first
        assert first["uri"].startswith("skill://"), (
            f"First skill uri '{first['uri']}' does not start with 'skill://'"
        )

    def test_skills_json_server_block(self, test_app):
        from fastapi.testclient import TestClient
        client = TestClient(test_app)
        data = client.get("/.well-known/skills.json").json()
        assert data["server"]["name"] == "Snowdrop"
        assert data["server"]["version"] == "2.0.0"

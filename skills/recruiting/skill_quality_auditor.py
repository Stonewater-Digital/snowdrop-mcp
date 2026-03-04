"""
skill_quality_auditor.py — AST-based security and quality audit for submitted skill code.

Executive Summary:
    Analyzes submitted Python skill code using AST only (never imports or executes).
    Tier 1 blocks dangerous module imports. Tier 2 blocks dangerous built-in calls.
    On violations, generates A2A-compliant revision_requested feedback with line numbers
    and suggestions. Edge cases: obfuscated getattr calls, nested exec, string-built
    dangerous calls.

MCP Tool Name: skill_quality_auditor
"""
import ast
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any

logger = logging.getLogger("snowdrop.skill_quality_auditor")

TOOL_META = {
    "name": "skill_quality_auditor",
    "description": (
        "AST-based security and quality audit for submitted skill code. "
        "Checks for dangerous imports, unsafe builtins, and TOOL_META compliance. "
        "Returns A2A-compliant feedback for revision requests."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python source code to audit."},
            "trace_id": {"type": "string"},
        },
        "required": ["code", "trace_id"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}

# Tier 1: Blocked module imports
BLOCKED_MODULES = {
    "subprocess", "ctypes", "pickle", "marshal",
    "shutil", "pty", "webbrowser",
}

# Tier 1: Blocked os functions (via os.X)
BLOCKED_OS_FUNCS = {"system", "popen", "exec", "execv", "execvp", "execvpe", "spawn", "spawnl"}

# Tier 2: Blocked built-in calls
BLOCKED_BUILTINS = {"eval", "exec", "__import__", "compile", "globals", "locals", "breakpoint"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


class _ViolationCollector(ast.NodeVisitor):
    """Walk AST and collect security violations."""

    def __init__(self):
        self.violations: list[dict] = []

    def _add(self, line: int, vtype: str, desc: str, suggestion: str):
        self.violations.append({
            "line": line,
            "type": vtype,
            "description": desc,
            "suggestion": suggestion,
        })

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            module_root = alias.name.split(".")[0]
            if module_root in BLOCKED_MODULES:
                self._add(
                    node.lineno, "tier1_import",
                    f"Blocked module import: '{alias.name}'",
                    f"Remove 'import {alias.name}'. Use a safe alternative or Snowdrop utility.",
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            module_root = node.module.split(".")[0]
            if module_root in BLOCKED_MODULES:
                self._add(
                    node.lineno, "tier1_import",
                    f"Blocked module import: 'from {node.module}'",
                    f"Remove 'from {node.module} import ...'. Use a safe alternative.",
                )
            # Check os.system, os.popen etc
            if node.module == "os" and node.names:
                for alias in node.names:
                    if alias.name in BLOCKED_OS_FUNCS:
                        self._add(
                            node.lineno, "tier1_import",
                            f"Blocked os function import: 'from os import {alias.name}'",
                            f"Remove 'from os import {alias.name}'. Use subprocess via Snowdrop utilities.",
                        )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Tier 2: Direct dangerous built-in calls
        func_name = self._get_call_name(node)
        if func_name in BLOCKED_BUILTINS:
            self._add(
                node.lineno, "tier2_builtin",
                f"Blocked built-in call: '{func_name}()'",
                f"Remove '{func_name}()'. Never use dynamic code execution in skills.",
            )

        # Edge case: getattr(builtins, 'eval') or getattr(__builtins__, 'eval')
        if func_name == "getattr" and len(node.args) >= 2:
            second_arg = node.args[1]
            if isinstance(second_arg, ast.Constant) and isinstance(second_arg.value, str):
                if second_arg.value in BLOCKED_BUILTINS:
                    self._add(
                        node.lineno, "tier2_obfuscated",
                        f"Obfuscated dangerous call: getattr(..., '{second_arg.value}')",
                        "Remove obfuscated access to dangerous builtins.",
                    )

        # Edge case: os.system(), os.popen()
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and
                    node.func.value.id == "os" and
                    node.func.attr in BLOCKED_OS_FUNCS):
                self._add(
                    node.lineno, "tier1_os_call",
                    f"Blocked os call: 'os.{node.func.attr}()'",
                    f"Remove 'os.{node.func.attr}()'. Use Snowdrop utilities instead.",
                )

        self.generic_visit(node)

    def _get_call_name(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""


def _check_tool_meta(tree: ast.Module) -> list[dict]:
    """Check for TOOL_META assignment at module level."""
    violations = []
    has_tool_meta = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TOOL_META":
                    has_tool_meta = True
    if not has_tool_meta:
        violations.append({
            "line": 1,
            "type": "missing_tool_meta",
            "description": "Missing TOOL_META dict assignment at module level.",
            "suggestion": "Add TOOL_META = {'name': '...', 'description': '...'} at module level.",
        })
    return violations


def _build_a2a_feedback(trace_id: str, violations: list[dict]) -> dict:
    """Build an A2A-compliant revision_requested feedback payload."""
    return {
        "a2a_version": "0.1.0",
        "sender": {
            "name": "Snowdrop",
            "agent_card": "https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/.well-known/agent.json",
        },
        "intent": "skill_review_feedback",
        "trace_id": trace_id,
        "payload": {
            "result": "revision_requested",
            "violations": violations,
            "max_resubmissions": 2,
            "resubmission_deadline": (datetime.now(timezone.utc) + timedelta(hours=48)).isoformat(),
        },
        "expected_response_schema": {
            "type": "object",
            "properties": {
                "a2a_version": {"type": "string"},
                "intent": {"const": "skill_resubmission"},
                "trace_id": {"type": "string"},
                "payload": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                    },
                    "required": ["code"],
                },
            },
            "required": ["a2a_version", "intent", "trace_id", "payload"],
        },
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=72)).isoformat(),
    }


def skill_quality_auditor(
    code: str,
    trace_id: str,
) -> dict:
    """Audit submitted skill code for security and quality.

    Args:
        code: Python source code to audit.
        trace_id: Correlation ID for traceability.

    Returns:
        Standard Snowdrop envelope with audit results.
    """
    logger.info("Auditing skill code: trace_id=%s, code_length=%d", trace_id, len(code))

    # Step 1: Parse AST
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        logger.warning("Syntax error in submitted code: %s trace_id=%s", exc, trace_id)
        return _wrap("ok", {
            "trace_id": trace_id,
            "score": 0,
            "passed": False,
            "parse_error": str(exc),
            "violations": [{
                "line": exc.lineno or 0,
                "type": "syntax_error",
                "description": f"Python syntax error: {exc.msg}",
                "suggestion": "Fix the syntax error and resubmit.",
            }],
        })

    # Step 2: Collect violations
    collector = _ViolationCollector()
    collector.visit(tree)
    violations = collector.violations + _check_tool_meta(tree)

    # Step 3: Calculate score
    score = 100
    for v in violations:
        if v["type"].startswith("tier1"):
            score -= 30
        elif v["type"].startswith("tier2"):
            score -= 25
        elif v["type"] == "missing_tool_meta":
            score -= 15
        else:
            score -= 10
    score = max(0, score)

    passed = len(violations) == 0

    result = {
        "trace_id": trace_id,
        "score": score,
        "passed": passed,
        "violations": violations,
        "violation_count": len(violations),
    }

    # If violations found, generate A2A feedback
    if violations:
        result["a2a_feedback"] = _build_a2a_feedback(trace_id, violations)

    logger.info("Audit complete: score=%d passed=%s violations=%d trace_id=%s",
                score, passed, len(violations), trace_id)
    return _wrap("ok", result)

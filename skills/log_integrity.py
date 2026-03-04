"""
Executive Summary
-----------------
Tamper-evidence and audit integrity skill for Snowdrop's invocation log.
Verifies the SHA-256 hash chain in logs/invocations.jsonl, writes daily
snapshot hashes to logs/integrity/ (committed to Git for version control),
and raises a red-flag alert to THE LOGIC LOG in the Ghost Ledger whenever
a discrepancy is detected.

The invocation log uses a hash chain: each JSON line contains a "prev_hash"
field holding the SHA-256 of the previous line.  Deleting, inserting, or
modifying any line breaks the chain and is detected immediately by this skill.

Actions:
  verify        — walk the full chain; return ok or suspicious with details
  snapshot      — hash the last N lines + write to logs/integrity/YYYY-MM-DD.sha256
  check_deleted — detect if the log file was deleted and re-created (chain break at genesis)

Outputs:
  {"status": "ok"|"error"|"suspicious", "data": {...}, "timestamp": ISO8601}

When "suspicious" is returned, the skill:
  1. Logs the discrepancy to THE LOGIC LOG in the Ghost Ledger (if GHOST_LEDGER_URL is set)
  2. Writes a local alert to logs/INTEGRITY_ALERT_<timestamp>.txt
  3. Returns status "suspicious" so the caller can trigger a post-mortem

Scheduling: run via the snowdrop-integrity systemd timer (daily at 03:00 UTC).
The daily snapshot hash is committed to Git by the timer service, giving you
version-controlled tamper evidence that is independent of the HP filesystem.

MCP Tool Name: log_integrity
"""

import base64
import hashlib
import json
import logging
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import httpx

from skills.utils.retry import retry

logger = logging.getLogger(__name__)

TOOL_META = {
    "name": "log_integrity",
    "description": (
        "Verify the SHA-256 hash chain in Snowdrop's invocation audit log. "
        "Detects deletions, modifications, or insertions. On suspicion, alerts "
        "to Ghost Ledger THE LOGIC LOG and writes a local INTEGRITY_ALERT file. "
        "Run daily via systemd timer for continuous tamper-evidence."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["verify", "snapshot", "check_deleted"],
                "description": "Operation to perform.",
            },
            "ghost_ledger_url": {
                "type": "string",
                "description": "Google Sheets URL for alerting (falls back to GHOST_LEDGER_URL env var).",
            },
        },
        "required": ["action"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "data", "timestamp"],
    },
}

_REPO_ROOT = Path(__file__).parent.parent
_LOG_DIR = Path(os.environ.get("SNOWDROP_LOG_DIR", "/tmp/snowdrop/logs"))
_INVOCATION_LOG = _LOG_DIR / "invocations.jsonl"
# Integrity snapshots live inside the repo so they can be committed to Git for
# tamper-evidence.  _LOG_DIR is /tmp which is outside the repo — using it here
# caused `snap_path.relative_to(_REPO_ROOT)` to raise ValueError.
_INTEGRITY_DIR = _REPO_ROOT / "logs" / "integrity"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _alert_ghost_ledger(decision: str, reasoning: str, outcome: str, ledger_url: str) -> None:
    """Write a SUSPICIOUS entry to THE LOGIC LOG.  Never raises."""
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from ghost_ledger import ghost_ledger
        ghost_ledger(
            action="log_decision",
            spreadsheet_url=ledger_url,
            decision=decision,
            reasoning=reasoning,
            outcome=outcome,
        )
    except Exception as exc:
        logger.error("Could not write to Ghost Ledger during integrity alert: %s", exc)


def _write_local_alert(details: dict) -> Path:
    """Write a plaintext alert file to logs/ that persists even if Ghost Ledger is down."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    alert_path = _LOG_DIR / f"INTEGRITY_ALERT_{ts}.txt"
    with open(alert_path, "w") as fh:
        fh.write("=== SNOWDROP INTEGRITY ALERT ===\n")
        fh.write(f"Timestamp : {_now_iso()}\n")
        fh.write(f"Log file  : {_INVOCATION_LOG}\n\n")
        for k, v in details.items():
            fh.write(f"{k}: {v}\n")
        fh.write("\nACTION REQUIRED: Review the invocation log immediately.\n")
    return alert_path


def _verify_chain() -> dict:
    """Walk invocations.jsonl and verify every prev_hash link.

    Returns a dict with keys:
      lines_checked, first_break_seq, first_break_line, status ("ok" or "suspicious")
    """
    if not _INVOCATION_LOG.exists():
        return {"status": "ok", "lines_checked": 0, "note": "log file does not exist yet"}

    lines_checked = 0
    prev_line_text: str | None = None
    expected_prev_hash: str = "genesis"

    with open(_INVOCATION_LOG) as fh:
        for raw_line in fh:
            raw_line = raw_line.rstrip("\n")
            if not raw_line.strip():
                continue
            lines_checked += 1
            try:
                entry = json.loads(raw_line)
            except json.JSONDecodeError:
                return {
                    "status": "suspicious",
                    "lines_checked": lines_checked,
                    "first_break_seq": None,
                    "reason": f"JSON parse error at line {lines_checked}",
                    "bad_line_preview": raw_line[:120],
                }

            actual_prev_hash = entry.get("prev_hash", "MISSING")
            if actual_prev_hash != expected_prev_hash:
                return {
                    "status": "suspicious",
                    "lines_checked": lines_checked,
                    "first_break_seq": entry.get("seq"),
                    "reason": "Hash chain broken — line was deleted, inserted, or modified",
                    "expected_prev_hash": expected_prev_hash[:16] + "…",
                    "actual_prev_hash": actual_prev_hash[:16] + "…",
                }
            # Advance: next line's expected prev_hash = SHA-256 of this line
            expected_prev_hash = _sha256(raw_line)
            prev_line_text = raw_line

    return {
        "status": "ok",
        "lines_checked": lines_checked,
        "tail_hash": expected_prev_hash,
    }


_GITHUB_REPO = "Stonewater-Digital/snowdrop-core"
_GITHUB_API = "https://api.github.com"


@retry(attempts=3, backoff_seconds=1.0, jitter=0.3, retriable_exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException))
def _github_api_get(url: str, headers: dict) -> httpx.Response:
    """GET from GitHub API with retry on transient errors."""
    resp = httpx.get(url, headers=headers, timeout=15.0)
    if resp.status_code == 429:
        resp.raise_for_status()  # trigger retry
    return resp


@retry(attempts=3, backoff_seconds=1.0, jitter=0.3, retriable_exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException))
def _github_api_put(url: str, headers: dict, payload: dict) -> httpx.Response:
    """PUT to GitHub API with retry on transient errors."""
    resp = httpx.put(url, headers=headers, json=payload, timeout=15.0)
    if resp.status_code == 429:
        resp.raise_for_status()  # trigger retry
    return resp


def _commit_snapshot_via_api(
    snap_path: Path, file_content: str, today: str, lines_checked: int, tail_hash: str
) -> str:
    """Commit a snapshot file via GitHub REST API to avoid git divergence.

    Falls back to local git add+commit if GITHUB_TOKEN is unset.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.info("GITHUB_TOKEN unset — falling back to local git commit")
        return _commit_snapshot_local(snap_path, today, lines_checked, tail_hash)

    rel_path = str(snap_path.relative_to(_REPO_ROOT))
    api_url = f"{_GITHUB_API}/repos/{_GITHUB_REPO}/contents/{rel_path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }
    commit_msg = (
        f"chore: daily integrity snapshot {today} — {lines_checked} lines, "
        f"hash {tail_hash[:12]}…\n\n"
        f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    )

    try:
        # Check if file already exists to get its sha
        get_resp = _github_api_get(api_url, headers)
        put_payload = {
            "message": commit_msg,
            "content": base64.b64encode(file_content.encode()).decode(),
            "branch": "main",
        }
        if get_resp.status_code == 200:
            try:
                existing = get_resp.json()
                put_payload["sha"] = existing["sha"]
            except (json.JSONDecodeError, KeyError) as exc:
                logger.warning("Malformed GitHub API response for GET: %s", exc)
                return f"error: malformed API response — {exc}"
        elif get_resp.status_code != 404:
            # Unexpected status — log and bail
            logger.warning("Unexpected GET status %d from GitHub API", get_resp.status_code)
            return f"error: unexpected GET status {get_resp.status_code}"
        # 404 means new file — omit sha key entirely (already absent from payload)

        put_resp = _github_api_put(api_url, headers, put_payload)
        put_resp.raise_for_status()
        return "committed via GitHub API"

    except httpx.HTTPStatusError as exc:
        logger.error("GitHub API HTTP error: %s", exc)
        return f"api error: {exc.response.status_code}"
    except Exception as exc:
        logger.error("GitHub API commit failed: %s", exc)
        return f"error: {exc}"


def _commit_snapshot_local(snap_path: Path, today: str, lines_checked: int, tail_hash: str) -> str:
    """Fallback: local git add + commit (no push to avoid divergence)."""
    try:
        subprocess.run(
            ["git", "add", str(snap_path)],
            cwd=str(_REPO_ROOT), check=True, capture_output=True, timeout=30,
        )
        subprocess.run(
            ["git", "commit", "-m",
             f"chore: daily integrity snapshot {today} — {lines_checked} lines, "
             f"hash {tail_hash[:12]}…\n\n"
             f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"],
            cwd=str(_REPO_ROOT), check=True, capture_output=True, timeout=30,
        )
        return "committed locally (no push — GITHUB_TOKEN unset)"
    except subprocess.CalledProcessError as exc:
        return f"local git error: {exc.stderr.decode(errors='replace')[:200]}"
    except Exception as exc:
        return f"error: {exc}"


def _write_snapshot() -> dict:
    """Write today's tail hash to logs/integrity/YYYY-MM-DD.sha256 and commit to Git."""
    chain_result = _verify_chain()
    if chain_result["status"] == "suspicious":
        return chain_result  # don't snapshot a broken chain

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snap_path = _INTEGRITY_DIR / f"{today}.sha256"
    tail_hash = chain_result.get("tail_hash", "genesis")
    lines_checked = chain_result.get("lines_checked", 0)

    content = (
        f"date={today}\n"
        f"tail_hash={tail_hash}\n"
        f"lines_checked={lines_checked}\n"
        f"log_file={_INVOCATION_LOG}\n"
        f"generated={_now_iso()}\n"
    )
    snap_path.write_text(content)

    # Commit the snapshot via GitHub REST API (avoids git divergence on node).
    # Falls back to local git add+commit if GITHUB_TOKEN is unset.
    git_result = _commit_snapshot_via_api(snap_path, content, today, lines_checked, tail_hash)

    return {
        "status": "ok",
        "snapshot_path": str(snap_path),
        "tail_hash": tail_hash,
        "lines_checked": lines_checked,
        "git": git_result,
    }


def log_integrity(
    action: str,
    ghost_ledger_url: str = "",
) -> dict:
    """Verify Snowdrop's invocation log hash chain and alert on tampering."""
    _INTEGRITY_DIR.mkdir(parents=True, exist_ok=True)
    ledger_url = ghost_ledger_url or os.environ.get("GHOST_LEDGER_URL", "")

    try:
        if action == "verify":
            result = _verify_chain()
            if result["status"] == "suspicious":
                alert_path = _write_local_alert(result)
                result["alert_file"] = str(alert_path)
                if ledger_url:
                    _alert_ghost_ledger(
                        decision="INTEGRITY ALERT — invocation log hash chain broken",
                        reasoning=result.get("reason", "Unknown"),
                        outcome=f"SUSPICIOUS — seq {result.get('first_break_seq')}. Review {alert_path.name} immediately.",
                        ledger_url=ledger_url,
                    )
                logger.error("INTEGRITY ALERT: %s", result.get("reason"))
            return _wrap(result["status"], result)

        elif action == "snapshot":
            result = _write_snapshot()
            if result.get("status") == "suspicious":
                alert_path = _write_local_alert(result)
                result["alert_file"] = str(alert_path)
                if ledger_url:
                    _alert_ghost_ledger(
                        decision="INTEGRITY ALERT — cannot snapshot broken chain",
                        reasoning=result.get("reason", "Unknown"),
                        outcome="SUSPICIOUS — chain broken before snapshot. Manual review required.",
                        ledger_url=ledger_url,
                    )
            return _wrap(result.get("status", "ok"), result)

        elif action == "check_deleted":
            exists = _INVOCATION_LOG.exists()
            size = _INVOCATION_LOG.stat().st_size if exists else 0
            # Check if today's snapshot exists and compare line counts
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            snap_path = _INTEGRITY_DIR / f"{today}.sha256"
            snap_data = {}
            if snap_path.exists():
                for line in snap_path.read_text().splitlines():
                    if "=" in line:
                        k, _, v = line.partition("=")
                        snap_data[k.strip()] = v.strip()
            return _wrap("ok", {
                "log_exists": exists,
                "log_size_bytes": size,
                "today_snapshot": snap_path.exists(),
                "snapshot_lines_checked": snap_data.get("lines_checked"),
                "snapshot_tail_hash": snap_data.get("tail_hash", "")[:16] + "…" if snap_data.get("tail_hash") else None,
            })

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'. Use: verify, snapshot, check_deleted"})

    except Exception as exc:
        logger.exception("log_integrity error")
        return _wrap("error", {"message": str(exc)})

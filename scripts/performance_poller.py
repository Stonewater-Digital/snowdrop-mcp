#!/usr/bin/env python3
"""
Snowdrop Performance Poller — A2A-compliant autonomous subagent.

Runs every 2 hours via cron on snowdrop-node. Polls Moltbook API for upvotes
and comments on all posts in POST LOG, writes to POST PERFORMANCE and
SUBMOLT PERFORMANCE tabs in Google Sheet.

Crontab entry:
    0 */2 * * * /home/snowdrop/snowdrop-core/venv/bin/python /home/snowdrop/snowdrop-mcp/scripts/performance_poller.py >> /tmp/performance_poller.log 2>&1

A2A agent card: https://snowdrop-mcp.fly.dev/.well-known/agent-performance-poller.json
"""
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import uuid4

import requests

# ── Path setup ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT))

STATE_FILE = REPO_ROOT / "state" / "poller_state.json"
LOG_FILE = Path("/tmp/performance_poller.log")

# ── Config ───────────────────────────────────────────────────────────────────
AGENT_ID = "performance-poller/1.0"
MOLTBOOK_BASE = os.environ.get("MOLTBOOK_BASE_URL", "https://www.moltbook.com")
MAX_POSTS_PER_RUN = 60          # rate-limit guard
REPOLL_HOURS = 2                # don't re-poll posts polled within this many hours
ROI_GRADE_THRESHOLDS = {        # avg upvotes → grade
    5.0: "A",
    2.0: "B",
    0.5: "C",
    0.0: "D",
}


# ── Structured logging ───────────────────────────────────────────────────────
def _log(run_id: str, action: str, **kwargs):
    entry = {
        "run_id": run_id,
        "agent": AGENT_ID,
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        **kwargs,
    }
    print(json.dumps(entry), flush=True)


# ── State management ─────────────────────────────────────────────────────────
def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {
        "last_run": None,
        "last_run_id": None,
        "run_count": 0,
        "total_posts_polled": 0,
        "posts_polled_last_run": 0,
        "polled_at": {},      # {post_id: ISO8601 timestamp of last poll}
        "errors_last_run": [],
    }


def _save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── Moltbook API ─────────────────────────────────────────────────────────────
def _get_headers() -> dict:
    token = os.environ.get("MOLTBOOK_API_TOKEN", "")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _fetch_post_metrics(post_id: str) -> dict | None:
    """Return {upvotes, comments} for a post or None on error."""
    try:
        resp = requests.get(
            f"{MOLTBOOK_BASE}/api/v1/posts/{post_id}",
            headers=_get_headers(),
            timeout=10,
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        post = resp.json()
        upvotes = post.get("upvotes", post.get("score", 0)) or 0
        comments = post.get("comments_count", post.get("num_comments", 0)) or 0
        return {
            "upvotes": upvotes,
            "comments": comments,
            "submolt": post.get("submolt", post.get("community", "")),
            "title": (post.get("title", "") or "")[:100],
        }
    except Exception:
        return None


# ── Google Sheet helpers ─────────────────────────────────────────────────────
def _get_sheet_client():
    """Return authenticated gspread client."""
    import gspread
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if sa_json and sa_json.strip().startswith("{"):
        return gspread.service_account_from_dict(json.loads(sa_json))
    if sa_json and os.path.exists(sa_json):
        return gspread.service_account(filename=sa_json)
    creds_path = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
    if creds_path and os.path.exists(creds_path):
        return gspread.service_account(filename=creds_path)
    raise ValueError("No Google service account credentials found")


SHEET_ID = "1dpOdvas07uS4sB80BAS_nG8eDNbHdgzpDsVdf6C-tbI"


def _read_post_log(sheet) -> list[dict]:
    """Return list of {post_id, submolt, title, url} from POST LOG."""
    ws = sheet.worksheet("POST LOG")
    rows = ws.get_all_records()
    posts = []
    for r in rows:
        pid = str(r.get("Post ID", "")).strip()
        if pid:
            posts.append({
                "post_id": pid,
                "submolt": r.get("Submolt", ""),
                "title": r.get("Title", ""),
                "url": r.get("URL", ""),
            })
    return posts


def _read_polled_ids(sheet) -> dict[str, str]:
    """Return {post_id: date_polled} from POST PERFORMANCE tab."""
    ws = sheet.worksheet("POST PERFORMANCE")
    rows = ws.get_all_records()
    # Expect cols: Post ID, Submolt, Title, Upvotes, Comments, ROI Score, Date Polled
    return {
        str(r.get("Post ID", "")): str(r.get("Date Polled", ""))
        for r in rows
        if r.get("Post ID")
    }


def _upsert_performance(sheet, post_id: str, submolt: str, title: str,
                         upvotes: int, comments: int, roi_score: int, date_polled: str):
    """Upsert a row in POST PERFORMANCE. Column order: A-G."""
    ws = sheet.worksheet("POST PERFORMANCE")
    all_vals = ws.get_all_values()
    new_row = [post_id, submolt, title[:100], upvotes, comments, roi_score, date_polled]

    target = None
    for i, row in enumerate(all_vals[1:], start=2):
        if row and str(row[0]) == post_id:
            target = i
            break

    if target:
        ws.update(f"A{target}:G{target}", [new_row])
    else:
        ws.append_row(new_row, value_input_option="USER_ENTERED")


def _recompute_submolt_perf(sheet, performance_rows: list[dict]):
    """Aggregate per-submolt stats and upsert SUBMOLT PERFORMANCE."""
    ws = sheet.worksheet("SUBMOLT PERFORMANCE")
    all_vals = ws.get_all_values()

    agg = defaultdict(lambda: {"upvotes": [], "comments": [], "post_ids": []})
    for r in performance_rows:
        sub = r.get("submolt", "")
        if sub:
            agg[sub]["upvotes"].append(r["upvotes"])
            agg[sub]["comments"].append(r["comments"])
            agg[sub]["post_ids"].append(r["post_id"])

    date_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for submolt, stats in agg.items():
        n = len(stats["upvotes"])
        if n == 0:
            continue
        total_up = sum(stats["upvotes"])
        total_co = sum(stats["comments"])
        avg_up = total_up / n
        avg_co = total_co / n

        # ROI grade
        grade = "F"
        for threshold, g in sorted(ROI_GRADE_THRESHOLDS.items(), reverse=True):
            if avg_up >= threshold:
                grade = g
                break

        # Best post = highest roi_score (upvotes*2 + comments*5)
        best_idx = max(
            range(n),
            key=lambda i: stats["upvotes"][i] * 2 + stats["comments"][i] * 5
        )
        best_post = stats["post_ids"][best_idx]

        new_row = [
            submolt, n, total_up, total_co,
            round(avg_up, 2), round(avg_co, 2),
            best_post, grade, date_now
        ]

        target = None
        for i, row in enumerate(all_vals[1:], start=2):
            if row and str(row[0]).lower() == submolt.lower():
                target = i
                break

        if target:
            ws.update(f"A{target}:I{target}", [new_row])
        else:
            ws.append_row(new_row, value_input_option="USER_ENTERED")

        # Keep all_vals current for subsequent submolts
        while len(all_vals) < target or target is None:
            all_vals.append([])


def _update_weekly_actual_engagement(sheet, total_comments: int, total_upvotes: int):
    """Fill in engagement_actual for the current week in WEEKLY FORECAST."""
    ws = sheet.worksheet("WEEKLY FORECAST")
    rows = ws.get_all_values()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for i, row in enumerate(rows[1:], start=2):
        if len(row) >= 2 and row[0] <= today <= row[1]:
            engagement_actual = total_upvotes + total_comments
            ws.update_cell(i, 6, engagement_actual)
            break


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    run_id = str(uuid4())
    start_time = time.time()
    state = _load_state()
    errors = []

    _log(run_id, "start", run_count=state["run_count"] + 1)

    try:
        gc = _get_sheet_client()
        sheet = gc.open_by_key(SHEET_ID)
    except Exception as e:
        _log(run_id, "error", stage="auth", error=str(e))
        state["errors_last_run"] = [str(e)]
        _save_state(state)
        return

    # Read all posts from POST LOG
    try:
        post_log = _read_post_log(sheet)
        _log(run_id, "read_post_log", total_posts=len(post_log))
    except Exception as e:
        _log(run_id, "error", stage="read_post_log", error=str(e))
        return

    # Read already-polled posts
    try:
        polled_map = _read_polled_ids(sheet)
    except Exception as e:
        _log(run_id, "warning", stage="read_polled_ids", error=str(e))
        polled_map = {}

    # Determine which posts to poll this run
    now = datetime.now(timezone.utc)
    repoll_cutoff = (now - timedelta(hours=REPOLL_HOURS)).strftime("%Y-%m-%d")
    is_first_run = state["run_count"] == 0

    to_poll = []
    for p in post_log:
        pid = p["post_id"]
        last_polled = polled_map.get(pid, "")
        if is_first_run or not last_polled or last_polled < repoll_cutoff:
            to_poll.append(p)
        if len(to_poll) >= MAX_POSTS_PER_RUN:
            break

    _log(run_id, "polling_plan", to_poll=len(to_poll), is_first_run=is_first_run)

    # Poll each post and upsert
    polled_results = []
    date_polled = now.strftime("%Y-%m-%d")

    for p in to_poll:
        pid = p["post_id"]
        metrics = _fetch_post_metrics(pid)
        if metrics is None:
            errors.append({"post_id": pid, "error": "not found or API error"})
            _log(run_id, "poll_error", post_id=pid)
            continue

        upvotes = metrics["upvotes"]
        comments = metrics["comments"]
        roi_score = upvotes * 2 + comments * 5
        submolt = metrics.get("submolt") or p.get("submolt", "")
        title = metrics.get("title") or p.get("title", "")

        try:
            _upsert_performance(sheet, pid, submolt, title, upvotes, comments, roi_score, date_polled)
        except Exception as e:
            errors.append({"post_id": pid, "error": str(e)})
            _log(run_id, "upsert_error", post_id=pid, error=str(e))
            continue

        polled_results.append({
            "post_id": pid,
            "submolt": submolt,
            "upvotes": upvotes,
            "comments": comments,
            "roi_score": roi_score,
        })
        _log(run_id, "polled", post_id=pid, submolt=submolt, upvotes=upvotes, comments=comments, roi=roi_score)
        time.sleep(0.3)  # gentle rate limiting

    # Recompute SUBMOLT PERFORMANCE from full POST PERFORMANCE data
    if polled_results:
        try:
            # Read full POST PERFORMANCE for accurate aggregation
            ws_perf = sheet.worksheet("POST PERFORMANCE")
            all_perf = ws_perf.get_all_records()
            full_perf = [
                {
                    "post_id": str(r.get("Post ID", "")),
                    "submolt": r.get("Submolt", ""),
                    "upvotes": int(r.get("Upvotes", 0) or 0),
                    "comments": int(r.get("Comments", 0) or 0),
                }
                for r in all_perf
                if r.get("Post ID")
            ]
            _recompute_submolt_perf(sheet, full_perf)
            _log(run_id, "submolt_perf_updated", submolts=len(set(r["submolt"] for r in full_perf)))
        except Exception as e:
            errors.append({"stage": "submolt_perf", "error": str(e)})
            _log(run_id, "error", stage="submolt_perf", error=str(e))

    # Update WEEKLY FORECAST engagement_actual
    if polled_results:
        try:
            total_up = sum(r["upvotes"] for r in polled_results)
            total_co = sum(r["comments"] for r in polled_results)
            _update_weekly_actual_engagement(sheet, total_co, total_up)
        except Exception as e:
            _log(run_id, "warning", stage="weekly_forecast", error=str(e))

    # Save state
    elapsed = round(time.time() - start_time, 1)
    state["last_run"] = now.isoformat()
    state["last_run_id"] = run_id
    state["run_count"] = state.get("run_count", 0) + 1
    state["posts_polled_last_run"] = len(polled_results)
    state["total_posts_polled"] = state.get("total_posts_polled", 0) + len(polled_results)
    state["errors_last_run"] = errors
    # Track individual poll timestamps
    for r in polled_results:
        state.setdefault("polled_at", {})[r["post_id"]] = now.isoformat()
    _save_state(state)

    _log(run_id, "complete",
         posts_polled=len(polled_results),
         errors=len(errors),
         total_time_s=elapsed)


if __name__ == "__main__":
    # Load .env if present
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

    main()

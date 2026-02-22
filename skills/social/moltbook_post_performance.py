"""
Moltbook Post Performance skill — fetch live upvotes and comments for any post.

Spot-check individual posts or verify the performance poller is working correctly.
ROI score = upvotes * 2 + comments * 5 (comments weighted higher for community signal).
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "moltbook_post_performance",
    "description": (
        "Fetch live upvotes and comments for one or more Moltbook posts by post_id. "
        "Returns engagement metrics, ROI score (upvotes*2 + comments*5), and traction status. "
        "Use for spot-checking specific posts or verifying the performance poller is working. "
        "Set write_to_sheet=True to also upsert results into the POST PERFORMANCE tab."
    ),
}

MOLTBOOK_BASE = os.environ.get("MOLTBOOK_BASE_URL", "https://www.moltbook.com")


def moltbook_post_performance(post_ids: list, write_to_sheet: bool = False) -> dict:
    """
    Fetch live upvotes and comments for Moltbook posts.

    Args:
        post_ids: List of Moltbook post ID strings to fetch metrics for
        write_to_sheet: If True, upsert results into POST PERFORMANCE tab in Google Sheet
    """
    ts = datetime.now(timezone.utc).isoformat()
    token = os.environ.get("MOLTBOOK_API_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    if not post_ids:
        return {
            "status": "error",
            "data": {"message": "post_ids list is empty"},
            "timestamp": ts,
        }

    results = []
    errors = []

    for post_id in post_ids:
        try:
            resp = requests.get(
                f"{MOLTBOOK_BASE}/api/v1/posts/{post_id}",
                headers=headers,
                timeout=10,
            )
            if resp.status_code == 404:
                errors.append({"post_id": post_id, "error": "not found"})
                continue
            resp.raise_for_status()
            post = resp.json()

            upvotes = post.get("upvotes", post.get("score", 0)) or 0
            comments = post.get("comments_count", post.get("num_comments", 0)) or 0
            roi_score = upvotes * 2 + comments * 5

            traction = "strong" if roi_score >= 20 else ("gaining" if roi_score >= 5 else "minimal")

            result = {
                "post_id": post_id,
                "submolt": post.get("submolt", post.get("community", "")),
                "title": (post.get("title", "") or "")[:80],
                "upvotes": upvotes,
                "comments": comments,
                "roi_score": roi_score,
                "traction": traction,
                "created_at": post.get("created_at", post.get("created", "")),
            }
            results.append(result)

        except Exception as e:
            errors.append({"post_id": post_id, "error": str(e)})

    # Optionally write to Google Sheet
    if write_to_sheet and results:
        try:
            from skills.social.moltbook_engagement_sheet import moltbook_engagement_sheet
            date_polled = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            for r in results:
                moltbook_engagement_sheet(
                    action="update_performance",
                    data={
                        "post_id": r["post_id"],
                        "submolt": r["submolt"],
                        "title": r["title"],
                        "upvotes": r["upvotes"],
                        "comments": r["comments"],
                        "roi_score": r["roi_score"],
                        "date_polled": date_polled,
                    },
                )
        except Exception as e:
            errors.append({"sheet_write": str(e)})

    total_upvotes = sum(r["upvotes"] for r in results)
    total_comments = sum(r["comments"] for r in results)
    avg_roi = round(sum(r["roi_score"] for r in results) / len(results), 2) if results else 0

    return {
        "status": "ok",
        "data": {
            "posts": results,
            "polled": len(results),
            "errors": errors,
            "summary": {
                "total_upvotes": total_upvotes,
                "total_comments": total_comments,
                "avg_roi_score": avg_roi,
            },
        },
        "timestamp": ts,
    }

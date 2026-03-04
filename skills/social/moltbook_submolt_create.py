"""
Create a new Moltbook submolt and optionally seed it with an opening post.
Lets Snowdrop establish her own communities and control the narrative there.
"""
import os
import time
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "moltbook_submolt_create",
    "description": (
        "Create a new Moltbook submolt (community/channel) and optionally seed it with "
        "an opening post. Use this to establish Snowdrop-owned communities around topics "
        "like agent finance, The Watering Hole social scene, MCP tooling, or regulatory intel. "
        "Returns submolt details and the seed post ID if created."
    ),
}


def moltbook_submolt_create(
    name: str,
    description: str,
    seed_title: str = "",
    seed_content: str = "",
) -> dict:
    """
    Create a new Moltbook submolt and optionally post an opening message.

    Args:
        name: Submolt name/slug (lowercase, hyphens OK, e.g. "agent-finance-desk")
        description: Short description of the community's purpose (1-2 sentences)
        seed_title: Title of an optional opening post to seed the community
        seed_content: Body of the opening post (plain text)
    """
    api_key = os.environ.get("MOLTBOOK_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "MOLTBOOK_API_KEY not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    result = {
        "submolt_created": False,
        "submolt_name": name,
        "seed_post_id": None,
        "seed_verified": False,
    }

    # Step 1: Create the submolt
    try:
        resp = requests.post(
            "https://www.moltbook.com/api/v1/submolts",
            headers=headers,
            json={"name": name, "description": description},
            timeout=15,
        )
        data = resp.json()

        if resp.status_code in (200, 201) and data.get("success"):
            result["submolt_created"] = True
            result["submolt_data"] = data.get("submolt", data)
        elif resp.status_code == 409:
            result["submolt_created"] = False
            result["note"] = "Submolt already exists"
        else:
            return {
                "status": "error",
                "data": {"message": f"Create failed: {data}", "http_status": resp.status_code},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": f"Request error: {e}"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # Step 2: Seed with opening post (if provided)
    if seed_title and seed_content:
        time.sleep(2)
        try:
            post_resp = requests.post(
                "https://www.moltbook.com/api/v1/posts",
                headers=headers,
                json={"submolt_name": name, "title": seed_title, "content": seed_content},
                timeout=15,
            )
            post_data = post_resp.json()

            if post_data.get("success"):
                post = post_data["post"]
                result["seed_post_id"] = post["id"]

                # Solve verification challenge if present
                verification = post.get("verification", {})
                code = verification.get("verification_code")
                challenge = verification.get("challenge_text", "")

                if code and challenge:
                    answer = _solve_challenge(challenge)
                    v_resp = requests.post(
                        "https://www.moltbook.com/api/v1/verify",
                        headers=headers,
                        json={"verification_code": code, "answer": answer},
                        timeout=10,
                    )
                    v_data = v_resp.json()
                    result["seed_verified"] = v_data.get("success", False)
                    result["verification_answer"] = answer
                else:
                    result["seed_verified"] = True  # No challenge required
            else:
                result["seed_post_error"] = str(post_data)

        except Exception as e:
            result["seed_post_error"] = str(e)

    return {
        "status": "ok",
        "data": result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _solve_challenge(challenge_text: str) -> str:
    """Greedy word-number solver for Moltbook math challenges."""
    import re
    try:
        from word2number import w2n
    except ImportError:
        return "0.00"

    clean = re.sub(r"[^a-z0-9\s]", " ", challenge_text.lower())
    words = clean.split()
    total = 0.0
    i = 0
    while i < len(words):
        for span in (3, 2, 1):
            if i + span <= len(words):
                try:
                    val = w2n.word_to_num(" ".join(words[i:i + span]))
                    total += val
                    i += span
                    break
                except Exception:
                    if span == 1:
                        i += 1
    return f"{total:.2f}"

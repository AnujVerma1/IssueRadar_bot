"""
filters.py — Deterministic filter engine.
Every check is based solely on config values; no AI or LLMs are used.
"""

from datetime import datetime, timezone
import config


def _lower_list(items: list[str]) -> list[str]:
    """Return a lowercased copy of a list of strings."""
    return [s.lower() for s in items]


def passes_all_filters(issue: dict, repo_info: dict | None) -> bool:
    """
    Return True only if *issue* satisfies every enabled filter in config.FILTERS.
    Any single failure rejects the issue immediately.
    """
    f = config.FILTERS
    labels = _lower_list([lbl["name"] for lbl in issue.get("labels", [])])

    # 1. Open only
    if f.get("open_only") and issue.get("state") != "open":
        return False

    # 2. Unassigned only
    if f.get("unassigned_only") and issue.get("assignee") is not None:
        return False

    # 3. Max comments
    max_comments = f.get("max_comments")
    if max_comments is not None:
        if issue.get("comments", 0) > max_comments:
            return False

    # 4. Beginner-friendly label requirement
    if f.get("beginner_friendly_only"):
        beginner_labels = _lower_list(f.get("beginner_labels", []))
        mode = f.get("label_match_mode", "any")

        if mode == "all":
            if not all(bl in labels for bl in beginner_labels):
                return False
        else:  # "any"
            if not any(bl in labels for bl in beginner_labels):
                return False

    # 5. Required labels (all must be present)
    required = f.get("required_labels", [])
    if required:
        required_lower = _lower_list(required)
        if not all(rl in labels for rl in required_lower):
            return False

    # 6. Programming language filter
    languages = f.get("languages", [])
    if languages and repo_info:
        repo_lang = (repo_info.get("language") or "").lower()
        if repo_lang not in _lower_list(languages):
            return False

    # 7. Include keywords (all must appear in title or body)
    include_kw = f.get("include_keywords", [])
    if include_kw:
        text = (issue.get("title", "") + " " + (issue.get("body") or "")).lower()
        if not all(kw.lower() in text for kw in include_kw):
            return False

    # 8. Exclude keywords (none may appear in title or body)
    exclude_kw = f.get("exclude_keywords", [])
    if exclude_kw:
        text = (issue.get("title", "") + " " + (issue.get("body") or "")).lower()
        if any(kw.lower() in text for kw in exclude_kw):
            return False

    # 9. Max issue age
    max_age = f.get("max_issue_age_hours")
    if max_age is not None:
        created_str = issue.get("created_at", "")
        if created_str:
            created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
            age_hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600
            if age_hours > max_age:
                return False

    # 10. Minimum repository stars
    min_stars = f.get("min_repo_stars")
    if min_stars is not None and repo_info:
        if repo_info.get("stargazers_count", 0) < min_stars:
            return False

    return True

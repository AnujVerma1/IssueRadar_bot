"""
github_client.py — Fetch issues and repo metadata from the GitHub REST API.
"""

import requests
import config

# GitHub API base URL
API_BASE = "https://api.github.com"

# Reusable session for connection pooling
_session = requests.Session()


def _headers() -> dict:
    """Build request headers, optionally including an auth token."""
    headers = {"Accept": "application/vnd.github+json"}
    if config.GITHUB_TOKEN:
        headers["Authorization"] = f"token {config.GITHUB_TOKEN}"
    return headers


def fetch_open_issues(repo: str, per_page: int = 100) -> list[dict]:
    """
    Fetch the most recent open issues for *repo* (e.g. "owner/name").
    Returns a list of issue dicts from the GitHub API.
    Pull requests are excluded (they also appear in the issues endpoint).
    """
    url = f"{API_BASE}/repos/{repo}/issues"
    params = {
        "state": "open",
        "sort": "created",
        "direction": "desc",
        "per_page": per_page,
    }

    try:
        response = _session.get(url, headers=_headers(), params=params, timeout=30)
        response.raise_for_status()
        issues = response.json()

        # GitHub's issues endpoint also returns pull requests — filter them out.
        return [issue for issue in issues if "pull_request" not in issue]

    except requests.RequestException as exc:
        print(f"  [ERROR] Failed to fetch issues for {repo}: {exc}")
        return []


def fetch_repo_info(repo: str) -> dict | None:
    """Fetch repository metadata (stars, language, etc.)."""
    url = f"{API_BASE}/repos/{repo}"

    try:
        response = _session.get(url, headers=_headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        print(f"  [ERROR] Failed to fetch repo info for {repo}: {exc}")
        return None

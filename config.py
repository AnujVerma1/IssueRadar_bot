"""
IssueRadar Configuration
========================
Edit this file to customize which GitHub issues trigger Telegram notifications.
"""

# ---------------------------------------------------------------------------
# Telegram Bot Settings
# ---------------------------------------------------------------------------
# 1. Create a bot via @BotFather on Telegram and paste the token below.
# 2. Send a message to your bot, then visit:
#    https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
#    to find your chat_id.
TELEGRAM_BOT_TOKEN = "9076037493:AAE8zlHafLUpPO262CZc5s6bl3Efo5nNNr8"
TELEGRAM_CHAT_ID = "1934300357"

# ---------------------------------------------------------------------------
# GitHub Settings (optional)
# ---------------------------------------------------------------------------
# A personal access token increases the rate limit from 60 to 5 000 req/hour.
# Leave empty to use unauthenticated requests.
GITHUB_TOKEN = ""

# ---------------------------------------------------------------------------
# Repositories to Monitor
# ---------------------------------------------------------------------------
TARGET_REPOSITORIES = [
    "docling-project/docling",
    "infiniflow/ragflow",
    "qdrant/fastembed",
    "Unstructured-IO/unstructured",
]

# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------
SCHEDULER = {
    "interval_minutes": 2,
}

# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
# Every filter is optional. Remove or set to None / empty to disable it.
FILTERS = {
    # Only consider open issues.
    "open_only": True,

    # Only consider issues with no assignee.
    "unassigned_only": True,

    # Maximum number of comments allowed (inclusive). Set to None to disable.
    "max_comments": 0,

    # Require at least one beginner-friendly label.
    "beginner_friendly_only": True,

    # Labels considered beginner-friendly (case-insensitive comparison).
    "beginner_labels": [
        "good first issue",
        "beginner",
        "beginner-friendly",
        "easy",
    ],

    # How beginner_labels are matched: "any" = at least one, "all" = every one.
    "label_match_mode": "any",

    # Require ALL of these labels to be present (case-insensitive).
    # Example: ["bug", "help wanted"]
    "required_labels": [],

    # Programming languages to include (case-insensitive).
    # Checked against the repository's primary language.
    # Example: ["python", "javascript"]
    "languages": [],

    # Keywords that MUST appear in the issue title or body (case-insensitive).
    # ALL keywords must match.
    "include_keywords": [],

    # Keywords that must NOT appear in the issue title or body (case-insensitive).
    # If ANY keyword is found the issue is rejected.
    "exclude_keywords": [],

    # Maximum age of the issue in hours. Set to None to disable.
    "max_issue_age_hours": None,

    # Minimum number of stars the repository must have. Set to None to disable.
    "min_repo_stars": None,
}

"""
IssueRadar Configuration
========================
Edit this file to customize which GitHub issues trigger Telegram notifications.
All secrets (tokens, chat IDs) are loaded from a .env file — never hardcode them here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Telegram Bot Settings (loaded from .env)
# ---------------------------------------------------------------------------
# 1. Create a bot via @BotFather on Telegram.
# 2. Send a message to your bot, then visit:
#    https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
#    to find your chat_id.
# 3. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your .env file.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ---------------------------------------------------------------------------
# GitHub Settings (loaded from .env, optional)
# ---------------------------------------------------------------------------
# A personal access token increases the rate limit from 60 to 5 000 req/hour.
# Set GITHUB_TOKEN in your .env file. Leave unset to use unauthenticated requests.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# ---------------------------------------------------------------------------
# Repositories to Monitor
# ---------------------------------------------------------------------------
TARGET_REPOSITORIES = [
    # Original
    "docling-project/docling",
    "infiniflow/ragflow",
    "qdrant/fastembed",
    "Unstructured-IO/unstructured",
    # RAG & LLM Frameworks
    "run-llama/llama_index",
    "deepset-ai/haystack",
    "langchain-ai/langchain",
    "HKUDS/LightRAG",
    "stanfordnlp/dspy",
    "pydantic/pydantic-ai",
    # Evaluation & Observability
    "explodinggradients/ragas",
    "langfuse/langfuse",
    "promptfoo/promptfoo",
    # Embeddings & Vector DBs
    "huggingface/sentence-transformers",
    "chroma-core/chroma",
    "lancedb/lancedb",
    "PrithivirajDamodaran/FlashRank",
    # LLM Tools
    "BerriAI/litellm",
    "FlowiseAI/Flowise",
    "ollama/ollama",
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

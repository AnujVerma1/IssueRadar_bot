"""
notifier.py — Send Telegram notifications via the Bot API.
"""

import requests
import config


def _format_message(issue: dict, repo: str) -> str:
    """Build a human-readable Telegram message for a matching issue."""
    title = issue.get("title", "No title")
    url = issue.get("html_url", "")
    labels = ", ".join(lbl["name"] for lbl in issue.get("labels", [])) or "None"
    created = issue.get("created_at", "Unknown")
    comments = issue.get("comments", 0)

    return (
        f"🔔 *IssueRadar — New Match*\n\n"
        f"📌 *Title:* {_escape_md(title)}\n"
        f"📦 *Repo:* {_escape_md(repo)}\n"
        f"🏷 *Labels:* {_escape_md(labels)}\n"
        f"📅 *Created:* {_escape_md(created)}\n"
        f"💬 *Comments:* {comments}\n\n"
        f"🔗 [Open on GitHub]({url})"
    )


def _escape_md(text: str) -> str:
    """Escape special Markdown characters for Telegram MarkdownV2."""
    special = r"_*[]()~`>#+-=|{}.!"
    for ch in special:
        text = text.replace(ch, f"\\{ch}")
    return text


def send_notification(issue: dict, repo: str) -> bool:
    """
    Send a Telegram message about *issue*.
    Returns True on success, False on failure.
    """
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID

    if not token:
        print("  [WARN] TELEGRAM_BOT_TOKEN not set in .env file. Skipping notification.")
        return False

    if not chat_id:
        print("  [WARN] TELEGRAM_CHAT_ID not set in .env file. Skipping notification.")
        return False

    message = _format_message(issue, repo)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            print(f"  [OK] Notification sent for issue #{issue['number']}")
            return True
        else:
            print(
                f"  [ERROR] Telegram API returned {response.status_code}: "
                f"{response.text}"
            )
            return False

    except requests.RequestException as exc:
        print(f"  [ERROR] Failed to send Telegram notification: {exc}")
        return False

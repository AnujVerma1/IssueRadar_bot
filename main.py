"""
IssueRadar — Lightweight GitHub Issue Monitor with Telegram Notifications.

Run:
    python main.py

The application checks configured repositories for new issues that match
your filters and sends a Telegram notification for each match. It polls
every N minutes (configurable) and never notifies about the same issue twice.
"""

import time
import sys
from datetime import datetime

import config
from github_client import fetch_open_issues, fetch_repo_info
from filters import passes_all_filters
from database import is_notified, mark_notified
from notifier import send_notification


def check_repositories() -> int:
    """
    Scan all configured repositories for matching issues.
    Returns the number of new notifications sent.
    """
    sent = 0

    for repo in config.TARGET_REPOSITORIES:
        print(f"  Checking {repo} ...")

        # Fetch repo metadata (stars, language) — needed by some filters.
        repo_info = fetch_repo_info(repo)

        # Fetch the latest open issues.
        issues = fetch_open_issues(repo)
        print(f"    Fetched {len(issues)} open issue(s)")

        for issue in issues:
            issue_id = issue["id"]

            # Skip if already notified.
            if is_notified(issue_id):
                continue

            # Apply deterministic filters.
            if not passes_all_filters(issue, repo_info):
                continue

            # Send Telegram notification.
            success = send_notification(issue, repo)
            if success:
                mark_notified(issue_id, repo, issue["title"], issue["html_url"])
                sent += 1
            else:
                # Still mark as notified if Telegram is not configured,
                # so we don't retry endlessly on config issues.
                # If it was a transient network error, we'll retry next cycle.
                pass

    return sent


def main() -> None:
    """Entry point — run initial check, then poll on a schedule."""
    run_once = "--once" in sys.argv
    interval = config.SCHEDULER.get("interval_minutes", 2)

    print("=" * 60)
    print("  IssueRadar — GitHub Issue Monitor")
    print("=" * 60)
    print(f"  Monitoring {len(config.TARGET_REPOSITORIES)} repository(ies)")
    if run_once:
        print("  Mode: single run (--once)")
    else:
        print(f"  Poll interval: {interval} minute(s)")
    print("=" * 60)
    print()

    # Initial check on startup.
    print(f"[{_now()}] Checking for new issues ...")
    sent = check_repositories()
    print(f"[{_now()}] Done — {sent} notification(s) sent.\n")

    # Exit immediately in single-run mode (used by GitHub Actions).
    if run_once:
        print(f"[{_now()}] Single run complete. Exiting.")
        return

    # Continuous polling loop (used when running locally).
    try:
        while True:
            print(f"[{_now()}] Sleeping for {interval} minute(s) ...")
            time.sleep(interval * 60)
            print(f"\n[{_now()}] Checking for new issues ...")
            sent = check_repositories()
            print(f"[{_now()}] Done — {sent} notification(s) sent.\n")
    except KeyboardInterrupt:
        print(f"\n[{_now()}] Stopped by user. Goodbye!")
        sys.exit(0)


def _now() -> str:
    """Return the current local time as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    main()

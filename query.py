#!/usr/bin/env python3
"""
Z.ai Quota Query Script

Queries Z.ai (z.ai-coding-plan) account quota usage.
Based on the opencode-mystatus plugin: https://github.com/vbgate/opencode-mystatus
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path


# Configuration
ZAI_QUOTA_API = "https://api.z.ai/api/monitor/usage/quota/limit"
REQUEST_TIMEOUT = 10  # seconds
HIGH_USAGE_THRESHOLD = 80


def read_auth_file():
    """Read the Z.ai API key from Claude Code's settings.json file."""
    settings_path = Path.home() / ".claude/settings.json"

    try:
        with open(settings_path, "r") as f:
            settings_data = json.load(f)

        api_key = settings_data.get("env", {}).get("ANTHROPIC_AUTH_TOKEN")
        if not api_key:
            return None

        return api_key
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return None


def mask_string(s: str, show_chars: int = 4) -> str:
    """Mask sensitive string showing only first and last few characters."""
    if len(s) <= show_chars * 2:
        return "*" * len(s)
    return f"{s[:show_chars]}****{s[-show_chars:]}"


def format_duration(milliseconds: int) -> str:
    """Format duration in human-readable format."""
    seconds = max(0, milliseconds) // 1000
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def format_reset_time(milliseconds: int) -> str:
    """Format reset time as datetime string in UTC+8 (Beijing time)."""
    # Create UTC datetime from timestamp
    dt_utc = datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc)
    # Convert to UTC+8
    tz_utc8 = timezone(timedelta(hours=8))
    dt_local = dt_utc.astimezone(tz_utc8)
    return dt_local.strftime("%Y-%m-%d %H:%M")


def create_progress_bar(percent: int, width: int = 25) -> str:
    """Create a visual progress bar."""
    safe_percent = max(0, min(100, percent))
    filled = round((safe_percent / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty


def query_zai_quota(api_key: str) -> dict:
    """Query the Z.ai quota API."""
    req = urllib.request.Request(
        ZAI_QUOTA_API,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "Claude-Code-ZaiQuota/1.0",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        error_text = e.read().decode()
        raise Exception(f"API error ({e.code}): {error_text[:100]}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}")
    except TimeoutError:
        raise Exception(f"Request timeout ({REQUEST_TIMEOUT}s)")
    except json.JSONDecodeError:
        raise Exception("Invalid API response format")


def format_quota_response(data: dict, api_key: str) -> str:
    """Format the quota API response for display."""
    lines = []

    # Header
    masked_key = mask_string(api_key)
    lines.append("## Z.ai Account Quota")
    lines.append("")
    lines.append(f"Account: {masked_key} (Z.ai)")
    lines.append("")

    # Check data structure
    if not data.get("success") or data.get("code") != 200:
        msg = data.get("msg", "Unknown error")
        lines.append(f"Error: {msg}")
        return "\n".join(lines)

    limits = data.get("data", {}).get("limits", [])
    if not limits:
        lines.append("No quota data available")
        return "\n".join(lines)

    # Find TOKENS_LIMIT and TIME_LIMIT
    tokens_limit = None
    time_limit = None

    for limit in limits:
        limit_type = limit.get("type")
        if limit_type == "TOKENS_LIMIT":
            tokens_limit = limit
        elif limit_type == "TIME_LIMIT":
            time_limit = limit

    # Display TOKENS_LIMIT (5-hour token limit)
    if tokens_limit:
        used_percent = round(tokens_limit.get("percentage", 0))
        remain_percent = 100 - used_percent
        progress_bar = create_progress_bar(remain_percent)

        lines.append("5-hour token limit")
        lines.append(f"{progress_bar} {remain_percent}% remaining")

        # Reset time
        next_reset_ms = tokens_limit.get("nextResetTime")
        if next_reset_ms:
            now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
            remaining_ms = max(0, next_reset_ms - now_ms)
            reset_time = format_reset_time(next_reset_ms)
            lines.append(f"Resets in: {format_duration(remaining_ms)} (at {reset_time})")

    # Display TIME_LIMIT (MCP monthly quota)
    if time_limit:
        if tokens_limit:
            lines.append("")  # Separator

        remain_percent = time_limit.get("remaining", 0)
        progress_bar = create_progress_bar(remain_percent)

        lines.append("MCP monthly quota")
        lines.append(f"{progress_bar} {remain_percent}% remaining")

        used = time_limit.get("currentValue", 0)
        total = time_limit.get("usage", 0)
        lines.append(f"Used: {used} / {total}")

    # Warning if high usage
    if tokens_limit and tokens_limit.get("percentage", 0) >= HIGH_USAGE_THRESHOLD:
        lines.append("")
        lines.append("⚠️  High token usage!")

    return "\n".join(lines)


def main():
    """Main entry point."""
    # Read API key
    api_key = read_auth_file()
    if not api_key:
        print("Error: Z.ai API key not found in ~/.claude/settings.json", file=sys.stderr)
        print('Expected format: {"env": {"ANTHROPIC_AUTH_TOKEN": "your-key"}}', file=sys.stderr)
        sys.exit(1)

    # Query quota
    try:
        data = query_zai_quota(api_key)
        output = format_quota_response(data, api_key)
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

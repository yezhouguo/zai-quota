---
name: zai-quota
description: Query Z.ai (z.ai-coding-plan) account quota usage including remaining tokens, usage stats, and reset countdowns with visual progress bars. Use when user asks about their Z.ai quota, remaining tokens, or account usage status.
---

# Z.ai Quota Query

This skill queries your Z.ai (z.ai-coding-plan) account quota usage directly from the Z.ai API.

## When to Use This Skill

Use this skill when the user asks about:
- Z.ai quota or remaining tokens
- Account usage status for Z.ai
- "how much quota do I have left"
- "check my z.ai usage"
- "z.ai account status"

## How It Works

The skill:
1. Reads your Z.ai API key from `~/.claude/settings.json`
2. Queries the Z.ai quota API at `https://api.z.ai/api/monitor/usage/quota/limit`
3. Displays results with visual progress bars for:
   - 5-hour token limit
   - MCP monthly quota
4. Shows reset countdowns and usage statistics

## Output Format

```
## Z.ai Account Quota

Account: 942b****v9S9 (Z.ai)

5-hour token limit
████████████████████████░ 99% remaining
Resets in: 4h 57m

MCP monthly quota
█████████████████████░░░░ 87% remaining
Used: 13 / 100
```

## Configuration

The Z.ai API key must be stored in `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-api-key-here"
  }
}
```

## Script Location

The main script is at: `/root/.agents/skills/zai-quota/query.py`

You can run it directly:
```bash
python3 /root/.agents/skills/zai-quota/query.py
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Z.ai API key not found` | Missing API key in settings.json | Add ANTHROPIC_AUTH_TOKEN to ~/.claude/settings.json |
| `API error (401)` | Invalid or expired API key | Update your API key |
| `Network error` | Connection problem | Check internet connection |
| `Request timeout` | API too slow | Try again later |

## Notes

- Token limit resets every 5 hours (rolling window)
- MCP monthly quota resets on the 1st of each month
- Progress bar: █ = remaining, ░ = used
- Warning shown if token usage exceeds 80%

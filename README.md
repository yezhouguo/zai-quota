# Z.ai Quota Query Skill for Claude Code

A Claude Code skill that queries your Z.ai (z.ai-coding-plan) account quota usage directly from the Z.ai API.

## Features

- **5-hour token limit**: Visual progress bar showing remaining tokens with reset countdown
- **MCP monthly quota**: Displays monthly quota usage with reset information
- **Beautiful output**: Progress bars and formatted statistics
- **Easy to use**: Simple command invocation or direct script execution

## Installation

### Option 1: Clone to Claude Code Skills Directory

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/zai-quota.git ~/.claude/skills/zai-quota

# Make scripts executable
chmod +x ~/.claude/skills/zai-quota/zai-quota
chmod +x ~/.claude/skills/zai-quota/query.py
```

### Option 2: Install from a Script

```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/zai-quota/main/install.sh)
```

## Usage

### In Claude Code

Simply use the command:

```
/zai-quota
```

Or ask Claude:

- "check my z.ai quota"
- "how much tokens do I have left"
- "z.ai account status"

### Standalone Script

```bash
# Run directly
~/.claude/skills/zai-quota/zai-quota

# Or with python
python3 ~/.claude/skills/zai-quota/query.py
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

## Output Example

```
## Z.ai Account Quota

Account: 942b****v9S9 (Z.ai)

5-hour token limit
████████████████████████░ 97% remaining
Resets in: 4h 53m (at 2026-03-04 14:29)

MCP monthly quota
█████████████████████████ 100% remaining
Used: 0 / 100
```

## Requirements

- Python 3.6+
- Claude Code (if using as a skill)
- Z.ai API key

## Based On

This skill is based on the [opencode-mystatus](https://github.com/vbgate/opencode-mystatus) plugin.

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please [open an issue](https://github.com/YOUR_USERNAME/zai-quota/issues).

---
description: "Query Z.ai account quota usage including 5-hour token limit reset countdown"
---

Query Z.ai quota by running the Python script from the skill directory:

```bash
# Find and run the query script from the skill base directory
SCRIPT_DIR="/root/.agents/skills/zai-quota"
python3 "$SCRIPT_DIR/query.py" 2>&1
```

Display the complete output including:
- 5-hour token limit with reset countdown
- MCP monthly quota usage
- Visual progress bars

**Important**: Run exactly once and return the full output without modification.

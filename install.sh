#!/bin/bash
# Z.ai Quota Skill Installation Script

set -e

INSTALL_DIR="$HOME/.claude/skills/zai-quota"
REPO_URL="https://github.com/yezhouguo/zai-quota"

echo "Installing Z.ai Quota Skill for Claude Code..."
echo ""

# Create skills directory if it doesn't exist
mkdir -p "$HOME/.claude/skills"

# Check if directory already exists
if [ -d "$INSTALL_DIR" ]; then
    echo "Directory already exists: $INSTALL_DIR"
    read -p "Remove and reinstall? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
    else
        echo "Installation cancelled."
        exit 1
    fi
fi

# Clone the repository
echo "Cloning repository..."
git clone "$REPO_URL" "$INSTALL_DIR"

# Make scripts executable
chmod +x "$INSTALL_DIR/zai-quota"
chmod +x "$INSTALL_DIR/query.py"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Usage:"
echo "  In Claude Code: /zai-quota"
echo "  Standalone:     $INSTALL_DIR/zai-quota"
echo ""
echo "Make sure your Z.ai API key is configured in ~/.claude/settings.json"

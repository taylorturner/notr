#!/bin/bash

# Define where main.py is (you can make this dynamic later if needed)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/main.py"

# Define where to place the symlink (change if you prefer a different dir)
LINK_NAME="/usr/local/bin/notr"

# Check if we need sudo
if [ ! -w "$(dirname "$LINK_NAME")" ]; then
  echo "🔒 You need sudo to create a symlink in $(dirname "$LINK_NAME")"
  SUDO="sudo"
else
  SUDO=""
fi

# Create symlink
echo "🔧 Setting up 'notr' command..."
$SUDO ln -sf "$TARGET" "$LINK_NAME"
$SUDO chmod +x "$TARGET"

echo "✅ Setup complete! You can now use 'notr' from anywhere."
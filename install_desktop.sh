#!/bin/bash

# Get absolute paths
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXEC="$APP_DIR/.venv/bin/python3"
MAIN_SCRIPT="$APP_DIR/main.py"
ICON_PATH="$APP_DIR/icon.png" # Optional: Can be created later

DESKTOP_FILE="$HOME/.local/share/applications/any-downloader-tool.desktop"

# Create the .desktop file content
cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Any Downloader Tool
Comment=A unified UI for open-source downloaders like spotdl and yt-dlp
Exec=$PYTHON_EXEC $MAIN_SCRIPT
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;Network;
EOF

# Make it executable
chmod +x "$DESKTOP_FILE"

echo "Desktop entry created at: $DESKTOP_FILE"
echo "You should now be able to find 'Any Downloader Tool' in your application launcher."

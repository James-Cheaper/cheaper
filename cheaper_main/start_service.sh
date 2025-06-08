#!/bin/bash

APP_NAME="Cheaper"
APP_FILE="main.py"
LOG_DIR="$HOME/CheaperLogs"

# Allow user to override PYTHON_PATH by setting it externally
if [ -z "$PYTHON_PATH" ]; then
  PYTHON_PATH=$(command -v python3)
fi

if [ -z "$PYTHON_PATH" ]; then
  PYTHON_PATH=$(command -v python)
fi

# Final fallback for Windows users (optional)
if [ -z "$PYTHON_PATH" ] && [ -f "/c/Users/$USERNAME/AppData/Local/Programs/Python/Python39/python.exe" ]; then
  PYTHON_PATH="/c/Users/$USERNAME/AppData/Local/Programs/Python/Python39/python.exe"
fi

# Validate Python path
if ! "$PYTHON_PATH" --version > /dev/null 2>&1; then
  echo "❌ Python not found. Please install it or set PYTHON_PATH manually."
  exit 1
fi

echo "✅ Using Python at: $PYTHON_PATH"

# Create log directory
mkdir -p "$LOG_DIR"

# Start with PM2
pm2 start "$APP_FILE" \
  --name "$APP_NAME" \
  --interpreter="$PYTHON_PATH" \
  --output "$LOG_DIR/out.log" \
  --error "$LOG_DIR/err.log" \
  --watch

pm2 save

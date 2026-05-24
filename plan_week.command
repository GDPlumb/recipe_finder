#!/bin/bash
# Double-click in Finder (or run in Terminal) to generate this week's prompt.
clear
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
  echo "No .venv found. First run:"
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  read -p "Press Enter to close..."
  exit 1
fi

prompt="$(.venv/bin/python plan_week.py)"
echo "$prompt"
printf '%s' "$prompt" | pbcopy

echo
echo "----------------------------------------------------------"
echo "Copied to clipboard. Paste into Claude with web search ON."
read -p "Press Enter to close..."

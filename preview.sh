#!/bin/bash
set -e

# Generate the theme file from the python script
.venv/bin/python gen-palettes.py > gen/harmonized.m.kdl
.venv/bin/python gen-root.py > maybe-material.kdl

# Check if a variant name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 \"<variant name>\""
  exit 1
fi

# Patch Zed's settings.json with the specified variant
zed-hct-theme-maker experimental-patch-settings maybe-material.kdl /home/sarah/.var/app/dev.zed.Zed/config/zed/settings.json "$1"

echo "Zed settings updated to use variant: $1"
echo "Theme file 'maybe-material.kdl' was (re)generated."
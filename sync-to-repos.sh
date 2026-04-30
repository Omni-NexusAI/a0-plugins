#!/usr/bin/env bash
# sync-to-repos.sh — push each plugin subdirectory to its own GitHub repo
# Usage: ./sync-to-repos.sh [ORG]
#   ORG defaults to Omni-NexusAI

set -euo pipefail

ORG="${1:-Omni-NexusAI}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"

for plugin_dir in "$PLUGINS_DIR"/*/; do
  plugin_name="$(basename "$plugin_dir")"
  repo_url="https://github.com/$ORG/$plugin_name.git"
  tmp_clone="$(mktemp -d)"

  echo ">>> Syncing $plugin_name → $ORG/$plugin_name"

  # Clone the per-plugin repo (or create it if it doesn't exist)
  if git clone "$repo_url" "$tmp_clone" 2>/dev/null; then
    echo "    Cloned existing repo"
  else
    echo "    Repo not found, creating via GitHub API..."
    curl -sf -X POST "https://api.github.com/user/repos" \
      -H "Authorization: token $(git config --global credential.helper || true)" \
      -d "{\"name\":\"$plugin_name\",\"private\":false,\"auto_init\":false}" > /dev/null 2>&1 || true
    sleep 2
    git clone "$repo_url" "$tmp_clone" 2>/dev/null || {
      echo "    ERROR: Could not clone $repo_url"
      continue
    }
  fi

  # Copy plugin files into the clone
  rsync -a --delete --exclude='.git' "$plugin_dir"/ "$tmp_clone/"

  # Commit and push
  cd "$tmp_clone"
  git add -A
  git diff --cached --quiet && echo "    No changes" && continue
  git commit -m "sync from a0-plugins monorepo $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git push origin HEAD:main || git push origin HEAD:master
  echo "    Pushed ✓"
  cd "$SCRIPT_DIR"

  rm -rf "$tmp_clone"
done

echo ">>> All plugins synced"

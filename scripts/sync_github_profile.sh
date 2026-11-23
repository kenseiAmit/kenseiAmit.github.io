#!/usr/bin/env bash
# Syncs kenseiAmit profile README, portfolio updates, and GitHub Bio/Website.
# Usage: GITHUB_PAT="<your_kenseiAmit_pat>" bash scripts/sync_github_profile.sh
set -euo pipefail

if [[ -z "${GITHUB_PAT:-}" ]]; then
  echo "Usage: GITHUB_PAT=\"<your_kenseiAmit_pat>\" bash $0"
  exit 1
fi

SHOWCASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

echo "1/3 Pushing prominent Live Portfolio CTA & HF Sandbox badge in kenseiAmit/kenseiAmit..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.git" main:main --quiet

echo "2/3 Pushing latest UI polish & HF Sandbox link in kenseiAmit/kenseiAmit.github.io..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit.github.io" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.github.io.git" main:main --quiet

echo "3/3 Updating @kenseiAmit GitHub Bio & Website URL..."
curl -fsSL -X PATCH "https://api.github.com/user" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "bio": "Data, MLOps & Agentic AI Engineer · IIT Kanpur · 28 Systems (MCP, A2A, ADK, LangGraph, AI Security & Cloud MLOps) → https://kenseiamit.github.io",
    "blog": "https://kenseiamit.github.io",
    "location": "Stockholm, Sweden"
  }' >/dev/null

echo "Done! Live at https://github.com/kenseiAmit and https://kenseiamit.github.io"

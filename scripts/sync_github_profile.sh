#!/usr/bin/env bash
# Syncs kenseiAmit profile README, portfolio polish, and GitHub Bio/Website.
# Usage: GITHUB_PAT="<your_kenseiAmit_pat>" bash scripts/sync_github_profile.sh
set -euo pipefail

if [[ -z "${GITHUB_PAT:-}" ]]; then
  echo "Usage: GITHUB_PAT=\"<your_kenseiAmit_pat>\" bash $0"
  exit 1
fi

SHOWCASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
AUTH_B64="$(printf "x-access-token:%s" "$GITHUB_PAT" | base64 | tr -d '\n')"

echo "1/3 Pushing prominent Live Portfolio CTA in kenseiAmit/kenseiAmit..."
git -C "$SHOWCASE_DIR/kenseiAmit" \
  -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $AUTH_B64" \
  push origin main

echo "2/3 Pushing latest UI polish in kenseiAmit/kenseiAmit.github.io..."
git -C "$SHOWCASE_DIR/kenseiAmit.github.io" \
  -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $AUTH_B64" \
  push origin main

echo "3/3 Updating @kenseiAmit GitHub Bio & Website URL..."
curl -fsSL -X PATCH "https://api.github.com/user" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "bio": "Data, MLOps & Agentic AI Engineer · IIT Kanpur · 28 Production Systems (MCP, A2A, ADK, LangGraph, AI Security & Cloud MLOps) → https://kenseiamit.github.io",
    "blog": "https://kenseiamit.github.io",
    "location": "Stockholm, Sweden"
  }' >/dev/null

echo "Done! Live at https://github.com/kenseiAmit and https://kenseiamit.github.io"

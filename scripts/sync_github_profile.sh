#!/usr/bin/env bash
# Syncs kenseiAmit profile README, portfolio website, all 27 project repos, and GitHub display name ("Amit Kumar").
# Optional: pass HF_TOKEN="<your_hf_token>" as well to sync the Hugging Face Space in the same run.
# Usage: GITHUB_PAT="<your_kenseiAmit_pat>" [HF_TOKEN="<your_hf_token>"] bash scripts/sync_github_profile.sh
set -euo pipefail

if [[ -z "${GITHUB_PAT:-}" ]]; then
  echo "Usage: GITHUB_PAT=\"<your_kenseiAmit_pat>\" [HF_TOKEN=\"<your_hf_token>\"] bash $0"
  exit 1
fi

SHOWCASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

echo "1/4 Updating @kenseiAmit GitHub Display Name ('Amit Kumar'), Bio & Website URL..."
curl -fsSL -X PATCH "https://api.github.com/user" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "name": "Amit Kumar",
    "bio": "Data, MLOps & Agentic AI Engineer · IIT Kanpur · 28 Systems (MCP, A2A, ADK, LangGraph, AI Security & Cloud MLOps) → https://kenseiamit.github.io",
    "blog": "https://kenseiamit.github.io",
    "location": "Stockholm, Sweden"
  }' >/dev/null

echo "2/4 Pushing kenseiAmit/kenseiAmit profile README & SVG banner..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.git" main:main --force --quiet

echo "3/4 Pushing kenseiAmit/kenseiAmit.github.io portfolio website..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit.github.io" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.github.io.git" main:main --force --quiet

echo "4/4 Syncing updated LICENSE & author metadata across all 27 project repositories..."
for repo_path in "$SHOWCASE_DIR"/*; do
  [[ -d "$repo_path/.git" ]] || continue
  repo_name="$(basename "$repo_path")"
  if [[ "$repo_name" == "kenseiAmit" || "$repo_name" == "kenseiAmit.github.io" || "$repo_name" == "hf-space-agentops-governance-demo" ]]; then
    continue
  fi
  GIT_TERMINAL_PROMPT=0 git -C "$repo_path" \
    -c "credential.helper=" \
    push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/${repo_name}.git" main:main --force --quiet
done

if [[ -n "${HF_TOKEN:-}" ]]; then
  echo "Bonus: Syncing Hugging Face Space (kenseiamit/agentops-governance-sandbox)..."
  HF_USERNAME="kenseiamit" HF_TOKEN="$HF_TOKEN" bash "$SHOWCASE_DIR/hf-space-agentops-governance-demo/deploy_to_hf_spaces.sh"
fi

echo "Done! All repositories and @kenseiAmit profile updated to 'Amit Kumar'."

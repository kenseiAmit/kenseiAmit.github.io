#!/usr/bin/env bash
# Syncs:
#   1. kenseiAmit/ecohome-energy-advisor-agent (creates repo if needed + pushes 15-commit history & v1.0.0 tag)
#   2. kenseiAmit/nasa-mission-rag-eval-engine (syncs structured 15-commit history & v1.0.0 tag)
#   3. @kenseiAmit GitHub display name ("Amit Kumar") + 30-System bio
#   4. kenseiAmit/kenseiAmit profile README & kenseiAmit/kenseiAmit.github.io website
# Usage: GITHUB_PAT="<your_kenseiAmit_pat>" [HF_TOKEN="<your_hf_token>"] bash scripts/sync_github_profile.sh
set -euo pipefail

if [[ -z "${GITHUB_PAT:-}" ]]; then
  echo "Usage: GITHUB_PAT=\"<your_kenseiAmit_pat>\" [HF_TOKEN=\"<your_hf_token>\"] bash $0"
  exit 1
fi

SHOWCASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
NEW_REPO="ecohome-energy-advisor-agent"
NASA_REPO="nasa-mission-rag-eval-engine"

echo "1/5 Ensuring kenseiAmit/${NEW_REPO} exists on GitHub & pushing main + tags..."
HTTP_CODE="$(curl -sS -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/kenseiAmit/${NEW_REPO}")"

if [[ "$HTTP_CODE" == "404" ]]; then
  curl -fsSL -X POST "https://api.github.com/user/repos" \
    -H "Authorization: Bearer $GITHUB_PAT" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    -d "{
      \"name\": \"${NEW_REPO}\",
      \"description\": \"Autonomous 7-Tool LangGraph Smart-Home Solar PV, EV, HVAC & Battery Time-of-Use Optimization Agent with ChromaDB RAG, SQLite Telemetry & LLM-as-a-Judge Evaluation (12/12 Pass · 95.8% Score)\",
      \"homepage\": \"https://kenseiamit.github.io/portfolio/?system=${NEW_REPO}\",
      \"private\": false,
      \"has_issues\": true,
      \"has_wiki\": false
    }" >/dev/null
fi

GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/${NEW_REPO}" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/${NEW_REPO}.git" main:main --force --tags --quiet

curl -fsSL -X PUT "https://api.github.com/repos/kenseiAmit/${NEW_REPO}/topics" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{"names":["langgraph","langchain","rag","chromadb","agentic-ai","llmops","energy-optimization","python"]}' >/dev/null || true

echo "2/5 Syncing kenseiAmit/${NASA_REPO} structured commit history & v1.0.0 release tag..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/${NASA_REPO}" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/${NASA_REPO}.git" main:main --force --tags --quiet

echo "3/5 Updating @kenseiAmit GitHub Display Name ('Amit Kumar'), Bio & Website URL..."
curl -fsSL -X PATCH "https://api.github.com/user" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "name": "Amit Kumar",
    "bio": "Data, MLOps & Agentic AI Engineer · IIT Kanpur · 30 Systems (MCP, A2A, ADK, LangGraph, AI Security & Cloud MLOps) → https://kenseiamit.github.io",
    "blog": "https://kenseiamit.github.io",
    "location": "Stockholm, Sweden"
  }' >/dev/null

echo "4/5 Pushing kenseiAmit/kenseiAmit profile README & SVG banner..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.git" main:main --force --quiet

echo "5/5 Pushing kenseiAmit/kenseiAmit.github.io portfolio website..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit.github.io" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.github.io.git" main:main --force --quiet

if [[ "${SYNC_ALL_REPOS:-0}" == "1" ]]; then
  echo "Bonus: Syncing all local project repositories..."
  for repo_path in "$SHOWCASE_DIR"/*; do
    [[ -d "$repo_path/.git" ]] || continue
    repo_name="$(basename "$repo_path")"
    if [[ "$repo_name" == "kenseiAmit" || "$repo_name" == "kenseiAmit.github.io" || "$repo_name" == "hf-space-agentops-governance-demo" || "$repo_name" == "$NEW_REPO" || "$repo_name" == "$NASA_REPO" ]]; then
      continue
    fi
    GIT_TERMINAL_PROMPT=0 git -C "$repo_path" \
      -c "credential.helper=" \
      push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/${repo_name}.git" main:main --force --quiet
  done
fi

if [[ -n "${HF_TOKEN:-}" ]]; then
  echo "Bonus: Syncing Hugging Face Space (kenseiamit/agentops-governance-sandbox)..."
  HF_USERNAME="kenseiamit" HF_TOKEN="$HF_TOKEN" bash "$SHOWCASE_DIR/hf-space-agentops-governance-demo/deploy_to_hf_spaces.sh"
fi

echo "Done! Published kenseiAmit/${NEW_REPO} + ${NASA_REPO} (with atomic commits & v1.0.0 tags) and updated @kenseiAmit + kenseiamit.github.io (30 Systems)."

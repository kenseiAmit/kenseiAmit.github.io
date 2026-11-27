#!/usr/bin/env bash
# Syncs kenseiAmit profile README, portfolio website, nasa-mission-rag-eval-engine (creating the GitHub repo if needed),
# and @kenseiAmit GitHub display name ("Amit Kumar") + 29-System bio.
# Optional: pass HF_TOKEN="<your_hf_token>" as well to sync the Hugging Face Space in the same run.
# Usage: GITHUB_PAT="<your_kenseiAmit_pat>" [HF_TOKEN="<your_hf_token>"] bash scripts/sync_github_profile.sh
set -euo pipefail

if [[ -z "${GITHUB_PAT:-}" ]]; then
  echo "Usage: GITHUB_PAT=\"<your_kenseiAmit_pat>\" [HF_TOKEN=\"<your_hf_token>\"] bash $0"
  exit 1
fi

SHOWCASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
NEW_REPO="nasa-mission-rag-eval-engine"

echo "1/5 Ensuring kenseiAmit/${NEW_REPO} exists on GitHub & pushing main..."
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
      \"description\": \"NASA Apollo 11, Apollo 13 & Challenger (STS-51L) Primary-Archive RAG & Concurrent Async RAGAS v0.4.3 Evaluation Engine (8,046 ChromaDB Chunks · 0.9861 Precision · 0.9583 Faithfulness)\",
      \"homepage\": \"https://kenseiamit.github.io/portfolio/?system=${NEW_REPO}\",
      \"private\": false,
      \"has_issues\": true,
      \"has_wiki\": false
    }" >/dev/null
fi

GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/${NEW_REPO}" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/${NEW_REPO}.git" main:main --force --quiet

curl -fsSL -X PUT "https://api.github.com/repos/kenseiAmit/${NEW_REPO}/topics" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{"names":["rag","llmops","ragas","chromadb","openai","streamlit","evaluation","python"]}' >/dev/null || true

echo "2/5 Updating @kenseiAmit GitHub Display Name ('Amit Kumar'), Bio & Website URL..."
curl -fsSL -X PATCH "https://api.github.com/user" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "name": "Amit Kumar",
    "bio": "Data, MLOps & Agentic AI Engineer · IIT Kanpur · 29 Systems (MCP, A2A, ADK, LangGraph, AI Security & Cloud MLOps) → https://kenseiamit.github.io",
    "blog": "https://kenseiamit.github.io",
    "location": "Stockholm, Sweden"
  }' >/dev/null

echo "3/5 Pushing kenseiAmit/kenseiAmit profile README & SVG banner..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.git" main:main --force --quiet

echo "4/5 Pushing kenseiAmit/kenseiAmit.github.io portfolio website..."
GIT_TERMINAL_PROMPT=0 git -C "$SHOWCASE_DIR/kenseiAmit.github.io" \
  -c "credential.helper=" \
  push "https://x-access-token:${GITHUB_PAT}@github.com/kenseiAmit/kenseiAmit.github.io.git" main:main --force --quiet

if [[ "${SYNC_ALL_REPOS:-0}" == "1" ]]; then
  echo "5/5 Syncing all 28 local project repositories..."
  for repo_path in "$SHOWCASE_DIR"/*; do
    [[ -d "$repo_path/.git" ]] || continue
    repo_name="$(basename "$repo_path")"
    if [[ "$repo_name" == "kenseiAmit" || "$repo_name" == "kenseiAmit.github.io" || "$repo_name" == "hf-space-agentops-governance-demo" || "$repo_name" == "$NEW_REPO" ]]; then
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

echo "Done! Published kenseiAmit/${NEW_REPO} and updated @kenseiAmit + kenseiamit.github.io (29 Systems)."

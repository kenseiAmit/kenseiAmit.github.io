#!/usr/bin/env python3
"""
Deterministic portfolio data & asset compiler for kenseiAmit.github.io.
Extracts real Mermaid topologies, quick-start snippets, empirical telemetry charts,
animated SVG traces, and verified runtime JSON payloads across all 29 repositories.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

SHOWCASE_ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = Path(__file__).resolve().parents[1]
DATA_OUT = SITE_ROOT / "data" / "portfolio.json"
DEMOS_DIR = SITE_ROOT / "assets" / "demos"
TELEMETRY_DIR = SITE_ROOT / "assets" / "telemetry"

GITHUB_USER = "kenseiAmit"

DOMAINS = [
    {
        "id": "multi-agent-mcp",
        "num": "01",
        "name": "Multi-Agent Orchestration, MCP & Agentic Protocols",
        "shortName": "Multi-Agent & MCP",
        "color": "#3B82F6",
        "description": "Distributed agent microservices over A2A JSON-RPC, Model Context Protocol (MCP) tool servers, Google ADK, LangGraph, Claude Agent SDK, and Microsoft Semantic Kernel."
    },
    {
        "id": "llmops-eval",
        "num": "02",
        "name": "LLMOps, AgentOps & Confidence Calibration",
        "shortName": "LLMOps & Calibration",
        "color": "#A855F7",
        "description": "Tiered LLM routing, sub-2ms semantic caching, AST-sandboxed agent runtimes, RAGAS retrieval sweeps, OpenTelemetry tracing, and sliced Brier confidence calibration."
    },
    {
        "id": "fintech-ai",
        "num": "03",
        "name": "Agentic AI for Financial Services & Quantitative Risk",
        "shortName": "FinTech & Quant AI",
        "color": "#10B981",
        "description": "Regulated banking & capital-markets systems enforcing FinCEN SAR statutory compliance, SWIFT MT103 wire screening, SEC Form 10-K RAG, and SEC Reg M trading controls."
    },
    {
        "id": "ai-security-grc",
        "num": "04",
        "name": "AI Security, Adversarial ML Red-Teaming & Governance",
        "shortName": "AI Security & GRC",
        "color": "#EF4444",
        "description": "Offensive FGSM/poisoning/RAG-exfiltration red-teaming, STRIDE-ML threat models, AWS Bedrock Guardrails, OWASP LLM Top 10 defense-in-depth, and EU AI Act Annex III fairness."
    },
    {
        "id": "mlops-pipelines",
        "num": "05",
        "name": "Production MLOps, Reproducible Workflows & Drift Monitoring",
        "shortName": "Production MLOps",
        "color": "#F59E0B",
        "description": "Leakage-safe training DAGs, DVC + MLflow gated @production promotion, Hydra sweeps, KL-divergence & Deepchecks drift gates, subgroup fairness audits, and CI/CD serving."
    },
    {
        "id": "cloud-swe",
        "num": "06",
        "name": "Cloud Architecture, Serverless AI & Software Engineering",
        "shortName": "Cloud & SWE",
        "color": "#06B6D4",
        "description": "Multi-account AWS Organizations & Control Tower landing zones, distributed AWS Glue 4.0 PySpark MLlib, CloudFormation Bedrock serverless IaC, and clean OOP Python."
    },
]

ROLE_TRACKS = [
    {
        "id": "all",
        "label": "Executive Overview",
        "badge": "All 29 Systems",
        "headline": "End-to-End Agentic AI, AI Security & Cloud MLOps Engineering",
        "pitch": "Curated view leading with 7 verified flagship architectures across multi-agent protocols (MCP, A2A, ADK, LangGraph), runtime AI security & EU AI Act governance, FinOps-optimized LLMOps gateways, and multi-cloud MLOps."
    },
    {
        "id": "agentic-ai",
        "label": "Agentic AI & MCP",
        "badge": "12 Systems",
        "headline": "Senior / Principal Agentic AI & Multi-Agent Systems Track",
        "pitch": "Production orchestration across Anthropic Claude Agent SDK, Google ADK (A2A JSON-RPC), LangGraph StateGraphs, Microsoft Semantic Kernel, PydanticAI, and custom FastMCP servers—combining deterministic math/SQL tools with bounded autonomy."
    },
    {
        "id": "llmops",
        "label": "LLMOps & Reliability",
        "badge": "8 Systems",
        "headline": "LLMOps, AgentOps, Evaluation & FinOps Platform Track",
        "pitch": "Focused on unit economics, latency, and post-deployment reliability: 61.9% tiered-routing cost savings, 1.4ms semantic caching, Arize Phoenix OpenTelemetry spans, RAGAS sweeps, AST sandboxes, and sliced Brier calibration."
    },
    {
        "id": "fintech",
        "label": "FinTech & Banking AI",
        "badge": "8 Systems",
        "headline": "Regulated Financial Services, AML Compliance & Quantitative AI Track",
        "pitch": "Built for high-stakes financial workflows: zero-knowledge A2A loan underwriting, FinCEN Form 111 SAR filing with SHA-256 audit logs, SWIFT MT103 OFAC/FATF screening, SEC 10-K + NL-to-SQL equity research, and FinBERT MLOps."
    },
    {
        "id": "ai-security",
        "label": "AI Security & GRC",
        "badge": "6 Systems",
        "headline": "AI Security Engineering, Red-Teaming & EU AI Act Governance Track",
        "pitch": "Both offensive exploit engineering (PyTorch FGSM evasion, label-flip poisoning, FAISS RAG exfiltration) and verifiable defense-in-depth (36/36 Bedrock Guardrails, STRIDE-ML, ML-BOM, IAM explicit-deny, TreeSHAP + EU AI Act Annex III)."
    },
    {
        "id": "mlops",
        "label": "MLOps & Data",
        "badge": "8 Systems",
        "headline": "Staff MLOps, Distributed Data & Reproducible ML Platform Track",
        "pitch": "Automated ML lifecycle systems spanning AWS Glue PySpark (10x speedup), MLflow + DVC + Hydra + W&B lineage, SciPy KL-divergence & Deepchecks NLP drift gates, Prometheus telemetry, and automated retraining loops."
    },
    {
        "id": "cloud",
        "label": "Cloud & Architecture",
        "badge": "7 Systems",
        "headline": "Multi-Cloud AI Infrastructure (AWS · GCP · Azure) & Software Architecture Track",
        "pitch": "Enterprise cloud governance and serverless AI across AWS Organizations/Control Tower SCPs, CloudFormation Bedrock dual-model resilience, ECS Fargate, GCP Vertex AI / Cloud SQL, and Azure AI Foundry."
    },
]

# Curated rich metadata per system (grounded 100% in each repo's verified README & benchmarks)
CURATED_SYSTEMS = {
    "guarded-salesops-agent-runtime": {
        "title": "Guarded SalesOps Agent Runtime",
        "domainId": "llmops-eval",
        "tracks": ["llmops", "agentic-ai", "ai-security"],
        "flagship": True,
        "flagshipRank": 1,
        "metrics": ["14/14 Eval Pass", "237 Logged Runs", "0 PII Leaks", "AST Sandbox + HITL"],
        "summary": "Defense-in-depth B2B CRM agent runtime enforcing pre-inference, tool-level, and post-inference guardrails, AST-constrained Python sandboxing, mandatory HITL outbound email gates, and PII-redacted structured tracing.",
        "tradeoff": "Replaced unconstrained Python `exec()` analytics with an AST whitelist validator + isolated SQLite tenant scoping, blocking arbitrary import/attribute traversal before code execution while keeping sub-10ms local CRM aggregation.",
        "stack": ["Anthropic Claude", "Python", "Pydantic", "AST Sandbox", "HITL", "SQLite", "Docker", "GitHub Actions"],
        "language": "Python"
    },
    "rag-gateway-eval-cost-controls": {
        "title": "Production RAG Gateway & Cost Controls",
        "domainId": "llmops-eval",
        "tracks": ["llmops", "agentic-ai", "cloud"],
        "flagship": True,
        "flagshipRank": 2,
        "metrics": ["61.9% Cost Saved", "1.4 ms Cache Hit", "1.000 RAGAS Recall", "235 Pytest Gates"],
        "summary": "End-to-end production LLMOps FAQ gateway (FastAPI SSE, ChromaDB, OpenAI, Arize Phoenix OTel, RAGAS, LLM Guard) combining tiered complexity routing (`gpt-4o-mini` vs `gpt-4o`), semantic caching, and hot-folder ingestion with quarantine.",
        "tradeoff": "Placed a >=0.92 cosine Chroma semantic cache and complexity classifier ahead of retrieval/generation—cutting p50 repeat-query latency by 1,468x (to 1.4 ms at $0 token cost) and saving 61.9% across mixed workloads without sacrificing 1.000 golden-set faithfulness.",
        "stack": ["FastAPI", "ChromaDB", "OpenAI", "RAGAS", "Arize Phoenix", "OpenTelemetry", "LLM Guard", "Python"],
        "language": "Python"
    },
    "multi-agent-banking-system": {
        "title": "Multi-Agent Banking System (A2A + LangGraph)",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "fintech", "cloud"],
        "flagship": True,
        "flagshipRank": 3,
        "metrics": ["18/18 A2A Pass", "Zero-Knowledge Equity", "MCP SQL Toolbox", "5/5 LangGraph Suites"],
        "summary": "Decoupled retail banking microservices (`manager`, `deposit`, `loan`) communicating over Google ADK Agent-to-Agent (A2A) JSON-RPC + MCP Database Toolbox, paired with a stateful LangGraph intent router and deterministic underwriting math.",
        "tradeoff": "Isolated loan debt-to-equity arithmetic inside a deterministic Python `BaseAgent` (`TotalValueAgent`) and exposed only a boolean `check-minimum-balance` A2A endpoint on `DepositAgent`—eliminating LLM math hallucinations and cross-service balance disclosure.",
        "stack": ["Google ADK", "A2A JSON-RPC", "LangGraph", "MCP Toolbox", "Vertex AI", "Cloud SQL", "Python", "GitHub Actions"],
        "language": "Python"
    },
    "trace-aml-sar-compliance-engine": {
        "title": "TRACE: FinCEN AML & SAR Compliance Engine",
        "domainId": "fintech-ai",
        "tracks": ["fintech", "agentic-ai", "ai-security"],
        "flagship": True,
        "flagshipRank": 4,
        "metrics": ["31/31 Tests Pass", "50% Compute Saved", "10 Verified SARs", "SHA-256 Audit Logs"],
        "summary": "Two-stage financial crime investigation and FinCEN Form 111 SAR filing engine combining Chain-of-Thought AML typology classification, mandatory human-in-the-loop compliance gates, ReACT statutory synthesis, and tamper-evident SHA-256 JSONL logs.",
        "tradeoff": "Inserted a mandatory HITL compliance gate between Stage-1 CoT triage and Stage-2 ReACT narrative drafting—halting false-positive alerts early for 50% Stage-2 LLM compute avoidance while enforcing regex-validated 31 CFR / 31 USC citations.",
        "stack": ["OpenAI", "Pydantic v2", "Chain-of-Thought", "ReACT", "HITL", "SHA-256 Audit", "Python", "GitHub Actions"],
        "language": "Python"
    },
    "bedrock-rag-threat-modeling-guardrails": {
        "title": "AWS Bedrock RAG Threat Modeling & Guardrails",
        "domainId": "ai-security-grc",
        "tracks": ["ai-security", "cloud", "llmops"],
        "flagship": True,
        "flagshipRank": 5,
        "metrics": ["36/36 Red-Team Blocked", "STRIDE-ML + ML-BOM", "IAM Explicit-Deny", "AgentCore Lockdown"],
        "summary": "Enterprise security hardening for an Amazon Bedrock Knowledge Base & Claude Sonnet 4.5 assistant: STRIDE-ML threat modeling, CycloneDX-style ML-BOM provenance, explicit-deny IAM scoping, AgentCore tool lockdown, and CloudWatch alarming.",
        "tradeoff": "Layered Bedrock Guardrails (topic/PII/prompt-attack filters) on top of IAM explicit-deny policies and AgentCore tool perimeter lockdown so even paraphrased multi-hop exfiltration prompts (`T5_paraphrased_pii`) fail closed (36/36 runs blocked).",
        "stack": ["AWS Bedrock", "Claude Sonnet 4.5", "Bedrock Guardrails", "IAM", "CloudWatch", "STRIDE-ML", "Python"],
        "language": "Python"
    },
    "clinical-ai-governance-fairness-audit": {
        "title": "HealthGuard: Clinical AI Governance & EU AI Act Audit",
        "domainId": "ai-security-grc",
        "tracks": ["ai-security", "mlops"],
        "flagship": True,
        "flagshipRank": 6,
        "metrics": ["-31.4 pp FNR Gap", "34/34 Tests Pass", "TreeSHAP Attribution", "EU AI Act Annex III"],
        "summary": "End-to-end AI Security Governance, Risk & Compliance (GRC) portfolio for clinical diabetes triage—combining intersectional subgroup fairness auditing, TreeSHAP proxy bias attribution, counterfactual de-biasing, MITRE ATLAS, and EU AI Act Annex III artifacts.",
        "tradeoff": "Used TreeSHAP interaction values to prove `insurance_type` acted as a socioeconomic proxy inflating Medicaid False Negative Rates, then applied counterfactual sample re-weighting to slash the Medicaid-Private FNR disparity by 31.4 percentage points without collapsing overall AUC.",
        "stack": ["Scikit-Learn", "TreeSHAP", "EU AI Act", "NIST AI RMF", "MITRE ATLAS", "Fairness AI", "Python", "GitHub Actions"],
        "language": "Python"
    },
    "claude-extraction-eval-observability": {
        "title": "Claude Extraction Eval & Confidence Calibration",
        "domainId": "llmops-eval",
        "tracks": ["llmops", "agentic-ai"],
        "flagship": True,
        "flagshipRank": 7,
        "metrics": ["104/104 Pytest Pass", "0.865 Slice Brier Caught", "0 Mypy/Ruff Errors", "3-Package Monorepo"],
        "summary": "Three-package production evaluation and observability monorepo for Anthropic Claude pipelines: sliced Brier confidence calibration with blind second-model review, two-pass arithmetic-validated mortgage extraction, and timeout-isolated supply-chain synthesis.",
        "tradeoff": "Aggregate Brier score (`0.291`) hid catastrophic overconfidence on `umbrella / exclusions` (`conf=0.93, acc=0.00, Brier=0.865`); slicing calibration across `policy_type x field` + error-classified retry halted `missing_source` failures in 1 call instead of 4.",
        "stack": ["Claude Haiku 4.5", "Brier Calibration", "Structured Outputs", "Pytest", "Mypy", "Sentence-Transformers", "Python", "GitHub Actions"],
        "language": "Python"
    },
    "nasa-mission-rag-eval-engine": {
        "title": "NASA Mission Archive RAG & Async RAGAS Engine",
        "domainId": "llmops-eval",
        "tracks": ["llmops", "agentic-ai"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["8,046 Chroma Chunks", "0.9861 RAGAS Precision", "0.9583 Faithfulness", "30 Pytest Gates"],
        "summary": "End-to-end aerospace RAG and real-time asynchronous RAGAS v0.4.3 evaluation engine over 6.23 MB of primary NASA Apollo 11, Apollo 13, and Challenger (STS-51L) transcripts—combining sentence-aligned idempotent ChromaDB indexing, query-inferred mission routing, epistemic grounding, and Streamlit live telemetry.",
        "tradeoff": "Paired query-inferred single-mission ChromaDB metadata routing + 2k candidate deduplication with concurrent AsyncOpenAI RAGAS scoring (`IncompleteOutput` 8k -> 16k fallback)—achieving 0.9861 context precision and 0.9583 faithfulness while preserving unfiltered cross-mission comparisons.",
        "stack": ["OpenAI", "ChromaDB", "RAGAS", "Streamlit", "AsyncIO", "Pytest", "Python", "GitHub Actions"],
        "language": "Python"
    },
    "claude-multiagent-pr-reviewer": {
        "title": "Claude Multi-Agent GitHub PR Reviewer",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["Parallel Subagents", "Claude Agent SDK", "MCP GitHub + ESLint", "Zod Bounded Schemas"],
        "summary": "Bounded-autonomy TypeScript GitHub Pull Request review orchestrator built on the Claude Agent SDK—coordinating parallel security/quality, extended-thinking test coverage, and refactoring subagents with MCP tools, sliding-window rate limits, and Zod validation.",
        "tradeoff": "Enforced read-only GitHub/ESLint MCP tool permissions, per-subagent turn budgets, and strict Zod output schemas so autonomous PR reviews never mutate branches or runaway on large diffs.",
        "stack": ["TypeScript", "Claude Agent SDK", "MCP", "GitHub API", "ESLint", "Zod", "GitHub Actions"],
        "language": "TypeScript"
    },
    "adk-research-workflow-engine": {
        "title": "ADK Autonomous Research Workflow Engine",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["7-Stage ADK Pipeline", "17-Source Parallel Fan-Out", "0.92 Critic Convergence", "3/3 Routing"],
        "summary": "Seven-stage autonomous research engine built on Google Agent Development Kit (ADK) and Vertex AI Gemini—orchestrating deterministic JSON routing, concurrent `ParallelAgent` source gathering, `LoopAgent` critic refinement, and APA synthesis.",
        "tradeoff": "Combined `ParallelAgent` fan-out across 17 academic/web sources with a bounded `LoopAgent` evaluator-optimizer critic that terminates automatically once rubric quality exceeds `0.90` (converging at `0.92`).",
        "stack": ["Google ADK", "Vertex AI", "Gemini", "ParallelAgent", "LoopAgent", "Python"],
        "language": "Python"
    },
    "adk-retail-concierge-agent": {
        "title": "ADK Multi-Tool Retail Concierge Agent",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["MCP MySQL Toolbox", "Vertex AI Search RAG", "Google Search Grounding", "Parameterized SQL"],
        "summary": "Domain-guarded retail customer concierge built with Google ADK and Gemini 2.5 Flash—unifying MCP Database Toolbox parameterized MySQL pricing queries, Vertex AI Discovery Engine chunked RAG, and Google Search grounded sub-agents.",
        "tradeoff": "Delegated catalog pricing strictly to parameterized MCP MySQL tool descriptors while routing care guides to Vertex AI Search RAG, eliminating SQL injection surfaces and price hallucinations.",
        "stack": ["Google ADK", "Gemini 2.5 Flash", "MCP Toolbox", "Vertex AI Search", "MySQL", "Python"],
        "language": "Python"
    },
    "vectrabank-agentic-rag": {
        "title": "VectraBank 6-Agent Azure Semantic Kernel RAG",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "fintech", "cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["30/30 Specialist Runs", "7/7 Fault-Injection Pass", "6 Chroma Collections", "Azure SQL + Blob"],
        "summary": "Regulated banking intelligence engine orchestrating 6 sequential Microsoft Semantic Kernel specialists grounded in Azure SQL ledgers, Azure Blob policy stores, and 6-collection ChromaDB hybrid RAG with deterministic Python risk scoring.",
        "tradeoff": "Separated qualitative policy retrieval (6 domain-isolated ChromaDB collections + Azure Blob) from deterministic Python credit/DTI scoring grounded in Azure SQL ledgers.",
        "stack": ["Semantic Kernel", "Azure AI Foundry", "Azure SQL", "Azure Blob", "ChromaDB", "Pydantic v2", "Python"],
        "language": "Python"
    },
    "agentquant-timeseries-pipeline": {
        "title": "AgentQuant Multi-Agent Time-Series Pipeline",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "fintech"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["6 Agents / 3 GroupChats", "IQR Outlier Scrubbing", "HITL Approval Gate", "Self-Healing Plots"],
        "summary": "Four-stage quantitative time-series analysis workflow orchestrated with Microsoft Semantic Kernel `AgentGroupChat` and Azure OpenAI—coordinating data cleaning, `AnalysisChecker` validation loops, HITL approval, and self-healing `PythonExecutor` plotting.",
        "tradeoff": "Paired every generative analysis stage with a deterministic `AnalysisChecker` critic inside `AgentGroupChat` before human sign-off and sandboxed matplotlib execution.",
        "stack": ["Semantic Kernel", "Azure OpenAI", "AgentGroupChat", "HITL", "Matplotlib", "Python"],
        "language": "Python"
    },
    "mcp-llm-pricing-intelligence": {
        "title": "MCP Cross-Provider LLM Pricing Intelligence",
        "domainId": "multi-agent-mcp",
        "tracks": ["agentic-ai", "llmops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["2 Custom MCP Servers", "FastMCP + Firecrawl v2", "SQLite Persistence", "Claude Sonnet 4.5"],
        "summary": "Autonomous LLM inference pricing analyst built on the Model Context Protocol (MCP), coordinating a custom FastMCP Firecrawl v2 web-scraping server, SQLite persistence MCP server, and Claude Sonnet 4.5 stdio JSON-RPC client.",
        "tradeoff": "Decoupled live web scraping (Firecrawl MCP) from normalized pricing queries (SQLite MCP) over stdio JSON-RPC so comparative token-cost analysis runs reproducibly over cached provider snapshots.",
        "stack": ["Model Context Protocol", "FastMCP", "Anthropic Claude", "Firecrawl", "SQLite", "Python"],
        "language": "Python"
    },
    "swiftguard-mt103-fraud-pipeline": {
        "title": "SWIFTGuard: MT103 International Wire Screening",
        "domainId": "fintech-ai",
        "tracks": ["fintech", "agentic-ai"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["4 Agentic Patterns", "ISO 9362 + OFAC/FATF", "3-Agent Parallel Screen", "MT103 Self-Healing"],
        "summary": "End-to-end SWIFT MT103 international wire screening pipeline orchestrating four agentic patterns: Evaluator-Optimizer syntax self-healing, 3-agent parallel fraud & OFAC/FATF corridor screening, 5-stage prompt chaining, and Orchestrator-Worker settlement.",
        "tradeoff": "Ran fraud behavioural scoring, ISO 9362 BIC validation, and OFAC/FATF sanctions checks concurrently via 3-way parallel fan-out after deterministic MT103 tag repair.",
        "stack": ["OpenAI GPT-4o", "SWIFT MT103", "OFAC Screening", "Multi-Agent Workflows", "Pydantic", "Python"],
        "language": "Python"
    },
    "edgar-rag-financial-analyst-agent": {
        "title": "FinTool: SEC EDGAR 10-K & NL-to-SQL Analyst",
        "domainId": "fintech-ai",
        "tracks": ["fintech", "agentic-ai"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["FY2024 SEC 10-K RAG", "Schema-Aware NL-to-SQL", "Live Yahoo Finance", "Auto PII Masking"],
        "summary": "Autonomous equity and portfolio research coordinator built with LlamaIndex—combining SEC Form 10-K vector retrieval (`AAPL`, `GOOGL`, `TSLA`), schema-aware SQLite NL-to-SQL portfolio queries, live Yahoo Finance telemetry, and automatic PII masking.",
        "tradeoff": "Enforced read-only SQLite validation and regex PII redaction on client portfolio tables before blending internal holdings with public SEC 10-K filings.",
        "stack": ["LlamaIndex", "SEC EDGAR", "Text-to-SQL", "Yahoo Finance", "PII Redaction", "SQLite", "Python"],
        "language": "Python"
    },
    "agentic-alpha-trading-system": {
        "title": "Agentic Alpha: 6-Agent Equity & Reg M Platform",
        "domainId": "fintech-ai",
        "tracks": ["fintech", "agentic-ai"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["6 PydanticAI Agents", "Fibonacci + RSI Tools", "SEC Reg M Compliance", "ACID Dual Storage"],
        "summary": "Six-agent quantitative equity analysis and risk governance platform built with PydanticAI and Streamlit—enforcing sequential analyst-to-supervisor execution, deterministic Fibonacci/RSI technical indicators, SEC Regulation M compliance, and SQLite/PostgreSQL ACID storage.",
        "tradeoff": "Gated trade recommendations behind an independent Compliance & Risk Supervisor agent validating position concentration limits and SEC Regulation M restricted-list rules.",
        "stack": ["PydanticAI", "Streamlit", "Quantitative Finance", "SEC Compliance", "PostgreSQL", "SQLite", "Python"],
        "language": "Python"
    },
    "adversarial-ml-rag-redteam-suite": {
        "title": "Offensive Adversarial ML & RAG Red-Team Suite",
        "domainId": "ai-security-grc",
        "tracks": ["ai-security", "mlops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["FGSM 94.4% -> 27.2%", "7.9% Poisoned Recall", "83.3% RAG Exfiltration", "804 Container CVEs"],
        "summary": "End-to-end offensive AI red-team assessment targeting an enterprise expense platform—demonstrating PyTorch FGSM gradient evasion, training-set label-flip poisoning, FAISS/OpenAI indirect RAG persona hijacking & salary exfiltration, and Trivy container auditing.",
        "tradeoff": "Quantified exact exploit blast radii across 5 attack surfaces (vision gradients, training weights, vector chunks, system prompts, and container base images) paired with prioritized remediation controls.",
        "stack": ["PyTorch", "FGSM Adversarial ML", "Data Poisoning", "FAISS", "RAG Security", "Trivy", "Python"],
        "language": "Python"
    },
    "hardened-rag-agent-security-gateway": {
        "title": "Hardened Local RAG Agent Security Gateway",
        "domainId": "ai-security-grc",
        "tracks": ["ai-security", "agentic-ai"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["8/8 Exploit Regression", "5-Layer Defense Runtime", "OWASP LLM Top 10", "SIEM Detection Rules"],
        "summary": "Offensive exploit suite and 5-layer defense-in-depth security runtime for a local ChromaDB + Mistral-7B (Ollama) tool-calling HR RAG agent—mitigating jailbreaks, indirect vector poisoning, and unauthorized HR database task hijacking.",
        "tradeoff": "Sanitized untrusted retrieved ChromaDB chunks and enforced least-privilege tool argument schemas + HITL confirmation so poisoned policy docs cannot trigger privileged HR DB mutations (8/8 regression pass).",
        "stack": ["Ollama (Mistral-7B)", "ChromaDB", "OWASP LLM Top 10", "Prompt Injection Defense", "SIEM", "Python"],
        "language": "Python"
    },
    "census-income-api": {
        "title": "Census Income MLOps & Subgroup Fairness API",
        "domainId": "mlops-pipelines",
        "tracks": ["mlops", "ai-security", "cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["8-Dim Fairness Audit", "Leakage-Safe Pipeline", "Live FastAPI Service", "CI/CD Render Deploy"],
        "summary": "End-to-end tabular MLOps pipeline and live FastAPI inference service for US Census income classification—featuring leakage-safe encoder serialization, automated subgroup metrics across 8 demographic dimensions, Model Card governance, and GitHub Actions CI/CD.",
        "tradeoff": "Fit one-hot encoders and scalers strictly on training folds and serialized artifacts jointly with the classifier, preventing train-test distribution leakage across demographic slices.",
        "stack": ["FastAPI", "Scikit-Learn", "Fairness Auditing", "Model Card", "Docker", "GitHub Actions", "Render", "Python"],
        "language": "Python",
        "liveUrl": "https://census-income-api-3hq5.onrender.com/docs"
    },
    "finbert-sentiment-mlops-service": {
        "title": "FinBERT Real-Time Sentiment MLOps Service",
        "domainId": "mlops-pipelines",
        "tracks": ["mlops", "fintech", "llmops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["DVC + MLflow Registry", "Prometheus Telemetry", "Deepchecks NLP Drift", "AWS ECS CI/CD"],
        "summary": "Production MLOps pipeline for financial news sentiment classification (`FinBERT`) featuring DVC data versioning, gated MLflow `@production` promotion, FastAPI + Prometheus latency/confidence metrics, Deepchecks NLP drift CI gates, and AWS ECS deployment.",
        "tradeoff": "Gated Docker image promotion on both MLflow macro-F1 regression thresholds and Deepchecks text-property drift checks inside GitHub Actions CI/CD.",
        "stack": ["FinBERT", "MLflow", "DVC", "FastAPI", "Prometheus", "Deepchecks", "AWS ECS", "GitHub Actions"],
        "language": "Python"
    },
    "nyc-rental-pricing-mlflow-pipeline": {
        "title": "NYC Rental Pricing MLflow + Hydra + W&B DAG",
        "domainId": "mlops-pipelines",
        "tracks": ["mlops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["$32.42 Val MAE", "KL-Divergence Gates", "Hydra Sweep Lineage", "TF-IDF + Geospatial"],
        "summary": "End-to-end reproducible 6-step MLflow + Hydra + Weights & Biases pipeline for NYC short-term rental price regression—featuring Pytest/SciPy KL-divergence data validation gates and multimodal TF-IDF + spatial feature engineering.",
        "tradeoff": "Enforced automated SciPy Kolmogorov-Smirnov / KL-divergence distribution checks as a blocking `pytest` step in the MLflow DAG prior to Random Forest training.",
        "stack": ["MLflow", "Hydra", "Weights & Biases", "Scikit-Learn", "SciPy", "Pytest", "Python"],
        "language": "Python"
    },
    "credit-card-churn-ml-pipeline": {
        "title": "Credit Card Customer Attrition ML Pipeline",
        "domainId": "mlops-pipelines",
        "tracks": ["mlops", "fintech"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["95% Test Accuracy", "0.84 Minority Churn F1", "10,127 Bank Profiles", "10.0/10 Pylint"],
        "summary": "Clean-code modular Python ML pipeline predicting credit card customer attrition across 10,127 banking profiles—featuring automated EDA artifact generation, `RandomizedSearchCV` Random Forest vs Logistic Regression benchmarking, structured logging, and Pytest suites.",
        "tradeoff": "Refactored monolithic notebook experimentation into PEP-8 (`10.0/10` Pylint) production modules with deterministic artifact fixtures and fixture-driven `pytest` assertions.",
        "stack": ["Scikit-Learn", "Random Forest", "SHAP", "Pytest", "Clean Code", "Python"],
        "language": "Python"
    },
    "automated-ml-drift-risk-monitor": {
        "title": "Closed-Loop ML Drift & Attrition Risk Monitor",
        "domainId": "mlops-pipelines",
        "tracks": ["mlops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["Raw-Comparison Drift Test", "Auto Cron Retraining", "4-Endpoint Flask API", "Versioned Archival"],
        "summary": "Closed-loop MLOps monitoring and corporate attrition risk assessment system in Python & Flask—automating multi-source batch ingestion, raw-comparison F1 drift detection, conditional model retraining & redeployment, and operational diagnostics.",
        "tradeoff": "Implemented strict raw-comparison drift gating (`new_f1 < deployed_f1` on fresh ground-truth batches) to trigger automated retraining only on genuine predictive degradation.",
        "stack": ["Flask", "Scikit-Learn", "Model Drift", "Cron Automation", "MLOps", "Python"],
        "language": "Python"
    },
    "Text-Summarizer-Project": {
        "title": "PEGASUS Abstractive NLP Summarization Pipeline",
        "domainId": "mlops-pipelines",
        "tracks": ["mlops", "llmops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["4-Stage Config DAG", "HuggingFace PEGASUS", "SAMSum Fine-Tuning", "FastAPI + Docker"],
        "summary": "Config-driven 4-stage abstractive NLP text summarization pipeline fine-tuning `google/pegasus-cnn_dailymail` on SAMSum dialogue corpora with PyTorch, Hugging Face Transformers, ROUGE evaluation, and Dockerized FastAPI serving.",
        "tradeoff": "Decoupled YAML schema configuration (`config.yaml` + `params.yaml`) from stage entities (` ingestion`, `validation`, `transformation`, `trainer`) for reproducible seq2seq fine-tuning.",
        "stack": ["PyTorch", "Hugging Face", "PEGASUS", "FastAPI", "Docker", "Python"],
        "language": "Python"
    },
    "aws-serverless-fraud-ml-pipeline": {
        "title": "AWS Glue PySpark & Serverless Fraud ML Pipeline",
        "domainId": "cloud-swe",
        "tracks": ["cloud", "mlops", "fintech"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["10x PySpark Speedup", "AWS Glue 4.0 MLlib", "S3 -> Lambda Retrain", "ECS Fargate FastAPI"],
        "summary": "Cloud-native AWS fraud detection platform migrating local PySpark training to distributed AWS Glue 4.0 MLlib, S3-triggered AWS Lambda automated retraining & timestamped model archival, and ECS Fargate FastAPI real-time inference.",
        "tradeoff": "Eliminated shuffle bottlenecks in distributed Glue 4.0 Random Forest training via `.repartition(16).cache()` before pipeline fitting—cutting job runtime ~10x while enforcing least-privilege IAM roles per service.",
        "stack": ["AWS Glue 4.0", "PySpark MLlib", "AWS Lambda", "ECS Fargate", "Amazon S3", "FastAPI", "IAM"],
        "language": "Python"
    },
    "aws-organizations-landing-zone-peering": {
        "title": "AWS Organizations M&A Landing Zone & FinOps",
        "domainId": "cloud-swe",
        "tracks": ["cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["5-OU Control Tower", "Tagging SCP + Config", "FinOps Budget Freeze", "56.7 ms Cross-Region RTT"],
        "summary": "Enterprise multi-account AWS Organizations and Control Tower landing zone for M&A cloud governance—combining preventative Tagging Service Control Policies (SCPs), AWS Config detective rules, automated FinOps Budget freezes, and verified cross-region VPC peering.",
        "tradeoff": "Paired preventative Organization SCPs (blocking untagged EC2/RDS creation at launch) with automated AWS Budgets IAM freeze actions to enforce hard M&A cost ceilings.",
        "stack": ["AWS Organizations", "Control Tower", "SCPs", "AWS Config", "VPC Peering", "FinOps", "Boto3"],
        "language": "Python"
    },
    "aws-bedrock-legal-summarizer-iac": {
        "title": "Serverless AWS Bedrock Legal Summarizer (IaC)",
        "domainId": "cloud-swe",
        "tracks": ["cloud", "llmops"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["2.13s E2E Latency", "CloudFormation IaC", "Nova Micro + Llama 3", "AES-256 S3 + FinOps"],
        "summary": "Event-driven serverless legal contract summarization infrastructure on AWS provisioned via CloudFormation—combining AES-256 S3 buckets, Python 3.11 Lambda, dual-model Amazon Bedrock fallback (`Nova Micro` + `Llama 3`), and S3 Intelligent-Tiering FinOps.",
        "tradeoff": "Architected automatic cross-family Bedrock fallback (`Amazon Nova Micro` primary -> `Meta Llama 3` secondary) inside Lambda to guarantee 2.13s low-cost summarization resilience under regional throttling.",
        "stack": ["AWS CloudFormation", "Amazon Bedrock", "AWS Lambda", "Amazon S3", "FinOps", "Serverless", "Python"],
        "language": "YAML / Python"
    },
    "adaptive-flashcard-cli": {
        "title": "Adaptive Spaced-Repetition CLI Engine",
        "domainId": "cloud-swe",
        "tracks": ["cloud"],
        "flagship": False,
        "flagshipRank": 99,
        "metrics": ["97% Pytest Coverage", "Zero Dependencies", "Strategy + Factory OOP", "Fuzzy Levenshtein Match"],
        "summary": "Zero-dependency Python CLI active-recall learning engine implementing Strategy & Factory quiz patterns (`Sequential`, `Random`, cooldown-spaced `Adaptive` retry scheduling), dual-schema JSON validation, and fuzzy typo tolerance.",
        "tradeoff": "Built purely on Python 3.11 stdlib (`dataclasses`, `abc`, `difflib`) with Strategy/Factory decoupling, achieving 97% test coverage and instant portable execution without third-party dependency drift.",
        "stack": ["Python 3.11", "Design Patterns", "Strategy Pattern", "Pytest (97%)", "Type-Checked", "CLI"],
        "language": "Python"
    },
}


FALLBACK_MERMAIDS = {
    "adversarial-ml-rag-redteam-suite": (
        "flowchart LR\n"
        "    T[\"Target Expense AI Platform\"] --> S1[\"01 · PyTorch FGSM Vision Evasion\\n94.36% -> 27.18% Acc\"]\n"
        "    T --> S2[\"02 · Label-Flip Data Poisoning\\n7.92% Target Class Recall\"]\n"
        "    T --> S3[\"03 · Direct Prompt Hijacking\\nPersona & Policy Override\"]\n"
        "    T --> S4[\"04 · FAISS RAG Exfiltration\\n83.3% Exec Salary Leak\"]\n"
        "    T --> S5[\"05 · Trivy Container Audit\\n804 Base Image CVEs\"]\n"
        "    S1 & S2 & S3 & S4 & S5 --> REM[\"Prioritized Defense-in-Depth Remediation Matrix\"]"
    ),
    "aws-bedrock-legal-summarizer-iac": (
        "flowchart LR\n"
        "    DOC[\"Legal Contract Upload\"] --> S3IN[\"AES-256 S3 Input Bucket\\nEvent Notification\"]\n"
        "    S3IN --> LMB[\"AWS Lambda (Python 3.11)\\n2.13s E2E Orchestrator\"]\n"
        "    LMB -->|Primary| NOVA[\"Amazon Bedrock\\nNova Micro\"]\n"
        "    LMB -.->|Throttle Fallback| LLAMA[\"Amazon Bedrock\\nMeta Llama 3\"]\n"
        "    NOVA & LLAMA --> S3OUT[\"AES-256 S3 Output Bucket\\nIntelligent-Tiering FinOps\"]\n"
        "    LMB --> CW[\"CloudWatch Logs & Alarms\"]"
    ),
    "aws-organizations-landing-zone-peering": (
        "flowchart TD\n"
        "    ROOT[\"AWS Organizations Management Account\\nControl Tower Landing Zone\"] --> SCP[\"Preventative Tagging SCP\\nBlock Untagged EC2/RDS\"]\n"
        "    ROOT --> CFG[\"Detective AWS Config Rules\\nrequired-tags Compliance\"]\n"
        "    ROOT --> FIN[\"FinOps AWS Budgets\\nAutomated IAM Freeze Action\"]\n"
        "    ROOT --> OUS[\"5 Organizational Units\\nSecurity · Infra · Prod · Sandbox · M&A\"]\n"
        "    OUS --> VPC[\"Verified Cross-Region VPC Peering\\nus-east-1 <-> us-west-2 (56.7ms RTT)\"]"
    ),
    "claude-extraction-eval-observability": (
        "flowchart LR\n"
        "    subgraph P1[\"01 · Policy Extractor (45 Tests)\"]\n"
        "        E1[\"Claude Primary Extractor\"] --> R1[\"Blind Second-Model Reviewer\"]\n"
        "        R1 --> B1[\"Policy x Field Sliced Brier\\n(Caught 0.865 Umbrella Overconfidence)\"]\n"
        "    end\n"
        "    subgraph P2[\"02 · Mortgage Validator (25 Tests)\"]\n"
        "        E2[\"2-Pass Doc Classifier\"] --> A2[\"Python Cross-Field Math Gate\\n(Caught -$1,250 YTD Mismatch)\"]\n"
        "    end\n"
        "    subgraph P3[\"03 · Supply-Chain Synthesis (34 Tests)\"]\n"
        "        E3[\"Timeout-Isolated ReaderResult\"] --> V3[\"MiniLM Vector Claim Corroboration\"]\n"
        "    end"
    ),
    "claude-multiagent-pr-reviewer": (
        "flowchart TD\n"
        "    PR[\"GitHub Pull Request Diff\"] --> ORCH[\"Claude Agent SDK Orchestrator\\nSliding-Window Rate Limiter\"]\n"
        "    ORCH --> A1[\"Security & Code Quality Subagent\\nGitHub + ESLint MCP Tools\"]\n"
        "    ORCH --> A2[\"Test Coverage Subagent\\nExtended Thinking Budget\"]\n"
        "    ORCH --> A3[\"Refactoring & Maintainability Subagent\"]\n"
        "    A1 & A2 & A3 --> ZOD[\"Strict Zod Report Validator\\nBounded Read-Only Autonomy\"]"
    ),
    "clinical-ai-governance-fairness-audit": (
        "flowchart LR\n"
        "    DATA[\"Clinical Diabetes Triage Cohort\"] --> BASE[\"Baseline Classifier\\nIntersectional Subgroup Audit\"]\n"
        "    BASE --> SHAP[\"TreeSHAP Proxy Attribution\\nInsurance -> Socioeconomic Bias\"]\n"
        "    SHAP --> DEBIAS[\"Counterfactual Sample Re-Weighting\\n-31.4 pp Medicaid-Private FNR Gap\"]\n"
        "    DEBIAS --> GRC[\"EU AI Act Annex III + NIST AI RMF\\nKRIs · MITRE ATLAS · Schrems II TIA\"]"
    ),
}


def extract_repo_details(slug: str) -> dict:
    repo_dir = SHOWCASE_ROOT / slug
    details = {
        "highlights": [],
        "mermaids": [],
        "quickStart": "",
        "ciWorkflow": None,
        "hasLiveDemoSvg": False,
        "primaryImage": None,
        "gallery": [],
    }
    if not repo_dir.exists():
        # Text-Summarizer-Project (remote-only in workspace)
        details["highlights"] = [
            "Modular 4-stage NLP pipeline (`data_ingestion`, `data_validation`, `data_transformation`, `model_trainer`) driven by YAML configuration.",
            "Fine-tunes `google/pegasus-cnn_dailymail` transformer weights on conversational SAMSum dialogue summaries with ROUGE-1/2/L evaluation.",
            "Exposes containerized FastAPI `/predict` & `/train` endpoints with GitHub Actions workflow templates."
        ]
        details["mermaids"] = [
            "flowchart LR\n    CFG[\"config.yaml + params.yaml\"] --> S1[\"Stage 1: Data Ingestion\\n(SAMSum Corpus)\"]\n    S1 --> S2[\"Stage 2: Schema Validation\"]\n    S2 --> S3[\"Stage 3: Tokenizer Transformation\\n(PEGASUS Seq2Seq)\"]\n    S3 --> S4[\"Stage 4: PyTorch Trainer\\n+ ROUGE Evaluation\"]\n    S4 --> API[\"Dockerized FastAPI\\nInference Endpoint\"]"
        ]
        details["quickStart"] = "git clone https://github.com/kenseiAmit/Text-Summarizer-Project.git\ncd Text-Summarizer-Project\npip install -r requirements.txt\npython app.py"
        TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
        svg_path = TELEMETRY_DIR / "Text-Summarizer-Project.svg"
        svg_path.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 420" width="100%">'
            '<rect width="960" height="420" rx="16" fill="#0B1120" stroke="#1E293B" stroke-width="2"/>'
            '<text x="44" y="56" fill="#F8FAFC" font-family="ui-sans-serif, system-ui, sans-serif" font-size="22" font-weight="700">PEGASUS 4-Stage Abstractive Summarization Pipeline</text>'
            '<text x="44" y="84" fill="#94A3B8" font-family="ui-monospace, monospace" font-size="13">google/pegasus-cnn_dailymail · SAMSum Dialogue Corpus · PyTorch + FastAPI + Docker</text>'
            '<g transform="translate(44, 128)">'
            '<rect width="196" height="132" rx="12" fill="#111827" stroke="#3B82F6" stroke-opacity="0.5"/>'
            '<text x="20" y="34" fill="#38BDF8" font-family="ui-monospace, monospace" font-size="12" font-weight="700">STAGE 01</text>'
            '<text x="20" y="62" fill="#F8FAFC" font-family="ui-sans-serif, sans-serif" font-size="15" font-weight="700">Data Ingestion</text>'
            '<text x="20" y="88" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">SAMSum zip fetch &amp;</text>'
            '<text x="20" y="106" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">artifact extraction</text>'
            '</g>'
            '<g transform="translate(268, 128)">'
            '<rect width="196" height="132" rx="12" fill="#111827" stroke="#06B6D4" stroke-opacity="0.5"/>'
            '<text x="20" y="34" fill="#06B6D4" font-family="ui-monospace, monospace" font-size="12" font-weight="700">STAGE 02</text>'
            '<text x="20" y="62" fill="#F8FAFC" font-family="ui-sans-serif, sans-serif" font-size="15" font-weight="700">Schema Validation</text>'
            '<text x="20" y="88" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">Train/Val/Test split</text>'
            '<text x="20" y="106" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">contract verification</text>'
            '</g>'
            '<g transform="translate(492, 128)">'
            '<rect width="196" height="132" rx="12" fill="#111827" stroke="#A855F7" stroke-opacity="0.5"/>'
            '<text x="20" y="34" fill="#C084FC" font-family="ui-monospace, monospace" font-size="12" font-weight="700">STAGE 03</text>'
            '<text x="20" y="62" fill="#F8FAFC" font-family="ui-sans-serif, sans-serif" font-size="15" font-weight="700">Tokenization</text>'
            '<text x="20" y="88" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">AutoTokenizer seq2seq</text>'
            '<text x="20" y="106" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">1024/128 tensor masks</text>'
            '</g>'
            '<g transform="translate(716, 128)">'
            '<rect width="200" height="132" rx="12" fill="#111827" stroke="#10B981" stroke-opacity="0.5"/>'
            '<text x="20" y="34" fill="#34D399" font-family="ui-monospace, monospace" font-size="12" font-weight="700">STAGE 04</text>'
            '<text x="20" y="62" fill="#F8FAFC" font-family="ui-sans-serif, sans-serif" font-size="15" font-weight="700">Trainer &amp; FastAPI</text>'
            '<text x="20" y="88" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">ROUGE-1/2/L eval +</text>'
            '<text x="20" y="106" fill="#94A3B8" font-family="ui-sans-serif, sans-serif" font-size="12">Docker REST serving</text>'
            '</g>'
            '<rect x="44" y="294" width="872" height="82" rx="12" fill="#0F172A" stroke="#1E293B"/>'
            '<text x="68" y="328" fill="#E2E8F0" font-family="ui-monospace, monospace" font-size="13" font-weight="600">Config-Driven MLOps Architecture: config/config.yaml + params.yaml -&gt; Modular Entities -&gt; FastAPI /predict</text>'
            '<text x="68" y="354" fill="#94A3B8" font-family="ui-monospace, monospace" font-size="12">Backbone: google/pegasus-cnn_dailymail · Metrics: ROUGE-1 / ROUGE-2 / ROUGE-L / ROUGE-Lsum · Container: Docker</text>'
            '</svg>',
            encoding="utf-8",
        )
        details["primaryImage"] = "assets/telemetry/Text-Summarizer-Project.svg"
        details["gallery"] = [{"caption": "4-Stage PEGASUS Seq2Seq Pipeline Architecture", "url": "assets/telemetry/Text-Summarizer-Project.svg"}]
        return details

    # Check CI workflow
    wf_dir = repo_dir / ".github" / "workflows"
    if wf_dir.exists():
        ymls = sorted(wf_dir.glob("*.yml"))
        if ymls:
            wf_name = ymls[0].name
            details["ciWorkflow"] = {
                "badge": f"https://github.com/{GITHUB_USER}/{slug}/actions/workflows/{wf_name}/badge.svg",
                "url": f"https://github.com/{GITHUB_USER}/{slug}/actions/workflows/{wf_name}"
            }

    # Copy live-demo.svg if present and ensure intrinsic width/height from viewBox for <img> rendering
    live_svg = repo_dir / "assets" / "live-demo.svg"
    if live_svg.exists():
        DEMOS_DIR.mkdir(parents=True, exist_ok=True)
        dest = DEMOS_DIR / f"{slug}.svg"
        svg_txt = live_svg.read_text(encoding="utf-8", errors="ignore")
        vb = re.search(r'viewBox="0\s+0\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)"', svg_txt)
        if vb:
            w_val, h_val = vb.group(1), vb.group(2)
            svg_txt = re.sub(r'\swidth="100%"', f' width="{w_val}" height="{h_val}"', svg_txt, count=1)
        dest.write_text(svg_txt, encoding="utf-8")
        details["hasLiveDemoSvg"] = True

    readme_path = repo_dir / "README.md"
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8", errors="ignore")

        # Extract mermaid diagrams
        mermaids = [m.strip() for m in re.findall(r"```mermaid\s*\n(.*?)```", text, re.S)]
        if not mermaids and slug in FALLBACK_MERMAIDS:
            mermaids = [FALLBACK_MERMAIDS[slug]]
        details["mermaids"] = mermaids[:2]

        # Extract bullet highlights if present
        bullets = re.findall(r"^-\s+\*\*([^*]+)\*\*:?\s*(.+)$", text, re.M)
        for b_title, b_rest in bullets[:5]:
            clean_title = b_title.strip().rstrip(":")
            clean_rest = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", b_rest).strip()
            clean_rest = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean_rest)
            # Strip inline latex $...$ for clean plain-text rendering
            clean_rest = re.sub(r"\$+[^$]+\$+", "", clean_rest)
            clean_rest = re.sub(r"\(\s*\)", "", clean_rest)
            clean_rest = re.sub(r"\s{2,}", " ", clean_rest).strip()
            if len(clean_rest) > 15:
                details["highlights"].append(f"{clean_title}: {clean_rest}")

        # Extract bash quickstart block
        bash_blocks = re.findall(r"```(?:bash|sh|zsh)\s*\n(.*?)```", text, re.S)
        if bash_blocks:
            details["quickStart"] = bash_blocks[-1].strip()

        # Extract markdown images
        imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)
        seen_paths = set()
        for idx, (alt, rel_path) in enumerate(imgs):
            rel_clean = rel_path.strip()
            if rel_clean.startswith("http") or rel_clean in seen_paths:
                continue
            src_file = repo_dir / rel_clean
            if src_file.exists() and src_file.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg"):
                seen_paths.add(rel_clean)
                if details["primaryImage"] is None and src_file.suffix.lower() == ".png":
                    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
                    dest_img = TELEMETRY_DIR / f"{slug}.png"
                    shutil.copy2(src_file, dest_img)
                    details["primaryImage"] = f"assets/telemetry/{slug}.png"
                    details["gallery"].append({
                        "caption": alt or "Empirical System Telemetry",
                        "url": f"assets/telemetry/{slug}.png"
                    })
                else:
                    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{slug}/main/{rel_clean}"
                    details["gallery"].append({
                        "caption": alt or Path(rel_clean).stem.replace("_", " ").title(),
                        "url": raw_url
                    })

    # Fallback if primaryImage wasn't matched in markdown but PNG exists in repo
    if details["primaryImage"] is None:
        pngs = [p for p in repo_dir.rglob("*.png") if ".venv" not in str(p) and "node_modules" not in str(p)]
        if pngs:
            TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
            dest_img = TELEMETRY_DIR / f"{slug}.png"
            shutil.copy2(pngs[0], dest_img)
            details["primaryImage"] = f"assets/telemetry/{slug}.png"
            details["gallery"].insert(0, {
                "caption": pngs[0].stem.replace("_", " ").title(),
                "url": f"assets/telemetry/{slug}.png"
            })

    return details


def build_trace_scenarios() -> list[dict]:
    """Load real verified runtime JSON traces & evaluation outputs from showcase repos."""
    # 1. Guarded SalesOps - Prompt Injection Blocked
    s1_raw = json.loads(
        (SHOWCASE_ROOT / "guarded-salesops-agent-runtime/traces/samples/03_input_guardrail_blocked.json")
        .read_text(encoding="utf-8")
    )
    # 2. Guarded SalesOps - HITL Outbound Email Gate
    s2_raw = json.loads(
        (SHOWCASE_ROOT / "guarded-salesops-agent-runtime/traces/samples/06_hitl_email_approved.json")
        .read_text(encoding="utf-8")
    )
    # 3. RAG Gateway Eval & Cost Ledger
    rag_eval = json.loads(
        (SHOWCASE_ROOT / "rag-gateway-eval-cost-controls/data/eval_results.json")
        .read_text(encoding="utf-8")
    )
    cost_lines = [
        json.loads(line)
        for line in (SHOWCASE_ROOT / "rag-gateway-eval-cost-controls/data/cost_log.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()[:6]
        if line.strip()
    ]
    # 4. FinCEN SAR Filing Artifact
    sar_raw = json.loads(
        (SHOWCASE_ROOT / "trace-aml-sar-compliance-engine/outputs/filed_sars/SAR_20261019_15EED0C0.json")
        .read_text(encoding="utf-8")
    )
    # 5. Bedrock Guardrails 36/36 Red-Team Summary
    bedrock_raw = json.loads(
        (SHOWCASE_ROOT / "bedrock-rag-threat-modeling-guardrails/evidence/07_final_summary.json")
        .read_text(encoding="utf-8")
    )

    return [
        {
            "id": "salesops-injection-block",
            "systemSlug": "guarded-salesops-agent-runtime",
            "badge": "GUARDRAIL BLOCK",
            "badgeTone": "danger",
            "title": "Prompt Injection & HR Policy Probe Blocked Pre-Inference",
            "subtitle": "guarded-salesops-agent-runtime · run_038eb543a3ef",
            "prompt": s1_raw["input"],
            "outcome": s1_raw["final_output"],
            "kpis": [
                {"label": "Guardrail Stage", "value": "Pre-Inference Input Gate"},
                {"label": "LLM Tokens Billed", "value": "0 (Short-Circuited)"},
                {"label": "Tools Invoked", "value": "0"},
                {"label": "PII / HR Leakage", "value": "0 Bytes"}
            ],
            "steps": [
                {
                    "stage": "01 · Request Ingress",
                    "status": "received",
                    "latency": "0.2 ms",
                    "detail": "Adversarial instruction-override prompt attempting to extract confidential layoff/termination data."
                },
                {
                    "stage": "02 · Input Guardrail (`salesops_data_access_policy`)",
                    "status": "blocked",
                    "latency": "3.8 ms",
                    "detail": "Matched restricted category `layoffs_and_terminations` -> immediate `action: block` before LLM invocation."
                },
                {
                    "stage": "03 · Structured Audit Sink",
                    "status": "ok",
                    "latency": "0.6 ms",
                    "detail": "Persisted immutable JSON trace `run_038eb543a3ef` with matched policy metadata and zero downstream tool execution."
                }
            ],
            "rawPayload": s1_raw
        },
        {
            "id": "salesops-hitl-approved",
            "systemSlug": "guarded-salesops-agent-runtime",
            "badge": "HITL GATED",
            "badgeTone": "success",
            "title": "Outbound B2B CRM Email Paused for Mandatory Human Approval",
            "subtitle": "guarded-salesops-agent-runtime · run_05648c187b54",
            "prompt": s2_raw["input"],
            "outcome": "Verified 5-stage defense chain: Input Allow -> Tool Schema Allow -> Mandatory HITL Approval -> Email Sent -> Redacted Output Trace.",
            "kpis": [
                {"label": "Defense Layers", "value": "5 Sequential Gates"},
                {"label": "HITL Decision", "value": "Operator Approved"},
                {"label": "Target Tool", "value": "send_email"},
                {"label": "Audit Status", "value": "PII-Scrubbed Pass"}
            ],
            "steps": [
                {
                    "stage": "01 · Input Guardrail",
                    "status": "ok",
                    "latency": "1.9 ms",
                    "detail": "Validated B2B SalesOps intent (`salesops_data_access_policy` -> `allow`)."
                },
                {
                    "stage": "02 · Tool Argument Guardrail",
                    "status": "ok",
                    "latency": "1.2 ms",
                    "detail": "Inspected `send_email` recipient & payload schema prior to side-effect execution."
                },
                {
                    "stage": "03 · Human-in-the-Loop Gate (`hitl_gate`)",
                    "status": "hitl",
                    "latency": "Operator Sign-Off",
                    "detail": "`requires_approval: true` -> Paused outbound external email until explicit operator approval."
                },
                {
                    "stage": "04 · Tool Execution & Post-Inference Scrub",
                    "status": "ok",
                    "latency": "14.2 ms",
                    "detail": "Dispatched email and passed output guardrail PII/policy verification."
                }
            ],
            "rawPayload": {
                "run_id": s2_raw["run_id"],
                "input": s2_raw["input"],
                "selected_tools": s2_raw["selected_tools"],
                "hitl_decision": s2_raw["hitl_decision"],
                "steps": s2_raw["steps"][:4]
            }
        },
        {
            "id": "rag-gateway-finops",
            "systemSlug": "rag-gateway-eval-cost-controls",
            "badge": "61.9% SAVED",
            "badgeTone": "info",
            "title": "Tiered LLM Routing (`gpt-4o-mini` vs `gpt-4o`) + 1.4ms Semantic Cache",
            "subtitle": "rag-gateway-eval-cost-controls · RAGAS 0.4.3 + OTel Cost Ledger",
            "prompt": "What is the weight of the Selkirk AMPED S2, and how does tiered routing optimize RAG unit economics?",
            "outcome": "Achieved 1.000 Faithfulness & Context Recall on golden eval set while cutting token spend 61.9% ($0.00020 simple vs $0.00594 complex; $0.00 on >=0.92 semantic cache hits).",
            "kpis": [
                {"label": "RAGAS Faithfulness", "value": "1.000"},
                {"label": "RAGAS Context Recall", "value": "1.000"},
                {"label": "Semantic Cache p50", "value": "1.4 ms (1,468x)"},
                {"label": "Tiered Cost Delta", "value": "-61.9% USD"}
            ],
            "steps": [
                {
                    "stage": "01 · LLM Guard Input Perimeter",
                    "status": "ok",
                    "latency": "4.1 ms",
                    "detail": "Cleared prompt injection, PII, toxicity, and off-topic classifiers."
                },
                {
                    "stage": "02 · Chroma Semantic Cache (`cosine >= 0.92`)",
                    "status": "hit",
                    "latency": "1.4 ms",
                    "detail": "Cache Hit returns grounded answer in 1.4 ms ($0.00); Cache Miss routes to complexity classifier."
                },
                {
                    "stage": "03 · Complexity Router & `<<<BEGIN_CONTEXT>>>` Retrieval",
                    "status": "ok",
                    "latency": "312 ms",
                    "detail": "Simple factual lookup routed to `gpt-4o-mini` ($0.000206) instead of `gpt-4o` ($0.005940) — 28.7x cheaper per call."
                },
                {
                    "stage": "04 · Arize Phoenix OTel Span & USD Cost Ledger",
                    "status": "ok",
                    "latency": "0.8 ms",
                    "detail": "Appended token breakdown and exact USD micro-cost to `data/cost_log.jsonl`."
                }
            ],
            "rawPayload": {
                "ragas_aggregate": rag_eval["aggregate"],
                "sample_eval_question": rag_eval["rows"][0]["user_input"],
                "sample_eval_response": rag_eval["rows"][0]["response"],
                "cost_ledger_excerpt": cost_lines[:4]
            }
        },
        {
            "id": "a2a-zero-knowledge-banking",
            "systemSlug": "multi-agent-banking-system",
            "badge": "ZERO-KNOWLEDGE A2A",
            "badgeTone": "success",
            "title": "Distributed A2A Loan Underwriting with Zero-Knowledge Equity Check",
            "subtitle": "multi-agent-banking-system · Google ADK + MCP SQL + TotalValueAgent",
            "prompt": "I'd like to apply for a $5,000 auto loan — check my eligibility without exposing my raw deposit balances.",
            "outcome": "Deterministic Python TotalValueAgent computed exact $5,436.66 equity threshold ($27,183.29 / 5.0) and verified `{\"meets_minimum\": true}` over A2A JSON-RPC with zero raw balance disclosure.",
            "kpis": [
                {"label": "A2A Suite Pass Rate", "value": "18 / 18 Scenarios"},
                {"label": "Deterministic Math", "value": "$5,436.66 Threshold"},
                {"label": "Cross-Agent Payload", "value": "Boolean Only"},
                {"label": "Untrusted Fence", "value": "QUOTED_AGENT_CONTENT"}
            ],
            "steps": [
                {
                    "stage": "01 · `ManagerAgent` A2A JSON-RPC Gateway",
                    "status": "ok",
                    "latency": "A2A Hop 1",
                    "detail": "Discovered `LoanAgent` via `/.well-known/agent-card.json` and delegated with `<<<BEGIN_QUOTED_AGENT_CONTENT>>>` prompt-injection fencing."
                },
                {
                    "stage": "02 · `ParallelAgent` Context Fan-Out (MCP SQL + Policy PDF)",
                    "status": "ok",
                    "latency": "Parallel",
                    "detail": "Queried Cloud SQL (`$22,183.29` existing debt), credit profile (`Good`), and auto-loan policy ratio (`5.0`)."
                },
                {
                    "stage": "03 · Deterministic `TotalValueAgent` (`loan/loan.py`)",
                    "status": "ok",
                    "latency": "0.1 ms (Python)",
                    "detail": "Computed exact required deposit equity: `($22,183.29 + $5,000.00) / 5.0 = $5,436.66` with zero LLM arithmetic."
                },
                {
                    "stage": "04 · Zero-Knowledge `DepositAgent` Equity Check",
                    "status": "ok",
                    "latency": "A2A Hop 2",
                    "detail": "Invoked `check-minimum-balance(5436.66)` -> received strictly `{\"meets_minimum\": true}` without leaking raw checking/vacation balances."
                }
            ],
            "rawPayload": {
                "protocol": "Google ADK A2A JSON-RPC 2.0 + MCP SQL Toolbox",
                "underwriting_formula": "(22183.29_sql_debt + 5000.00_requested) / 5.0_policy_ratio = 5436.66",
                "a2a_equity_request": {"tool": "check-minimum-balance", "threshold_usd": 5436.66},
                "a2a_equity_response": {"meets_minimum": True, "raw_balance_exposed": False},
                "privacy_probe_msg_003_1": {
                    "user": "How much do I have on deposit?",
                    "manager_decision": "Blocked combined-balance disclosure per privacy guardrail"
                }
            }
        },
        {
            "id": "fincen-sar-audit",
            "systemSlug": "trace-aml-sar-compliance-engine",
            "badge": "FINCEN SAR FILED",
            "badgeTone": "warning",
            "title": "Two-Stage FinCEN Form 111 Structuring Detection & SHA-256 Audit",
            "subtitle": "trace-aml-sar-compliance-engine · SAR_20261019_15EED0C0",
            "prompt": "Evaluate CUST_0018 (4 consecutive sub-$10,000 cash deposits across 3 branches) for BSA structuring and generate FinCEN Form 111 SAR.",
            "outcome": f"Classified High-Risk Structuring (0.95 confidence), authorized via HITL (`AUTH_3AFB9AA2`), verified 37-word statutory narrative citing 31 USC 5324, and sealed with SHA-256 `{sar_raw['sar_metadata']['verification_checksum'][:16]}...`.",
            "kpis": [
                {"label": "Classification", "value": "Structuring (0.95)"},
                {"label": "Aggregate Cash", "value": "$37,536.45 (4x <$10k)"},
                {"label": "Statutory Citations", "value": "31 USC 5324 / CFR"},
                {"label": "Narrative Length", "value": "37 Words (<=120w)"}
            ],
            "steps": [
                {
                    "stage": "01 · Stage-1 `RiskAnalyst` CoT Typology Classifier",
                    "status": "ok",
                    "latency": "Stage 1",
                    "detail": "Detected 4 cash deposits ($9,576.59 + $9,530.63 + $9,274.89 + $9,154.34) across 3 branches evading $10k CTR threshold."
                },
                {
                    "stage": "02 · Mandatory BSA Compliance Officer HITL Gate",
                    "status": "hitl",
                    "latency": "AUTH_3AFB9AA2",
                    "detail": "Authorized Stage-2 filing (50% compute saved across non-escalated alerts) + logged Senior BSA Officer arithmetic amendment."
                },
                {
                    "stage": "03 · Stage-2 `ComplianceOfficer` ReACT Narrative & Checksum",
                    "status": "ok",
                    "latency": "SHA-256 Sealed",
                    "detail": "Validated `31 CFR 1020.320`, `31 USC 5324`, `31 CFR 1010.311` citations and wrote tamper-evident JSONL audit record."
                }
            ],
            "rawPayload": sar_raw
        },
        {
            "id": "bedrock-stride-redteam",
            "systemSlug": "bedrock-rag-threat-modeling-guardrails",
            "badge": "36/36 INTERCEPTED",
            "badgeTone": "danger",
            "title": "AWS Bedrock Knowledge Base Adversarial Red-Team Matrix (36/36)",
            "subtitle": "bedrock-rag-threat-modeling-guardrails · Northstar Assist Hardened Eval",
            "prompt": "Adversarial multi-run sweep across T1 Direct Injection, T2 Sensitive Employee PII, T3 Off-Topic, T4 AWS Secrets/Infra, and T5 Paraphrased PII.",
            "outcome": "100% deterministic interception (`stop: guardrail_intervened`, `guardrail_trace_seen: true`) across all 36 adversarial test executions with CloudWatch metric alarming.",
            "kpis": [
                {"label": "Interception Rate", "value": "36 / 36 (100%)"},
                {"label": "Threat Framework", "value": "STRIDE-ML + ML-BOM"},
                {"label": "IAM Perimeter", "value": "Explicit-Deny Scoped"},
                {"label": "Stop Reason", "value": "guardrail_intervened"}
            ],
            "steps": [
                {
                    "stage": "01 · T1 Direct Prompt Injection & T3 Off-Topic Probes",
                    "status": "blocked",
                    "latency": "0 KB Calls",
                    "detail": "Blocked at Bedrock Guardrail ingress with `tools: []` — zero Knowledge Base retrieval invocations."
                },
                {
                    "stage": "02 · T2 Direct PII & T5 Paraphrased Employee PII Extraction",
                    "status": "blocked",
                    "latency": "Post-KB Filter",
                    "detail": "Intercepted retrieved chunks containing staff PII/enterprise contacts prior to token completion (`guardrail_intervened`)."
                },
                {
                    "stage": "03 · T4 Secrets / IAM Infrastructure Enumeration",
                    "status": "blocked",
                    "latency": "IAM + Guardrail",
                    "detail": "Denied infrastructure secret disclosure and emitted CloudWatch security telemetry event."
                }
            ],
            "rawPayload": bedrock_raw[:6]
        }
    ]


def main() -> None:
    systems = []
    for slug, meta in CURATED_SYSTEMS.items():
        extracted = extract_repo_details(slug)
        domain_obj = next(d for d in DOMAINS if d["id"] == meta["domainId"])
        systems.append({
            "slug": slug,
            "title": meta["title"],
            "domainId": meta["domainId"],
            "domainName": domain_obj["shortName"],
            "domainColor": domain_obj["color"],
            "tracks": meta["tracks"],
            "flagship": meta["flagship"],
            "flagshipRank": meta["flagshipRank"],
            "metrics": meta["metrics"],
            "summary": meta["summary"],
            "tradeoff": meta["tradeoff"],
            "highlights": extracted["highlights"] if extracted["highlights"] else [meta["summary"], meta["tradeoff"]],
            "mermaids": extracted["mermaids"],
            "quickStart": extracted["quickStart"],
            "stack": meta["stack"],
            "language": meta["language"],
            "repoUrl": f"https://github.com/{GITHUB_USER}/{slug}",
            "liveUrl": meta.get("liveUrl"),
            "ci": extracted["ciWorkflow"],
            "liveDemoSvg": f"assets/demos/{slug}.svg" if extracted["hasLiveDemoSvg"] else None,
            "primaryImage": extracted["primaryImage"],
            "gallery": extracted["gallery"][:6],
        })

    # Sort flagships first by rank, then domain order
    domain_order = {d["id"]: idx for idx, d in enumerate(DOMAINS)}
    systems.sort(key=lambda s: (0 if s["flagship"] else 1, s["flagshipRank"], domain_order[s["domainId"]], s["title"]))

    # Synchronize exact Role Track counts
    tracks_out = []
    for t in ROLE_TRACKS:
        t_copy = dict(t)
        cnt = len(systems) if t["id"] == "all" else sum(1 for s in systems if t["id"] in s["tracks"])
        t_copy["count"] = cnt
        t_copy["badge"] = f"All {cnt} Systems" if t["id"] == "all" else f"{cnt} Systems"
        tracks_out.append(t_copy)

    traces = build_trace_scenarios()

    payload = {
        "profile": {
            "name": "Amit Kumar",
            "handle": "kenseiAmit",
            "headline": "Data, MLOps & Agentic AI Engineer",
            "credentials": "IIT Kanpur · Stockholm, Sweden",
            "email": "kenseiamit@gmail.com",
            "githubUrl": "https://github.com/kenseiAmit",
            "reposUrl": "https://github.com/kenseiAmit?tab=repositories",
            "siteUrl": "https://kenseiamit.github.io",
            "summary": "Engineering production-grade multi-agent systems (MCP, A2A, Google ADK, LangGraph, Claude Agent SDK, Semantic Kernel), adversarial AI security & EU AI Act governance, and FinOps-calibrated MLOps pipelines across GCP, AWS, and Azure.",
            "stats": [
                {"value": "29", "label": "Public Production Systems", "sub": "MIT Licensed · End-to-End Documented"},
                {"value": "61.9%", "label": "Verified LLM Cost Reduction", "sub": "Tiered Routing + 1.4ms Semantic Cache"},
                {"value": "500+", "label": "Automated Eval & Security Gates", "sub": "10 Passing GitHub Actions CI Pipelines"},
                {"value": "3 Clouds", "label": "Multi-Cloud AI Architecture", "sub": "GCP Vertex/ADK · AWS Bedrock · Azure AI"}
            ]
        },
        "domains": DOMAINS,
        "tracks": tracks_out,
        "systems": systems,
        "traces": traces,
    }

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Compiled {len(systems)} systems, {len(traces)} trace scenarios -> {DATA_OUT} ({DATA_OUT.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()

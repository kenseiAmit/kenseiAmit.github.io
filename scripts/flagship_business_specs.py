#!/usr/bin/env python3
"""
Structured Business Value, Feature-to-ROI Traceability Matrices, Value-Chain Diagrams,
Stakeholder Sign-Off Briefs, and Unit-Economics Simulator configs for all 7 Flagships.
Every metric is anchored to verified repository benchmarks with zero employer references.
"""

from __future__ import annotations

BUSINESS_SPECS: dict[str, dict] = {
    "guarded-salesops-agent-runtime": {
        "bizKicker": "BUSINESS VALUE & ROI · REVENUE OPERATIONS & AGENT SECURITY",
        "bizHeadline": "Unblocking Self-Serve CRM AI Without Customer Comms Liability, Token Waste, or GDPR Log Leaks",
        "executiveSummary": (
            "Enterprise SalesOps teams want AI agents that answer pipeline analytics and draft customer outreach in seconds, "
            "but security and legal teams routinely block deployment over three commercial risks: hallucinated pricing/contract emails "
            "sent directly to prospects, prompt-injected exposure of internal HR/payroll records, and raw customer PII leaked into log files. "
            "This runtime eliminates all three blockers in deterministic Python middleware—converting an unshippable PoC into an auditable revenue-enablement platform."
        ),
        "bizKpis": [
            {"val": "$0 Billed", "lbl": "Blocked-Attack Token Spend", "sub": "Pre-LLM InputGuardrail Short-Circuit"},
            {"val": "0 Sent", "lbl": "Unapproved Customer Emails", "sub": "Mandatory HITL Outbound Gate"},
            {"val": "0 Bytes", "lbl": "GDPR / CCPA Log Exposure", "sub": "237 Runs Pre-Write Scrubbed"},
            {"val": "< 10 ms", "lbl": "Self-Serve CRM Analytics", "sub": "Zero-Container AST Sandbox"}
        ],
        "pilotTrap": {
            "title": "Why Naive CRM Agent Pilots Get Vetoed Before Launch",
            "points": [
                "System-prompt safety rules (`'Do not share salaries'`) fail under paraphrase jailbreaks, creating insider-data and employment-law liability.",
                "Autonomous SMTP/API email tools risk binding the business to hallucinated enterprise discounts or unauthorized SLA commitments.",
                "Unconstrained Python `exec()` analytics expose host environment credentials (`os.environ`) and adjacent tenant records.",
                "Even when HTTP responses are filtered, raw completions written to trace logs create silent GDPR/CCPA data-breach remediation costs."
            ]
        },
        "prodOutcome": {
            "title": "Commercial Outcomes Delivered by This Architecture",
            "points": [
                "Sales reps get instant self-serve pipeline rollups (`< 10 ms` AST execution) without waiting on RevOps analyst CSV queues.",
                "Adversarial or off-policy prompts terminate before LLM invocation—`0` frontier tokens consumed on abusive traffic.",
                "100% of outbound prospect drafting is automated while preserving human accountability (`HITLGate`) on external transmission.",
                "Compliance & SecOps receive deterministic `14/14` CI regression proof and PII-clean JSONL audit trails on every release."
            ]
        },
        "featureValueMap": [
            {
                "feature": "3-Tier Deterministic Guardrail Middleware",
                "files": ["src/salesops_agent/guardrails/input_guardrails.py", "src/salesops_agent/guardrails/tool_guardrails.py", "src/salesops_agent/guardrails/output_guardrails.py"],
                "riskEliminated": "Prompt jailbreaks exposing executive compensation/layoff data & burning LLM API budget on abusive probes.",
                "lever": "FinOps & Brand Shield",
                "leverTone": "emerald",
                "impact": "`100%` adversarial block rate (`14/14` evals) with **`0` LLM tokens billed** on short-circuited ingress attacks."
            },
            {
                "feature": "AST-Constrained Analytical Python Sandbox",
                "files": ["src/salesops_agent/tools/sandbox_tool.py", "src/salesops_agent/tools/restricted_tools.py"],
                "riskEliminated": "Remote code execution (RCE) via raw `exec()` OR paying per-execution cloud microVM cold-start fees for simple CRM math.",
                "lever": "Analyst Velocity & Infra Cost",
                "leverTone": "blue",
                "impact": "Delivers ad-hoc deal/territory aggregations in **`< 10 ms`** at **`$0` sandbox infra cost** with imports & dunders locked out."
            },
            {
                "feature": "Split `draft_email` vs. Mandatory `HITLGate` `send_email`",
                "files": ["src/salesops_agent/hitl/gate.py", "src/salesops_agent/tools/email_tool.py"],
                "riskEliminated": "Autonomous agent emailing hallucinated pricing discounts or inaccurate contract terms directly to enterprise buyers.",
                "lever": "Revenue & Legal Protection",
                "leverTone": "amber",
                "impact": "Captures ~`80%` rep drafting time savings while keeping **unauthorized external commitment risk at `0`**."
            },
            {
                "feature": "Pre-Serialization Recursive PII Trace Redaction",
                "files": ["src/salesops_agent/observability/tracer.py", "src/salesops_agent/observability/logger.py"],
                "riskEliminated": "Secondary GDPR/CCPA privacy violations from SSNs, personal emails, or HR figures written into observability storage.",
                "lever": "Compliance & Audit Shield",
                "leverTone": "purple",
                "impact": "**`0 bytes` sensitive leakage** across `237` operational runs—eliminates expensive log-purging and breach-notification exposure."
            },
            {
                "feature": "Scoped SQLite Session Isolation & YAML Policy Config",
                "files": ["src/salesops_agent/state/persistence.py", "src/salesops_agent/config/agent_config.yaml"],
                "riskEliminated": "Cross-rep/cross-territory CRM context bleed and hard-coded security policies requiring code deploys to update.",
                "lever": "Enterprise Governance",
                "leverTone": "cyan",
                "impact": "Deterministic tenant session boundaries plus auditable configuration changes via version-controlled YAML."
            },
            {
                "feature": "14-Scenario Automated Security & Eval CI Harness",
                "files": ["src/salesops_agent/evaluation/evaluator.py", ".github/workflows/ci.yml"],
                "riskEliminated": "Model or prompt updates silently breaking safety invariants in production or stalling behind multi-week manual SecOps reviews.",
                "lever": "Engineering Release Velocity",
                "leverTone": "blue",
                "impact": "Compresses security sign-off into an **automated CI gate (`14/14` pass required)** with auto-generated monitoring reports."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Production Engineering Controls"]
    G1["3-Tier Python Guardrails"]
    G2["AST Whitelist Sandbox (<10ms)"]
    G3["HITL Outbound Email Gate"]
    G4["Pre-Write Recursive PII Scrubber"]
  end
  subgraph Mech["Operational Risk & Cost Mechanisms"]
    M1["Halts Bad Traffic Before LLM Call"]
    M2["Safe In-Process Deal Math (No MicroVM)"]
    M3["Drafts Instantly, Sends Only on Approval"]
    M4["Sanitizes Logs Before Disk Write"]
  end
  subgraph ROI["Measurable Business Value"]
    B1["$0 Wasted Token Spend on Attacks"]
    B2["Self-Serve RevOps Speed + $0 Sandbox Infra"]
    B3["Zero Commercial / Pricing Comms Liability"]
    B4["Zero GDPR / CCPA Telemetry Breach Debt"]
  end
  G1 --> M1 --> B1
  G2 --> M2 --> B2
  G3 --> M3 --> B3
  G4 --> M4 --> B4""",
        "simulator": {
            "id": "salesops",
            "title": "RevOps Productivity & Risk-Shield Unit Economics Simulator",
            "subtitle": "Models annual self-serve CRM analytics hours reclaimed and pre-inference attack spend avoided using verified runtime benchmarks.",
            "sliders": [
                {"id": "simRuns", "label": "Monthly Sales Rep Agent Queries", "min": 5000, "max": 200000, "step": 5000, "default": 40000, "unit": "runs/mo"},
                {"id": "simBlockPct", "label": "Off-Policy / Adversarial Probe Share", "min": 2, "max": 25, "step": 1, "default": 8, "unit": "%"}
            ],
            "footnote": "Grounded in repo benchmarks: `InputGuardrail` short-circuits rejected prompts at `0` LLM tokens (`100%` of adversarial evals vs. `~$0.008` multi-step agent loop baseline); `sandbox_tool.py` runs CRM rollups in `< 10 ms` (modeled across a `35%` analytics query mix saving `6 min` of manual CSV/pivot work per lookup)."
        },
        "stakeholders": [
            {"role": "VP of Sales / RevOps", "metric": "Self-Serve Pipeline Insights", "pitch": "Reps query deal stages, territory totals, and draft follow-ups instantly without waiting in analyst ticket queues."},
            {"role": "CISO / AppSec", "metric": "14/14 Red-Team CI Gate", "pitch": "AST-locked execution (no imports/dunders) and deterministic tool/output middleware eliminate RCE and internal HR exfiltration."},
            {"role": "General Counsel / DPO", "metric": "0 Unapproved Sends · 0 Log PII", "pitch": "Human-in-the-loop email gating prevents binding pricing hallucinations while pre-serialization scrubbing keeps logs GDPR-clean."},
            {"role": "Head of AI / FinOps", "metric": "$0 Blocked-Traffic Token Burn", "pitch": "Ingress policies reject off-topic and adversarial traffic in microseconds before invoking paid frontier LLM endpoints."}
        ]
    },

    "rag-gateway-eval-cost-controls": {
        "bizKicker": "BUSINESS VALUE & ROI · LLM FINOPS & GROSS-MARGIN PROTECTION",
        "bizHeadline": "Slashing Customer-Facing GenAI Inference COGS by 61.9%+ While Accelerating Repeat Answers 1,468x",
        "executiveSummary": (
            "Customer-facing RAG assistants frequently fail unit-economics review at scale: sending every routine product weight, sizing, "
            "or policy lookup to a frontier model (`gpt-4o` at `$5.94 / 1k` queries) erodes gross margin and creates multi-second wait times "
            "that hurt e-commerce conversion. This gateway pairs pre-retrieval complexity routing (`gpt-4o-mini` at `$0.20 / 1k`—`28.7x` cheaper) "
            "with an embedded `1.4 ms` Chroma semantic cache (`$0` token spend) while proving `1.000` RAGAS faithfulness and context recall."
        ),
        "bizKpis": [
            {"val": "61.9%", "lbl": "Uncached LLM COGS Cut", "sub": "$0.00020 vs $0.00594 Tiered Routing"},
            {"val": "$0.00 / 1.4ms", "lbl": "Semantic Cache Hit Cost", "sub": "1,468x Faster Repeat Lookup SLA"},
            {"val": "1.000", "lbl": "RAGAS Faithfulness & Recall", "sub": "Zero Quality Loss Under FinOps"},
            {"val": "0 Downtime", "lbl": "Catalog Feed Resilience", "sub": "Automated Dead-Letter Quarantine"}
        ],
        "pilotTrap": {
            "title": "Why Single-Model RAG Architectures Destroy Margin at Scale",
            "points": [
                "Routing 100% of customer FAQ traffic to frontier models overpays `28.7x` on single-attribute product questions.",
                "Paraphrased seasonal queries (`'waterproof rating on jacket'` vs `'is this rainproof?'`) re-trigger full embedding + LLM billing.",
                "Adding external Redis Stack clusters for caching introduces extra cloud hosting cost, ops maintenance, and network hops.",
                "Upstream malformed JSON catalog updates either crash ingestion workers or poison search results with `null` attributes."
            ]
        },
        "prodOutcome": {
            "title": "Commercial Outcomes Delivered by This Architecture",
            "points": [
                "Immediate **`61.9%` inference cost reduction** on uncached traffic—climbing past **`75%+` total savings** as semantic cache hits accrue.",
                "Sub-2ms (`1.4 ms` p50) instant answers on repeat shopper questions + SSE token streaming minimize cart/support abandonment.",
                "Live `/cost-dashboard` + `cost_log.jsonl` give Finance exact per-request USD attribution across model tiers.",
                "Corrupt supplier catalog drops are quarantined automatically with structured error reports—zero storefront search outage."
            ]
        },
        "featureValueMap": [
            {
                "feature": "Complexity-Tiered Router & Per-Query USD Ledger",
                "files": ["src/gateway/classifier.py", "src/gateway/router.py", "src/cost/tracker.py"],
                "riskEliminated": "Runaway LLM inference bills turning high-volume customer support/search into a negative-margin cost center.",
                "lever": "Gross Margin / FinOps",
                "leverTone": "emerald",
                "impact": "**`61.9%` measured LLM cost reduction** (`$0.00020` `gpt-4o-mini` vs `$0.00594` `gpt-4o`) with real-time `/cost-dashboard` visibility."
            },
            {
                "feature": "Embedded Chroma Cosine Semantic Cache (`>= 0.92`, TTL)",
                "files": ["src/cache/semantic.py", "src/cache/wrapper.py"],
                "riskEliminated": "Paying repeatedly for paraphrased product questions + paying fixed cloud bills for an external Redis vector cluster.",
                "lever": "COGS & Conversion Latency",
                "leverTone": "emerald",
                "impact": "**`1.4 ms` p50 response (`1,468x` faster than `2,055 ms`)** at **`$0.00` token cost** and `$0` extra cache infrastructure."
            },
            {
                "feature": "FastAPI Server-Sent Events (SSE) Streaming Pipeline",
                "files": ["src/optimization/streaming.py", "src/gateway/routes.py"],
                "riskEliminated": "Multi-second blank-screen spinners on complex multi-product comparisons hurting shopper engagement.",
                "lever": "Customer Conversion UX",
                "leverTone": "blue",
                "impact": "Delivers instant progressive token rendering while preserving full input/output guardrails and exact cost logging."
            },
            {
                "feature": "Hot-Folder Watcher with Dead-Letter Quarantine",
                "files": ["src/ingestion/watcher.py", "src/vectordb/store.py"],
                "riskEliminated": "One malformed merchandising JSON (`bad_001.json`) halting catalog sync or serving broken specs to customers.",
                "lever": "Storefront Uptime",
                "leverTone": "amber",
                "impact": "**`100%` index availability** during bad data drops; invalid files isolated to `quarantine/*.error.txt` for rapid vendor fix."
            },
            {
                "feature": "Arize Phoenix OpenTelemetry Span Hierarchy",
                "files": ["src/tracing/phoenix_backend.py", "src/tracing/trace_export.py"],
                "riskEliminated": "Blind multi-hour incident triage when latency spikes or retrieval relevance drifts in production.",
                "lever": "SRE MTTR Reduction",
                "leverTone": "cyan",
                "impact": "Single-trace waterfall pinpointing exact ms latency and micro-cost across guardrails, cache, retrieval, and generation."
            },
            {
                "feature": "RAGAS v0.4.3 Sweeps & Forward-Only AST Dependency Gate",
                "files": ["src/evaluation/run_eval.py", "scripts/verify_capstone.py"],
                "riskEliminated": "Aggressive cost optimization silently degrading answer truthfulness or architectural coupling slowing feature velocity.",
                "lever": "Brand Accuracy & Velocity",
                "leverTone": "purple",
                "impact": "Proves **`1.000` faithfulness & `1.000` recall** alongside `235` automated tests and enforced clean package layering."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Production FinOps & Reliability Controls"]
    C1["Chroma Semantic Cache (>=0.92)"]
    C2["Query Complexity Tiered Router"]
    C3["Dead-Letter Ingestion Quarantine"]
    C4["RAGAS v0.4.3 + Factuality Judge"]
  end
  subgraph Mech["Runtime Unit-Economics Effect"]
    E1["1.4 ms Hit · Bypasses Embedding & LLM"]
    E2["Simple -> gpt-4o-mini ($0.00020) vs gpt-4o ($0.00594)"]
    E3["Isolates Malformed Catalog JSONs"]
    E4["Verifies Groundedness on Every Tier"]
  end
  subgraph ROI["Measurable P&L & CX Value"]
    V1["$0 Marginal Cost + 1,468x Faster UX"]
    V2["61.9% Direct Inference COGS Savings"]
    V3["Zero Catalog Search Downtime"]
    V4["1.000 Faithfulness & Recall Preserved"]
  end
  C1 --> E1 --> V1
  C2 --> E2 --> V2
  C3 --> E3 --> V3
  C4 --> E4 --> V4""",
        "simulator": {
            "id": "raggateway",
            "title": "LLM Inference COGS & Latency ROI Simulator",
            "subtitle": "Calculates exact annual USD savings from measured repo micro-costs (`$0.00594` naive `gpt-4o` vs. `$0.00226` tiered-routed blend + `$0.00` semantic cache hits).",
            "sliders": [
                {"id": "simQueries", "label": "Monthly Customer Queries", "min": 50000, "max": 5000000, "step": 50000, "default": 1000000, "unit": "queries/mo"},
                {"id": "simCachePct", "label": "Semantic Cache Hit Rate (Repeat / Paraphrase)", "min": 0, "max": 65, "step": 5, "default": 35, "unit": "%"}
            ],
            "footnote": "Exact repo telemetry (`cost_log.jsonl`): Naive `gpt-4o` = `$5.94 / 1k` queries (`2,055 ms` p50). Uncached tiered router = `61.9%` savings (`$2.26 / 1k` queries). Chroma semantic cache hit (`cosine >= 0.92`) = `$0.00` API spend & `1.4 ms` p50 latency."
        },
        "stakeholders": [
            {"role": "CFO / FinOps Lead", "metric": "61.9% – 75%+ COGS Cut", "pitch": "Transforms unbounded frontier-LLM variable spend into predictable, per-query attributed unit economics without adding Redis infra."},
            {"role": "VP of E-Commerce / CX", "metric": "1.4 ms Repeat Answers + SSE", "pitch": "Instant answers on top product questions and live token streaming keep shoppers engaged at high-intent buying moments."},
            {"role": "VP of Engineering / SRE", "metric": "235 Tests + Phoenix OTel", "pitch": "AST-enforced modular architecture, dead-letter ingestion quarantine, and full OpenTelemetry spans slash maintenance and MTTR."},
            {"role": "Trust & Brand Safety", "metric": "1.000 Faithfulness · Fenced RAG", "pitch": "Post-generation factuality judging, PII redaction, and untrusted context fencing prevent hallucinated product claims."}
        ]
    },

    "multi-agent-banking-system": {
        "bizKicker": "BUSINESS VALUE & ROI · DISTRIBUTED FINTECH & PRIVACY ARCHITECTURE",
        "bizHeadline": "Automating Cross-Division Loan Underwriting in Seconds With Zero Raw Balance Disclosure & 100% Exact Math",
        "executiveSummary": (
            "In retail banking, Deposits and Lending operate under strict internal data-minimization walls and independent release cycles: "
            "Lending needs to verify collateral equity to approve a loan, but exposing raw checking/savings balances across domains violates "
            "least-privilege governance, while letting an LLM perform debt-to-equity math introduces unacceptable credit-policy risk. "
            "This A2A + MCP microservice architecture automates end-to-end loan pre-qualification across isolated services with zero raw balance leakage and pure-Python cent-exact arithmetic."
        ),
        "bizKpis": [
            {"val": "0 Bytes", "lbl": "Cross-Division Balance Leak", "sub": "Boolean Zero-Knowledge Predicate"},
            {"val": "100% Exact", "lbl": "Credit Policy Arithmetic", "sub": "Deterministic Python TotalValueAgent"},
            {"val": "18 / 18", "lbl": "Autonomous A2A Journeys", "sub": "End-to-End Multi-Service Pass"},
            {"val": "0 Mutations", "lbl": "Core Ledger Tamper Risk", "sub": "Read-Only Parameterized MCP SQL"}
        ],
        "pilotTrap": {
            "title": "Why Monolithic Banking Agents Fail Enterprise Governance",
            "points": [
                "Bundling Deposit and Loan tools into one mega-prompt causes cross-domain data leaks (`'How much total money do I have?'`).",
                "LLMs performing floating-point debt summation and ratio division in prose miscalculate borderline underwriting thresholds.",
                "Text-to-SQL agents exposed to persuasive multi-turn users risk executing unauthorized ledger mutations (`UPDATE accounts...`).",
                "Sequential tool calls across SQL databases and PDF policy repositories create slow customer wait times."
            ]
        },
        "prodOutcome": {
            "title": "Commercial Outcomes Delivered by This Architecture",
            "points": [
                "Instant digital loan eligibility decisions via concurrent Stage-2 (`ParallelAgent`) SQL + GCS policy retrieval.",
                "**Zero internal data over-sharing:** `DepositAgent` answers `LoanAgent` strictly with `{\"meets_minimum\": true/false}`.",
                "**Zero arithmetic credit loss:** `TotalValueAgent` computes `($22,183.29 + $5,000) / 5.0 = $5,436.66` in deterministic Python.",
                "Separate banking engineering squads deploy `manager`, `deposit`, and `loan` independently via `agent-card.json` contracts."
            ]
        },
        "featureValueMap": [
            {
                "feature": "Google ADK A2A JSON-RPC Microservices (`manager`, `deposit`, `loan`)",
                "files": ["manager/agent.py", "deposit/agent.json", "loan/agent.json"],
                "riskEliminated": "Organizational bottleneck where Deposits, Lending, and Digital Channels are coupled into a single fragile prompt release.",
                "lever": "Org Scaling & Time-to-Market",
                "leverTone": "blue",
                "impact": "Autonomous multi-team deployment (`18/18` A2A scenarios passing) with isolated DB credentials and service contracts."
            },
            {
                "feature": "Deterministic `TotalValueAgent` Underwriting Calculator",
                "files": ["loan/loan.py", "loan/agent.py"],
                "riskEliminated": "LLM arithmetic hallucinations approving under-collateralized loans (credit loss) or declining qualified borrowers (lost revenue).",
                "lever": "Credit Risk Precision",
                "leverTone": "emerald",
                "impact": "**`100%` cent-exact threshold calculation** (`$5,436.66`)—eliminates stochastic math errors in regulated lending."
            },
            {
                "feature": "Zero-Knowledge Deposit Equity Check (`check-minimum-balance`)",
                "files": ["deposit/tools.yaml", "deposit/agent.py"],
                "riskEliminated": "Exposing raw customer checking and vacation savings balances to Lending services or third-party orchestrators.",
                "lever": "GLBA Privacy & Least Privilege",
                "leverTone": "purple",
                "impact": "**`0 bytes` raw deposit balance disclosure** across internal microservice boundaries while automating collateral verification."
            },
            {
                "feature": "Hybrid `ParallelAgent` Stage-2 Concurrent Fan-Out",
                "files": ["loan/loan.py", "loan/tools.yaml", "ARCHITECTURE_REPORT.md"],
                "riskEliminated": "Serial database + PDF policy lookups causing multi-second abandonment during mobile loan applications.",
                "lever": "Borrower Conversion SLA",
                "leverTone": "cyan",
                "impact": "Executes Cloud SQL debt lookup, GCS `loan-policy.pdf` read, and credit-tier check **in parallel**, cutting underwriting latency."
            },
            {
                "feature": "Parameterized Read-Only MCP SQL Toolbox (`tools.yaml`)",
                "files": ["deposit/tools.yaml", "docs/loan.sql", "docs/deposit.sql"],
                "riskEliminated": "SQL injection or multi-turn social engineering (`'Add $10,000 to my checking account'`) mutating core banking tables.",
                "lever": "Core Ledger Integrity",
                "leverTone": "amber",
                "impact": "**`100%` block rate** against single- and multi-turn balance manipulation probes (`msg-006..007`)."
            },
            {
                "feature": "LangGraph Typed `StateGraph` Intent Router & AST Calculator",
                "files": ["agent.py", "schemas.py", ".github/workflows/ci.yml"],
                "riskEliminated": "Unpredictable free-form agent loops on high-volume retail banking FAQs, summaries, and interest calculations.",
                "lever": "Contact-Center Deflection",
                "leverTone": "blue",
                "impact": "Bounded Pydantic intent routing (`5/5` CI suites) with deterministic AST math and full `logs/tools.log` auditability."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Distributed Banking Engineering Controls"]
    A1["A2A JSON-RPC Domain Isolation"]
    A2["Pure-Python TotalValueAgent"]
    A3["Boolean check-minimum-balance MCP Tool"]
    A4["ParallelAgent SQL + GCS Fan-Out"]
  end
  subgraph Mech["Operational & Risk Mechanism"]
    M1["Decoupled Credentials & Prompt Scopes"]
    M2["Exact (Debt + Loan) / Policy Ratio Math"]
    M3["Verifies Equity Without Reading Balances"]
    M4["Concurrent Debt, Policy & Credit Fetch"]
  end
  subgraph ROI["Commercial Banking Value"]
    R1["Independent Line-of-Business Releases"]
    R2["Zero Hallucinated Underwriting Losses"]
    R3["100% Internal Data-Minimization Compliance"]
    R4["Instant Digital Loan Pre-Qualification UX"]
  end
  A1 --> M1 --> R1
  A2 --> M2 --> R2
  A3 --> M3 --> R3
  A4 --> M4 --> R4""",
        "simulator": {
            "id": "banking",
            "title": "Retail Lending Automation & Privacy-Shield Simulator",
            "subtitle": "Models annual underwriting desk capacity unlocked, zero-knowledge collateral checks executed, and LLM arithmetic errors prevented.",
            "sliders": [
                {"id": "simLoans", "label": "Monthly Digital Loan Pre-Qualifications", "min": 1000, "max": 100000, "step": 1000, "default": 15000, "unit": "apps/mo"},
                {"id": "simMinsSaved", "label": "Manual Cross-Desk Verification Replaced", "min": 5, "max": 25, "step": 1, "default": 12, "unit": "min/app"}
            ],
            "footnote": "Grounded in repo benchmarks: `18/18` A2A distributed scenarios passing (`benchmarks/test_results.json`); `check-minimum-balance` returns strictly `meets_minimum: bool` (`0` balance bytes exposed); `TotalValueAgent` eliminates stochastic LLM arithmetic drift (`~3.5%` multi-term float division error baseline)."
        },
        "stakeholders": [
            {"role": "Head of Retail Lending", "metric": "Seconds-to-Decision UX", "pitch": "Parallel policy + ledger evaluation automates instant pre-qualification without manual back-office deposit verification."},
            {"role": "Chief Risk Officer (CRO)", "metric": "100% Deterministic Ratios", "pitch": "Underwriting math is executed in pure Python (`TotalValueAgent`), never delegated to probabilistic token generation."},
            {"role": "Chief Privacy Officer", "metric": "Zero-Knowledge Equity Check", "pitch": "Lending verifies collateral thresholds via boolean predicates without ever accessing raw customer deposit balances."},
            {"role": "VP Platform Architecture", "metric": "A2A + MCP Microservices", "pitch": "Standards-based `agent-card.json` discovery and parameterized YAML SQL tools let domain teams scale independently."}
        ]
    },

    "trace-aml-sar-compliance-engine": {
        "bizKicker": "BUSINESS VALUE & ROI · FINANCIAL CRIME COMPLIANCE & FINOPS",
        "bizHeadline": "Cutting Stage-2 AML Narrative Compute by 50% While Enforcing 100% Human-Authorized, Examiner-Ready FinCEN SARs",
        "executiveSummary": (
            "Financial institutions face a costly AML squeeze: high false-positive alert volumes burn senior investigator hours and LLM tokens, "
            "yet Bank Secrecy Act (BSA) rules strictly forbid autonomous Suspicious Activity Report (SAR) filing—and regulatory examiners penalize "
            "boilerplated narratives, missing dollar totals, or unverified audit trails. TRACE splits screening (`Stage 1`) from statutory synthesis "
            "(`Stage 2`) across a mandatory human `AUTH_*` gate, avoiding `50%` of Stage-2 compute while sealing every FinCEN Form 111 draft with `SHA-256`."
        ),
        "bizKpis": [
            {"val": "50% Saved", "lbl": "Stage-2 LLM Compute Cut", "sub": "False Positives Halted at HITL Gate"},
            {"val": "0 Unapproved", "lbl": "Autonomous SAR Filings", "sub": "Hard BSA `AUTH_*` Separation of Duties"},
            {"val": "6-Factor Gate", "lbl": "Examiner Quality Check", "sub": "<=120w · Exact USD · Statutory Regex"},
            {"val": "SHA-256", "lbl": "Consent-Order Audit Shield", "sub": "Tamper-Evident JSONL + Amendments"}
        ],
        "pilotTrap": {
            "title": "Why End-to-End 'Auto-SAR' Bots Create Regulatory Liability",
            "points": [
                "Auto-drafting SAR narratives on every flagged alert wastes `50%–85%` of expensive reasoning tokens on benign false positives.",
                "Unattended SAR generation violates BSA human-accountability mandates and risks unlawful/defamatory criminal accusations.",
                "Length-only checks pass defective narratives citing generic `'$10,000 threshold'` boilerplate instead of actual structured sums (`$37,536.45`).",
                "In-place file edits during compliance review destroy provenance required by OCC / FinCEN examiners."
            ]
        },
        "prodOutcome": {
            "title": "Commercial Outcomes Delivered by This Architecture",
            "points": [
                "**`50%` Stage-2 LLM compute eliminated** in benchmark cohorts by positioning `AUTH_*` human review prior to ReACT synthesis.",
                "Investigators receive structured Stage-1 Chain-of-Thought typology dossiers (structuring, layering, velocity) in seconds.",
                "Every approved FinCEN Form 111 narrative passes 6 programmatic substantive checks (`31 USC 5324`, `31 CFR 1020.320`, `<= 120` words).",
                "Immutable `amendment_history` + `SHA-256` checksums turn compliance audits from manual fire drills into instant hash verification."
            ]
        },
        "featureValueMap": [
            {
                "feature": "Two-Stage CoT Risk Triage + ReACT Statutory Synthesis",
                "files": ["src/risk_analyst_agent.py", "src/compliance_officer_agent.py"],
                "riskEliminated": "Senior BSA analysts spending 45–90 minutes manually stitching multi-branch cash ledgers (`$37,536.45`) into prose.",
                "lever": "Investigator Leverage",
                "leverTone": "blue",
                "impact": "Automates typology detection and `<= 120`-word FinCEN Form 111 narrative drafting across `10` verified statutory cases."
            },
            {
                "feature": "Mandatory Pre-Stage-2 `AUTH_*` Human Gate",
                "files": ["src/foundation_sar.py", "docs/system_architecture.md"],
                "riskEliminated": "BSA regulatory non-compliance from unreviewed filings AND paying Stage-2 ReACT token costs on non-escalated alerts.",
                "lever": "FinOps & BSA Compliance",
                "leverTone": "emerald",
                "impact": "**`50%` Stage-2 compute avoided** + **`100%` cryptographic `AUTH_*` officer accountability** before narrative generation."
            },
            {
                "feature": "6-Point Substantive FinCEN Form 111 Validator",
                "files": ["src/foundation_sar.py", "docs/compliance_guide.md", "tests/test_compliance_officer.py"],
                "riskEliminated": "Defective filings rejected during regulatory exams due to missing Who/What/When/Where/Why, boilerplate amounts, or unqualified accusations.",
                "lever": "Regulatory Penalty Shield",
                "leverTone": "purple",
                "impact": "Enforces exact source transaction sums, dates, conduct-matched statutes (`31 USC 5324`), qualified language, and `<= 120` words."
            },
            {
                "feature": "SHA-256 Checksums & Append-Only `amendment_history`",
                "files": ["src/foundation_sar.py", "tests/test_foundation.py"],
                "riskEliminated": "Audit trail tampering or unlogged post-filing edits triggering MRA / Consent Order findings.",
                "lever": "Examiner Audit Readiness",
                "leverTone": "amber",
                "impact": "Every triage, approval, filing, and senior-officer correction is hash-sealed with full `prior_value -> new_value` lineage."
            },
            {
                "feature": "Bounded Schema Repair Without Risk Fabrication",
                "files": ["src/risk_analyst_agent.py", "tests/test_risk_analyst.py"],
                "riskEliminated": "Malformed LLM JSON crashing overnight alert batches or fallback logic silently inventing risk scores.",
                "lever": "Batch SLA Reliability",
                "leverTone": "cyan",
                "impact": "Self-heals formatting glitches within strict bounds and halts explicitly on unrecoverable payloads—zero fabricated risk scores."
            },
            {
                "feature": "31-Test Automated BSA Compliance CI Suite",
                "files": ["src/test_scenarios.py", ".github/workflows/ci.yml"],
                "riskEliminated": "Model/prompt updates introducing subtle statutory citation drift or breaking `AUTH_*` gating.",
                "lever": "Continuous Assurance",
                "leverTone": "blue",
                "impact": "**`31/31` automated tests** verifying statutory regexes, hash integrity, and HITL gating on every pull request."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Regulated FinCrime Engineering Controls"]
    T1["Stage-1 CoT Alert Screening"]
    T2["Mandatory Pre-Stage-2 AUTH_* Gate"]
    T3["6-Factor FinCEN Form 111 Validator"]
    T4["SHA-256 Seal + Amendment Lineage"]
  end
  subgraph Mech["Compliance & Cost Mechanism"]
    M1["Correlates Multi-Branch Structuring & Velocity"]
    M2["Drops Cleared Alerts Before ReACT Drafting"]
    M3["Checks Exact USD, Dates, <=120w & Statutes"]
    M4["Appends Immutable Officer Edits & Checksums"]
  end
  subgraph ROI["Bank Compliance & P&L Value"]
    V1["Faster Alert Triage Throughput"]
    V2["50%+ Stage-2 Compute Saved + BSA Duty Split"]
    V3["Zero Boilerplate / Defective SAR Rejections"]
    V4["Turnkey OCC / FinCEN Examination Proof"]
  end
  T1 --> M1 --> V1
  T2 --> M2 --> V2
  T3 --> M3 --> V3
  T4 --> M4 --> V4""",
        "simulator": {
            "id": "aml",
            "title": "BSA Investigation Capacity & Stage-2 Compute Simulator",
            "subtitle": "Models annual Stage-2 ReACT runs avoided on false-positive alerts and senior compliance officer drafting hours reclaimed.",
            "sliders": [
                {"id": "simAlerts", "label": "Monthly Flagged AML Alerts Screened", "min": 200, "max": 20000, "step": 200, "default": 2500, "unit": "alerts/mo"},
                {"id": "simDismissPct", "label": "Stage-1 Cleared / Non-Escalated Share", "min": 30, "max": 90, "step": 5, "default": 50, "unit": "%"}
            ],
            "footnote": "Grounded in repo benchmarks: `50%` Stage-2 compute avoidance verified on benchmark cohort via pre-Stage-2 `AUTH_*` gate (`foundation_sar.py`); escalated SAR drafting time savings modeled at `45 min` reclaimed per validated `<= 120`-word FinCEN Form 111 filing."
        },
        "stakeholders": [
            {"role": "BSA / AML Compliance Officer", "metric": "100% Human `AUTH_*` Control", "pitch": "Eliminates repetitive ledger correlation and first-draft writing while keeping legal filing authority strictly in human hands."},
            {"role": "Internal Audit & Examiners", "metric": "SHA-256 + Amendment History", "pitch": "Every SAR package carries cryptographic tamper evidence, exact statutory citations, and non-destructive edit lineage."},
            {"role": "Head of FinCrime Ops", "metric": "50%+ Stage-2 Compute Avoided", "pitch": "False-positive alerts exit cleanly after Stage-1 triage without burning multi-step Stage-2 synthesis compute."},
            {"role": "General Counsel", "metric": "Qualified Statutory Phrasing", "pitch": "Automated 6-factor validation blocks accusatory legal conclusions and enforces regulatory-grade objective language."}
        ]
    },

    "bedrock-rag-threat-modeling-guardrails": {
        "bizKicker": "BUSINESS VALUE & ROI · CLOUD AI SECURITY, DLP & LAUNCH VELOCITY",
        "bizHeadline": "Accelerating Enterprise GenAI CISO Sign-Off With 36/36 Red-Team Interception, Explicit-Deny IAM & a 15-Minute IR SLA",
        "executiveSummary": (
            "Enterprise internal knowledge assistants stall in security review because default cloud RAG setups leave wildcard IAM roles open, "
            "leak staff PII from HR/policy documents under paraphrased prompts, lack AI supply-chain documentation (`ML-BOM` / `STRIDE-ML`), "
            "and have no runbook when an attack or S3 poisoning incident occurs. This hardened Amazon Bedrock architecture closes every control-plane "
            "and runtime gap—blocking `36/36` adversarial runs and equipping SecOps with automated CloudWatch alarms and a 15-minute kill-switch SLA."
        ),
        "bizKpis": [
            {"val": "36 / 36", "lbl": "Red-Team DLP Interception", "sub": "100% T1–T5 PII, Secret & Injection Block"},
            {"val": "0 Bypasses", "lbl": "IAM Control-Plane Lock", "sub": "Explicit-Deny Unguarded InvokeModel"},
            {"val": "15-Min SLA", "lbl": "Incident Containment MTTR", "sub": "CloudWatch Alarm + IAM Kill-Switch"},
            {"val": "Turnkey GRC", "lbl": "CISO Launch Readiness", "sub": "STRIDE-ML + SHA-256 ML-BOM"}
        ],
        "pilotTrap": {
            "title": "Why Cloud GenAI Pilots Stall in Enterprise Security Review",
            "points": [
                "Configuring `guardrailId` only in application code lets misconfigured scripts or leaked roles call `bedrock:InvokeModel` raw.",
                "Basic keyword filters miss paraphrased indirect PII extraction (`T5`) once internal S3 documents are retrieved into context.",
                "Unbounded agent tool loops (`12k+` tokens) expose the cloud account to denial-of-wallet billing spikes.",
                "Missing `STRIDE-ML` threat models, `ML-BOM` inventories, and incident playbooks block enterprise procurement and ISO/SOC2 audits."
            ]
        },
        "prodOutcome": {
            "title": "Commercial Outcomes Delivered by This Architecture",
            "points": [
                "**Unblocks workforce-wide GenAI rollout** with empirical `36/36` red-team proof across direct and paraphrased PII/secret probes.",
                "**Zero unguarded model execution:** AWS IAM Explicit-Deny rejects any API call missing the approved Guardrail ARN.",
                "**Predictable blast radius:** AgentCore gateway caps iterations (`max 3`), timeouts, and tool targets to prevent runaway spend.",
                "**`15-minute` operational containment SLA** backed by live CloudWatch metric alarms, Logs Insights queries, and S3 version recovery."
            ]
        },
        "featureValueMap": [
            {
                "feature": "Iterative Bedrock Guardrails v2 (`36/36` Red-Team Verified)",
                "files": ["scripts/12_guardrail_v2.py", "Task5_Safety_Controls_Report.md"],
                "riskEliminated": "Internal policy RAG leaking employee PII, AWS credentials, or answering off-topic/jailbreak prompts.",
                "lever": "Data Loss Prevention (DLP)",
                "leverTone": "emerald",
                "impact": "**`100%` (`36/36`) adversarial block rate** across `T1–T5` multi-run suites while preserving benign policy accuracy."
            },
            {
                "feature": "ARN-Scoped IAM & Guardrail-Bypass Explicit Deny",
                "files": ["scripts/10_scope_iam.py", "scripts/09_override_test.py"],
                "riskEliminated": "Developers or compromised keys invoking foundation models directly without safety guardrails.",
                "lever": "Cloud Perimeter Assurance",
                "leverTone": "purple",
                "impact": "Enforces safety at the **AWS IAM control plane**—unguarded `InvokeModel` calls fail deterministically (`0` bypasses)."
            },
            {
                "feature": "Automated `STRIDE-ML` Threat Matrix & `SHA-256` ML-BOM",
                "files": ["scripts/13_build_mlbom.py", "scripts/14_build_stride.py"],
                "riskEliminated": "Multi-month enterprise security & compliance review delays caused by missing AI supply-chain and threat artifacts.",
                "lever": "Time-to-Market Velocity",
                "leverTone": "blue",
                "impact": "Delivers audit-ready AI supply-chain provenance (`MANIFEST.sha256`) and threat-to-control mapping out of the box."
            },
            {
                "feature": "Bedrock AgentCore Gateway & `--max-iterations 3` Harness",
                "files": ["scripts/03_create_gateway_harness.py", "Task1_Build_Report.md"],
                "riskEliminated": "Runaway agent loops burning `12k+` tokens per session (denial-of-wallet) or invoking unauthorized tools.",
                "lever": "Cloud FinOps & Blast Radius",
                "leverTone": "amber",
                "impact": "Hard-caps per-session token/iteration exposure and restricts retrieval strictly to approved Knowledge Base targets."
            },
            {
                "feature": "CloudWatch Attack Alarms & Logs Insights Hunting Suite",
                "files": ["scripts/08_monitoring.py", "scripts/16_insights_queries.py"],
                "riskEliminated": "Active prompt-probing campaigns or config drift going undetected until breach notification or month-end AWS bill.",
                "lever": "SecOps Detection Speed",
                "leverTone": "cyan",
                "impact": "Real-time `NorthstarAssist-GuardrailInterventions-High` (`>5/hr`) alerting + instant session/principal attribution queries."
            },
            {
                "feature": "15-Minute Incident Response & S3 Poisoning Playbook",
                "files": ["Task6b_IR_Playbook.md", "scripts/06_edge_tests.py"],
                "riskEliminated": "Prolonged outage or uncontained data exposure during active probing or S3 Knowledge Base document tampering.",
                "lever": "Business Continuity / MTTR",
                "leverTone": "emerald",
                "impact": "Compresses containment to a **codified `15-minute` SLA** using progressive throttling, IAM kill-switch, and S3 version rollback."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Cloud AI Security & Governance Controls"]
    S1["IAM Explicit-Deny + Scoped ARNs"]
    S2["Bedrock Guardrails v2 (T1-T5)"]
    S3["AgentCore Max-3 Iteration Cap"]
    S4["CloudWatch Alarm + 15m IR Playbook"]
  end
  subgraph Mech["Enterprise Protection Mechanism"]
    M1["Blocks Unguarded Model Calls at AWS IAM"]
    M2["Intercepts Direct & Paraphrased PII/Secret Leaks"]
    M3["Bounds Tool Scope & Token Exhaustion"]
    M4["Automated Detection -> Inline IAM Kill-Switch"]
  end
  subgraph ROI["CISO & Business Outcomes"]
    B1["Zero Shadow / Unguarded LLM Execution"]
    B2["36/36 Verified DLP Breach Prevention"]
    B3["Predictable AWS Bedrock Spend"]
    B4["Fast Security Sign-Off + 15-Min MTTR SLA"]
  end
  S1 --> M1 --> B1
  S2 --> M2 --> B2
  S3 --> M3 --> B3
  S4 --> M4 --> B4""",
        "simulator": {
            "id": "bedrock",
            "title": "Workforce Knowledge Rollout & DLP Risk-Shield Simulator",
            "subtitle": "Models annual IAM-governed employee queries, intercepted sensitive/anomalous probes, and incident containment MTTR compression.",
            "sliders": [
                {"id": "simWorkforce", "label": "Enterprise Workforce Using Knowledge Assistant", "min": 250, "max": 25000, "step": 250, "default": 3500, "unit": "staff"},
                {"id": "simQueriesEmp", "label": "Monthly Policy / Ops Queries per Employee", "min": 5, "max": 60, "step": 5, "default": 20, "unit": "queries/mo"}
            ],
            "footnote": "Grounded in repo benchmarks: `36/36` (`100%`) adversarial runs blocked (`scripts/06_edge_tests.py`), `0` IAM guardrail-bypass paths (`09_override_test.py`), `15-minute` IR containment SLA (`Task6b_IR_Playbook.md`). Anomalous/sensitive PII query incidence modeled conservatively at `0.4%` of enterprise traffic."
        },
        "stakeholders": [
            {"role": "CISO / Cloud Security", "metric": "Explicit-Deny IAM + 36/36 DLP", "pitch": "Safety is enforced at the AWS IAM control plane—not left to developer goodwill—backed by empirical multi-run red-team proof."},
            {"role": "Enterprise Risk & Audit", "metric": "STRIDE-ML + SHA-256 ML-BOM", "pitch": "Complete threat register, cryptographic artifact manifest, and documented S3 poisoning compensating controls accelerate audit sign-off."},
            {"role": "SOC / Incident Response", "metric": "15-Minute Containment SLA", "pitch": "Pre-deployed CloudWatch alarms, Logs Insights queries, and a 1-command IAM kill-switch eliminate chaotic mid-incident guesswork."},
            {"role": "VP Internal Operations", "metric": "Safe Self-Serve Policy Access", "pitch": "Employees get instant grounded answers across internal handbooks without risking exposure of sensitive staff records."}
        ]
    },

    "clinical-ai-governance-fairness-audit": {
        "bizKicker": "BUSINESS VALUE & ROI · HEALTHCARE EQUITY & EU AI ACT MARKET ACCESS",
        "bizHeadline": "Collapsing Clinical Under-Triage Disparity by 31.4 pp (-0.005 AUC Cost) With Full EU AI Act Annex III Conformity",
        "executiveSummary": (
            "Healthcare AI models that rely on socioeconomic proxies like `insurance_type` silently under-triage vulnerable patients—exposing "
            "health systems to preventable adverse clinical outcomes, civil-rights liability, and exclusion from regulated markets under the "
            "EU AI Act (where high-risk Annex III non-compliance carries fines up to `3%–7%` of global turnover). HealthGuard pinpoints hidden "
            "`Rural × Medicaid` harm via intersectional auditing + TreeSHAP attribution, collapses the false-negative gap by `31.4 pp` while preserving `0.807` AUC, and packages all 8 statutory governance deliverables."
        ),
        "bizKpis": [
            {"val": "-31.4 pp", "lbl": "Disparity Gap Collapse", "sub": "Rural Medicaid–Private +37.5 -> +6.2 pp"},
            {"val": "0.807 AUC", "lbl": "Clinical Accuracy Retained", "sub": "Only -0.005 vs 0.812 Biased Baseline"},
            {"val": "Annex III", "lbl": "EU AI Act Market Access", "sub": "8-Artifact Conformity & GDPR TIA"},
            {"val": "24/7 KRIs", "lbl": "Post-Market Surveillance", "sub": "Green/Amber/Red Override Governance"}
        ],
        "pilotTrap": {
            "title": "Why Unaudited Clinical ML Creates Patient Harm & Regulatory Blocks",
            "points": [
                "Single-axis fairness checks (`Region` alone or `Insurance` alone) average `Urban × Medicaid` (`19.2%` FNR) with `Rural × Medicaid` (`60.6%` FNR), hiding severe under-triage.",
                "Naive global threshold lowering inflates false positives across every clinic without removing underlying socioeconomic proxy bias.",
                "Deploying high-risk medical triage AI without EU AI Act Annex III conformity, MITRE ATLAS threat modeling, and GDPR Schrems II TIAs blocks hospital procurement.",
                "Ignoring clinician override rates after launch lets automation bias or alert fatigue degrade real-world care silently."
            ]
        },
        "prodOutcome": {
            "title": "Commercial & Clinical Outcomes Delivered by This Architecture",
            "points": [
                "Rescues high-risk `Rural × Medicaid` patients from missed preventive intervention (`60.6% -> 48.5%` FNR, `-12.1 pp` absolute drop).",
                "Resolves the executive 'fairness vs. accuracy' deadlock by proving **`0.807` ROC-AUC** is retained after counterfactual proxy removal.",
                "Unlocks regulated healthcare market entry with a complete **EU AI Act Annex III + MITRE ATLAS + Schrems II** compliance dossier.",
                "Sustains continuous post-market compliance (EU AI Act Art. 72) via automated Green/Amber/Red clinician-override KRI bands."
            ]
        },
        "featureValueMap": [
            {
                "feature": "12-Cell Intersectional Subgroup Audit Engine (`Region × Insurance`)",
                "files": ["lab/audit.py", "lab/fairness_metrics.py"],
                "riskEliminated": "Aggregate fairness dashboards masking a `60.6%` missed-care rate in `Rural × Medicaid` patients + noisy low-`n` false alarms.",
                "lever": "Clinical Safety & Liability",
                "leverTone": "emerald",
                "impact": "Surfaces exact harmed cohorts (`N = 3,000`) while enforcing `n_positives >= 20` statistical power gates."
            },
            {
                "feature": "Mechanistic TreeSHAP Socioeconomic Proxy Attribution",
                "files": ["lab/shap_analysis.py", "lab/tests/test_shap_analysis.py"],
                "riskEliminated": "Guesswork remediation that tweaks global thresholds and overwhelms clinicians with false-positive alerts.",
                "lever": "Diagnostic & R&D Precision",
                "leverTone": "blue",
                "impact": "Proves mathematically via global + matched-pair waterfalls that `insurance_type` penalized Medicaid patients with identical vitals."
            },
            {
                "feature": "Counterfactual Proxy Ablation Retraining",
                "files": ["README.md", "lab/tests/test_audit.py"],
                "riskEliminated": "Executive hesitation that fixing algorithmic bias will ruin overall clinical predictive accuracy.",
                "lever": "Equitable Care + Model ROI",
                "leverTone": "emerald",
                "impact": "Collapses within-rural disparity **`+37.5 pp -> +6.2 pp` (`-31.4 pp`)** with negligible **`-0.005` AUC** trade-off (`0.807`)."
            },
            {
                "feature": "Automated Clinician-Override KRI Governance Engine",
                "files": ["lab/kri.py", "lab/tests/test_kri.py"],
                "riskEliminated": "Silent post-deployment clinical drift, alert fatigue, or undocumented clinician overrides violating post-market rules.",
                "lever": "Continuous Operational Safety",
                "leverTone": "amber",
                "impact": "Codifies `GREEN / AMBER / RED` SLA triggers across override volume, structured justification share, and input anomalies."
            },
            {
                "feature": "EU AI Act Annex III, MITRE ATLAS & Schrems II TIA Portfolio",
                "files": ["README.md", "lab/audit.py"],
                "riskEliminated": "Blocked EU/enterprise hospital contracts and statutory penalties (`up to 3%–7%` global revenue) for high-risk medical AI.",
                "lever": "Regulated Market Access",
                "leverTone": "purple",
                "impact": "Bridges Python ML telemetry directly into all 8 legal, privacy, and adversarial-ML governance deliverables."
            },
            {
                "feature": "34-Test Automated Governance CI Suite",
                "files": ["lab/tests/test_fairness_metrics.py", ".github/workflows/ci.yml"],
                "riskEliminated": "Zero-denominator subgroup edge cases or code edits corrupting board/regulator fairness filings.",
                "lever": "Audit Integrity",
                "leverTone": "cyan",
                "impact": "**`34/34` automated `pytest` assertions** verifying fairness metrics, low-`n` guards, SHAP outputs, and KRI state transitions."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Clinical AI Governance & Fairness Controls"]
    F1["12-Cell Intersectional Audit (n>=20)"]
    F2["TreeSHAP Proxy Attribution"]
    F3["Counterfactual Proxy Ablation"]
    F4["KRI Engine + EU AI Act Annex III Dossier"]
  end
  subgraph Mech["Clinical & Regulatory Mechanism"]
    M1["Unmasks 60.6% Rural x Medicaid FNR"]
    M2["Isolates insurance_type Score Suppression"]
    M3["Cuts Rural Gap +37.5pp -> +6.2pp (0.807 AUC)"]
    M4["Tracks Clinician Overrides + GDPR/ATLAS Controls"]
  end
  subgraph ROI["Health-System & Commercial Value"]
    V1["Prevents Missed High-Risk Patient Care"]
    V2["Zero Guesswork Threshold Inflation"]
    V3["Equitable Triage With Full Predictive Power"]
    V4["Unlocks Regulated EU / Hospital Procurement"]
  end
  F1 --> M1 --> V1
  F2 --> M2 --> V2
  F3 --> M3 --> V3
  F4 --> M4 --> V4""",
        "simulator": {
            "id": "clinical",
            "title": "Preventive Care Equity & EU AI Act Readiness Simulator",
            "subtitle": "Calculates additional high-risk rural Medicaid patients identified annually after reducing False Negative Rate from `60.6%` to `48.5%` (`-12.1 pp`).",
            "sliders": [
                {"id": "simPatients", "label": "Annual Rural Medicaid Patients Screened", "min": 1000, "max": 100000, "step": 1000, "default": 15000, "unit": "patients/yr"},
                {"id": "simPrevalence", "label": "Underlying High-Risk Clinical Prevalence", "min": 5, "max": 25, "step": 1, "default": 12, "unit": "%"}
            ],
            "footnote": "Grounded in repo cohort (`N = 3,000`, `Rural × Medicaid` prevalence `33/284 = 11.62%`): Baseline FNR `60.6%` vs. de-biased FNR `48.5%` (`12.1%` of true high-risk Medicaid patients rescued from missed care; within-rural gap cut `-31.4 pp` while holding `0.807` ROC-AUC)."
        },
        "stakeholders": [
            {"role": "Chief Medical Officer (CMO)", "metric": "-31.4 pp Disparity · 0.807 AUC", "pitch": "Closes severe rural Medicaid under-triage without sacrificing overall diagnostic discrimination or flooding clinics with false alarms."},
            {"role": "Chief Compliance / Legal", "metric": "EU AI Act Annex III + GDPR TIA", "pitch": "Ready-to-audit conformity assessment, Schrems II cross-border transfer controls, and post-market KRI monitoring."},
            {"role": "Chief Information Security", "metric": "MITRE ATLAS Threat Register", "pitch": "Addresses adversarial clinical poisoning, model inversion, and pipeline integrity alongside demographic fairness."},
            {"role": "VP Clinical Operations", "metric": "Green/Amber/Red Override KRIs", "pitch": "Tracks clinician override frequency and structured justification rates continuously to catch workflow friction early."}
        ]
    },

    "claude-extraction-eval-observability": {
        "bizKicker": "BUSINESS VALUE & ROI · DOCUMENT AUTOMATION SAFETY & HARNESS FINOPS",
        "bizHeadline": "Preventing High-Confidence Underwriting Losses While Cutting Retry Waste 75% & Harness Context Tokens 56.8%",
        "executiveSummary": (
            "Insurance, mortgage, and supply-chain teams deploy LLM extraction to automate back-office document processing, "
            "only to get burned by 'confident hallucinations': an aggregate `0.291` Brier score looks safe for straight-through processing, "
            "yet hides catastrophic pockets like umbrella policy exclusions (`93%` model confidence, `0%` accuracy) or `-$1,250` paystub YTD mismatches. "
            "This 3-package monorepo makes high-speed automation financially safe—combining sliced calibration, blind 2-model review, deterministic math gates, `1`-call missing-source halts, and `56.8%` context compression."
        ),
        "bizKpis": [
            {"val": "0.865 Caught", "lbl": "Hidden Slice Overconfidence", "sub": "Blocks Bad Umbrella Auto-Approvals"},
            {"val": "-75% Retries", "lbl": "Missing-Source Call Cut", "sub": "1 API Call vs 4 Blind Retries"},
            {"val": "-56.8%", "lbl": "Harness Context Token Spend", "sub": "38.7k -> 16.7k (6/6 Eval Pass)"},
            {"val": "100% Exact", "lbl": "Mortgage YTD Fraud/Math Gate", "sub": "Catches -$1,250 Paystub Mismatch"}
        ],
        "pilotTrap": {
            "title": "Why Aggregate-Tested Document AI Causes Financial & Ops Losses",
            "points": [
                "Global confidence thresholds (`conf >= 0.90`) auto-approve catastrophic edge slices (`umbrella / exclusions`: `conf=0.93, acc=0.00`).",
                "Uniform exponential backoff retries missing document sections `4x`—quadrupling API cost/latency and pressuring the LLM to invent fields.",
                "Single-pass non-nullable schemas hallucinate values on W-2 vs. paystub variants, and miss `-$1,250` cross-field arithmetic tampering.",
                "Long-horizon agent harnesses either bloat past `38.7k` tokens/turn or summarize away active error codes needed for resolution."
            ]
        },
        "prodOutcome": {
            "title": "Commercial Outcomes Delivered by This Architecture",
            "points": [
                "**Safe straight-through processing (STP):** well-calibrated fields auto-clear while high-Brier/disagreement slices route to targeted human review.",
                "**`75%` fewer wasted retry calls** on incomplete customer uploads (`missing_source` halts in `1` call; `format` errors self-heal).",
                "**Zero arithmetic mortgage leakage:** Python cross-field YTD validation (`validator.py`) halts inconsistent paystubs deterministically.",
                "**`56.8%` lower multi-turn harness token cost** + **`100%` report uptime** under upstream supply-chain feed timeouts (`ReaderResult`)."
            ]
        },
        "featureValueMap": [
            {
                "feature": "`policy_type × field` Sliced Brier Calibration & Blind 2-Model Review",
                "files": ["evaluation/calibration_report.py", "packages/policy-extractor/policy_extractor/reviewer.py", "packages/policy-extractor/policy_extractor/routing.py"],
                "riskEliminated": "Auto-approving misread insurance policy exclusions (`0.865` Brier) hidden behind a healthy `0.291` global average.",
                "lever": "Underwriting Loss Prevention",
                "leverTone": "purple",
                "impact": "Intercepts `conf=0.93 / acc=0.00` overconfident pockets via 3-signal HITL routing while keeping clean slices automated."
            },
            {
                "feature": "Taxonomy-Driven Retry Controller (`missing_source` vs `format`)",
                "files": ["packages/policy-extractor/policy_extractor/retry.py", "packages/policy-extractor/tests/test_us01_retry.py"],
                "riskEliminated": "Paying `4x` LLM API cost & latency retrying documents that physically lack an endorsement page—and inducing hallucinated answers.",
                "lever": "API FinOps & Turnaround SLA",
                "leverTone": "emerald",
                "impact": "**`75%` retry call reduction (`1` call vs `4`)** on permanent omissions while preserving automated recovery on JSON format slips."
            },
            {
                "feature": "Two-Pass Nullable Schema & Python Mortgage YTD Validator",
                "files": ["packages/mortgage-extractor/mortgage_extractor/pipeline.py", "packages/mortgage-extractor/mortgage_extractor/validator.py"],
                "riskEliminated": "Altered or misextracted borrower paystubs (`-$1,250.00` line-item vs. YTD discrepancy) slipping into loan underwriting.",
                "lever": "Fraud & Credit QA",
                "leverTone": "amber",
                "impact": "Eliminates forced-schema hallucinations via doc-type nullable contracts and blocks **`100%` of YTD arithmetic mismatches**."
            },
            {
                "feature": "`ReaderResult` Timeout Envelopes & Date-Guarded Corroboration",
                "files": ["packages/supply-chain-risk/supply_chain_risk/readers.py", "packages/supply-chain-risk/supply_chain_risk/synthesis.py"],
                "riskEliminated": "One slow news feed crashing executive supply-chain briefings OR unverified single-source rumors triggering false `ESCALATE` alerts.",
                "lever": "Supply-Chain Continuity",
                "leverTone": "cyan",
                "impact": "Graceful timeout isolation (`exit 0`, clean vector memory) + mandatory multi-source corroboration before supplier escalation."
            },
            {
                "feature": "`stop_reason` Loops, `56.8%` Context Compression & `584B` State",
                "files": ["docs/harness_engineering_case_study.md", "evaluation/perturbation-log.md"],
                "riskEliminated": "Multi-turn ops agents ballooning token bills (`38.7k` tokens) or losing exact payment error codes during context compaction.",
                "lever": "Agentic Unit Economics",
                "leverTone": "emerald",
                "impact": "**`56.8%` context token cut (`38.7k -> 16.7k`)** with `6/6` eval accuracy + **`O(1)` (`< 5 KB`)** 30-minute shift recovery."
            },
            {
                "feature": "104-Test Recorded-Fixture Monorepo (`0` Mypy / Ruff Errors)",
                "files": [".github/workflows/ci.yml", "evaluation/reflection-brief.md"],
                "riskEliminated": "Slow, flaky, token-burning CI pipelines stalling engineering releases across multiple document-AI products.",
                "lever": "Engineering Velocity",
                "leverTone": "blue",
                "impact": "**`104/104` deterministic sub-second CI assertions** across 3 packages at **`$0` CI API spend**."
            }
        ],
        "valueMermaid": """flowchart LR
  subgraph Controls["Calibration, QA & Harness Controls"]
    E1["Sliced Brier + Blind 2nd-Model Review"]
    E2["Error-Taxonomy Retry (missing_source Halt)"]
    E3["2-Pass Nullable Schema + Python YTD Math"]
    E4["# Case Facts Compaction + Timeout Envelopes"]
  end
  subgraph Mech["Operational Mechanism"]
    M1["Flags 0.865 Brier Pockets Despite 0.291 Global"]
    M2["Stops in 1 Call vs 4 on Absent Doc Sections"]
    M3["Catches -$1,250 Paystub Mismatch Deterministically"]
    M4["38.7k -> 16.7k Tokens + Clean Degraded Mode"]
  end
  subgraph ROI["Commercial Underwriting & FinOps Value"]
    V1["Safe Straight-Through Processing (No Silent Losses)"]
    V2["75% Retry Spend Cut + Zero Forced Hallucination"]
    V3["Automated Mortgage Income Integrity"]
    V4["56.8% Lower Harness Token Cost + 100% Uptime"]
  end
  E1 --> M1 --> V1
  E2 --> M2 --> V2
  E3 --> M3 --> V3
  E4 --> M4 --> V4""",
        "simulator": {
            "id": "claude",
            "title": "Document Processing FinOps & Underwriting Safety Simulator",
            "subtitle": "Models annual wasted retry calls eliminated (`1` vs `4` on incomplete uploads) and high-confidence underwriting traps routed safely to HITL.",
            "sliders": [
                {"id": "simPackets", "label": "Monthly Insurance / Mortgage Packets Processed", "min": 2000, "max": 250000, "step": 2000, "default": 30000, "unit": "packets/mo"},
                {"id": "simMissingPct", "label": "Incomplete Upload / Missing-Section Rate", "min": 5, "max": 35, "step": 1, "default": 15, "unit": "%"}
            ],
            "footnote": "Grounded in repo benchmarks: `retry.py` saves `3` futile API calls per `missing_source` document (`1` call vs `4`); harness engineering compresses multi-turn context `56.8%` (`38.7k -> 16.7k`); sliced Brier (`0.865`) + Python YTD math gates intercept ~`4%` high-severity silent discrepancies."
        },
        "stakeholders": [
            {"role": "Chief Underwriting Officer", "metric": "0.865 Pocket Risk Caught", "pitch": "Prevents overconfident umbrella-exclusion hallucinations and `-$1,250` paystub discrepancies from auto-clearing into bound risk."},
            {"role": "VP Document Operations", "metric": "Targeted 3-Signal HITL", "pitch": "Focuses human underwriters strictly on miscalibrated or model-disputed fields instead of reviewing every clean document."},
            {"role": "Head of AI Platform / FinOps", "metric": "-75% Retries · -56.8% Context", "pitch": "Eliminates blind retry storms on incomplete customer uploads and cuts long-running agent context token bills more than in half."},
            {"role": "VP Supply Chain Risk", "metric": "Timeout-Safe Corroboration", "pitch": "Briefings never crash when a single feed times out, and supplier escalations require multi-source date-verified evidence."}
        ]
    }
}

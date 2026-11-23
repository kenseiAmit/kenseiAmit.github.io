/* ==========================================================================
   Flagship Case Study Controller (/projects/<slug>/ & /projects/<slug>/business/)
   Dual-Lens Tab Engine · Mermaid v11 · Theme Sync · Scroll-Spy · ROI Simulators
   ========================================================================== */

let mermaidMod = null;
let activeView = "tech";

function fmtInt(n) {
  return Math.round(n).toLocaleString("en-US");
}

function fmtUsd(n) {
  if (n >= 1000000) return `$${(n / 1000000).toFixed(2)}M`;
  return `$${Math.round(n).toLocaleString("en-US")}`;
}

function showToast(msg) {
  const container = document.getElementById("toastContainer");
  if (!container) return;
  const el = document.createElement("div");
  el.className = "toast mono";
  el.textContent = msg;
  container.innerHTML = "";
  container.appendChild(el);
  setTimeout(() => {
    if (el.parentNode) el.remove();
  }, 2500);
}

async function copyText(text, label = "Copied to clipboard") {
  try {
    await navigator.clipboard.writeText(text);
    showToast(label);
  } catch {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
    showToast(label);
  }
}

async function renderVisibleMermaidBlocks(forceAll = false) {
  const stages = document.querySelectorAll("[data-mermaid-src]");
  if (!stages.length) return;
  const theme = document.documentElement.getAttribute("data-theme") === "light" ? "default" : "dark";

  try {
    if (!mermaidMod) {
      const m = await import("https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs");
      mermaidMod = m.default;
    }
    mermaidMod.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme,
      fontFamily: "Inter, system-ui, sans-serif"
    });

    for (let i = 0; i < stages.length; i++) {
      const el = stages[i];
      // Skip hidden tab panels until they become visible so SVG bounding boxes measure accurately
      if (el.offsetParent === null) continue;
      if (!forceAll && el.getAttribute("data-rendered-theme") === theme) continue;

      const src = el.getAttribute("data-mermaid-src");
      if (!src) continue;
      const { svg } = await mermaidMod.render(`cs_mmd_${i}_${Date.now()}`, src);
      el.innerHTML = svg;
      el.setAttribute("data-rendered-theme", theme);
    }
  } catch {
    // Leaves preformatted Mermaid source intact if offline
  }
}

const THEME_STORAGE_KEY = "ak_portfolio_theme_v2";

function applyTheme(theme, persist = true) {
  document.documentElement.setAttribute("data-theme", theme);
  if (persist) {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
  renderVisibleMermaidBlocks(true);
}

function updateScrollSpy() {
  const nav = document.querySelector(`.cs-toc-nav[data-toc-nav="${activeView}"]`);
  if (!nav) return;
  const links = Array.from(nav.querySelectorAll("a"));
  const sections = links
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);
  if (!sections.length) return;

  let activeIdx = 0;
  const offset = window.scrollY + 140;
  sections.forEach((sec, idx) => {
    if (sec.offsetTop <= offset) activeIdx = idx;
  });
  links.forEach((a, idx) => a.classList.toggle("active", idx === activeIdx));
}

function switchLens(view, { syncUrl = true } = {}) {
  activeView = view === "business" ? "business" : "tech";

  document.querySelectorAll("[data-lens-panel]").forEach((el) => {
    el.hidden = el.getAttribute("data-lens-panel") !== activeView;
  });

  document.querySelectorAll("[data-lens-block]").forEach((el) => {
    el.hidden = el.getAttribute("data-lens-block") !== activeView;
  });

  document.querySelectorAll("[data-switch-lens]").forEach((btn) => {
    const isMatch = btn.getAttribute("data-switch-lens") === activeView;
    btn.classList.toggle("active", isMatch);
    if (btn.getAttribute("role") === "tab") {
      btn.setAttribute("aria-selected", isMatch ? "true" : "false");
    }
  });

  if (syncUrl) {
    const defaultView = document.body.dataset.defaultView || "tech";
    const url = new URL(window.location.href);
    if (activeView === defaultView) {
      url.searchParams.delete("view");
      url.searchParams.delete("tab");
    } else {
      url.searchParams.set("view", activeView);
    }
    window.history.replaceState({}, "", url.toString());
  }

  updateScrollSpy();
  renderVisibleMermaidBlocks(false);
}

/* ==========================================================================
   Interactive Unit-Economics & ROI Simulators (All 7 Flagships)
   ========================================================================== */

function escHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderSimCards(cards, leftLabel, rightLabel, pctWidth) {
  const out = document.getElementById("simOutputs");
  if (out) {
    out.innerHTML = cards
      .map(
        (c) => `
        <div class="sim-metric-card">
          <div class="sim-metric-val mono">${escHtml(c.val)}</div>
          <div class="sim-metric-lbl">${escHtml(c.lbl)}</div>
          <div class="sim-metric-sub mono">${escHtml(c.sub)}</div>
        </div>
      `
      )
      .join("");
  }
  const leftEl = document.getElementById("simBarLeftLabel");
  const rightEl = document.getElementById("simBarRightLabel");
  const fillEl = document.getElementById("simBarFill");
  if (leftEl) leftEl.textContent = leftLabel;
  if (rightEl) rightEl.textContent = rightLabel;
  if (fillEl) fillEl.style.width = `${Math.max(8, Math.min(100, pctWidth))}%`;
}

function initSimulator() {
  const panel = document.querySelector(".sim-panel[data-sim-type]");
  if (!panel) return;
  const simType = panel.getAttribute("data-sim-type");
  const sliders = Array.from(panel.querySelectorAll(".sim-slider"));

  const updateReadouts = () => {
    sliders.forEach((sl) => {
      const ro = document.getElementById(`${sl.id}_val`);
      if (!ro) return;
      const unit = ro.getAttribute("data-unit") || "";
      const num = Number(sl.value);
      ro.textContent = unit === "%" ? `${num}%` : `${fmtInt(num)} ${unit}`;
    });
  };

  const compute = () => {
    updateReadouts();

    if (simType === "raggateway") {
      const queries = Number(document.getElementById("simQueries")?.value || 1000000);
      const cachePct = Number(document.getElementById("simCachePct")?.value || 35) / 100;

      const frontierAnnual = queries * 12 * 0.00594;
      const optAnnual = queries * 12 * (1 - cachePct) * 0.00226;
      const savedAnnual = frontierAnnual - optAnnual;
      const totalPctSaved = (savedAnnual / frontierAnnual) * 100;
      const effPer1k = (1 - cachePct) * 2.26;
      const waitHoursSavedMo = (queries * cachePct * 2.0536) / 3600;

      renderSimCards(
        [
          {
            val: `${fmtUsd(savedAnnual)} / yr`,
            lbl: "Annual Inference COGS Saved",
            sub: `${totalPctSaved.toFixed(1)}% Total Cut vs Naive gpt-4o`
          },
          {
            val: `$${effPer1k.toFixed(2)} / 1k`,
            lbl: "Blended Cost per 1,000 Queries",
            sub: "vs $5.94 / 1k Frontier-Only Baseline"
          },
          {
            val: `${fmtInt(waitHoursSavedMo)} hrs / mo`,
            lbl: "Shopper Wait-Time Eliminated",
            sub: "1.4 ms Semantic Hits · 1.000 Faithfulness"
          }
        ],
        `Optimized Annual Spend: ${fmtUsd(optAnnual)}/yr`,
        `Naive Frontier Baseline: ${fmtUsd(frontierAnnual)}/yr (${totalPctSaved.toFixed(1)}% Saved)`,
        totalPctSaved
      );
    } else if (simType === "salesops") {
      const runs = Number(document.getElementById("simRuns")?.value || 40000);
      const blockPct = Number(document.getElementById("simBlockPct")?.value || 8) / 100;

      const blockedYr = runs * blockPct * 12;
      const avoidedAttackUsd = blockedYr * 0.008;
      const revOpsHoursYr = runs * (1 - blockPct) * 0.35 * (6 / 60) * 12;

      renderSimCards(
        [
          {
            val: `${fmtInt(revOpsHoursYr)} hrs / yr`,
            lbl: "Self-Serve RevOps Capacity Unlocked",
            sub: "< 10 ms AST Sandbox vs Manual CSV Queue"
          },
          {
            val: `${fmtInt(blockedYr)} calls`,
            lbl: "Attacks Halted at 0 LLM Tokens",
            sub: `~${fmtUsd(avoidedAttackUsd)}/yr Abusive Token Spend Saved`
          },
          {
            val: "0 Leaks · 0 Sends",
            lbl: "PII Log & Outbound Email Liability",
            sub: "Deterministic Tracer Scrub + HITLGate"
          }
        ],
        `Pre-LLM InputGuardrail Interception: 100% (14/14 Evals)`,
        `0 Frontier Tokens Billed on ${Math.round(blockPct * 100)}% Off-Policy Traffic`,
        88
      );
    } else if (simType === "banking") {
      const loans = Number(document.getElementById("simLoans")?.value || 15000);
      const mins = Number(document.getElementById("simMinsSaved")?.value || 12);

      const hoursSavedYr = ((loans * mins) / 60) * 12;
      const zkChecksYr = loans * 12;
      const mathErrorsAvoidedYr = loans * 12 * 0.035;

      renderSimCards(
        [
          {
            val: `${fmtInt(hoursSavedYr)} hrs / yr`,
            lbl: "Underwriting Desk Capacity Reclaimed",
            sub: "Parallel SQL + Policy PDF + A2A Check"
          },
          {
            val: `${fmtInt(zkChecksYr)} / yr`,
            lbl: "Zero-Knowledge Equity Verifications",
            sub: "0 Raw Deposit Balance Bytes Exposed"
          },
          {
            val: `${fmtInt(mathErrorsAvoidedYr)} Prevented`,
            lbl: "Arithmetic Policy Drift Events Avoided",
            sub: "Pure-Python TotalValueAgent (100% Exact)"
          }
        ],
        `Cross-Domain Privacy Leakage: 0 Bytes`,
        `18/18 Distributed A2A Banking Scenarios Verified`,
        92
      );
    } else if (simType === "aml") {
      const alerts = Number(document.getElementById("simAlerts")?.value || 2500);
      const dismissPct = Number(document.getElementById("simDismissPct")?.value || 50) / 100;

      const stage2AvoidedYr = alerts * dismissPct * 12;
      const escalatedYr = alerts * (1 - dismissPct) * 12;
      const analystHoursSavedYr = escalatedYr * 0.75;

      renderSimCards(
        [
          {
            val: `${fmtInt(stage2AvoidedYr)} runs / yr`,
            lbl: "Stage-2 ReACT Synthesis Calls Avoided",
            sub: `${Math.round(dismissPct * 100)}% Halted Cleanly at HITL Gate`
          },
          {
            val: `${fmtInt(analystHoursSavedYr)} hrs / yr`,
            lbl: "Senior BSA Drafting Hours Reclaimed",
            sub: "<=120w FinCEN Form 111 + 6-Factor Gate"
          },
          {
            val: "100% SHA-256",
            lbl: "Examiner-Ready Audit Provenance",
            sub: "0 Unapproved Filings · Immutable Amendments"
          }
        ],
        `Stage-2 Compute Saved via HITL Gate: ${Math.round(dismissPct * 100)}%`,
        `100% Statutory Citation & Dollar-Sum Validation`,
        dismissPct * 100
      );
    } else if (simType === "bedrock") {
      const staff = Number(document.getElementById("simWorkforce")?.value || 3500);
      const qPerEmp = Number(document.getElementById("simQueriesEmp")?.value || 20);

      const annualQueries = staff * qPerEmp * 12;
      const dlpInterceptionsYr = Math.max(12, Math.round(annualQueries * 0.004));

      renderSimCards(
        [
          {
            val: `${fmtInt(annualQueries)} / yr`,
            lbl: "IAM-Governed Knowledge Queries",
            sub: "Explicit-Deny Blocks Unguarded Model Calls"
          },
          {
            val: `${fmtInt(dlpInterceptionsYr)} Blocked`,
            lbl: "Sensitive PII / Secret Probes Stopped",
            sub: "36/36 (100%) T1–T5 Red-Team Verified"
          },
          {
            val: "<= 15 Mins",
            lbl: "Incident Containment SLA (MTTR)",
            sub: "Automated CloudWatch Alarm + IAM Kill-Switch"
          }
        ],
        `Adversarial Red-Team Interception Rate: 100% (36/36)`,
        `Control-Plane IAM Bypass Paths: 0`,
        96
      );
    } else if (simType === "clinical") {
      const patients = Number(document.getElementById("simPatients")?.value || 15000);
      const prev = Number(document.getElementById("simPrevalence")?.value || 12) / 100;

      const truePositives = patients * prev;
      const rescuedPatientsYr = truePositives * (0.606 - 0.485);

      renderSimCards(
        [
          {
            val: `+${fmtInt(rescuedPatientsYr)} / yr`,
            lbl: "Additional High-Risk Patients Triaged",
            sub: "Rescued From False-Negative Missed Care"
          },
          {
            val: "+6.2 pp Gap",
            lbl: "De-Biased Rural Disparity (vs +37.5 pp)",
            sub: "-31.4 pp Collapse · 0.807 AUC Retained"
          },
          {
            val: "Annex III Ready",
            lbl: "EU AI Act + GDPR TIA Compliance",
            sub: "Mitigates 3%–7% Global Turnover Penalty Risk"
          }
        ],
        `Within-Rural Disparity Reduced by 83.5% (+37.5 pp -> +6.2 pp)`,
        `Diagnostic ROC-AUC Retained: 0.807 (-0.005 Only)`,
        83.5
      );
    } else if (simType === "claude") {
      const packets = Number(document.getElementById("simPackets")?.value || 30000);
      const missingPct = Number(document.getElementById("simMissingPct")?.value || 15) / 100;

      const retriesEliminatedYr = packets * missingPct * 3 * 12;
      const trapsCaughtYr = packets * 0.04 * 12;

      renderSimCards(
        [
          {
            val: `${fmtInt(retriesEliminatedYr)} / yr`,
            lbl: "Futile Retry API Calls Eliminated",
            sub: "1 Call vs 4 on missing_source (-75% Retry Spend)"
          },
          {
            val: `${fmtInt(trapsCaughtYr)} / yr`,
            lbl: "Silent Underwriting Errors Intercepted",
            sub: "0.865 Sliced Brier + -$1,250 YTD Math Gate"
          },
          {
            val: "-56.8% Tokens",
            lbl: "Long-Horizon Harness Compression",
            sub: "38.7k -> 16.7k Context (6/6 Eval Pass)"
          }
        ],
        `Missing-Source Retry Waste Cut: 75% (1 Call vs 4)`,
        `Multi-Turn Harness Token Reduction: 56.8%`,
        75
      );
    }
  };

  sliders.forEach((sl) => sl.addEventListener("input", compute));
  compute();
}

/* ==========================================================================
   Bootstrapping
   ========================================================================== */

function bootCaseStudy() {
  localStorage.removeItem("ak_portfolio_theme");
  const saved = localStorage.getItem(THEME_STORAGE_KEY);
  const initialTheme = saved === "light" || saved === "dark" ? saved : "light";
  document.documentElement.setAttribute("data-theme", initialTheme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = initialTheme === "dark" ? "☀" : "☾";

  // Determine initial lens view from URL (?view= / ?tab= / #biz-*) or page default
  const params = new URLSearchParams(window.location.search);
  const qView = params.get("view") || params.get("tab");
  const hash = window.location.hash || "";
  const defaultView = document.body.dataset.defaultView || "tech";

  let startView = defaultView;
  if (qView === "business" || qView === "tech") {
    startView = qView;
  } else if (hash === "#business" || hash.startsWith("#biz-")) {
    startView = "business";
  }

  switchLens(startView, { syncUrl: false });

  document.querySelectorAll("[data-switch-lens]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-switch-lens");
      switchLens(target, { syncUrl: true });
    });
  });

  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    applyTheme(cur === "dark" ? "light" : "dark", true);
  });

  document.getElementById("copyPageUrlBtn")?.addEventListener("click", () => {
    const slug = document.body.dataset.slug;
    const projPrefix = document.body.dataset.projPrefix || "..";
    const relTarget = activeView === "business" ? `${projPrefix}/${slug}/business/` : `${projPrefix}/${slug}/`;
    const shareUrl = new URL(relTarget, window.location.href).href;
    copyText(
      shareUrl,
      activeView === "business" ? "Copied Business Value & ROI URL" : "Copied Technical Case Study URL"
    );
  });

  document.getElementById("flagshipSelect")?.addEventListener("change", (e) => {
    const targetSlug = e.target.value;
    if (!targetSlug) return;
    const projPrefix = document.body.dataset.projPrefix || "..";
    const suffix = activeView === "business" ? "business/" : "";
    window.location.href = `${projPrefix}/${targetSlug}/${suffix}`;
  });

  document.querySelectorAll("[data-copy-target]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.getAttribute("data-copy-target"));
      if (target) copyText(target.textContent, btn.getAttribute("data-copy-label") || "Copied");
    });
  });

  window.addEventListener("scroll", updateScrollSpy, { passive: true });
  initSimulator();
}

bootCaseStudy();

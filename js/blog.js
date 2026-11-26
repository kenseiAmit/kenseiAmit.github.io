/* ==========================================================================
   Blog & Interactive Essay Controller (/blog/ & /blog/agentic-sre/)
   Light-Default Theme · Reading Progress · Mermaid v11 · G0-G6 Simulator
   ========================================================================== */

const THEME_STORAGE_KEY = "ak_portfolio_theme_v2";
let mermaidMod = null;

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

async function copyText(text, label = "Copied link") {
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

async function renderMermaidDiagrams() {
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
      const src = el.getAttribute("data-mermaid-src");
      if (!src) continue;
      const { svg } = await mermaidMod.render(`blog_mmd_${i}_${Date.now()}`, src);
      el.innerHTML = svg;
    }
  } catch {
    // Leaves preformatted Mermaid fallback intact if offline
  }
}

function applyTheme(theme, persist = true) {
  document.documentElement.setAttribute("data-theme", theme);
  if (persist) {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
  renderMermaidDiagrams();
}

function initScrollAndProgress() {
  const bar = document.getElementById("readingProgress");
  const links = Array.from(document.querySelectorAll(".article-toc-nav a"));
  const sections = links.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);

  const onScroll = () => {
    if (bar) {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docHeight > 0 ? Math.min(100, Math.max(0, (window.scrollY / docHeight) * 100)) : 0;
      bar.style.width = `${pct}%`;
    }
    if (sections.length) {
      let activeIdx = 0;
      const offset = window.scrollY + 140;
      sections.forEach((sec, idx) => {
        if (sec.offsetTop <= offset) activeIdx = idx;
      });
      links.forEach((a, idx) => a.classList.toggle("active", idx === activeIdx));
    }
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ==========================================================================
   Deterministic G0–G6 Risk Grading & Policy Override Simulator
   ========================================================================== */

const GRADES = [
  {
    code: "G0",
    name: "RECORD",
    tone: "g-low",
    playbook: "Record on incident timeline & include in daily digest (zero channel noise).",
    autonomy: "Automatic · Timeline only"
  },
  {
    code: "G1",
    name: "WATCH",
    tone: "g-low",
    playbook: "Enter timed watch state with explicit recheck cadence & escalation triggers.",
    autonomy: "Automatic (L3 internal watch)"
  },
  {
    code: "G2",
    name: "INFORM / PREDICT",
    tone: "g-med",
    playbook: "Notify system owner in Slack/Teams with trend forecast, time-to-breach & suggested action.",
    autonomy: "Automatic (L1 advise)"
  },
  {
    code: "G3",
    name: "SELF-HEAL",
    tone: "g-med",
    playbook: "Execute allowlisted idempotent runbook (e.g., 1 retry with backoff), verify, then notify.",
    autonomy: "Automatic (requires L3-approved runbook)"
  },
  {
    code: "G4",
    name: "PROPOSE",
    tone: "g-warn",
    playbook: "Prepare exact remediation + rollback plan and request one-click human approval.",
    autonomy: "Human Approves (L2 gate)"
  },
  {
    code: "G5",
    name: "ESCALATE / PAGE",
    tone: "g-crit",
    playbook: "Page on-call immediately with short diagnosis, cited evidence links & ruled-out hypotheses.",
    autonomy: "Human Leads (PagerDuty + Incident Channel)"
  },
  {
    code: "G6",
    name: "MAJOR INCIDENT",
    tone: "g-crit",
    playbook: "Open major incident bridge; agent acts strictly as read-only scribe & status drafter.",
    autonomy: "Incident Commander Leads"
  }
];

function initGradeSimulator() {
  const root = document.getElementById("gradeSimulator");
  if (!root) return;

  const els = {
    impact: document.getElementById("gsImpact"),
    crit: document.getElementById("gsCrit"),
    urg: document.getElementById("gsUrg"),
    impactVal: document.getElementById("gsImpactVal"),
    critVal: document.getElementById("gsCritVal"),
    urgVal: document.getElementById("gsUrgVal"),
    runbook: document.getElementById("gsRunbook"),
    worsening: document.getElementById("gsWorsening"),
    multiDownstream: document.getElementById("gsBlast"),
    lowConf: document.getElementById("gsLowConf"),
    failedHeal: document.getElementById("gsFailedHeal"),
    maint: document.getElementById("gsMaint"),
    pill: document.getElementById("gsVerdictPill"),
    code: document.getElementById("gsVerdictCode"),
    name: document.getElementById("gsVerdictName"),
    playbook: document.getElementById("gsPlaybook"),
    rationale: document.getElementById("gsRationale")
  };

  const labels = ["1 (Low)", "2 (Medium)", "3 (High / Tier-1)"];

  const evaluate = () => {
    const imp = Number(els.impact.value);
    const crt = Number(els.crit.value);
    const urg = Number(els.urg.value);
    els.impactVal.textContent = labels[imp - 1];
    els.critVal.textContent = labels[crt - 1];
    els.urgVal.textContent = labels[urg - 1];

    const rawScore = imp * crt * urg; // 1..27
    const notes = [`Base risk score: ${imp} × ${crt} × ${urg} = ${rawScore}/27`];

    // Base band mapping from Section 9.2
    let gradeIdx = 0;
    if (rawScore <= 1) gradeIdx = 0; // G0
    else if (rawScore <= 3) gradeIdx = 1; // G1
    else if (rawScore <= 8) gradeIdx = els.runbook.checked ? 3 : 2; // G3 if approved L3 runbook, else G2
    else if (rawScore <= 17) gradeIdx = els.runbook.checked ? 4 : 5; // G4 if fix exists for approval, else G5
    else gradeIdx = rawScore >= 24 ? 6 : 5; // G5 or G6

    if (els.worsening.checked) {
      gradeIdx = Math.min(6, gradeIdx + 1);
      notes.push("+1 band (worsening trend)");
    }
    if (els.multiDownstream.checked) {
      gradeIdx = Math.min(6, gradeIdx + 1);
      notes.push("+1 band (multi-consumer blast radius)");
    }

    // Deterministic Policy Modifiers (Section 9.3)
    if (els.maint.checked && imp < 3) {
      gradeIdx = 0;
      notes.push("Maintenance window active → lowered expected alert to G0");
    } else {
      if (els.failedHeal.checked) {
        gradeIdx = Math.max(gradeIdx + 1, imp >= 2 ? 5 : 4);
        gradeIdx = Math.min(6, gradeIdx);
        notes.push("Failed self-heal → auto-retries halted & grade raised");
      }
      if (els.lowConf.checked) {
        if (imp >= 3 || (crt === 3 && urg >= 2)) {
          gradeIdx = Math.max(gradeIdx, 5);
          notes.push("Low confidence + high impact → escalated to G5 (no auto-action)");
        } else {
          gradeIdx = Math.min(gradeIdx, 2);
          notes.push("Low confidence → capped at G2 (no automatic action)");
        }
      }
      if (crt === 3) {
        gradeIdx = Math.max(gradeIdx, 2);
        if (imp >= 2 && (!els.runbook.checked || els.failedHeal.checked)) {
          gradeIdx = Math.max(gradeIdx, 5);
          notes.push("Tier-1 critical system with consumer/SLA risk & no auto-fix → floor G5");
        }
      }
    }

    const g = GRADES[gradeIdx];
    els.pill.className = `grade-verdict-pill mono ${g.tone}`;
    els.code.textContent = g.code;
    els.name.textContent = g.name;
    els.playbook.textContent = `${g.playbook} (${g.autonomy})`;
    els.rationale.textContent = notes.join(" · ");
  };

  root.querySelectorAll("input").forEach((inp) => inp.addEventListener("input", evaluate));
  root.querySelectorAll("input[type='checkbox']").forEach((inp) => inp.addEventListener("change", evaluate));
  evaluate();
}

function bootBlog() {
  localStorage.removeItem("ak_portfolio_theme");
  const saved = localStorage.getItem(THEME_STORAGE_KEY);
  const initialTheme = saved === "light" || saved === "dark" ? saved : "light";
  document.documentElement.setAttribute("data-theme", initialTheme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = initialTheme === "dark" ? "☀" : "☾";

  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    applyTheme(cur === "dark" ? "light" : "dark", true);
  });

  document.getElementById("sharePostBtn")?.addEventListener("click", () => {
    copyText(window.location.href, "Copied article URL for sharing");
  });

  initScrollAndProgress();
  initGradeSimulator();
  renderMermaidDiagrams();
}

bootBlog();

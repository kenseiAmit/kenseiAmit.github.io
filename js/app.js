/* ==========================================================================
   kenseiAmit.github.io — Interactive Engineering Portfolio Controller
   Role-Lens Deep Linking · Runtime Trace Replay Lab · Mermaid v11 Topologies
   ========================================================================== */

const STACK_QUICK_FILTERS = [
  "All Stack",
  "Claude",
  "Google ADK",
  "LangGraph",
  "MCP",
  "Semantic Kernel",
  "AWS",
  "FastAPI",
  "MLflow",
  "PyTorch",
  "Fairness / GRC"
];

const state = {
  data: null,
  activeTrack: "all",
  activeTraceId: null,
  domainFilter: "all",
  stackFilter: "All Stack",
  ciOnly: false,
  searchQuery: "",
  catalogView: "cards",
  modalSystemSlug: null,
  modalTab: "overview",
  cmdOpen: false,
  cmdSelectedIndex: 0,
  cmdFilteredItems: [],
  mermaidModule: null
};

const esc = (str) =>
  String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

const richText = (str) =>
  esc(str).replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

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
  }, 2600);
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

/* ==========================================================================
   Theme Management
   ========================================================================== */

const THEME_STORAGE_KEY = "ak_portfolio_theme_v2";

function initTheme() {
  localStorage.removeItem("ak_portfolio_theme");
  const saved = localStorage.getItem(THEME_STORAGE_KEY);
  const theme = saved === "light" || saved === "dark" ? saved : "light";
  applyTheme(theme, false);
}

function applyTheme(theme, persist = true) {
  document.documentElement.setAttribute("data-theme", theme);
  if (persist) {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
  // Re-render mermaid if topology tab is currently open
  if (state.modalSystemSlug && state.modalTab === "topology") {
    renderCaseStudyModalBody();
  }
}

/* ==========================================================================
   URL State Sync (?track=...&system=...)
   ========================================================================== */

function readUrlState() {
  const params = new URLSearchParams(window.location.search);
  const track = params.get("track");
  const sys = params.get("system");
  if (track && state.data.tracks.some((t) => t.id === track)) {
    state.activeTrack = track;
  }
  if (sys && state.data.systems.some((s) => s.slug === sys)) {
    state.modalSystemSlug = sys;
  }
}

function syncUrlState() {
  const params = new URLSearchParams();
  if (state.activeTrack && state.activeTrack !== "all") {
    params.set("track", state.activeTrack);
  }
  if (state.modalSystemSlug) {
    params.set("system", state.modalSystemSlug);
  }
  const qs = params.toString();
  const nextUrl = `${window.location.pathname}${qs ? `?${qs}` : ""}${window.location.hash}`;
  window.history.replaceState({}, "", nextUrl);
}

function buildShareUrl(paramsObj) {
  const base = `${window.location.origin}${window.location.pathname}`;
  const p = new URLSearchParams();
  Object.entries(paramsObj).forEach(([k, v]) => {
    if (v && v !== "all") p.set(k, v);
  });
  const qs = p.toString();
  return qs ? `${base}?${qs}` : base;
}

/* ==========================================================================
   Role Lens & Flagships Rendering
   ========================================================================== */

function renderRoleLens() {
  const tabsEl = document.getElementById("trackTabs");
  const briefEl = document.getElementById("trackBrief");
  if (!tabsEl || !briefEl) return;

  tabsEl.innerHTML = state.data.tracks
    .map((t) => {
      const active = t.id === state.activeTrack ? "active" : "";
      return `
        <button type="button" role="tab" aria-selected="${t.id === state.activeTrack}" class="track-tab ${active}" data-track="${esc(t.id)}">
          <span>${esc(t.label)}</span>
          <span class="track-count mono">${esc(t.badge)}</span>
        </button>
      `;
    })
    .join("");

  const currentTrack = state.data.tracks.find((t) => t.id === state.activeTrack) || state.data.tracks[0];
  briefEl.innerHTML = `
    <div>
      <h2>${esc(currentTrack.headline)}</h2>
      <p>${esc(currentTrack.pitch)}</p>
    </div>
    <div style="display:flex;gap:8px;flex-shrink:0;flex-wrap:wrap;">
      ${
        state.activeTrack !== "all"
          ? `<button type="button" class="btn btn-secondary btn-sm" id="filterCatalogByTrackBtn">Filter Catalog to ${esc(currentTrack.label)} ↓</button>`
          : ""
      }
    </div>
  `;

  tabsEl.querySelectorAll("[data-track]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.activeTrack = btn.getAttribute("data-track");
      syncUrlState();
      renderRoleLens();
      renderFlagships();
    });
  });

  const filterBtn = document.getElementById("filterCatalogByTrackBtn");
  if (filterBtn) {
    filterBtn.addEventListener("click", () => {
      document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
      renderCatalog();
    });
  }
}

function getFeaturedSystemsForTrack() {
  const all = state.data.systems;
  if (state.activeTrack === "all") {
    return all.filter((s) => s.flagship);
  }
  const matching = all.filter((s) => s.tracks.includes(state.activeTrack));
  // Flagships in that track first, then remaining systems up to 7
  return matching.slice(0, 7);
}

function findTraceForSystem(slug) {
  return state.data.traces.find((t) => t.systemSlug === slug) || null;
}

function renderFlagships() {
  const grid = document.getElementById("flagshipGrid");
  const heading = document.getElementById("flagshipHeading");
  const kicker = document.getElementById("flagshipKicker");
  if (!grid) return;

  const trackObj = state.data.tracks.find((t) => t.id === state.activeTrack) || state.data.tracks[0];
  const featured = getFeaturedSystemsForTrack();

  if (heading && kicker) {
    if (state.activeTrack === "all") {
      kicker.textContent = "01 · Featured Engineering Case Studies (7 Flagships)";
      heading.textContent = "Flagship Production Architectures";
    } else {
      kicker.textContent = `01 · Role Lens: ${trackObj.label} (${featured.length} Featured)`;
      heading.textContent = `Priority Systems for ${trackObj.label}`;
    }
  }

  grid.innerHTML = featured
    .map((sys, idx) => {
      const isHeroSpan = idx === 0 && featured.length % 2 === 1;
      const linkedTrace = findTraceForSystem(sys.slug);
      const flagshipHref = sys.flagship ? `projects/${esc(sys.slug)}/` : null;
      return `
        <article class="flagship-card ${isHeroSpan ? "hero-span" : ""}">
          ${
            flagshipHref
              ? `<a href="${flagshipHref}" class="card-media" title="Open ${esc(sys.title)} full production case study">`
              : `<div class="card-media" data-open-system="${esc(sys.slug)}" title="Inspect ${esc(sys.title)} architecture & telemetry">`
          }
            <img src="${esc(sys.primaryImage)}" alt="${esc(sys.title)} empirical telemetry" loading="${idx < 2 ? "eager" : "lazy"}" />
            <div class="media-badges mono">
              <span class="pill pill-dark">${sys.flagship ? `★ FLAGSHIP #${sys.flagshipRank}` : esc(sys.domainName)}</span>
              <span style="display:flex;gap:6px;">
                ${sys.liveDemoSvg ? `<span class="pill pill-dark">▶ Live SVG Trace</span>` : ""}
                ${sys.ci ? `<span class="pill pill-ci">✓ CI Passing</span>` : ""}
              </span>
            </div>
          ${flagshipHref ? `</a>` : `</div>`}

          <div class="card-body">
            <div class="card-meta-row">
              <span class="domain-tag mono">
                <span class="domain-dot" style="background:${esc(sys.domainColor)}"></span>
                ${esc(sys.domainName)}
              </span>
              <span class="mono" style="font-size:0.72rem;color:var(--text-faint);">${esc(sys.slug)}</span>
            </div>

            ${
              flagshipHref
                ? `<h3 class="card-title"><a href="${flagshipHref}">${esc(sys.title)}</a></h3>`
                : `<h3 class="card-title" data-open-system="${esc(sys.slug)}">${esc(sys.title)}</h3>`
            }
            <p class="card-summary">${richText(sys.summary)}</p>

            <div class="kpi-row mono">
              ${sys.metrics.map((m) => `<span class="kpi-chip">${esc(m)}</span>`).join("")}
            </div>

            <div class="tradeoff-box">
              <strong class="mono">Key Architectural Decision</strong>
              ${richText(sys.tradeoff)}
            </div>

            <div class="stack-row mono">
              ${sys.stack.slice(0, 7).map((st) => `<span class="stack-chip">${esc(st)}</span>`).join("")}
            </div>

            <div class="card-actions">
              ${
                flagshipHref
                  ? `<a href="${flagshipHref}" class="btn btn-primary btn-sm">Production Case Study →</a>
                     <a href="${flagshipHref}business/" class="btn btn-secondary btn-sm">📈 Business Value &amp; ROI →</a>
                     <button type="button" class="btn btn-ghost btn-sm" data-open-system="${esc(sys.slug)}">Quick Spec</button>`
                  : `<button type="button" class="btn btn-primary btn-sm" data-open-system="${esc(sys.slug)}">Case Study &amp; Topology</button>`
              }
              ${
                linkedTrace
                  ? `<button type="button" class="btn btn-ghost btn-sm" data-jump-trace="${esc(linkedTrace.id)}">Replay Trace</button>`
                  : ""
              }
              <a href="${esc(sys.repoUrl)}" target="_blank" rel="noopener" class="btn btn-ghost btn-sm">
                GitHub ↗
              </a>
              ${
                sys.liveUrl
                  ? `<a href="${esc(sys.liveUrl)}" target="_blank" rel="noopener" class="btn btn-ghost btn-sm mono">Live API ↗</a>`
                  : ""
              }
            </div>
          </div>
        </article>
      `;
    })
    .join("");

  bindSystemTriggers(grid);
}

/* ==========================================================================
   Runtime Trace & Telemetry Replay Lab
   ========================================================================== */

function renderTraceLab() {
  const rail = document.getElementById("traceRailList");
  const stage = document.getElementById("traceStage");
  if (!rail || !stage) return;

  if (!state.activeTraceId && state.data.traces.length) {
    state.activeTraceId = state.data.traces[0].id;
  }

  rail.innerHTML = state.data.traces
    .map((tr) => {
      const active = tr.id === state.activeTraceId ? "active" : "";
      return `
        <button type="button" class="trace-item-btn ${active}" data-trace-id="${esc(tr.id)}">
          <span class="trace-badge mono tone-${esc(tr.badgeTone)}">${esc(tr.badge)}</span>
          <div class="trace-item-title">${esc(tr.title)}</div>
          <div class="trace-item-sub mono">${esc(tr.systemSlug)}</div>
        </button>
      `;
    })
    .join("");

  const tr = state.data.traces.find((x) => x.id === state.activeTraceId) || state.data.traces[0];
  const rawJson = JSON.stringify(tr.rawPayload, null, 2);

  stage.innerHTML = `
    <div class="trace-stage-top">
      <div>
        <span class="trace-badge mono tone-${esc(tr.badgeTone)}">${esc(tr.badge)}</span>
        <h3 class="trace-stage-title">${esc(tr.title)}</h3>
        <div class="mono" style="font-size:0.76rem;color:var(--text-muted);margin-top:3px;">${esc(tr.subtitle)}</div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button type="button" class="btn btn-secondary btn-sm" data-open-system="${esc(tr.systemSlug)}">
          Open System Architecture
        </button>
        <a href="https://github.com/kenseiAmit/${esc(tr.systemSlug)}" target="_blank" rel="noopener" class="btn btn-ghost btn-sm">
          Repo Source ↗
        </a>
      </div>
    </div>

    <div class="trace-io-grid">
      <div class="io-box">
        <div class="io-label mono">Recorded Input / Adversarial Probe</div>
        <div class="io-text mono" style="font-size:0.8rem;">${esc(tr.prompt)}</div>
      </div>
      <div class="io-box" style="border-color:var(--border-accent);">
        <div class="io-label mono">Verified Runtime Outcome</div>
        <div class="io-text">${richText(tr.outcome)}</div>
      </div>
    </div>

    <div class="trace-kpi-strip">
      ${tr.kpis
        .map(
          (k) => `
          <div class="trace-kpi">
            <div class="trace-kpi-lbl mono">${esc(k.label)}</div>
            <div class="trace-kpi-val mono">${esc(k.value)}</div>
          </div>
        `
        )
        .join("")}
    </div>

    <div>
      <div class="io-label mono" style="margin-bottom:8px;">Execution Span &amp; Guardrail Waterfall</div>
      <div class="waterfall">
        ${tr.steps
          .map(
            (st) => `
            <div class="wf-step">
              <div class="wf-stage-name mono">${richText(st.stage)}</div>
              <div><span class="wf-badge mono wf-${esc(st.status)}">${esc(st.status)}</span></div>
              <div class="wf-detail">
                <span>${richText(st.detail)}</span>
                <span class="wf-latency mono">${esc(st.latency)}</span>
              </div>
            </div>
          `
          )
          .join("")}
      </div>
    </div>

    <div class="raw-json-panel">
      <div class="raw-json-bar mono">
        <span>Verified Repository Artifact Payload (JSON)</span>
        <button type="button" class="icon-btn mono" style="height:26px;font-size:0.72rem;" id="copyTraceJsonBtn">Copy JSON</button>
      </div>
      <pre class="raw-json-pre mono">${esc(rawJson)}</pre>
    </div>
  `;

  rail.querySelectorAll("[data-trace-id]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.activeTraceId = btn.getAttribute("data-trace-id");
      renderTraceLab();
    });
  });

  document.getElementById("copyTraceJsonBtn")?.addEventListener("click", () => {
    copyText(rawJson, "Copied trace JSON artifact");
  });

  bindSystemTriggers(stage);
}

/* ==========================================================================
   28-System Engineering Catalog & Domain Cards
   ========================================================================== */

function matchesStackFilter(sys, filter) {
  if (!filter || filter === "All Stack") return true;
  const hay = `${sys.stack.join(" ")} ${sys.summary} ${sys.title}`.toLowerCase();
  if (filter === "Fairness / GRC") {
    return /fairness|shap|eu ai act|stride|guardrail|grc|owasp/.test(hay);
  }
  return hay.includes(filter.toLowerCase());
}

function getFilteredCatalogSystems() {
  const q = state.searchQuery.trim().toLowerCase();
  return state.data.systems.filter((sys) => {
    if (state.domainFilter !== "all" && sys.domainId !== state.domainFilter) return false;
    if (state.ciOnly && !sys.ci) return false;
    if (!matchesStackFilter(sys, state.stackFilter)) return false;
    if (q) {
      const hay = `${sys.slug} ${sys.title} ${sys.domainName} ${sys.summary} ${sys.tradeoff} ${sys.metrics.join(" ")} ${sys.stack.join(" ")}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

function renderCatalogFilters() {
  const domWrap = document.getElementById("domainFilterPills");
  const stackWrap = document.getElementById("stackFilterPills");
  if (!domWrap || !stackWrap) return;

  const domButtons = [
    `<button type="button" class="filter-pill ${state.domainFilter === "all" ? "active" : ""}" data-dom="all">All 6 Domains (28)</button>`,
    ...state.data.domains.map((d) => {
      const cnt = state.data.systems.filter((s) => s.domainId === d.id).length;
      const active = state.domainFilter === d.id ? "active" : "";
      return `<button type="button" class="filter-pill ${active}" data-dom="${esc(d.id)}">${esc(d.num)} · ${esc(d.shortName)} (${cnt})</button>`;
    })
  ];
  domWrap.innerHTML = domButtons.join("");

  stackWrap.innerHTML = STACK_QUICK_FILTERS.map((sf) => {
    const active = state.stackFilter === sf ? "active" : "";
    return `<button type="button" class="filter-pill mono ${active}" data-stack="${esc(sf)}" style="font-size:0.73rem;">${esc(sf)}</button>`;
  }).join("");

  domWrap.querySelectorAll("[data-dom]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.domainFilter = btn.getAttribute("data-dom");
      renderCatalogFilters();
      renderCatalog();
    });
  });

  stackWrap.querySelectorAll("[data-stack]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.stackFilter = btn.getAttribute("data-stack");
      renderCatalogFilters();
      renderCatalog();
    });
  });
}

function renderCatalog() {
  const container = document.getElementById("catalogContainer");
  const countLabel = document.getElementById("catalogCountLabel");
  if (!container) return;

  const filtered = getFilteredCatalogSystems();
  if (countLabel) {
    countLabel.textContent = `Showing ${filtered.length} of ${state.data.systems.length} systems`;
  }

  if (!filtered.length) {
    container.innerHTML = `
      <div style="padding:40px;text-align:center;border-radius:14px;background:var(--bg-card);border:1px solid var(--border-subtle);">
        <p style="margin:0 0 12px;color:var(--text-muted);">No systems matched the active filter combination.</p>
        <button type="button" class="btn btn-secondary btn-sm" id="resetFiltersBtn">Reset All Filters</button>
      </div>
    `;
    document.getElementById("resetFiltersBtn")?.addEventListener("click", () => {
      state.domainFilter = "all";
      state.stackFilter = "All Stack";
      state.ciOnly = false;
      state.searchQuery = "";
      const si = document.getElementById("catalogSearchInput");
      if (si) si.value = "";
      const ci = document.getElementById("ciOnlyToggle");
      if (ci) ci.checked = false;
      renderCatalogFilters();
      renderCatalog();
    });
    return;
  }

  if (state.catalogView === "matrix") {
    container.innerHTML = `
      <div class="matrix-wrap">
        <table class="matrix-table">
          <thead>
            <tr>
              <th>System</th>
              <th>Domain</th>
              <th>Verified Benchmarks</th>
              <th>Core Stack</th>
              <th>CI</th>
              <th>Inspect</th>
            </tr>
          </thead>
          <tbody>
            ${filtered
              .map(
                (sys) => `
                <tr>
                  <td>
                    <div style="font-weight:700;cursor:pointer;color:var(--text-primary);" data-open-system="${esc(sys.slug)}">
                      ${sys.flagship ? "★ " : ""}${esc(sys.title)}
                    </div>
                    <div class="mono" style="font-size:0.72rem;color:var(--text-faint);">${esc(sys.slug)}</div>
                  </td>
                  <td>
                    <span class="domain-tag mono" style="font-size:0.7rem;">
                      <span class="domain-dot" style="background:${esc(sys.domainColor)}"></span>
                      ${esc(sys.domainName)}
                    </span>
                  </td>
                  <td class="mono" style="font-size:0.75rem;color:var(--text-secondary);">
                    ${sys.metrics.slice(0, 3).map(esc).join(" · ")}
                  </td>
                  <td class="mono" style="font-size:0.73rem;color:var(--text-muted);">
                    ${sys.stack.slice(0, 4).map(esc).join(" · ")}
                  </td>
                  <td class="mono" style="font-size:0.74rem;">
                    ${sys.ci ? `<span style="color:var(--accent-emerald);font-weight:700;">PASS</span>` : `<span style="color:var(--text-faint);">v1.0</span>`}
                  </td>
                  <td style="white-space:nowrap;">
                    ${
                      sys.flagship
                        ? `<a href="projects/${esc(sys.slug)}/" class="btn btn-primary btn-sm" style="padding:4px 9px;font-size:0.74rem;">Tech →</a>
                           <a href="projects/${esc(sys.slug)}/business/" class="btn btn-secondary btn-sm" style="padding:4px 9px;font-size:0.74rem;">Business →</a>`
                        : `<button type="button" class="btn btn-secondary btn-sm" style="padding:4px 9px;font-size:0.74rem;" data-open-system="${esc(sys.slug)}">Spec</button>`
                    }
                    <a href="${esc(sys.repoUrl)}" target="_blank" rel="noopener" class="btn btn-ghost btn-sm" style="padding:4px 9px;font-size:0.74rem;">Repo ↗</a>
                  </td>
                </tr>
              `
              )
              .join("")}
          </tbody>
        </table>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="catalog-grid">
        ${filtered
          .map(
            (sys) => `
            <article class="sys-card">
              <div class="card-meta-row">
                <span class="domain-tag mono" style="font-size:0.69rem;">
                  <span class="domain-dot" style="background:${esc(sys.domainColor)}"></span>
                  ${esc(sys.domainName)}
                </span>
                ${
                  sys.ci
                    ? `<span class="pill pill-ci mono" style="font-size:0.66rem;">✓ CI</span>`
                    : sys.flagship
                    ? `<span class="pill mono" style="font-size:0.66rem;background:var(--bg-subtle);">★ Flagship</span>`
                    : ""
                }
              </div>

              <h3 class="sys-card-title" data-open-system="${esc(sys.slug)}">${esc(sys.title)}</h3>
              <p class="sys-card-desc">${richText(sys.summary)}</p>

              <div class="kpi-row mono" style="margin-bottom:10px;">
                ${sys.metrics
                  .slice(0, 3)
                  .map((m) => `<span class="kpi-chip" style="font-size:0.69rem;padding:3px 7px;">${esc(m)}</span>`)
                  .join("")}
              </div>

              <div class="stack-row mono" style="margin-bottom:12px;">
                ${sys.stack
                  .slice(0, 5)
                  .map((st) => `<span class="stack-chip" style="font-size:0.68rem;">${esc(st)}</span>`)
                  .join("")}
              </div>

              <div class="card-actions" style="margin-top:auto;">
                ${
                  sys.flagship
                    ? `<a href="projects/${esc(sys.slug)}/" class="btn btn-primary btn-sm" style="flex:1;justify-content:center;">Case Study →</a>
                       <a href="projects/${esc(sys.slug)}/business/" class="btn btn-secondary btn-sm" title="Business Value & ROI">📈 ROI</a>`
                    : `<button type="button" class="btn btn-secondary btn-sm" style="flex:1;justify-content:center;" data-open-system="${esc(sys.slug)}">Architecture &amp; Evidence</button>`
                }
                <a href="${esc(sys.repoUrl)}" target="_blank" rel="noopener" class="btn btn-ghost btn-sm" aria-label="Open ${esc(sys.title)} on GitHub">
                  GitHub ↗
                </a>
              </div>
            </article>
          `
          )
          .join("")}
      </div>
    `;
  }

  bindSystemTriggers(container);
}

function renderDomainsGrid() {
  const grid = document.getElementById("domainsGrid");
  if (!grid) return;

  grid.innerHTML = state.data.domains
    .map((d) => {
      const cnt = state.data.systems.filter((s) => s.domainId === d.id).length;
      return `
        <div class="domain-card" data-select-domain="${esc(d.id)}" role="button" tabindex="0">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span class="domain-num mono" style="color:${esc(d.color)}">DOMAIN ${esc(d.num)}</span>
            <span class="track-count mono">${cnt} Systems</span>
          </div>
          <h3>${esc(d.name)}</h3>
          <p>${esc(d.description)}</p>
        </div>
      `;
    })
    .join("");

  grid.querySelectorAll("[data-select-domain]").forEach((card) => {
    const activate = () => {
      state.domainFilter = card.getAttribute("data-select-domain");
      renderCatalogFilters();
      renderCatalog();
      document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
    };
    card.addEventListener("click", activate);
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        activate();
      }
    });
  });
}

/* ==========================================================================
   Deep-Dive System Case Study Modal & Mermaid v11 Rendering
   ========================================================================== */

async function ensureMermaid() {
  if (state.mermaidModule) return state.mermaidModule;
  try {
    const mod = await import("https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs");
    state.mermaidModule = mod.default;
    return state.mermaidModule;
  } catch {
    return null;
  }
}

function openSystemModal(slug, tab = "overview") {
  const sys = state.data.systems.find((s) => s.slug === slug);
  if (!sys) return;
  state.modalSystemSlug = slug;
  state.modalTab = tab;
  syncUrlState();

  const backdrop = document.getElementById("caseModalBackdrop");
  const titleEl = document.getElementById("caseModalTitle");
  const domEl = document.getElementById("caseModalDomain");
  const footerLinks = document.getElementById("caseModalFooterLinks");

  if (titleEl) titleEl.textContent = sys.title;
  if (domEl) {
    domEl.innerHTML = `<span class="domain-dot" style="background:${esc(sys.domainColor)}"></span> ${esc(sys.domainName)} · ${esc(sys.slug)}`;
  }
  if (footerLinks) {
    footerLinks.innerHTML = `
      ${
        sys.ci
          ? `<a href="${esc(sys.ci.url)}" target="_blank" rel="noopener" class="btn btn-ghost btn-sm mono" style="color:var(--accent-emerald);">✓ CI Workflow ↗</a>`
          : ""
      }
      ${
        sys.liveUrl
          ? `<a href="${esc(sys.liveUrl)}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm mono">Live Swagger API ↗</a>`
          : ""
      }
      ${
        sys.flagship
          ? `<a href="projects/${esc(sys.slug)}/" class="btn btn-secondary btn-sm">Technical Case Study →</a>
             <a href="projects/${esc(sys.slug)}/business/" class="btn btn-secondary btn-sm">📈 Business Value &amp; ROI →</a>`
          : ""
      }
      <a href="${esc(sys.repoUrl)}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Open GitHub Repository ↗</a>
    `;
  }

  document.querySelectorAll("#caseModalTabs .modal-tab").forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-tab") === state.modalTab);
  });

  renderCaseStudyModalBody();
  if (backdrop) {
    backdrop.hidden = false;
    document.body.style.overflow = "hidden";
  }
}

function closeSystemModal() {
  state.modalSystemSlug = null;
  syncUrlState();
  const backdrop = document.getElementById("caseModalBackdrop");
  if (backdrop) backdrop.hidden = true;
  document.body.style.overflow = "";
}

async function renderCaseStudyModalBody() {
  const body = document.getElementById("caseModalBody");
  const sys = state.data.systems.find((s) => s.slug === state.modalSystemSlug);
  if (!body || !sys) return;

  if (state.modalTab === "overview") {
    body.innerHTML = `
      <div style="display:grid;grid-template-columns:1.15fr 0.85fr;gap:22px;align-items:start;" class="hero-grid">
        <div>
          <p style="margin:0 0 16px;font-size:0.96rem;color:var(--text-secondary);">${richText(sys.summary)}</p>

          <div class="kpi-row mono" style="margin-bottom:18px;">
            ${sys.metrics.map((m) => `<span class="kpi-chip">${esc(m)}</span>`).join("")}
          </div>

          <div class="tradeoff-box" style="margin-bottom:20px;">
            <strong class="mono">Key Engineering Decision &amp; Trade-Off</strong>
            ${richText(sys.tradeoff)}
          </div>

          <h4 class="mono" style="margin:0 0 10px;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-muted);">
            Architectural Highlights
          </h4>
          <ul style="margin:0 0 20px;padding-left:18px;color:var(--text-secondary);font-size:0.87rem;display:flex;flex-direction:column;gap:8px;">
            ${sys.highlights.map((h) => `<li>${richText(h)}</li>`).join("")}
          </ul>

          <h4 class="mono" style="margin:0 0 8px;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-muted);">
            Technology Stack
          </h4>
          <div class="stack-row mono" style="margin-bottom:0;">
            ${sys.stack.map((st) => `<span class="stack-chip">${esc(st)}</span>`).join("")}
          </div>
        </div>

        <div>
          <figure class="gallery-figure">
            <img src="${esc(sys.primaryImage)}" alt="${esc(sys.title)} telemetry" />
            <figcaption class="gallery-caption mono">Verified Empirical Telemetry · ${esc(sys.slug)}</figcaption>
          </figure>
          ${
            sys.liveDemoSvg
              ? `<figure class="gallery-figure" style="margin-top:14px;">
                  <img src="${esc(sys.liveDemoSvg)}" alt="${esc(sys.title)} animated execution trace" />
                  <figcaption class="gallery-caption mono">Recorded Terminal Execution Trace</figcaption>
                 </figure>`
              : ""
          }
        </div>
      </div>
    `;
  } else if (state.modalTab === "topology") {
    body.innerHTML = `
      <div style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <div class="mono" style="font-size:0.78rem;color:var(--text-muted);">
          System Architecture Topology (${sys.mermaids.length} Diagram${sys.mermaids.length > 1 ? "s" : ""})
        </div>
      </div>
      ${sys.mermaids
        .map(
          (m, idx) => `
          <div class="mermaid-stage" id="mermaidStage_${idx}">
            <pre class="mono" style="text-align:left;font-size:0.78rem;color:var(--text-muted);overflow:auto;">${esc(m)}</pre>
          </div>
        `
        )
        .join("")}
    `;

    const mermaid = await ensureMermaid();
    if (mermaid) {
      const isDark = document.documentElement.getAttribute("data-theme") !== "light";
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: isDark ? "dark" : "default",
        fontFamily: "Inter, system-ui, sans-serif"
      });
      for (let i = 0; i < sys.mermaids.length; i++) {
        const container = document.getElementById(`mermaidStage_${i}`);
        if (!container) continue;
        try {
          const id = `mmd_${sys.slug.replace(/[^a-zA-Z0-9]/g, "_")}_${i}_${Date.now()}`;
          const { svg } = await mermaid.render(id, sys.mermaids[i]);
          container.innerHTML = svg;
        } catch {
          // Keeps clean preformatted Mermaid source fallback if syntax edge-case occurs
        }
      }
    }
  } else if (state.modalTab === "telemetry") {
    body.innerHTML = `
      ${
        sys.liveDemoSvg
          ? `<div style="margin-bottom:20px;">
              <div class="io-label mono" style="margin-bottom:8px;">Animated Terminal Execution Trace</div>
              <figure class="gallery-figure">
                <img src="${esc(sys.liveDemoSvg)}" alt="${esc(sys.title)} live execution trace" />
              </figure>
             </div>`
          : ""
      }
      <div class="io-label mono" style="margin-bottom:8px;">Empirical Telemetry, Dashboards &amp; Screenshots (${sys.gallery.length})</div>
      <div class="gallery-grid">
        ${sys.gallery
          .map(
            (img) => `
            <figure class="gallery-figure">
              <a href="${esc(img.url)}" target="_blank" rel="noopener" title="Open full-resolution image in new tab">
                <img src="${esc(img.url)}" alt="${esc(img.caption)}" loading="lazy" />
              </a>
              <figcaption class="gallery-caption mono">${esc(img.caption)} (Click for full-res ↗)</figcaption>
            </figure>
          `
          )
          .join("")}
      </div>
    `;
  } else if (state.modalTab === "quickstart") {
    const qs = sys.quickStart || `git clone ${sys.repoUrl}.git\ncd ${sys.slug}`;
    body.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:16px;">
        <div class="raw-json-panel">
          <div class="raw-json-bar mono">
            <span>Local Reproduction &amp; Verification Commands</span>
            <button type="button" class="icon-btn mono" style="height:26px;font-size:0.72rem;" id="copyQuickStartBtn">Copy Commands</button>
          </div>
          <pre class="raw-json-pre mono" style="max-height:320px;">${esc(qs)}</pre>
        </div>

        <div class="io-box">
          <div class="io-label mono">Repository &amp; Verification Links</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">
            <a href="${esc(sys.repoUrl)}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">GitHub Repository (${esc(sys.slug)}) ↗</a>
            ${
              sys.ci
                ? `<a href="${esc(sys.ci.url)}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm mono">GitHub Actions CI Pipeline ↗</a>`
                : ""
            }
            ${
              sys.liveUrl
                ? `<a href="${esc(sys.liveUrl)}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm mono">Live Swagger Endpoint ↗</a>`
                : ""
            }
          </div>
        </div>
      </div>
    `;
    document.getElementById("copyQuickStartBtn")?.addEventListener("click", () => {
      copyText(qs, "Copied setup commands");
    });
  }
}

function stepModalSystem(delta) {
  if (!state.modalSystemSlug) return;
  const list = state.data.systems;
  const idx = list.findIndex((s) => s.slug === state.modalSystemSlug);
  if (idx === -1) return;
  const nextIdx = (idx + delta + list.length) % list.length;
  openSystemModal(list[nextIdx].slug, state.modalTab);
}

/* ==========================================================================
   Cmd+K Instant Command Palette
   ========================================================================== */

function buildCommandItems(query) {
  const q = query.trim().toLowerCase();
  const items = [];

  state.data.systems
    .filter((s) => s.flagship)
    .forEach((sys) => {
      items.push({
        type: "Flagship Tech",
        title: `Case Study: ${sys.title}`,
        sub: `/projects/${sys.slug}/ · ${sys.metrics.slice(0, 2).join(" · ")}`,
        haystack: `${sys.slug} ${sys.stack.join(" ")} ${sys.summary} flagship case study architecture`.toLowerCase(),
        action: () => {
          window.location.href = `projects/${sys.slug}/`;
        }
      });
      items.push({
        type: "Business ROI",
        title: `Business Value & ROI: ${sys.title}`,
        sub: `/projects/${sys.slug}/business/ · Feature-to-Value Matrix & Simulator`,
        haystack: `${sys.slug} ${sys.title} business value roi finops unit economics executive impact`.toLowerCase(),
        action: () => {
          window.location.href = `projects/${sys.slug}/business/`;
        }
      });
    });

  state.data.tracks.forEach((t) => {
    items.push({
      type: "Role Lens",
      title: `Switch Role Lens: ${t.label}`,
      sub: t.badge,
      action: () => {
        state.activeTrack = t.id;
        syncUrlState();
        renderRoleLens();
        renderFlagships();
        document.getElementById("flagships")?.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  state.data.traces.forEach((tr) => {
    items.push({
      type: "Trace Replay",
      title: tr.title,
      sub: tr.badge,
      action: () => {
        state.activeTraceId = tr.id;
        renderTraceLab();
        document.getElementById("trace-lab")?.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  state.data.systems.forEach((sys) => {
    items.push({
      type: sys.flagship ? "★ System" : "System",
      title: sys.title,
      sub: `${sys.domainName} · ${sys.metrics[0] || ""}`,
      haystack: `${sys.slug} ${sys.stack.join(" ")} ${sys.summary}`.toLowerCase(),
      action: () => openSystemModal(sys.slug, "overview")
    });
  });

  if (!q) return items.slice(0, 16);
  return items.filter((it) => {
    const hay = `${it.type} ${it.title} ${it.sub} ${it.haystack || ""}`.toLowerCase();
    return hay.includes(q);
  });
}

function openCmdPalette() {
  state.cmdOpen = true;
  state.cmdSelectedIndex = 0;
  const backdrop = document.getElementById("cmdBackdrop");
  const input = document.getElementById("cmdInput");
  if (backdrop) backdrop.hidden = false;
  if (input) {
    input.value = "";
    renderCmdList("");
    setTimeout(() => input.focus(), 10);
  }
}

function closeCmdPalette() {
  state.cmdOpen = false;
  const backdrop = document.getElementById("cmdBackdrop");
  if (backdrop) backdrop.hidden = true;
}

function renderCmdList(query) {
  const listEl = document.getElementById("cmdList");
  if (!listEl) return;
  state.cmdFilteredItems = buildCommandItems(query);
  if (state.cmdSelectedIndex >= state.cmdFilteredItems.length) {
    state.cmdSelectedIndex = 0;
  }

  if (!state.cmdFilteredItems.length) {
    listEl.innerHTML = `<div style="padding:18px;text-align:center;color:var(--text-muted);font-size:0.85rem;">No matching systems, protocols, or tracks.</div>`;
    return;
  }

  listEl.innerHTML = state.cmdFilteredItems
    .map((it, idx) => {
      const sel = idx === state.cmdSelectedIndex ? "selected" : "";
      return `
        <button type="button" class="cmd-item ${sel}" data-cmd-idx="${idx}">
          <div>
            <div style="font-size:0.87rem;font-weight:650;">${esc(it.title)}</div>
            <div class="mono" style="font-size:0.72rem;color:var(--text-muted);">${esc(it.sub)}</div>
          </div>
          <span class="kbd mono">${esc(it.type)}</span>
        </button>
      `;
    })
    .join("");

  listEl.querySelectorAll("[data-cmd-idx]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const idx = Number(btn.getAttribute("data-cmd-idx"));
      const item = state.cmdFilteredItems[idx];
      closeCmdPalette();
      if (item) item.action();
    });
  });
}

/* ==========================================================================
   Shared Event Delegation & Initialization
   ========================================================================== */

function bindSystemTriggers(root) {
  root.querySelectorAll("[data-open-system]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.stopPropagation();
      openSystemModal(el.getAttribute("data-open-system"), "overview");
    });
  });
  root.querySelectorAll("[data-jump-trace]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.stopPropagation();
      state.activeTraceId = el.getAttribute("data-jump-trace");
      renderTraceLab();
      document.getElementById("trace-lab")?.scrollIntoView({ behavior: "smooth" });
    });
  });
}

function bindGlobalEvents() {
  // Theme Toggle
  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    applyTheme(cur === "dark" ? "light" : "dark", true);
  });

  // Share View / Copy Track Link
  const copyTrackHandler = () => {
    const url = buildShareUrl({ track: state.activeTrack });
    const trackObj = state.data.tracks.find((t) => t.id === state.activeTrack);
    copyText(url, `Copied ${trackObj ? trackObj.label : "Portfolio"} link: ${url}`);
  };
  document.getElementById("shareViewBtn")?.addEventListener("click", copyTrackHandler);
  document.getElementById("copyTrackUrlBtn")?.addEventListener("click", copyTrackHandler);

  // Catalog search, CI toggle, View switcher
  document.getElementById("catalogSearchInput")?.addEventListener("input", (e) => {
    state.searchQuery = e.target.value;
    renderCatalog();
  });

  document.getElementById("ciOnlyToggle")?.addEventListener("change", (e) => {
    state.ciOnly = e.target.checked;
    renderCatalog();
  });

  document.getElementById("viewCardsBtn")?.addEventListener("click", () => {
    state.catalogView = "cards";
    document.getElementById("viewCardsBtn")?.classList.add("active");
    document.getElementById("viewMatrixBtn")?.classList.remove("active");
    renderCatalog();
  });

  document.getElementById("viewMatrixBtn")?.addEventListener("click", () => {
    state.catalogView = "matrix";
    document.getElementById("viewMatrixBtn")?.classList.add("active");
    document.getElementById("viewCardsBtn")?.classList.remove("active");
    renderCatalog();
  });

  // Case Study Modal controls
  document.getElementById("closeCaseModalBtn")?.addEventListener("click", closeSystemModal);
  document.getElementById("caseModalBackdrop")?.addEventListener("click", (e) => {
    if (e.target.id === "caseModalBackdrop") closeSystemModal();
  });
  document.getElementById("prevSystemBtn")?.addEventListener("click", () => stepModalSystem(-1));
  document.getElementById("nextSystemBtn")?.addEventListener("click", () => stepModalSystem(1));

  document.getElementById("copySystemLinkBtn")?.addEventListener("click", () => {
    const url = buildShareUrl({ track: state.activeTrack, system: state.modalSystemSlug });
    copyText(url, "Copied direct Case Study URL");
  });

  document.querySelectorAll("#caseModalTabs .modal-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.modalTab = btn.getAttribute("data-tab");
      document.querySelectorAll("#caseModalTabs .modal-tab").forEach((b) =>
        b.classList.toggle("active", b === btn)
      );
      renderCaseStudyModalBody();
    });
  });

  // Command Palette
  document.getElementById("openCmdBtn")?.addEventListener("click", openCmdPalette);
  document.getElementById("cmdBackdrop")?.addEventListener("click", (e) => {
    if (e.target.id === "cmdBackdrop") closeCmdPalette();
  });
  document.getElementById("cmdInput")?.addEventListener("input", (e) => {
    state.cmdSelectedIndex = 0;
    renderCmdList(e.target.value);
  });

  // Global Keyboard Shortcuts
  window.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      state.cmdOpen ? closeCmdPalette() : openCmdPalette();
      return;
    }
    if (state.cmdOpen) {
      if (e.key === "Escape") {
        closeCmdPalette();
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        state.cmdSelectedIndex = (state.cmdSelectedIndex + 1) % Math.max(1, state.cmdFilteredItems.length);
        renderCmdList(document.getElementById("cmdInput")?.value || "");
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        state.cmdSelectedIndex =
          (state.cmdSelectedIndex - 1 + Math.max(1, state.cmdFilteredItems.length)) %
          Math.max(1, state.cmdFilteredItems.length);
        renderCmdList(document.getElementById("cmdInput")?.value || "");
      } else if (e.key === "Enter" && state.cmdFilteredItems[state.cmdSelectedIndex]) {
        e.preventDefault();
        const item = state.cmdFilteredItems[state.cmdSelectedIndex];
        closeCmdPalette();
        item.action();
      }
      return;
    }
    if (state.modalSystemSlug) {
      if (e.key === "Escape") closeSystemModal();
      if (e.key === "ArrowLeft") stepModalSystem(-1);
      if (e.key === "ArrowRight") stepModalSystem(1);
    }
  });
}

async function boot() {
  initTheme();
  const res = await fetch("data/portfolio.json");
  state.data = await res.json();

  readUrlState();
  bindGlobalEvents();

  renderRoleLens();
  renderFlagships();
  renderTraceLab();
  renderCatalogFilters();
  renderCatalog();
  renderDomainsGrid();

  if (state.modalSystemSlug) {
    openSystemModal(state.modalSystemSlug, "overview");
  }
}

boot();

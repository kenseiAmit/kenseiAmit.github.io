/* ==========================================================================
   Flagship Case Study Page Controller (/projects/<slug>/)
   Mermaid v11 Rendering · Theme Sync · TOC Scroll-Spy · Copy Utilities
   ========================================================================== */

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

async function renderMermaidBlocks() {
  const stages = document.querySelectorAll("[data-mermaid-src]");
  if (!stages.length) return;
  try {
    if (!mermaidMod) {
      const m = await import("https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs");
      mermaidMod = m.default;
    }
    const isDark = document.documentElement.getAttribute("data-theme") !== "light";
    mermaidMod.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: isDark ? "dark" : "default",
      fontFamily: "Inter, system-ui, sans-serif"
    });
    for (let i = 0; i < stages.length; i++) {
      const el = stages[i];
      const src = el.getAttribute("data-mermaid-src");
      if (!src) continue;
      const { svg } = await mermaidMod.render(`cs_mmd_${i}_${Date.now()}`, src);
      el.innerHTML = svg;
    }
  } catch {
    // Leaves preformatted Mermaid source intact if offline
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("ak_portfolio_theme", theme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
  renderMermaidBlocks();
}

function initScrollSpy() {
  const links = Array.from(document.querySelectorAll(".cs-toc-nav a"));
  const sections = links
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);
  if (!sections.length) return;

  const onScroll = () => {
    let activeIdx = 0;
    const offset = window.scrollY + 130;
    sections.forEach((sec, idx) => {
      if (sec.offsetTop <= offset) activeIdx = idx;
    });
    links.forEach((a, idx) => a.classList.toggle("active", idx === activeIdx));
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

function bootCaseStudy() {
  const saved = localStorage.getItem("ak_portfolio_theme");
  const initialTheme = saved === "light" || saved === "dark" ? saved : "dark";
  document.documentElement.setAttribute("data-theme", initialTheme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = initialTheme === "dark" ? "☀" : "☾";

  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "dark";
    applyTheme(cur === "dark" ? "light" : "dark");
  });

  document.getElementById("copyPageUrlBtn")?.addEventListener("click", () => {
    copyText(window.location.href, "Copied Case Study URL");
  });

  document.getElementById("flagshipSelect")?.addEventListener("change", (e) => {
    if (e.target.value) window.location.href = e.target.value;
  });

  document.querySelectorAll("[data-copy-target]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.getAttribute("data-copy-target"));
      if (target) copyText(target.textContent, btn.getAttribute("data-copy-label") || "Copied");
    });
  });

  initScrollSpy();
  renderMermaidBlocks();
}

bootCaseStudy();

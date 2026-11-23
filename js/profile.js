/* ==========================================================================
   AES-256-GCM Encrypted Executive Profile Controller (/profile/#k=...)
   Zero plaintext resume data in repository; unlocked strictly via URL fragment
   ========================================================================== */

let activeLenses = null;
let unlockedKey = null;

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

async function copyText(text, label = "Copied") {
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

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("ak_portfolio_theme", theme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
}

function b64ToBytes(b64) {
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr;
}

function extractKeyCandidate(raw) {
  const trimmed = String(raw || "").trim();
  if (!trimmed) return "";
  const hashIdx = trimmed.indexOf("#");
  if (hashIdx !== -1) {
    const hp = new URLSearchParams(trimmed.slice(hashIdx + 1));
    return hp.get("k") || hp.get("key") || "";
  }
  return trimmed;
}

function readFragmentKey() {
  if (!window.location.hash || window.location.hash.length < 2) return "";
  const hp = new URLSearchParams(window.location.hash.slice(1));
  return hp.get("k") || hp.get("key") || "";
}

async function decryptPayload(candidateKey) {
  const res = await fetch("../data/profile.enc.json", { cache: "no-cache" });
  if (!res.ok) throw new Error("Missing encrypted payload");
  const enc = await res.json();

  const salt = b64ToBytes(enc.salt);
  const iv = b64ToBytes(enc.iv);
  const ct = b64ToBytes(enc.ct);

  const baseKey = await window.crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(candidateKey),
    "PBKDF2",
    false,
    ["deriveKey"]
  );

  const aesKey = await window.crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: enc.iter, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["decrypt"]
  );

  const plainBuf = await window.crypto.subtle.decrypt(
    { name: "AES-GCM", iv },
    aesKey,
    ct
  );

  return JSON.parse(new TextDecoder().decode(plainBuf));
}

function applyLens(lensKey, pushState = true) {
  if (!activeLenses) return;
  const key = activeLenses[lensKey] ? lensKey : "unified";
  const cfg = activeLenses[key];

  const hl = document.getElementById("profHeadline");
  const sm = document.getElementById("profSummary");
  const hm = document.getElementById("hmRoleContext");
  if (hl) hl.textContent = cfg.headline;
  if (sm) sm.textContent = cfg.summary;
  if (hm) hm.textContent = cfg.hmContext;

  document.querySelectorAll("[data-lens]").forEach((btn) => {
    const active = btn.getAttribute("data-lens") === key;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-selected", String(active));
  });

  if (pushState && unlockedKey) {
    const params = new URLSearchParams(window.location.search);
    if (key === "unified") params.delete("lens");
    else params.set("lens", key);
    const qs = params.toString();
    window.history.replaceState(
      {},
      "",
      `${window.location.pathname}${qs ? `?${qs}` : ""}#k=${encodeURIComponent(unlockedKey)}`
    );
  }
}

function initScrollSpy() {
  const links = Array.from(document.querySelectorAll(".cs-toc-nav a"));
  const sections = links
    .map((a) => {
      const href = a.getAttribute("href");
      return href && href.startsWith("#") ? document.querySelector(href) : null;
    })
    .filter(Boolean);
  if (!sections.length) return;

  links.forEach((a) => {
    a.addEventListener("click", (e) => {
      const href = a.getAttribute("href");
      if (href && href.startsWith("#")) {
        e.preventDefault();
        document.querySelector(href)?.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

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

function mountDecryptedProfile(decrypted, keyUsed) {
  unlockedKey = keyUsed;
  activeLenses = decrypted.lenses;

  const gate = document.getElementById("restrictedGate");
  const root = document.getElementById("unlockedRoot");
  if (gate) gate.hidden = true;
  if (root) {
    root.innerHTML = decrypted.html;
    root.hidden = false;
  }

  const copyBtn = document.getElementById("copyProfileUrlBtn");
  const printBtn = document.getElementById("printCvBtn");
  if (copyBtn) copyBtn.hidden = false;
  if (printBtn) printBtn.hidden = false;

  document.title = "Amit Kumar Koshta — Executive Profile & Experience";

  document.querySelectorAll("[data-lens]").forEach((btn) => {
    btn.addEventListener("click", () => applyLens(btn.getAttribute("data-lens"), true));
  });

  const params = new URLSearchParams(window.location.search);
  const initialLens = params.get("lens") || "unified";
  applyLens(initialLens, true);
  initScrollSpy();
}

async function tryUnlock(candidateKey, showError = false) {
  const errEl = document.getElementById("gateError");
  if (errEl) errEl.hidden = true;
  try {
    const decrypted = await decryptPayload(candidateKey);
    mountDecryptedProfile(decrypted, candidateKey);
    return true;
  } catch {
    if (showError && errEl) errEl.hidden = false;
    return false;
  }
}

async function boot() {
  const saved = localStorage.getItem("ak_portfolio_theme");
  applyTheme(saved === "light" || saved === "dark" ? saved : "dark");

  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "dark";
    applyTheme(cur === "dark" ? "light" : "dark");
  });

  document.getElementById("copyProfileUrlBtn")?.addEventListener("click", () => {
    if (!unlockedKey) return;
    const url = `${window.location.origin}${window.location.pathname}${window.location.search}#k=${encodeURIComponent(unlockedKey)}`;
    copyText(url, "Copied private secret Profile URL");
  });

  document.getElementById("printCvBtn")?.addEventListener("click", () => {
    window.print();
  });

  document.getElementById("unlockForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const raw = document.getElementById("accessKeyInput")?.value || "";
    const key = extractKeyCandidate(raw);
    if (key) await tryUnlock(key, true);
  });

  const fragKey = readFragmentKey();
  if (fragKey) {
    await tryUnlock(fragKey, true);
  }
}

boot();

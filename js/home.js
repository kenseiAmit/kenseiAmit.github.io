/* ==========================================================================
   Lightweight Home Page Controller (/)
   Theme Toggle · Legacy Deep-Link Forwarding (?track= / ?system= -> /portfolio/)
   ========================================================================== */

const THEME_STORAGE_KEY = "ak_portfolio_theme_v2";

function applyTheme(theme, persist = true) {
  document.documentElement.setAttribute("data-theme", theme);
  if (persist) {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
}

function bootHome() {
  localStorage.removeItem("ak_portfolio_theme");
  const saved = localStorage.getItem(THEME_STORAGE_KEY);
  applyTheme(saved === "light" || saved === "dark" ? saved : "light", false);

  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    applyTheme(cur === "dark" ? "light" : "dark", true);
  });
}

bootHome();

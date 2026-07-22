const DESHARE_NAV = [
  {
    label: "Protocol",
    items: [
      ["overview", "Protocol overview", "index.html"],
      ["capabilities", "Capabilities & boundaries", "2-platform-features.html"],
      ["transactions", "Transaction lifecycle", "2-1-core-features.html"],
      ["asset-model", "Asset & custody model", "2-2-product-suite.html"],
      ["ipo-model", "IPO / Pre-IPO model", "2-3-ipo-investing.html"]
    ]
  },
  {
    label: "Architecture",
    items: [
      ["architecture", "System map", "3-architecture.html"],
      ["contracts-architecture", "Contract architecture", "3-1-technical-architecture.html"],
      ["order-lifecycle", "Order lifecycle", "3-2-protocol-mechanism.html"]
    ]
  },
  {
    label: "Verification",
    items: [
      ["security", "Security model", "4-security.html"],
      ["reserves", "Custody & reserves", "4-1-trusted-custody.html"],
      ["deployments", "Deployments", "4-2-deployments.html"],
      ["audit", "Security assessment", "4-3-security-audit.html"]
    ]
  },
  {
    label: "Developers",
    items: [
      ["developer", "Developer overview", "5-developer-docs.html"],
      ["api", "API reference", "5-1-api-reference.html"],
      ["contract-reference", "Contract & ABI", "5-2-contract-reference.html"],
      ["faq", "Operational FAQ", "5-faq.html"]
    ]
  },
  {
    label: "Offerings",
    items: [
      ["spacex-en", "Pre SpaceX · EN", "6-1-pre-spacex-en.html"],
      ["spacex-zh", "Pre SpaceX · 中文", "6-1-pre-spacex-zh.html"],
      ["anthropic-en", "Pre Anthropic · EN", "6-2-pre-anthropic-en.html"],
      ["anthropic-zh", "Pre Anthropic · 中文", "6-2-pre-anthropic-zh.html"],
      ["kimi-en", "Pre Kimi · EN", "6-3-pre-kimi-en.html"],
      ["kimi-zh", "Pre Kimi · 中文", "6-3-pre-kimi-zh.html"]
    ]
  },
  {
    label: "Legal",
    items: [
      ["terms", "Terms of Service", "terms.html"],
      ["privacy", "Privacy Policy", "privacy.html"]
    ]
  }
];

function renderNavigation() {
  const mount = document.querySelector("[data-site-nav]");
  if (!mount) return;
  const active = document.body.dataset.page;
  mount.innerHTML = DESHARE_NAV.map(group => `
    <section class="nav-group">
      <h2>${group.label}</h2>
      ${group.items.map(([key, label, href]) => `
        <a href="${href}" ${key === active ? 'aria-current="page"' : ""}>${label}</a>
      `).join("")}
    </section>
  `).join("");
}

function toggleMobileNavigation(force) {
  const button = document.querySelector("[data-nav-toggle]");
  const sidebar = document.querySelector("[data-sidebar]");
  if (!button || !sidebar) return;
  const open = typeof force === "boolean" ? force : button.getAttribute("aria-expanded") !== "true";
  button.setAttribute("aria-expanded", String(open));
  sidebar.dataset.open = String(open);
  document.body.classList.toggle("nav-open", open);
}

document.addEventListener("DOMContentLoaded", () => {
  renderNavigation();
  const button = document.querySelector("[data-nav-toggle]");
  if (button) button.addEventListener("click", () => toggleMobileNavigation());
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") toggleMobileNavigation(false);
  });
});

window.DESHARE_NAV = DESHARE_NAV;
window.renderNavigation = renderNavigation;
window.toggleMobileNavigation = toggleMobileNavigation;

/**
 * PERRITOS FELICES — Interactividad Endurecida (Zero-Trust DOM, CWV INP Optimization & WCAG 2.2)
 * Cumple OWASP ASVS & Modern Web Guidance: Cero uso de innerHTML/eval, Trusted Types ('pf-policy'),
 * creación segura de nodos con textContent/createElement, <dialog closedby="any"> y :user-invalid + aria-invalid.
 */

// Trusted Types Tinyfill & Policy ('pf-policy') para navegadores con y sin soporte nativo
if (!window.trustedTypes) {
  window.trustedTypes = {
    createPolicy: (name, rules) => ({
      createHTML: (s) => (rules.createHTML ? rules.createHTML(s) : s),
      createScriptURL: (s) => (rules.createScriptURL ? rules.createScriptURL(s) : s),
      createScript: (s) => (rules.createScript ? rules.createScript(s) : s)
    })
  };
}

if (window.trustedTypes && window.trustedTypes.createPolicy) {
  try {
    window.pfTrustedPolicy = window.trustedTypes.createPolicy("pf-policy", {
      createHTML: () => {
        throw new TypeError("[CSP Trusted Types] Asignación directa de HTML bloqueada por pf-policy. Usa createEl/textContent.");
      },
      createScriptURL: (url) => {
        const parsed = new URL(url, window.location.origin);
        if (parsed.origin === window.location.origin) {
          return parsed.href;
        }
        throw new TypeError(`[CSP Trusted Types] Script URL no autorizada: ${url}`);
      }
    });
  } catch (_) {
    // Política ya registrada
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initHeaderAndMobileNav();
  initToastSystem();
  initNewsletterForms();
  initHomePage();
  initBlogPage();
  initDirectoryPage();
  initArticlePage();
});

/* ==========================================================================
   Utilidades Seguras de Creación de Nodos DOM (Prevención total de XSS)
   ========================================================================== */
function createEl(tag, options = {}, children = []) {
  const node = document.createElement(tag);
  if (options.className) node.className = options.className;
  if (options.id) node.id = options.id;
  if (options.text !== undefined) node.textContent = String(options.text);
  if (options.style) node.setAttribute("style", options.style);
  if (options.attrs) {
    Object.entries(options.attrs).forEach(([k, v]) => {
      if (v !== undefined && v !== null) node.setAttribute(k, String(v));
    });
  }
  if (options.dataset) {
    Object.entries(options.dataset).forEach(([k, v]) => {
      if (v !== undefined && v !== null) node.dataset[k] = String(v);
    });
  }
  children.forEach((child) => {
    if (!child) return;
    if (typeof child === "string") {
      node.appendChild(document.createTextNode(child));
    } else {
      node.appendChild(child);
    }
  });
  return node;
}

function createSvgEl(tag, attrs = {}, children = []) {
  const ns = "http://www.w3.org/2000/svg";
  const el = document.createElementNS(ns, tag);
  Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, String(v)));
  children.forEach((c) => el.appendChild(c));
  return el;
}

const SAFE_SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*\.html$/i;
const SAFE_GRADIENT_PATTERN =
  /^linear-gradient\(\s*\d{1,3}deg\s*,\s*#[0-9a-fA-F]{3,8}\s+\d{1,3}%\s*,\s*#[0-9a-fA-F]{3,8}\s+\d{1,3}%\s*\)$/;
const FALLBACK_BG_GRADIENT = "linear-gradient(135deg, #FFBE58 0%, #FFE2AD 100%)";

function sanitizeString(input, maxLen = 120) {
  if (typeof input !== "string") return "";
  return input
    .replace(/[\u0000-\u001F\u007F\u202A-\u202E\u2066-\u2069]/g, "")
    .trim()
    .slice(0, maxLen);
}

function sanitizeArticleSlug(rawSlug) {
  const clean = sanitizeString(String(rawSlug || ""), 120);
  return SAFE_SLUG_PATTERN.test(clean) ? clean : "guia-alimentacion-natural-perros.html";
}

function sanitizeBgGradient(rawGradient) {
  const clean = sanitizeString(String(rawGradient || ""), 120);
  return SAFE_GRADIENT_PATTERN.test(clean) ? clean : FALLBACK_BG_GRADIENT;
}

/* ==========================================================================
   1. Header Sticky & Menú Móvil (Passive Scroll Listener para INP)
   ========================================================================== */
function initHeaderAndMobileNav() {
  const header = document.querySelector(".site-header");
  const mobileBtn = document.querySelector(".mobile-menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (header) {
    window.addEventListener(
      "scroll",
      () => {
        header.classList.toggle("scrolled", window.scrollY > 20);
      },
      { passive: true }
    );
  }

  if (mobileBtn && navLinks) {
    const closeMenu = () => {
      navLinks.classList.remove("open");
      mobileBtn.setAttribute("aria-expanded", "false");
    };

    mobileBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = navLinks.classList.toggle("open");
      mobileBtn.setAttribute("aria-expanded", String(isOpen));
    });

    // Cerrar al hacer clic en cualquier enlace de navegación
    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        closeMenu();
      });
    });

    // Cerrar al hacer clic fuera del menú o del header
    document.addEventListener("click", (e) => {
      if (navLinks.classList.contains("open") && !navLinks.contains(e.target) && !mobileBtn.contains(e.target)) {
        closeMenu();
      }
    });

    // Cerrar al presionar la tecla Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navLinks.classList.contains("open")) {
        closeMenu();
        mobileBtn.focus();
      }
    });
  }
}

/* ==========================================================================
   2. Sistema de Notificaciones Toast
   ========================================================================== */
let toastTimeout = null;
function initToastSystem() {
  if (!document.getElementById("pf-toast")) {
    const toast = createEl("div", {
      id: "pf-toast",
      className: "toast",
      attrs: { role: "status", "aria-live": "polite" }
    });
    document.body.appendChild(toast);
  }
}

window.showToast = function (message) {
  const toast = document.getElementById("pf-toast");
  if (!toast) return;
  toast.textContent = sanitizeString(message, 180);
  toast.classList.add("show");
  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 3600);
};

/* ==========================================================================
   3. Formularios de Newsletter y Sincronización Accesible (:user-invalid + aria-invalid)
   ========================================================================== */
function syncFormControlsAria(root = document) {
  const supportsUserInvalid =
    typeof CSS !== "undefined" && CSS.supports && CSS.supports("selector(:user-invalid)");
  const controls = root.querySelectorAll("input, textarea, select");

  controls.forEach((input) => {
    const syncAria = () => {
      if (!supportsUserInvalid) {
        input.classList.add("is-dirty");
      }
      const isInvalid = !input.validity.valid;
      input.setAttribute("aria-invalid", isInvalid ? "true" : "false");
    };

    input.addEventListener("blur", syncAria);
    input.addEventListener("input", () => {
      if (input.getAttribute("aria-invalid") === "true") {
        syncAria();
      }
    });
  });

  root.querySelectorAll("form").forEach((form) => {
    form.addEventListener("reset", () => {
      form.querySelectorAll("input, textarea, select").forEach((el) => {
        el.classList.remove("is-dirty");
        el.removeAttribute("aria-invalid");
      });
    });
  });
}

function initNewsletterForms() {
  syncFormControlsAria(document);

  const forms = document.querySelectorAll(".js-newsletter-form");
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      const email = sanitizeString(emailInput ? emailInput.value : "", 100);
      if (email && emailRegex.test(email)) {
        window.showToast(`[OK] Suscripción confirmada para ${email} — Guía enviada.`);
        form.reset();
      } else {
        if (emailInput) emailInput.setAttribute("aria-invalid", "true");
        window.showToast("[AVISO] Por favor ingresa un correo electrónico válido.");
      }
    });
  });
}

/* ==========================================================================
   4. View Transitions API (CSP-Safe & Reduced-Motion Aware) + Nodos SVG
   ========================================================================== */
function updateViewWithMotion(mutateDomCallback) {
  const prefersReducedMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!document.startViewTransition || prefersReducedMotion) {
    mutateDomCallback();
    return;
  }
  document.startViewTransition(() => {
    mutateDomCallback();
  });
}

function createCategorySvgNode(category) {
  const baseAttrs = {
    class: "article-svg-art",
    viewBox: "0 0 120 120",
    fill: "none",
    "aria-hidden": "true"
  };

  if (category === "Nutrición") {
    return createSvgEl("svg", baseAttrs, [
      createSvgEl("circle", { cx: 60, cy: 60, r: 46, stroke: "#10152B", "stroke-width": 2.5, fill: "#FFFFFF", pathLength: 1, class: "svg-draw-path" }),
      createSvgEl("circle", { cx: 60, cy: 60, r: 32, stroke: "#2241C8", "stroke-width": 2, "stroke-dasharray": "4 4" }),
      createSvgEl("path", { d: "M40 60 C40 46, 80 46, 80 60 C80 76, 40 76, 40 60 Z", fill: "#FFBE58", stroke: "#10152B", "stroke-width": 2 }),
      createSvgEl("circle", { cx: 52, cy: 58, r: 4, fill: "#2241C8" }),
      createSvgEl("circle", { cx: 68, cy: 62, r: 5, fill: "#10152B" })
    ]);
  }

  if (category === "Comportamiento") {
    return createSvgEl("svg", baseAttrs, [
      createSvgEl("rect", { x: 18, y: 18, width: 84, height: 84, rx: 12, fill: "#FFFFFF", stroke: "#10152B", "stroke-width": 2.5 }),
      createSvgEl("path", { d: "M28 65 Q45 30 60 65 T92 55", stroke: "#2241C8", "stroke-width": 3.5, fill: "none", pathLength: 1, class: "svg-draw-path" }),
      createSvgEl("circle", { cx: 45, cy: 48, r: 6, fill: "#FFBE58", stroke: "#10152B", "stroke-width": 2 }),
      createSvgEl("circle", { cx: 78, cy: 68, r: 6, fill: "#2241C8" })
    ]);
  }

  if (category === "Salud y Prevención") {
    return createSvgEl("svg", baseAttrs, [
      createSvgEl("circle", { cx: 60, cy: 60, r: 45, fill: "#FFFFFF", stroke: "#10152B", "stroke-width": 2.5, pathLength: 1, class: "svg-draw-path" }),
      createSvgEl("path", { d: "M52 36 H68 V52 H84 V68 H68 V84 H52 V68 H36 V52 H52 V36 Z", fill: "#2241C8", stroke: "#10152B", "stroke-width": 2 }),
      createSvgEl("circle", { cx: 60, cy: 60, r: 6, fill: "#FFBE58" })
    ]);
  }

  if (category === "Bienestar y Juegos") {
    return createSvgEl("svg", baseAttrs, [
      createSvgEl("circle", { cx: 60, cy: 60, r: 46, stroke: "#10152B", "stroke-width": 2, fill: "#FFFFFF", pathLength: 1, class: "svg-draw-path" }),
      createSvgEl("circle", { cx: 60, cy: 60, r: 32, stroke: "#2241C8", "stroke-width": 2 }),
      createSvgEl("circle", { cx: 60, cy: 60, r: 18, fill: "#FFBE58", stroke: "#10152B", "stroke-width": 2 }),
      createSvgEl("line", { x1: 60, y1: 8, x2: 60, y2: 112, stroke: "#10152B", "stroke-width": 1.5, "stroke-dasharray": "3 3" }),
      createSvgEl("line", { x1: 8, y1: 60, x2: 112, y2: 60, stroke: "#10152B", "stroke-width": 1.5, "stroke-dasharray": "3 3" })
    ]);
  }

  return createSvgEl("svg", baseAttrs, [
    createSvgEl("rect", { x: 20, y: 20, width: 80, height: 80, rx: 40, fill: "#FFFFFF", stroke: "#10152B", "stroke-width": 2.5, pathLength: 1, class: "svg-draw-path" }),
    createSvgEl("polygon", { points: "60,32 86,78 34,78", fill: "#FFBE58", stroke: "#10152B", "stroke-width": 2 }),
    createSvgEl("circle", { cx: 60, cy: 64, r: 6, fill: "#2241C8" })
  ]);
}

function createArticleCardNode(article, basePath = "articulos/", idx = 0) {
  const docNum = article.id ? sanitizeString(article.id, 24).replace("art-", "Guía #") : `Guía #0${idx + 1}`;
  const safeSlug = sanitizeArticleSlug(article.slug);
  const safeHref = `${basePath}${encodeURIComponent(safeSlug)}`;
  const safeGradient = sanitizeBgGradient(article.bgGradient);

  const thumbLink = createEl(
    "a",
    {
      className: "article-thumb",
      attrs: { href: safeHref },
      style: `background: ${safeGradient};`
    },
    [
      createEl("div", { className: "article-thumb-top" }, [
        createEl("span", { className: "article-doc-id", text: docNum }),
        createEl("span", { className: "badge badge-category", text: article.category })
      ]),
      createCategorySvgNode(article.category),
      createEl("div", {
        style: "font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: var(--ink-primary); z-index: 2;",
        text: `Por ${article.author}`
      })
    ]
  );

  const body = createEl("div", { className: "article-body" }, [
    createEl("div", { className: "article-meta" }, [
      createEl("span", { text: article.date }),
      createEl("span", { text: "•" }),
      createEl("span", { text: article.readTime })
    ]),
    createEl("h3", { className: "article-title" }, [
      createEl("a", { attrs: { href: safeHref }, text: article.title })
    ]),
    createEl("p", { className: "article-excerpt", text: article.excerpt }),
    createEl("a", { className: "article-readmore", attrs: { href: safeHref } }, [
      createEl("span", { text: "Leer guía paso a paso" }),
      createEl("span", { className: "arrow-diag", text: "↗" })
    ])
  ]);

  return createEl(
    "article",
    { className: "article-card reg-cross", dataset: { category: article.category } },
    [thumbLink, body]
  );
}

function createBusinessCardNode(biz, idx = 0) {
  const isOfficial = Boolean(biz.verified);
  const code = isOfficial
    ? (biz.id ? sanitizeString(biz.id, 24).replace("dir-", "Verificado #") : `Verificado #0${idx + 1}`)
    : "Postulación Local";
  const badgesWrap = createEl("div", { className: "business-badges" });

  if (isOfficial) {
    badgesWrap.appendChild(
      createEl("span", { className: "badge badge-verified" }, [
        createEl("span", { className: "led-dot led-green" }),
        " Trato Amable"
      ])
    );
  } else {
    badgesWrap.appendChild(
      createEl("span", { className: "badge badge-city" }, [
        createEl("span", { className: "led-dot led-gold" }),
        " En Revisión"
      ])
    );
  }
  badgesWrap.appendChild(createEl("span", { className: "badge badge-category", text: biz.category }));

  const highlightsWrap = createEl("div", {
    style: "display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:1rem;"
  });
  (biz.highlights || []).forEach((h) => {
    highlightsWrap.appendChild(createEl("span", { className: "badge badge-city", text: h }));
  });

  const topBlock = createEl("div", {}, [
    createEl("div", { className: "business-card-header" }, [
      createEl("span", { className: "business-code", text: code }),
      badgesWrap
    ]),
    createEl("h3", { className: "business-title", text: biz.name }),
    createEl("div", { className: "business-rating" }, [
      createEl("span", { className: "rating-pill", text: `★ ${Number(biz.rating).toFixed(1)} / 5.0` }),
      createEl("span", {
        style: "color: var(--ink-muted); font-weight: 500;",
        text: `(${Number(biz.reviews)} opiniones de familias)`
      })
    ]),
    createEl("p", { className: "business-desc", text: biz.description }),
    highlightsWrap
  ]);

  const contactBtn = createEl("button", {
    className: "btn btn-outline btn-sm js-contact-biz",
    attrs: { type: "button" },
    dataset: { name: biz.name, phone: biz.phone },
    text: "Ver teléfono"
  });
  contactBtn.addEventListener("click", () => {
    window.showToast(`Teléfono de ${biz.name}: ${biz.phone}`);
  });

  const mapUrl = `https://maps.google.com/?q=${encodeURIComponent(biz.name + " " + biz.address)}`;
  const mapLink = createEl(
    "a",
    {
      className: "btn btn-primary btn-sm",
      attrs: { href: mapUrl, target: "_blank", rel: "noopener noreferrer" }
    },
    ["Ver en Mapa ", createEl("span", { className: "arrow-diag", text: "↗" })]
  );

  const bottomBlock = createEl("div", {}, [
    createEl("div", { className: "business-meta" }, [
      createEl("span", {}, [
        createEl("strong", { className: "meta-key", text: "Ubicación:" }),
        ` ${biz.city} — ${biz.address}`
      ]),
      createEl("span", {}, [
        createEl("strong", { className: "meta-key", text: "Horario:" }),
        ` ${biz.hours}`
      ]),
      createEl("span", {}, [
        createEl("strong", { className: "meta-key", text: "Teléfono:" }),
        ` ${biz.phone}`
      ])
    ]),
    createEl("div", { className: "business-footer" }, [contactBtn, mapLink])
  ]);

  return createEl("article", { className: "business-card", dataset: { id: biz.id } }, [topBlock, bottomBlock]);
}

/* ==========================================================================
   5. Landing Page (index.html)
   ========================================================================== */
function initHomePage() {
  const homeDirectoryGrid = document.getElementById("home-directory-grid");
  const homeArticlesGrid = document.getElementById("home-articles-grid");

  if (!window.PERRITOS_DATA) return;

  if (homeDirectoryGrid) {
    const previewBiz = window.PERRITOS_DATA.directory.slice(0, 3);
    homeDirectoryGrid.replaceChildren(...previewBiz.map((b, i) => createBusinessCardNode(b, i)));
  }

  if (homeArticlesGrid) {
    const latestArticles = window.PERRITOS_DATA.articles.slice(0, 3);
    homeArticlesGrid.replaceChildren(...latestArticles.map((a, i) => createArticleCardNode(a, "articulos/", i)));
  }
}

/* ==========================================================================
   6. Blog Page (blog.html) con View Transitions API
   ========================================================================== */
function initBlogPage() {
  const blogGrid = document.getElementById("blog-posts-grid");
  const categoryPills = document.querySelectorAll(".js-category-pill");
  const searchInput = document.getElementById("blog-search-input");
  const countEl = document.getElementById("blog-results-count");

  if (!blogGrid || !window.PERRITOS_DATA) return;

  let activeCategory = "Todos";
  let searchQuery = "";

  function updateBlogGrid() {
    const filtered = window.PERRITOS_DATA.articles.filter((art) => {
      const matchesCategory = activeCategory === "Todos" || art.category === activeCategory;
      const q = searchQuery.toLowerCase();
      const matchesSearch =
        !q ||
        art.title.toLowerCase().includes(q) ||
        art.excerpt.toLowerCase().includes(q) ||
        art.category.toLowerCase().includes(q) ||
        art.author.toLowerCase().includes(q);
      return matchesCategory && matchesSearch;
    });

    if (countEl) {
      countEl.textContent = `Mostrando ${filtered.length} de ${window.PERRITOS_DATA.articles.length} guías prácticas`;
    }

    if (filtered.length === 0) {
      const resetBtn = createEl("button", {
        className: "btn btn-outline btn-sm",
        attrs: { type: "button" },
        text: "Ver todas las guías"
      });
      resetBtn.addEventListener("click", () => {
        activeCategory = "Todos";
        searchQuery = "";
        if (searchInput) searchInput.value = "";
        categoryPills.forEach((p) => p.classList.toggle("active", p.dataset.category === "Todos"));
        updateViewWithMotion(updateBlogGrid);
      });

      const emptyBox = createEl(
        "div",
        {
          style:
            "grid-column: 1 / -1; text-align:center; padding: 3rem; background: var(--surface-white); border-radius: var(--radius-md); border: 1.5px dashed var(--border-strong);"
        },
        [
          createEl("p", {
            className: "mono-label",
            style: "color: var(--logo-blue); margin-bottom: 0.5rem;",
            text: "SIN COINCIDENCIAS"
          }),
          createEl("h3", { style: "margin-bottom: 0.5rem;", text: "No encontramos guías con esa búsqueda" }),
          createEl("p", {
            style: "color: var(--ink-secondary); margin-bottom: 1.25rem;",
            text: "Intenta con otra palabra o vuelve a ver todas las guías disponibles."
          }),
          resetBtn
        ]
      );
      blogGrid.replaceChildren(emptyBox);
      return;
    }

    blogGrid.replaceChildren(...filtered.map((a, i) => createArticleCardNode(a, "articulos/", i)));
  }

  categoryPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      categoryPills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      activeCategory = pill.dataset.category || "Todos";
      updateViewWithMotion(updateBlogGrid);
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchQuery = sanitizeString(e.target.value, 80);
      updateBlogGrid();
    });
  }

  updateBlogGrid();
}

/* ==========================================================================
   7. Directorio Page (directorio.html) con Validación Estricta de Esquemas
   ========================================================================== */
const ALLOWED_CATEGORIES = [
  "Veterinaria y Salud",
  "Guardería y Hotel",
  "Estética y Spa",
  "Entrenamiento y Etología",
  "Nutrición y Tienda",
  "Cafés y Parques"
];

const ALLOWED_CITIES = [
  "Ciudad de Guatemala",
  "Antigua Guatemala",
  "Ciudad de México",
  "Guadalajara",
  "Monterrey",
  "Bogotá"
];

function loadValidatedCustomBusinesses() {
  try {
    const raw = JSON.parse(localStorage.getItem("pf_custom_businesses") || "[]");
    if (!Array.isArray(raw)) return [];
    return raw
      .filter((item) => Object.prototype.toString.call(item) === "[object Object]")
      .slice(0, 30)
      .map((item, idx) => ({
        id: sanitizeString(item.id || `dir-c${idx}`, 20),
        name: sanitizeString(item.name || "Centro Canino", 80),
        category: ALLOWED_CATEGORIES.includes(item.category) ? item.category : "Veterinaria y Salud",
        city: ALLOWED_CITIES.includes(item.city) ? item.city : "Ciudad de Guatemala",
        rating: Math.min(Math.max(Number(item.rating) || 5.0, 1.0), 5.0),
        reviews: Math.max(parseInt(item.reviews, 10) || 1, 1),
        verified: false, // Las postulaciones locales nunca falsifican el sello oficial verificado
        description: sanitizeString(item.description || "", 320),
        address: sanitizeString(item.address || "", 140),
        phone: sanitizeString(item.phone || "", 24),
        hours: sanitizeString(item.hours || "", 60),
        highlights: Array.isArray(item.highlights)
          ? item.highlights.slice(0, 4).map((h) => sanitizeString(h, 40))
          : ["Postulación en Revisión"]
      }));
  } catch {
    return [];
  }
}

function initDirectoryPage() {
  const dirGrid = document.getElementById("directory-full-grid");
  if (!dirGrid || !window.PERRITOS_DATA) return;

  const searchInput = document.getElementById("dir-search");
  const citySelect = document.getElementById("dir-city");
  const categorySelect = document.getElementById("dir-category");
  const ratingSelect = document.getElementById("dir-rating");
  const clearBtn = document.getElementById("dir-clear-btn");
  const countEl = document.getElementById("dir-results-count");

  let allBusinesses = [...loadValidatedCustomBusinesses(), ...window.PERRITOS_DATA.directory];

  function filterAndRenderDirectory() {
    const q = sanitizeString(searchInput?.value || "", 80).toLowerCase();
    const city = citySelect?.value || "Todas";
    const category = categorySelect?.value || "Todas";
    const minRating = parseFloat(ratingSelect?.value || "0");

    const filtered = allBusinesses.filter((biz) => {
      const matchesQ =
        !q ||
        biz.name.toLowerCase().includes(q) ||
        biz.description.toLowerCase().includes(q) ||
        biz.address.toLowerCase().includes(q) ||
        (biz.highlights || []).some((h) => h.toLowerCase().includes(q));
      const matchesCity = city === "Todas" || biz.city === city;
      const matchesCategory = category === "Todas" || biz.category === category;
      const matchesRating = biz.rating >= minRating;
      return matchesQ && matchesCity && matchesCategory && matchesRating;
    });

    if (countEl) {
      countEl.textContent = `MOSTRANDO ${filtered.length} ${
        filtered.length === 1 ? "ESPACIO VERIFICADO" : "ESPACIOS VERIFICADOS"
      }`;
    }

    if (filtered.length === 0) {
      const emptyNode = createEl(
        "div",
        {
          style:
            "grid-column: 1 / -1; text-align:center; padding: 3rem; background: var(--surface-white); border-radius: var(--radius-md); border: 1.5px dashed var(--border-strong);"
        },
        [
          createEl("p", {
            className: "mono-label",
            style: "color: var(--logo-blue); margin-bottom: 0.5rem;",
            text: "SIN RESULTADOS"
          }),
          createEl("h3", { style: "margin-bottom: 0.5rem;", text: "No encontramos centros con estos filtros" }),
          createEl("p", {
            style: "color: var(--ink-secondary);",
            text: "Prueba seleccionando todas las ciudades o limpia tu búsqueda para ver los espacios verificados."
          })
        ]
      );
      dirGrid.replaceChildren(emptyNode);
      return;
    }

    dirGrid.replaceChildren(...filtered.map((b, i) => createBusinessCardNode(b, i)));
  }

  if (searchInput) {
    searchInput.addEventListener("input", filterAndRenderDirectory);
  }
  [citySelect, categorySelect, ratingSelect].forEach((el) => {
    if (el) {
      el.addEventListener("change", () => {
        updateViewWithMotion(filterAndRenderDirectory);
      });
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      if (citySelect) citySelect.value = "Todas";
      if (categorySelect) categorySelect.value = "Todas";
      if (ratingSelect) ratingSelect.value = "0";
      updateViewWithMotion(filterAndRenderDirectory);
    });
  }

  // Modal de Registro de Negocio (<dialog closedby="any"> + fallback para navegadores sin closedBy)
  const openModalBtns = document.querySelectorAll(".js-open-register-modal");
  const modal = document.getElementById("register-business-modal");
  const closeModalBtn = document.getElementById("close-register-modal");
  const registerForm = document.getElementById("register-business-form");

  const openRegisterDialog = () => {
    if (!modal) return;
    if (typeof modal.showModal === "function") {
      if (!modal.open) modal.showModal();
    } else {
      modal.classList.add("open");
    }
  };

  const closeRegisterDialog = () => {
    if (!modal) return;
    if (typeof modal.close === "function" && modal.open) {
      modal.close();
    } else {
      modal.classList.remove("open");
    }
  };

  openModalBtns.forEach((btn) => {
    btn.addEventListener("click", openRegisterDialog);
  });

  if (closeModalBtn && modal) {
    closeModalBtn.addEventListener("click", closeRegisterDialog);

    // Fallback obligatorio para navegadores que aún no soportan 'closedby="any"' en HTMLDialogElement
    if (typeof HTMLDialogElement === "undefined" || !("closedBy" in HTMLDialogElement.prototype)) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          const rect = modal.getBoundingClientRect();
          const isInDialog =
            rect.top <= e.clientY &&
            e.clientY <= rect.top + rect.height &&
            rect.left <= e.clientX &&
            e.clientX <= rect.left + rect.width;
          if (!isInDialog) {
            closeRegisterDialog();
          }
        }
      });
    }
  }

  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);

      const rawName = sanitizeString(formData.get("bizName"), 80);
      const rawCat = String(formData.get("bizCategory") || "");
      const rawCity = String(formData.get("bizCity") || "");
      const rawDesc = sanitizeString(formData.get("bizDesc"), 320);
      const rawPhone = sanitizeString(formData.get("bizPhone"), 24);
      const rawHours = sanitizeString(formData.get("bizHours"), 60);
      const rawAddress = sanitizeString(formData.get("bizAddress"), 140);

      if (!rawName || !rawDesc || !rawAddress || !/^[0-9+\-\s()]{6,24}$/.test(rawPhone)) {
        window.showToast("[ERROR DE VALIDACIÓN] Verifica los datos y el formato telefónico.");
        return;
      }

      const newBiz = {
        id: "dir-" + String(allBusinesses.length + 1).padStart(2, "0"),
        name: rawName,
        category: ALLOWED_CATEGORIES.includes(rawCat) ? rawCat : "Veterinaria y Salud",
        city: ALLOWED_CITIES.includes(rawCity) ? rawCity : "Ciudad de Guatemala",
        rating: 5.0,
        reviews: 1,
        verified: false,
        description: rawDesc,
        address: rawAddress,
        phone: rawPhone,
        hours: rawHours || "Lun - Sáb: 9:00 AM a 6:00 PM",
        highlights: ["Postulación en Revisión", "Pendiente Auditoría"]
      };

      const existing = loadValidatedCustomBusinesses();
      existing.unshift(newBiz);
      localStorage.setItem("pf_custom_businesses", JSON.stringify(existing.slice(0, 30)));

      allBusinesses = [newBiz, ...allBusinesses];
      filterAndRenderDirectory();
      registerForm.reset();
      closeRegisterDialog();
      window.showToast(`[POSTULACIÓN RECIBIDA] ${newBiz.name} guardado en vista previa (En Revisión).`);
    });
  }

  filterAndRenderDirectory();
}

/* ==========================================================================
   8. Páginas de Artículo Individual (GPU transform scaleX, Passive Scroll, TOC & Share)
   ========================================================================== */
function initArticlePage() {
  const progressBar = document.getElementById("reading-progress-bar");
  const articleBody = document.querySelector(".article-content");

  if (progressBar && articleBody) {
    window.addEventListener(
      "scroll",
      () => {
        const rect = articleBody.getBoundingClientRect();
        const scrollTop = window.scrollY;
        const articleTop = rect.top + scrollTop;
        const articleHeight = articleBody.offsetHeight;
        const windowHeight = window.innerHeight;
        const maxScroll = Math.max(articleHeight - windowHeight * 0.5, 1);
        const current = Math.min(Math.max(scrollTop - articleTop + windowHeight * 0.25, 0), maxScroll);
        const ratio = (current / maxScroll).toFixed(4);
        progressBar.style.transform = `scaleX(${ratio})`;
      },
      { passive: true }
    );
  }

  const tocLinks = document.querySelectorAll(".toc-link");
  const headings = document.querySelectorAll(".article-content h2[id]");
  if (tocLinks.length > 0 && headings.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute("id");
            tocLinks.forEach((link) => {
              link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
            });
          }
        });
      },
      { rootMargin: "-100px 0px -65% 0px", threshold: 0.1 }
    );
    headings.forEach((h) => observer.observe(h));
  }

  const shareBtns = document.querySelectorAll(".js-share-btn");
  shareBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const network = btn.dataset.share;
      const url = window.location.protocol.startsWith("http")
        ? window.location.href
        : "https://www.perritosfelices.com/";
      const title = sanitizeString(document.title, 140);

      function openSafePopup(targetUrl) {
        const win = window.open(targetUrl, "_blank", "noopener,noreferrer");
        if (win) win.opener = null;
      }

      if (network === "whatsapp") {
        openSafePopup(`https://wa.me/?text=${encodeURIComponent(title + " " + url)}`);
      } else if (network === "twitter") {
        openSafePopup(
          `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`
        );
      } else if (network === "facebook") {
        openSafePopup(
          `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`
        );
      } else if (network === "copy") {
        if (navigator.clipboard) {
          navigator.clipboard.writeText(url).then(() => {
            window.showToast("[COPIADO] Enlace del artículo guardado en el portapapeles.");
          });
        } else {
          window.showToast("[OK] Enlace listo para compartir.");
        }
      }
    });
  });

  const relatedGrid = document.getElementById("related-articles-grid");
  if (relatedGrid && window.PERRITOS_DATA) {
    const currentSlug = window.location.pathname.split("/").pop();
    const currentArticle = window.PERRITOS_DATA.articles.find((a) => a.slug === currentSlug);
    const others = window.PERRITOS_DATA.articles.filter((a) => a.slug !== currentSlug);

    others.sort((a, b) => {
      const aMatch = currentArticle && a.category === currentArticle.category ? -1 : 1;
      const bMatch = currentArticle && b.category === currentArticle.category ? -1 : 1;
      return aMatch - bMatch;
    });

    const related = others.slice(0, 3);
    relatedGrid.replaceChildren(...related.map((a, i) => createArticleCardNode(a, "", i)));
  }
}

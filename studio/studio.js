/**
 * PERRITOS FELICES STUDIO — Cliente Visual Zero-Trust
 * Cumple OWASP ASVS & Trusted Types ('pf-policy'): Cero uso de innerHTML/outerHTML/eval.
 * Permite controlar Portada & Marketing, Guías por bloques, Calendario Editorial, Directorio y Compilación en 1 clic.
 */

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
        throw new TypeError("[CSP Trusted Types] Bloqueado por pf-policy.");
      },
      createScriptURL: (url) => {
        const parsed = new URL(url, window.location.origin);
        if (parsed.origin === window.location.origin) return parsed.href;
        throw new TypeError(`[CSP Trusted Types] Script URL no autorizada: ${url}`);
      }
    });
  } catch (_) {}
}

function el(tag, options = {}, children = []) {
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

const STUDIO_STATE = {
  articles: [],
  directory: [],
  calendar: [],
  marketing: {},
  selectedArticleSlug: null,
  selectedBizId: null
};

let toastTimer = null;
function showStudioToast(msg) {
  const t = document.getElementById("studio-toast");
  if (!t) return;
  t.textContent = String(msg || "");
  t.classList.add("show");
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 3600);
}

function logConsole(text) {
  const box = document.getElementById("console-output");
  if (!box) return;
  const now = new Date().toLocaleTimeString("es-GT");
  box.textContent = `[${now}] ${text}\n\n` + box.textContent;
}

function slugifyText(text) {
  const clean = String(text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return (clean || "nueva-guia") + ".html";
}

async function apiRequest(path, method = "GET", body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" }
  };
  if (body !== null) {
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(path, opts);
  const data = await res.json();
  if (!res.ok || data.error) {
    throw new Error(data.error || `Error HTTP ${res.status}`);
  }
  return data;
}

document.addEventListener("DOMContentLoaded", async () => {
  initNavigation();
  initTopbarButtons();
  initMarketingForm();
  initArticlesWorkspace();
  initCalendarWorkspace();
  initDirectoryWorkspace();
  initPreviewWorkspace();

  await loadAllStudioData();
});

async function loadAllStudioData() {
  try {
    const data = await apiRequest("/api/state");
    STUDIO_STATE.articles = data.articles || [];
    STUDIO_STATE.directory = data.directory || [];
    STUDIO_STATE.calendar = data.calendar || [];
    STUDIO_STATE.marketing = data.marketing || {};

    renderDashboardKpis();
    populateMarketingForm();
    renderArticlesList();
    renderCalendarKanban();
    renderDirectoryList();
    refreshPreviewArticleSelect();

    if (STUDIO_STATE.articles.length > 0 && !STUDIO_STATE.selectedArticleSlug) {
      selectArticleForEditing(STUDIO_STATE.articles[0].slug);
    }
    if (STUDIO_STATE.directory.length > 0 && !STUDIO_STATE.selectedBizId) {
      selectBizForEditing(STUDIO_STATE.directory[0].id);
    }
  } catch (err) {
    showStudioToast("Error cargando datos: " + err.message);
    logConsole("ERROR: " + err.message);
  }
}

/* ==========================================================================
   1. Navegación de Pestañas y Dashboard
   ========================================================================== */
const VIEW_META = {
  dashboard: { eyebrow: "CENTRO DE OPERACIONES EDITORIAL Y DISEÑO", title: "Resumen General del Sitio" },
  marketing: { eyebrow: "ESTRUCTURA DE CONVERSIÓN Y MARCA", title: "Portada Principal, Hero & Llamados a la Acción" },
  articles: { eyebrow: "BIBLIOTECA DE BIENESTAR CANINO", title: "Constructor Visual de Guías Paso a Paso" },
  calendar: { eyebrow: "ORGANIZACIÓN Y PLANIFICACIÓN SEO", title: "Calendario Editorial & Tablero de Ideas" },
  directory: { eyebrow: "RED DE CONFIANZA LIBRE DE JAULAS", title: "Directorio de Especialistas Verificados" },
  preview: { eyebrow: "VERIFICACIÓN MULTI-DISPOSITIVO", title: "Simulador Interactivo en Vivo" }
};

function switchStudioTab(tabId) {
  document.querySelectorAll(".nav-tab").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });
  document.querySelectorAll(".studio-view").forEach((sec) => {
    sec.classList.toggle("active", sec.id === `view-${tabId}`);
  });
  const meta = VIEW_META[tabId] || VIEW_META.dashboard;
  document.getElementById("current-view-eyebrow").textContent = meta.eyebrow;
  document.getElementById("current-view-title").textContent = meta.title;

  if (tabId === "preview") {
    const iframe = document.getElementById("studio-preview-iframe");
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.location.reload();
    }
  }
}

function initNavigation() {
  document.querySelectorAll(".nav-tab").forEach((btn) => {
    btn.addEventListener("click", () => switchStudioTab(btn.dataset.tab));
  });

  document.querySelectorAll(".action-tile").forEach((tile) => {
    tile.addEventListener("click", () => {
      const target = tile.dataset.goto;
      const act = tile.dataset.action;
      switchStudioTab(target);
      if (act === "new-article") startNewArticleForm();
      if (act === "new-biz") startNewBizForm();
    });
  });
}

function renderDashboardKpis() {
  const wrap = document.getElementById("dashboard-kpis");
  if (!wrap) return;
  const pendingIdeas = STUDIO_STATE.calendar.filter((c) => c.status !== "publicado").length;
  wrap.replaceChildren(
    el("div", { className: "kpi-card" }, [
      el("div", { className: "kpi-num", text: STUDIO_STATE.articles.length }),
      el("div", { className: "kpi-label", text: "GUÍAS PUBLICADAS" })
    ]),
    el("div", { className: "kpi-card" }, [
      el("div", { className: "kpi-num", text: STUDIO_STATE.directory.length }),
      el("div", { className: "kpi-label", text: "ESPECIALISTAS" })
    ]),
    el("div", { className: "kpi-card" }, [
      el("div", { className: "kpi-num", text: pendingIdeas }),
      el("div", { className: "kpi-label", text: "IDEAS EN COLA" })
    ])
  );
}

function initTopbarButtons() {
  document.getElementById("btn-build-now").addEventListener("click", async () => {
    try {
      showStudioToast("⚡ Compilando todo el sitio...");
      const res = await apiRequest("/api/build", "POST", {});
      logConsole(res.output || "Compilación completada.");
      showStudioToast("✔ Sitio compilado y actualizado con éxito.");
      await loadAllStudioData();
    } catch (err) {
      showStudioToast("❌ Error al compilar: " + err.message);
      logConsole("ERROR BUILD:\n" + err.message);
    }
  });

  document.getElementById("btn-audit-now").addEventListener("click", async () => {
    try {
      showStudioToast("🛡️ Ejecutando auditoría Zero-Trust...");
      const res = await apiRequest("/api/audit", "POST", {});
      logConsole(res.output || "Auditoría finalizada.");
      showStudioToast("🛡️ Auditoría completada: 0 vulnerabilidades.");
      switchStudioTab("dashboard");
    } catch (err) {
      showStudioToast("❌ Alerta en auditoría: " + err.message);
      logConsole("ALERTA AUDITORÍA:\n" + err.message);
    }
  });
}

/* ==========================================================================
   2. Editor de Portada y Marketing
   ========================================================================== */
const MARKETING_FIELDS = [
  "topbarRight",
  "heroTag",
  "heroCoords",
  "heroTitleMain",
  "heroTitleHighlight",
  "heroDescription",
  "heroBtnPrimary",
  "heroBtnSecondary",
  "stat1Number",
  "stat1Label",
  "stat2Number",
  "stat2Label",
  "stat3Number",
  "stat3Label",
  "newsletterTitle",
  "newsletterDescription",
  "newsletterBtn",
  "ctaBoxTag",
  "ctaBoxTitle",
  "ctaBoxDesc"
];

function populateMarketingForm() {
  const m = STUDIO_STATE.marketing || {};
  MARKETING_FIELDS.forEach((f) => {
    const input = document.getElementById(`mkt-${f}`);
    if (input && m[f] !== undefined) {
      input.value = m[f];
    }
  });
  const tickerInput = document.getElementById("mkt-tickerItems");
  if (tickerInput && Array.isArray(m.tickerItems)) {
    tickerInput.value = m.tickerItems.join(", ");
  }
  renderMarketingLivePreview();
}

function renderMarketingLivePreview() {
  const box = document.getElementById("marketing-live-preview");
  if (!box) return;
  const getVal = (id) => {
    const n = document.getElementById(`mkt-${id}`);
    return n ? n.value : "";
  };

  box.replaceChildren(
    el("div", { className: "preview-eyebrow", text: `● ${getVal("heroTag")} // ${getVal("heroCoords")}` }),
    el("div", { className: "preview-h1" }, [
      getVal("heroTitleMain") + " ",
      el("span", { className: "preview-highlight", text: getVal("heroTitleHighlight") })
    ]),
    el("p", { className: "preview-desc", text: getVal("heroDescription") }),
    el("div", { style: "display:flex; gap:0.5rem; flex-wrap:wrap;" }, [
      el("span", { className: "btn btn-primary btn-sm", text: getVal("heroBtnPrimary") + " ↗" }),
      el("span", { className: "btn btn-secondary btn-sm", text: getVal("heroBtnSecondary") + " ↗" })
    ]),
    el("div", { className: "preview-stats-mini" }, [
      el("div", { className: "preview-stat-box" }, [
        el("strong", { text: getVal("stat1Number") }),
        el("span", { text: getVal("stat1Label") })
      ]),
      el("div", { className: "preview-stat-box" }, [
        el("strong", { text: getVal("stat2Number") }),
        el("span", { text: getVal("stat2Label") })
      ]),
      el("div", { className: "preview-stat-box" }, [
        el("strong", { text: getVal("stat3Number") }),
        el("span", { text: getVal("stat3Label") })
      ])
    ])
  );
}

function initMarketingForm() {
  const form = document.getElementById("form-marketing");
  if (!form) return;

  form.addEventListener("input", () => renderMarketingLivePreview());

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {};
    MARKETING_FIELDS.forEach((f) => {
      const input = document.getElementById(`mkt-${f}`);
      payload[f] = input ? input.value.trim() : "";
    });
    const tickerRaw = document.getElementById("mkt-tickerItems").value;
    payload.tickerItems = tickerRaw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    try {
      showStudioToast("💾 Guardando portada y recompilando...");
      const res = await apiRequest("/api/marketing", "POST", payload);
      logConsole(res.output || "Portada actualizada.");
      showStudioToast("✔ Portada y textos de marketing actualizados en el sitio.");
      await loadAllStudioData();
    } catch (err) {
      showStudioToast("❌ Error guardando portada: " + err.message);
    }
  });
}

/* ==========================================================================
   3. Constructor Visual de Guías y Artículos
   ========================================================================== */
function parseHtmlBodyIntoSections(bodyHtml) {
  if (!bodyHtml || typeof bodyHtml !== "string") {
    return [createEmptySectionObj(1)];
  }
  const parser = new DOMParser();
  const doc = parser.parseFromString(`<div>${bodyHtml}</div>`, "text/html");
  const root = doc.body.firstChild;
  if (!root) return [createEmptySectionObj(1)];

  const sections = [];
  let current = null;

  Array.from(root.children).forEach((child) => {
    const tag = child.tagName.toUpperCase();
    if (tag === "H2") {
      if (current) sections.push(current);
      const rawTitle = child.textContent.replace(/^\d+\.\s*/, "").trim();
      current = {
        id: child.getAttribute("id") || "",
        heading: rawTitle,
        paragraphs: [],
        bullets: [],
        tipTitle: "🌿 Consejo práctico de bienestar",
        tip: "",
        tipType: "tip-sage"
      };
    } else {
      if (!current) {
        current = createEmptySectionObj(1);
      }
      if (tag === "P") {
        current.paragraphs.push(child.textContent.trim().replace(/\s+/g, " "));
      } else if (tag === "UL" || tag === "OL") {
        Array.from(child.querySelectorAll("li")).forEach((li) => {
          current.bullets.push(li.textContent.trim().replace(/\s+/g, " "));
        });
      } else if (tag === "DIV" && child.classList.contains("callout-box")) {
        current.tipType = child.classList.contains("alert-orange") ? "alert-orange" : "tip-sage";
        const strongEl = child.querySelector("strong");
        if (strongEl) {
          current.tipTitle = strongEl.textContent.trim();
        }
        const clone = child.cloneNode(true);
        const s = clone.querySelector("strong");
        if (s) s.remove();
        current.tip = clone.textContent.trim().replace(/\s+/g, " ");
      }
    }
  });

  if (current) sections.push(current);
  return sections.length > 0 ? sections : [createEmptySectionObj(1)];
}

function createEmptySectionObj(num = 1) {
  return {
    id: `seccion-${num}`,
    heading: "",
    paragraphs: [""],
    bullets: [],
    tipTitle: "🌿 Consejo práctico de bienestar",
    tip: "",
    tipType: "tip-sage"
  };
}

function renderSectionBuilderBlocks(sections) {
  const container = document.getElementById("article-sections-builder");
  if (!container) return;

  const nodes = sections.map((sec, idx) => {
    const blockCard = el("div", { className: "section-block-card", dataset: { index: idx } });

    const removeBtn = el("button", {
      className: "btn btn-danger btn-sm",
      attrs: { type: "button" },
      text: "Quitar sección"
    });
    removeBtn.addEventListener("click", () => {
      const currentData = collectSectionsFromBuilder();
      if (currentData.length <= 1) {
        showStudioToast("La guía debe tener al menos 1 sección.");
        return;
      }
      currentData.splice(idx, 1);
      renderSectionBuilderBlocks(currentData);
    });

    const header = el("div", { className: "section-block-header" }, [
      el("span", { className: "section-badge-num", text: `SECCIÓN ${idx + 1}` }),
      removeBtn
    ]);

    const headingInput = el("input", {
      className: "js-sec-heading",
      attrs: {
        type: "text",
        required: "true",
        placeholder: `Título del subtítulo ${idx + 1} (aparecerá en el Índice Lateral)`,
        value: sec.heading || ""
      }
    });
    headingInput.value = sec.heading || "";

    const paragraphsArea = el("textarea", {
      className: "js-sec-paragraphs",
      attrs: {
        rows: "4",
        placeholder: "Escribe los párrafos de esta sección (separa cada párrafo con una línea en blanco)..."
      }
    });
    paragraphsArea.value = (sec.paragraphs || []).join("\n\n");

    const bulletsArea = el("textarea", {
      className: "js-sec-bullets",
      attrs: {
        rows: "3",
        placeholder: "Opcional: escribe un punto clave por línea para crear una lista con viñetas..."
      }
    });
    bulletsArea.value = (sec.bullets || []).join("\n");

    const tipTypeSelect = el("select", { className: "js-sec-tiptype" }, [
      el("option", { attrs: { value: "tip-sage" }, text: "🌿 Recuadro Verde (Consejo Práctico)" }),
      el("option", { attrs: { value: "alert-orange" }, text: "⚠️ Recuadro Ámbar (Alerta / Precaución)" })
    ]);
    tipTypeSelect.value = sec.tipType || "tip-sage";

    const tipTitleInput = el("input", {
      className: "js-sec-tiptitle",
      attrs: {
        type: "text",
        placeholder: "Título del recuadro (ej: 🌿 Consejo práctico en casa)"
      }
    });
    tipTitleInput.value = sec.tipTitle || "🌿 Consejo práctico de bienestar";

    const tipTextInput = el("textarea", {
      className: "js-sec-tiptext",
      attrs: {
        rows: "2",
        placeholder: "Opcional: escribe aquí un consejo destacado para encerrarlo en una caja especial..."
      }
    });
    tipTextInput.value = sec.tip || "";

    blockCard.append(
      header,
      el("div", { className: "form-group" }, [
        el("label", { text: `Subtítulo H2 de la Sección ${idx + 1}` }),
        headingInput
      ]),
      el("div", { className: "form-group" }, [
        el("label", { text: "Párrafos Explicativos (separa párrafos con Enter doble)" }),
        paragraphsArea
      ]),
      el("div", { className: "form-group" }, [
        el("label", { text: "Lista de Puntos o Pasos (1 viñeta por línea — opcional)" }),
        bulletsArea
      ]),
      el("div", { className: "form-row two-cols" }, [
        el("div", { className: "form-group" }, [
          el("label", { text: "Estilo del Recuadro Destacado" }),
          tipTypeSelect
        ]),
        el("div", { className: "form-group" }, [
          el("label", { text: "Encabezado del Recuadro" }),
          tipTitleInput
        ])
      ]),
      el("div", { className: "form-group" }, [
        el("label", { text: "Texto del Recuadro Destacado (dejar vacío si no lleva recuadro)" }),
        tipTextInput
      ])
    );

    return blockCard;
  });

  container.replaceChildren(...nodes);
}

function collectSectionsFromBuilder() {
  const cards = document.querySelectorAll("#article-sections-builder .section-block-card");
  return Array.from(cards).map((card, idx) => {
    const heading = card.querySelector(".js-sec-heading").value.trim();
    const rawParas = card.querySelector(".js-sec-paragraphs").value;
    const paragraphs = rawParas
      .split(/\n\s*\n/)
      .map((p) => p.trim())
      .filter(Boolean);
    const rawBullets = card.querySelector(".js-sec-bullets").value;
    const bullets = rawBullets
      .split("\n")
      .map((b) => b.trim())
      .filter(Boolean);
    const tipType = card.querySelector(".js-sec-tiptype").value;
    const tipTitle = card.querySelector(".js-sec-tiptitle").value.trim();
    const tip = card.querySelector(".js-sec-tiptext").value.trim();

    return {
      id: `seccion-${idx + 1}`,
      heading: heading || `Sección ${idx + 1}`,
      paragraphs,
      bullets,
      tipType,
      tipTitle: tipTitle || "🌿 Consejo práctico de bienestar",
      tip
    };
  });
}

function renderArticlesList() {
  const listEl = document.getElementById("studio-articles-list");
  const countBadge = document.getElementById("articles-count-badge");
  const query = (document.getElementById("search-articles-studio").value || "").toLowerCase().trim();

  if (countBadge) countBadge.textContent = STUDIO_STATE.articles.length;
  if (!listEl) return;

  const filtered = STUDIO_STATE.articles.filter((a) => {
    if (!query) return true;
    return (
      a.title.toLowerCase().includes(query) ||
      a.category.toLowerCase().includes(query) ||
      a.slug.toLowerCase().includes(query)
    );
  });

  const nodes = filtered.map((art) => {
    const isSel = art.slug === STUDIO_STATE.selectedArticleSlug;
    const card = el(
      "div",
      { className: `studio-item-card${isSel ? " selected" : ""}` },
      [
        el("div", { className: "item-card-top" }, [
          el("span", { text: `${art.emoji || "🐾"} ${art.category}` }),
          el("span", { text: art.featured ? "⭐ DESTACADA" : art.date })
        ]),
        el("div", { className: "item-card-title", text: art.title }),
        el("div", { className: "item-card-sub", text: `/articulos/${art.slug}` })
      ]
    );
    card.addEventListener("click", () => selectArticleForEditing(art.slug));
    return card;
  });

  listEl.replaceChildren(...nodes);
}

function selectArticleForEditing(slug) {
  const art = STUDIO_STATE.articles.find((a) => a.slug === slug);
  if (!art) return;
  STUDIO_STATE.selectedArticleSlug = art.slug;
  renderArticlesList();

  document.getElementById("article-editor-heading").textContent = `✏️ Editando: ${art.title.slice(0, 42)}...`;
  document.getElementById("art-id").value = art.id || "";
  document.getElementById("art-title").value = art.title || "";
  document.getElementById("art-slug").value = art.slug || "";
  document.getElementById("art-category").value = art.category || "Bienestar y Juegos";
  document.getElementById("art-readTime").value = art.readTime || "7 min de lectura";
  document.getElementById("art-date").value = art.date || "";
  document.getElementById("art-author").value = art.author || "Equipo Editorial";
  document.getElementById("art-authorRole").value = art.authorRole || "Perritos Felices";
  document.getElementById("art-featured").checked = Boolean(art.featured);
  document.getElementById("art-excerpt").value = art.excerpt || "";
  document.getElementById("art-subtitle").value = art.subtitle || art.excerpt || "";

  const liveBtn = document.getElementById("btn-open-article-live");
  if (liveBtn) liveBtn.setAttribute("href", `/site/articulos/${encodeURIComponent(art.slug)}`);

  const parsedSections = parseHtmlBodyIntoSections(art.bodyHtml || "");
  renderSectionBuilderBlocks(parsedSections);
}

function startNewArticleForm(prefill = {}) {
  STUDIO_STATE.selectedArticleSlug = null;
  renderArticlesList();

  const nextNum = STUDIO_STATE.articles.length + 1;
  const months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
  const now = new Date();
  const todayStr = `${String(now.getDate()).padStart(2, "0")} ${months[now.getMonth()]} ${now.getFullYear()}`;

  document.getElementById("article-editor-heading").textContent = "✨ Crear Nueva Guía Paso a Paso";
  document.getElementById("art-id").value = `art-${String(nextNum).padStart(2, "0")}`;
  document.getElementById("art-title").value = prefill.title || "";
  document.getElementById("art-slug").value = prefill.title ? slugifyText(prefill.title) : "";
  document.getElementById("art-category").value = prefill.category || "Bienestar y Juegos";
  document.getElementById("art-readTime").value = "7 min de lectura";
  document.getElementById("art-date").value = todayStr;
  document.getElementById("art-author").value = "Equipo Editorial";
  document.getElementById("art-authorRole").value = "Perritos Felices";
  document.getElementById("art-featured").checked = false;
  document.getElementById("art-excerpt").value = prefill.excerpt || "";
  document.getElementById("art-subtitle").value = prefill.subtitle || "";

  renderSectionBuilderBlocks([
    {
      id: "seccion-1",
      heading: "Por qué es importante para el bienestar de tu perro",
      paragraphs: ["Escribe aquí la introducción empática y clara para la familia..."],
      bullets: ["Beneficio principal en casa", "Señal positiva a observar"],
      tipType: "tip-sage",
      tipTitle: "🌿 Consejo práctico de bienestar",
      tip: "Recuerda acompañar siempre con premios suaves y voz calmada."
    },
    {
      id: "seccion-2",
      heading: "Paso a paso para aplicarlo hoy mismo en casa",
      paragraphs: ["Explica aquí los pasos sencillos sin usar tecnicismos complicados..."],
      bullets: [],
      tipType: "tip-sage",
      tipTitle: "🌿 Consejo práctico de bienestar",
      tip: ""
    }
  ]);
}

function initArticlesWorkspace() {
  document.getElementById("search-articles-studio").addEventListener("input", () => renderArticlesList());

  document.getElementById("btn-new-article").addEventListener("click", () => startNewArticleForm());

  const titleInput = document.getElementById("art-title");
  const slugInput = document.getElementById("art-slug");
  titleInput.addEventListener("input", () => {
    if (!STUDIO_STATE.selectedArticleSlug) {
      slugInput.value = slugifyText(titleInput.value);
    }
  });

  document.getElementById("btn-add-section-block").addEventListener("click", () => {
    const current = collectSectionsFromBuilder();
    current.push(createEmptySectionObj(current.length + 1));
    renderSectionBuilderBlocks(current);
  });

  document.getElementById("form-article").addEventListener("submit", async (e) => {
    e.preventDefault();
    const sections = collectSectionsFromBuilder();
    const payload = {
      id: document.getElementById("art-id").value.trim(),
      title: document.getElementById("art-title").value.trim(),
      slug: document.getElementById("art-slug").value.trim(),
      category: document.getElementById("art-category").value,
      readTime: document.getElementById("art-readTime").value.trim(),
      date: document.getElementById("art-date").value.trim(),
      author: document.getElementById("art-author").value.trim(),
      authorRole: document.getElementById("art-authorRole").value.trim(),
      featured: document.getElementById("art-featured").checked,
      excerpt: document.getElementById("art-excerpt").value.trim(),
      subtitle: document.getElementById("art-subtitle").value.trim(),
      sections
    };

    try {
      showStudioToast("💾 Guardando guía y generando página HTML + SEO...");
      const res = await apiRequest("/api/article", "POST", payload);
      STUDIO_STATE.selectedArticleSlug = res.slug;
      logConsole(res.output || `Guía ${res.slug} guardada.`);
      showStudioToast("✔ Guía publicada y compilada en el sitio.");
      await loadAllStudioData();
    } catch (err) {
      showStudioToast("❌ Error guardando guía: " + err.message);
    }
  });
}

/* ==========================================================================
   4. Calendario Editorial Kanban
   ========================================================================== */
function renderCalendarKanban() {
  const board = document.getElementById("calendar-kanban");
  if (!board) return;

  const columns = [
    { key: "pendiente", label: "💡 Ideas Pendientes" },
    { key: "en_redaccion", label: "✍️ En Preparación" },
    { key: "publicado", label: "✅ Publicadas en el Blog" }
  ];

  const colNodes = columns.map((col) => {
    const items = STUDIO_STATE.calendar.filter((c) => (c.status || "pendiente") === col.key);
    const cardsWrap = el("div", { className: "kanban-cards" });

    items.forEach((item) => {
      const redactBtn = el("button", {
        className: "btn btn-primary btn-sm",
        attrs: { type: "button" },
        text: "✍️ Redactar Guía Ahora"
      });
      redactBtn.addEventListener("click", () => {
        switchStudioTab("articles");
        startNewArticleForm({
          title: item.title,
          category: item.category,
          excerpt: item.targetAudience || "",
          subtitle: item.targetAudience || ""
        });
        showStudioToast("Idea cargada en el constructor de guías.");
      });

      const statusSelect = el("select", { className: "btn btn-outline btn-sm" }, [
        el("option", { attrs: { value: "pendiente" }, text: "Estado: Pendiente" }),
        el("option", { attrs: { value: "en_redaccion" }, text: "Estado: En Preparación" }),
        el("option", { attrs: { value: "publicado" }, text: "Estado: Publicado" })
      ]);
      statusSelect.value = item.status || "pendiente";
      statusSelect.addEventListener("change", async () => {
        item.status = statusSelect.value;
        await saveCalendarState();
      });

      const delBtn = el("button", {
        className: "btn btn-danger btn-sm",
        attrs: { type: "button" },
        text: "🗑️"
      });
      delBtn.addEventListener("click", async () => {
        STUDIO_STATE.calendar = STUDIO_STATE.calendar.filter((c) => c.id !== item.id);
        await saveCalendarState();
      });

      cardsWrap.appendChild(
        el("div", { className: "kanban-card" }, [
          el("div", { className: "item-card-top" }, [
            el("span", { text: item.category || "General" }),
            el("span", { text: item.id || "" })
          ]),
          el("h4", { text: item.title }),
          el("p", { text: item.targetAudience || "Sin descripción de audiencia" }),
          el("div", { className: "kanban-actions" }, [redactBtn, statusSelect, delBtn])
        ])
      );
    });

    return el("div", { className: "kanban-col" }, [
      el("div", { className: "kanban-col-header" }, [
        el("span", { text: col.label }),
        el("span", { className: "badge-pill", style: "margin:0;", text: items.length })
      ]),
      cardsWrap
    ]);
  });

  board.replaceChildren(...colNodes);
}

async function saveCalendarState() {
  try {
    await apiRequest("/api/calendar", "POST", { calendar: STUDIO_STATE.calendar });
    showStudioToast("🗓️ Calendario editorial actualizado.");
    renderCalendarKanban();
    renderDashboardKpis();
  } catch (err) {
    showStudioToast("❌ Error en calendario: " + err.message);
  }
}

function initCalendarWorkspace() {
  const form = document.getElementById("form-calendar-idea");
  const btnOpen = document.getElementById("btn-new-calendar-idea");
  const btnCancel = document.getElementById("btn-cancel-idea");

  btnOpen.addEventListener("click", () => form.classList.remove("hidden"));
  btnCancel.addEventListener("click", () => form.classList.add("hidden"));

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nextNum = STUDIO_STATE.calendar.length + 1;
    const kwRaw = document.getElementById("cal-keywords").value;
    const newIdea = {
      id: `cal-0${nextNum}`,
      status: "pendiente",
      title: document.getElementById("cal-title").value.trim(),
      category: document.getElementById("cal-category").value,
      author: "Equipo Editorial",
      authorRole: "Perritos Felices",
      targetAudience: document.getElementById("cal-audience").value.trim(),
      keywords: kwRaw.split(",").map((k) => k.trim()).filter(Boolean)
    };
    STUDIO_STATE.calendar.unshift(newIdea);
    form.reset();
    form.classList.add("hidden");
    await saveCalendarState();
  });
}

/* ==========================================================================
   5. Directorio Canino Verificado
   ========================================================================== */
function renderDirectoryList() {
  const listEl = document.getElementById("studio-directory-list");
  const badge = document.getElementById("directory-count-badge");
  const query = (document.getElementById("search-directory-studio").value || "").toLowerCase().trim();

  if (badge) badge.textContent = STUDIO_STATE.directory.length;
  if (!listEl) return;

  const filtered = STUDIO_STATE.directory.filter((b) => {
    if (!query) return true;
    return (
      b.name.toLowerCase().includes(query) ||
      b.city.toLowerCase().includes(query) ||
      b.category.toLowerCase().includes(query)
    );
  });

  const nodes = filtered.map((biz) => {
    const isSel = biz.id === STUDIO_STATE.selectedBizId;
    const card = el(
      "div",
      { className: `studio-item-card${isSel ? " selected" : ""}` },
      [
        el("div", { className: "item-card-top" }, [
          el("span", { text: `${biz.emoji || "🏥"} ${biz.category}` }),
          el("span", { text: `★ ${Number(biz.rating).toFixed(1)}` })
        ]),
        el("div", { className: "item-card-title", text: biz.name }),
        el("div", { className: "item-card-sub", text: `📍 ${biz.city} — ${biz.phone}` })
      ]
    );
    card.addEventListener("click", () => selectBizForEditing(biz.id));
    return card;
  });

  listEl.replaceChildren(...nodes);
}

function selectBizForEditing(bizId) {
  const biz = STUDIO_STATE.directory.find((b) => b.id === bizId);
  if (!biz) return;
  STUDIO_STATE.selectedBizId = biz.id;
  renderDirectoryList();

  document.getElementById("biz-editor-heading").textContent = `🏥 Editando: ${biz.name}`;
  document.getElementById("biz-id").value = biz.id;
  document.getElementById("biz-name").value = biz.name || "";
  document.getElementById("biz-category").value = biz.category || "Veterinaria y Salud";
  document.getElementById("biz-city").value = biz.city || "Ciudad de Guatemala";
  document.getElementById("biz-phone").value = biz.phone || "";
  document.getElementById("biz-emoji").value = biz.emoji || "🏥";
  document.getElementById("biz-address").value = biz.address || "";
  document.getElementById("biz-hours").value = biz.hours || "";
  document.getElementById("biz-rating").value = biz.rating || 5.0;
  document.getElementById("biz-reviews").value = biz.reviews || 15;
  document.getElementById("biz-verified").checked = Boolean(biz.verified);
  document.getElementById("biz-description").value = biz.description || "";
  document.getElementById("biz-highlights").value = (biz.highlights || []).join(", ");

  document.getElementById("btn-delete-biz").classList.remove("hidden");
}

function startNewBizForm() {
  STUDIO_STATE.selectedBizId = null;
  renderDirectoryList();

  const nextNum = STUDIO_STATE.directory.length + 1;
  document.getElementById("biz-editor-heading").textContent = "✨ Registrar Nuevo Especialista en el Directorio";
  document.getElementById("biz-id").value = `dir-${String(nextNum).padStart(2, "0")}`;
  document.getElementById("biz-name").value = "";
  document.getElementById("biz-category").value = "Veterinaria y Salud";
  document.getElementById("biz-city").value = "Ciudad de Guatemala";
  document.getElementById("biz-phone").value = "+502 ";
  document.getElementById("biz-emoji").value = "🏥";
  document.getElementById("biz-address").value = "";
  document.getElementById("biz-hours").value = "Lun - Sáb: 8:00 AM a 6:00 PM";
  document.getElementById("biz-rating").value = "5.0";
  document.getElementById("biz-reviews").value = "15";
  document.getElementById("biz-verified").checked = true;
  document.getElementById("biz-description").value = "";
  document.getElementById("biz-highlights").value = "Certificación Fear Free, 100% Libre de Jaulas, Trato Amable";

  document.getElementById("btn-delete-biz").classList.add("hidden");
}

function initDirectoryWorkspace() {
  document.getElementById("search-directory-studio").addEventListener("input", () => renderDirectoryList());
  document.getElementById("btn-new-biz").addEventListener("click", () => startNewBizForm());

  document.getElementById("form-directory").addEventListener("submit", async (e) => {
    e.preventDefault();
    const highlights = document
      .getElementById("biz-highlights")
      .value.split(",")
      .map((h) => h.trim())
      .filter(Boolean);

    const payload = {
      id: document.getElementById("biz-id").value.trim(),
      name: document.getElementById("biz-name").value.trim(),
      category: document.getElementById("biz-category").value,
      city: document.getElementById("biz-city").value.trim(),
      phone: document.getElementById("biz-phone").value.trim(),
      emoji: document.getElementById("biz-emoji").value.trim(),
      address: document.getElementById("biz-address").value.trim(),
      hours: document.getElementById("biz-hours").value.trim(),
      rating: parseFloat(document.getElementById("biz-rating").value) || 5.0,
      reviews: parseInt(document.getElementById("biz-reviews").value, 10) || 10,
      verified: document.getElementById("biz-verified").checked,
      description: document.getElementById("biz-description").value.trim(),
      highlights
    };

    try {
      showStudioToast("💾 Guardando especialista en el Directorio...");
      const res = await apiRequest("/api/directory", "POST", payload);
      STUDIO_STATE.selectedBizId = res.id;
      logConsole(res.output || `Especialista ${payload.name} guardado.`);
      showStudioToast("✔ Directorio actualizado y compilado.");
      await loadAllStudioData();
    } catch (err) {
      showStudioToast("❌ Error en directorio: " + err.message);
    }
  });

  document.getElementById("btn-delete-biz").addEventListener("click", async () => {
    if (!STUDIO_STATE.selectedBizId) return;
    try {
      const res = await apiRequest("/api/directory/delete", "POST", { id: STUDIO_STATE.selectedBizId });
      STUDIO_STATE.selectedBizId = null;
      logConsole(res.output || "Registro eliminado.");
      showStudioToast("🗑️ Registro eliminado del directorio.");
      await loadAllStudioData();
    } catch (err) {
      showStudioToast("❌ Error al eliminar: " + err.message);
    }
  });
}

/* ==========================================================================
   6. Vista Previa Interactiva (Simulador Escritorio / Celular)
   ========================================================================== */
function refreshPreviewArticleSelect() {
  const sel = document.getElementById("preview-page-selector");
  if (!sel) return;
  const currentVal = sel.value;

  const baseOptions = [
    el("option", { attrs: { value: "/site/index.html" }, text: "🏠 Portada Principal (index.html)" }),
    el("option", { attrs: { value: "/site/blog.html" }, text: "📚 Archivo de Guías (blog.html)" }),
    el("option", { attrs: { value: "/site/directorio.html" }, text: "🏥 Directorio Canino (directorio.html)" })
  ];

  const artOptions = STUDIO_STATE.articles.map((a) =>
    el("option", {
      attrs: { value: `/site/articulos/${a.slug}` },
      text: `📄 Guía: ${a.title.slice(0, 48)}`
    })
  );

  sel.replaceChildren(...baseOptions, ...artOptions);
  if (currentVal) sel.value = currentVal;
}

function initPreviewWorkspace() {
  const sel = document.getElementById("preview-page-selector");
  const iframe = document.getElementById("studio-preview-iframe");
  const reloadBtn = document.getElementById("btn-reload-preview");

  sel.addEventListener("change", () => {
    iframe.setAttribute("src", sel.value);
  });

  reloadBtn.addEventListener("click", () => {
    if (iframe.contentWindow) iframe.contentWindow.location.reload();
  });

  document.querySelectorAll(".js-viewport-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".js-viewport-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      iframe.style.width = btn.dataset.vp;
    });
  });
}

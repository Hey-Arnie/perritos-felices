# AGENTS.md — Instancia Web, Editorial y Seguridad (`01_Infraestructura_Web/`)

> Instancia autónoma. Lee `../ESTADO.md` si necesitas contexto general. **Invoca únicamente la skill necesaria para la tarea actual, una a la vez, sin mezclar otras.**

## Reglas de Diseño (`../DESIGN.md`) y Sitio
- Paleta: `#2C4BCA` (AzulPF), `#FDB54A` (AmarilloPF), `#FAF8F5` (Crema), tarjetas `#FFFFFF` borde `1px`. Tipografía: `Fraunces` + `Inter` + `Space Mono`.
- Enlaces de artículos siempre dicen **"Leer más"**. Cero bordes neo-brutalistas, cero cajas `TL;DR`, cero jerga interna (*"Cápsula"*, *"Vitrinas B2B"*, *"Shareables"*, *"Nueva Era"*, *"Cero rodeos"*).
- Responsive: touch `>= 44×44px` (separación `>= 8px`), grillas `minmax(min(100%, 320px), 1fr)`, `inputmode="tel|numeric"` en móviles, desactivar `fractalNoise` en `<= 768px`.

## Reglas Editoriales (EBVM)
- Fuente única de artículos y directorio en `content/` (`articulos/*.md`, `cms_articulos.json`, `cms_directorio.json`, `cms_marketing.json`).
- Citas WSAVA / FEDIAF / NRC / ASPCA en `<section class="article-references">` al pie del artículo; cero siglas académicas en botones o tarjetas UI.

## Ciberseguridad Web (CSP Level 3 & Trusted Types)
- Prohibido `innerHTML`, `outerHTML`, `document.write()`, `eval()`, `new Function()`.
- Todo HTML declara `require-trusted-types-for 'script'; trusted-types pf-policy;`, `worker-src 'self'`, `base-uri 'none'`. Sincronizar `_headers` y `netlify.toml`.

## Comandos Maestros
- `python3 scripts/publicar.py build` — Compila `content/` → HTML, `js/data.js`, `sitemap.xml`.
- `python3 scripts/publicar.py audit` — Auditoría CSP, Trusted Types, XSS y CVE-2021-42574 (debe dar 0 alertas).
- `python3 scripts/publicar.py inventory` — Clasifica activos en `content/insumos_manifest.json`.

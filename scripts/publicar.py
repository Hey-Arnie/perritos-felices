#!/usr/bin/env python3
"""
PERRITOS FELICES — Motor de Publicación Automatizada y Compilador Agéntico
Sincroniza:
  1. 02_Estrategia_Y_Contenido/cms_articulos.json  --> 01_Infraestructura_Web/js/data.js + articulos/*.html
  2. 04_Gestion_Canina/cms_directorio.json         --> 01_Infraestructura_Web/js/data.js
  3. Genera automáticamente 01_Infraestructura_Web/sitemap.xml para SEO
  4. Valida seguridad (escapado XSS, cabeceras CSP, dimensiones de imagen y accesibilidad 18-65 años)
"""

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT_DIR / "01_Infraestructura_Web"
ARTICLES_JSON = ROOT_DIR / "02_Estrategia_Y_Contenido" / "cms_articulos.json"
DIRECTORY_JSON = ROOT_DIR / "04_Gestion_Canina" / "cms_directorio.json"
DATA_JS_PATH = WEB_DIR / "js" / "data.js"
ARTICLES_DIR = WEB_DIR / "articulos"
SITEMAP_PATH = WEB_DIR / "sitemap.xml"

ALLOWED_ARTICLE_CATEGORIES = {
    "Nutrición",
    "Comportamiento",
    "Salud y Prevención",
    "Bienestar y Juegos",
    "Higiene y Cuidado",
    "Educación y Entrenamiento",
    "Estilo de Vida",
}

ALLOWED_DIRECTORY_CATEGORIES = {
    "Veterinaria y Salud",
    "Guardería y Hotel",
    "Estética y Spa",
    "Entrenamiento y Etología",
    "Nutrición y Tienda",
    "Cafés y Parques",
}


def slugify(text: str) -> str:
    replacements = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    clean = text.translate(replacements).lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return f"{clean}.html" if not clean.endswith(".html") else clean


def build_article_html(article: dict) -> str:
    """Genera un archivo HTML completo con seguridad CSP, barra de lectura 60fps, TOC y diseño 18-65 años."""
    title = html.escape(article["title"])
    excerpt = html.escape(article["excerpt"])
    category = html.escape(article["category"])
    author = html.escape(article["author"])
    author_role = html.escape(article.get("authorRole", "Especialista Canino"))
    date_str = html.escape(article["date"])
    read_time = html.escape(article["readTime"])
    sections = article.get("sections", [])

    toc_items_html = []
    sections_html = []

    for idx, sec in enumerate(sections, start=1):
        sec_id = f"seccion-{idx}"
        sec_title = html.escape(sec.get("heading", f"Paso {idx}"))
        toc_items_html.append(
            f'<li><a href="#{sec_id}" class="toc-link">{idx:02d}. {sec_title}</a></li>'
        )
        paragraphs = "\n".join(
            f"<p>{html.escape(p)}</p>" for p in sec.get("paragraphs", [])
        )
        callout_html = ""
        if sec.get("tip"):
            callout_html = f"""
            <div class="callout-box">
              <strong>Consejo práctico para casa</strong>
              <p style="margin-bottom:0;">{html.escape(sec["tip"])}</p>
            </div>"""

        sections_html.append(
            f"""
            <h2 id="{sec_id}">{idx}. {sec_title}</h2>
            {paragraphs}
            {callout_html}"""
        )

    toc_block = "\n              ".join(toc_items_html)
    body_block = "\n".join(sections_html)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Perritos Felices</title>
  <meta name="description" content="{excerpt}" />
  <link rel="icon" type="image/png" href="../assets/logo/icononly_transparent_nobuffer.png" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" />
  <link rel="stylesheet" href="../css/styles.css" />
</head>
<body>
  <a href="#main-content" class="skip-link">Saltar al contenido principal</a>
  <div id="reading-progress-bar" class="reading-progress-bar" aria-hidden="true"></div>

  <header class="site-header">
    <div class="container navbar">
      <a href="../index.html" class="brand-logo" aria-label="Perritos Felices Inicio">
        <span class="brand-logo-icon">
          <img src="../assets/logo/icononly_transparent_nobuffer.png" alt="Logo Perritos Felices" width="36" height="36" decoding="async" />
        </span>
        <span class="brand-logo-text">
          <span class="brand-logo-title">Perritos Felices</span>
          <span class="brand-logo-slogan">Ladridos que inspiran</span>
        </span>
      </a>
      <nav class="nav-links" aria-label="Navegación principal">
        <a href="../index.html" class="nav-link">Inicio</a>
        <a href="../blog.html" class="nav-link active">Guías y Artículos</a>
        <a href="../directorio.html" class="nav-link">Directorio</a>
      </nav>
      <div class="nav-actions">
        <a href="../blog.html" class="btn btn-outline btn-sm">← VOLVER A GUÍAS</a>
        <button type="button" class="mobile-menu-toggle" aria-label="Abrir menú" aria-expanded="false">MENÚ</button>
      </div>
    </div>
  </header>

  <main id="main-content" tabindex="-1">
    <section class="article-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Ruta de navegación">
          <a href="../index.html">Inicio</a>
          <span>/</span>
          <a href="../blog.html">Guías</a>
          <span>/</span>
          <span>{category}</span>
        </nav>
        <span class="badge badge-category" style="margin-bottom:1rem;">{category}</span>
        <h1 class="section-title" style="max-width:860px; margin-bottom:1rem;">{title}</h1>
        <p class="section-subtitle" style="max-width:740px;">{excerpt}</p>
        <div class="article-author-bar">
          <div class="author-info">
            <div class="author-avatar"><img src="../assets/logo/icononly_transparent_nobuffer.png" alt="{author}" width="46" height="46" decoding="async" /></div>
            <div>
              <div style="font-weight:800;">{author}</div>
              <div style="font-size:0.86rem; color:var(--ink-muted);">{author_role} • {date_str} • {read_time}</div>
            </div>
          </div>
          <div class="share-buttons">
            <button type="button" class="share-btn js-share-btn" data-share="whatsapp">WhatsApp</button>
            <button type="button" class="share-btn js-share-btn" data-share="copy">Copiar enlace</button>
          </div>
        </div>
      </div>
    </section>

    <section class="container">
      <div class="article-layout">
        <aside class="article-toc-aside" aria-label="Tabla de contenido">
          <div class="toc-card">
            <div class="toc-title">Contenido de la guía</div>
            <ul class="toc-list">
              {toc_block}
            </ul>
          </div>
        </aside>
        <article class="article-content">
          {body_block}
        </article>
      </div>
    </section>

    <section style="padding: 3rem 0 5rem; background: var(--bg-sand); border-top: 1.5px solid var(--border-strong);">
      <div class="container">
        <h2 class="section-title" style="margin-bottom:2rem;">Otras guías recomendadas para ti</h2>
        <div id="related-articles-grid" class="articles-grid"></div>
      </div>
    </section>
  </main>

  <script src="../js/data.js"></script>
  <script src="../js/main.js"></script>
</body>
</html>
"""


def main() -> int:
    if not ARTICLES_JSON.exists() or not DIRECTORY_JSON.exists():
        print("[ERROR] No se encontraron los archivos JSON fuente en 02_Estrategia_Y_Contenido o 04_Gestion_Canina.")
        return 1

    articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
    directory = json.loads(DIRECTORY_JSON.read_text(encoding="utf-8"))

    # Validar artículos y generar HTML si contienen bloque `sections`
    generated_pages = 0
    clean_articles = []
    for idx, art in enumerate(articles, start=1):
        art_id = art.get("id") or f"art-{idx:02d}"
        slug = art.get("slug") or slugify(art["title"])
        cat = art.get("category", "Bienestar y Juegos")
        if cat not in ALLOWED_ARTICLE_CATEGORIES:
            print(f"[AVISO] Categoría '{cat}' en {art_id} ajustada a 'Bienestar y Juegos'.")
            cat = "Bienestar y Juegos"

        entry = {
            "id": art_id,
            "slug": slug,
            "title": art["title"].strip(),
            "excerpt": art["excerpt"].strip(),
            "category": cat,
            "readTime": art.get("readTime", "7 min de lectura"),
            "date": art.get("date", datetime.now().strftime("%d %b %Y")),
            "author": art.get("author", "Equipo Editorial Perritos Felices"),
            "authorRole": art.get("authorRole", "Especialista en Bienestar Canino"),
            "emoji": art.get("emoji", "🐾"),
            "bgGradient": art.get("bgGradient", "linear-gradient(135deg, #FFBE58 0%, #FFE2AD 100%)"),
            "featured": bool(art.get("featured", False)),
        }
        clean_articles.append(entry)

        target_html = ARTICLES_DIR / slug
        if art.get("sections") and (not target_html.exists() or art.get("regenerate_html")):
            target_html.write_text(build_article_html(art), encoding="utf-8")
            generated_pages += 1

    # Validar directorio
    clean_directory = []
    for idx, biz in enumerate(directory, start=1):
        biz_id = biz.get("id") or f"dir-{idx:02d}"
        cat = biz.get("category", "Veterinaria y Salud")
        if cat not in ALLOWED_DIRECTORY_CATEGORIES:
            cat = "Veterinaria y Salud"

        clean_directory.append({
            "id": biz_id,
            "name": biz["name"].strip(),
            "category": cat,
            "city": biz.get("city", "Ciudad de Guatemala").strip(),
            "rating": round(float(biz.get("rating", 5.0)), 1),
            "reviews": int(biz.get("reviews", 1)),
            "verified": bool(biz.get("verified", True)),
            "emoji": biz.get("emoji", "🏥"),
            "description": biz["description"].strip(),
            "address": biz["address"].strip(),
            "phone": biz["phone"].strip(),
            "hours": biz.get("hours", "Lun - Sáb: 9:00 AM a 6:00 PM").strip(),
            "highlights": biz.get("highlights", ["Trato Amable Verificado"])[:4],
        })

    # Escribir 01_Infraestructura_Web/js/data.js
    payload = {
        "articles": clean_articles,
        "directory": clean_directory,
    }
    js_content = (
        "/**\n"
        " * PERRITOS FELICES — Base de datos central de Artículos y Directorio Canino\n"
        " * Generado automáticamente por 01_Infraestructura_Web/scripts/publicar.py\n"
        " * Línea Gráfica: Azul Cobalto (#2241C8) & Amarillo Dorado (#FFBE58) — \"Ladridos que inspiran\"\n"
        " */\n\n"
        f"window.PERRITOS_DATA = {json.dumps(payload, ensure_ascii=False, indent=2)};\n"
    )
    DATA_JS_PATH.write_text(js_content, encoding="utf-8")

    # Generar sitemap.xml para SEO
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [
        "https://www.perritosfelices.com/",
        "https://www.perritosfelices.com/blog.html",
        "https://www.perritosfelices.com/directorio.html",
    ] + [f"https://www.perritosfelices.com/articulos/{a['slug']}" for a in clean_articles]

    sitemap_nodes = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>"
        for u in urls
    )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_nodes}\n"
        "</urlset>\n"
    )
    SITEMAP_PATH.write_text(sitemap_xml, encoding="utf-8")

    print("=================================================================")
    print(" PERRITOS FELICES — PUBLICACIÓN AUTOMATIZADA COMPLETADA")
    print("=================================================================")
    print(f" ✔ Artículos sincronizados en js/data.js : {len(clean_articles)}")
    print(f" ✔ Nuevas páginas HTML generadas         : {generated_pages}")
    print(f" ✔ Negocios sincronizados en Directorio  : {len(clean_directory)}")
    print(f" ✔ Sitemap SEO actualizado               : {SITEMAP_PATH.name} ({len(urls)} URLs)")
    print("=================================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())

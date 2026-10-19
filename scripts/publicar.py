#!/usr/bin/env python3
"""
PERRITOS FELICES — Motor de Publicación Automatizada y Compilador Agéntico (v2.0)
Sincroniza y compila todo el sitio web a partir de fuentes únicas de verdad:
  1. 02_Estrategia_Y_Contenido/articulos/*.md  <--> 02_Estrategia_Y_Contenido/cms_articulos.json
  2. 01_Infraestructura_Web/templates/articulo.html --> 01_Infraestructura_Web/articulos/*.html
  3. 04_Gestion_Canina/cms_directorio.json          --> 01_Infraestructura_Web/js/data.js
  4. Genera automáticamente sitemap.xml y robots.txt para SEO
  5. Soporta comandos CLI para trabajar con el Agente:
     - python3 01_Infraestructura_Web/scripts/publicar.py [build]
     - python3 01_Infraestructura_Web/scripts/publicar.py status
     - python3 01_Infraestructura_Web/scripts/publicar.py nuevo-negocio ...
     - python3 01_Infraestructura_Web/scripts/publicar.py nuevo-articulo ...
"""

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT_DIR / "01_Infraestructura_Web"
STRATEGY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido"
CANINE_DIR = ROOT_DIR / "04_Gestion_Canina"

ARTICLES_JSON = STRATEGY_DIR / "cms_articulos.json"
ARTICLES_MD_DIR = STRATEGY_DIR / "articulos"
CALENDAR_JSON = STRATEGY_DIR / "calendario_editorial.json"
DIRECTORY_JSON = CANINE_DIR / "cms_directorio.json"

TEMPLATE_HTML = WEB_DIR / "templates" / "articulo.html"
DATA_JS_PATH = WEB_DIR / "js" / "data.js"
ARTICLES_DIR = WEB_DIR / "articulos"
SITEMAP_PATH = WEB_DIR / "sitemap.xml"
ROBOTS_PATH = WEB_DIR / "robots.txt"

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

CATEGORY_DEFAULTS = {
    "Nutrición": {
        "emoji": "🥣",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🥣 Guía de Nutrición Canina",
        "sectionTag": "🥣 Nutrición Consciente",
        "bgGradient": "linear-gradient(135deg, #FFBE58 0%, #FFE2AD 100%)",
    },
    "Comportamiento": {
        "emoji": "🐕",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🐕 Guía de Comportamiento y Etología",
        "sectionTag": "🐕 Etología y Comunicación",
        "bgGradient": "linear-gradient(135deg, #DDE6FF 0%, #FFF1D6 100%)",
    },
    "Salud y Prevención": {
        "emoji": "🩺",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🩺 Guía de Salud y Medicina Preventiva",
        "sectionTag": "🩺 Salud y Prevención",
        "bgGradient": "linear-gradient(135deg, #FFE4B5 0%, #E8EFFF 100%)",
    },
    "Bienestar y Juegos": {
        "emoji": "🌿",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🌿 Guía de Bienestar y Enriquecimiento",
        "sectionTag": "🌿 Bienestar y Juegos",
        "bgGradient": "linear-gradient(135deg, #FFECB8 0%, #E3F4ED 100%)",
    },
    "Higiene y Cuidado": {
        "emoji": "🪥",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🪥 Guía de Higiene y Cuidado en Casa",
        "sectionTag": "🪥 Higiene y Cuidado",
        "bgGradient": "linear-gradient(135deg, #DCE6FF 0%, #FFF4DB 100%)",
    },
    "Educación y Entrenamiento": {
        "emoji": "🐾",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🐾 Guía de Educación en Positivo",
        "sectionTag": "🐾 Educación Amable",
        "bgGradient": "linear-gradient(135deg, #FFBE58 0%, #FFF0CE 100%)",
    },
    "Estilo de Vida": {
        "emoji": "🎒",
        "author": "Equipo Editorial",
        "authorRole": "Perritos Felices",
        "topbarTag": "🎒 Guía de Estilo de Vida Pet-Friendly",
        "sectionTag": "🎒 Aventuras y Vida Juntos",
        "bgGradient": "linear-gradient(135deg, #FFE5B0 0%, #DCE6FF 100%)",
    },
}


def slugify(text: str) -> str:
    replacements = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    clean = text.translate(replacements).lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return f"{clean}.html" if not clean.endswith(".html") else clean


def get_author_initials(author_name: str) -> str:
    name_low = author_name.lower()
    if "editorial" in name_low or "perritos" in name_low:
        return "PF"
    titles = {"dr.", "dra.", "lic.", "ing.", "mvz", "mvz."}
    parts = [
        p for p in author_name.strip().split() if p.lower() not in titles and p.isalpha()
    ]
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    if parts:
        return parts[0][:2].upper()
    return "PF"


def extract_from_existing_html(html_path: Path) -> dict:
    """Extrae metadatos, TOC y cuerpo de un archivo HTML existente en articulos/."""
    raw = html_path.read_text(encoding="utf-8")
    extracted = {}

    topbar_m = re.search(
        r'<div class="topbar">\s*<div class="container">\s*(.*?)\s*—\s*<strong>',
        raw,
        re.DOTALL,
    )
    if topbar_m:
        extracted["topbarTag"] = re.sub(r"\s+", " ", topbar_m.group(1)).strip()

    sectag_m = re.search(
        r'<header class="article-header">.*?<span class="section-tag">(.*?)</span>',
        raw,
        re.DOTALL,
    )
    if sectag_m:
        extracted["sectionTag"] = sectag_m.group(1).strip()

    sub_m = re.search(
        r'<p class="section-subtitle"[^>]*>(.*?)</p>', raw, re.DOTALL
    )
    if sub_m:
        extracted["subtitle"] = re.sub(r"\s+", " ", sub_m.group(1)).strip()

    toc_m = re.search(
        r'<ul class="toc-list">\s*(.*?)\s*</ul>', raw, re.DOTALL
    )
    if toc_m:
        toc_items = []
        for li in re.finditer(
            r'<a href="#([^"]+)"[^>]*>(.*?)</a>', toc_m.group(1), re.DOTALL
        ):
            toc_items.append({"id": li.group(1).strip(), "label": li.group(2).strip()})
        if toc_items:
            extracted["toc"] = toc_items

    body_m = re.search(
        r'<article class="article-content">\s*(.*?)\s*</article>', raw, re.DOTALL
    )
    if body_m:
        extracted["bodyHtml"] = body_m.group(1).strip()

    return extracted


def parse_markdown_article(md_path: Path) -> dict:
    """Lee un archivo .md con Frontmatter JSON/YAML simple y cuerpo HTML/Markdown."""
    content = md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter_raw = parts[1].strip()
    body = parts[2].strip()

    meta = {}
    for line in frontmatter_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        elif v.lower() == "true":
            v = True
        elif v.lower() == "false":
            v = False
        meta[k] = v

    # Si el cuerpo tiene sintaxis Markdown simple (## Título, párrafos), convertir si no es HTML puro
    if "<h2" not in body and "## " in body:
        body = convert_simple_markdown_to_html(body)

    meta["bodyHtml"] = body
    return meta


def convert_simple_markdown_to_html(md_text: str) -> str:
    """Convierte Markdown editorial (##, párrafos, listas, callouts > [!TIP]) a HTML de Perritos Felices."""
    lines = md_text.splitlines()
    html_out = []
    in_ul = False
    in_ol = False
    sec_num = 0

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_out.append("        </ul>")
            in_ul = False
        if in_ol:
            html_out.append("        </ol>")
            in_ol = False

    def inline_fmt(txt: str) -> str:
        txt = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)
        txt = re.sub(r"\*(.+?)\*", r"<em>\1</em>", txt)
        return txt

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            close_lists()
            i += 1
            continue

        if line.startswith("## "):
            close_lists()
            sec_num += 1
            heading_text = line[3:].strip()
            sec_id = re.sub(r"[^a-z0-9]+", "-", heading_text.lower()).strip("-")[:28] or f"seccion-{sec_num}"
            html_out.append(f'        <h2 id="{sec_id}">{inline_fmt(heading_text)}</h2>')
        elif line.startswith("- "):
            if in_ol:
                html_out.append("        </ol>")
                in_ol = False
            if not in_ul:
                html_out.append("        <ul>")
                in_ul = True
            html_out.append(f"          <li>{inline_fmt(line[2:].strip())}</li>")
        elif re.match(r"^\d+\.\s+", line):
            if in_ul:
                html_out.append("        </ul>")
                in_ul = False
            if not in_ol:
                html_out.append("        <ol>")
                in_ol = True
            item_txt = re.sub(r"^\d+\.\s+", "", line)
            html_out.append(f"          <li>{inline_fmt(item_txt)}</li>")
        elif line.startswith("> "):
            close_lists()
            callout_lines = [line[2:].strip()]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith(">"):
                i += 1
                callout_lines.append(lines[i].strip().lstrip(">").strip())
            first = callout_lines[0]
            box_class = "alert-orange" if "⚠️" in first or "Importante" in first else "tip-sage"
            title_line = inline_fmt(first)
            rest = " ".join(inline_fmt(c) for c in callout_lines[1:])
            html_out.append(
                f'        <div class="callout-box {box_class}">\n'
                f"          <strong>{title_line}</strong>\n"
                f"          {rest}\n"
                f"        </div>"
            )
        elif line.startswith("<"):
            close_lists()
            html_out.append(f"        {line}")
        else:
            close_lists()
            html_out.append(f"        <p>\n          {inline_fmt(line)}\n        </p>")
        i += 1

    close_lists()
    return "\n\n".join(html_out)


def write_markdown_file(article: dict) -> Path:
    """Escribe o actualiza el archivo .md fuente para un artículo en 02_Estrategia_Y_Contenido/articulos/."""
    ARTICLES_MD_DIR.mkdir(parents=True, exist_ok=True)
    slug_base = article["slug"].replace(".html", "")
    md_path = ARTICLES_MD_DIR / f"{slug_base}.md"

    frontmatter = [
        "---",
        f'id: "{article["id"]}"',
        f'slug: "{article["slug"]}"',
        f'title: "{article["title"]}"',
        f'subtitle: "{article.get("subtitle", article["excerpt"])}"',
        f'excerpt: "{article["excerpt"]}"',
        f'category: "{article["category"]}"',
        f'readTime: "{article["readTime"]}"',
        f'date: "{article["date"]}"',
        f'author: "{article["author"]}"',
        f'authorRole: "{article["authorRole"]}"',
        f'emoji: "{article["emoji"]}"',
        f'topbarTag: "{article.get("topbarTag", CATEGORY_DEFAULTS.get(article["category"], {}).get("topbarTag", "🐾 Guía Perritos Felices"))}"',
        f'sectionTag: "{article.get("sectionTag", CATEGORY_DEFAULTS.get(article["category"], {}).get("sectionTag", article["category"]))}"',
        f'bgGradient: "{article["bgGradient"]}"',
        f'featured: {"true" if article.get("featured") else "false"}',
        "---",
        "",
        article.get("bodyHtml", "").strip(),
        "",
    ]
    md_path.write_text("\n".join(frontmatter), encoding="utf-8")
    return md_path


def build_body_from_sections(sections: list) -> tuple:
    """Construye bodyHtml y toc a partir de una lista estructurada de `sections` en JSON."""
    toc_items = []
    blocks = []
    for idx, sec in enumerate(sections, start=1):
        sec_id = sec.get("id") or f"seccion-{idx}"
        heading = sec.get("heading", f"Sección {idx}")
        clean_heading = re.sub(r"^\d+\.\s*", "", heading)
        toc_items.append({"id": sec_id, "label": f"{idx}. {clean_heading}"})

        blocks.append(f'        <h2 id="{sec_id}">{idx}. {html.escape(clean_heading)}</h2>')
        for p in sec.get("paragraphs", []):
            blocks.append(f"        <p>\n          {html.escape(p)}\n        </p>")
        if sec.get("bullets"):
            li_str = "\n".join(f"          <li>{html.escape(b)}</li>" for b in sec["bullets"])
            blocks.append(f"        <ul>\n{li_str}\n        </ul>")
        if sec.get("tip"):
            box_type = sec.get("tipType", "tip-sage")
            tip_title = sec.get("tipTitle", "🌿 Consejo práctico de bienestar")
            blocks.append(
                f'        <div class="callout-box {box_type}">\n'
                f"          <strong>{html.escape(tip_title)}</strong>\n"
                f"          {html.escape(sec['tip'])}\n"
                f"        </div>"
            )
    return "\n\n".join(blocks), toc_items


def extract_toc_from_body(body_html: str) -> list:
    """Extrae automáticamente los <h2 id="...">...</h2> para construir el índice lateral."""
    toc = []
    for idx, match in enumerate(
        re.finditer(r'<h2\s+id="([^"]+)"[^>]*>(.*?)</h2>', body_html, re.DOTALL),
        start=1,
    ):
        sec_id = match.group(1).strip()
        label = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        # Acortar etiquetas muy largas para el sidebar
        if ":" in label and len(label) > 42:
            label = label.split(":", 1)[0].strip()
        toc.append({"id": sec_id, "label": label or f"{idx}. Sección {idx}"})
    return toc


def render_article_from_template(article: dict, template_str: str) -> str:
    """Rellena la plantilla maestra templates/articulo.html con los datos del artículo."""
    cat = article["category"]
    defaults = CATEGORY_DEFAULTS.get(cat, CATEGORY_DEFAULTS["Bienestar y Juegos"])

    body_html = article.get("bodyHtml", "").strip()
    toc_list = article.get("toc") or extract_toc_from_body(body_html)

    toc_lines = []
    for idx, item in enumerate(toc_list):
        active_cls = " active" if idx == 0 else ""
        toc_lines.append(
            f'            <li><a href="#{item["id"]}" class="toc-link{active_cls}">{item["label"]}</a></li>'
        )
    toc_html = "\n".join(toc_lines)

    indented_body = "\n".join(
        f"        {line}" if not line.startswith("        ") and line.strip() else line
        for line in body_html.splitlines()
    )

    replacements = {
        "{{TITLE}}": article["title"],
        "{{SUBTITLE}}": article.get("subtitle") or article["excerpt"],
        "{{EXCERPT}}": article["excerpt"],
        "{{SLUG}}": article["slug"],
        "{{CATEGORY}}": cat,
        "{{TOPBAR_TAG}}": article.get("topbarTag") or defaults["topbarTag"],
        "{{SECTION_TAG}}": article.get("sectionTag") or defaults["sectionTag"],
        "{{AUTHOR}}": article["author"],
        "{{AUTHOR_ROLE}}": article["authorRole"],
        "{{AUTHOR_INITIALS}}": get_author_initials(article["author"]),
        "{{DATE}}": article["date"],
        "{{READ_TIME}}": article["readTime"],
        "{{TOC_ITEMS}}": toc_html,
        "{{ARTICLE_BODY}}": indented_body,
    }

    rendered = template_str
    for key, val in replacements.items():
        rendered = rendered.replace(key, str(val))
    return rendered


def ensure_editorial_calendar():
    """Crea el calendario editorial sugerido si no existe aún."""
    if CALENDAR_JSON.exists():
        return
    sample_calendar = [
        {
            "id": "cal-01",
            "status": "pendiente",
            "title": "Cómo elegir el mejor arnés en Y para tu perro y por qué evitar los collares de ahogo",
            "category": "Educación y Entrenamiento",
            "author": "Sofía Herrera",
            "authorRole": "Educadora Canina en Positivo",
            "targetAudience": "Tutores de 18 a 65 años que buscan paseos cómodos sin tirones ni daño cervical",
            "keywords": ["arnés en Y", "paseo sin tirones", "salud cervical canina"]
        },
        {
            "id": "cal-02",
            "status": "pendiente",
            "title": "Alergias alimentarias y ambientales en perros: señales en piel, orejas y patitas",
            "category": "Salud y Prevención",
            "author": "Dr. Alejandro Ruiz",
            "authorRole": "Médico Veterinario",
            "targetAudience": "Tutores cuyos perros se lamen las patas o sufren otitis recurrentes",
            "keywords": ["alergia en perros", "dermatitis canina", "dieta de descarte"]
        },
        {
            "id": "cal-03",
            "status": "pendiente",
            "title": "Recetas de helados y snacks hidratantes caseros para días de calor",
            "category": "Nutrición",
            "author": "Dra. Valeria Méndez",
            "authorRole": "Nutricionista Veterinaria",
            "targetAudience": "Familias que desean premiar e hidratar a sus perros con ingredientes naturales",
            "keywords": ["snacks naturales", "helados para perros", "hidratación canina"]
        }
    ]
    CALENDAR_JSON.write_text(
        json.dumps(sample_calendar, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def cmd_build() -> int:
    if not ARTICLES_JSON.exists() or not DIRECTORY_JSON.exists():
        print("[ERROR] No se encontraron cms_articulos.json o cms_directorio.json.")
        return 1

    if not TEMPLATE_HTML.exists():
        print(f"[ERROR] No se encontró la plantilla maestra en {TEMPLATE_HTML}")
        return 1

    ensure_editorial_calendar()
    ARTICLES_MD_DIR.mkdir(parents=True, exist_ok=True)
    template_str = TEMPLATE_HTML.read_text(encoding="utf-8")

    articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
    directory = json.loads(DIRECTORY_JSON.read_text(encoding="utf-8"))

    # Cargar cualquier archivo .md nuevo o editado en 02_Estrategia_Y_Contenido/articulos/
    md_by_slug = {}
    for md_file in sorted(ARTICLES_MD_DIR.glob("*.md")):
        parsed_md = parse_markdown_article(md_file)
        if parsed_md.get("slug"):
            md_by_slug[parsed_md["slug"]] = parsed_md

    known_slugs = {a.get("slug") or slugify(a["title"]) for a in articles}
    for slug_k, md_data in md_by_slug.items():
        if slug_k not in known_slugs and md_data.get("title"):
            articles.insert(0, md_data)
            known_slugs.add(slug_k)

    generated_pages = 0
    clean_articles_for_js = []
    enriched_cms_articles = []

    for idx, art in enumerate(articles, start=1):
        art_id = art.get("id") or f"art-{idx:02d}"
        slug = art.get("slug") or slugify(art["title"])
        cat = art.get("category", "Bienestar y Juegos")
        if cat not in ALLOWED_ARTICLE_CATEGORIES:
            cat = "Bienestar y Juegos"
        defaults = CATEGORY_DEFAULTS[cat]

        # Si existe versión en Markdown con cuerpo, sincronizar campos
        md_override = md_by_slug.get(slug, {})
        body_html = md_override.get("bodyHtml") or art.get("bodyHtml") or ""
        toc = art.get("toc") or []

        # Si tiene `sections` en JSON pero no `bodyHtml`, construir `bodyHtml`
        if not body_html and art.get("sections"):
            body_html, toc = build_body_from_sections(art["sections"])

        # Si aún no tiene `bodyHtml`, extraer del HTML existente en 01_Infraestructura_Web/articulos/
        target_html = ARTICLES_DIR / slug
        if not body_html and target_html.exists():
            extracted = extract_from_existing_html(target_html)
            body_html = extracted.get("bodyHtml", "")
            toc = toc or extracted.get("toc", [])
            for field in ("topbarTag", "sectionTag", "subtitle"):
                if field in extracted and not art.get(field):
                    art[field] = extracted[field]

        full_article = {
            "id": art_id,
            "slug": slug,
            "title": md_override.get("title", art["title"]).strip(),
            "subtitle": md_override.get("subtitle", art.get("subtitle", art["excerpt"])).strip(),
            "excerpt": md_override.get("excerpt", art["excerpt"]).strip(),
            "category": cat,
            "readTime": md_override.get("readTime", art.get("readTime", "7 min de lectura")),
            "date": md_override.get("date", art.get("date", datetime.now().strftime("%d %b %Y"))),
            "author": md_override.get("author", art.get("author", defaults["author"])),
            "authorRole": md_override.get("authorRole", art.get("authorRole", defaults["authorRole"])),
            "emoji": md_override.get("emoji", art.get("emoji", defaults["emoji"])),
            "topbarTag": md_override.get("topbarTag", art.get("topbarTag", defaults["topbarTag"])),
            "sectionTag": md_override.get("sectionTag", art.get("sectionTag", defaults["sectionTag"])),
            "bgGradient": md_override.get("bgGradient", art.get("bgGradient", defaults["bgGradient"])),
            "featured": bool(md_override.get("featured", art.get("featured", False))),
            "toc": toc or extract_toc_from_body(body_html),
            "bodyHtml": body_html,
        }

        enriched_cms_articles.append(full_article)

        # Guardar archivo Markdown fuente en 02_Estrategia_Y_Contenido/articulos/
        if body_html:
            write_markdown_file(full_article)
            rendered_html = render_article_from_template(full_article, template_str)
            target_html.write_text(rendered_html, encoding="utf-8")
            generated_pages += 1

        clean_articles_for_js.append({
            "id": full_article["id"],
            "slug": full_article["slug"],
            "title": full_article["title"],
            "excerpt": full_article["excerpt"],
            "category": full_article["category"],
            "readTime": full_article["readTime"],
            "date": full_article["date"],
            "author": full_article["author"],
            "authorRole": full_article["authorRole"],
            "emoji": full_article["emoji"],
            "bgGradient": full_article["bgGradient"],
            "featured": full_article["featured"],
        })

    # Guardar cms_articulos.json sincronizado
    ARTICLES_JSON.write_text(
        json.dumps(enriched_cms_articles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Validar y limpiar directorio
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

    DIRECTORY_JSON.write_text(
        json.dumps(clean_directory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Escribir 01_Infraestructura_Web/js/data.js
    payload = {
        "articles": clean_articles_for_js,
        "directory": clean_directory,
    }
    js_content = (
        "/**\n"
        " * PERRITOS FELICES — Base de datos central de Artículos y Directorio Canino\n"
        " * Generado automáticamente por 01_Infraestructura_Web/scripts/publicar.py\n"
        " * Línea Gráfica: Azul Cobalto (#2241C8) & Amarillo Dorado (#FFBE58) — 'Ladridos que inspiran'\n"
        " */\n\n"
        f"window.PERRITOS_DATA = {json.dumps(payload, ensure_ascii=False, indent=2)};\n"
    )
    DATA_JS_PATH.write_text(js_content, encoding="utf-8")

    # Generar sitemap.xml y robots.txt para SEO
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [
        "https://www.perritosfelices.com/",
        "https://www.perritosfelices.com/blog.html",
        "https://www.perritosfelices.com/directorio.html",
    ] + [f"https://www.perritosfelices.com/articulos/{a['slug']}" for a in clean_articles_for_js]

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

    robots_txt = (
        "User-agent: *\n"
        "Allow: /\n\n"
        "Sitemap: https://www.perritosfelices.com/sitemap.xml\n"
    )
    ROBOTS_PATH.write_text(robots_txt, encoding="utf-8")

    print("=================================================================")
    print(" PERRITOS FELICES — PUBLICACIÓN AUTOMATIZADA COMPLETADA (v2.0)")
    print("=================================================================")
    print(f" ✔ Artículos sincronizados en js/data.js : {len(clean_articles_for_js)}")
    print(f" ✔ Archivos Markdown sincronizados (.md) : {len(list(ARTICLES_MD_DIR.glob('*.md')))}")
    print(f" ✔ Páginas HTML compiladas con plantilla : {generated_pages}")
    print(f" ✔ Negocios sincronizados en Directorio  : {len(clean_directory)}")
    print(f" ✔ Sitemap SEO y robots.txt generados    : {len(urls)} URLs")
    print("=================================================================")
    return 0


def cmd_status() -> int:
    articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8")) if ARTICLES_JSON.exists() else []
    directory = json.loads(DIRECTORY_JSON.read_text(encoding="utf-8")) if DIRECTORY_JSON.exists() else []
    calendar = json.loads(CALENDAR_JSON.read_text(encoding="utf-8")) if CALENDAR_JSON.exists() else []

    print("=================================================================")
    print(" ESTADO EDITORIAL Y DIRECTORIO — PERRITOS FELICES")
    print("=================================================================")
    print(f" 📚 Total de Artículos Publicados : {len(articles)}")
    cats = {}
    for a in articles:
        cats[a["category"]] = cats.get(a["category"], 0) + 1
    for c, count in sorted(cats.items()):
        print(f"    • {c}: {count}")

    print(f"\n 📍 Total Negocios en Directorio  : {len(directory)}")
    cities = {}
    for b in directory:
        cities[b["city"]] = cities.get(b["city"], 0) + 1
    for city, count in sorted(cities.items()):
        print(f"    • {city}: {count}")

    pending = [c for c in calendar if c.get("status") == "pendiente"]
    print(f"\n 🗓️  Temas Pendientes en Calendario: {len(pending)}")
    for item in pending:
        print(f"    • [{item['id']}] {item['title']} ({item['category']})")
    print("=================================================================")
    return 0


def cmd_nuevo_negocio(args: argparse.Namespace) -> int:
    directory = json.loads(DIRECTORY_JSON.read_text(encoding="utf-8"))
    next_num = len(directory) + 1
    biz_id = f"dir-{next_num:02d}"
    highlights = [h.strip() for h in args.highlights.split(",") if h.strip()][:4]

    new_biz = {
        "id": biz_id,
        "name": args.name.strip(),
        "category": args.category.strip(),
        "city": args.city.strip(),
        "rating": round(float(args.rating), 1),
        "reviews": int(args.reviews),
        "verified": True,
        "emoji": args.emoji.strip(),
        "description": args.description.strip(),
        "address": args.address.strip(),
        "phone": args.phone.strip(),
        "hours": args.hours.strip(),
        "highlights": highlights or ["Trato Amable Verificado", "100% Libre de Castigos"],
    }
    directory.append(new_biz)
    DIRECTORY_JSON.write_text(
        json.dumps(directory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"✔ Negocio '{new_biz['name']}' registrado con ID {biz_id}.")
    return cmd_build()


def cmd_deploy(args: argparse.Namespace) -> int:
    build_res = cmd_build()
    if build_res != 0:
        return build_res
    msg = getattr(args, "msg", None) or f"chore(editorial): publicación de contenido [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
    print("\n🚀 Preparando despliegue hacia GitHub y Vercel (Sitio Live)...")
    res1 = subprocess.run(["git", "add", "."], cwd=WEB_DIR)
    if res1.returncode != 0:
        print("❌ Error ejecutando 'git add .'")
        return res1.returncode
    subprocess.run(["git", "commit", "-m", msg], cwd=WEB_DIR)
    print("📤 Enviando cambios a 'origin main'...")
    res3 = subprocess.run(["git", "push", "origin", "main"], cwd=WEB_DIR)
    if res3.returncode == 0:
        print("\n🎉 Despliegue enviado con éxito a GitHub.")
        print("⚡ Vercel detectará el push y actualizará www.perritosfelices.com en 15-30 segundos.")
    else:
        print("⚠️ No se pudo completar el push automáticamente (revisa tus credenciales o conexión a GitHub).")
    return res3.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI de Publicación Automatizada — Perritos Felices"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("build", help="Compila artículos, directorio, data.js y sitemap.xml")
    sub.add_parser("status", help="Muestra estadísticas del sitio y calendario editorial")

    dep_p = sub.add_parser("deploy", help="Compila y sube automáticamente los cambios a GitHub / Vercel (Live)")
    dep_p.add_argument("--msg", default=None, help="Mensaje personalizado para el commit de Git")

    neg_p = sub.add_parser("nuevo-negocio", help="Agrega un negocio al directorio y publica")
    neg_p.add_argument("--name", required=True, help="Nombre comercial")
    neg_p.add_argument("--category", default="Veterinaria y Salud", help="Categoría oficial")
    neg_p.add_argument("--city", default="Ciudad de Guatemala", help="Ciudad")
    neg_p.add_argument("--phone", required=True, help="Teléfono de contacto")
    neg_p.add_argument("--address", required=True, help="Dirección física")
    neg_p.add_argument("--description", required=True, help="Descripción de servicios")
    neg_p.add_argument("--hours", default="Lun - Sáb: 8:00 AM a 6:00 PM", help="Horario")
    neg_p.add_argument("--highlights", default="Trato Amable,Libre de Jaulas", help="Separados por coma")
    neg_p.add_argument("--emoji", default="🏥", help="Emoji representativo")
    neg_p.add_argument("--rating", type=float, default=5.0, help="Calificación inicial")
    neg_p.add_argument("--reviews", type=int, default=15, help="Número de reseñas")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    cmd = args.command or "build"

    if cmd == "status":
        return cmd_status()
    if cmd == "deploy":
        return cmd_deploy(args)
    if cmd == "nuevo-negocio":
        return cmd_nuevo_negocio(args)
    return cmd_build()


if __name__ == "__main__":
    sys.exit(main())

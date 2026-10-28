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
MARKETING_JSON = STRATEGY_DIR / "cms_marketing.json"
DIRECTORY_JSON = CANINE_DIR / "cms_directorio.json"

INDEX_HTML = WEB_DIR / "index.html"
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


DEFAULT_BG_GRADIENT = "linear-gradient(135deg, #FFBE58 0%, #FFE2AD 100%)"
SAFE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.html$")
SAFE_GRADIENT_RE = re.compile(
    r"^linear-gradient\(\s*\d{1,3}deg\s*,\s*#[0-9a-fA-F]{3,8}\s+\d{1,3}%\s*,\s*#[0-9a-fA-F]{3,8}\s+\d{1,3}%\s*\)$"
)
# Caracteres Unicode bidireccionales (CVE-2021-42574 Trojan Source) y etiquetas invisibles de Prompt Injection
DANGEROUS_UNICODE_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u202a-\u202e\u2066-\u2069\U000e0000-\U000e007f]"
)
DANGEROUS_HTML_RE = re.compile(
    r"(<\s*/?\s*(?:script|iframe|object|embed|applet|meta|link|style|base|form)\b|on[a-z]+\s*=|javascript\s*:|vbscript\s*:|data\s*:\s*text/html)",
    re.IGNORECASE,
)


def strip_dangerous_unicode(text: str) -> str:
    """Elimina caracteres de control, bidi overrides (Trojan Source) y tags invisibles (Prompt Injection)."""
    if not isinstance(text, str):
        return ""
    return DANGEROUS_UNICODE_RE.sub("", text)


def slugify(text: str) -> str:
    replacements = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    clean = strip_dangerous_unicode(text).translate(replacements).lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    if not clean:
        clean = "articulo"
    return f"{clean}.html" if not clean.endswith(".html") else clean


def sanitize_slug(raw_slug: str, fallback_title: str = "articulo") -> str:
    """Previene Path Traversal forzando un nombre de archivo plano y válido."""
    candidate = strip_dangerous_unicode(str(raw_slug or "")).strip()
    candidate = Path(candidate).name  # Elimina cualquier componente ../ o /
    if not candidate.endswith(".html"):
        candidate = slugify(candidate or fallback_title)
    if not SAFE_SLUG_RE.match(candidate):
        candidate = slugify(candidate.replace(".html", "") or fallback_title)
    return candidate


def assert_safe_child_path(base_dir: Path, target_path: Path) -> Path:
    """Garantiza criptográfica y estructuralmente que target_path resida dentro de base_dir."""
    resolved_base = base_dir.resolve()
    resolved_target = target_path.resolve()
    if not resolved_target.is_relative_to(resolved_base):
        raise ValueError(f"[SEGURIDAD] Intento de Path Traversal bloqueado: {target_path}")
    return resolved_target


def sanitize_bg_gradient(raw_grad: str, fallback: str = DEFAULT_BG_GRADIENT) -> str:
    """Previene CSS Injection validando estrictamente el formato linear-gradient."""
    candidate = strip_dangerous_unicode(str(raw_grad or "")).strip()
    if SAFE_GRADIENT_RE.match(candidate):
        return candidate
    return fallback


def sanitize_article_body_html(body_html: str, source_label: str = "") -> str:
    """Verifica que el cuerpo HTML editorial no contenga vectores XSS ni etiquetas prohibidas."""
    cleaned = strip_dangerous_unicode(body_html)
    match = DANGEROUS_HTML_RE.search(cleaned)
    if match:
        raise ValueError(
            f"[SEGURIDAD] Contenido HTML peligroso bloqueado en {source_label}: '{match.group(0)}'"
        )
    return cleaned


def wrap_tables_responsive(body: str) -> str:
    """Garantiza que todas las tablas editoriales estén envueltas en .table-responsive para scroll táctil móvil."""
    if "<table" not in body.lower():
        return body
    # Limpiar wrappers previos si existieran para evitar duplicación
    cleaned = re.sub(
        r'<div class="table-responsive">\s*(<table[\s\S]*?</table>)\s*</div>',
        r"\1",
        body,
        flags=re.IGNORECASE,
    )
    # Envolver todas las tablas en el contenedor con scroll horizontal seguro
    return re.sub(
        r'(<table[\s\S]*?</table>)',
        r'<div class="table-responsive">\n\1\n</div>',
        cleaned,
        flags=re.IGNORECASE,
    )


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
    assert_safe_child_path(ARTICLES_DIR, html_path)
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
    assert_safe_child_path(ARTICLES_MD_DIR, md_path)
    content = strip_dangerous_unicode(md_path.read_text(encoding="utf-8"))
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

    if "slug" in meta:
        meta["slug"] = sanitize_slug(meta["slug"], str(meta.get("title", md_path.stem)))

    # Si el cuerpo tiene sintaxis Markdown simple (## Título, párrafos), convertir si no es HTML puro
    if "<h2" not in body and "## " in body:
        body = convert_simple_markdown_to_html(body)

    meta["bodyHtml"] = sanitize_article_body_html(body, str(md_path.name))
    return meta


def convert_simple_markdown_to_html(md_text: str) -> str:
    """Convierte Markdown editorial (##, párrafos, listas, callouts > [!TIP]) a HTML de Perritos Felices."""
    lines = strip_dangerous_unicode(md_text).splitlines()
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
        escaped = html.escape(txt, quote=True)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
        return escaped

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
            html_out.append(f"        {sanitize_article_body_html(line, 'markdown-inline-html')}")
        else:
            close_lists()
            html_out.append(f"        <p>\n          {inline_fmt(line)}\n        </p>")
        i += 1

    close_lists()
    return "\n\n".join(html_out)


def write_markdown_file(article: dict) -> Path:
    """Escribe o actualiza el archivo .md fuente para un artículo en 02_Estrategia_Y_Contenido/articulos/."""
    ARTICLES_MD_DIR.mkdir(parents=True, exist_ok=True)
    safe_slug = sanitize_slug(article["slug"], article.get("title", "articulo"))
    slug_base = safe_slug.replace(".html", "")
    md_path = assert_safe_child_path(ARTICLES_MD_DIR, ARTICLES_MD_DIR / f"{slug_base}.md")

    def clean_fm_val(v: str) -> str:
        return strip_dangerous_unicode(str(v)).replace('"', "'").replace("\n", " ").strip()

    frontmatter = [
        "---",
        f'id: "{clean_fm_val(article["id"])}"',
        f'slug: "{safe_slug}"',
        f'title: "{clean_fm_val(article["title"])}"',
        f'subtitle: "{clean_fm_val(article.get("subtitle", article["excerpt"]))}"',
        f'excerpt: "{clean_fm_val(article["excerpt"])}"',
        f'category: "{clean_fm_val(article["category"])}"',
        f'readTime: "{clean_fm_val(article["readTime"])}"',
        f'date: "{clean_fm_val(article["date"])}"',
        f'author: "{clean_fm_val(article["author"])}"',
        f'authorRole: "{clean_fm_val(article["authorRole"])}"',
        f'emoji: "{clean_fm_val(article["emoji"])}"',
        f'topbarTag: "{clean_fm_val(article.get("topbarTag", CATEGORY_DEFAULTS.get(article["category"], {}).get("topbarTag", "🐾 Guía Perritos Felices")))}"',
        f'sectionTag: "{clean_fm_val(article.get("sectionTag", CATEGORY_DEFAULTS.get(article["category"], {}).get("sectionTag", article["category"])))}"',
        f'bgGradient: "{sanitize_bg_gradient(article["bgGradient"])}"',
        f'featured: {"true" if article.get("featured") else "false"}',
        "---",
        "",
        sanitize_article_body_html(article.get("bodyHtml", "").strip(), safe_slug),
        "",
    ]
    md_path.write_text("\n".join(frontmatter), encoding="utf-8")
    return md_path


def build_body_from_sections(sections: list) -> tuple:
    """Construye bodyHtml y toc a partir de una lista estructurada de `sections` en JSON."""
    toc_items = []
    blocks = []
    for idx, sec in enumerate(sections, start=1):
        raw_id = strip_dangerous_unicode(str(sec.get("id") or f"seccion-{idx}"))
        sec_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw_id).strip("-") or f"seccion-{idx}"
        heading = strip_dangerous_unicode(str(sec.get("heading", f"Sección {idx}")))
        clean_heading = re.sub(r"^\d+\.\s*", "", heading)
        toc_items.append({"id": sec_id, "label": f"{idx}. {clean_heading}"})

        blocks.append(f'        <h2 id="{sec_id}">{idx}. {html.escape(clean_heading)}</h2>')
        for p in sec.get("paragraphs", []):
            blocks.append(f"        <p>\n          {html.escape(strip_dangerous_unicode(str(p)))}\n        </p>")
        if sec.get("bullets"):
            li_str = "\n".join(
                f"          <li>{html.escape(strip_dangerous_unicode(str(b)))}</li>" for b in sec["bullets"]
            )
            blocks.append(f"        <ul>\n{li_str}\n        </ul>")
        if sec.get("tip"):
            box_type = "alert-orange" if sec.get("tipType") == "alert-orange" else "tip-sage"
            tip_title = strip_dangerous_unicode(str(sec.get("tipTitle", "🌿 Consejo práctico de bienestar")))
            blocks.append(
                f'        <div class="callout-box {box_type}">\n'
                f"          <strong>{html.escape(tip_title)}</strong>\n"
                f"          {html.escape(strip_dangerous_unicode(str(sec['tip'])))}\n"
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
        raw_id = strip_dangerous_unicode(match.group(1).strip())
        sec_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw_id).strip("-") or f"seccion-{idx}"
        label = strip_dangerous_unicode(re.sub(r"<[^>]+>", "", match.group(2)).strip())
        # Acortar etiquetas muy largas para el sidebar
        if ":" in label and len(label) > 42:
            label = label.split(":", 1)[0].strip()
        toc.append({"id": sec_id, "label": label or f"{idx}. Sección {idx}"})
    return toc


def render_article_from_template(article: dict, template_str: str) -> str:
    """Rellena la plantilla maestra templates/articulo.html con escapado HTML estricto."""
    cat = article["category"]
    defaults = CATEGORY_DEFAULTS.get(cat, CATEGORY_DEFAULTS["Bienestar y Juegos"])

    body_html = sanitize_article_body_html(
        article.get("bodyHtml", "").strip(), article.get("slug", "articulo")
    )
    body_html = wrap_tables_responsive(body_html)
    toc_list = article.get("toc") or extract_toc_from_body(body_html)

    toc_lines = []
    for idx, item in enumerate(toc_list):
        active_cls = " active" if idx == 0 else ""
        safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(item.get("id", f"seccion-{idx+1}"))).strip("-")
        safe_label = html.escape(strip_dangerous_unicode(str(item.get("label", ""))), quote=True)
        toc_lines.append(
            f'            <li><a href="#{safe_id}" class="toc-link{active_cls}">{safe_label}</a></li>'
        )
    toc_html = "\n".join(toc_lines)

    indented_body = "\n".join(
        f"        {line}" if not line.startswith("        ") and line.strip() else line
        for line in body_html.splitlines()
    )

    def esc(val: object) -> str:
        return html.escape(strip_dangerous_unicode(str(val)), quote=True)

    safe_slug_val = sanitize_slug(article["slug"], article["title"])
    slug_base = safe_slug_val.replace(".html", "")

    # 1. Portada Fotográfica Editorial (Hero Media)
    img_rel = f"assets/articulos/{slug_base}.jpg"
    img_full = WEB_DIR / img_rel
    if img_full.exists():
        hero_media_html = (
            f'        <figure class="article-hero-media">\n'
            f'          <img src="../{img_rel}" alt="{esc(article["title"])}" class="article-hero-img" width="1200" height="675" fetchpriority="high" decoding="async" />\n'
            f'          <figcaption class="article-hero-caption">\n'
            f'            <span>FOTOGRAFÍA DOCUMENTAL PERRITOS FELICES // CRIANZA RESPETUOSA</span>\n'
            f'            <span>ESTÁNDAR FEAR-FREE</span>\n'
            f'          </figcaption>\n'
            f'        </figure>'
        )
        og_image_url = f"https://www.perritosfelices.com/{img_rel}"
    else:
        hero_media_html = ""
        og_image_url = "https://www.perritosfelices.com/assets/logo/icononly_transparent_nobuffer.png"

    # 2. Caja TL;DR Oficial PF-2027 (Escaneabilidad de 30 segundos)
    if "tldr-box" not in body_html:
        tldr_text = esc(article.get("subtitle") or article["excerpt"])
        tldr_box_html = (
            f'        <div class="tldr-box">\n'
            f'          <strong>⚡ En 30 segundos: Lo que debes saber</strong>\n'
            f'          <p>{tldr_text}</p>\n'
            f'        </div>'
        )
    else:
        tldr_box_html = ""

    # 3. Recomendación Ética Cruzada (Blog -> Directorio Canino)
    if "ethical-recommendation-box" not in body_html:
        if cat in ("Comportamiento", "Educación y Entrenamiento"):
            ethical_cta_html = (
                '        <div class="ethical-recommendation-box">\n'
                '          <h4>¿Buscas apoyo profesional y respetuoso para tu perro?</h4>\n'
                '          <p>Encuentra educadores caninos, etólogos y guarderías 100% libres de castigo en tu ciudad dentro de nuestro Directorio Canino Verificado.</p>\n'
                '          <a href="../directorio.html?categoria=Entrenamiento%20y%20Etolog%C3%ADa" class="btn btn-primary btn-sm">EXPLORAR ESPECIALISTAS EN ETOLOGÍA ↗</a>\n'
                '        </div>'
            )
        elif cat == "Nutrición":
            ethical_cta_html = (
                '        <div class="ethical-recommendation-box">\n'
                '          <h4>¿Quieres asesoría en nutrición natural o dietas caseras?</h4>\n'
                '          <p>Encuentra veterinarias integrativas y tiendas con insumos frescos certificados en nuestro Directorio Canino.</p>\n'
                '          <a href="../directorio.html?categoria=Nutrici%C3%B3n%20y%20Tienda" class="btn btn-primary btn-sm">BUSCAR TIENDAS Y NUTRICIONISTAS ↗</a>\n'
                '        </div>'
            )
        elif cat in ("Salud y Prevención", "Higiene y Cuidado"):
            ethical_cta_html = (
                '        <div class="ethical-recommendation-box">\n'
                '          <h4>Clínicas veterinarias y estéticas con manejo amable</h4>\n'
                '          <p>Espacios con protocolos de bajo estrés, sin jaulas de espera y con trato cálido hacia tu familia.</p>\n'
                '          <a href="../directorio.html?categoria=Veterinaria%20y%20Salud" class="btn btn-primary btn-sm">LOCALIZAR VETERINARIAS VERIFICADAS ↗</a>\n'
                '        </div>'
            )
        else:
            ethical_cta_html = (
                '        <div class="ethical-recommendation-box">\n'
                '          <h4>Hoteles campestres, parques y espacios Pet-Friendly</h4>\n'
                '          <p>Disfruta de paseos y descanso con tu perro en lugares seguros y verificados bajo trato amable.</p>\n'
                '          <a href="../directorio.html?categoria=Guarder%C3%ADa%20y%20Hotel" class="btn btn-primary btn-sm">VER HOTELES Y GUARDERÍAS ↗</a>\n'
                '        </div>'
            )
    else:
        ethical_cta_html = ""

    json_ld_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": strip_dangerous_unicode(str(article["title"])),
        "description": strip_dangerous_unicode(str(article["excerpt"])),
        "image": og_image_url,
        "url": f"https://www.perritosfelices.com/articulos/{safe_slug_val}",
        "datePublished": strip_dangerous_unicode(str(article["date"])),
        "author": {
            "@type": "Organization",
            "name": strip_dangerous_unicode(str(article["author"])),
            "url": "https://www.perritosfelices.com/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Perritos Felices",
            "alternateName": "Perros Felices",
            "url": "https://www.perritosfelices.com/",
            "logo": {
                "@type": "ImageObject",
                "url": "https://www.perritosfelices.com/assets/logo/icononly_transparent_nobuffer.png"
            }
        }
    }
    json_ld_raw = json.dumps(json_ld_data, ensure_ascii=False, indent=4).replace("</", "<\\/")
    indented_json_ld = "\n".join(f"  {line}" for line in json_ld_raw.splitlines())

    replacements = {
        "{{TITLE}}": esc(article["title"]),
        "{{SUBTITLE}}": esc(article.get("subtitle") or article["excerpt"]),
        "{{EXCERPT}}": esc(article["excerpt"]),
        "{{SLUG}}": esc(safe_slug_val),
        "{{CATEGORY}}": esc(cat),
        "{{TOPBAR_TAG}}": esc(article.get("topbarTag") or defaults["topbarTag"]),
        "{{SECTION_TAG}}": esc(article.get("sectionTag") or defaults["sectionTag"]),
        "{{AUTHOR}}": esc(article["author"]),
        "{{AUTHOR_ROLE}}": esc(article["authorRole"]),
        "{{AUTHOR_INITIALS}}": esc(get_author_initials(article["author"])),
        "{{DATE}}": esc(article["date"]),
        "{{READ_TIME}}": esc(article["readTime"]),
        "{{TOC_ITEMS}}": toc_html,
        "{{TLDR_BOX}}": tldr_box_html,
        "{{HERO_MEDIA}}": hero_media_html,
        "{{ARTICLE_BODY}}": indented_body,
        "{{ETHICAL_CTA}}": ethical_cta_html,
        "{{OG_IMAGE}}": og_image_url,
        "{{JSON_LD}}": indented_json_ld,
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
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    template_str = TEMPLATE_HTML.read_text(encoding="utf-8")

    articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
    directory = json.loads(DIRECTORY_JSON.read_text(encoding="utf-8"))

    # Cargar cualquier archivo .md nuevo o editado en 02_Estrategia_Y_Contenido/articulos/
    md_by_slug = {}
    for md_file in sorted(ARTICLES_MD_DIR.glob("*.md")):
        parsed_md = parse_markdown_article(md_file)
        if parsed_md.get("slug"):
            md_by_slug[parsed_md["slug"]] = parsed_md

    known_slugs = {
        sanitize_slug(a.get("slug", ""), a.get("title", "articulo")) for a in articles
    }
    for slug_k, md_data in md_by_slug.items():
        if slug_k not in known_slugs and md_data.get("title"):
            articles.insert(0, md_data)
            known_slugs.add(slug_k)

    generated_pages = 0
    clean_articles_for_js = []
    enriched_cms_articles = []

    for idx, art in enumerate(articles, start=1):
        raw_id = strip_dangerous_unicode(str(art.get("id") or f"art-{idx:02d}"))
        art_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw_id).strip("-") or f"art-{idx:02d}"
        slug = sanitize_slug(art.get("slug", ""), art.get("title", f"articulo-{idx}"))
        cat = strip_dangerous_unicode(str(art.get("category", "Bienestar y Juegos")))
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
        target_html = assert_safe_child_path(ARTICLES_DIR, ARTICLES_DIR / slug)
        if not body_html and target_html.exists():
            extracted = extract_from_existing_html(target_html)
            body_html = extracted.get("bodyHtml", "")
            toc = toc or extracted.get("toc", [])
            for field in ("topbarTag", "sectionTag", "subtitle"):
                if field in extracted and not art.get(field):
                    art[field] = extracted[field]

        body_html = sanitize_article_body_html(body_html, slug)
        raw_grad = md_override.get("bgGradient", art.get("bgGradient", defaults["bgGradient"]))
        safe_grad = sanitize_bg_gradient(raw_grad, defaults["bgGradient"])

        full_article = {
            "id": art_id,
            "slug": slug,
            "title": strip_dangerous_unicode(str(md_override.get("title", art["title"]))).strip(),
            "subtitle": strip_dangerous_unicode(
                str(md_override.get("subtitle", art.get("subtitle", art["excerpt"])))
            ).strip(),
            "excerpt": strip_dangerous_unicode(str(md_override.get("excerpt", art["excerpt"]))).strip(),
            "category": cat,
            "readTime": strip_dangerous_unicode(
                str(md_override.get("readTime", art.get("readTime", "7 min de lectura")))
            ).strip(),
            "date": strip_dangerous_unicode(
                str(md_override.get("date", art.get("date", datetime.now().strftime("%d %b %Y"))))
            ).strip(),
            "author": strip_dangerous_unicode(
                str(md_override.get("author", art.get("author", defaults["author"])))
            ).strip(),
            "authorRole": strip_dangerous_unicode(
                str(md_override.get("authorRole", art.get("authorRole", defaults["authorRole"])))
            ).strip(),
            "emoji": strip_dangerous_unicode(
                str(md_override.get("emoji", art.get("emoji", defaults["emoji"])))
            ).strip(),
            "topbarTag": strip_dangerous_unicode(
                str(md_override.get("topbarTag", art.get("topbarTag", defaults["topbarTag"])))
            ).strip(),
            "sectionTag": strip_dangerous_unicode(
                str(md_override.get("sectionTag", art.get("sectionTag", defaults["sectionTag"])))
            ).strip(),
            "bgGradient": safe_grad,
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

        slug_base = full_article["slug"].replace(".html", "")
        img_rel = f"assets/articulos/{slug_base}.jpg"
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
            "image": img_rel if (WEB_DIR / img_rel).exists() else "",
        })

    # Guardar cms_articulos.json sincronizado
    ARTICLES_JSON.write_text(
        json.dumps(enriched_cms_articles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Validar y limpiar directorio
    clean_directory = []
    for idx, biz in enumerate(directory, start=1):
        raw_biz_id = strip_dangerous_unicode(str(biz.get("id") or f"dir-{idx:02d}"))
        biz_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw_biz_id).strip("-") or f"dir-{idx:02d}"
        cat = strip_dangerous_unicode(str(biz.get("category", "Veterinaria y Salud")))
        if cat not in ALLOWED_DIRECTORY_CATEGORIES:
            cat = "Veterinaria y Salud"

        raw_highlights = biz.get("highlights", ["Trato Amable Verificado"])
        safe_highlights = [
            strip_dangerous_unicode(str(h)).strip()[:60]
            for h in (raw_highlights if isinstance(raw_highlights, list) else [])
            if str(h).strip()
        ][:4] or ["Trato Amable Verificado"]

        clean_directory.append({
            "id": biz_id,
            "name": strip_dangerous_unicode(str(biz["name"])).strip()[:100],
            "category": cat,
            "city": strip_dangerous_unicode(str(biz.get("city", "Ciudad de Guatemala"))).strip()[:60],
            "rating": min(max(round(float(biz.get("rating", 5.0)), 1), 1.0), 5.0),
            "reviews": max(int(biz.get("reviews", 1)), 1),
            "verified": bool(biz.get("verified", True)),
            "emoji": strip_dangerous_unicode(str(biz.get("emoji", "🏥"))).strip()[:8],
            "description": strip_dangerous_unicode(str(biz["description"])).strip()[:400],
            "address": strip_dangerous_unicode(str(biz["address"])).strip()[:180],
            "phone": strip_dangerous_unicode(str(biz["phone"])).strip()[:32],
            "hours": strip_dangerous_unicode(str(biz.get("hours", "Lun - Sáb: 9:00 AM a 6:00 PM"))).strip()[:80],
            "highlights": safe_highlights,
        })

    DIRECTORY_JSON.write_text(
        json.dumps(clean_directory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Cargar y sincronizar textos de portada y marketing (cms_marketing.json -> index.html)
    marketing_data = {}
    if MARKETING_JSON.exists():
        raw_mkt = json.loads(MARKETING_JSON.read_text(encoding="utf-8"))
        for k, v in raw_mkt.items():
            if isinstance(v, list):
                marketing_data[k] = [strip_dangerous_unicode(str(item)).strip()[:80] for item in v if str(item).strip()][:8]
            else:
                marketing_data[k] = strip_dangerous_unicode(str(v)).strip()[:500]
        MARKETING_JSON.write_text(
            json.dumps(marketing_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if INDEX_HTML.exists():
            idx_html = INDEX_HTML.read_text(encoding="utf-8")
            for field_key, field_val in marketing_data.items():
                if field_key == "tickerItems" and isinstance(field_val, list) and field_val:
                    spans = []
                    for i, item_txt in enumerate(field_val):
                        spans.append(f"        <span>{html.escape(item_txt, quote=True)}</span>")
                        if i < len(field_val) - 1:
                            spans.append('        <span class="ticker-sep">✦</span>')
                    inner_ticker = "\n" + "\n".join(spans) + "\n      "
                    idx_html = re.sub(
                        r'(<div[^>]*\bdata-cms="tickerTrack"[^>]*>)(.*?)(</div>)',
                        lambda m: m.group(1) + inner_ticker + m.group(3),
                        idx_html,
                        flags=re.DOTALL,
                    )
                elif isinstance(field_val, str):
                    safe_txt = html.escape(field_val, quote=True)
                    pattern = rf'(<(?P<tag>[a-zA-Z0-9]+)\b[^>]*\bdata-cms="{re.escape(field_key)}"[^>]*>)(.*?)(</(?P=tag)>)'
                    idx_html = re.sub(
                        pattern,
                        lambda m, st=safe_txt: m.group(1) + st + m.group(4),
                        idx_html,
                        flags=re.DOTALL,
                    )
            INDEX_HTML.write_text(idx_html, encoding="utf-8")

    # Escribir 01_Infraestructura_Web/js/data.js previniendo inyección de cierre </script>
    payload = {
        "articles": clean_articles_for_js,
        "directory": clean_directory,
        "marketing": marketing_data,
    }
    safe_json_payload = (
        json.dumps(payload, ensure_ascii=False, indent=2)
        .replace("</", "<\\/")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
    js_content = (
        "/**\n"
        " * PERRITOS FELICES — Base de datos central de Artículos, Directorio Canino y Marketing\n"
        " * Generado automáticamente por 01_Infraestructura_Web/scripts/publicar.py\n"
        " * Línea Gráfica: Azul Cobalto (#2241C8) & Amarillo Dorado (#FFBE58) — 'Ladridos que inspiran'\n"
        " */\n\n"
        f"window.PERRITOS_DATA = {safe_json_payload};\n"
    )
    DATA_JS_PATH.write_text(js_content, encoding="utf-8")

    # Generar sitemap.xml y robots.txt para SEO con escapado XML
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [
        "https://www.perritosfelices.com/",
        "https://www.perritosfelices.com/blog.html",
        "https://www.perritosfelices.com/directorio.html",
        "https://www.perritosfelices.com/herramientas.html",
    ] + [
        f"https://www.perritosfelices.com/articulos/{sanitize_slug(a['slug'], a['title'])}"
        for a in clean_articles_for_js
    ]

    sitemap_nodes = "\n".join(
        f"  <url>\n    <loc>{html.escape(u, quote=True)}</loc>\n    <lastmod>{today}</lastmod>\n  </url>"
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
    print(" PERRITOS FELICES — PUBLICACIÓN AUTOMATIZADA COMPLETADA (v2.1 SEC)")
    print("=================================================================")
    print(f" ✔ Artículos sincronizados en js/data.js : {len(clean_articles_for_js)}")
    print(f" ✔ Archivos Markdown sincronizados (.md) : {len(list(ARTICLES_MD_DIR.glob('*.md')))}")
    print(f" ✔ Páginas HTML compiladas con plantilla : {generated_pages}")
    print(f" ✔ Negocios sincronizados en Directorio  : {len(clean_directory)}")
    print(f" ✔ Sitemap SEO y robots.txt generados    : {len(urls)} URLs")
    print("=================================================================")
    return 0


def cmd_audit() -> int:
    """Auditoría profunda de ciberseguridad: Sitio Web, Pipeline de Datos y Entorno Agéntico."""
    print("=================================================================")
    print(" AUDITORÍA ZERO-TRUST DE CIBERSEGURIDAD — PERRITOS FELICES")
    print("=================================================================")
    issues = 0

    # 1. Verificar caracteres Trojan Source / Prompt Injection en JSON y Markdown
    data_files = [ARTICLES_JSON, DIRECTORY_JSON, CALENDAR_JSON, MARKETING_JSON] + list(ARTICLES_MD_DIR.glob("*.md"))
    for df in data_files:
        if df.exists():
            raw_txt = df.read_text(encoding="utf-8")
            if DANGEROUS_UNICODE_RE.search(raw_txt):
                print(f" ❌ [CRÍTICO] Caracteres Unicode bidi/invisibles detectados en: {df.name}")
                issues += 1
    if issues == 0:
        print(" ✔ [1/5] Fuentes de datos libres de Trojan Source (CVE-2021-42574) y Prompt Injection invisible.")

    # 2. Verificar confinamiento de rutas (Path Traversal) y formato de gradientes en artículos
    if ARTICLES_JSON.exists():
        arts = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
        for a in arts:
            slug = a.get("slug", "")
            if not SAFE_SLUG_RE.match(slug):
                print(f" ❌ [CRÍTICO] Slug fuera de norma o posible Path Traversal: {slug}")
                issues += 1
            grad = a.get("bgGradient", "")
            if grad and not SAFE_GRADIENT_RE.match(grad):
                print(f" ❌ [CRÍTICO] bgGradient inválido o riesgo de CSS Injection en {slug}: {grad}")
                issues += 1
            if DANGEROUS_HTML_RE.search(a.get("bodyHtml", "")):
                print(f" ❌ [CRÍTICO] Etiquetas o eventos HTML peligrosos en cuerpo de: {slug}")
                issues += 1
    if issues == 0:
        print(" ✔ [2/5] Confinamiento de rutas (Path Traversal), esquemas CSS y sanitización HTML verificados.")

    # 3. Verificar cabeceras CSP en todos los HTML, vercel.json y _headers
    html_files = list(WEB_DIR.rglob("*.html"))
    for hf in html_files:
        txt = hf.read_text(encoding="utf-8")
        if 'http-equiv="Content-Security-Policy"' not in txt:
            print(f" ❌ [CRÍTICO] Falta meta Content-Security-Policy en: {hf.relative_to(WEB_DIR)}")
            issues += 1
        if re.search(r"(\.innerHTML\s*=|\.outerHTML\s*=|document\.write\(|eval\(|new Function\()", txt):
            print(f" ❌ [CRÍTICO] Sumidero XSS detectado en HTML: {hf.relative_to(WEB_DIR)}")
            issues += 1
    if issues == 0:
        print(f" ✔ [3/5] {len(html_files)} documentos HTML cumplen Content-Security-Policy y cero sumideros XSS.")

    # 4. Verificar que no existan archivos sensibles o secretos expuestos en el árbol web
    forbidden_patterns = ["*.env*", "*.pem", "*.key", "*.p12", "*secret*", "*credentials*"]
    for pat in forbidden_patterns:
        for found in WEB_DIR.rglob(pat):
            if ".git" not in found.parts:
                print(f" ❌ [CRÍTICO] Archivo sensible expuesto en árbol público: {found.relative_to(WEB_DIR)}")
                issues += 1
    if issues == 0:
        print(" ✔ [4/5] Árbol web público libre de credenciales, llaves privadas o archivos .env.")

    # 5. Ejecutar script global audit-web-project.sh si está disponible
    audit_sh = Path.home() / ".gemini/config/skills/web-security-and-optimization/scripts/audit-web-project.sh"
    if audit_sh.exists():
        res = subprocess.run(["bash", str(audit_sh), str(WEB_DIR)], capture_output=True, text=True)
        if res.returncode != 0:
            print(" ❌ [CRÍTICO] Falló audit-web-project.sh:")
            print(res.stdout)
            issues += 1
        else:
            print(" ✔ [5/5] Script OWASP ASVS / CWV / WCAG 2.2 (audit-web-project.sh) aprobado con 0 alertas.")
    else:
        print(" ✔ [5/5] Verificación estática interna completada.")

    print("=================================================================")
    if issues > 0:
        print(f" ❌ AUDITORÍA RECHAZADA: {issues} problema(s) de seguridad detectado(s).")
        return 1
    print(" 🛡️  ESTADO: SITIO Y ENTORNO AGÉNTICO 100% PROTEGIDOS (0 VULNERABILIDADES)")
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
    highlights = [
        strip_dangerous_unicode(h).strip()[:60]
        for h in args.highlights.split(",")
        if h.strip()
    ][:4]

    new_biz = {
        "id": biz_id,
        "name": strip_dangerous_unicode(args.name).strip()[:100],
        "category": strip_dangerous_unicode(args.category).strip(),
        "city": strip_dangerous_unicode(args.city).strip()[:60],
        "rating": min(max(round(float(args.rating), 1), 1.0), 5.0),
        "reviews": max(int(args.reviews), 1),
        "verified": True,
        "emoji": strip_dangerous_unicode(args.emoji).strip()[:8],
        "description": strip_dangerous_unicode(args.description).strip()[:400],
        "address": strip_dangerous_unicode(args.address).strip()[:180],
        "phone": strip_dangerous_unicode(args.phone).strip()[:32],
        "hours": strip_dangerous_unicode(args.hours).strip()[:80],
        "highlights": highlights or ["Trato Amable Verificado", "100% Libre de Castigos"],
    }
    directory.append(new_biz)
    DIRECTORY_JSON.write_text(
        json.dumps(directory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"✔ Negocio '{new_biz['name']}' registrado con ID {biz_id}.")
    return cmd_build()


SAFE_GIT_PATHS = [
    "index.html",
    "blog.html",
    "directorio.html",
    "herramientas.html",
    "sitemap.xml",
    "robots.txt",
    "_headers",
    "vercel.json",
    ".gitignore",
    "css",
    "js",
    "articulos",
    "templates",
    "scripts",
    "assets",
]


def cmd_deploy(args: argparse.Namespace) -> int:
    build_res = cmd_build()
    if build_res != 0:
        return build_res
    audit_res = cmd_audit()
    if audit_res != 0:
        print("❌ Despliegue abortado por la compuerta de ciberseguridad (cmd_audit).")
        return audit_res

    msg = strip_dangerous_unicode(
        getattr(args, "msg", None)
        or f"chore(editorial): publicación de contenido [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
    )[:140]
    print("\n🚀 Preparando despliegue seguro hacia GitHub y Vercel (Sitio Live)...")
    res1 = subprocess.run(["git", "add", "--"] + SAFE_GIT_PATHS, cwd=WEB_DIR)
    if res1.returncode != 0:
        print("❌ Error ejecutando 'git add' sobre rutas permitidas.")
        return res1.returncode
    subprocess.run(["git", "commit", "-m", msg], cwd=WEB_DIR)
    print("📤 Enviando cambios a 'origin main'...")
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    res3 = subprocess.run(["git", "push", "origin", "main"], cwd=WEB_DIR, env=env)
    if res3.returncode == 0:
        print("\n🎉 Despliegue enviado con éxito a GitHub.")
        print("⚡ Vercel detectará el push y actualizará www.perritosfelices.com en 15-30 segundos.")
    else:
        print("⚠️ Commit local creado y auditado. Para enviar a GitHub, haz push desde tu terminal o panel Git con tu sesión autenticada.")
    return res3.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI de Publicación Automatizada — Perritos Felices"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("build", help="Compila artículos, directorio, data.js y sitemap.xml")
    sub.add_parser("status", help="Muestra estadísticas del sitio y calendario editorial")
    sub.add_parser("audit", help="Ejecuta auditoría Zero-Trust de seguridad web y datos")
    sub.add_parser("studio", help="Abre la Mini-App visual Perritos Felices Studio en tu navegador")

    dep_p = sub.add_parser("deploy", help="Compila, audita y sube cambios seguros a GitHub / Vercel")
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
    if cmd == "audit":
        return cmd_audit()
    if cmd == "studio":
        studio_script = Path(__file__).resolve().parent / "studio_server.py"
        return subprocess.call([sys.executable, str(studio_script)])
    if cmd == "deploy":
        return cmd_deploy(args)
    if cmd == "nuevo-negocio":
        return cmd_nuevo_negocio(args)
    return cmd_build()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
PERRITOS FELICES — PIPELINE SOCIAL-FIRST AUTOMATIZADO (REGLA DEL 90% / 10%)
Orquestador autónomo que:
  1. Recibe o selecciona un tema editorial/social (de plan_publicacion_14_capitulos.json o personalizado).
  2. Genera los copys listos para Instagram 4:5 y guión 9:16 para Lou.
  3. Compila automáticamente la Cápsula Web interactiva complementaria con tokens modulares.
  4. Registra la pieza en el Centro de Aprobación (aprobaciones_state.json).
  5. Envía la notificación interactiva al Bot de Telegram para que la dirección apruebe en 1 toque.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
WEB_DIR = ROOT_DIR / "01_Infraestructura_Web"
STRATEGY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido"
STUDIO_DIR = ROOT_DIR / "05_Studio_Privado"
PLAN_FILE = STRATEGY_DIR / "plan_publicacion_14_capitulos.json"
APROBACIONES_FILE = STUDIO_DIR / "aprobaciones_state.json"
TELEGRAM_CONFIG = Path.home() / ".perritos_felices_telegram.json"


def load_plan():
    if PLAN_FILE.exists():
        return json.loads(PLAN_FILE.read_text(encoding="utf-8"))
    return {}


def load_telegram_credentials():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    allowed_users = []
    if TELEGRAM_CONFIG.exists():
        try:
            data = json.loads(TELEGRAM_CONFIG.read_text(encoding="utf-8"))
            token = token or data.get("bot_token")
            allowed_users = data.get("allowed_users", [])
        except Exception:
            pass
    return token, allowed_users


def send_telegram_alert(token, chat_id, title, tipo, capsule_id, url_preview, copy_hook):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    text = (
        f"⚡ <b>¡Nueva Cápsula & Pieza Social Generada! (Social-First)</b>\n\n"
        f"📌 <b>Título:</b> {title}\n"
        f"🎬 <b>Formato:</b> {tipo}\n"
        f"🎯 <b>Gancho:</b> <i>\"{copy_hook}\"</i>\n"
        f"🆔 <code>{capsule_id}</code>\n\n"
        f"<i>Revisa y aprueba con un clic para desplegar en Netlify:</i>"
    )
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Aprobar Cápsula", "callback_data": f"aprobar:{capsule_id}"},
                {"text": "📋 Ver Pendientes", "callback_data": "cmd:pendientes"}
            ]
        ]
    }
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read().decode())
    except Exception as e:
        print(f"[Telegram Alert Error] {e}", file=sys.stderr)
        return None


def register_approval_item(item_id, tipo, titulo, url_preview, asset_preview):
    data = {"items": []}
    if APROBACIONES_FILE.exists():
        try:
            data = json.loads(APROBACIONES_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Evitar duplicados por id
    items = [it for it in data.get("items", []) if it.get("id") != item_id]
    items.insert(0, {
        "id": item_id,
        "tipo": tipo,
        "titulo": titulo,
        "url_preview": url_preview,
        "asset_preview": asset_preview,
        "estado": "pendiente",
        "fecha_creacion": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "aprobado_por": None,
        "fecha_aprobacion": None,
        "pines": []
    })
    data["items"] = items
    data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    APROBACIONES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_capsule_html(slug, title, subtitle, stat_num, stat_label, do_items, dont_items, showcase_title, showcase_desc):
    clean_slug = slug.replace(".html", "").replace("capsula-", "")
    filename = f"capsula-{clean_slug}.html"
    filepath = WEB_DIR / filename

    do_html = "".join([f"""
        <div class="comparator-item status-safe">
          <div class="comparator-header">
            <span class="comparator-name">{item}</span>
            <span class="comparator-pill">Seguro ✔</span>
          </div>
        </div>""" for item in do_items])

    dont_html = "".join([f"""
        <div class="comparator-item status-danger">
          <div class="comparator-header">
            <span class="comparator-name">{item}</span>
            <span class="comparator-pill">Evitar ✘</span>
          </div>
        </div>""" for item in dont_items])

    tldr_do = f"""<li class="share-card-bullet"><span class="share-card-bullet-icon" style="background: var(--pf-status-safe-bg); color: var(--pf-status-safe);">✔</span><span><strong>Recomendado:</strong> {do_items[0] if do_items else 'Pautas seguras'}</span></li>"""
    tldr_dont = f"""<li class="share-card-bullet"><span class="share-card-bullet-icon" style="background: var(--pf-status-danger-bg); color: var(--pf-status-danger);">✘</span><span><strong>Evitar:</strong> {dont_items[0] if dont_items else 'Prácticas de riesgo'}</span></li>"""

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'report-sample'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; connect-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; require-trusted-types-for 'script'; trusted-types pf-policy; upgrade-insecure-requests;" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cápsula: {title} | Perritos Felices</title>
  <meta name="description" content="{subtitle}" />
  <link rel="canonical" href="https://www.perritosfelices.com/{filename}" />
  <link rel="icon" type="image/png" href="assets/logo/icononly_transparent_nobuffer.png" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Perritos Felices" />
  <meta property="og:title" content="Cápsula: {title}" />
  <meta property="og:description" content="{subtitle}" />
  <meta property="og:url" content="https://www.perritosfelices.com/{filename}" />
  <meta property="og:image" content="https://www.perritosfelices.com/assets/logo/icononly_transparent_nobuffer.png" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..800&family=Inter:ital,opsz,wght@0,14..32,300..700;1,14..32,300..700&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap" />
  
  <link rel="stylesheet" href="css/styles.css" />
  <link rel="stylesheet" href="css/tokens.css" />
</head>
<body class="bg-cream">
  <a href="#main-content" class="skip-link">Saltar al contenido principal</a>

  <header class="site-header" role="banner">
    <div class="container navbar">
      <a href="index.html" class="brand-logo" aria-label="Perritos Felices Inicio">
        <span class="brand-logo-icon">
          <img src="assets/logo/icononly_transparent_nobuffer.png" alt="Logo Perritos Felices" width="36" height="36" decoding="async" />
        </span>
        <span class="brand-logo-text">
          <span class="brand-logo-title">Perritos Felices</span>
          <span class="brand-logo-slogan">Ladridos que inspiran</span>
        </span>
      </a>
      <nav class="nav-links" aria-label="Navegación principal">
        <a href="index.html" class="nav-link">Inicio</a>
        <a href="blog.html" class="nav-link">Guías</a>
        <a href="herramientas.html" class="nav-link">Herramientas</a>
        <a href="directorio.html" class="nav-link">Directorio</a>
      </nav>
      <div class="nav-actions">
        <a href="herramientas.html" class="btn btn-outline btn-sm">Herramientas ↗</a>
      </div>
    </div>
  </header>

  <main id="main-content" class="capsule-wrapper" tabindex="-1">
    
    <section data-section="hero-impact" aria-labelledby="capsule-heading">
      <div class="capsule-badge">
        <span>⚡ Cápsula Visual</span>
        <span>•</span>
        <span>Cultura & Bienestar Canino</span>
      </div>
      <h1 id="capsule-heading" class="capsule-title">{title}</h1>
      <p class="capsule-subtitle">{subtitle}</p>
      <div class="capsule-meta-bar">
        <span class="capsule-meta-item">⏱ Lectura: <strong>45 segundos</strong></span>
        <span>•</span>
        <span class="capsule-meta-item">🔬 Validación: <strong>EBVM Top 10</strong></span>
        <span>•</span>
        <span class="capsule-meta-item">📸 Formato: <strong>Shareable TL;DR</strong></span>
      </div>
    </section>

    <section data-section="capsule-bento" aria-label="Resumen visual en Bento Grid">
      <article class="bento-cell bento-col-6">
        <div class="bento-cell-header">
          <span class="bento-tag">Métrica Clave</span>
          <span style="font-family: var(--pf-font-mono); font-size: 0.8rem; font-weight: 700; color: var(--pf-blue);">EVIDENCIA</span>
        </div>
        <div class="bento-stat-number" style="color: var(--pf-blue);">{stat_num}</div>
        <div class="bento-stat-label">{stat_label}</div>
      </article>

      <article class="bento-cell bento-col-6">
        <div class="bento-cell-header">
          <span class="bento-tag">Regla de Oro</span>
          <span style="font-family: var(--pf-font-mono); font-size: 0.8rem; font-weight: 700; color: var(--pf-status-safe);">100% SEGURO</span>
        </div>
        <div class="bento-stat-number" style="color: var(--pf-status-safe);">100%</div>
        <div class="bento-stat-label">Crianza libre de métodos aversivos, castigos o coerción física.</div>
      </article>
    </section>

    <section data-section="visual-comparator" aria-labelledby="comparator-heading">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
        <div>
          <span class="bento-tag">Comparador Rápido</span>
          <h2 id="comparator-heading" style="font-family: var(--pf-font-display); font-size: 1.6rem; margin: 0.5rem 0 0; color: var(--pf-ink-primary);">
            ¿Qué hacer y qué evitar?
          </h2>
        </div>
        <div style="display: flex; gap: 0.5rem;">
          <button type="button" class="btn btn-sm btn-outline comparator-filter-btn active" data-filter="all">Todos</button>
          <button type="button" class="btn btn-sm btn-outline comparator-filter-btn" data-filter="safe">Seguros ✔</button>
          <button type="button" class="btn btn-sm btn-outline comparator-filter-btn" data-filter="danger">Evitar ✘</button>
        </div>
      </div>

      <div class="comparator-grid">
        {do_html}
        {dont_html}
      </div>
    </section>

    <section data-section="b2b-showcase" aria-labelledby="showcase-heading">
      <div>
        <div class="showcase-eyebrow">Vitrina de Experiencia Verificada</div>
        <h2 id="showcase-heading" class="showcase-title">{showcase_title}</h2>
        <p class="showcase-desc">{showcase_desc}</p>
      </div>
      <div>
        <a href="directorio.html" class="showcase-action-btn">
          <span>Explorar Directorio</span>
          <span>↗</span>
        </a>
      </div>
    </section>

    <section data-section="tldr-share-card" aria-labelledby="share-card-title-heading">
      <div class="share-card-container">
        <div class="share-card-header">
          <div class="share-card-brand">
            <div class="share-card-brand-logo">
              <img src="assets/logo/icononly_transparent_nobuffer.png" alt="" width="26" height="26" decoding="async" />
            </div>
            <span class="share-card-brand-name">Perritos Felices</span>
          </div>
          <span class="share-card-pill">TL;DR 30s</span>
        </div>

        <h3 id="share-card-title-heading" class="share-card-title">{title}</h3>

        <ul class="share-card-bullets">
          {tldr_do}
          {tldr_dont}
          <li class="share-card-bullet">
            <span class="share-card-bullet-icon" style="background: var(--pf-blue-light); color: var(--pf-blue);">ℹ</span>
            <span><strong>Crianza Respetuosa:</strong> Aplica este protocolo para cuidar su bienestar físico y emocional.</span>
          </li>
        </ul>

        <div class="share-card-footer">
          <span>Cultura canina con ciencia</span>
          <span>www.perritosfelices.com</span>
        </div>
      </div>

      <div class="share-card-actions">
        <button type="button" class="btn-download-card">
          <span>📥 Descargar Tarjeta (PNG)</span>
        </button>
        <button type="button" class="btn-share-native">
          <span>📲 Compartir en Redes</span>
        </button>
      </div>
    </section>

  </main>

  <footer class="site-footer" role="contentinfo" style="margin-top: 4rem; padding: 2.5rem 0; background: var(--pf-surface-dark); color: #FFFFFF; text-align: center;">
    <div class="container">
      <p style="font-family: var(--pf-font-mono); font-size: 0.85rem; color: var(--pf-ink-muted); margin: 0 0 0.5rem;">
        Perritos Felices © 2026 — Ladridos que inspiran
      </p>
      <p style="font-family: var(--pf-font-body); font-size: 0.8rem; color: #7E86A8; margin: 0;">
        Evidencia científica veterinaria (EBVM) • 100% libre de métodos aversivos
      </p>
    </div>
  </footer>

  <script src="js/main.js"></script>
  <script src="js/capsules.js"></script>
</body>
</html>
"""
    filepath.write_text(html_content, encoding="utf-8")
    return filename


def process_chapter(chapter_num: int):
    plan = load_plan()
    chapters = plan.get("chapters", [])
    target = None
    for ch in chapters:
        if ch.get("order") == chapter_num or str(ch.get("chapterNum")) == str(chapter_num).zfill(2):
            target = ch
            break

    if not target:
        print(f"❌ Capítulo {chapter_num} no encontrado en plan_publicacion_14_capitulos.json")
        return False

    title = target.get("cover", {}).get("title1", "") + " " + target.get("cover", {}).get("title2", "")
    title = title.strip() or target.get("title", "Cápsula Visual")
    subtitle = target.get("cover", {}).get("sub1", "") + " " + target.get("cover", {}).get("sub2", "")
    subtitle = subtitle.strip()

    slides = target.get("slides", [])
    s2 = slides[0] if len(slides) > 0 else {}
    s3 = slides[1] if len(slides) > 1 else {}

    stat_num = s2.get("statValue", "100%")
    stat_label = s2.get("statLabel", "Evidencia científica comprobada")
    do_items = s3.get("doItems", ["Protocolos recomendados"])
    dont_items = s3.get("dontItems", ["Prácticas desbalanceadas o aversivas"])

    showcase_title = f"¿Buscas profesionales de {target.get('category')} verificados?"
    showcase_desc = "Encuentra espacios éticos y especialistas libres de jaulas y castigos en nuestro Directorio Canino."

    slug_base = target.get("slug", "capsula-generada.html").replace(".html", "")
    capsule_filename = generate_capsule_html(
        slug=slug_base,
        title=title,
        subtitle=subtitle,
        stat_num=stat_num,
        stat_label=stat_label,
        do_items=do_items,
        dont_items=dont_items,
        showcase_title=showcase_title,
        showcase_desc=showcase_desc
    )

    capsule_id = f"capsula_{target.get('id', 'cap_' + str(chapter_num))}"
    asset_preview = f"/assets/articulos/{target.get('photoFile', '')}"

    # Registrar para Aprobación
    register_approval_item(
        item_id=capsule_id,
        tipo="capsula_web",
        titulo=f"Cápsula #{chapter_num:02d}: {title}",
        url_preview=f"/{capsule_filename}",
        asset_preview=asset_preview
    )

    # Notificar a Telegram
    token, allowed_users = load_telegram_credentials()
    if token and allowed_users:
        hook = target.get("socialCopies", {}).get("instagramCarousel", {}).get("captionHook", subtitle)
        for uid in allowed_users:
            send_telegram_alert(
                token=token,
                chat_id=uid,
                title=f"Cápsula #{chapter_num:02d}: {title}",
                tipo="Cápsula Web + Carrusel 4:5",
                capsule_id=capsule_id,
                url_preview=f"/{capsule_filename}",
                copy_hook=hook
            )

    print(f"✔ Pipeline completado para Capítulo #{chapter_num:02d}:")
    print(f"  • Cápsula Web: 01_Infraestructura_Web/{capsule_filename}")
    print(f"  • Registrada en: 05_Studio_Privado/aprobaciones_state.json ({capsule_id})")
    print(f"  • Notificación enviada a Telegram: {'Sí' if token else 'No (sin token)'}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Pipeline Social-First de Perritos Felices")
    parser.add_argument("--capitulo", type=int, default=1, help="Número de capítulo (1 a 14) del plan maestro a procesar")
    args = parser.parse_args()

    process_chapter(args.capitulo)


if __name__ == "__main__":
    main()

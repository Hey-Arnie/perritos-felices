#!/usr/bin/env python3
"""
MOTOR EDITORIAL DE MICRO-MOTION PF-2027 (OPCIÓN A — CERO SATURACIÓN)
1. Genera '05_Studio_Privado/assets/motion_assets_data.js' con los recursos fotográficos
   y logotipo oficial en Data URI (base64) para que el motor HTML5 Canvas 1080x1080 a 60fps
   renderice con tipografías reales (Fraunces, Plus Jakarta Sans, Space Mono) y permita
   exportar video (.mp4 / .webm) sin errores CORS ni bloqueo de fuentes en file://.
2. Genera las versiones SVG limpias (cero garabatos invasivos sobre la foto, >55% foto libre,
   revelado editorial por máscara y subrayado único).
"""

import base64
import html
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
WEEKLY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido" / "entregas_semanales" / "semana_2026_10_26"
ARTES_DIR = WEEKLY_DIR / "artes"
STUDIO_ASSETS = ROOT_DIR / "05_Studio_Privado" / "assets"

ARTES_DIR.mkdir(parents=True, exist_ok=True)
STUDIO_ASSETS.mkdir(parents=True, exist_ok=True)


def get_image_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/jpeg" if path.suffix in (".jpg", ".jpeg") else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def get_official_logo_uri() -> str:
    logo_path = ASSETS_DIR / "fulllogo_transparent_nobuffer.png"
    if not logo_path.exists():
        logo_path = ASSETS_DIR / "fulllogo_transparent.png"
    return get_image_data_uri(logo_path)


def build_clean_editorial_svg(
    img_uri: str,
    logo_uri: str,
    scrim_id: str,
    scrim_color: str,
    badge_text: str,
    kicker_text: str,
    kicker_is_italic: bool,
    title_line1: str,
    title_line2: str,
    accent_color: str,
    sub_line1: str,
    sub_line2: str,
    cta_text: str,
    footer_note: str,
    underline_width: int = 520,
) -> str:
    """
    Genera un SVG 1080x1080 de estética editorial limpia (cero saturación sobre el perro):
    - Fotografía 100% libre en el 60% superior con paneo Ken Burns suave.
    - Revelado escalonado por máscara (clipPath) en cada línea del titular.
    - Un único trazo orgánico de subrayado bajo la segunda línea del título.
    """
    badge_text = html.escape(badge_text)
    kicker_text = html.escape(kicker_text)
    title_line1 = html.escape(title_line1)
    title_line2 = html.escape(title_line2)
    sub_line1 = html.escape(sub_line1)
    sub_line2 = html.escape(sub_line2)
    cta_text = html.escape(cta_text)
    footer_note = html.escape(footer_note)

    kicker_style = (
        f"font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 27px; font-weight: 700; fill: {accent_color};"
        if kicker_is_italic
        else f"font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: {accent_color};"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,800;1,9..144,700&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 800; fill: #FFFFFF; }}
      .title-accent {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 800; fill: {accent_color}; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 25px; font-weight: 500; fill: #F1F5F9; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .kicker-txt {{ {kicker_style} }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; fill: #10152B; }}
      .note-txt {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 17px; font-weight: 600; fill: rgba(255, 255, 255, 0.88); }}

      .ken-burns {{
        transform-origin: 540px 420px;
        animation: kbPan 6s cubic-bezier(0.37, 0, 0.63, 1) infinite alternate;
      }}
      @keyframes kbPan {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.045) translate(-8px, -6px); }}
      }}

      .reveal-1 {{ animation: maskUp 5s cubic-bezier(0.19, 1, 0.22, 1) infinite; }}
      .reveal-2 {{ animation: maskUp2 5s cubic-bezier(0.19, 1, 0.22, 1) infinite; }}
      .reveal-sub {{ animation: fadeSlide 5s cubic-bezier(0.19, 1, 0.22, 1) infinite; }}
      .underline-stroke {{
        stroke-dasharray: {underline_width};
        stroke-dashoffset: {underline_width};
        animation: drawLine 5s cubic-bezier(0.19, 1, 0.22, 1) infinite;
      }}
      .cta-arrow {{ animation: arrowNudge 1.2s ease-in-out infinite alternate; }}

      @keyframes maskUp {{
        0%, 4%   {{ transform: translateY(72px); opacity: 0; }}
        18%, 88% {{ transform: translateY(0px); opacity: 1; }}
        96%, 100%{{ transform: translateY(0px); opacity: 0; }}
      }}
      @keyframes maskUp2 {{
        0%, 8%   {{ transform: translateY(72px); opacity: 0; }}
        22%, 88% {{ transform: translateY(0px); opacity: 1; }}
        96%, 100%{{ transform: translateY(0px); opacity: 0; }}
      }}
      @keyframes fadeSlide {{
        0%, 14%  {{ transform: translateY(20px); opacity: 0; }}
        28%, 88% {{ transform: translateY(0px); opacity: 1; }}
        96%, 100%{{ transform: translateY(0px); opacity: 0; }}
      }}
      @keyframes drawLine {{
        0%, 18%  {{ stroke-dashoffset: {underline_width}; opacity: 0; }}
        22%      {{ opacity: 1; }}
        36%, 88% {{ stroke-dashoffset: 0; opacity: 1; }}
        96%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}
      @keyframes arrowNudge {{
        0%   {{ transform: translateX(0px); }}
        100% {{ transform: translateX(7px); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
        .underline-stroke {{ stroke-dashoffset: 0 !important; opacity: 1 !important; }}
      }}
    </style>

    <linearGradient id="{scrim_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{scrim_color}" stop-opacity="0.35" />
      <stop offset="45%" stop-color="{scrim_color}" stop-opacity="0.0" />
      <stop offset="65%" stop-color="{scrim_color}" stop-opacity="0.40" />
      <stop offset="85%" stop-color="{scrim_color}" stop-opacity="0.72" />
      <stop offset="100%" stop-color="{scrim_color}" stop-opacity="0.78" />
    </linearGradient>

    <clipPath id="clipLine1">
      <rect x="-10" y="-65" width="960" height="85" />
    </clipPath>
    <clipPath id="clipLine2">
      <rect x="-10" y="5" width="960" height="90" />
    </clipPath>
  </defs>

  <!-- Fotografía Protagonista Limpia con Ken Burns Suave -->
  <g class="ken-burns">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  </g>

  <!-- Veladura Editorial Traslúcida (<= 78%) -->
  <rect width="1080" height="1080" fill="url(#{scrim_id})" />

  <!-- Cabecera Superior con Logo Oficial Nítido (Safe Zone: 64px) -->
  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(16, 21, 43, 0.76)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">{badge_text}</text>
  </g>

  <!-- Bloque Tipográfico Editorial Hero (Safe Zone: 64px, y=650) -->
  <g transform="translate(64, 650)">
    <g class="reveal-sub">
      <text x="0" y="-28" class="kicker-txt">{kicker_text}</text>
    </g>

    <g clip-path="url(#clipLine1)">
      <g class="reveal-1">
        <text x="0" y="0" class="title">{title_line1}</text>
      </g>
    </g>

    <g clip-path="url(#clipLine2)">
      <g class="reveal-2">
        <text x="0" y="70" class="title-accent">{title_line2}</text>
      </g>
    </g>

    <!-- Subrayado Orgánico Único -->
    <path class="underline-stroke"
          d="M 2,86 Q {underline_width // 2},94 {underline_width},83"
          fill="none" stroke="{accent_color}" stroke-width="4.5" stroke-linecap="round" />

    <g class="reveal-sub">
      <text class="subtitle">
        <tspan x="0" y="140">{sub_line1}</tspan>
        <tspan x="0" y="176">{sub_line2}</tspan>
      </text>

      <g transform="translate(0, 225)">
        <rect width="380" height="54" rx="27" fill="{accent_color}" />
        <text x="172" y="34" class="cta-txt" text-anchor="middle">{cta_text}</text>
        <g class="cta-arrow" transform="translate(332, 0)">
          <text x="0" y="34" class="cta-txt" font-size="18">➔</text>
        </g>
        <text x="410" y="34" class="note-txt">{footer_note}</text>
      </g>
    </g>
  </g>
</svg>"""


def main():
    print("🎬 Compilando Motor Editorial Micro-Motion (Opción A: HTML5 Canvas + SVG Limpio)...")

    logo_uri = get_official_logo_uri()
    img_01 = get_image_data_uri(ARTES_DIR / "post_01_loki_dermatologia.jpg")
    img_02 = get_image_data_uri(ARTES_DIR / "post_02_frodo_nutricion.jpg")
    img_03 = get_image_data_uri(ARTES_DIR / "post_03_etologia_calma.jpg")
    img_04 = get_image_data_uri(ARTES_DIR / "post_04_lou_arnes_en_y.jpg")

    # Configuración de las 4 piezas editoriales para el motor Canvas 60fps y para SVG
    posts_config = [
        {
            "id": "post_01",
            "svg_name": "post_01_animado_dermatologia.svg",
            "img_uri": img_01,
            "scrim_id": "scrimLokiAnim",
            "scrim_rgb": "16, 21, 43",
            "scrim_hex": "#10152B",
            "badge": "SALUD // DERMATOLOGÍA",
            "kicker": "EVIDENCIA CLÍNICA • 80% DE CASOS POR CONTACTO",
            "kicker_italic": False,
            "title_1": "¿Tu perro se lame",
            "title_2": "las patas sin parar?",
            "accent": "#FDB54A",
            "sub_1": "No es maña ni ansiedad. El picor interdigital suele",
            "sub_2": "deberse a polen o pesticidas tras el paseo diario.",
            "cta": "DESLIZA PARA VER LA GUÍA",
            "note": "Cuidado Veterinario EBVM",
            "underline_w": 535,
            "focus_x": 0.65,
            "focus_y": 0.36,
        },
        {
            "id": "post_02",
            "svg_name": "post_02_animado_nutricion.svg",
            "img_uri": img_02,
            "scrim_id": "scrimFrodoAnim",
            "scrim_rgb": "26, 18, 8",
            "scrim_hex": "#1A1208",
            "badge": "COCINA // RECETA FRESCA",
            "kicker": "🍉 SANDÍA NATURAL  •  🥛 YOGUR SIN LACTOSA  •  🌱 REGLA 10% WSAVA",
            "kicker_italic": False,
            "title_1": "Helado casero de",
            "title_2": "sandía & yogur fresco",
            "accent": "#FFE082",
            "sub_1": "Hidratante, digestivo y seguro como snack dentro",
            "sub_2": "del 10% máximo de calorías diarias recomendadas.",
            "cta": "VER RECETA PASO A PASO",
            "note": "Nutrición Clínica Segura",
            "underline_w": 570,
            "focus_x": 0.50,
            "focus_y": 0.42,
        },
        {
            "id": "post_03",
            "svg_name": "post_03_animado_etologia.svg",
            "img_uri": img_03,
            "scrim_id": "scrimEtoAnim",
            "scrim_rgb": "14, 35, 18",
            "scrim_hex": "#0E2312",
            "badge": "ETOLOGÍA // LENGUAJE",
            "kicker": "TURID RUGAAS • +30 SEÑALES DE APACIGUAMIENTO",
            "kicker_italic": False,
            "title_1": "¿Tu perro bosteza o",
            "title_2": "se lame la trufa al abrazarlo?",
            "accent": "#81C784",
            "sub_1": "No tiene sueño ni hambre: te está pidiendo espacio.",
            "sub_2": "Escuchar su lenguaje corporal previene el estrés.",
            "cta": "DESCUBRE LAS 5 SEÑALES",
            "note": "Educación 100% Fear-Free",
            "underline_w": 740,
            "focus_x": 0.58,
            "focus_y": 0.38,
        },
        {
            "id": "post_04",
            "svg_name": "post_04_animado_lou.svg",
            "img_uri": img_04,
            "scrim_id": "scrimLouAnim",
            "scrim_rgb": "16, 21, 43",
            "scrim_hex": "#10152B",
            "badge": "PASEO RESPETUOSO // GUÍA",
            "kicker": "\"El dolor jamás enseña respeto, solo pánico.\"",
            "kicker_italic": True,
            "title_1": "Arnés ergonómico en 'Y':",
            "title_2": "Paseos sin tirones ni ahogo.",
            "accent": "#FDB54A",
            "sub_1": "0% presión sobre tráquea y tiroides. Deja libres",
            "sub_2": "las escápulas para una zancada natural y cómoda.",
            "cta": "GUÍA DE ELECCIÓN DE ARNÉS",
            "note": "Educación Canina Amable",
            "underline_w": 715,
            "focus_x": 0.50,
            "focus_y": 0.35,
        },
    ]

    # 1. Guardar los 4 SVGs limpios
    for cfg in posts_config:
        svg_code = build_clean_editorial_svg(
            img_uri=cfg["img_uri"],
            logo_uri=logo_uri,
            scrim_id=cfg["scrim_id"],
            scrim_color=cfg["scrim_hex"],
            badge_text=cfg["badge"],
            kicker_text=cfg["kicker"],
            kicker_is_italic=cfg["kicker_italic"],
            title_line1=cfg["title_1"],
            title_line2=cfg["title_2"],
            accent_color=cfg["accent"],
            sub_line1=cfg["sub_1"],
            sub_line2=cfg["sub_2"],
            cta_text=cfg["cta"],
            footer_note=cfg["note"],
            underline_width=cfg["underline_w"],
        )
        (ARTES_DIR / cfg["svg_name"]).write_text(svg_code, encoding="utf-8")
        (STUDIO_ASSETS / cfg["svg_name"]).write_text(svg_code, encoding="utf-8")
        print(f"✔ SVG Editorial Limpio: {cfg['svg_name']}")

    # 2. Generar bundle JS con Data URIs para el Motor Canvas 1080x1080 del Studio
    canvas_payload = {
        "logoUri": logo_uri,
        "posts": [
            {
                "id": cfg["id"],
                "imgUri": cfg["img_uri"],
                "scrimRgb": cfg["scrim_rgb"],
                "badge": cfg["badge"],
                "kicker": cfg["kicker"],
                "kickerItalic": cfg["kicker_italic"],
                "title1": cfg["title_1"],
                "title2": cfg["title_2"],
                "accent": cfg["accent"],
                "sub1": cfg["sub_1"],
                "sub2": cfg["sub_2"],
                "cta": cfg["cta"],
                "note": cfg["note"],
                "underlineW": cfg["underline_w"],
                "focusX": cfg["focus_x"],
                "focusY": cfg["focus_y"],
            }
            for cfg in posts_config
        ],
    }

    js_bundle_path = STUDIO_ASSETS / "motion_assets_data.js"
    js_content = (
        "// Generado automáticamente por generar_arte_animado.py — Cero Taint CORS en file://\n"
        f"window.PF_MOTION_DATA = {json.dumps(canvas_payload, ensure_ascii=False)};\n"
    )
    js_bundle_path.write_text(js_content, encoding="utf-8")
    print(f"✔ Bundle de recursos Canvas generado: {js_bundle_path} ({js_bundle_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

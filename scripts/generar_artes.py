#!/usr/bin/env python3
"""
GENERADOR DE ARTES EDITORIALES PARA REDES SOCIALES (PF-2027 SOCIAL-FIRST)
Inspirado en Hue (Brand-Consistent Design Systems) e InstaLanding (Clean-Slate Modular Assets)
Produce piezas verticales 4:5 (1080x1350) para las 5 Cápsulas Visuales con >68% de fotografía limpia.
"""

import base64
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
WEB_ASSETS = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos"
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
        logo_path = ASSETS_DIR / "pack_logos_originales_master" / "fulllogo_transparent_nobuffer.png"
    if not logo_path.exists():
        logo_path = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "logo" / "fulllogo_transparent_nobuffer.png"
    return get_image_data_uri(logo_path)


# ARTE 1: TOXICOLOGÍA (UVAS VS ZANAHORIA)
def generar_arte_toxicidad() -> str:
    img_path = WEB_ASSETS / "snacks-hidratantes-caseros-perros.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&amp;family=Inter:wght@600;700&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 68px; font-weight: 800; fill: #FFFFFF; line-height: 1.05; letter-spacing: -0.02em; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 600; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #10152B; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FDB54A; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimTox" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.35" />
      <stop offset="45%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#10152B" stop-opacity="0.5" />
      <stop offset="88%" stop-color="#10152B" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.82" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimTox)" />

  <g transform="translate(64, 64)">
    <rect width="420" height="58" rx="29" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
    <image href="{logo_uri}" x="10" y="6" width="46" height="46" preserveAspectRatio="xMidYMid meet" />
    <text x="68" y="36" class="badge-txt">⚡ CÁPSULA #01 // TOXICOLOGÍA</text>
  </g>

  <g transform="translate(64, 880)">
    <text x="0" y="-24" class="kicker-txt">CONSENSO VETERINARIO WSAVA &amp; ASPCA APCC</text>
    <text class="title">
      <tspan x="0" y="42">¿Una sola uva?</tspan>
      <tspan x="0" y="118" class="title-accent">Falla renal en 24h</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="185">No hay dosis segura conocida. Descubre por qué</tspan>
      <tspan x="0" y="225">la zanahoria es la alternativa crujiente 100% segura.</tspan>
    </text>

    <g transform="translate(0, 275)">
      <rect width="360" height="54" rx="27" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
      <text x="32" y="34" class="cta-txt">DESLIZA EL CARRUSEL ➔</text>
    </g>
  </g>
</svg>"""


# ARTE 2: BIOMECÁNICA (ARNÉS EN Y)
def generar_arte_arnes() -> str:
    img_path = WEB_ASSETS / "como-elegir-arnes-en-y-perros.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&amp;family=Inter:wght@600;700&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 68px; font-weight: 800; fill: #FFFFFF; line-height: 1.05; letter-spacing: -0.02em; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 600; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #10152B; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FDB54A; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimArnes" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.35" />
      <stop offset="45%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#10152B" stop-opacity="0.5" />
      <stop offset="88%" stop-color="#10152B" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.82" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimArnes)" />

  <g transform="translate(64, 64)">
    <rect width="420" height="58" rx="29" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
    <image href="{logo_uri}" x="10" y="6" width="46" height="46" preserveAspectRatio="xMidYMid meet" />
    <text x="68" y="36" class="badge-txt">⚡ CÁPSULA #02 // BIOMECÁNICA</text>
  </g>

  <g transform="translate(64, 880)">
    <text x="0" y="-24" class="kicker-txt">BIOMECÁNICA CANINA &amp; PASEO RESPETUOSO</text>
    <text class="title">
      <tspan x="0" y="42">Su cuello no es un parachoques:</tspan>
      <tspan x="0" y="118" class="title-accent">la regla del arnés en "Y"</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="185">Protege su tráquea, tiroides y escápulas.</tspan>
      <tspan x="0" y="225">Por qué el collar tradicional lesiona su respiración.</tspan>
    </text>

    <g transform="translate(0, 275)">
      <rect width="360" height="54" rx="27" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
      <text x="32" y="34" class="cta-txt">DESLIZA EL CARRUSEL ➔</text>
    </g>
  </g>
</svg>"""


# ARTE 3: ETOLOGÍA (SEÑALES DE CALMA)
def generar_arte_calma() -> str:
    img_path = WEB_ASSETS / "lenguaje-corporal-canino-senales.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&amp;family=Inter:wght@600;700&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 68px; font-weight: 800; fill: #FFFFFF; line-height: 1.05; letter-spacing: -0.02em; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 600; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #10152B; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FDB54A; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimCalma" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.35" />
      <stop offset="45%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#10152B" stop-opacity="0.5" />
      <stop offset="88%" stop-color="#10152B" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.82" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimCalma)" />

  <g transform="translate(64, 64)">
    <rect width="420" height="58" rx="29" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
    <image href="{logo_uri}" x="10" y="6" width="46" height="46" preserveAspectRatio="xMidYMid meet" />
    <text x="68" y="36" class="badge-txt">⚡ CÁPSULA #03 // ETOLOGÍA</text>
  </g>

  <g transform="translate(64, 880)">
    <text x="0" y="-24" class="kicker-txt">ETOLOGÍA CLÍNICA • TURID RUGAAS</text>
    <text class="title">
      <tspan x="0" y="42">Mover la cola</tspan>
      <tspan x="0" y="118" class="title-accent">no siempre es alegría</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="185">Decodifica el bostezo, el lamido y el desvío</tspan>
      <tspan x="0" y="225">de mirada antes de que aparezca el estrés.</tspan>
    </text>

    <g transform="translate(0, 275)">
      <rect width="360" height="54" rx="27" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
      <text x="32" y="34" class="cta-txt">DESLIZA EL CARRUSEL ➔</text>
    </g>
  </g>
</svg>"""


# ARTE 4: DERMATOLOGÍA (ALERGIAS & PATITAS)
def generar_arte_alergias() -> str:
    img_path = WEB_ASSETS / "alergias-alimentarias-ambientales-perros-guia.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&amp;family=Inter:wght@600;700&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 68px; font-weight: 800; fill: #FFFFFF; line-height: 1.05; letter-spacing: -0.02em; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 600; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #10152B; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FDB54A; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimAlergia" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.35" />
      <stop offset="45%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#10152B" stop-opacity="0.5" />
      <stop offset="88%" stop-color="#10152B" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.82" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimAlergia)" />

  <g transform="translate(64, 64)">
    <rect width="420" height="58" rx="29" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
    <image href="{logo_uri}" x="10" y="6" width="46" height="46" preserveAspectRatio="xMidYMid meet" />
    <text x="68" y="36" class="badge-txt">⚡ CÁPSULA #04 // DERMATOLOGÍA</text>
  </g>

  <g transform="translate(64, 880)">
    <text x="0" y="-24" class="kicker-txt">DERMATOLOGÍA CLÍNICA • CONSENSO ICADA</text>
    <text class="title">
      <tspan x="0" y="42">¿Se lame las patas sin parar?</tspan>
      <tspan x="0" y="118" class="title-accent">No es manía: es prurito</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="185">Aprende a diferenciar la atopia ambiental</tspan>
      <tspan x="0" y="225">por polen de la intolerancia alimentaria.</tspan>
    </text>

    <g transform="translate(0, 275)">
      <rect width="360" height="54" rx="27" fill="#FDB54A" stroke="#10152B" stroke-width="2" />
      <text x="32" y="34" class="cta-txt">DESLIZA EL CARRUSEL ➔</text>
    </g>
  </g>
</svg>"""


def main():
    artes = {
        "arte_01_toxicidad_45.svg": generar_arte_toxicidad(),
        "arte_02_arnes_45.svg": generar_arte_arnes(),
        "arte_03_calma_45.svg": generar_arte_calma(),
        "arte_04_alergias_45.svg": generar_arte_alergias()
    }

    print("🎨 Generando nuevos artes 4:5 estilo Hue e InstaLanding...")
    for filename, svg_data in artes.items():
        out_p = ARTES_DIR / filename
        out_p.write_text(svg_data, encoding="utf-8")
        # Copiar también a Studio
        (STUDIO_ASSETS / filename).write_text(svg_data, encoding="utf-8")
        print(f"  ✔ {filename} generado ({len(svg_data)} bytes)")

    # Empaquetar ZIP descargable para Studio
    zip_path = STUDIO_ASSETS / "kit_descargables_semana_2026_10_26.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename in artes.keys():
            f_path = ARTES_DIR / filename
            if f_path.exists():
                zf.write(f_path, arcname=filename)
    print(f"📦 Kit ZIP regenerado en: {zip_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GENERADOR DE LÍNEA GRÁFICA EDITORIAL PF-2027 (Perritos Felices Studio)
Produce artes vectoriales verticales 4:5 (1080x1350) con jerarquía tipográfica Fraunces / Space Mono,
paleta oficial (#2C4BCA, #FDB54A, #FDFBF7, #10152B, #E8EDFF, #EAF2EB, #FFF3E0) y >60% de fotografía libre.
"""

import base64
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
WEEKLY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido" / "entregas_semanales" / "semana_2026_10_26"
ARTES_DIR = WEEKLY_DIR / "artes"
VIDEOS_DIR = WEEKLY_DIR / "videos"
STUDIO_ASSETS = ROOT_DIR / "05_Studio_Privado" / "assets"

ARTES_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
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


# 1. PLANTILLA 1 (4:5 - 1080x1350): PILAR A (SALUD & CLÍNICA — AZUL GLACIAL #E8EDFF + AMARILLOPF #FDB54A)
def generar_arte_loki() -> str:
    loki_img = ARTES_DIR / "post_01_loki_dermatologia.jpg"
    if not loki_img.exists():
        loki_img = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos" / "alergias-alimentarias-ambientales-perros-guia.jpg"
    img_uri = get_image_data_uri(loki_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 64px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 500; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FDB54A; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimLoki45" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.32" />
      <stop offset="48%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#10152B" stop-opacity="0.42" />
      <stop offset="86%" stop-color="#10152B" stop-opacity="0.72" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.78" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimLoki45)" />

  <g transform="translate(64, 64)">
    <rect width="390" height="56" rx="28" fill="rgba(16, 21, 43, 0.78)" stroke="rgba(232, 237, 255, 0.32)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="34" class="badge-txt">SALUD // DERMATOLOGÍA</text>
  </g>

  <g transform="translate(64, 860)">
    <text x="0" y="-26" class="kicker-txt">PILAR SALUD • EVIDENCIA ICADA &amp; UC DAVIS</text>
    <text class="title">
      <tspan x="0" y="36">¿Tu perro se lame</tspan>
      <tspan x="0" y="108" class="title-accent">las patas sin parar?</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="172">No es maña ni ansiedad. El 80% de los casos es picor</tspan>
      <tspan x="0" y="210">alérgico por polen o químicos tras el paseo diario.</tspan>
    </text>
    <g transform="translate(0, 260)">
      <rect width="380" height="58" rx="29" fill="#FDB54A" />
      <text x="190" y="35" class="cta-txt" text-anchor="middle">DESLIZA EL CARRUSEL ➔</text>
      <text x="410" y="35" font-family="Plus Jakarta Sans" font-size="18" font-weight="600" fill="#E8EDFF">Formato 4:5 • 5 Láminas</text>
    </g>
  </g>
</svg>"""


# 2. PLANTILLA 2 (4:5 - 1080x1350): PILAR B (NUTRICIÓN & NATURALEZA — MENTA BOTÁNICA #EAF2EB + DORADO #FFE082)
def generar_arte_frodo() -> str:
    frodo_img = ARTES_DIR / "post_02_frodo_nutricion.jpg"
    if not frodo_img.exists():
        frodo_img = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos" / "guia-alimentacion-natural-perros.jpg"
    img_uri = get_image_data_uri(frodo_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 62px; font-weight: 800; fill: #FDFBF7; line-height: 1.08; }}
      .title-accent {{ fill: #FFE082; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 25px; font-weight: 500; fill: #EAF2EB; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFE082; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimFrodo45" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E2318" stop-opacity="0.32" />
      <stop offset="48%" stop-color="#0E2318" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#0E2318" stop-opacity="0.42" />
      <stop offset="86%" stop-color="#0E2318" stop-opacity="0.72" />
      <stop offset="100%" stop-color="#0E2318" stop-opacity="0.78" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimFrodo45)" />

  <g transform="translate(64, 64)">
    <rect width="390" height="56" rx="28" fill="rgba(14, 35, 24, 0.78)" stroke="rgba(234, 242, 235, 0.35)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="34" class="badge-txt">CAPÍTULO 01 // NUTRICIÓN</text>
  </g>

  <g transform="translate(64, 860)">
    <text x="0" y="-26" class="kicker-txt">CONSENSO WSAVA &amp; FEDIAF • REGLA DEL 10%</text>
    <text class="title">
      <tspan x="0" y="36">Alimentación natural:</tspan>
      <tspan x="0" y="108" class="title-accent">la regla del 10% seguro</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="172">Cómo sumar snacks frescos e hidratantes sin</tspan>
      <tspan x="0" y="210">desbalancear el calcio y fósforo de su plato diario.</tspan>
    </text>
    <g transform="translate(0, 260)">
      <rect width="380" height="58" rx="29" fill="#FFE082" />
      <text x="190" y="35" class="cta-txt" text-anchor="middle">VER GUÍA EN 5 LÁMINAS ➔</text>
      <text x="410" y="35" font-family="Plus Jakarta Sans" font-size="18" font-weight="600" fill="#EAF2EB">Pilar Nutrición • #EAF2EB</text>
    </g>
  </g>
</svg>"""


# 3. PLANTILLA 3 (4:5 - 1080x1350): PILAR C (ETOLOGÍA & VÍNCULO — DURAZNO SUAVE #FFF3E0 + AMARILLOPF #FDB54A)
def generar_arte_etologia() -> str:
    eto_img = ARTES_DIR / "post_03_etologia_calma.jpg"
    if not eto_img.exists():
        eto_img = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos" / "lenguaje-corporal-canino-senales.jpg"
    img_uri = get_image_data_uri(eto_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 800; fill: #FDFBF7; line-height: 1.08; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 25px; font-weight: 500; fill: #FFF3E0; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .kicker-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FDB54A; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimEto45" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1E1610" stop-opacity="0.32" />
      <stop offset="48%" stop-color="#1E1610" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#1E1610" stop-opacity="0.42" />
      <stop offset="86%" stop-color="#1E1610" stop-opacity="0.72" />
      <stop offset="100%" stop-color="#1E1610" stop-opacity="0.78" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimEto45)" />

  <g transform="translate(64, 64)">
    <rect width="390" height="56" rx="28" fill="rgba(30, 22, 16, 0.78)" stroke="rgba(255, 243, 224, 0.35)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="34" class="badge-txt">CAPÍTULO 02 // ETOLOGÍA</text>
  </g>

  <g transform="translate(64, 860)">
    <text x="0" y="-26" class="kicker-txt">TURID RUGAAS • 15 SEÑALES DE CALMA</text>
    <text class="title">
      <tspan x="0" y="36">¿Tu perro bosteza o</tspan>
      <tspan x="0" y="108" class="title-accent">se lame la trufa al abrazarlo?</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="172">No tiene sueño ni hambre: te está pidiendo espacio.</tspan>
      <tspan x="0" y="210">Escuchar su lenguaje corporal previene el estrés.</tspan>
    </text>
    <g transform="translate(0, 260)">
      <rect width="380" height="58" rx="29" fill="#FDB54A" />
      <text x="190" y="35" class="cta-txt" text-anchor="middle">DESCUBRE LAS SEÑALES ➔</text>
      <text x="410" y="35" font-family="Plus Jakarta Sans" font-size="18" font-weight="600" fill="#FFF3E0">Pilar Etología • #FFF3E0</text>
    </g>
  </g>
</svg>"""


# 4. PLANTILLA 4 (4:5 - 1080x1350): PILAR D (BIOMECÁNICA & MITOS — TINTA PROFUNDA #10152B + CORAL/AMARILLO)
def generar_arte_lou() -> str:
    lou_img = ARTES_DIR / "post_04_lou_arnes_en_y.jpg"
    if not lou_img.exists():
        lou_img = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos" / "como-elegir-arnes-en-y-perros.jpg"
    img_uri = get_image_data_uri(lou_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,800;1,9..144,700&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 58px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FDB54A; }}
      .quote {{ font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 28px; font-weight: 700; fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 25px; font-weight: 500; fill: #FDFBF7; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimLou45" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.32" />
      <stop offset="48%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="68%" stop-color="#10152B" stop-opacity="0.45" />
      <stop offset="86%" stop-color="#10152B" stop-opacity="0.72" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.78" />
    </linearGradient>
  </defs>

  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#scrimLou45)" />

  <g transform="translate(64, 64)">
    <rect width="410" height="56" rx="28" fill="rgba(16, 21, 43, 0.80)" stroke="rgba(217, 56, 30, 0.55)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="34" class="badge-txt">BIOMECÁNICA // PASEO SEGURO</text>
  </g>

  <g transform="translate(64, 860)">
    <text x="0" y="-24" class="quote">"El dolor jamás enseña respeto, solo pánico."</text>
    <text class="title">
      <tspan x="0" y="36">Arnés ergonómico en 'Y':</tspan>
      <tspan x="0" y="106" class="title-accent">Paseos sin tirones ni ahogo.</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="172">0% presión sobre tráquea y tiroides. Deja libres</tspan>
      <tspan x="0" y="210">las escápulas para una zancada natural y cómoda.</tspan>
    </text>
    <g transform="translate(0, 260)">
      <rect width="380" height="58" rx="29" fill="#FDB54A" />
      <text x="190" y="35" class="cta-txt" text-anchor="middle">GUÍA DE ARNÉS EN Y ➔</text>
      <text x="410" y="35" font-family="Plus Jakarta Sans" font-size="18" font-weight="600" fill="#FDFBF7">Pilar Contraste • #10152B</text>
    </g>
  </g>
</svg>"""


def main():
    print("🎨 Generando artes vectoriales verticales 4:5 (1080x1350) para los 4 pilares cromáticos...")

    artes = {
        "post_01_instagram_loki.svg": generar_arte_loki(),
        "post_02_instagram_frodo.svg": generar_arte_frodo(),
        "post_03_etologia_senales.svg": generar_arte_etologia(),
        "post_04_lou_arnes_en_y.svg": generar_arte_lou(),
    }

    for filename, svg_content in artes.items():
        target = ARTES_DIR / filename
        target.write_text(svg_content, encoding="utf-8")
        (STUDIO_ASSETS / filename).write_text(svg_content, encoding="utf-8")
        print(f"✔ Arte 4:5 (1080x1350) generado: {target.name}")

    zip_path = WEEKLY_DIR / "kit_descargables_semana_2026_10_26.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in ARTES_DIR.glob("*"):
            if file_path.is_file():
                zf.write(file_path, f"01_Artes_Redes_Sociales/{file_path.name}")

        for vid_path in VIDEOS_DIR.glob("*.mp4"):
            zf.write(vid_path, f"02_Videos_TikTok_Reels_9x16/{vid_path.name}")

        reel_ensamblado = ROOT_DIR / "02_Estrategia_Y_Contenido" / "videos_flow_generados" / "reel_completo_lou_frodo_loki.mp4"
        if reel_ensamblado.exists():
            zf.write(reel_ensamblado, "02_Videos_TikTok_Reels_9x16/reel_completo_lou_frodo_loki_24s.mp4")

        plan_json = ROOT_DIR / "02_Estrategia_Y_Contenido" / "plan_publicacion_14_capitulos.json"
        if plan_json.exists():
            zf.write(plan_json, "03_Plan_Maestro_14_Capitulos/plan_publicacion_14_capitulos.json")

    studio_zip = STUDIO_ASSETS / "kit_descargables_semana_2026_10_26.zip"
    studio_zip.write_bytes(zip_path.read_bytes())
    print(f"📦 Kit ZIP actualizado ({zip_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

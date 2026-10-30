#!/usr/bin/env python3
"""
GENERADOR DE PROTOTIPO DINÁMICO EDITORIAL PF-2027
Crea 'post_01_animado_dermatologia.svg' con micro-movimiento cinético:
1. Ken Burns sutil sobre la foto (100% -> 104.5%)
2. Trazo doodle vivo (Paperpillar style) dibujándose alrededor de la almohadilla
3. Micro-indicador de radar / pulsación clínica
4. Bento Card de datos '80%' (Habitat style) con micro-flotación
5. Resaltado doodle sobre la frase clave
6. Flecha de swipe interactiva continua (➔)
7. Logotipo oficial completo nítido (#FFBE58 + silueta azul)
"""

import base64
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


def generar_arte_animado_dermatologia() -> str:
    img_path = ARTES_DIR / "post_01_loki_dermatologia.jpg"
    logo_path = ASSETS_DIR / "fulllogo_transparent_nobuffer.png"

    img_uri = get_image_data_uri(img_path)
    logo_uri = get_image_data_uri(logo_path)

    # Coordenadas focales de la patita: centro aprox en x=710, y=380
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .stat-num {{ font-family: 'Space Mono', monospace; font-size: 46px; font-weight: 700; fill: #FDB54A; }}
      .stat-lbl {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 600; fill: #FFFFFF; line-height: 1.25; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; fill: #10152B; }}
      .pill-annotation {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 700; fill: #10152B; }}

      /* ==========================================================
         MICRO-ANIMACIONES CINÉTICAS A 60FPS (COMPOSITOR GPU)
         ========================================================== */
      
      /* 1. Ken Burns Breathing Zoom sutil (Foco en la patita x:710, y:380) */
      .ken-burns-layer {{
        transform-origin: 710px 380px;
        animation: kenBurns 7s ease-in-out infinite alternate;
      }}
      @keyframes kenBurns {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.045); }}
      }}

      /* 2. Trazo Doodle Vivo alrededor de la almohadilla (Paperpillar style) */
      .doodle-loop-paw {{
        stroke-dasharray: 650;
        stroke-dashoffset: 650;
        animation: drawPawLoop 4.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
      }}
      @keyframes drawPawLoop {{
        0%, 10%  {{ stroke-dashoffset: 650; opacity: 0; }}
        20%      {{ opacity: 1; }}
        45%, 82% {{ stroke-dashoffset: 0; opacity: 1; }}
        92%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}

      /* 3. Flecha curva hacia la almohadilla */
      .doodle-arrow-paw {{
        stroke-dasharray: 220;
        stroke-dashoffset: 220;
        animation: drawArrow 4.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
      }}
      @keyframes drawArrow {{
        0%, 12%  {{ stroke-dashoffset: 220; opacity: 0; }}
        22%      {{ opacity: 1; }}
        48%, 82% {{ stroke-dashoffset: 0; opacity: 1; }}
        92%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}

      /* 4. Micro-Radar clínico pulsante sobre la almohadilla */
      .radar-pulse-1 {{
        animation: radarPing 3s cubic-bezier(0.2, 0.8, 0.4, 1) infinite;
      }}
      .radar-pulse-2 {{
        animation: radarPing 3s cubic-bezier(0.2, 0.8, 0.4, 1) infinite 0.75s;
      }}
      @keyframes radarPing {{
        0%   {{ r: 10px; opacity: 0.85; stroke-width: 3.5px; }}
        75%  {{ r: 48px; opacity: 0; stroke-width: 1px; }}
        100% {{ r: 48px; opacity: 0; stroke-width: 0px; }}
      }}

      /* 5. Sticker de Anotación Flotante (Vektora style) */
      .floating-tag {{
        animation: floatTag 4s ease-in-out infinite alternate;
      }}
      @keyframes floatTag {{
        0%   {{ transform: translate(450px, 240px); }}
        100% {{ transform: translate(450px, 232px); }}
      }}

      /* 6. Bento Badge 80% (Habitat style) con leve pulso de respiración */
      .stat-bento-card {{
        animation: bentoFloat 5s ease-in-out infinite alternate;
      }}
      @keyframes bentoFloat {{
        0%   {{ transform: translate(64px, 530px); }}
        100% {{ transform: translate(64px, 524px); }}
      }}

      /* 7. Resaltado doodle alrededor del texto */
      .text-highlight-loop {{
        stroke-dasharray: 600;
        stroke-dashoffset: 600;
        animation: drawTextHighlight 4.5s cubic-bezier(0.16, 1, 0.3, 1) infinite 0.5s;
      }}
      @keyframes drawTextHighlight {{
        0%, 15%  {{ stroke-dashoffset: 600; opacity: 0; }}
        25%      {{ opacity: 1; }}
        55%, 85% {{ stroke-dashoffset: 0; opacity: 1; }}
        95%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}

      /* 8. Desplazamiento continuo de flecha de Swipe (➔) */
      .swipe-arrow {{
        animation: slideSwipe 1.4s ease-in-out infinite alternate;
      }}
      @keyframes slideSwipe {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(8px); }}
      }}

      /* 9. Destellos cinéticos (✦) */
      .twinkle-star {{
        transform-origin: center;
        animation: twinkle 3s ease-in-out infinite alternate;
      }}
      @keyframes twinkle {{
        0%   {{ transform: scale(0.7) rotate(0deg); opacity: 0.35; }}
        50%  {{ transform: scale(1.15) rotate(45deg); opacity: 1; }}
        100% {{ transform: scale(0.85) rotate(90deg); opacity: 0.5; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
        .doodle-loop-paw, .doodle-arrow-paw, .text-highlight-loop {{ stroke-dashoffset: 0 !important; opacity: 1 !important; }}
      }}
    </style>

    <!-- Gradiente Cinematográfico Suave (máx 0.78, sin ocluir foto) -->
    <linearGradient id="scrimLokiAnim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.40" />
      <stop offset="40%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="60%" stop-color="#10152B" stop-opacity="0.38" />
      <stop offset="82%" stop-color="#10152B" stop-opacity="0.70" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.78" />
    </linearGradient>

    <!-- Filtro de Sombra Suave para Stickers -->
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.4" />
    </filter>
  </defs>

  <!-- ==========================================================
       CAPA 1: FOTOGRAFÍA PROTAGONISTA CON KEN BURNS ANIMADO
       ========================================================== -->
  <g class="ken-burns-layer">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  </g>

  <!-- CAPA 2: VELADURA DE CONTRASTE TIPOGRÁFICO -->
  <rect width="1080" height="1080" fill="url(#scrimLokiAnim)" />

  <!-- ==========================================================
       CAPA 3: MICRO-INTERACCIONES CLÍNICAS Y DOODLES SOBRE LA PATITA
       ========================================================== -->
  <!-- Micro-Radar Clínico Pulsante en el centro de la almohadilla (x:710, y:390) -->
  <g transform="translate(710, 390)">
    <circle class="radar-pulse-1" cx="0" cy="0" r="10" fill="none" stroke="#FDB54A" />
    <circle class="radar-pulse-2" cx="0" cy="0" r="10" fill="none" stroke="#FFFFFF" />
    <circle cx="0" cy="0" r="5" fill="#FDB54A" />
  </g>

  <!-- Trazo Doodle Orgánico que rodea la patita e inspección (Paperpillar style) -->
  <path class="doodle-loop-paw"
        d="M 620,330 C 660,280 770,290 810,340 C 840,380 820,460 760,490 C 700,520 620,480 600,430 C 580,380 600,345 625,330"
        fill="none" stroke="#FDB54A" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />

  <!-- Flecha Doodle Curva conectando etiqueta a la patita -->
  <path class="doodle-arrow-paw"
        d="M 575,268 C 615,280 645,310 660,335"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-dasharray="6 6" />

  <!-- Sticker Flotante de Anotación (Vektora style) -->
  <g class="floating-tag" filter="url(#softShadow)">
    <rect width="165" height="42" rx="21" fill="#FDB54A" stroke="#FFFFFF" stroke-width="2" />
    <text x="82" y="26" class="pill-annotation" text-anchor="middle">🔍 ZONA INTERDIGITAL</text>
  </g>

  <!-- Destello (✦) cerca de la patita -->
  <g class="twinkle-star" transform="translate(835, 305)">
    <path d="M 0,-12 Q 0,0 12,0 Q 0,0 0,12 Q 0,0 -12,0 Q 0,0 0,-12 Z" fill="#FDB54A" />
  </g>

  <!-- ==========================================================
       CAPA 4: CABECERA CON LOGO OFICIAL NÍTIDO (Safe Zone: 64px)
       ========================================================== -->
  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(16, 21, 43, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">SALUD // DERMATOLOGÍA</text>
  </g>

  <!-- ==========================================================
       CAPA 5: BENTO BADGE 80% (HABITAT / WEAVE & PITCH STYLE)
       ========================================================== -->
  <g class="stat-bento-card" filter="url(#softShadow)">
    <rect width="250" height="92" rx="22" fill="rgba(16, 21, 43, 0.88)" stroke="#FDB54A" stroke-width="2" />
    <text x="24" y="62" class="stat-num">80%</text>
    <text x="130" y="42" class="stat-lbl">
      <tspan x="130" dy="0">Picor por</tspan>
      <tspan x="130" dy="18" fill="#FDB54A">polen o piso</tspan>
      <tspan x="130" dy="18" font-size="12" fill="rgba(255,255,255,0.7)">(no es maña)</tspan>
    </text>
  </g>

  <!-- ==========================================================
       CAPA 6: BLOQUE TIPOGRÁFICO EDITORIAL HERO (Safe Zone: 64px)
       ========================================================== -->
  <g transform="translate(64, 650)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro se lame</tspan>
      <tspan x="0" y="70" class="title-accent">las patas sin parar?</tspan>
    </text>

    <!-- Resaltado Doodle que se dibuja alrededor de "las patas sin parar?" -->
    <path class="text-highlight-loop"
          d="M -10,95 Q 260,105 530,95 Q 545,55 530,35 Q 260,25 -10,35 Q -25,65 -10,95 Z"
          fill="none" stroke="#FDB54A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

    <text class="subtitle">
      <tspan x="0" y="145">El lamido compulsivo de patitas tras pasear indica</tspan>
      <tspan x="0" y="180">contacto con alérgenos. Guía médica de alivio clínico.</tspan>
    </text>

    <!-- Barra de Acción y Swipe Interactivo -->
    <g transform="translate(0, 225)">
      <rect width="380" height="54" rx="27" fill="#FDB54A" />
      <g>
        <text x="175" y="34" class="cta-txt" text-anchor="middle">DESLIZA PARA VER LA GUÍA</text>
        <g class="swipe-arrow" transform="translate(325, 0)">
          <text x="0" y="34" class="cta-txt" font-size="18">➔</text>
        </g>
      </g>
      <text x="415" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="rgba(255, 255, 255, 0.85)">Cuidado Veterinario EBVM</text>
    </g>
  </g>
</svg>"""


def main():
    print("🎨 Generando prototipo animado de dermatología...")
    svg_code = generar_arte_animado_dermatologia()

    out_file_artes = ARTES_DIR / "post_01_animado_dermatologia.svg"
    out_file_studio = STUDIO_ASSETS / "post_01_animado_dermatologia.svg"

    out_file_artes.write_text(svg_code, encoding="utf-8")
    out_file_studio.write_text(svg_code, encoding="utf-8")

    print(f"✔ SVG Animado guardado en: {out_file_artes}")
    print(f"✔ SVG Animado sincronizado con Studio: {out_file_studio}")


if __name__ == "__main__":
    main()

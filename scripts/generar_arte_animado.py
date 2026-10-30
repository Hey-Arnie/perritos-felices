#!/usr/bin/env python3
"""
SUITE DE ARTES DINÁMICOS EDITORIALES PF-2027 (MICRO-MOTION 60FPS)
Genera las 4 plantillas animadas en SVG para redes sociales e Instagram Reels:
1. post_01_animado_dermatologia.svg (Salud • Inspección de patitas & alérgenos)
2. post_02_animado_nutricion.svg (Nutrición • Helados hidratantes y regla 10% WSAVA)
3. post_03_animado_etologia.svg (Etología • Señales de calma y Turid Rugaas)
4. post_04_animado_lou.svg (Educación • Lou te enseña arnés anatómico en 'Y')

Técnicas incorporadas:
- Ken Burns cinemático sobre fotografía original de Flow
- Trazos doodle interactivos (Paperpillar style) con stroke-dashoffset
- Tarjetas bento de estadísticas clínicas (Habitat style) con micro-flotación
- Stickers y marcadores táctiles (Vektora style) con sombras suaves
- Micro-radar y flechas de swipe interactivas (➔)
- Logotipo oficial completo nítido (#FFBE58 + silueta azul)
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


def get_official_logo_uri() -> str:
    logo_path = ASSETS_DIR / "fulllogo_transparent_nobuffer.png"
    if not logo_path.exists():
        logo_path = ASSETS_DIR / "fulllogo_transparent.png"
    return get_image_data_uri(logo_path)


# =====================================================================
# 1. POST 01: DERMATOLOGÍA Y SALUD CANINA
# =====================================================================
def generar_animado_dermatologia() -> str:
    img_path = ARTES_DIR / "post_01_loki_dermatologia.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

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

      .ken-burns-layer {{
        transform-origin: 710px 380px;
        animation: kenBurns 7s ease-in-out infinite alternate;
      }}
      @keyframes kenBurns {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.045); }}
      }}

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

      .radar-pulse-1 {{ animation: radarPing 3s cubic-bezier(0.2, 0.8, 0.4, 1) infinite; }}
      .radar-pulse-2 {{ animation: radarPing 3s cubic-bezier(0.2, 0.8, 0.4, 1) infinite 0.75s; }}
      @keyframes radarPing {{
        0%   {{ r: 10px; opacity: 0.85; stroke-width: 3.5px; }}
        75%  {{ r: 48px; opacity: 0; stroke-width: 1px; }}
        100% {{ r: 48px; opacity: 0; stroke-width: 0px; }}
      }}

      .floating-tag {{ animation: floatTag 4s ease-in-out infinite alternate; }}
      @keyframes floatTag {{
        0%   {{ transform: translate(450px, 240px); }}
        100% {{ transform: translate(450px, 232px); }}
      }}

      .stat-bento-card {{ animation: bentoFloat 5s ease-in-out infinite alternate; }}
      @keyframes bentoFloat {{
        0%   {{ transform: translate(64px, 530px); }}
        100% {{ transform: translate(64px, 524px); }}
      }}

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

      .swipe-arrow {{ animation: slideSwipe 1.4s ease-in-out infinite alternate; }}
      @keyframes slideSwipe {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(8px); }}
      }}

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

    <linearGradient id="scrimLokiAnim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.40" />
      <stop offset="40%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="60%" stop-color="#10152B" stop-opacity="0.38" />
      <stop offset="82%" stop-color="#10152B" stop-opacity="0.70" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.78" />
    </linearGradient>

    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.4" />
    </filter>
  </defs>

  <g class="ken-burns-layer">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  </g>

  <rect width="1080" height="1080" fill="url(#scrimLokiAnim)" />

  <g transform="translate(710, 390)">
    <circle class="radar-pulse-1" cx="0" cy="0" r="10" fill="none" stroke="#FDB54A" />
    <circle class="radar-pulse-2" cx="0" cy="0" r="10" fill="none" stroke="#FFFFFF" />
    <circle cx="0" cy="0" r="5" fill="#FDB54A" />
  </g>

  <path class="doodle-loop-paw"
        d="M 620,330 C 660,280 770,290 810,340 C 840,380 820,460 760,490 C 700,520 620,480 600,430 C 580,380 600,345 625,330"
        fill="none" stroke="#FDB54A" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />

  <path class="doodle-arrow-paw"
        d="M 575,268 C 615,280 645,310 660,335"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-dasharray="6 6" />

  <g class="floating-tag" filter="url(#softShadow)">
    <rect width="165" height="42" rx="21" fill="#FDB54A" stroke="#FFFFFF" stroke-width="2" />
    <text x="82" y="26" class="pill-annotation" text-anchor="middle">🔍 ZONA INTERDIGITAL</text>
  </g>

  <g class="twinkle-star" transform="translate(835, 305)">
    <path d="M 0,-12 Q 0,0 12,0 Q 0,0 0,12 Q 0,0 -12,0 Q 0,0 0,-12 Z" fill="#FDB54A" />
  </g>

  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(16, 21, 43, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">SALUD // DERMATOLOGÍA</text>
  </g>

  <g class="stat-bento-card" filter="url(#softShadow)">
    <rect width="250" height="92" rx="22" fill="rgba(16, 21, 43, 0.88)" stroke="#FDB54A" stroke-width="2" />
    <text x="24" y="62" class="stat-num">80%</text>
    <text x="130" y="42" class="stat-lbl">
      <tspan x="130" dy="0">Picor por</tspan>
      <tspan x="130" dy="18" fill="#FDB54A">polen o piso</tspan>
      <tspan x="130" dy="18" font-size="12" fill="rgba(255,255,255,0.7)">(no es maña)</tspan>
    </text>
  </g>

  <g transform="translate(64, 650)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro se lame</tspan>
      <tspan x="0" y="70" class="title-accent">las patas sin parar?</tspan>
    </text>

    <path class="text-highlight-loop"
          d="M -10,95 Q 260,105 530,95 Q 545,55 530,35 Q 260,25 -10,35 Q -25,65 -10,95 Z"
          fill="none" stroke="#FDB54A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

    <text class="subtitle">
      <tspan x="0" y="145">El lamido compulsivo de patitas tras pasear indica</tspan>
      <tspan x="0" y="180">contacto con alérgenos. Guía médica de alivio clínico.</tspan>
    </text>

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


# =====================================================================
# 2. POST 02: NUTRICIÓN Y RECETAS FRESCAS
# =====================================================================
def generar_animado_nutricion() -> str:
    img_path = ARTES_DIR / "post_02_frodo_nutricion.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 58px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FFE082; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; fill: #FFF3E0; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .stat-num {{ font-family: 'Space Mono', monospace; font-size: 46px; font-weight: 700; fill: #FFE082; }}
      .stat-lbl {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 600; fill: #FFFFFF; line-height: 1.25; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; fill: #10152B; }}
      .pill-ing {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 700; fill: #FFFFFF; }}

      .ken-burns-nutri {{
        transform-origin: 540px 420px;
        animation: kenBurnsNutri 8s ease-in-out infinite alternate;
      }}
      @keyframes kenBurnsNutri {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.04); }}
      }}

      /* Doodles vapor aromático de comida (Paperpillar style) */
      .aroma-line-1 {{
        stroke-dasharray: 120;
        stroke-dashoffset: 120;
        animation: steamRise 3s ease-in-out infinite;
      }}
      .aroma-line-2 {{
        stroke-dasharray: 120;
        stroke-dashoffset: 120;
        animation: steamRise 3s ease-in-out infinite 0.8s;
      }}
      @keyframes steamRise {{
        0%   {{ stroke-dashoffset: 120; opacity: 0; transform: translateY(0); }}
        30%  {{ opacity: 0.9; }}
        70%  {{ stroke-dashoffset: 0; opacity: 0.9; }}
        100% {{ stroke-dashoffset: -50; opacity: 0; transform: translateY(-30px); }}
      }}

      /* Corazón flotante doodle al ver el snack */
      .heart-doodle {{
        animation: heartPulse 2.8s ease-in-out infinite;
      }}
      @keyframes heartPulse {{
        0%   {{ transform: translate(720px, 320px) scale(0.6); opacity: 0; }}
        25%  {{ opacity: 1; transform: translate(720px, 305px) scale(1.1); }}
        60%  {{ opacity: 0.9; transform: translate(720px, 280px) scale(1.0); }}
        100% {{ opacity: 0; transform: translate(720px, 250px) scale(0.8); }}
      }}

      .stat-bento-nutri {{ animation: floatNutri 5s ease-in-out infinite alternate; }}
      @keyframes floatNutri {{
        0%   {{ transform: translate(64px, 530px); }}
        100% {{ transform: translate(64px, 524px); }}
      }}

      .pill-float-1 {{ animation: pillHop 3s ease-in-out infinite alternate; }}
      .pill-float-2 {{ animation: pillHop 3s ease-in-out infinite alternate 0.3s; }}
      .pill-float-3 {{ animation: pillHop 3s ease-in-out infinite alternate 0.6s; }}
      @keyframes pillHop {{
        0%   {{ transform: translateY(0); }}
        100% {{ transform: translateY(-4px); }}
      }}

      .swipe-arrow-nutri {{ animation: slideSwipe 1.4s ease-in-out infinite alternate; }}
      @keyframes slideSwipe {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(8px); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>

    <linearGradient id="scrimFrodoAnim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1A1208" stop-opacity="0.38" />
      <stop offset="40%" stop-color="#1A1208" stop-opacity="0.0" />
      <stop offset="60%" stop-color="#1A1208" stop-opacity="0.38" />
      <stop offset="82%" stop-color="#1A1208" stop-opacity="0.70" />
      <stop offset="100%" stop-color="#1A1208" stop-opacity="0.78" />
    </linearGradient>

    <filter id="softShadowNutri" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.45" />
    </filter>
  </defs>

  <g class="ken-burns-nutri">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  </g>

  <rect width="1080" height="1080" fill="url(#scrimFrodoAnim)" />

  <!-- Doodles de Aroma & Corazón sobre los snacks caseros -->
  <g transform="translate(480, 360)">
    <path class="aroma-line-1" d="M 0,40 Q 15,20 0,0 Q -15,-20 0,-40" fill="none" stroke="#FFE082" stroke-width="3" stroke-linecap="round" />
    <path class="aroma-line-2" d="M 35,45 Q 50,25 35,5 Q 20,-15 35,-35" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" />
  </g>

  <!-- Corazón Doodle en bucle (Paperpillar style) -->
  <g class="heart-doodle">
    <path d="M 0,0 C -10,-12 -25,2 0,22 C 25,2 10,-12 0,0 Z" fill="#FFE082" stroke="#FFFFFF" stroke-width="2" />
  </g>

  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(26, 18, 8, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">COCINA // RECETA FRESCA</text>
  </g>

  <!-- Bento Card 10% WSAVA (Habitat style) -->
  <g class="stat-bento-nutri" filter="url(#softShadowNutri)">
    <rect width="250" height="92" rx="22" fill="rgba(26, 18, 8, 0.90)" stroke="#FFE082" stroke-width="2" />
    <text x="24" y="62" class="stat-num">10%</text>
    <text x="130" y="42" class="stat-lbl">
      <tspan x="130" dy="0">Toppers máx.</tspan>
      <tspan x="130" dy="18" fill="#FFE082">Regla WSAVA</tspan>
      <tspan x="130" dy="18" font-size="12" fill="rgba(255,255,255,0.7)">(seguro &amp; digestivo)</tspan>
    </text>
  </g>

  <!-- Bloque Hero -->
  <g transform="translate(64, 650)">
    <!-- 3 Pills de Ingredientes con sutil flotación escalonada -->
    <g transform="translate(0, 0)">
      <g class="pill-float-1">
        <rect width="175" height="36" rx="18" fill="rgba(255, 255, 255, 0.22)" stroke="rgba(255, 255, 255, 0.35)" />
        <text x="87" y="24" class="pill-ing" text-anchor="middle">🍉 Sandía natural</text>
      </g>
      <g class="pill-float-2" transform="translate(190, 0)">
        <rect width="190" height="36" rx="18" fill="rgba(255, 255, 255, 0.22)" stroke="rgba(255, 255, 255, 0.35)" />
        <text x="95" y="24" class="pill-ing" text-anchor="middle">🥛 Yogur sin lactosa</text>
      </g>
      <g class="pill-float-3" transform="translate(395, 0)">
        <rect width="150" height="36" rx="18" fill="rgba(255, 255, 255, 0.22)" stroke="rgba(255, 255, 255, 0.35)" />
        <text x="75" y="24" class="pill-ing" text-anchor="middle">🌱 Menta fresca</text>
      </g>
    </g>

    <text class="title">
      <tspan x="0" y="85">Helado casero de</tspan>
      <tspan x="0" y="150" class="title-accent">sandía &amp; yogur fresco</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="200">Digestivo, hidratante y antiinflamatorio para días calurosos.</tspan>
    </text>

    <g transform="translate(0, 230)">
      <rect width="360" height="54" rx="27" fill="#FFE082" />
      <g>
        <text x="165" y="34" class="cta-txt" text-anchor="middle">VER RECETA PASO A PASO</text>
        <g class="swipe-arrow-nutri" transform="translate(305, 0)">
          <text x="0" y="34" class="cta-txt" font-size="18">➔</text>
        </g>
      </g>
      <text x="395" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="rgba(255, 255, 255, 0.85)">Snack Saludable &amp; Seguro</text>
    </g>
  </g>
</svg>"""


# =====================================================================
# 3. POST 03: ETOLOGÍA Y SEÑALES DE CALMA
# =====================================================================
def generar_animado_etologia() -> str:
    img_path = ARTES_DIR / "post_03_etologia_calma.jpg"
    img_uri = get_image_data_uri(img_path)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 58px; font-weight: 800; fill: #FFFFFF; line-height: 1.1; }}
      .title-accent {{ fill: #81C784; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; fill: #E8F5E9; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .stat-num {{ font-family: 'Space Mono', monospace; font-size: 46px; font-weight: 700; fill: #81C784; }}
      .stat-lbl {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 600; fill: #FFFFFF; line-height: 1.25; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; fill: #10152B; }}
      .pill-annotation {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 700; fill: #10152B; }}

      .ken-burns-eto {{
        transform-origin: 620px 400px;
        animation: kenBurnsEto 8s ease-in-out infinite alternate;
      }}
      @keyframes kenBurnsEto {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.045); }}
      }}

      /* Lazo doodle que se dibuja en la trufa del perro (Paperpillar style) */
      .doodle-loop-trufa {{
        stroke-dasharray: 550;
        stroke-dashoffset: 550;
        animation: drawTrufaLoop 4.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
      }}
      @keyframes drawTrufaLoop {{
        0%, 10%  {{ stroke-dashoffset: 550; opacity: 0; }}
        20%      {{ opacity: 1; }}
        45%, 82% {{ stroke-dashoffset: 0; opacity: 1; }}
        92%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}

      .floating-tag-eto {{ animation: floatTagEto 4s ease-in-out infinite alternate; }}
      @keyframes floatTagEto {{
        0%   {{ transform: translate(370px, 320px); }}
        100% {{ transform: translate(370px, 312px); }}
      }}

      .stat-bento-eto {{ animation: floatBentoEto 5s ease-in-out infinite alternate; }}
      @keyframes floatBentoEto {{
        0%   {{ transform: translate(64px, 530px); }}
        100% {{ transform: translate(64px, 524px); }}
      }}

      .swipe-arrow-eto {{ animation: slideSwipe 1.4s ease-in-out infinite alternate; }}
      @keyframes slideSwipe {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(8px); }}
      }}

      .twinkle-eto {{
        transform-origin: center;
        animation: twinkleEto 3s ease-in-out infinite alternate;
      }}
      @keyframes twinkleEto {{
        0%   {{ transform: scale(0.7) rotate(0deg); opacity: 0.35; }}
        50%  {{ transform: scale(1.2) rotate(45deg); opacity: 1; }}
        100% {{ transform: scale(0.8) rotate(90deg); opacity: 0.45; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>

    <linearGradient id="scrimEtoAnim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E2312" stop-opacity="0.40" />
      <stop offset="40%" stop-color="#0E2312" stop-opacity="0.0" />
      <stop offset="60%" stop-color="#0E2312" stop-opacity="0.38" />
      <stop offset="82%" stop-color="#0E2312" stop-opacity="0.70" />
      <stop offset="100%" stop-color="#0E2312" stop-opacity="0.78" />
    </linearGradient>

    <filter id="softShadowEto" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.45" />
    </filter>
  </defs>

  <g class="ken-burns-eto">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  </g>

  <rect width="1080" height="1080" fill="url(#scrimEtoAnim)" />

  <!-- Doodle vivo en trufa (Paperpillar style) -->
  <path class="doodle-loop-trufa"
        d="M 540,360 C 580,320 680,330 710,380 C 730,420 700,470 640,480 C 580,490 520,440 510,400 C 505,370 520,350 540,360"
        fill="none" stroke="#81C784" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />

  <!-- Sticker de Anotación Flotante -->
  <g class="floating-tag-eto" filter="url(#softShadowEto)">
    <rect width="180" height="42" rx="21" fill="#81C784" stroke="#FFFFFF" stroke-width="2" />
    <text x="90" y="26" class="pill-annotation" text-anchor="middle">🐾 SEÑAL DE APACIGUAR</text>
  </g>

  <!-- Destello (✦) -->
  <g class="twinkle-eto" transform="translate(740, 320)">
    <path d="M 0,-12 Q 0,0 12,0 Q 0,0 0,12 Q 0,0 -12,0 Q 0,0 0,-12 Z" fill="#81C784" />
  </g>

  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(14, 35, 18, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">ETOLOGÍA // LENGUAJE</text>
  </g>

  <!-- Bento Card 30+ Señales (Habitat style) -->
  <g class="stat-bento-eto" filter="url(#softShadowEto)">
    <rect width="250" height="92" rx="22" fill="rgba(14, 35, 18, 0.90)" stroke="#81C784" stroke-width="2" />
    <text x="24" y="62" class="stat-num">30+</text>
    <text x="130" y="42" class="stat-lbl">
      <tspan x="130" dy="0">Señales de calma</tspan>
      <tspan x="130" dy="18" fill="#81C784">Turid Rugaas</tspan>
      <tspan x="130" dy="18" font-size="12" fill="rgba(255,255,255,0.7)">(comunicación pura)</tspan>
    </text>
  </g>

  <g transform="translate(64, 650)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro bosteza o</tspan>
      <tspan x="0" y="68" class="title-accent">se lame la trufa al abrazarlo?</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="145">No tiene sueño ni hambre: te está pidiendo espacio.</tspan>
      <tspan x="0" y="180">Aprender su idioma es el mayor acto de amor y respeto.</tspan>
    </text>

    <g transform="translate(0, 225)">
      <rect width="380" height="54" rx="27" fill="#81C784" />
      <g>
        <text x="175" y="34" class="cta-txt" text-anchor="middle">DESCUBRE LAS 5 SEÑALES</text>
        <g class="swipe-arrow-eto" transform="translate(325, 0)">
          <text x="0" y="34" class="cta-txt" font-size="18">➔</text>
        </g>
      </g>
      <text x="415" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="rgba(255, 255, 255, 0.85)">Educación 100% Positiva • Fear-Free</text>
    </g>
  </g>
</svg>"""


# =====================================================================
# 4. POST 04: "LOU TE ENSEÑA" (ARNÉS EN 'Y')
# =====================================================================
def generar_animado_lou() -> str:
    lou_img = ARTES_DIR / "post_04_lou_arnes_en_y.jpg"
    img_uri = get_image_data_uri(lou_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 56px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .stat-num {{ font-family: 'Space Mono', monospace; font-size: 46px; font-weight: 700; fill: #FDB54A; }}
      .stat-lbl {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 600; fill: #FFFFFF; line-height: 1.25; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; fill: #10152B; }}
      .quote-italics {{ font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 28px; font-weight: 700; fill: #FDB54A; }}

      .ken-burns-lou {{
        transform-origin: 540px 380px;
        animation: kenBurnsLou 8s ease-in-out infinite alternate;
      }}
      @keyframes kenBurnsLou {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.04); }}
      }}

      /* Trazo en 'Y' animado sobre el arnés anatómico (Paperpillar style) */
      .doodle-y-harness {{
        stroke-dasharray: 300;
        stroke-dashoffset: 300;
        animation: drawYHarness 4.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
      }}
      @keyframes drawYHarness {{
        0%, 15%  {{ stroke-dashoffset: 300; opacity: 0; }}
        25%      {{ opacity: 1; }}
        55%, 85% {{ stroke-dashoffset: 0; opacity: 1; }}
        95%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}

      .stat-bento-lou {{ animation: floatLou 5s ease-in-out infinite alternate; }}
      @keyframes floatLou {{
        0%   {{ transform: translate(64px, 530px); }}
        100% {{ transform: translate(64px, 524px); }}
      }}

      .swipe-arrow-lou {{ animation: slideSwipe 1.4s ease-in-out infinite alternate; }}
      @keyframes slideSwipe {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(8px); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>

    <linearGradient id="scrimLouAnim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.40" />
      <stop offset="40%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="60%" stop-color="#10152B" stop-opacity="0.38" />
      <stop offset="82%" stop-color="#10152B" stop-opacity="0.70" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.78" />
    </linearGradient>

    <filter id="softShadowLou" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.45" />
    </filter>
  </defs>

  <g class="ken-burns-lou">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  </g>

  <rect width="1080" height="1080" fill="url(#scrimLouAnim)" />

  <!-- Trazo animado de ergonomía en 'Y' (Paperpillar style) sobre el arnés -->
  <g transform="translate(680, 440)">
    <path class="doodle-y-harness"
          d="M -30,-45 L 0,0 L 30,-45 M 0,0 L 0,55"
          fill="none" stroke="#FDB54A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
    <circle cx="0" cy="55" r="5" fill="#FFFFFF" />
  </g>

  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(16, 21, 43, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">PASEO RESPETUOSO // GUÍA</text>
  </g>

  <!-- Bento Card 0% Ahogo (Habitat style) -->
  <g class="stat-bento-lou" filter="url(#softShadowLou)">
    <rect width="250" height="92" rx="22" fill="rgba(16, 21, 43, 0.90)" stroke="#FDB54A" stroke-width="2" />
    <text x="24" y="62" class="stat-num">0%</text>
    <text x="130" y="42" class="stat-lbl">
      <tspan x="130" dy="0">Presión traqueal</tspan>
      <tspan x="130" dy="18" fill="#FDB54A">Arnés en 'Y'</tspan>
      <tspan x="130" dy="18" font-size="12" fill="rgba(255,255,255,0.7)">(hombros libres)</tspan>
    </text>
  </g>

  <g transform="translate(64, 650)">
    <text class="quote-italics">"El dolor jamás enseña respeto, solo pánico."</text>

    <text class="title">
      <tspan x="0" y="62">Arnés ergonómico en 'Y':</tspan>
      <tspan x="0" y="126" class="title-accent">Paseos sin tirones ni ahogo.</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="185">Libera las escápulas, protege la tráquea y cervicales.</tspan>
    </text>

    <g transform="translate(0, 225)">
      <rect width="360" height="54" rx="27" fill="#FDB54A" />
      <g>
        <text x="165" y="34" class="cta-txt" text-anchor="middle">GUÍA DE ELECCIÓN DE ARNÉS</text>
        <g class="swipe-arrow-lou" transform="translate(305, 0)">
          <text x="0" y="34" class="cta-txt" font-size="18">➔</text>
        </g>
      </g>
      <text x="395" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="rgba(255, 255, 255, 0.85)">Educación Canina Amable</text>
    </g>
  </g>
</svg>"""


def main():
    print("🎨 Generando Suite de 4 Artes Dinámicos (Micro-Motion 60fps)...")

    artes = [
        ("post_01_animado_dermatologia.svg", generar_animado_dermatologia()),
        ("post_02_animado_nutricion.svg", generar_animado_nutricion()),
        ("post_03_animado_etologia.svg", generar_animado_etologia()),
        ("post_04_animado_lou.svg", generar_animado_lou()),
    ]

    for fname, svg_code in artes:
        out_artes = ARTES_DIR / fname
        out_studio = STUDIO_ASSETS / fname
        out_artes.write_text(svg_code, encoding="utf-8")
        out_studio.write_text(svg_code, encoding="utf-8")
        print(f"✔ Generado: {fname}")


if __name__ == "__main__":
    main()

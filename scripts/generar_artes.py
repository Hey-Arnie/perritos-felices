#!/usr/bin/env python3
"""
GENERADOR DE LÍNEA GRÁFICA EDITORIAL PF-2027 (Perritos Felices Studio)
Produce artes vectoriales 1080x1080 con jerarquía tipográfica Fraunces / Space Mono,
paleta oficial (#2C4BCA, #FDB54A, #FDFBF7, #10152B), sellos Fear-Free y variedad de caninos.
"""

import base64
import json
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
WEEKLY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido" / "entregas_semanales" / "semana_2026_10_26"
ARTES_DIR = WEEKLY_DIR / "artes"
VIDEOS_DIR = WEEKLY_DIR / "videos"

ARTES_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def get_image_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/jpeg" if path.suffix in (".jpg", ".jpeg") else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


# 1. PLANTILLA 1: GUÍA MÉDICA / SALUD (LOKI - EL NEGRO)
def generar_arte_loki() -> str:
    loki_img = ARTES_DIR / "post_01_loki_dermatologia.jpg"
    if not loki_img.exists():
        loki_img = ASSETS_DIR / "referencias_mascotas" / "loki_01_face.jpg"
    img_uri = get_image_data_uri(loki_img)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 58px; font-weight: 800; fill: #10152B; line-height: 1.1; }}
      .title-accent {{ fill: #2C4BCA; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 500; fill: #575E7E; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 20px; font-weight: 700; text-transform: uppercase; fill: #2C4BCA; }}
      .card-bold {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 700; fill: #10152B; }}
      .card-desc {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 20px; font-weight: 500; fill: #575E7E; }}
      .pill-txt {{ font-family: 'Space Mono', monospace; font-size: 18px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FDFBF7" />
      <stop offset="100%" stop-color="#F4EFE6" />
    </linearGradient>
    <clipPath id="lokiClip">
      <rect x="580" y="240" width="440" height="480" rx="40" ry="40" />
    </clipPath>
    <filter id="shadow" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#10152B" flood-opacity="0.08" />
    </filter>
  </defs>

  <!-- Fondo Editorial -->
  <rect width="1080" height="1080" fill="url(#bgGrad)" />

  <!-- Patrón de fondo geométrico sutil -->
  <circle cx="980" cy="100" r="320" fill="#E8EDFF" opacity="0.6" />
  <circle cx="100" cy="980" r="280" fill="#FFF3E0" opacity="0.5" />

  <!-- Cabecera Superior: Branding Oficial -->
  <g transform="translate(60, 60)">
    <rect width="52" height="52" rx="14" fill="#2C4BCA" />
    <text x="26" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="28" font-weight="800" fill="#FDB54A" text-anchor="middle">PF</text>
    <text x="70" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="800" fill="#10152B">Perritos Felices</text>
    
    <!-- Tag Categoría -->
    <rect x="680" y="4" width="280" height="44" rx="22" fill="#E8EDFF" stroke="#2C4BCA" stroke-width="2" />
    <text x="820" y="32" class="badge-txt" text-anchor="middle">SALUD &amp; DERMATOLOGÍA</text>
  </g>

  <!-- Título Masivo Editorial -->
  <g transform="translate(60, 180)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro se lame</tspan>
      <tspan x="0" y="68" class="title-accent">las patas sin parar?</tspan>
    </text>
    <text x="0" y="125" class="subtitle">No es ansiedad ni maña: el 80% de las veces es picor alérgico.</text>
  </g>

  <!-- Tarjeta Fotográfica con Loki -->
  <g filter="url(#shadow)">
    <!-- Marco y Sombra -->
    <rect x="580" y="240" width="440" height="480" rx="40" fill="#10152B" />
    <image href="{img_uri}" x="580" y="240" width="440" height="480" preserveAspectRatio="xMidYMid slice" clip-path="url(#lokiClip)" />
    
    <!-- Borde decorativo -->
    <rect x="580" y="240" width="440" height="480" rx="40" fill="none" stroke="#FDB54A" stroke-width="6" />

    <!-- Badge Embajador Loki -->
    <g transform="translate(610, 650)">
      <rect width="220" height="46" rx="23" fill="#10152B" />
      <text x="110" y="30" font-family="'Space Mono', monospace" font-size="16" font-weight="700" fill="#FDB54A" text-anchor="middle">LOKI • RESCATADO</text>
    </g>
  </g>

  <!-- 3 Puntos Clave de Alivio (Lado Izquierdo) -->
  <g transform="translate(60, 360)">
    <!-- Punto 1 -->
    <g transform="translate(0, 0)">
      <circle cx="28" cy="28" r="28" fill="#FDB54A" />
      <text x="28" y="36" font-family="'Fraunces', serif" font-size="24" font-weight="800" fill="#10152B" text-anchor="middle">1</text>
      <text x="76" y="26" class="card-bold">Lava sus patas pospaseo</text>
      <text x="76" y="54" class="card-desc">Agua tibia + avena coloidal quita polen y químicos.</text>
    </g>

    <!-- Punto 2 -->
    <g transform="translate(0, 110)">
      <circle cx="28" cy="28" r="28" fill="#FDB54A" />
      <text x="28" y="36" font-family="'Fraunces', serif" font-size="24" font-weight="800" fill="#10152B" text-anchor="middle">2</text>
      <text x="76" y="26" class="card-bold">Seca siempre entre dedos</text>
      <text x="76" y="54" class="card-desc">La humedad constante atrae hongos (Malassezia).</text>
    </g>

    <!-- Punto 3 -->
    <g transform="translate(0, 220)">
      <circle cx="28" cy="28" r="28" fill="#FDB54A" />
      <text x="28" y="36" font-family="'Fraunces', serif" font-size="24" font-weight="800" fill="#10152B" text-anchor="middle">3</text>
      <text x="76" y="26" class="card-bold">Cero castigos ni conos</text>
      <text x="76" y="54" class="card-desc">El picor causa estrés real. Busca atención médica.</text>
    </g>
  </g>

  <!-- Tarjeta Footer / Call to Action Fear-Free -->
  <g transform="translate(60, 840)">
    <rect width="960" height="160" rx="30" fill="#2C4BCA" />
    
    <!-- Sello Fear-Free -->
    <g transform="translate(40, 35)">
      <circle cx="45" cy="45" r="42" fill="#FDB54A" />
      <text x="45" y="52" font-family="'Space Mono', monospace" font-size="12" font-weight="700" fill="#10152B" text-anchor="middle">100%</text>
      <text x="45" y="66" font-family="'Space Mono', monospace" font-size="11" font-weight="700" fill="#10152B" text-anchor="middle">FEAR-FREE</text>
    </g>

    <text x="160" y="68" font-family="'Fraunces', serif" font-size="30" font-weight="700" fill="#FFFFFF">Guía Médica Completa &amp; Directorio Veterinario</text>
    <text x="160" y="106" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="500" fill="#E8EDFF">Encuentra clínicas sin jaulas en perritosfelices.com</text>

    <!-- Botón / Micro-sticker -->
    <rect x="760" y="52" width="160" height="56" rx="28" fill="#FDB54A" />
    <text x="840" y="87" class="pill-txt" text-anchor="middle">LEER ↗</text>
  </g>
</svg>"""


# 2. PLANTILLA 2: NUTRICIÓN FRESCA Y RECETAS (FRODO - EL RUBIO)
def generar_arte_frodo() -> str:
    frodo_img = ARTES_DIR / "post_02_frodo_nutricion.jpg"
    if not frodo_img.exists():
        frodo_img = ASSETS_DIR / "referencias_mascotas" / "frodo_01_front.jpg"
    img_uri = get_image_data_uri(frodo_img)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 56px; font-weight: 800; fill: #10152B; line-height: 1.1; }}
      .title-accent {{ fill: #E65100; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; fill: #575E7E; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 19px; font-weight: 700; fill: #E65100; }}
      .box-title {{ font-family: 'Fraunces', serif; font-size: 26px; font-weight: 700; fill: #10152B; }}
      .box-desc {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 500; fill: #3D4463; }}
      .ing-pill {{ font-family: 'Space Mono', monospace; font-size: 18px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="bgNutri" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFF8E7" />
      <stop offset="100%" stop-color="#FBF4E2" />
    </linearGradient>
    <clipPath id="frodoClip">
      <rect x="60" y="240" width="440" height="480" rx="40" ry="40" />
    </clipPath>
    <filter id="shadow" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#10152B" flood-opacity="0.08" />
    </filter>
  </defs>

  <!-- Fondo Gastronómico Cálido -->
  <rect width="1080" height="1080" fill="url(#bgNutri)" />

  <!-- Círculos de luz suaves -->
  <circle cx="150" cy="120" r="280" fill="#FFE082" opacity="0.3" />
  <circle cx="950" cy="900" r="340" fill="#FFCC80" opacity="0.25" />

  <!-- Cabecera Superior -->
  <g transform="translate(60, 60)">
    <rect width="52" height="52" rx="14" fill="#E65100" />
    <text x="26" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">PF</text>
    <text x="70" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="800" fill="#10152B">Perritos Felices • Cocina Natural</text>
    
    <!-- Tag Nutrición -->
    <rect x="710" y="4" width="250" height="44" rx="22" fill="#FFE0B2" stroke="#E65100" stroke-width="2" />
    <text x="835" y="32" class="badge-txt" text-anchor="middle">SNACK FRESCO</text>
  </g>

  <!-- Foto con Frodo (Lado Izquierdo) -->
  <g filter="url(#shadow)">
    <rect x="60" y="240" width="440" height="480" rx="40" fill="#10152B" />
    <image href="{img_uri}" x="60" y="240" width="440" height="480" preserveAspectRatio="xMidYMid slice" clip-path="url(#frodoClip)" />
    <rect x="60" y="240" width="440" height="480" rx="40" fill="none" stroke="#E65100" stroke-width="6" />

    <!-- Badge Frodo -->
    <g transform="translate(90, 650)">
      <rect width="230" height="46" rx="23" fill="#10152B" />
      <text x="115" y="30" font-family="'Space Mono', monospace" font-size="16" font-weight="700" fill="#FFE082" text-anchor="middle">FRODO • EL RUBIO 🐕</text>
    </g>
  </g>

  <!-- Título y Receta (Lado Derecho) -->
  <g transform="translate(540, 180)">
    <text class="title">
      <tspan x="0" y="0">Helado casero de</tspan>
      <tspan x="0" y="66" class="title-accent">zanahoria &amp; manzana</tspan>
    </text>
    <text x="0" y="118" class="subtitle">100% natural, digestivo y libre de lactosa dañina.</text>
  </g>

  <!-- Lista de Ingredientes en Cajitas Bento -->
  <g transform="translate(540, 340)">
    <!-- Ingrediente 1 -->
    <rect x="0" y="0" width="480" height="80" rx="20" fill="#FFFFFF" stroke="#FFE0B2" stroke-width="2" />
    <text x="24" y="48" font-size="30">🥕</text>
    <text x="76" y="38" class="box-title">1 taza de puré de zanahoria</text>
    <text x="76" y="64" class="box-desc">Cocida y sin sal (rica en betacarotenos y fibra)</text>

    <!-- Ingrediente 2 -->
    <rect x="0" y="96" width="480" height="80" rx="20" fill="#FFFFFF" stroke="#FFE0B2" stroke-width="2" />
    <text x="24" y="144" font-size="30">🍎</text>
    <text x="76" y="134" class="box-title">1 manzana sin semillas</text>
    <text x="76" y="160" class="box-desc">Pectina prebiótica para su flora intestinal</text>

    <!-- Ingrediente 3 -->
    <rect x="0" y="192" width="480" height="80" rx="20" fill="#FFFFFF" stroke="#FFE0B2" stroke-width="2" />
    <text x="24" y="240" font-size="30">🥣</text>
    <text x="76" y="230" class="box-title">Caldo de huesos o agua fresca</text>
    <text x="76" y="256" class="box-desc">Hidratación antiinflamatoria sin condimentos</text>

    <!-- Ingrediente 4 -->
    <rect x="0" y="288" width="480" height="80" rx="20" fill="#FFFFFF" stroke="#FFE0B2" stroke-width="2" />
    <text x="24" y="336" font-size="30">🌿</text>
    <text x="76" y="326" class="box-title">Pizca de perejil fresco</text>
    <text x="76" y="352" class="box-desc">Aliento fresco y apoyo renal natural</text>
  </g>

  <!-- Footer con Preparación -->
  <g transform="translate(60, 840)">
    <rect width="960" height="160" rx="30" fill="#10152B" />
    <g transform="translate(40, 40)">
      <circle cx="40" cy="40" r="38" fill="#FDB54A" />
      <text x="40" y="48" font-size="32" text-anchor="middle">❄️</text>
    </g>
    <text x="150" y="65" font-family="'Fraunces', serif" font-size="28" font-weight="700" fill="#FFFFFF">Modo de preparación: 3 horas al congelador</text>
    <text x="150" y="102" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="500" fill="#D1D5E8">Licúa todo, sirve en moldes de silicona o tapete LickiMat y ¡a disfrutar!</text>
    
    <rect x="760" y="52" width="160" height="56" rx="28" fill="#FDB54A" />
    <text x="840" y="87" class="ing-pill" text-anchor="middle">GUARDAR 📥</text>
  </g>
</svg>"""


# 3. PLANTILLA 3: ETOLOGÍA & SEÑALES DE CALMA (FOTOGRAFÍA DOCUMENTAL + BENTO)
def generar_arte_etologia() -> str:
    eto_img = ARTES_DIR / "post_03_etologia_calma.jpg"
    img_uri = get_image_data_uri(eto_img)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 56px; font-weight: 800; fill: #10152B; line-height: 1.1; }}
      .title-accent {{ fill: #2E7D32; }}
      .card-title {{ font-family: 'Fraunces', serif; font-size: 22px; font-weight: 700; fill: #10152B; }}
      .card-desc {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 500; fill: #575E7E; line-height: 1.35; }}
    </style>
    <linearGradient id="bgEto" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F4FAF5" />
      <stop offset="100%" stop-color="#EBF4EC" />
    </linearGradient>
    <clipPath id="etoClip">
      <rect x="60" y="240" width="440" height="480" rx="40" ry="40" />
    </clipPath>
    <filter id="shadowEto" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#10152B" flood-opacity="0.08" />
    </filter>
  </defs>

  <rect width="1080" height="1080" fill="url(#bgEto)" />
  <circle cx="950" cy="150" r="320" fill="#D4EDDA" opacity="0.6" />

  <!-- Cabecera -->
  <g transform="translate(60, 60)">
    <rect width="52" height="52" rx="14" fill="#2E7D32" />
    <text x="26" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">PF</text>
    <text x="70" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="800" fill="#10152B">Perritos Felices • Etología y Lenguaje</text>
    
    <rect x="680" y="4" width="280" height="44" rx="22" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2" />
    <text x="820" y="32" font-family="'Space Mono', monospace" font-size="19" font-weight="700" fill="#2E7D32" text-anchor="middle">SEÑALES DE CALMA</text>
  </g>

  <!-- Foto Documental con Señal de Calma (Lado Izquierdo) -->
  <g filter="url(#shadowEto)">
    <rect x="60" y="240" width="440" height="480" rx="40" fill="#10152B" />
    <image href="{img_uri}" x="60" y="240" width="440" height="480" preserveAspectRatio="xMidYMid slice" clip-path="url(#etoClip)" />
    <rect x="60" y="240" width="440" height="480" rx="40" fill="none" stroke="#2E7D32" stroke-width="6" />

    <!-- Badge Foto Calma -->
    <g transform="translate(90, 650)">
      <rect width="250" height="46" rx="23" fill="#10152B" />
      <text x="125" y="30" font-family="'Space Mono', monospace" font-size="15" font-weight="700" fill="#A5D6A7" text-anchor="middle">LAMIDO DE TRUFA 👅</text>
    </g>
  </g>

  <!-- Título y 4 Señales Bento (Lado Derecho) -->
  <g transform="translate(540, 175)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro bosteza</tspan>
      <tspan x="0" y="62" class="title-accent">cuando lo abrazas?</tspan>
    </text>
    <text x="0" y="112" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="500" fill="#575E7E">No tiene sueño: te está pidiendo un poco de espacio respetuoso.</text>
  </g>

  <!-- Grilla Bento Compacta (Lado Derecho) -->
  <g transform="translate(540, 310)">
    <!-- Bento 1: Bostezo -->
    <rect x="0" y="0" width="480" height="92" rx="20" fill="#FFFFFF" stroke="#C8E6C9" stroke-width="2" />
    <text x="24" y="56" font-size="34">🥱</text>
    <text x="76" y="38" class="card-title">El Bostezo Social</text>
    <text x="76" y="66" class="card-desc">Reduce la tensión propia y la de quien tiene enfrente.</text>

    <!-- Bento 2: Lamerse la trufa -->
    <rect x="0" y="104" width="480" height="92" rx="20" fill="#FFFFFF" stroke="#C8E6C9" stroke-width="2" />
    <text x="24" y="160" font-size="34">👅</text>
    <text x="76" y="142" class="card-title">Lamido de Hocico</text>
    <text x="76" y="170" class="card-desc">Lengua rápida a la nariz ante movimientos invasivos.</text>

    <!-- Bento 3: Mirada desviada -->
    <rect x="0" y="208" width="480" height="92" rx="20" fill="#FFFFFF" stroke="#C8E6C9" stroke-width="2" />
    <text x="24" y="264" font-size="34">👀</text>
    <text x="76" y="246" class="card-title">Girar la Cabeza</text>
    <text x="76" y="274" class="card-desc">Evita contacto visual directo para pacificar la situación.</text>

    <!-- Bento 4: Sacudida -->
    <rect x="0" y="312" width="480" height="92" rx="20" fill="#FFFFFF" stroke="#C8E6C9" stroke-width="2" />
    <text x="24" y="368" font-size="34">🐕</text>
    <text x="76" y="350" class="card-title">Sacudirse en Seco</text>
    <text x="76" y="378" class="card-desc">Resetea su sistema nervioso tras un momento de tensión.</text>
  </g>

  <!-- Footer Fear-Free -->
  <g transform="translate(60, 840)">
    <rect width="960" height="160" rx="30" fill="#2E7D32" />
    <text x="50" y="70" font-family="'Fraunces', serif" font-size="30" font-weight="700" fill="#FFFFFF">Amar a tu perro es aprender su lenguaje</text>
    <text x="50" y="110" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="500" fill="#D4EDDA">Descubre la guía completa de etología positiva en perritosfelices.com</text>
    <rect x="760" y="52" width="160" height="56" rx="28" fill="#FDB54A" />
    <text x="840" y="87" font-family="'Space Mono', monospace" font-size="18" font-weight="700" fill="#10152B" text-anchor="middle">COMPARTIR ↗</text>
  </g>
</svg>"""


# 4. PLANTILLA 4: "LOU TE ENSEÑA" (FOTOGRAFÍA OFICIAL DE LOU, FRODO Y LOKI)
def generar_arte_lou() -> str:
    lou_img = ARTES_DIR / "post_04_lou_arnes_en_y.jpg"
    if not lou_img.exists():
        lou_img = ARTES_DIR / "post_04_lou_arnes.jpg"
    img_uri = get_image_data_uri(lou_img)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 52px; font-weight: 800; fill: #10152B; line-height: 1.15; }}
      .title-accent {{ fill: #2C4BCA; }}
      .col-h {{ font-family: 'Fraunces', serif; font-size: 24px; font-weight: 800; }}
      .col-p {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17px; font-weight: 500; fill: #3D4463; line-height: 1.45; }}
    </style>
    <linearGradient id="bgLou" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FDFBF7" />
      <stop offset="100%" stop-color="#E8EDFF" />
    </linearGradient>
    <clipPath id="louClip">
      <rect x="580" y="240" width="440" height="480" rx="40" ry="40" />
    </clipPath>
    <filter id="shadowLou" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#10152B" flood-opacity="0.08" />
    </filter>
  </defs>

  <rect width="1080" height="1080" fill="url(#bgLou)" />

  <!-- Cabecera -->
  <g transform="translate(60, 60)">
    <circle cx="28" cy="28" r="28" fill="#2C4BCA" />
    <text x="28" y="38" font-size="28" text-anchor="middle">👩‍🦰</text>
    <text x="75" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="800" fill="#10152B">Lou • Educadora Canina Fear-Free</text>
    <text x="75" y="54" font-family="'Space Mono', monospace" font-size="14" font-weight="700" fill="#575E7E">27 AÑOS • CRIANZA POSITIVA CON LOKI &amp; FRODO</text>
    
    <rect x="710" y="8" width="250" height="42" rx="21" fill="#FDB54A" />
    <text x="835" y="35" font-family="'Space Mono', monospace" font-size="18" font-weight="700" fill="#10152B" text-anchor="middle">GUÍA DE PASEO</text>
  </g>

  <!-- Título -->
  <g transform="translate(60, 165)">
    <text class="title">
      <tspan x="0" y="0">Arnés en "Y" vs. Collares de Ahogo:</tspan>
      <tspan x="0" y="58" class="title-accent">¿Por qué nunca debes estrangularlo?</tspan>
    </text>
  </g>

  <!-- Comparativa (Lado Izquierdo) -->
  <g transform="translate(60, 275)">
    <!-- Peligro: Collar de Ahogo -->
    <rect x="0" y="0" width="490" height="210" rx="24" fill="#FFEBEE" stroke="#EF5350" stroke-width="2" />
    <rect x="25" y="20" width="115" height="34" rx="17" fill="#D32F2F" />
    <text x="82" y="43" font-family="'Space Mono', monospace" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">PELIGRO ❌</text>
    <text x="155" y="44" class="col-h" fill="#C62828">Collar de ahogo o púas</text>
    <text x="25" y="85" class="col-p">• Aplasta tráquea, tiroides y daña cervicales.</text>
    <text x="25" y="115" class="col-p">• Dispara presión ocular e induce pánico.</text>
    <text x="25" y="145" class="col-p">• Provoca agresividad defensiva por dolor.</text>

    <!-- Correcto: Arnés Anatómico en Y -->
    <rect x="0" y="230" width="490" height="210" rx="24" fill="#E8F5E9" stroke="#66BB6A" stroke-width="2" />
    <rect x="25" y="250" width="125" height="34" rx="17" fill="#2E7D32" />
    <text x="87" y="273" font-family="'Space Mono', monospace" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">CORRECTO ✔</text>
    <text x="165" y="274" class="col-h" fill="#1B5E20">Arnés Ergonómico en 'Y'</text>
    <text x="25" y="315" class="col-p">• Reparte la tracción en el esternón seguro.</text>
    <text x="25" y="345" class="col-p">• Deja escápulas 100% libres de fricción.</text>
    <text x="25" y="375" class="col-p">• Paseos relajados basados en olfateo libre.</text>
  </g>

  <!-- Foto de Lou con Loki y Frodo (Lado Derecho) -->
  <g filter="url(#shadowLou)">
    <rect x="580" y="240" width="440" height="480" rx="40" fill="#10152B" />
    <image href="{img_uri}" x="580" y="240" width="440" height="480" preserveAspectRatio="xMidYMid slice" clip-path="url(#louClip)" />
    <rect x="580" y="240" width="440" height="480" rx="40" fill="none" stroke="#2C4BCA" stroke-width="6" />

    <!-- Badge Lou & Mascotas -->
    <g transform="translate(610, 650)">
      <rect width="260" height="46" rx="23" fill="#10152B" />
      <text x="130" y="30" font-family="'Space Mono', monospace" font-size="15" font-weight="700" fill="#FDB54A" text-anchor="middle">LOU + FRODO &amp; LOKI 🐕‍🦺</text>
    </g>
  </g>

  <!-- Footer con Cita de Lou -->
  <g transform="translate(60, 840)">
    <rect width="960" height="160" rx="30" fill="#10152B" />
    <text x="50" y="70" font-family="'Fraunces', serif" font-size="28" font-weight="700" fill="#FDB54A">"El dolor jamás enseña respeto, solo enseña pánico."</text>
    <text x="50" y="110" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="500" fill="#FFFFFF">— Lou, educadora canina en Perritos Felices</text>

    <rect x="760" y="52" width="160" height="56" rx="28" fill="#2C4BCA" />
    <text x="840" y="87" font-family="'Space Mono', monospace" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">VER GUÍA ↗</text>
  </g>
</svg>"""


# 5. CREACIÓN DE FICHERO DE PROYECTO GOOGLE FLOW (.flow.json)
def generar_flow_project() -> dict:
    return {
        "flowVersion": "3.1-labs",
        "projectName": "Perritos Felices — Semana 26 Octubre",
        "aspectRatio": "9:16",
        "engine": "Google Veo 3.1 Fast",
        "characters": [
            {
                "id": "char-lou",
                "name": "Lou",
                "role": "Canine Educator",
                "consistencyPrompt": "27-year-old female canine educator, authentic centennial Gen-Z vibe, straight long brunette hair, 1.60m, athletic 90-60-90 silhouette, oversized cobalt blue hoodie (#2C4BCA) and relaxed cargo pants, skate sneakers, warm genuine Hispanic smile",
                "referenceSeed": 948271
            },
            {
                "id": "char-frodo",
                "name": "Frodo",
                "role": "Blond Rescue Companion",
                "consistencyPrompt": "Small elongated dog, corgi and dachshund mix, sturdy short legs, dense golden honey caramel coat, hazel eyes, curled tail over back, wearing mint green anatomical Y-harness",
                "referenceSeed": 839211
            },
            {
                "id": "char-loki",
                "name": "Loki",
                "role": "Black Athletic Rescue Companion",
                "consistencyPrompt": "Medium sleek jet-black athletic dog, sighthound and labrador mix, distinct white patch on chest, expressive amber soulful eyes, wearing soft lavender anatomical Y-harness",
                "referenceSeed": 749102
            }
        ],
        "shots": [
            {
                "shotId": "shot-01-hook",
                "durationSeconds": 3.0,
                "camera": "Eye-level medium shot, shallow depth of field, warm morning living room sunlight",
                "charactersInFrame": ["char-lou", "char-frodo"],
                "action": "Lou sitting comfortably on wooden floor petting Frodo who yawns peacefully. Lou looks directly at the camera with sincere empathy.",
                "voiceover": "Si tu perro hace esto después del paseo... no lo regañes, te está pidiendo auxilio."
            },
            {
                "shotId": "shot-02-problem",
                "durationSeconds": 5.0,
                "camera": "Close-up macro shot on paws",
                "charactersInFrame": ["char-lou", "char-frodo"],
                "action": "Gentle hands of Lou gently lifting a paw, showing red skin between pads without causing any stress to the dog.",
                "voiceover": "El pasto tratado con fertilizantes o el polen se queda atrapado entre sus dedos y les quema la piel."
            },
            {
                "shotId": "shot-03-cta",
                "durationSeconds": 7.0,
                "camera": "Wide dynamic low-angle shot",
                "charactersInFrame": ["char-lou", "char-frodo", "char-loki"],
                "action": "Loki trots happily into frame wagging his tail. Lou rewards both dogs with a treat and smiles at camera.",
                "voiceover": "Un enjuague de 2 minutos les salva semanas de dermatitis. Ve a perritosfelices.com para la guía completa."
            }
        ]
    }


def main():
    print("🎨 Generando Sistema Visual Editorial PF-2027...")

    # Generar SVG artes
    p1 = ARTES_DIR / "post_01_instagram_loki.svg"
    p2 = ARTES_DIR / "post_02_instagram_frodo.svg"
    p3 = ARTES_DIR / "post_03_etologia_senales.svg"
    p4 = ARTES_DIR / "post_04_lou_arnes_en_y.svg"

    p1.write_text(generar_arte_loki(), encoding="utf-8")
    p2.write_text(generar_arte_frodo(), encoding="utf-8")
    p3.write_text(generar_arte_etologia(), encoding="utf-8")
    p4.write_text(generar_arte_lou(), encoding="utf-8")

    # Generar archivo de proyecto Google Flow
    flow_file = VIDEOS_DIR / "proyecto_semana_flow.json"
    flow_data = generar_flow_project()
    flow_file.write_text(json.dumps(flow_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Crear guión en texto plano para Creator Studio
    guion_file = VIDEOS_DIR / "guion_tiktok_lou_frodo_loki.txt"
    guion_text = """TIKTOK & REELS — PERRITOS FELICES
TEMA: Alergias y Picor de Patas
PROTAGONISTAS: Lou (Educadora), Frodo (El Rubio), Loki (El Negro)
DURACIÓN: 15 Segundos (Formato Vertical 9:16)
MOTOR DE VIDEO: Google Flow / Veo 3.1

[00:00 - 00:03] GANCHO:
Visual: Lou en el suelo acariciando a Frodo.
Voz: "Si tu perro hace esto después del paseo... no lo regañes, te está pidiendo auxilio."

[00:03 - 00:08] EL PROBLEMA:
Visual: Primer plano de patitas y cómo revisar suavemente entre dedos.
Voz: "El pasto tratado con fertilizantes o el polen se queda atrapado entre sus dedos y les quema la piel."

[00:08 - 00:15] SOLUCIÓN & CTA:
Visual: Loki entra moviendo la cola, Lou les da un premio a ambos.
Voz: "Un enjuague de 2 minutos les salva semanas de dermatitis. Ve a perritosfelices.com para la guía completa."

HASHTAGS: #PerritosFelices #AlergiasCaninas #LokiElPerro #FrodoElPerro #CuidadoRespetuoso #EducacionCanina #GuatePets
"""
    guion_file.write_text(guion_text, encoding="utf-8")

    # Empaquetar Kit Descargables ZIP Completo
    zip_path = WEEKLY_DIR / "kit_descargables_semana_2026_10_26.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 4 Plantillas Vectoriales SVG
        zf.write(p1, arcname="artes/post_01_instagram_loki.svg")
        zf.write(p2, arcname="artes/post_02_instagram_frodo.svg")
        zf.write(p3, arcname="artes/post_03_etologia_senales.svg")
        zf.write(p4, arcname="artes/post_04_lou_arnes_en_y.svg")

        # 4 Fotografías Editoriales de Alta Resolución (Generativas Flow)
        for img_name in [
            "post_01_loki_dermatologia.jpg",
            "post_02_frodo_nutricion.jpg",
            "post_03_etologia_calma.jpg",
            "post_04_lou_arnes_en_y.jpg"
        ]:
            img_file = ARTES_DIR / img_name
            if img_file.exists():
                zf.write(img_file, arcname=f"artes_hd/{img_name}")

        # Guiones y Proyecto Flow
        zf.write(flow_file, arcname="video_flow/proyecto_semana_flow.json")
        zf.write(guion_file, arcname="video_flow/guion_tiktok_lou_frodo_loki.txt")

        # Videos y Subtítulos
        reel_completo = VIDEOS_DIR / "reel_completo_lou_frodo_loki.mp4"
        if not reel_completo.exists():
            reel_completo = ROOT_DIR / "02_Estrategia_Y_Contenido" / "videos_flow_generados" / "reel_completo_lou_frodo_loki.mp4"
        if reel_completo.exists():
            zf.write(reel_completo, arcname="video_flow/reel_completo_lou_frodo_loki.mp4")

        srt_file = VIDEOS_DIR / "subtitulos_lou_reel.srt"
        if not srt_file.exists():
            srt_file = ROOT_DIR / "05_Studio_Privado" / "assets" / "subtitulos_lou_reel.srt"
        if srt_file.exists():
            zf.write(srt_file, arcname="video_flow/subtitulos_lou_reel.srt")

        ref_lou = ASSETS_DIR / "referencias_personajes" / "lou_frodo_loki_reference.jpg"
        if ref_lou.exists():
            zf.write(ref_lou, arcname="video_flow/lou_frodo_loki_reference.jpg")
            zf.write(ref_lou, arcname="referencias/lou_personaje_oficial.jpg")
        char_sheet = ASSETS_DIR / "referencias_personajes" / "LOU_CHARACTER_SHEET.md"
        if char_sheet.exists():
            zf.write(char_sheet, arcname="referencias/FICHA_TECNICA_LOU.md")

        # Proyecto Oficial Flow
        flow_proj_master = ROOT_DIR / "02_Estrategia_Y_Contenido" / "proyectos_flow" / "perritos_felices_flow" / "flow_project.json"
        if flow_proj_master.exists():
            zf.write(flow_proj_master, arcname="google_flow/flow_project_master.json")

        # 3 Personajes Oficiales por separado
        char_base = ASSETS_DIR / "personajes_oficiales"
        for cname in ["lou", "frodo", "loki"]:
            cdir = char_base / cname
            if cdir.exists():
                for f in cdir.glob("*"):
                    if f.is_file():
                        zf.write(f, arcname=f"personajes_oficiales/{cname}/{f.name}")

    print(f"✔ 4 Artes vectoriales generados en: {ARTES_DIR}")
    print(f"✔ Proyecto Google Flow generado en: {flow_file}")
    print(f"✔ Kit ZIP empaquetado: {zip_path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

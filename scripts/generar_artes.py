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


# =====================================================================
# PLANTILLAS EDITORIALES PF-2027 (ESTÁNDARES FIGMA RESOURCE LIBRARY)
# Fotografía Full-Bleed a sangre, gradientes cinematográficos y logo oficial
# =====================================================================

def get_official_logo_uri() -> str:
    logo_path = ASSETS_DIR / "fulllogo_transparent_nobuffer.png"
    if not logo_path.exists():
        logo_path = ASSETS_DIR / "fulllogo_transparent.png"
    return get_image_data_uri(logo_path)


# 1. PLANTILLA 1: GUÍA MÉDICA / SALUD — FULL-BLEED EDITORIAL
def generar_arte_loki() -> str:
    loki_img = ARTES_DIR / "post_01_loki_dermatologia.jpg"
    if not loki_img.exists():
        loki_img = ASSETS_DIR / "referencias_mascotas" / "loki_01_face.jpg"
    img_uri = get_image_data_uri(loki_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 64px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 500; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <!-- Gradiente Cinematográfico Full-Bleed (Regla Figma Safe-Zones) -->
    <linearGradient id="scrimLoki" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.45" />
      <stop offset="30%" stop-color="#10152B" stop-opacity="0.05" />
      <stop offset="55%" stop-color="#10152B" stop-opacity="0.5" />
      <stop offset="80%" stop-color="#10152B" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.98" />
    </linearGradient>
  </defs>

  <!-- Fotografía Protagonista a Sangre Completa -->
  <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  
  <!-- Veladura de Contraste Tipográfico -->
  <rect width="1080" height="1080" fill="url(#scrimLoki)" />

  <!-- Cabecera Superior (Safe Zone: 64px) con Logo Oficial Nítido (Sin sellos invasivos) -->
  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(16, 21, 43, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">SALUD // DERMATOLOGÍA</text>
  </g>

  <!-- Bloque Tipográfico Hero (Foco Único: Pregunta Provocadora + Diagnóstico) -->
  <g transform="translate(64, 660)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro se lame</tspan>
      <tspan x="0" y="74" class="title-accent">las patas sin parar?</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="155">No es maña ni ansiedad. El 80% de los casos es picor</tspan>
      <tspan x="0" y="195">por contacto con polen o pesticidas tras el paseo.</tspan>
    </text>

    <!-- Barra de Acción y Deslizar -->
    <g transform="translate(0, 240)">
      <rect width="380" height="54" rx="27" fill="#FDB54A" />
      <text x="190" y="34" class="cta-txt" text-anchor="middle">DESLIZA PARA VER LA GUÍA ➔</text>
      <text x="420" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="rgba(255, 255, 255, 0.8)">Cuidado Veterinario Preventivo</text>
    </g>
  </g>
</svg>"""


# 2. PLANTILLA 2: NUTRICIÓN FRESCA Y RECETAS — FULL-BLEED EDITORIAL
def generar_arte_frodo() -> str:
    frodo_img = ARTES_DIR / "post_02_frodo_nutricion.jpg"
    if not frodo_img.exists():
        frodo_img = ASSETS_DIR / "referencias_mascotas" / "frodo_01_front.jpg"
    img_uri = get_image_data_uri(frodo_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 62px; font-weight: 800; fill: #FFFFFF; line-height: 1.08; }}
      .title-accent {{ fill: #FFE082; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 500; fill: #FFF3E0; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
      .pill-ing {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17px; font-weight: 700; fill: #FFFFFF; }}
    </style>
    <linearGradient id="scrimFrodo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1A1208" stop-opacity="0.45" />
      <stop offset="30%" stop-color="#1A1208" stop-opacity="0.05" />
      <stop offset="55%" stop-color="#1A1208" stop-opacity="0.5" />
      <stop offset="80%" stop-color="#1A1208" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#1A1208" stop-opacity="0.98" />
    </linearGradient>
  </defs>

  <!-- Fotografía Protagonista a Sangre Completa -->
  <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  
  <!-- Veladura Cálida -->
  <rect width="1080" height="1080" fill="url(#scrimFrodo)" />

  <!-- Cabecera Superior con Logo Oficial Nítido -->
  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(26, 18, 8, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">COCINA // RECETA FRESCA</text>
  </g>

  <!-- Bloque Tipográfico Hero -->
  <g transform="translate(64, 650)">
    <!-- 3 Pills de Ingredientes Limpias -->
    <g transform="translate(0, 0)">
      <rect width="180" height="38" rx="19" fill="rgba(255, 255, 255, 0.2)" />
      <text x="90" y="25" class="pill-ing" text-anchor="middle">🍉 Sandía natural</text>

      <rect x="195" y="0" width="195" height="38" rx="19" fill="rgba(255, 255, 255, 0.2)" />
      <text x="292" y="25" class="pill-ing" text-anchor="middle">🥛 Yogur sin lactosa</text>

      <rect x="405" y="0" width="155" height="38" rx="19" fill="rgba(255, 255, 255, 0.2)" />
      <text x="482" y="25" class="pill-ing" text-anchor="middle">🌱 Menta fresca</text>
    </g>

    <text class="title">
      <tspan x="0" y="95">Helado casero de</tspan>
      <tspan x="0" y="165" class="title-accent">sandía &amp; yogur fresco</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="225">Digestivo, hidratante y antiinflamatorio para días calurosos.</tspan>
    </text>

    <!-- Botón CTA -->
    <g transform="translate(0, 260)">
      <rect width="360" height="54" rx="27" fill="#FFE082" />
      <text x="180" y="34" class="cta-txt" text-anchor="middle">VER RECETA PASO A PASO ➔</text>
      <text x="400" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="rgba(255, 255, 255, 0.8)">Snack Saludable &amp; Seguro</text>
    </g>
  </g>
</svg>"""


# 3. PLANTILLA 3: ETOLOGÍA & SEÑALES DE CALMA — FULL-BLEED EDITORIAL
def generar_arte_etologia() -> str:
    eto_img = ARTES_DIR / "post_03_etologia_calma.jpg"
    img_uri = get_image_data_uri(eto_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 62px; font-weight: 800; fill: #FFFFFF; line-height: 1.1; }}
      .title-accent {{ fill: #81C784; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 500; fill: #E8F5E9; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
    </style>
    <linearGradient id="scrimEto" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E2312" stop-opacity="0.45" />
      <stop offset="30%" stop-color="#0E2312" stop-opacity="0.05" />
      <stop offset="55%" stop-color="#0E2312" stop-opacity="0.5" />
      <stop offset="80%" stop-color="#0E2312" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#0E2312" stop-opacity="0.98" />
    </linearGradient>
  </defs>

  <!-- Fotografía Protagonista a Sangre Completa -->
  <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  
  <!-- Veladura Verde Bosque Oscuro -->
  <rect width="1080" height="1080" fill="url(#scrimEto)" />

  <!-- Cabecera Superior con Logo Oficial Nítido -->
  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(14, 35, 18, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">ETOLOGÍA // LENGUAJE</text>
  </g>

  <!-- Bloque Tipográfico Hero -->
  <g transform="translate(64, 660)">
    <text class="title">
      <tspan x="0" y="0">¿Tu perro bosteza o</tspan>
      <tspan x="0" y="74" class="title-accent">se lame la trufa al abrazarlo?</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="155">No tiene sueño ni hambre: te está pidiendo espacio.</tspan>
      <tspan x="0" y="195">Aprender a leer su lenguaje es el mayor acto de amor.</tspan>
    </text>

    <!-- Botón CTA -->
    <g transform="translate(0, 240)">
      <rect width="380" height="54" rx="27" fill="#81C784" />
      <text x="190" y="34" class="cta-txt" text-anchor="middle">DESCUBRE LAS 5 SEÑALES ➔</text>
      <text x="420" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="rgba(255, 255, 255, 0.8)">Educación 100% Positiva • Fear-Free</text>
    </g>
  </g>
</svg>"""


# 4. PLANTILLA 4: "LOU TE ENSEÑA" (ARNÉS EN Y) — FULL-BLEED EDITORIAL
def generar_arte_lou() -> str:
    lou_img = ARTES_DIR / "post_04_lou_arnes_en_y.jpg"
    if not lou_img.exists():
        lou_img = ARTES_DIR / "post_04_lou_arnes.jpg"
    img_uri = get_image_data_uri(lou_img)
    logo_uri = get_official_logo_uri()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 58px; font-weight: 800; fill: #FFFFFF; line-height: 1.1; }}
      .title-accent {{ fill: #FDB54A; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 500; fill: #E8EDFF; line-height: 1.4; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; fill: #10152B; }}
      .quote-italics {{ font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 32px; font-weight: 700; fill: #FDB54A; }}
    </style>
    <linearGradient id="scrimLou" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.45" />
      <stop offset="30%" stop-color="#10152B" stop-opacity="0.05" />
      <stop offset="55%" stop-color="#10152B" stop-opacity="0.5" />
      <stop offset="80%" stop-color="#10152B" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.98" />
    </linearGradient>
  </defs>

  <!-- Fotografía Protagonista de Lou a Sangre Completa -->
  <image href="{img_uri}" x="0" y="0" width="1080" height="1080" preserveAspectRatio="xMidYMid slice" />
  
  <!-- Veladura de Contraste Tipográfico AzulPF Profundo -->
  <rect width="1080" height="1080" fill="url(#scrimLou)" />

  <!-- Cabecera Superior con Logo Oficial Nítido -->
  <g transform="translate(64, 64)">
    <rect width="360" height="56" rx="28" fill="rgba(16, 21, 43, 0.75)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">PASEO RESPETUOSO // GUÍA</text>
  </g>

  <!-- Bloque Tipográfico Hero con la Cita Inmortal de Lou -->
  <g transform="translate(64, 650)">
    <text class="quote-italics">"El dolor jamás enseña respeto, solo pánico."</text>

    <text class="title">
      <tspan x="0" y="68">Arnés ergonómico en 'Y':</tspan>
      <tspan x="0" y="136" class="title-accent">Paseos sin tirones ni ahogo.</tspan>
    </text>

    <text class="subtitle">
      <tspan x="0" y="205">Libera hombros, protege tráquea y cervicales.</tspan>
    </text>

    <!-- Botón CTA -->
    <g transform="translate(0, 245)">
      <rect width="360" height="54" rx="27" fill="#FDB54A" />
      <text x="180" y="34" class="cta-txt" text-anchor="middle">GUÍA DE ELECCIÓN DE ARNÉS ➔</text>
      <text x="400" y="35" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="rgba(255, 255, 255, 0.8)">Educación Canina Amable</text>
    </g>
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

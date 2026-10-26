#!/usr/bin/env python3
"""
Motor Gráfico Editorial PF-2027 (Zero-Tokens / Local)
Genera artes listos para redes (Instagram 1080x1080, Banners 1920x1080, Stories 1080x1920)
cumpliendo la identidad oficial: Azul Cobalto (#2C4BCA), Amarillo (#FDB54A), Fraunces y Space Mono.
"""

import base64
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
DELIVERY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido" / "entregas_semanales" / "semana_2026_10_26" / "artes"


def img_to_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_instagram_post(title: str, subtitle: str, category_tag: str, image_path: Path, output_path: Path):
    data_uri = img_to_data_uri(image_path)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700;9..144,800&amp;family=Plus+Jakarta+Sans:wght@500;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      .font-display {{ font-family: 'Fraunces', serif; }}
      .font-sans {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
      .font-mono {{ font-family: 'Space Mono', monospace; }}
    </style>
    <linearGradient id="gradOver" x1="0" y1="0.3" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0" />
      <stop offset="65%" stop-color="#10152B" stop-opacity="0.85" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.98" />
    </linearGradient>
    <clipPath id="squircleClip">
      <rect x="40" y="40" width="1000" height="1000" rx="40" ry="40" />
    </clipPath>
  </defs>

  <!-- Fondo General -->
  <rect width="1080" height="1080" fill="#FDFBF7" />

  <!-- Marco Exterior Squircle -->
  <g clip-path="url(#squircleClip)">
    <!-- Foto del perro / personaje -->
    <image href="{data_uri}" x="40" y="40" width="1000" height="1000" preserveAspectRatio="xMidYMid slice" />
    
    <!-- Degradado cinematográfico de lectura -->
    <rect x="40" y="300" width="1000" height="740" fill="url(#gradOver)" />

    <!-- Topbar Marca -->
    <rect x="80" y="80" width="280" height="48" rx="24" fill="#2C4BCA" />
    <text x="105" y="111" class="font-mono" font-size="16" font-weight="700" fill="#FFFFFF">PERRITOS FELICES</text>

    <!-- Chip de Categoría -->
    <rect x="80" y="700" width="220" height="40" rx="20" fill="#FDB54A" />
    <text x="105" y="726" class="font-mono" font-size="14" font-weight="700" fill="#10152B">{category_tag.upper()}</text>

    <!-- Titular Editorial Impactante -->
    <text x="80" y="800" class="font-display" font-size="52" font-weight="800" fill="#FFFFFF">{title}</text>

    <!-- Subtítulo / Gancho -->
    <text x="80" y="870" class="font-sans" font-size="24" font-weight="500" fill="#E8EDFF">{subtitle}</text>

    <!-- Barra Inferior de Acción / Swipe -->
    <line x1="80" y1="940" x2="1000" y2="940" stroke="#FDB54A" stroke-width="2" stroke-opacity="0.5" />
    <text x="80" y="985" class="font-sans" font-size="20" font-weight="700" fill="#FFFFFF">Guarda este post y visita perritosfelices.com</text>
    <text x="960" y="985" class="font-mono" font-size="22" font-weight="700" fill="#FDB54A">➔</text>
  </g>
</svg>"""
    output_path.write_text(svg, encoding="utf-8")


def main():
    DELIVERY_DIR.mkdir(parents=True, exist_ok=True)
    ref_loki = ASSETS_DIR / "referencias_mascotas" / "loki_01_face.jpg"
    ref_frodo = ASSETS_DIR / "referencias_mascotas" / "frodo_01_front.jpg"

    # Arte 1: Instagram Post con Loki
    render_instagram_post(
      title="¿Tu perro se lame las patas?",
      subtitle="3 señales silenciosas de alergia ambiental que confunden con manía.",
      category_tag="Salud y Prevención",
      image_path=ref_loki,
      output_path=DELIVERY_DIR / "post_01_instagram_loki.svg"
    )

    # Arte 2: Instagram Post con Frodo
    render_instagram_post(
      title="Cuidado con los Helados Caseros",
      subtitle="Los ingredientes prohibidos que jamás debes poner en sus snacks.",
      category_tag="Nutrición Canina",
      image_path=ref_frodo,
      output_path=DELIVERY_DIR / "post_02_instagram_frodo.svg"
    )

    print("✔ Artes SVG de alta fidelidad generados en:", DELIVERY_DIR)


if __name__ == "__main__":
    main()

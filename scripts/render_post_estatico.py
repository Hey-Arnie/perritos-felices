#!/usr/bin/env python3
"""
render_post_estatico.py — Motor de Renderizado Code-to-Image (PF-2027)
Aplica estrictamente el Blueprint Visual de PerritosFelices.com:
- Composición determinista en HTML5 + CSS + SVG puro (Cero AI Slop)
- Integración de los personajes paramétricos oficiales: Loki y Frodo (dog_characters_svg.py)
- Tipografía nativa Plus Jakarta Sans (800) e Inter (400/500)
- Salida 4:5 vertical (1080x1350 px lógicas / 2160x2700 px Retina 2x)
- Renderizado determinista mediante Google Chrome Headless + sips
"""

import argparse
import base64
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Rutas del proyecto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
OUTPUT_DIR = ASSETS_DIR / "posts_estaticos_blueprint"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Asegurar import de dog_characters_svg
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))
import dog_characters_svg as dogs

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_official_logo_svg_or_b64() -> str:
    """Retorna el logotipo oficial como data URI para incrustar sin dependencias."""
    logo_path = ASSETS_DIR / "fulllogo_transparent_nobuffer.png"
    if not logo_path.exists():
        logo_path = ASSETS_DIR / "pack_logos_originales_master" / "fulllogo_transparent_nobuffer.png"
    if not logo_path.exists():
        logo_path = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "logo" / "fulllogo_transparent_nobuffer.png"
    if logo_path.exists():
        data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{data}"
    return ""


def build_html_post(
    category_badge: str,
    title: str,
    subtitle: str,
    main_content_html: str,
    footer_note: str = "perritosfelices.com",
    footer_action: str = "Toca para guardar o compartir",
) -> str:
    """
    Plantilla base de diseño editorial según el Blueprint Visual:
    - Lienzo: #F8FAFC (Slate 50)
    - Títulos: Plus Jakarta Sans 800
    - Textos: Inter 400/500
    - Cabecera con badge y logotipo a 44px
    """
    logo_uri = get_official_logo_svg_or_b64()
    logo_html = f'<img src="{logo_uri}" style="height: 48px; width: auto;" alt="Perritos Felices" />' if logo_uri else '<span style="font-weight: 800; font-size: 24px; color: #FF6B35;">Perritos Felices</span>'

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: 1080px;
      height: 1350px;
      background-color: #F8FAFC;
      color: #0F172A;
      font-family: 'Inter', -apple-system, sans-serif;
      padding: 70px 65px 80px 65px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      position: relative;
    }}

    /* Cabecera */
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      height: 60px;
    }}
    .badge {{
      background: #FF6B35;
      color: #FFFFFF;
      padding: 8px 22px;
      border-radius: 24px;
      font-weight: 800;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 18px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}

    /* Contenido Principal */
    .main-body {{
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: center;
      margin-top: 25px;
      margin-bottom: 25px;
    }}
    .title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 56px;
      font-weight: 800;
      line-height: 1.14;
      color: #0F172A;
      letter-spacing: -0.025em;
      margin-bottom: 16px;
    }}
    .subtitle {{
      font-size: 24px;
      font-weight: 500;
      color: #475569;
      line-height: 1.42;
      margin-bottom: 30px;
    }}

    /* Zona del Contenido Especializado */
    .content-canvas {{
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    /* Pie de Página */
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 2px solid #E2E8F0;
      padding-top: 25px;
      width: 100%;
    }}
    .footer-brand {{
      font-size: 20px;
      font-weight: 600;
      color: #64748B;
      letter-spacing: -0.01em;
    }}
    .footer-cta {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 20px;
      font-weight: 700;
      color: #FF6B35;
    }}
  </style>
</head>
<body>
  <div class="header">
    <span class="badge">{category_badge}</span>
    {logo_html}
  </div>

  <div class="main-body">
    <h1 class="title">{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="content-canvas">
      {main_content_html}
    </div>
  </div>

  <div class="footer">
    <span class="footer-brand">{footer_note}</span>
    <span class="footer-cta">{footer_action} →</span>
  </div>
</body>
</html>"""


# ==============================================================================
# FORMATOS ESPECÍFICOS DEL BLUEPRINT
# ==============================================================================

def build_formato_semaforo_frutas() -> str:
    """Formato 3: La Guía de Bolsillo (Semáforo de Frutas para Perros)."""
    loki_happy = dogs.render_dog_svg("loki", "happy", width=280, height=280)
    frodo_stress = dogs.render_dog_svg("frodo", "stress", width=240, height=240)

    content = f"""
    <div style="display: flex; flex-direction: column; width: 100%; gap: 16px;">
      <!-- Verde: Seguras -->
      <div style="background: #FFFFFF; border: 2.5px solid #2EC4B6; border-radius: 18px; padding: 22px 28px; display: flex; align-items: center; gap: 24px; box-shadow: 0 4px 12px rgba(46, 196, 182, 0.08);">
        <div style="background: #2EC4B6; color: white; width: 54px; height: 54px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 800; flex-shrink: 0;">✓</div>
        <div style="flex: 1;">
          <h3 style="font-family: 'Plus Jakarta Sans'; font-size: 26px; color: #0F172A; font-weight: 800;">Verde (Seguras y Frescas)</h3>
          <p style="font-size: 20px; color: #334155; margin-top: 4px; line-height: 1.35;">• <b>Zanahoria:</b> cruda o al vapor (limpia dientes).<br>• <b>Sandía:</b> cubos frescos sin semillas ni cáscara.<br>• <b>Pepino:</b> hidratante bajo en calorías.</p>
        </div>
      </div>

      <!-- Amarillo: Precaución / Dosis -->
      <div style="background: #FFFFFF; border: 2.5px solid #F59E0B; border-radius: 18px; padding: 22px 28px; display: flex; align-items: center; gap: 24px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.08);">
        <div style="background: #F59E0B; color: white; width: 54px; height: 54px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 800; flex-shrink: 0;">!</div>
        <div style="flex: 1;">
          <h3 style="font-family: 'Plus Jakarta Sans'; font-size: 26px; color: #0F172A; font-weight: 800;">Amarillo (Con Moderación)</h3>
          <p style="font-size: 20px; color: #334155; margin-top: 4px; line-height: 1.35;">• <b>Plátano y Manzana:</b> sin centro ni semillas (azúcar natural). Máximo 10% de su ración diaria.</p>
        </div>
      </div>

      <!-- Rojo: Tóxicas Prohibidas -->
      <div style="background: #FFFFFF; border: 2.5px solid #E63946; border-radius: 18px; padding: 22px 28px; display: flex; align-items: center; gap: 24px; box-shadow: 0 4px 12px rgba(230, 57, 70, 0.08);">
        <div style="background: #E63946; color: white; width: 54px; height: 54px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 800; flex-shrink: 0;">✕</div>
        <div style="flex: 1;">
          <h3 style="font-family: 'Plus Jakarta Sans'; font-size: 26px; color: #E63946; font-weight: 800;">Rojo (Peligro Renal Severo)</h3>
          <p style="font-size: 20px; color: #334155; margin-top: 4px; line-height: 1.35;">• <b>Uvas y Pasas:</b> causan fallo renal agudo en cualquier dosis.<br>• <b>Cebolla, ajo y chocolate:</b> estrictamente prohibidos.</p>
        </div>
      </div>

      <!-- Personajes en base -->
      <div style="display: flex; justify-content: space-around; align-items: flex-end; margin-top: 10px;">
        <div style="text-align: center;">
          {loki_happy}
          <span style="font-family: 'Plus Jakarta Sans'; font-weight: 700; color: #FF6B35; font-size: 18px;">Loki disfruta lo seguro</span>
        </div>
        <div style="text-align: center;">
          {frodo_stress}
          <span style="font-family: 'Plus Jakarta Sans'; font-weight: 700; color: #E63946; font-size: 18px;">Frodo evita las uvas</span>
        </div>
      </div>
    </div>
    """
    return build_html_post(
        category_badge="Nutrición Canina",
        title="Frutas Seguras vs. Uvas en Casa: Semáforo de Bolsillo",
        subtitle="Antes de compartir de tu plato en la cocina, consulta qué premios son saludables y cuáles ponen en riesgo sus riñones.",
        main_content_html=content,
        footer_note="perritosfelices.com • Basado en evidencia WSAVA/EBVM",
        footer_action="Guarda esta guía rápida",
    )


def build_formato_contraste_arnes() -> str:
    """Formato 2: Carrusel de Contraste (Lo que haces vs. Lo que tu perro siente con el arnés)."""
    loki_alert = dogs.render_dog_svg("loki", "alert", width=290, height=290)
    frodo_stress = dogs.render_dog_svg("frodo", "fear", width=290, height=290)

    content = f"""
    <div style="display: flex; flex-direction: column; width: 100%; gap: 20px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
        <!-- Lado Humano / Error -->
        <div style="background: #FFFFFF; border: 2.5px solid #E2E8F0; border-radius: 20px; padding: 28px 24px; display: flex; flex-direction: column; align-items: center; text-align: center;">
          <span style="background: #FFE4E6; color: #E63946; font-weight: 800; font-family: 'Plus Jakarta Sans'; padding: 6px 16px; border-radius: 12px; font-size: 17px; margin-bottom: 12px;">Pechera Recta Tradicional</span>
          {frodo_stress}
          <h4 style="font-family: 'Plus Jakarta Sans'; font-size: 22px; color: #E63946; font-weight: 800; margin-top: 8px;">Lo que siente tu perro</h4>
          <p style="font-size: 18px; color: #475569; margin-top: 8px; line-height: 1.35;">La tira horizontal cruza directamente los hombros, bloqueando su zancada y forzando sus articulaciones al caminar.</p>
        </div>

        <!-- Lado Etológico / Solución -->
        <div style="background: #FFFFFF; border: 2.5px solid #2EC4B6; border-radius: 20px; padding: 28px 24px; display: flex; flex-direction: column; align-items: center; text-align: center; box-shadow: 0 6px 16px rgba(46, 196, 182, 0.1);">
          <span style="background: #D1FAE5; color: #059669; font-weight: 800; font-family: 'Plus Jakarta Sans'; padding: 6px 16px; border-radius: 12px; font-size: 17px; margin-bottom: 12px;">Arnés Ergonómico en Y</span>
          {loki_alert}
          <h4 style="font-family: 'Plus Jakarta Sans'; font-size: 22px; color: #059669; font-weight: 800; margin-top: 8px;">Libertad de movimiento</h4>
          <p style="font-size: 18px; color: #475569; margin-top: 8px; line-height: 1.35;">Forma una "Y" en el pecho, deja la tráquea libre y permite el movimiento natural completo de los hombros.</p>
        </div>
      </div>

      <!-- Tip práctico -->
      <div style="background: #F1F5F9; border-radius: 16px; padding: 18px 24px; display: flex; align-items: center; gap: 16px;">
        <span style="font-size: 28px;">💡</span>
        <p style="font-size: 19px; color: #1E293B; font-weight: 500; line-height: 1.35;"><b>Regla de los 2 dedos:</b> La cinta del abdomen debe quedar al menos a 2 o 3 dedos detrás de las axilas para evitar rozaduras.</p>
      </div>
    </div>
    """
    return build_html_post(
        category_badge="Paseo y Bienestar",
        title="Pechera Recta vs. Arnés en Y: ¿Qué Siente tu Perro?",
        subtitle="Un perro que camina con un arnés restrictivo modifica su marcha para no sentir molestias. Mira la diferencia en su anatomía.",
        main_content_html=content,
        footer_note="perritosfelices.com • Educación sin métodos aversivos",
        footer_action="Lee la guía de paseo",
    )


def build_formato_senales_calma() -> str:
    """Formato 1: El Mapa de Señales (Infografía Anatómica de Señales de Calma)."""
    frodo_stress = dogs.render_dog_svg("frodo", "stress", width=380, height=380)

    content = f"""
    <div style="display: flex; flex-direction: column; width: 100%; align-items: center; gap: 20px;">
      <!-- Personaje central con marcadores -->
      <div style="position: relative; width: 420px; height: 380px; display: flex; justify-content: center;">
        {frodo_stress}
        <!-- Punteros flotantes tipo manual etológico -->
        <div style="position: absolute; top: 75px; left: -40px; background: white; border: 2px solid #FF6B35; border-radius: 12px; padding: 8px 14px; font-size: 16px; font-weight: 700; color: #0F172A; box-shadow: 0 4px 10px rgba(0,0,0,0.06);">
          1. Orejas hacia atrás 👂
        </div>
        <div style="position: absolute; top: 135px; right: -50px; background: white; border: 2px solid #FF6B35; border-radius: 12px; padding: 8px 14px; font-size: 16px; font-weight: 700; color: #0F172A; box-shadow: 0 4px 10px rgba(0,0,0,0.06);">
          2. Ojo de ballena (esclera) 👀
        </div>
        <div style="position: absolute; bottom: 85px; left: -50px; background: white; border: 2px solid #FF6B35; border-radius: 12px; padding: 8px 14px; font-size: 16px; font-weight: 700; color: #0F172A; box-shadow: 0 4px 10px rgba(0,0,0,0.06);">
          3. Lamido rápido de trufa 👅
        </div>
      </div>

      <!-- Cuadrícula explicativa -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; width: 100%; margin-top: 10px;">
        <div style="background: white; border-radius: 16px; padding: 18px 20px; border: 1.5px solid #E2E8F0;">
          <h4 style="font-family: 'Plus Jakarta Sans'; font-size: 20px; color: #FF6B35; font-weight: 800;">¿Por qué lo hacen?</h4>
          <p style="font-size: 17px; color: #475569; margin-top: 6px; line-height: 1.35;">Son gestos corporales de autorregulación (Turid Rugaas) para pedir espacio amablemente y calmar la tensión.</p>
        </div>
        <div style="background: white; border-radius: 16px; padding: 18px 20px; border: 1.5px solid #E2E8F0;">
          <h4 style="font-family: 'Plus Jakarta Sans'; font-size: 20px; color: #2EC4B6; font-weight: 800;">¿Qué debes hacer?</h4>
          <p style="font-size: 17px; color: #475569; margin-top: 6px; line-height: 1.35;">Detén la caricia intensa, da un paso atrás y reduce el estímulo. Escuchar estas señales previene el gruñido.</p>
        </div>
      </div>
    </div>
    """
    return build_html_post(
        category_badge="Lenguaje Canino",
        title="3 Señales Tempranas de que tu Perro Pide Espacio",
        subtitle="Mucho antes de ladrar o apartarse, los perros conversan con pequeños gestos sutiles en rostro y postura.",
        main_content_html=content,
        footer_note="perritosfelices.com • Etología clínica Fear-Free",
        footer_action="Comparte con un tutor",
    )


def build_formato_desmontador_mitos() -> str:
    """Formato 5: El Desmontador de Mitos (Mito de la dominancia vs Ciencia)."""
    loki_calm = dogs.render_dog_svg("loki", "calm", width=310, height=310)

    content = f"""
    <div style="display: flex; flex-direction: column; width: 100%; gap: 20px;">
      <!-- Sello Falso -->
      <div style="background: #FEF2F2; border: 2.5px solid #E63946; border-radius: 20px; padding: 24px 28px; position: relative;">
        <span style="background: #E63946; color: white; font-family: 'Plus Jakarta Sans'; font-weight: 800; padding: 4px 16px; border-radius: 8px; font-size: 16px; text-transform: uppercase;">Mito Popular</span>
        <h3 style="font-family: 'Plus Jakarta Sans'; font-size: 26px; color: #991B1B; font-weight: 800; margin-top: 10px;">
          "Tu perro se sube al sillón o sale primero por la puerta para dominarte"
        </h3>
        <p style="font-size: 19px; color: #7F1D1D; margin-top: 6px; line-height: 1.35;">Falso. La teoría de la dominancia sobre lobos cautivos de los años 70 fue refutada hace décadas por la propia ciencia veterinaria.</p>
      </div>

      <!-- Realidad Científica -->
      <div style="background: #FFFFFF; border: 2.5px solid #2EC4B6; border-radius: 20px; padding: 24px 28px; display: flex; align-items: center; gap: 24px; box-shadow: 0 4px 14px rgba(46, 196, 182, 0.1);">
        <div style="flex: 1;">
          <span style="background: #D1FAE5; color: #059669; font-family: 'Plus Jakarta Sans'; font-weight: 800; padding: 4px 16px; border-radius: 8px; font-size: 16px; text-transform: uppercase;">La Realidad Etológica</span>
          <h3 style="font-family: 'Plus Jakarta Sans'; font-size: 26px; color: #0F172A; font-weight: 800; margin-top: 10px;">
            Busca comodidad y estímulos
          </h3>
          <p style="font-size: 19px; color: #334155; margin-top: 6px; line-height: 1.4;">
            El sillón es suave y huele a ti. Salir rápido es pura emoción por oler el parque. La relación con tu perro se basa en apego seguro y comunicación clara, no en jerarquías de manada.
          </p>
        </div>
        <div style="flex-shrink: 0;">
          {loki_calm}
        </div>
      </div>
    </div>
    """
    return build_html_post(
        category_badge="Etología y Ciencia",
        title="El Gran Mito de la Dominancia: Lo que Dice la Ciencia",
        subtitle="Tu perro no compite contra ti por el control de la casa. Entiende las verdaderas motivaciones de su conducta.",
        main_content_html=content,
        footer_note="perritosfelices.com • Consenso AVSAB / Karen Overall",
        footer_action="Guarda para consultar",
    )


# ==============================================================================
# COMPILACIÓN A ALTA RESOLUCIÓN HEADLESS
# ==============================================================================

def render_html_to_retina_image(html_content: str, output_path: Path, retina: bool = True) -> bool:
    """Renderiza el HTML en resolución 1080x1350 (o 2160x2700 Retina 2x) usando Chrome Headless."""
    if not Path(CHROME_BIN).exists():
        print(f"❌ Error: Chrome no encontrado en {CHROME_BIN}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory(prefix="pf_blueprint_") as tmpdir:
        tmp_dir = Path(tmpdir)
        html_file = tmp_dir / "canvas.html"
        tmp_png = tmp_dir / "capture.png"
        chrome_profile = tmp_dir / "chrome_profile"

        html_file.write_text(html_content, encoding="utf-8")

        # Escala Retina 2x si se solicita
        window_size = "2160,2700" if retina else "1080,1350"

        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--no-sandbox",
            f"--user-data-dir={chrome_profile}",
            "--disable-gpu",
            f"--window-size={window_size}",
            "--hide-scrollbars",
            f"--screenshot={tmp_png}",
            html_file.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if not tmp_png.exists():
            print(f"❌ Error en renderizado: {res.stderr[-300:]}", file=sys.stderr)
            return False

        # Si el destino es JPEG o PNG, convertir con sips
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fmt = "jpeg" if output_path.suffix.lower() in (".jpg", ".jpeg") else "png"
        sips_cmd = ["sips", "-s", "format", fmt]
        if fmt == "jpeg":
            sips_cmd.extend(["-s", "formatOptions", "95"])
        sips_cmd.extend([str(tmp_png), "--out", str(output_path)])

        subprocess.run(sips_cmd, capture_output=True, text=True, check=True)
        return True


def render_all_preset_posts():
    """Genera el lote inicial de 4 posts estáticos basados en el Blueprint Visual."""
    print("=" * 72)
    print(" 🎨 COMPILANDO POSTS ESTÁTICOS DETERMINISTAS (BLUEPRINT VISUAL 2027)")
    print("=" * 72)

    posts = [
        ("post_01_semaforo_frutas", build_formato_semaforo_frutas),
        ("post_02_contraste_arnes", build_formato_contraste_arnes),
        ("post_03_mapa_senales_calma", build_formato_senales_calma),
        ("post_04_desmontador_mitos", build_formato_desmontador_mitos),
    ]

    for slug, builder in posts:
        html = builder()
        html_dest = OUTPUT_DIR / f"{slug}.html"
        jpg_dest = OUTPUT_DIR / f"{slug}.jpg"
        png_retina_dest = OUTPUT_DIR / f"{slug}_2x_retina.png"

        html_dest.write_text(html, encoding="utf-8")
        ok_jpg = render_html_to_retina_image(html, jpg_dest, retina=False)
        ok_png = render_html_to_retina_image(html, png_retina_dest, retina=True)

        if ok_jpg and ok_png:
            jpg_kb = jpg_dest.stat().st_size / 1024
            png_kb = png_retina_dest.stat().st_size / 1024
            print(f" ✔ [{slug}]")
            print(f"    • JPG Feed (1080x1350): {jpg_kb:.1f} KB -> {jpg_dest.relative_to(ROOT_DIR)}")
            print(f"    • PNG Retina 2x (2160x2700): {png_kb:.1f} KB -> {png_retina_dest.relative_to(ROOT_DIR)}")
        else:
            print(f" ❌ Falló renderizado de {slug}")

    print("=" * 72)
    print(" ✅ LOTE DE POSTS ESTÁTICOS VECTORIALES COMPLETADO")
    print("=" * 72)


if __name__ == "__main__":
    render_all_preset_posts()

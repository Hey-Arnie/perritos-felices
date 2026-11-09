#!/usr/bin/env python3
"""
GENERADOR DE ARTES EDITORIALES PARA REDES SOCIALES (PF-2027)
Aplica los lineamientos de:
- alchaincyf/huashu-design (composición editorial limpia, jerarquía tipográfica y aire visual)
- charlie947/social-media-skills (graphic-designer & post-writer)
- blader/humanizer (redacción natural, empática y libre de clichés de IA)
Produce piezas verticales 4:5 (1080x1350) con >75% de fotografía limpia y logotipo oficial íntegro.
"""

import base64
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
WEB_ASSETS = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos"
REDES_2026_DIR = ASSETS_DIR / "artes_redes_2026"
WEEKLY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido" / "entregas_semanales" / "semana_2026_10_26"
ARTES_DIR = WEEKLY_DIR / "artes"
STUDIO_ASSETS = ROOT_DIR / "05_Studio_Privado" / "assets"

REDES_2026_DIR.mkdir(parents=True, exist_ok=True)
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


def build_editorial_card_svg(
    img_uri: str,
    logo_uri: str,
    category_label: str,
    title_line_1: str,
    title_line_2: str,
    subtitle_line_1: str,
    subtitle_line_2: str,
    footer_note: str = "perritosfelices.com",
) -> str:
    """
    Composición editorial limpia 4:5 (1080x1350):
    - 75% superior de la fotografía completamente despejado (cero oclusión de ojos, trufa o patitas).
    - Cabecera discreta con el logotipo oficial completo sobre pastilla crema traslúcida.
    - Degradado inferior suave (máximo 76% de opacidad en la base) para lectura cómoda.
    """
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&amp;family=Plus+Jakarta+Sans:wght@500;600;700&amp;display=swap');
      .brand-pill-txt {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 20px; font-weight: 600; fill: #181D2E; letter-spacing: -0.01em; }}
      .cat-pill-txt {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 18px; font-weight: 600; fill: #FDB54A; letter-spacing: 0.02em; }}
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 700; fill: #FFFFFF; letter-spacing: -0.025em; }}
      .title-warm {{ fill: #FFE2AD; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 26px; font-weight: 500; fill: rgba(255, 255, 255, 0.92); }}
      .footer-domain {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 20px; font-weight: 600; fill: rgba(255, 255, 255, 0.78); }}
      .footer-cta {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 20px; font-weight: 600; fill: #FFFFFF; }}
    </style>
    <linearGradient id="editorialScrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="58%" stop-color="#10152B" stop-opacity="0.0" />
      <stop offset="74%" stop-color="#10152B" stop-opacity="0.42" />
      <stop offset="88%" stop-color="#10152B" stop-opacity="0.68" />
      <stop offset="100%" stop-color="#10152B" stop-opacity="0.76" />
    </linearGradient>
  </defs>

  <!-- Fotografía protagonista a sangre -->
  <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  <rect width="1080" height="1350" fill="url(#editorialScrim)" />

  <!-- Firma editorial limpia en esquina superior izquierda -->
  <g transform="translate(56, 56)">
    <rect width="276" height="64" rx="32" fill="#FAF8F5" fill-opacity="0.94" />
    <image href="{logo_uri}" x="10" y="8" width="48" height="48" preserveAspectRatio="xMidYMid meet" />
    <text x="70" y="39" class="brand-pill-txt">Perritos Felices</text>
  </g>

  <!-- Bloque tipográfico editorial en el cuarto inferior -->
  <g transform="translate(64, 930)">
    <text x="0" y="0" class="cat-pill-txt">{category_label}</text>
    <text class="title">
      <tspan x="0" y="64">{title_line_1}</tspan>
      <tspan x="0" y="134" class="title-warm">{title_line_2}</tspan>
    </text>
    <text class="subtitle">
      <tspan x="0" y="196">{subtitle_line_1}</tspan>
      <tspan x="0" y="234">{subtitle_line_2}</tspan>
    </text>

    <!-- Línea divisoria sutil y pie limpio -->
    <line x1="0" y1="280" x2="952" y2="280" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5" />
    <text x="0" y="322" class="footer-domain">{footer_note}</text>
    <text x="952" y="322" text-anchor="end" class="footer-cta">Guía completa en el perfil →</text>
  </g>
</svg>"""


def generar_arte_toxicidad() -> str:
    img_uri = get_image_data_uri(WEB_ASSETS / "snacks-hidratantes-caseros-perros.jpg")
    logo_uri = get_official_logo_uri()
    return build_editorial_card_svg(
        img_uri=img_uri,
        logo_uri=logo_uri,
        category_label="Nutrición y seguridad en casa",
        title_line_1="Por qué las uvas nunca",
        title_line_2="deben ser un premio",
        subtitle_line_1="Incluso una cantidad pequeña puede dañar sus riñones.",
        subtitle_line_2="Qué frutas frescas sí puedes compartir con tranquilidad.",
    )


def generar_arte_arnes() -> str:
    img_uri = get_image_data_uri(WEB_ASSETS / "como-elegir-arnes-en-y-perros.jpg")
    logo_uri = get_official_logo_uri()
    return build_editorial_card_svg(
        img_uri=img_uri,
        logo_uri=logo_uri,
        category_label="Paseo diario y bienestar",
        title_line_1="Cómo elegir un arnés que",
        title_line_2="deje libres sus hombros",
        subtitle_line_1="El diseño en forma de Y reparte la fuerza en el pecho",
        subtitle_line_2="sin presionar su cuello ni rozar sus axilas al caminar.",
    )


def generar_arte_calma() -> str:
    img_uri = get_image_data_uri(WEB_ASSETS / "lenguaje-corporal-canino-senales.jpg")
    logo_uri = get_official_logo_uri()
    return build_editorial_card_svg(
        img_uri=img_uri,
        logo_uri=logo_uri,
        category_label="Convivencia y lenguaje canino",
        title_line_1="Lo que tu perro intenta",
        title_line_2="decirte antes de ladrar",
        subtitle_line_1="Bostezar a destiempo, lamerse la nariz o girar la cabeza",
        subtitle_line_2="son gestos pacíficos para pedirte un poco de espacio.",
    )


def generar_arte_alergias() -> str:
    img_uri = get_image_data_uri(WEB_ASSETS / "alergias-alimentarias-ambientales-perros-guia.jpg")
    logo_uri = get_official_logo_uri()
    return build_editorial_card_svg(
        img_uri=img_uri,
        logo_uri=logo_uri,
        category_label="Salud de la piel y cuidado",
        title_line_1="¿Se lame mucho las patas",
        title_line_2="después de volver del parque?",
        subtitle_line_1="Cómo distinguir si se trata de polen en el pasto",
        subtitle_line_2="o de algún ingrediente de su comida habitual.",
    )


def generar_copy_redes() -> str:
    return """# Textos y Hashtags para Redes Sociales — Perritos Felices

Redacción revisada con criterio editorial humano (`blader/humanizer` y `charlie947/social-media-skills`): tono cercano, útil para familias tutoras y libre de tecnicismos innecesarios.

---

## Publicación 1: Frutas seguras vs. uvas en casa (`arte_01_toxicidad_45.svg`)

**Texto para Instagram / Facebook:**
A veces, mientras picamos fruta en la cocina, es fácil pensar que un grano de uva no hace daño. En los perros, sin embargo, las uvas y las pasas contienen compuestos que pueden afectar seriamente sus riñones en pocas horas, sin importar su raza o su tamaño.

Si quieres compartir algo fresco y crujiente con tu perro a media tarde, hay opciones seguras que les encantan:
• Trozos pequeños de zanahoria cruda o cocida al vapor.
• Cubitos de sandía sin semillas ni cáscara.
• Rodajas de pepino pelado o arándanos frescos.

Recuerda que cualquier premio extra debe ser solo un pequeño complemento (alrededor del 10% de lo que come en el día). En nuestro sitio dejamos un buscador rápido de alimentos para consultar dudas en segundos.

**Hashtags:**
#PerritosFelices #NutricionCanina #CuidadoCanino #VidaConPerros #SaludVeterinaria #FamiliaMultiespecie

---

## Publicación 2: Cómo elegir un buen arnés en Y (`arte_02_arnes_45.svg`)

**Texto para Instagram / Facebook:**
Cuando un perro tira de la correa con un collar tradicional, toda esa presión recae directamente sobre su tráquea y su cuello. Pero cambiar a cualquier pechera tampoco resuelve el problema si tiene una tira recta que cruza sus hombros y le impide dar el paso completo.

Al buscar un arnés para el paseo diario, fíjate en tres detalles sencillos:
1. Que forme una letra "Y" vista desde el frente, dejando libre la garganta.
2. Que las tiras permitan mover los hombros sin bloqueo.
3. Que la cinta del abdomen quede al menos a dos dedos detrás de sus axilas para evitar rozaduras.

Un perro cómodo camina más relajado y disfruta mucho más el paseo. Lee la guía completa en el enlace de nuestro perfil.

**Hashtags:**
#PaseoCanino #ArnesEnY #BienestarAnimal #CrianzaRespetuosa #PerrosDeInstagram #PerritosFelices

---

## Publicación 3: Señales tempranas de incomodidad (`arte_03_calma_45.svg`)

**Texto para Instagram / Facebook:**
Mucho antes de gruñir o ladrar, los perros conversan con todo el cuerpo. Cuando una situación los abruma —como un abrazo apretado, una visita ruidosa o otro perro que se acerca demasiado rápido—, suelen hacer gestos sutiles para pedir calma:

• Bostezar aunque no tengan sueño.
• Lamerse rápidamente la punta de la nariz.
• Girar la cabeza o mirar de reojo.
• Olfatear el suelo de repente como si buscaran algo.

Reconocer estas señales a tiempo y darles espacio les enseña que no necesitan defenderse para ser escuchados.

**Hashtags:**
#LenguajeCanino #EtologiaCanina #EntenderAMiPerro #ConvivenciaCanina #CrianzaSinCastigos #PerritosFelices

---

## Publicación 4: Lamido constante de patas (`arte_04_alergias_45.svg`)

**Texto para Instagram / Facebook:**
Si notas que tu perro se lame las patas insistentemente por las noches o que el pelo entre sus dedos toma un tono rojizo por la saliva, casi nunca es por simple costumbre: suele ser picazón.

En muchos casos se debe al contacto con pólenes o pastos durante el paseo; en otros, a sensibilidad hacia alguna proteína de su dieta. Limpiar suavemente sus almohadillas con un paño húmedo al regresar a casa ayuda a retirar alérgenos del parque mientras tu veterinario de confianza evalúa el origen.

En nuestra web encontrarás una guía clara para observar sus síntomas antes de ir a consulta.

**Hashtags:**
#SaludCanina #CuidadoDePatitas #AlergiasEnPerros #VeterinariaPreventiva #TutoresResponsables #PerritosFelices
"""


def main():
    artes = {
        "arte_01_toxicidad_45.svg": generar_arte_toxicidad(),
        "arte_02_arnes_45.svg": generar_arte_arnes(),
        "arte_03_calma_45.svg": generar_arte_calma(),
        "arte_04_alergias_45.svg": generar_arte_alergias(),
    }

    print("🎨 Generando artes editoriales 4:5 (1080x1350) limpios y sin etiquetas artificiales...")
    for filename, svg_data in artes.items():
        (REDES_2026_DIR / filename).write_text(svg_data, encoding="utf-8")
        (ARTES_DIR / filename).write_text(svg_data, encoding="utf-8")
        (STUDIO_ASSETS / filename).write_text(svg_data, encoding="utf-8")
        print(f"  ✔ {filename} generado ({len(svg_data)} bytes)")

    copy_path = REDES_2026_DIR / "COPY_Y_HASHTAGS_REDES.md"
    copy_path.write_text(generar_copy_redes(), encoding="utf-8")
    print(f"  ✔ Copy editorial guardado en: {copy_path}")

    zip_path = STUDIO_ASSETS / "kit_descargables_semana_2026_10_26.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename in artes.keys():
            f_path = REDES_2026_DIR / filename
            if f_path.exists():
                zf.write(f_path, arcname=filename)
        zf.write(copy_path, arcname="COPY_Y_HASHTAGS_REDES.md")
    print(f"📦 Kit ZIP actualizado en: {zip_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
dog_characters_svg.py — Componente Paramétrico de Personajes Vectoriales SVG (PF-2027)
Implementa la especificación del Blueprint Visual:
- Personajes oficiales: Loki (el mestizo ágil y curioso) y Frodo (el mestizo pequeño y expresivo)
- 8 Estados Emocionales Etológicos (Calma, Alerta, Estrés, Miedo, Reactividad, Alegría, Olfato, Descanso)
- Filtro orgánico ink-sketch (feTurbulence + feDisplacementMap) estilo cuaderno de campo
"""

from typing import Literal

DogCharacter = Literal["loki", "frodo"]
DogEmotion = Literal[
    "calm",
    "alert",
    "stress",
    "fear",
    "reactive",
    "happy",
    "sniffing",
    "resting",
]


def get_ink_sketch_filter() -> str:
    """Filtro SVG orgánico que simula el trazo manual de tinta china etológica."""
    return """
    <filter id="ink-sketch" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.5" xChannelSelector="R" yChannelSelector="G" result="displaced" />
      <feMorphology operator="dilate" radius="0.3" in="displaced" />
    </filter>
    """


def render_dog_svg(
    character: DogCharacter = "loki",
    emotion: DogEmotion = "calm",
    width: int = 360,
    height: int = 360,
    show_filter: bool = True,
) -> str:
    """
    Renderiza el personaje canino en SVG puro paramétrico.
    """
    is_loki = character == "loki"

    # Paleta del personaje
    base_color = "#8B4513" if is_loki else "#E6C280"        # Pardo Sienna (Loki) / Dorado-Crema (Frodo)
    chest_color = "#F8FAFC" if is_loki else "#B8860B"       # Pecho blanco (Loki) / Detalle ocre (Frodo)
    accessory_color = "#FF6B35" if is_loki else "#2EC4B6"   # Arnés naranja (Loki) / Pañuelo turquesa (Frodo)
    stroke_color = "#1E293B"

    # Diccionario de Estados Emocionales Etológicos
    # ear_rotate (grados), eye_type, mouth_type, tail_rotate, pupil_dx, pupil_dy
    emotions_map = {
        "calm": {
            "ear_l_rot": 0,
            "ear_r_rot": 0,
            "eye_l": '<path d="M 140 178 Q 155 170 170 178" fill="none" stroke="#1E293B" stroke-width="5" stroke-linecap="round" />',
            "eye_r": '<path d="M 230 178 Q 245 170 260 178" fill="none" stroke="#1E293B" stroke-width="5" stroke-linecap="round" />',
            "mouth": '<path d="M 185 220 Q 200 226 215 220" fill="none" stroke="#1E293B" stroke-width="4" stroke-linecap="round" />',
            "tongue": "",
            "tail_rot": 0,
        },
        "alert": {
            "ear_l_rot": -12,
            "ear_r_rot": 12,
            "eye_l": '<circle cx="155" cy="175" r="9" fill="#1E293B" /><circle cx="158" cy="172" r="3" fill="#FFFFFF" />',
            "eye_r": '<circle cx="245" cy="175" r="9" fill="#1E293B" /><circle cx="248" cy="172" r="3" fill="#FFFFFF" />',
            "mouth": '<path d="M 188 218 L 212 218" fill="none" stroke="#1E293B" stroke-width="4" stroke-linecap="round" />',
            "tongue": "",
            "tail_rot": 22,
        },
        "stress": {  # Señal de calma / ojo de ballena
            "ear_l_rot": 18,
            "ear_r_rot": -18,
            "eye_l": '<ellipse cx="155" cy="175" rx="12" ry="11" fill="#FFFFFF" stroke="#1E293B" stroke-width="2" /><circle cx="152" cy="175" r="7" fill="#1E293B" />',
            "eye_r": '<ellipse cx="245" cy="175" rx="12" ry="11" fill="#FFFFFF" stroke="#1E293B" stroke-width="2" /><circle cx="242" cy="175" r="7" fill="#1E293B" />',
            "mouth": '<path d="M 180 224 Q 200 220 220 224" fill="none" stroke="#1E293B" stroke-width="4" stroke-linecap="round" />',
            "tongue": '<path d="M 194 208 Q 200 200 206 208 Q 200 216 194 208 Z" fill="#FF8A8A" stroke="#1E293B" stroke-width="2" />',  # Lamido de trufa sutil
            "tail_rot": -35,
        },
        "fear": {  # Miedo / orejas pegadas
            "ear_l_rot": 32,
            "ear_r_rot": -32,
            "eye_l": '<circle cx="155" cy="175" r="14" fill="#FFFFFF" stroke="#1E293B" stroke-width="2.5" /><circle cx="153" cy="175" r="6" fill="#1E293B" />',
            "eye_r": '<circle cx="245" cy="175" r="14" fill="#FFFFFF" stroke="#1E293B" stroke-width="2.5" /><circle cx="243" cy="175" r="6" fill="#1E293B" />',
            "mouth": '<path d="M 175 228 Q 200 218 225 228" fill="none" stroke="#1E293B" stroke-width="4" stroke-linecap="round" />',
            "tongue": "",
            "tail_rot": -50,
        },
        "reactive": {  # Tensión / ladrido
            "ear_l_rot": -16,
            "ear_r_rot": 16,
            "eye_l": '<circle cx="155" cy="173" r="8" fill="#1E293B" />',
            "eye_r": '<circle cx="245" cy="173" r="8" fill="#1E293B" />',
            "mouth": '<path d="M 180 214 Q 200 236 220 214 Z" fill="#E63946" stroke="#1E293B" stroke-width="4" stroke-linejoin="round" />',
            "tongue": '<path d="M 190 224 Q 200 236 210 224 Z" fill="#FF8A8A" />',
            "tail_rot": 35,
        },
        "happy": {  # Alegría / juego
            "ear_l_rot": -6,
            "ear_r_rot": 6,
            "eye_l": '<path d="M 140 178 Q 155 162 170 178" fill="none" stroke="#1E293B" stroke-width="5" stroke-linecap="round" />',
            "eye_r": '<path d="M 230 178 Q 245 162 260 178" fill="none" stroke="#1E293B" stroke-width="5" stroke-linecap="round" />',
            "mouth": '<path d="M 180 216 Q 200 240 220 216 Z" fill="#FF6B35" stroke="#1E293B" stroke-width="3.5" />',
            "tongue": '<path d="M 192 226 Q 200 248 208 226 Z" fill="#FF8A8A" stroke="#1E293B" stroke-width="2" />',
            "tail_rot": 18,
        },
        "sniffing": {  # Olfato / concentración en suelo
            "ear_l_rot": 12,
            "ear_r_rot": -12,
            "eye_l": '<path d="M 145 180 L 165 180" fill="none" stroke="#1E293B" stroke-width="5" stroke-linecap="round" />',
            "eye_r": '<path d="M 235 180 L 255 180" fill="none" stroke="#1E293B" stroke-width="5" stroke-linecap="round" />',
            "mouth": '<path d="M 188 222 Q 200 226 212 222" fill="none" stroke="#1E293B" stroke-width="4" stroke-linecap="round" />',
            "tongue": "",
            "tail_rot": 5,
        },
        "resting": {  # Sueño / descanso
            "ear_l_rot": 20,
            "ear_r_rot": -20,
            "eye_l": '<path d="M 142 180 Q 155 188 168 180" fill="none" stroke="#1E293B" stroke-width="4.5" stroke-linecap="round" />',
            "eye_r": '<path d="M 232 180 Q 245 188 258 180" fill="none" stroke="#1E293B" stroke-width="4.5" stroke-linecap="round" />',
            "mouth": '<path d="M 190 220 Q 200 223 210 220" fill="none" stroke="#1E293B" stroke-width="3" stroke-linecap="round" />',
            "tongue": "",
            "tail_rot": -30,
        },
    }

    cfg = emotions_map.get(emotion, emotions_map["calm"])
    filter_attr = 'filter="url(#ink-sketch)"' if show_filter else ""

    # Orejas específicas según anatomía de Loki (semi-erguidas) vs Frodo (caídas suaves)
    if is_loki:
        ears_svg = f"""
        <!-- Orejas Loki (Ágiles, semi-erguidas) -->
        <g id="ear-left" transform="rotate({cfg['ear_l_rot']}, 115, 140)">
          <path d="M 125 140 C 95 65, 75 80, 110 165 Z" fill="{base_color}" stroke="{stroke_color}" stroke-width="4" stroke-linejoin="round" />
          <path d="M 115 135 C 98 85, 88 95, 110 150 Z" fill="#D2996E" opacity="0.65" />
        </g>
        <g id="ear-right" transform="rotate({cfg['ear_r_rot']}, 285, 140)">
          <path d="M 275 140 C 305 65, 325 80, 290 165 Z" fill="{base_color}" stroke="{stroke_color}" stroke-width="4" stroke-linejoin="round" />
          <path d="M 285 135 C 302 85, 312 95, 290 150 Z" fill="#D2996E" opacity="0.65" />
        </g>
        """
    else:
        ears_svg = f"""
        <!-- Orejas Frodo (Grandes, caídas y redondeadas) -->
        <g id="ear-left" transform="rotate({cfg['ear_l_rot']}, 110, 130)">
          <path d="M 125 125 C 70 140, 75 240, 115 235 C 135 230, 140 170, 130 125 Z" fill="{base_color}" stroke="{stroke_color}" stroke-width="4" stroke-linejoin="round" />
          <path d="M 115 140 C 85 160, 90 220, 115 215 Z" fill="#C99F53" opacity="0.5" />
        </g>
        <g id="ear-right" transform="rotate({cfg['ear_r_rot']}, 290, 130)">
          <path d="M 275 125 C 330 140, 325 240, 285 235 C 265 230, 260 170, 270 125 Z" fill="{base_color}" stroke="{stroke_color}" stroke-width="4" stroke-linejoin="round" />
          <path d="M 285 140 C 315 160, 310 220, 285 215 Z" fill="#C99F53" opacity="0.5" />
        </g>
        """

    # Accesorio: Arnés Y (Loki) vs Pañuelo de cuello (Frodo)
    if is_loki:
        accessory_svg = f"""
        <!-- Arnés ergonómico en Y (Loki) -->
        <path d="M 140 265 L 260 265 L 250 295 L 150 295 Z" fill="{accessory_color}" stroke="{stroke_color}" stroke-width="3" stroke-linejoin="round" />
        <line x1="200" y1="265" x2="200" y2="335" stroke="{accessory_color}" stroke-width="12" stroke-linecap="round" />
        <circle cx="200" cy="275" r="5" fill="#FFFFFF" stroke="{stroke_color}" stroke-width="2" />
        """
    else:
        accessory_svg = f"""
        <!-- Pañuelo de cuello festivo (Frodo) -->
        <polygon points="150,250 250,250 200,305" fill="{accessory_color}" stroke="{stroke_color}" stroke-width="3.5" stroke-linejoin="round" />
        <path d="M 145 250 Q 200 256 255 250" stroke="{accessory_color}" stroke-width="10" stroke-linecap="round" fill="none" />
        """

    # Mancha facial asimétrica característica de Loki
    loki_patch = ""
    if is_loki:
        loki_patch = f"""
        <!-- Parche asimétrico en ojo derecho de Loki -->
        <path d="M 225 145 C 265 140, 275 190, 250 205 C 220 200, 215 160, 225 145 Z" fill="#6B3410" opacity="0.45" />
        """

    return f"""<svg width="{width}" height="{height}" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" data-character="{character}" data-emotion="{emotion}">
  <defs>
    {get_ink_sketch_filter() if show_filter else ""}
  </defs>

  <g {filter_attr}>
    <!-- Sombra en suelo -->
    <ellipse cx="200" cy="365" rx="115" ry="16" fill="#0F172A" opacity="0.12" />

    <!-- Cola expresiva -->
    <g id="tail" transform="rotate({cfg['tail_rot']}, 280, 310)">
      <path d="M 270 310 C 330 300, 355 250, 340 220 C 330 240, 305 285, 270 325 Z" fill="{base_color}" stroke="{stroke_color}" stroke-width="4" stroke-linejoin="round" />
    </g>

    <!-- Cuerpo principal -->
    <path d="M 125 240 C 120 185, 280 185, 275 240 L 290 350 L 110 350 Z" fill="{base_color}" stroke="{stroke_color}" stroke-width="4" stroke-linejoin="round" />
    
    <!-- Parche en pecho -->
    <path d="M 165 245 C 180 215, 220 215, 235 245 L 250 350 L 150 350 Z" fill="{chest_color}" stroke="{stroke_color}" stroke-width="2.5" />

    {accessory_svg}

    <!-- Cabeza -->
    <g id="head-group">
      {ears_svg}

      <!-- Cráneo -->
      <circle cx="200" cy="165" r="76" fill="{base_color}" stroke="{stroke_color}" stroke-width="4.5" />
      
      {loki_patch}

      <!-- Hocico -->
      <ellipse cx="200" cy="202" rx="38" ry="26" fill="{chest_color}" stroke="{stroke_color}" stroke-width="3" />
      
      <!-- Trufa (Nariz) -->
      <path d="M 188 188 Q 200 184 212 188 Q 200 204 188 188 Z" fill="#1E293B" stroke="#1E293B" stroke-width="1.5" />
      <ellipse cx="196" cy="189" rx="2" ry="1.2" fill="#FFFFFF" opacity="0.6" />

      <!-- Ojos dinámicos -->
      <g id="eyes">
        {cfg['eye_l']}
        {cfg['eye_r']}
      </g>

      <!-- Boca y Lengua -->
      <g id="mouth">
        {cfg['mouth']}
        {cfg['tongue']}
      </g>
    </g>
  </g>
</svg>"""

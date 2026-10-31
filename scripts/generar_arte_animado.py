#!/usr/bin/env python3
"""
MOTOR EDITORIAL MICRO-MOTION PF-2027 & PLAN SECUENCIAL DE 14 CAPÍTULOS (#01 AL #14)
1. Migra los artes y el motor Micro-Motion a formato Vertical 4:5 (1080x1350) y 9:16 (1080x1920).
2. Define las 4 Combinaciones Cromáticas Oficiales por Pilar (PF-2027):
   - Pilar A (salud_glacial): Azul Glacial #E8EDFF + AzulPF #2C4BCA + AmarilloPF #FDB54A
   - Pilar B (nutricion_menta): Menta Botánica #EAF2EB + Salvia #007A56 + Dorado #FFE082
   - Pilar C (etologia_durazno): Durazno Suave #FFF3E0 + Crema #FDFBF7 + AmarilloPF #FDB54A
   - Pilar D (urgencias_nocturno): Tinta Profunda #10152B + Coral Alerta #D9381E + AmarilloPF #FDB54A
3. Compila los 14 Artículos en estricto orden (#01 al #14) con sus 5 láminas de carrusel (70 láminas en total),
   portada animada 60fps, copys para Instagram, TikTok Photo Mode y guiones 9:16 con Lou.
"""

import base64
import html
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "03_Assets_Visuales"
WEB_ARTICLES_ASSETS = ROOT_DIR / "01_Infraestructura_Web" / "assets" / "articulos"
WEEKLY_DIR = ROOT_DIR / "02_Estrategia_Y_Contenido" / "entregas_semanales" / "semana_2026_10_26"
ARTES_DIR = WEEKLY_DIR / "artes"
STUDIO_ASSETS = ROOT_DIR / "05_Studio_Privado" / "assets"
PLAN_JSON_PATH = ROOT_DIR / "02_Estrategia_Y_Contenido" / "plan_publicacion_14_capitulos.json"

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


# ==============================================================================
# LAS 4 COMBINACIONES CROMÁTICAS OFICIALES POR PILAR (PF-2027)
# ==============================================================================
PALETTES = {
    "salud_glacial": {
        "id": "salud_glacial",
        "name": "Pilar A • Salud & Clínica (Azul Glacial)",
        "shortName": "Salud Glacial (#E8EDFF)",
        "scrimRgb": "16, 21, 43",
        "scrimHex": "#10152B",
        "coverAccent": "#FDB54A",
        "coverSub": "#E8EDFF",
        "slideBg": "#E8EDFF",
        "cardBg": "#FFFFFF",
        "inkPrimary": "#10152B",
        "inkSecondary": "#3D4463",
        "brandAccent": "#2C4BCA",
        "pillBg": "#2C4BCA",
        "pillTxt": "#FFFFFF",
        "highlightBg": "#FDB54A",
    },
    "nutricion_menta": {
        "id": "nutricion_menta",
        "name": "Pilar B • Nutrición & Naturaleza (Menta Botánica)",
        "shortName": "Nutrición Menta (#EAF2EB)",
        "scrimRgb": "14, 35, 24",
        "scrimHex": "#0E2318",
        "coverAccent": "#FFE082",
        "coverSub": "#EAF2EB",
        "slideBg": "#EAF2EB",
        "cardBg": "#FFFFFF",
        "inkPrimary": "#10152B",
        "inkSecondary": "#2D4238",
        "brandAccent": "#007A56",
        "pillBg": "#007A56",
        "pillTxt": "#FFFFFF",
        "highlightBg": "#FFE082",
    },
    "etologia_durazno": {
        "id": "etologia_durazno",
        "name": "Pilar C • Etología & Vínculo (Durazno Suave)",
        "shortName": "Etología Durazno (#FFF3E0)",
        "scrimRgb": "28, 20, 12",
        "scrimHex": "#1C140C",
        "coverAccent": "#FDB54A",
        "coverSub": "#FFF3E0",
        "slideBg": "#FFF3E0",
        "cardBg": "#FDFBF7",
        "inkPrimary": "#10152B",
        "inkSecondary": "#433628",
        "brandAccent": "#B45309",
        "pillBg": "#10152B",
        "pillTxt": "#FDB54A",
        "highlightBg": "#FDB54A",
    },
    "urgencias_nocturno": {
        "id": "urgencias_nocturno",
        "name": "Pilar D • Urgencias, Biomecánica & Mitos (Alto Contraste)",
        "shortName": "Urgencias Contraste (#10152B)",
        "scrimRgb": "13, 18, 38",
        "scrimHex": "#0D1226",
        "coverAccent": "#FDB54A",
        "coverSub": "#FDFBF7",
        "slideBg": "#FDFBF7",
        "cardBg": "#FFFFFF",
        "inkPrimary": "#10152B",
        "inkSecondary": "#3D4463",
        "brandAccent": "#D9381E",
        "pillBg": "#D9381E",
        "pillTxt": "#FFFFFF",
        "highlightBg": "#FDB54A",
    },
}


# ==============================================================================
# LOS 14 CAPÍTULOS EN ORDEN ESTRICTO (#01 AL #14) DESDE EL PRIMER ARTÍCULO
# ==============================================================================
CHAPTERS_14 = [
    {
        "order": 1,
        "chapterNum": "01",
        "id": "art-01",
        "slug": "guia-alimentacion-natural-perros.html",
        "photoFile": "guia-alimentacion-natural-perros.jpg",
        "title": "Guía completa de alimentación natural y balanceada para tu perro",
        "category": "Nutrición",
        "paletteId": "nutricion_menta",
        "focusX": 0.50,
        "focusY": 0.38,
        "cover": {
            "badge": "CAPÍTULO 01 // NUTRICIÓN CLÍNICA",
            "kicker": "CONSENSO WSAVA & FEDIAF • BALANCE Ca:P",
            "kickerItalic": False,
            "title1": "Alimentación natural:",
            "title2": "la regla del 10% seguro",
            "sub1": "Cómo sumar alimentos frescos e hidratantes sin",
            "sub2": "desbalancear el calcio y fósforo de su plato diario.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Nutrición Veterinaria EBVM",
            "underlineW": 595,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // EVIDENCIA CIENTÍFICA WSAVA & UC DAVIS",
                "headline": "Cocinar en casa sin suplementar calcio desmineraliza sus huesos",
                "body": "La carne y el pollo son ricos en fósforo pero casi nulos en calcio. Una dieta casera completa exige formulación veterinaria con relación Ca:P de 1.2:1 a 1.4:1.",
                "statValue": "10% MÁX",
                "statLabel": "Tope seguro de snacks o toppers frescos sobre sus calorías diarias (MER)",
                "citation": "Fuente: WSAVA Global Nutrition Guidelines & FEDIAF (2024)",
            },
            {
                "slideNum": 3,
                "tag": "02 // SEMÁFORO NUTRICIONAL EN CASA",
                "headline": "Toppers seguros vs. Errores frecuentes en el plato",
                "doTitle": "✔ SEGURO (DENTRO DEL 10% MER)",
                "doItems": [
                    "Arándanos, manzana sin semillas y sandía fresca",
                    "Zanahoria, calabaza cocida y ejotes al vapor",
                    "Pechuga o pescado cocido sin sal ni condimentos",
                ],
                "dontTitle": "✘ PELIGROSO O DESBALANCEADO",
                "dontItems": [
                    "Recetas caseras al ojo (60/25/15) sin calcio medido",
                    "Más de 5% de hígado diario (riesgo de hipervitaminosis A)",
                    "Uvas, pasas, cebolla, ajo, xilitol o huesos cocidos",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // PROTOCOLO DE TRANSICIÓN EN 3 PASOS",
                "headline": "Cómo mejorar su plato hoy sin causarle diarrea",
                "steps": [
                    {"num": "01", "title": "Calcula su 10% con precisión", "desc": "Usa nuestra Calculadora Metabólica gratuita en perritosfelices.com según su peso y condición."},
                    {"num": "02", "title": "Transición gradual de 7 días", "desc": "Introduce un solo alimento fresco nuevo a la vez (25% -> 50% -> 75% -> 100%) vigilando sus heces."},
                    {"num": "03", "title": "Cocción suave e inocua", "desc": "Cocina al vapor o plancha sin cebolla, ajo ni aceites recalentados para evitar pancreatitis."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTA GUÍA & DIRECTORIO ÉTICO",
                "headline": "La nutrición fresca suma vida cuando se apoya en la ciencia",
                "goldenRule": "Regla de Oro: Usa el 10% en toppers frescos hoy mismo; si deseas pasar al 100% casero, formúlalo con un nutricionista veterinario.",
                "directoryCta": "Encuentra Nutricionistas Veterinarios y Tiendas Naturales en perritosfelices.com",
            },
        ],
        "igCaption": """🥣 ¿Le pones pollito, verduras o fruta al plato de tu perro? Hacerlo es maravilloso, pero hay una regla clínica que todo tutor debe conocer: la Regla del 10% de la WSAVA.

Desliza este carrusel (Capítulo #01 de nuestra serie maestra) para descubrir:
1️⃣ Por qué las recetas caseras "al ojo" sin suplemento de calcio desmineralizan los huesos (relación Ca:P 1.2:1).
2️⃣ Qué frutas y verduras frescas puedes darle hoy mismo con total seguridad.
3️⃣ Cómo hacer la transición en 7 días para proteger su microbiota.

📌 Guarda este post para tu próxima compra del súper y usa nuestra Calculadora Metabólica en el link de la bio (perritosfelices.com).

#NutricionCanina #PerritosFelices #AlimentacionNaturalPerros #WSAVA #CrianzaRespetuosa #SaludCanina""",
        "tiktokPhotoCopy": """🥣 Capítulo 01: Cómo sumar comida real al plato de tu perro sin desbalancear su calcio (Regla del 10% WSAVA). Desliza las 5 láminas 👉 y guarda el semáforo de alimentos seguros. #NutricionCanina #PerritosFelices #PerrosTikTok #ComidaParaPerros""",
        "reelScript": {
            "hook": "0-3s • Lou: 'Si cocinas para tu perro en casa sin medir el calcio, podrías estar debilitando sus huesos sin darte cuenta.'",
            "problem": "3-8s • Lou muestra un plato con pollo y arroz: 'La carne tiene mucho fósforo pero casi nada de calcio. Sin fórmula veterinaria, el cuerpo saca calcio de sus propios huesos.'",
            "solution": "8-18s • Lou añade arándanos y calabaza como topper: 'Usa la regla del 10% de la WSAVA en snacks frescos y calcula los gramos exactos en perritosfelices.com.'",
        },
    },
    {
        "order": 2,
        "chapterNum": "02",
        "id": "art-02",
        "slug": "lenguaje-corporal-canino-senales.html",
        "photoFile": "lenguaje-corporal-canino-senales.jpg",
        "title": "Cómo entender el lenguaje corporal de tu perro: 15 señales clave",
        "category": "Comportamiento",
        "paletteId": "etologia_durazno",
        "focusX": 0.55,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 02 // ETOLOGÍA CANINA",
            "kicker": "TURID RUGAAS • COMUNICACIÓN Y SEÑALES DE CALMA",
            "kickerItalic": False,
            "title1": "¿Tu perro bosteza o",
            "title2": "se lame la trufa al abrazarlo?",
            "sub1": "No tiene sueño ni hambre: te está pidiendo espacio.",
            "sub2": "Aprende las 15 señales que previenen mordidas y estrés.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Etología Clínica Fear-Free",
            "underlineW": 740,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // LA ESCALERA DE LA COMUNICACIÓN CANINA",
                "headline": "Ningún perro muerde 'de la nada': antes susurró con su cuerpo",
                "body": "Los perros son pacifistas por naturaleza. Antes de gruñir, emiten decenas de señales de apaciguamiento sutiles para desescalar la tensión social.",
                "statValue": "+30 SEÑALES",
                "statLabel": "De calma documentadas en etología para evitar conflictos sin agresividad",
                "citation": "Fuente: Turid Rugaas (On Talking Terms with Dogs) & Dra. Kendal Shepherd",
            },
            {
                "slideNum": 3,
                "tag": "02 // CÓMO LEER SU CUERPO EN SEGUNDOS",
                "headline": "Señales de calma reales vs. Malentendidos humanos",
                "doTitle": "✔ LO QUE REALMENTE TE DICE",
                "doItems": [
                    "Bostezo o lamido rápido de trufa = 'Me siento incómodo'",
                    "Ojo de ballena (esclerótica blanca) = 'Por favor aléjate'",
                    "Sacudirse en seco como mojado = 'Liberando adrenalina'",
                ],
                "dontTitle": "✘ ERRORES QUE DEBEMOS EVITAR",
                "dontItems": [
                    "Creer que toda cola moviéndose es felicidad (puede ser alerta)",
                    "Regañar el gruñido (apagas su alarma de aviso y creas mordidas)",
                    "Forzar abrazos en el cuello cuando gira la cabeza",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // PROTOCOLO DE ESCUCHA EMPÁTICA EN 3 PASOS",
                "headline": "Qué hacer cuando tu perro emite una señal de calma",
                "steps": [
                    {"num": "01", "title": "Detén la presión de inmediato", "desc": "Si estabas abrazándolo o acercando a un desconocido, dale 2 metros de espacio al instante."},
                    {"num": "02", "title": "Gira tu cuerpo ligeramente de lado", "desc": "Evita mirarlo fijo de frente; curvar tu postura le confirma que entendiste su mensaje."},
                    {"num": "03", "title": "Aplica el test de los 3 segundos", "desc": "Acaricia el pecho 3 segundos y retira la mano: si se acerca pide más; si se aparta, respeta su pausa."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTE DECODIFICADOR ETOLÓGICO",
                "headline": "Escuchar su idioma es el mayor acto de amor diario",
                "goldenRule": "Regla de Oro: Nunca castigues un gruñido ni ignores un bostezo tenso; un perro escuchado es un perro seguro.",
                "directoryCta": "Explora el Decodificador Interactivo y Etólogos Fear-Free en perritosfelices.com",
            },
        ],
        "igCaption": """🐕 ¿Sabías que cuando abrazas a tu perro y él bosteza o se lame la nariz rápido no tiene sueño? En etología se llaman Señales de Calma y significan: 'Te quiero, pero esto me incomoda un poco'.

En este Capítulo #02 de nuestro plan editorial aprenderás:
1️⃣ Por qué mover la cola no siempre es felicidad (cola alta y rígida = tensión).
2️⃣ Qué es el 'ojo de ballena' y la sacudida de descarga de cortisol.
3️⃣ La regla de consentimiento de los 3 segundos para acariciar sin invadir.

📌 Guarda esta guía y compártela en tus historias para que más familias hablen el idioma canino.

#LenguajeCanino #EtologiaCanina #SenalesDeCalma #PerritosFelices #FearFree #CrianzaRespetuosa""",
        "tiktokPhotoCopy": """🐕 Capítulo 02: 15 señales del lenguaje corporal de tu perro que todo tutor debe saber leer. Desliza 👉 para descubrir qué significa el bostezo, el lamido de trufa y el 'ojo de ballena'. #EtologiaCanina #LenguajeCanino #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou: '¿Tu perro bosteza o se lame la nariz justo cuando lo abrazas? No tiene sueño, te está hablando.'",
            "problem": "3-8s • Toma de perro girando la cabeza suavemente: 'Turid Rugaas documentó más de 30 señales de calma que usan para pedirnos espacio antes de estresarse.'",
            "solution": "8-18s • Lou aplica el test de 3 segundos en el pecho: 'Acaricia 3 segundos y suelta. Si vuelve, quiere más. Usa nuestro decodificador en perritosfelices.com.'",
        },
    },
    {
        "order": 3,
        "chapterNum": "03",
        "id": "art-03",
        "slug": "calendario-vacunacion-desparasitacion.html",
        "photoFile": "calendario-vacunacion-desparasitacion.jpg",
        "title": "Calendario de vacunación y desparasitación: de cachorro a senior",
        "category": "Salud y Prevención",
        "paletteId": "salud_glacial",
        "focusX": 0.50,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 03 // MEDICINA PREVENTIVA",
            "kicker": "DIRECTRICES WSAVA 2024 & AAHA • INMUNOLOGÍA",
            "kickerItalic": False,
            "title1": "Vacunas y desparasitación:",
            "title2": "el calendario de cachorro a senior",
            "sub1": "Por qué el refuerzo de la semana 16 es innegociable",
            "sub2": "y cómo protegerlo sin sobre-vacunar cada año.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Inmunología Clínica WSAVA",
            "underlineW": 710,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // ANTICUERPOS MATERNOS Y VENTANA DE RIESGO",
                "headline": "Por qué las vacunas de cachorro deben terminar a las 16 semanas o más",
                "body": "Los anticuerpos de la leche materna (MDA) pueden neutralizar las primeras dosis. La dosis de la semana 16+ y el refuerzo a los 6 meses aseguran inmunidad real.",
                "statValue": "SEM 16+",
                "statLabel": "Edad mínima de la última dosis de vacunas esenciales (Parvo, Moquillo, Adenovirus)",
                "citation": "Fuente: WSAVA Vaccination Guidelines Group (2024) & AAHA",
            },
            {
                "slideNum": 3,
                "tag": "02 // ESENCIALES VS. COMPLEMENTARIAS",
                "headline": "Medicina preventiva inteligente según su estilo de vida",
                "doTitle": "✔ VACUNAS ESENCIALES (CORE)",
                "doItems": [
                    "Parvovirus Canino (CPV-2), Moquillo (CDV) y Adenovirus",
                    "Rabia (obligatoria por salud pública y ley sanitaria)",
                    "Leptospirosis en regiones húmedas o con fauna urbana",
                ],
                "dontTitle": "✘ MITOS QUE PONEN EN RIESGO SU SALUD",
                "dontItems": [
                    "Creer que un perro senior ya no necesita chequeo ni vacunas",
                    "Desparasitar con una pastilla al azar sin examen coproparasitoscópico",
                    "Encerrar al cachorro 4 meses sin socialización segura en brazos",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // CRONOGRAMA CLÍNICO EN 3 ETAPAS",
                "headline": "Tu hoja de ruta preventiva durante toda su vida",
                "steps": [
                    {"num": "01", "title": "Cachorro (6–16+ semanas)", "desc": "Dosis cada 3–4 semanas finalizando en semana 16 o posterior, más refuerzo clave a los 6 meses."},
                    {"num": "02", "title": "Adulto (Refuerzos inteligentes)", "desc": "Cada 1 a 3 años en esenciales según vacuna y serología; anual en Leptospira y Bordetella."},
                    {"num": "03", "title": "Escudo Antiparasitario", "desc": "Control externo mensual (pulgas/garrapatas) y examen de heces cada 3 a 6 meses (guías CAPC)."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA EL CALENDARIO OFICIAL",
                "headline": "Prevenir sin miedo: visitas veterinarias con premios y calma",
                "goldenRule": "Regla de Oro: Lleva su manta y snacks de alto valor a la consulta para que asocie la clínica con seguridad.",
                "directoryCta": "Localiza Clínicas Veterinarias Fear-Free en tu ciudad en perritosfelices.com",
            },
        ],
        "igCaption": """🩺 ¿Sabes por qué un cachorro puede enfermar de Parvovirus aunque ya tenga 2 vacunas puestas? La respuesta está en los anticuerpos maternos y la regla de la Semana 16 de la WSAVA.

En el Capítulo #03 de nuestra serie editorial te explicamos de forma clara:
1️⃣ El calendario actualizado WSAVA 2024 de cachorro a perro senior.
2️⃣ Qué vacunas son esenciales para todos y cuáles dependen de su estilo de vida.
3️⃣ Cómo combinar vacunas y desparasitación interna/externa sin estrés.

📌 Guarda este calendario en tu colección de Salud Canina para tenerlo listo antes de su próximo chequeo anual.

#VacunacionCanina #SaludVeterinaria #Cachorros #WSAVA #PerritosFelices #MedicinaPreventiva""",
        "tiktokPhotoCopy": """🩺 Capítulo 03: Calendario oficial de vacunación y desparasitación canina (WSAVA 2024) de cachorro a senior. Desliza 👉 y guárdalo para su próxima consulta. #Veterinaria #SaludCanina #Cachorros #PerritosFelices""",
        "reelScript": {
            "hook": "0-3s • Lou: 'El error número uno con las vacunas de cachorro es terminar antes de las 16 semanas.'",
            "problem": "3-8s • Lou explica con gráfico simple: 'Los anticuerpos de su mamá bloquean las primeras dosis. Si paras a las 12 semanas, puede quedar desprotegido ante el Parvovirus.'",
            "solution": "8-18s • Lou acaricia a Frodo con premio: 'Asegura la dosis de la semana 16 y descarga el calendario completo WSAVA en perritosfelices.com.'",
        },
    },
    {
        "order": 4,
        "chapterNum": "04",
        "id": "art-04",
        "slug": "ansiedad-por-separacion-como-ayudarlo.html",
        "photoFile": "ansiedad-por-separacion-como-ayudarlo.jpg",
        "title": "Ansiedad por separación en perros: causas, señales y ejercicios prácticos",
        "category": "Comportamiento",
        "paletteId": "etologia_durazno",
        "focusX": 0.50,
        "focusY": 0.35,
        "cover": {
            "badge": "CAPÍTULO 04 // SALUD EMOCIONAL",
            "kicker": "DRA. KAREN OVERALL & MALENA DEMARTINI • SIN CASTIGOS",
            "kickerItalic": False,
            "title1": "¿Llora o rompe cosas",
            "title2": "cuando te vas de casa?",
            "sub1": "No es venganza ni rebeldía: es un ataque de pánico",
            "sub2": "involuntario que se supera con seguridad progresiva.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Modificación Conductual Amable",
            "underlineW": 565,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // NEUROBIOLOGÍA DEL PÁNICO AL QUEDARSE SOLO",
                "headline": "Tu perro no destruye la puerta por rencor: intenta escapar del miedo",
                "body": "La ansiedad por separación ocurre en los primeros 15–30 minutos tras tu salida. Regañarlo al volver horas después solo le enseña a temer tu regreso.",
                "statValue": "0% RENCOR",
                "statLabel": "La destrucción de marcos de puerta, jadeo y aullido son síntomas clínicos de pánico",
                "citation": "Fuente: Dra. Karen Overall (Clinical Behavioral Medicine) & Malena DeMartini",
            },
            {
                "slideNum": 3,
                "tag": "02 // ANSIEDAD REAL VS. FALTA DE ENRIQUECIMIENTO",
                "headline": "Cómo distinguir el pánico clínico del aburrimiento cotidiano",
                "doTitle": "✔ SEÑALES DE ANSIEDAD REAL",
                "doItems": [
                    "Hiperapego: te sigue de cuarto en cuarto sin poder dormir",
                    "Tiembla desde que tomas las llaves o te pones los zapatos",
                    "No toca ni sus premios favoritos mientras está solo",
                ],
                "dontTitle": "✘ LO QUE EMPEORA EL CUADRO",
                "dontItems": [
                    "Encerrarlo en jaula metálica (causa fracturas dentales y uñas)",
                    "Castigar o señalar lo que rompió cuando regresas a casa",
                    "Forzar salidas de 4 horas sin entrenar su umbral de calma",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // PROTOCOLO PROGRESIVO EN 3 PASOS",
                "headline": "Cómo construir ausencias seguras bajo el umbral del miedo",
                "steps": [
                    {"num": "01", "title": "Desactiva las pistas de salida", "desc": "Toma las llaves o ponte la chamarra y vuelve a sentarte en el sofá 3 veces al día sin salir."},
                    {"num": "02", "title": "Graba los primeros 20 minutos", "desc": "Deja tu celular o cámara grabando para conocer su umbral exacto antes de que aparezca el jadeo."},
                    {"num": "03", "title": "Micro-salidas sub-umbral", "desc": "Entrena salidas de segundos a minutos regresando SIEMPRE antes de que se angustie."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTE PROTOCOLO CONDUCTUAL",
                "headline": "La independencia emocional nace de sentirse seguro, nunca del encierro",
                "goldenRule": "Regla de Oro: Si el pánico no le permite ni comer cuando sales, apóyate en un etólogo clínico certificado.",
                "directoryCta": "Encuentra Etólogos y Guarderías Sin Jaulas en perritosfelices.com",
            },
        ],
        "igCaption": """💙 Si al volver a casa encuentras la puerta arañada o los vecinos te dicen que tu perro aulló toda la mañana, respira profundo: no lo hace por 'venganza' ni para retarte. Está sufriendo un ataque de pánico real.

En este Capítulo #04 analizamos con evidencia clínica (Dra. Karen Overall & Malena DeMartini):
1️⃣ Cómo diferenciar la ansiedad por separación real del simple aburrimiento.
2️⃣ Por qué encerrarlo en una jaula o regañarlo al volver agrava el trauma.
3️⃣ Cómo desactivar las 'pistas de salida' (llaves, zapatos) y entrenar ausencias bajo su umbral.

📌 Guarda esta guía si estás entrenando a tu compañero a quedarse tranquilo en casa.

#AnsiedadPorSeparacion #EtologiaCanina #PerritosFelices #CrianzaRespetuosa #SinJaulas #BienestarCanino""",
        "tiktokPhotoCopy": """💙 Capítulo 04: ¿Tu perro llora o rompe cosas cuando sales de casa? No es venganza, es pánico. Desliza 👉 para ver los 3 ejercicios prácticos sin jaulas ni regaños. #AnsiedadPorSeparacion #EtologiaCanina #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou: 'Tu perro no rompe tus zapatos por venganza cuando lo dejas solo. Lo hace porque tiene pánico y tu olor lo calma.'",
            "problem": "3-8s • Lou toma las llaves y Loki la mira alerta: 'Su ansiedad empieza antes de que abras la puerta, cuando ve tus llaves o tus tenis.'",
            "solution": "8-18s • Lou toma las llaves y se sienta a leer tranquila: 'Practica desactivar pistas de salida y lee el protocolo paso a paso en perritosfelices.com.'",
        },
    },
    {
        "order": 5,
        "chapterNum": "05",
        "id": "art-05",
        "slug": "paseos-olfativos-enriquecimiento-ambiental.html",
        "photoFile": "paseos-olfativos-enriquecimiento-ambiental.jpg",
        "title": "Paseos olfativos y enriquecimiento ambiental: el secreto de un perro equilibrado",
        "category": "Bienestar y Juegos",
        "paletteId": "nutricion_menta",
        "focusX": 0.50,
        "focusY": 0.38,
        "cover": {
            "badge": "CAPÍTULO 05 // PASEOS OLFATIVOS",
            "kicker": "DRA. ALEXANDRA HOROWITZ • NEUROBIOLOGÍA DEL OLFATO",
            "kickerItalic": False,
            "title1": "20 minutos olfateando",
            "title2": "relajan más que 1h corriendo",
            "sub1": "El trote continuo dispara adrenalina; olfatear a su",
            "sub2": "propio ritmo baja las pulsaciones y el cortisol.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Enriquecimiento Ambiental",
            "underlineW": 655,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // EL SUPERPODER DE LA TRUFA CANINA",
                "headline": "300 millones de receptores olfativos: su forma de leer el mundo",
                "body": "El bulbo olfatorio del perro es 40 veces mayor en proporción que el humano. Impedirle oler en el paseo es como caminar con los ojos vendados.",
                "statValue": "-42% ESTRÉS",
                "statLabel": "Reducción del ritmo cardíaco y conductas de frustración mediante olfateo libre",
                "citation": "Fuente: Dra. Alexandra Horowitz (Barnard College) & Christina B. Duranton (2019)",
            },
            {
                "slideNum": 3,
                "tag": "02 // MARCHA MILITAR VS. PASEO DE DESCOMPRESIÓN",
                "headline": "Cansar el cuerpo no es lo mismo que relajar la mente",
                "doTitle": "✔ PASEO OLFATIVO DE CALIDAD",
                "doItems": [
                    "Correa larga (3 a 5 m) siempre destensada en sonrisa",
                    "Permitirle elegir qué árbol o pasto explorar sin prisa",
                    "Arnés ergonómico en 'Y' que libera hombros y tráquea",
                ],
                "dontTitle": "✘ PASEO HIPERACTIVO O RESTRICTIVO",
                "dontItems": [
                    "Caminata militar pegado a tu rodilla sin dejarlo oler",
                    "Lanzar la pelota 40 veces seguidas (genera adicción y cortisol)",
                    "Dar tirones de correa cada vez que baja la cabeza",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // ENRIQUECIMIENTO EN CASA EN 3 JUEGOS",
                "headline": "Días de lluvia: cómo activar su nariz dentro de casa",
                "steps": [
                    {"num": "01", "title": "La toalla enrollada (Snuffle casero)", "desc": "Esconde premios secos en los pliegues de una toalla vieja enrollada para que busque con la trufa."},
                    {"num": "02", "title": "Sembrado de premios en jardín o sala", "desc": "Esparce parte de su ración diaria para que rastree pieza por pieza a baja velocidad."},
                    {"num": "03", "title": "Masticación y lamido (LickiMat)", "desc": "15 minutos de lamido de calabaza o yogur liberan serotonina y endorfinas antes de dormir."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTA RUTINA DE BIENESTAR",
                "headline": "El paseo pertenece a tu perro: regálale tiempo para leer su entorno",
                "goldenRule": "Regla de Oro: Mide la calidad del paseo por cuántos olores exploró, no por cuántos kilómetros caminaron.",
                "directoryCta": "Descubre Parques, Cafés y Paseadores Éticos en perritosfelices.com",
            },
        ],
        "igCaption": """🌿 ¿Sales a caminar rápido con tu perro durante una hora y al volver a casa sigue igual de inquieto? El secreto está en la diferencia entre cansancio físico (adrenalina) y calma mental (olfato).

En nuestro Capítulo #05 exploramos la ciencia del Paseo Olfativo:
1️⃣ Por qué 20 minutos usando sus 300 millones de receptores olfativos bajan su ritmo cardíaco.
2️⃣ Por qué lanzar la pelota sin parar puede volverlo adicto al cortisol.
3️⃣ 3 juegos caseros de olfato y lamido que puedes armar hoy en 2 minutos.

📌 Guarda este carrusel y pruébalo en su paseo de esta tarde: déjalo elegir el ritmo.

#PaseoOlfativo #EnriquecimientoAmbiental #PerritosFelices #BienestarCanino #Etologia #CrianzaRespetuosa""",
        "tiktokPhotoCopy": """🌿 Capítulo 05: Por qué 20 minutos de paseo olfativo relajan más a tu perro que 1 hora corriendo. Desliza 👉 y aprende 3 juegos de olfato caseros. #PaseoOlfativo #EnriquecimientoAmbiental #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou en el parque con correa larga: 'Deja de medir el paseo de tu perro en kilómetros y empieza a medirlo en olores.'",
            "problem": "3-8s • Toma de Frodo olfateando el pasto con calma: 'Correr sin parar sube su adrenalina; usar sus 300 millones de receptores olfativos baja sus pulsaciones.'",
            "solution": "8-18s • Lou muestra correa en curva suave: 'Dale 20 minutos de olfato libre con arnés en Y. Más juegos mentales en perritosfelices.com.'",
        },
    },
    {
        "order": 6,
        "chapterNum": "06",
        "id": "art-06",
        "slug": "primeros-auxilios-caninos-botiquin.html",
        "photoFile": "primeros-auxilios-caninos-botiquin.jpg",
        "title": "Primeros auxilios para perros: qué tener en casa y cómo actuar en emergencias",
        "category": "Salud y Prevención",
        "paletteId": "urgencias_nocturno",
        "focusX": 0.50,
        "focusY": 0.35,
        "cover": {
            "badge": "CAPÍTULO 06 // URGENCIAS & BOTIQUÍN",
            "kicker": "CONSENSO RECOVER & ASPCA APCC • EMERGENCIAS ECC",
            "kickerItalic": False,
            "title1": "Primeros auxilios:",
            "title2": "3 errores que empeoran todo",
            "sub1": "Por qué jamás debes usar hielo en un golpe de calor",
            "sub2": "ni inducir el vómito sin orden veterinaria.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Protocolo Urgencias RECOVER",
            "underlineW": 650,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // SIGNOS VITALES NORMALES EN REPOSO",
                "headline": "Conocer sus constantes sanas te permite detectar una urgencia a tiempo",
                "body": "En una emergencia cada minuto cuenta. Revisa hoy mismo sus encías en reposo para conocer su color rosa salmón normal y su llenado capilar (< 2 segundos).",
                "statValue": "38°–39.2°C",
                "statLabel": "Temperatura normal canina (FC: 60–140 lpm • FR: 15–30 rpm en reposo)",
                "citation": "Fuente: RECOVER Initiative Guidelines (2024) & ASPCA Poison Control",
            },
            {
                "slideNum": 3,
                "tag": "02 // PROTOCOLO DE URGENCIAS: QUÉ HACER Y QUÉ PROHIBIR",
                "headline": "Maniobras que salvan vidas vs. Remedios caseros peligrosos",
                "doTitle": "✔ ACTUACIÓN CLÍNICA CORRECTA",
                "doItems": [
                    "Golpe de calor (>40.5°C): agua fresca (no helada) en abdomen e ingles",
                    "Sangrado en almohadilla: presión directa con gasa estéril 3–5 min",
                    "Intoxicación: tomar foto del envase/planta y llamar a urgencias",
                ],
                "dontTitle": "✘ CONTRAINDICACIONES MÉDICAS GRAVES",
                "dontItems": [
                    "Cubrir con toallas mojadas o usar hielo (causa vasoconstricción)",
                    "Dar leche, aceite o inducir vómito ante cáusticos o punzantes",
                    "Automedicar con ibuprofeno, paracetamol o naproxeno (letales)",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // CHECKLIST DE TU BOTIQUÍN CANINO EN CASA",
                "headline": "Los 3 pilares que deben estar listos en tu mochila hoy",
                "steps": [
                    {"num": "01", "title": "Curación y limpieza estéril", "desc": "Gasas estériles no adherentes, suero fisiológico 0.9%, clorhexidina acuosa y venda cohesiva."},
                    {"num": "02", "title": "Diagnóstico rápido", "desc": "Termómetro digital de punta flexible (uso exclusivo), pinza garrapatera y linterna."},
                    {"num": "03", "title": "Contacto de Urgencias 24/7", "desc": "Teléfono y ruta en Maps de la clínica veterinaria 24 horas más cercana a tu hogar."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTE MANUAL DE EMERGENCIA",
                "headline": "Estar preparado mantiene tu mente serena cuando tu perro más te necesita",
                "goldenRule": "Regla de Oro: Consulta el Semáforo Toxicológico en nuestra web antes de cualquier maniobra en casa.",
                "directoryCta": "Localiza Hospitales Veterinarios 24/7 en perritosfelices.com",
            },
        ],
        "igCaption": """⛑️ En una emergencia veterinaria, las buenas intenciones sin información clínica pueden ser peligrosas. ¿Sabías que poner hielo o tapar con una toalla mojada a un perro con golpe de calor atrapa el calor interno y empeora el daño orgánico?

En el Capítulo #06 de nuestro plan maestro (validado con guías RECOVER y ASPCA APCC) tienes:
1️⃣ Los signos vitales normales de un perro sano en reposo (Temperatura, pulso y encías).
2️⃣ Qué hacer y qué NUNCA hacer ante golpe de calor, cortes en patitas e intoxicaciones.
3️⃣ El checklist exacto para armar el botiquín canino de tu casa hoy mismo.

📌 GUARDA este post en tu celular: es la guía que querrás tener a un toque si ocurre un imprevisto.

#PrimerosAuxiliosCaninos #UrgenciasVeterinarias #BotiquinCanino #PerritosFelices #SaludCanina #RECOVER""",
        "tiktokPhotoCopy": """⛑️ Capítulo 06: Primeros auxilios para perros y qué tener en tu botiquín en casa. Desliza 👉 para ver los signos vitales normales y los 3 errores que nunca debes cometer. #PrimerosAuxilios #Veterinaria #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou con botiquín en mano: 'Tres errores de primeros auxilios en perros que casi todo el mundo comete por desconocimiento.'",
            "problem": "3-8s • Lou enumera: 'Uno: poner hielo en un golpe de calor cierra los vasos sanguíneos. Dos: provocar el vómito con sal o aceite.'",
            "solution": "8-18s • Lou muestra gasas y suero: 'Usa agua fresca en ingles y abdomen, y revisa el Semáforo Toxicológico en perritosfelices.com.'",
        },
    },
    {
        "order": 7,
        "chapterNum": "07",
        "id": "art-07",
        "slug": "cuidado-dental-perros-guia-practica.html",
        "photoFile": "cuidado-dental-perros-guia-practica.jpg",
        "title": "Higiene dental canina: cómo prevenir el sarro y cuidar su sonrisa en casa",
        "category": "Higiene y Cuidado",
        "paletteId": "salud_glacial",
        "focusX": 0.50,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 07 // ODONTOLOGÍA CANINA",
            "kicker": "CONSENSO AVDC & VOHC • SALUD CARDIORRENAL",
            "kickerItalic": False,
            "title1": "El mal aliento en perros",
            "title2": "no es normal: es infección",
            "sub1": "El 80% de los perros mayores de 3 años sufre enfermedad",
            "sub2": "periodontal que afecta corazón, hígado y riñones.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Odontología Veterinaria AVDC",
            "underlineW": 620,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // DE LA BOCA AL CORAZÓN Y LOS RIÑONES",
                "headline": "La placa bacteriana se mineraliza en sarro duro en solo 48 a 72 horas",
                "body": "Las bacterias de las encías inflamadas (gingivitis) pasan al torrente sanguíneo en cada mordida, pudiendo alojarse en las válvulas del corazón y los riñones.",
                "statValue": "80% EN >3 AÑOS",
                "statLabel": "Presenta algún grado de enfermedad periodontal prevenible con higiene en casa",
                "citation": "Fuente: American Veterinary Dental College (AVDC) & VOHC",
            },
            {
                "slideNum": 3,
                "tag": "02 // CUIDADO DENTAL SEGURO VS. PRÁCTICAS RIESGOSAS",
                "headline": "Cómo proteger sus dientes sin fracturas ni intoxicaciones",
                "doTitle": "✔ ODONTOLOGÍA PREVENTIVA SEGURA",
                "doItems": [
                    "Pasta enzimática exclusiva para perros (sabor pollo/maní)",
                    "Dedal de silicona suave o cepillo en ángulo de 45 grados",
                    "Masticables flexibles certificados con sello VOHC",
                ],
                "dontTitle": "✘ RIESGOS ODONTOLÓGICOS SEVEROS",
                "dontItems": [
                    "Usar pasta dental humana (contiene flúor y xilitol tóxicos)",
                    "Astas de ciervo, pezuñas duras o huesos cocidos (fracturan muelas)",
                    "Raspado dental estético 'sin anestesia' (deja sarro bajo la encía)",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // PLAN FEAR-FREE DE 4 DÍAS PARA EL CEPILLADO",
                "headline": "Cómo lograr que acepte el cepillado sin forcejeos",
                "steps": [
                    {"num": "01", "title": "Día 1–2: Sabor positivo", "desc": "Deja que lama un poco de pasta enzimática canina directamente de tu dedo como un premio."},
                    {"num": "02", "title": "Día 3–4: Gasa o dedal en colmillos", "desc": "Desliza suavemente por la cara externa de los colmillos durante 5 segundos y premia."},
                    {"num": "03", "title": "Rutina: 30 segundos por lado", "desc": "Cepilla solo la cara externa (la lengua limpia la interna) 3 a 4 veces por semana."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTA RUTINA DENTAL",
                "headline": "30 segundos de cepillado amable le regalan años de vida sana",
                "goldenRule": "Regla de Oro: Si no puedes marcar un mordedor con la uña de tu pulgar, es demasiado duro para sus muelas (Regla AVDC).",
                "directoryCta": "Encuentra Odontología Veterinaria Certificada en perritosfelices.com",
            },
        ],
        "igCaption": """🪥 'Es normal que a los perros les huela feo la boca'. ¡Falso! El mal aliento (halitosis) es la primera señal de proliferación bacteriana y enfermedad periodontal, presente en el 80% de los perros mayores de 3 años.

En este Capítulo #07 (con aval de las guías AVDC y VOHC) descubrirás:
1️⃣ Por qué la salud de sus encías protege directamente su corazón y sus riñones.
2️⃣ Por qué las limpiezas 'sin anestesia' son un peligro cosmético que no limpia bajo la encía.
3️⃣ El método Fear-Free de 4 pasos para que tu perro disfrute el cepillado en casa.

📌 Guarda este post y haz hoy la prueba de la uña del pulgar con los juguetes de tu perro.

#SaludDentalCanina #HigieneCanina #OdontologiaVeterinaria #PerritosFelices #AVDC #CrianzaRespetuosa""",
        "tiktokPhotoCopy": """🪥 Capítulo 07: El mal aliento en tu perro NO es normal. Desliza 👉 para aprender el plan de 4 pasos para cepillar sus dientes sin estrés y evitar que el sarro dañe su corazón. #SaludDentalCanina #Veterinaria #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou: 'Si a tu perro le huele mal el aliento, no es por la edad: son bacterias que pueden llegar a su corazón.'",
            "problem": "3-8s • Lou muestra cepillo canino: 'A los 3 años, el 80% de los perros ya tiene enfermedad periodontal porque nadie nos enseñó a acostumbrarlos al cepillo.'",
            "solution": "8-18s • Lou pone pasta enzimática en su dedo para Frodo: 'Empieza dejando que lama pasta enzimática de tu dedo. Plan de 4 pasos en perritosfelices.com.'",
        },
    },
    {
        "order": 8,
        "chapterNum": "08",
        "id": "art-08",
        "slug": "socializacion-cachorros-primeros-meses.html",
        "photoFile": "socializacion-cachorros-primeros-meses.jpg",
        "title": "Socialización temprana del cachorro: guía paso a paso para sus primeros 4 meses",
        "category": "Educación y Entrenamiento",
        "paletteId": "etologia_durazno",
        "focusX": 0.50,
        "focusY": 0.35,
        "cover": {
            "badge": "CAPÍTULO 08 // EDUCACIÓN DE CACHORROS",
            "kicker": "CONSENSO AVSAB • VENTANA CRÍTICA 3 A 16 SEMANAS",
            "kickerItalic": False,
            "title1": "Socializar a tu cachorro:",
            "title2": "calidad antes que cantidad",
            "sub1": "Socializar no es soltarlo con 10 perros desconocidos;",
            "sub2": "es enseñarle a observar el mundo sintiéndose seguro.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Etología Temprana AVSAB",
            "underlineW": 625,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // LA VENTANA NEURONAL DE LAS 3 A 16 SEMANAS",
                "headline": "Esperar a los 4 meses sin ver la calle multiplica el miedo crónico",
                "body": "La AVSAB advierte que los problemas de conducta por falta de socialización temprana causan más abandonos que las enfermedades infecciosas. Se puede socializar sin pisar suelo público.",
                "statValue": "3–16 SEM",
                "statLabel": "Periodo sensible donde el cerebro del cachorro clasifica qué es seguro en la vida",
                "citation": "Fuente: AVSAB Position Statement on Early Puppy Socialization",
            },
            {
                "slideNum": 3,
                "tag": "02 // SOCIALIZACIÓN POSITIVA VS. INUNDACIÓN",
                "headline": "Proteger su espacio hoy evita la reactividad mañana",
                "doTitle": "✔ SOCIALIZACIÓN SEGURA Y POSITIVA",
                "doItems": [
                    "Paseos en brazos o mochila antes de completar sus vacunas",
                    "Premiar la calma mientras observa bicis, paraguas o camiones",
                    "Encuentros 1 a 1 con perros adultos vacunados y equilibrados",
                ],
                "dontTitle": "✘ ERRORES QUE CREAN PERROS REACTIVOS",
                "dontItems": [
                    "Meterlo a un parque canino caótico donde otros lo revuelquen",
                    "Obligarlo a que extraños lo acaricien cuando se esconde tras de ti",
                    "Encerrarlo en casa 4 meses sin escuchar ni ver la ciudad",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // CHECKLIST DEL PRIMER MES EN 3 PILARES",
                "headline": "Experiencias positivas que inmunizan su mente contra el miedo",
                "steps": [
                    {"num": "01", "title": "Superficies y sonidos graduales", "desc": "Caminar en casa sobre alfombra, metal o cartón y oír sonidos de tormenta a volumen bajo con premios."},
                    {"num": "02", "title": "Personas diversas a distancia", "desc": "Ver personas con gorra, casco, bastón o niños corriendo sin forzar el contacto directo."},
                    {"num": "03", "title": "Manejo cooperativo (Husbandry)", "desc": "Tocar suavemente orejas, patitas y dientes 2 segundos seguido siempre de un premio delicioso."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTA GUÍA DE CACHORROS",
                "headline": "Sé siempre el refugio seguro al que tu cachorro pueda acudir",
                "goldenRule": "Regla de Oro: Una sola experiencia tranquila vale más que diez interacciones abrumadoras.",
                "directoryCta": "Encuentra Clases de Cachorros (Puppy Class) Fear-Free en perritosfelices.com",
            },
        ],
        "igCaption": """🐾 ¿Te dijeron que tu cachorro no puede ni asomarse a la ventana hasta terminar todas sus vacunas a los 4 meses? Cuidado: entre las semanas 3 y 16 ocurre el cierre de su ventana crítica de socialización neuronal.

En el Capítulo #08 (basado en la postura oficial de la AVSAB) te enseñamos:
1️⃣ Cómo socializar de forma 100% segura en brazos, coche o con perros sanos conocidos sin riesgo de contagio.
2️⃣ Por qué 'socializar' NO significa obligarlo a que todos los extraños lo toquen ni soltarlo en parques caóticos.
3️⃣ El checklist de sonidos, superficies y manejo cooperativo para su primer mes.

📌 Guarda esta guía o envíasela a ese amigo que acaba de adoptar un cachorro.

#SocializacionCachorros #EducacionCanina #CachorrosFelices #AVSAB #PerritosFelices #CrianzaRespetuosa""",
        "tiktokPhotoCopy": """🐾 Capítulo 08: Cómo socializar a tu cachorro entre las 3 y 16 semanas sin poner en riesgo su salud. Desliza 👉 el checklist completo de la AVSAB. #Cachorros #EducacionCanina #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou: 'El mito más peligroso al tener un cachorro es dejarlo encerrado 4 meses sin ver el mundo.'",
            "problem": "3-8s • Lou explica: 'Su ventana neuronal de socialización se cierra a las 16 semanas. Pero tampoco debes tirarlo al suelo sucio del parque.'",
            "solution": "8-18s • Lou muestra cómo llevarlo en brazos premiando la calma: 'Sal en brazos o mochila a ver el mundo con premios. Checklist en perritosfelices.com.'",
        },
    },
    {
        "order": 9,
        "chapterNum": "09",
        "id": "art-09",
        "slug": "cuidados-perro-senior-calidad-vida.html",
        "photoFile": "cuidados-perro-senior-calidad-vida.jpg",
        "title": "Cómo cuidar a un perro senior: nutrición, movilidad y amor en su etapa dorada",
        "category": "Salud y Prevención",
        "paletteId": "salud_glacial",
        "focusX": 0.50,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 09 // GERIATRÍA CANINA",
            "kicker": "DIRECTRICES AAHA SENIOR CARE • CONFORT ARTICULAR",
            "kickerItalic": False,
            "title1": "Tu perro senior no es",
            "title2": "'flojo': le duelen las articulaciones",
            "sub1": "Pequeños ajustes de pisos, rampas y Omega-3 le",
            "sub2": "devuelven años de movilidad y alegría sin dolor.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Geriatría Veterinaria AAHA",
            "underlineW": 730,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // LA EDAD NO ES UNA ENFERMEDAD (AAHA)",
                "headline": "La osteoartritis silenciosa afecta a más del 80% de los perros geriátricos",
                "body": "Los perros ocultan el dolor crónico por instinto evolutivo. Si tarda en levantarse, duda antes de subir un escalón o se resbala en el piso, hay dolor tratable.",
                "statValue": "CADA 6 MESES",
                "statLabel": "Frecuencia recomendada de chequeo geriátrico (sangre, orina y presión arterial)",
                "citation": "Fuente: AAHA Senior Care Guidelines for Dogs and Cats (2023)",
            },
            {
                "slideNum": 3,
                "tag": "02 // ARQUITECTURA DE CONFORT EN EL HOGAR",
                "headline": "Adaptaciones simples que protegen sus caderas y columna",
                "doTitle": "✔ HOGAR AMIGABLE PARA PERRO SENIOR",
                "doItems": [
                    "Pasillos de alfombras antideslizantes sobre pisos laminados/cerámicos",
                    "Colchón ortopédico viscoelástico lejos de corrientes frías",
                    "Platos elevados a la altura del codo y rampas suaves para el auto",
                ],
                "dontTitle": "✘ ERRORES QUE ACELERAN SU DETERIORO",
                "dontItems": [
                    "Recortar la proteína sin diagnóstico renal (causa sarcopenia muscular)",
                    "Dejar las uñas largas (alteran el apoyo de sus dedos y muñecas)",
                    "Exigir saltos desde la cama o caminatas bajo el sol del mediodía",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // LONGEVIDAD ACTIVA EN 3 PILARES CLÍNICOS",
                "headline": "Cuerpo sin dolor y mente despierta en su etapa dorada",
                "steps": [
                    {"num": "01", "title": "Nutrición muscular y EPA/DHA", "desc": "Proteína de alta digestibilidad para preservar masa muscular y Omega-3 marino antiinflamatorio."},
                    {"num": "02", "title": "Paseos cortos y olfativos", "desc": "Sustituye una caminata larga por 2 o 3 paseos suaves de 15 minutos en terreno plano."},
                    {"num": "03", "title": "Neuroprotección cognitiva", "desc": "Juegos sencillos de olfato y antioxidantes previenen el Síndrome de Disfunción Cognitiva."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTE MANUAL DE ETAPA DORADA",
                "headline": "Acompañar sus canas con dignidad es devolverle toda una vida de lealtad",
                "goldenRule": "Regla de Oro: Un año humano equivale a 5–7 años biológicos en un senior; el chequeo semestral detecta todo a tiempo.",
                "directoryCta": "Encuentra Fisioterapia y Veterinarias Geriátricas en perritosfelices.com",
            },
        ],
        "igCaption": """🤍 No hay amor más noble que el de un perro con el hocico lleno de canas. Cuando tu compañero entra en su etapa senior (a los 6 años en razas gigantes y a los 8–9 en pequeñas), sus necesidades cambian por completo.

En este Capítulo #09 (basado en las guías AAHA Senior Care) revisamos:
1️⃣ Cómo detectar el dolor articular silencioso antes de que cojee.
2️⃣ Por qué un piso resbaladizo y las uñas largas son el mayor enemigo de sus caderas.
3️⃣ Por qué un perro senior sano necesita excelente proteína para no perder masa muscular (sarcopenia).

📌 Guarda esta guía si tienes un viejito en casa y regálale hoy un sendero antideslizante.

#PerroSenior #GeriatriaCanina #PerrosViejitos #SaludCanina #PerritosFelices #AAHA #CrianzaRespetuosa""",
        "tiktokPhotoCopy": """🤍 Capítulo 09: Guía práctica para mejorar la calidad de vida de tu perro senior hoy mismo. Desliza 👉 para ver los ajustes de casa, nutrición y articulaciones. #PerroSenior #PerrosViejitos #Veterinaria #PerritosFelices""",
        "reelScript": {
            "hook": "0-3s • Lou acariciando a un perro senior: 'Tu perro viejito no se volvió flojo de repente: el piso resbaloso de tu casa le da miedo porque le duelen las caderas.'",
            "problem": "3-8s • Toma de patitas sobre piso liso: 'Con la artrosis, cada resbalón le genera micro-lesiones y tensión muscular constante.'",
            "solution": "8-18s • Lou coloca tapetes antideslizantes y plato a altura del pecho: 'Pon caminos de tapetes, corta sus uñas y revisa nuestra guía senior en perritosfelices.com.'",
        },
    },
    {
        "order": 10,
        "chapterNum": "10",
        "id": "art-10",
        "slug": "viajar-con-tu-perro-consejos-seguridad.html",
        "photoFile": "viajar-con-tu-perro-consejos-seguridad.jpg",
        "title": "Viajar con tu perro en auto o avión: checklist completo para una aventura segura",
        "category": "Estilo de Vida",
        "paletteId": "nutricion_menta",
        "focusX": 0.50,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 10 // VIAJES & RUTA SEGURA",
            "kicker": "ESTÁNDARES CPS & IATA • BIOMECÁNICA DE IMPACTO",
            "kickerItalic": False,
            "title1": "Viajar con tu perro:",
            "title2": "el peligro de ir suelto o al cuello",
            "sub1": "A solo 50 km/h, un frenazo multiplica su peso por 30.",
            "sub2": "Aprende a sujetarlo con arnés de pecho certificado.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Seguridad Vial Canina CPS",
            "underlineW": 710,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // FÍSICA DE IMPACTO EN EL AUTOMÓVIL",
                "headline": "Un perro de 15 kg suelto en un choque a 50 km/h proyecta 450 kg de fuerza",
                "body": "El asiento trasero con arnés en 'Y' acolchado anclado al cinturón (o transportadora crash-tested) protege su vida y la de toda la familia.",
                "statValue": "0% AL CUELLO",
                "statLabel": "Jamás conectes el cinturón de seguridad del auto al collar de tu perro",
                "citation": "Fuente: Center for Pet Safety (CPS) Crash Test Standards & IATA",
            },
            {
                "slideNum": 3,
                "tag": "02 // VIAJE SEGURO VS. PRÁCTICAS DE ALTO RIESGO",
                "headline": "Checklist de seguridad vial y aérea libre de accidentes",
                "doTitle": "✔ PROTOCOLO DE VIAJE SEGURO",
                "doItems": [
                    "Asiento trasero con arnés de pecho o transportadora fija",
                    "Ayuno de comida sólida 3 a 4 horas antes (agua siempre libre)",
                    "Paradas cada 2 horas para estirar patas, hidratar y olfatear",
                ],
                "dontTitle": "✘ PELIGROS VIALES Y AÉREOS",
                "dontItems": [
                    "Llevarlo en las piernas del copiloto (el airbag resulta letal)",
                    "Sacar la cabeza por la ventanilla a alta velocidad (úlceras corneales)",
                    "Sedar al perro en vuelos de avión (deprime su termorregulación)",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // MALETA Y LLEGADA AL HOTEL EN 3 PASOS",
                "headline": "Cómo lograr que duerma tranquilo en un lugar desconocido",
                "steps": [
                    {"num": "01", "title": "Su manta con olor a casa", "desc": "Lleva su cama o manta sin lavar; el olor familiar reduce su vigilancia nocturna en el hotel."},
                    {"num": "02", "title": "Su propia comida y agua habitual", "desc": "No cambies de marca de alimento ni de agua bruscamente durante las vacaciones."},
                    {"num": "03", "title": "Paseo olfativo antes de entrar", "desc": "Al bajar del auto, camina 15 minutos tranquilo antes de entrar a la habitación nueva."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTE CHECKLIST DE VIAJE",
                "headline": "Las mejores vacaciones son aquellas donde todos regresan sanos a casa",
                "goldenRule": "Regla de Oro: Placa con código QR y teléfono con prefijo internacional (+502 / +52 / +57) siempre puesta.",
                "directoryCta": "Explora Hoteles Pet-Friendly y Guarderías Sin Jaulas en perritosfelices.com",
            },
        ],
        "igCaption": """🎒🚗 ¿Te vas de viaje con tu perro este fin de semana? Antes de arrancar el auto, revisa esta regla de oro de seguridad vial: NUNCA conectes el cinturón de seguridad a su collar.

En el Capítulo #10 de nuestra serie editorial te compartimos:
1️⃣ Por qué en un frenazo a 50 km/h solo un arnés en 'Y' de pecho o transportadora fija evita lesiones cervicales.
2️⃣ Por qué las aerolíneas y la IATA prohíben sedar a los perros para viajar en avión.
3️⃣ El checklist completo de maleta y adaptación al llegar a un hotel Pet-Friendly.

📌 Guarda esta lista para revisarla antes de cada salida a carretera.

#ViajarConPerros #PerrosViajeros #PetFriendly #SeguridadVialCanina #PerritosFelices #CrianzaRespetuosa""",
        "tiktokPhotoCopy": """🎒 Capítulo 10: Checklist completo para viajar en auto o avión con tu perro de forma 100% segura. Desliza 👉 y descubre por qué nunca debes abrochar el cinturón a su collar. #ViajarConPerros #PetFriendly #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou junto al auto: 'Si abrochas el cinturón de seguridad del auto al collar de tu perro, un solo frenazo puede lesionar su cuello.'",
            "problem": "3-8s • Lou muestra la correa de auto: 'A 50 kilómetros por hora, el peso de tu perro se multiplica por 30. Tampoco lo lleves en el asiento del copiloto por el airbag.'",
            "solution": "8-18s • Lou ancla el cinturón al arnés en Y en el asiento trasero: 'Usa siempre arnés de pecho en el asiento trasero. Checklist de viaje en perritosfelices.com.'",
        },
    },
    {
        "order": 11,
        "chapterNum": "11",
        "id": "art-11",
        "slug": "como-elegir-arnes-en-y-perros.html",
        "photoFile": "como-elegir-arnes-en-y-perros.jpg",
        "title": "Cómo elegir el mejor arnés en Y para tu perro y por qué evitar los collares de ahogo",
        "category": "Educación y Entrenamiento",
        "paletteId": "urgencias_nocturno",
        "focusX": 0.50,
        "focusY": 0.35,
        "cover": {
            "badge": "CAPÍTULO 11 // BIOMECÁNICA DE PASEO",
            "kicker": "\"El dolor jamás enseña respeto, solo pánico.\"",
            "kickerItalic": True,
            "title1": "Arnés ergonómico en 'Y':",
            "title2": "Paseos sin tirones ni ahogo",
            "sub1": "0% presión sobre tráquea y tiroides. Deja libres",
            "sub2": "las escápulas para una zancada natural y cómoda.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Biomecánica Canina UC Davis",
            "underlineW": 715,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // ANATOMÍA CERVICAL CANINA VS. HUMANA",
                "headline": "El cuello de tu perro alberga tráquea, tiroides, yugular y nervios oculares",
                "body": "Estudios de la Universidad de Nottingham y UC Davis demuestran que ningún collar (ni siquiera los anchos) evita picos de presión capaces de dañar la tráquea ante un tirón.",
                "statValue": "0% PRESIÓN",
                "statLabel": "En tráquea y glándula tiroides al distribuir la fuerza sobre el esternón óseo con arnés en Y",
                "citation": "Fuente: Carter et al. (2020, Veterinary Record) & Dra. Christine Zink (Johns Hopkins)",
            },
            {
                "slideNum": 3,
                "tag": "02 // ARNÉS EN 'Y' VS. ARNÉS HORIZONTAL ('T') Y COLLARES",
                "headline": "No todos los arneses respetan el movimiento de sus hombros",
                "doTitle": "✔ ARNÉS ANATÓMICO EN 'Y'",
                "doItems": [
                    "Visto de frente dibuja una 'Y' que rodea la base del cuello sin ahorcar",
                    "Deja totalmente libre la articulación del hombro (escápula)",
                    "Holgura de 3 a 4 dedos detrás del codo para evitar rozaduras en axila",
                ],
                "dontTitle": "✘ EQUIPAMIENTO LESIVO O RESTRICTIVO",
                "dontItems": [
                    "Collares de ahogo, púas o descargas (causan hipotiroidismo y glaucoma)",
                    "Arnés tipo 'T' con banda horizontal en el pecho (bloquea la zancada)",
                    "Correas retráctiles tensas que premian el tirón constante",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // AJUSTE PERFECTO EN 3 COMPROBACIONES",
                "headline": "La prueba de los 2 dedos para saber si su arnés le queda bien",
                "steps": [
                    {"num": "01", "title": "Centro en el manubrio del esternón", "desc": "El punto de unión frontal debe descansar sobre el hueso del pecho, nunca arriba en la garganta."},
                    {"num": "02", "title": "Regla de los 2 dedos de ajuste", "desc": "Deben caber dos dedos planos entre las cintas y su cuerpo: firme para no girar, cómodo para respirar."},
                    {"num": "03", "title": "Colocación cooperativa con premio", "desc": "Presenta el aro del arnés con un snack enfrente para que él mismo introduzca la cabeza por elección."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTA GUÍA BIOMECÁNICA",
                "headline": "Caminar sin dolor transforma el comportamiento de tu perro en el paseo",
                "goldenRule": "Regla de Oro: Si tu perro tose o jadea ronco al caminar, cambia hoy mismo del collar al arnés en 'Y'.",
                "directoryCta": "Encuentra Educadores Positivos y Tiendas Éticas en perritosfelices.com",
            },
        ],
        "igCaption": """⚠️ 'Con el arnés tira más'. Ese mito ha lastimado la tráquea y la tiroides de millones de perros. La ciencia biomecánica (Carter et al., Veterinary Record) es contundente: cualquier tirón sobre el cuello comprime órganos vitales y dispara la presión intraocular.

En este Capítulo #11 con Lou aprenderás:
1️⃣ Por qué el arnés en forma de 'Y' es el único que protege la tráquea Y deja libre el hombro (a diferencia de los arneses horizontales en 'T').
2️⃣ Cómo aplicar la regla de los 2 dedos y la distancia a la axila para un ajuste ergonómico.
3️⃣ Cómo acostumbrar a tu perro a ponerse el arnés de forma cooperativa.

📌 Guarda esta comparativa antes de comprar su próximo equipo de paseo.

#ArnesEnY #NoAlCollarDeAhogo #PaseoRespetuoso #BiomecanicaCanina #PerritosFelices #EducacionCanina""",
        "tiktokPhotoCopy": """⚠️ Capítulo 11: Arnés en 'Y' vs. Arnés en 'T' y collares de ahogo. Desliza 👉 para ver cómo proteger la tráquea y los hombros de tu perro en cada paseo. #ArnesEnY #PaseoCanino #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou mostrando un arnés en Y: 'El dolor jamás enseña respeto, solo enseña pánico. Hablemos del cuello de tu perro.'",
            "problem": "3-8s • Lou señala la zona cervical: 'Ahí están su tráquea y su tiroides. Un tirón con collar o un arnés horizontal bloquea su respiración y sus hombros.'",
            "solution": "8-18s • Lou muestra el ajuste en Y en Frodo y Loki: 'Elige siempre arnés en Y apoyado en el esternón. Guía de tallas en perritosfelices.com.'",
        },
    },
    {
        "order": 12,
        "chapterNum": "12",
        "id": "art-12",
        "slug": "miedo-pirotecnia-ruidos-fuertes-perros.html",
        "photoFile": "miedo-pirotecnia-ruidos-fuertes-perros.jpg",
        "title": "Miedo a la pirotecnia y ruidos fuertes en perros: guía preventiva sin sedantes peligrosos",
        "category": "Comportamiento",
        "paletteId": "urgencias_nocturno",
        "focusX": 0.50,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 12 // FOBIA SONORA & PIROTECNIA",
            "kicker": "ALERTA FARMACOLÓGICA AVSAB • PROHIBIDO USAR ACEPROMACINA",
            "kickerItalic": False,
            "title1": "Pirotecnia y truenos:",
            "title2": "el peligro de las 'gotitas sedantes'",
            "sub1": "La acepromacina paraliza su cuerpo pero deja su",
            "sub2": "mente despierta y con más sensibilidad al ruido.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Etología Clínica & Farmacología",
            "underlineW": 745,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // ALERTA ROJA FARMACOLÓGICA: EL MITO DE LA INMOVILIDAD",
                "headline": "Por qué jamás debes darle 'gotitas para dormir' (Acepromacina) en fiestas",
                "body": "La acepromacina es un tranquilizante disociativo sin efecto ansiolítico: bloquea sus músculos para que no pueda moverse, pero su cerebro escucha cada explosión con terror multiplicado.",
                "statValue": "60,000 Hz",
                "statLabel": "Rango auditivo canino (el triple que el oído humano): los cohetes les causan dolor físico",
                "citation": "Fuente: Dra. Karen Overall & AVSAB Noise Aversion Consensus",
            },
            {
                "slideNum": 3,
                "tag": "02 // CONTENCIÓN RESPETUOSA VS. MITOS OBSOLETOS",
                "headline": "El miedo es una emoción involuntaria: consolarlo NUNCA refuerza el miedo",
                "doTitle": "✔ PROTOCOLO SEGURO ANTE RUIDOS",
                "doItems": [
                    "Acompañarlo con calma si busca contacto (el miedo no se refuerza)",
                    "Crear un búnker acústico interior con mantas, cortinas y ruido marrón",
                    "Consultar 3 semanas antes por ansiolíticos reales (Sileo/Trazodona)",
                ],
                "dontTitle": "✘ PELIGROS EN NOCHES DE PIROTECNIA",
                "dontItems": [
                    "Administrar gotas de acepromacina ('camisa de fuerza química')",
                    "Dejarlo en patios, terrazas o balcones (riesgo de escape y accidentes)",
                    "Ignorarlo cuando tiembla creyendo que 'así se hará más valiente'",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // PREPARA SU REFUGIO EN 3 PASOS",
                "headline": "Cómo amortiguar el impacto sensorial durante las detonaciones",
                "steps": [
                    {"num": "01", "title": "Zona Búnker sin ventanas", "desc": "Habilita el baño interior o vestidor con su cama y ropa tuya semanas antes para que lo asocie con paz."},
                    {"num": "02", "title": "Enmascaramiento con Ruido Marrón", "desc": "Pon música clásica a 50–60 BPM o ruido marrón/ventilador antes de que empiece el primer cohete."},
                    {"num": "03", "title": "Lamido calmante previo", "desc": "Ofrece un LickiMat congelado 40 minutos antes de la hora crítica para elevar su serotonina."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // COMPARTE ESTA ALERTA CON TODAS LAS FAMILIAS",
                "headline": "Ningún perro debería vivir una pesadilla atrapado en su propio cuerpo",
                "goldenRule": "Regla de Oro: Sí puedes abrazar y acompañar a tu perro si tiene miedo; tu presencia regula su sistema nervioso.",
                "directoryCta": "Consulta Etólogos Clínicos y Veterinarias Fear-Free en perritosfelices.com",
            },
        ],
        "igCaption": """🚨 ALERTA IMPORTANTE ANTE COHETES Y TORMENTAS: Si alguien te recomienda 'gotitas sedantes' (Acepromacina) para que tu perro no sufra con la pirotecnia, por favor lee y comparte este carrusel.

En el Capítulo #12 explicamos la evidencia neurofarmacológica:
1️⃣ La Acepromacina NO quita el miedo: paraliza el cuerpo de tu perro como una camisa de fuerza química mientras su cerebro sigue escuchando las explosiones con terror total.
2️⃣ Desmentimos el mito antiguo: acompañar y consolar a tu perro con calma NO refuerza el miedo (las emociones no se refuerzan como las conductas).
3️⃣ Cómo armar un refugio acústico con ruido marrón y cuándo pedir ansiolíticos seguros a tu veterinario.

📌 COMPARTE este post en tus historias: informar a tiempo salva a miles de perros del trauma.

#NoALaPirotecnia #MiedoACohetes #EtologiaClínica #AcepromacinaNo #PerritosFelices #BienestarAnimal""",
        "tiktokPhotoCopy": """🚨 Capítulo 12: Por qué NUNCA debes darle 'gotitas sedantes' (Acepromacina) a tu perro en noches de pirotecnia o truenos. Desliza 👉 y comparte esta alerta. #Pirotecnia #PerrosConMiedo #Veterinaria #PerritosFelices""",
        "reelScript": {
            "hook": "0-3s • Lou seria a cámara: 'Jamás le des las famosas gotitas sedantes de acepromacina a tu perro cuando hay cohetes o truenos.'",
            "problem": "3-8s • Lou explica: 'Ese sedante paraliza sus músculos pero deja su cerebro totalmente despierto. Siente todo el pánico sin poder moverse ni pedir ayuda.'",
            "solution": "8-18s • Lou prepara refugio con mantas y música suave: 'Arma un refugio con ruido marrón y sí, abrázalo si te busca. Guía completa en perritosfelices.com.'",
        },
    },
    {
        "order": 13,
        "chapterNum": "13",
        "id": "art-13",
        "slug": "como-saber-si-tu-perro-es-feliz.html",
        "photoFile": "como-saber-si-tu-perro-es-feliz.jpg",
        "title": "¿Cómo saber si tu perro es feliz? Señales de bienestar canino y etología",
        "category": "Comportamiento",
        "paletteId": "etologia_durazno",
        "focusX": 0.52,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 13 // GUÍA PILAR DE BIENESTAR",
            "kicker": "DR. MARC BEKOFF & MODELO DE LOS 5 DOMINIOS",
            "kickerItalic": False,
            "title1": "¿Cómo saber científicamente",
            "title2": "si tu perro es feliz?",
            "sub1": "La felicidad canina no es saltar eufórico: es dormir",
            "sub2": "profundo, elegir libremente y explorar en calma.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Ciencia del Bienestar Animal",
            "underlineW": 560,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // FELICIDAD REAL VS. SOBREEXCITACIÓN (AROUSAL)",
                "headline": "Un perro que nunca descansa no está 'súper feliz': está sobrecargado",
                "body": "La ciencia del bienestar actual (Modelo de los 5 Dominios de Mellor) mide la plenitud por la calma en el hogar, la calidad del sueño REM y la capacidad de elección.",
                "statValue": "12–14 HORAS",
                "statLabel": "De sueño reparador diario que necesita un perro adulto sano para regular sus emociones",
                "citation": "Fuente: Dr. Marc Bekoff (U. Colorado) & Dr. David Mellor (Five Domains Model)",
            },
            {
                "slideNum": 3,
                "tag": "02 // INDICADORES CLÍNICOS DE UN PERRO PLENO",
                "headline": "Cómo se ve el bienestar genuino en la rutina diaria",
                "doTitle": "✔ SEÑALES DE FELICIDAD AUTÉNTICA",
                "doItems": [
                    "Duerme panza arriba o totalmente estirado (confianza absoluta)",
                    "Ojos almendrados suaves, orejas neutras y 'cola helicóptero'",
                    "Invita al juego con reverencia (play bow) y hace micro-pausas",
                ],
                "dontTitle": "✘ SEÑALES DE ESTRÉS DISFRAZADO DE EUFORIA",
                "dontItems": [
                    "Saltar y morder la correa sin poder autorregularse",
                    "Jadeo constante con comisuras de la boca tensas hacia atrás",
                    "Incapacidad de dormir profundamente cuando te mueves por la casa",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // EL SECRETO DE LA AGENCIA (CAPACIDAD DE ELECCIÓN)",
                "headline": "3 decisiones cotidianas que disparan la autoconfianza de tu perro",
                "steps": [
                    {"num": "01", "title": "Elegir la ruta en el paseo", "desc": "En un cruce seguro, detente y deja que su trufa decida si vamos a la izquierda o a la derecha."},
                    {"num": "02", "title": "Elegir dónde descansar", "desc": "Ofrece una cama mullida en zona social y otra fresca en un rincón tranquilo para que se regule."},
                    {"num": "03", "title": "Respetar cuando dice 'basta'", "desc": "Permitirle retirarse de una visita o caricia le da control sobre su entorno y reduce la ansiedad."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTE TERMÓMETRO DE FELICIDAD",
                "headline": "La verdadera felicidad canina se parece muchísimo a la paz",
                "goldenRule": "Regla de Oro: Si tu perro duerme profundo, come con gusto, olfatea libre y confía en ti, lo estás haciendo increíble.",
                "directoryCta": "Haz el Test Completo en la Guía Pilar de perritosfelices.com",
            },
        ],
        "igCaption": """🐕💛 Todos nos hemos preguntado alguna vez mirándolo dormir: '¿Será realmente feliz conmigo?'. La etología moderna (Dr. Marc Bekoff y el Modelo de los 5 Dominios) tiene respuestas concretas más allá de mover la cola.

En este Capítulo #13 (nuestra Guía Pilar de Bienestar) descubrirás:
1️⃣ Por qué la verdadera felicidad canina se parece más a la calma y al sueño profundo (12–14h al día) que a la euforia hiperactiva.
2️⃣ Qué significa que duerma panza arriba y cómo distinguir una sonrisa relajada de un jadeo por estrés.
3️⃣ El poder de la 'Agencia': cómo darle pequeñas elecciones diarias transforma su salud mental.

📌 Guarda este post para recordar cada día qué es lo que más feliz hace a tu mejor amigo.

#PerroFeliz #BienestarCanino #Etologia #CrianzaRespetuosa #PerritosFelices #AmorPerruno""",
        "tiktokPhotoCopy": """🐕💛 Capítulo 13: ¿Cómo saber científicamente si tu perro es feliz contigo? Desliza 👉 las 5 señales etológicas de bienestar real (y por qué dormir panza arriba dice tanto). #PerroFeliz #EtologiaCanina #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou sonriendo junto a Frodo dormido panza arriba: '¿Quieres saber si tu perro es realmente feliz contigo según la ciencia?'",
            "problem": "3-8s • Lou explica: 'Solemos creer que un perro feliz es el que salta todo el día eufórico, pero eso suele ser exceso de cortisol.'",
            "solution": "8-18s • Toma de Loki y Frodo olfateando y descansando en paz: 'Un perro feliz duerme de 12 a 14 horas, elige su ruta de paseo y confía en su hogar. Haz el test en perritosfelices.com.'",
        },
    },
    {
        "order": 14,
        "chapterNum": "14",
        "id": "art-14",
        "slug": "alergias-alimentarias-ambientales-perros-guia.html",
        "photoFile": "alergias-alimentarias-ambientales-perros-guia.jpg",
        "title": "Alergias alimentarias y ambientales en perros: señales en piel, orejas y patitas",
        "category": "Salud y Prevención",
        "paletteId": "salud_glacial",
        "focusX": 0.65,
        "focusY": 0.36,
        "cover": {
            "badge": "CAPÍTULO 14 // DERMATOLOGÍA CLÍNICA",
            "kicker": "CONSENSO ICADA & CORNELL • 80% ALÉRGENOS DE CONTACTO",
            "kickerItalic": False,
            "title1": "¿Tu perro se lame",
            "title2": "las patas sin parar?",
            "sub1": "No es maña ni ansiedad. El picor interdigital suele",
            "sub2": "deberse a polen o pesticidas tras el paseo diario.",
            "cta": "DESLIZA EL CARRUSEL (1/5)",
            "note": "Dermatología Veterinaria EBVM",
            "underlineW": 535,
        },
        "slides": [
            {
                "slideNum": 2,
                "tag": "01 // PRURITO INTERDIGITAL Y TINCIÓN POR SALIVA",
                "headline": "El pelo rojizo entre sus dedos no es suciedad: son porfirinas de su saliva",
                "body": "Las almohadillas concentran terminaciones nerviosas que se inflaman al pisar pasto con fertilizantes, polen o ácaros. La humedad del lamido multiplica levaduras (Malassezia).",
                "statValue": "8 SEMANAS",
                "statLabel": "Duración de la dieta de eliminación hidrolizada (único método para diagnosticar alergia alimentaria)",
                "citation": "Fuente: Olivry et al. — ICADA Guidelines (2015) & Mueller et al. (2016)",
            },
            {
                "slideNum": 3,
                "tag": "02 // ALERGIA AMBIENTAL (ATOPIA) VS. ALIMENTARIA",
                "headline": "Cómo distinguir qué le está causando el picor y las otitis",
                "doTitle": "✔ PATRÓN AMBIENTAL VS. ALIMENTARIO",
                "doItems": [
                    "Ambiental: empeora tras el parque o en época de lluvias/polen",
                    "Alimentaria: pica los 365 días y suele dar gases o +3 heces al día",
                    "Baño de patitas de 2 min pospaseo retira el 80% de alérgenos",
                ],
                "dontTitle": "✘ ERRORES FRECUENTES EN DERMATOLOGÍA",
                "dontItems": [
                    "Gastar en tests de saliva o pelo para alergias (0% validez científica)",
                    "Ponerle cono isabelino o regañarlo sin aliviar primero el picor",
                    "Abusar de corticoides crónicos sin restaurar su barrera con Omega-3",
                ],
            },
            {
                "slideNum": 4,
                "tag": "03 // RUTINA DE ALIVIO DE BARRERA CUTÁNEA EN CASA",
                "headline": "3 pasos al volver del paseo para frenar el círculo de picor",
                "steps": [
                    {"num": "01", "title": "Enjuague pospaseo de 2 minutos", "desc": "Lava sus patitas con agua tibia y espuma de avena coloidal para barrer polen y pesticidas."},
                    {"num": "02", "title": "Secado suave entre los dedos", "desc": "Presiona con toalla limpia entre las almohadillas sin frotar para no dejar humedad a los hongos."},
                    {"num": "03", "title": "Omega-3 (EPA/DHA) y cama HEPA", "desc": "Lava su cama sin suavizantes perfumados y consulta la dosis de EPA/DHA con tu dermatólogo."},
                ],
            },
            {
                "slideNum": 5,
                "tag": "04 // GUARDA ESTA GUÍA DERMATOLÓGICA",
                "headline": "Aliviar el picor le devuelve el sueño profundo a tu perro y a toda la casa",
                "goldenRule": "Regla de Oro: Si además de lamerse las patas sacude la cabeza o le huelen las orejas, revisa otitis alérgica.",
                "directoryCta": "Encuentra Dermatólogos Veterinarios Fear-Free en perritosfelices.com",
            },
        ],
        "igCaption": """🩺🐾 ¿Has notado que el pelaje entre los dedos de tu perro se tiñe de color café rojizo y se lame las patas cada noche? No lo regañes diciendo 'deja ahí': las porfirinas de su saliva tiñen el pelo porque tiene picor alérgico (prurito).

En el Capítulo #14 de nuestra serie maestra (validado con las guías internacionales ICADA) aprenderás:
1️⃣ Cómo diferenciar una alergia ambiental (polen, pasto, ácaros) de una alergia alimentaria (pollo, res, lácteos).
2️⃣ Por qué los tests comerciales de saliva/sangre para alergia alimentaria no funcionan y cómo se hace la dieta de descarte de 8 semanas.
3️⃣ El ritual de 2 minutos al volver del parque que retira el 80% de los alérgenos de sus patitas.

📌 Guarda esta guía si tu compañero sufre de piel sensible u otitis frecuentes.

#DermatologiaCanina #AlergiaEnPerros #SaludCanina #PerritosFelices #ICADA #VeterinariaFearFree""",
        "tiktokPhotoCopy": """🩺 Capítulo 14: ¿Por qué tu perro se lame las patas hasta dejarlas rojizas? Desliza 👉 para diferenciar alergia ambiental vs alimentaria y ver el lavado de 2 minutos pospaseo. #AlergiaEnPerros #Veterinaria #PerritosFelices #PerrosTikTok""",
        "reelScript": {
            "hook": "0-3s • Lou acariciando a Frodo: 'Si tu perro se lame las patas después del paseo... no lo regañes, te está pidiendo auxilio.'",
            "problem": "3-8s • Lou muestra suavemente las almohadillas: 'El pasto con químicos o el polen se queda atrapado entre sus dedos y les quema la piel.'",
            "solution": "8-18s • Lou premia a Loki y muestra baño de avena: 'Un enjuague con agua tibia de 2 minutos les salva semanas de dermatitis. Guía en perritosfelices.com.'",
        },
    },
]


def build_clean_editorial_svg_45(
    img_uri: str,
    logo_uri: str,
    scrim_id: str,
    scrim_color: str,
    badge_text: str,
    kicker_text: str,
    kicker_is_italic: bool,
    title_line1: str,
    title_line2: str,
    accent_color: str,
    sub_line1: str,
    sub_line2: str,
    cta_text: str,
    footer_note: str,
    underline_width: int = 520,
) -> str:
    """
    Genera un SVG Vertical 4:5 (1080x1350) de estética editorial limpia (cero saturación sobre el perro):
    - Fotografía 100% libre en el 62% superior (840px de 1350px) con paneo Ken Burns suave.
    - Revelado escalonado por máscara (clipPath) en cada línea del titular.
    - Un único trazo orgánico de subrayado bajo la segunda línea del título.
    """
    badge_text = html.escape(badge_text)
    kicker_text = html.escape(kicker_text)
    title_line1 = html.escape(title_line1)
    title_line2 = html.escape(title_line2)
    sub_line1 = html.escape(sub_line1)
    sub_line2 = html.escape(sub_line2)
    cta_text = html.escape(cta_text)
    footer_note = html.escape(footer_note)

    kicker_style = (
        f"font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 27px; font-weight: 700; fill: {accent_color};"
        if kicker_is_italic
        else f"font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: {accent_color};"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,800;1,9..144,700&amp;family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=Space+Mono:wght@700&amp;display=swap');
      
      .title {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 800; fill: #FFFFFF; }}
      .title-accent {{ font-family: 'Fraunces', Georgia, serif; font-size: 60px; font-weight: 800; fill: {accent_color}; }}
      .subtitle {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 25px; font-weight: 500; fill: #F1F5F9; }}
      .badge-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; fill: #FFFFFF; text-transform: uppercase; }}
      .kicker-txt {{ {kicker_style} }}
      .cta-txt {{ font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; fill: #10152B; }}
      .note-txt {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 17px; font-weight: 600; fill: rgba(255, 255, 255, 0.88); }}

      .ken-burns {{
        transform-origin: 540px 500px;
        animation: kbPan 6s cubic-bezier(0.37, 0, 0.63, 1) infinite alternate;
      }}
      @keyframes kbPan {{
        0%   {{ transform: scale(1.0); }}
        100% {{ transform: scale(1.045) translate(-8px, -6px); }}
      }}

      .reveal-1 {{ animation: maskUp 5s cubic-bezier(0.19, 1, 0.22, 1) infinite; }}
      .reveal-2 {{ animation: maskUp2 5s cubic-bezier(0.19, 1, 0.22, 1) infinite; }}
      .reveal-sub {{ animation: fadeSlide 5s cubic-bezier(0.19, 1, 0.22, 1) infinite; }}
      .underline-stroke {{
        stroke-dasharray: {underline_width};
        stroke-dashoffset: {underline_width};
        animation: drawLine 5s cubic-bezier(0.19, 1, 0.22, 1) infinite;
      }}
      .cta-arrow {{ animation: arrowNudge 1.2s ease-in-out infinite alternate; }}

      @keyframes maskUp {{
        0%, 4%   {{ transform: translateY(72px); opacity: 0; }}
        18%, 88% {{ transform: translateY(0px); opacity: 1; }}
        96%, 100%{{ transform: translateY(0px); opacity: 0; }}
      }}
      @keyframes maskUp2 {{
        0%, 8%   {{ transform: translateY(72px); opacity: 0; }}
        22%, 88% {{ transform: translateY(0px); opacity: 1; }}
        96%, 100%{{ transform: translateY(0px); opacity: 0; }}
      }}
      @keyframes fadeSlide {{
        0%, 14%  {{ transform: translateY(20px); opacity: 0; }}
        28%, 88% {{ transform: translateY(0px); opacity: 1; }}
        96%, 100%{{ transform: translateY(0px); opacity: 0; }}
      }}
      @keyframes drawLine {{
        0%, 18%  {{ stroke-dashoffset: {underline_width}; opacity: 0; }}
        22%      {{ opacity: 1; }}
        36%, 88% {{ stroke-dashoffset: 0; opacity: 1; }}
        96%, 100%{{ stroke-dashoffset: 0; opacity: 0; }}
      }}
      @keyframes arrowNudge {{
        0%   {{ transform: translateX(0px); }}
        100% {{ transform: translateX(7px); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
        .underline-stroke {{ stroke-dashoffset: 0 !important; opacity: 1 !important; }}
      }}
    </style>

    <linearGradient id="{scrim_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{scrim_color}" stop-opacity="0.32" />
      <stop offset="48%" stop-color="{scrim_color}" stop-opacity="0.0" />
      <stop offset="68%" stop-color="{scrim_color}" stop-opacity="0.42" />
      <stop offset="86%" stop-color="{scrim_color}" stop-opacity="0.72" />
      <stop offset="100%" stop-color="{scrim_color}" stop-opacity="0.78" />
    </linearGradient>

    <clipPath id="clipLine1">
      <rect x="-10" y="-65" width="960" height="85" />
    </clipPath>
    <clipPath id="clipLine2">
      <rect x="-10" y="5" width="960" height="90" />
    </clipPath>
  </defs>

  <g class="ken-burns">
    <image href="{img_uri}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  </g>

  <rect width="1080" height="1350" fill="url(#{scrim_id})" />

  <g transform="translate(64, 64)">
    <rect width="390" height="56" rx="28" fill="rgba(16, 21, 43, 0.78)" stroke="rgba(255, 255, 255, 0.28)" stroke-width="1.5" />
    <image href="{logo_uri}" x="10" y="6" width="44" height="44" preserveAspectRatio="xMidYMid meet" />
    <text x="66" y="35" class="badge-txt">{badge_text}</text>
  </g>

  <!-- Bloque Tipográfico Editorial Hero en 4:5 (Safe Zone: 64px, y=860 -> >61% foto limpia arriba) -->
  <g transform="translate(64, 860)">
    <g class="reveal-sub">
      <text x="0" y="-28" class="kicker-txt">{kicker_text}</text>
    </g>

    <g clip-path="url(#clipLine1)">
      <g class="reveal-1">
        <text x="0" y="0" class="title">{title_line1}</text>
      </g>
    </g>

    <g clip-path="url(#clipLine2)">
      <g class="reveal-2">
        <text x="0" y="70" class="title-accent">{title_line2}</text>
      </g>
    </g>

    <path class="underline-stroke"
          d="M 2,86 Q {underline_width // 2},94 {underline_width},83"
          fill="none" stroke="{accent_color}" stroke-width="4.5" stroke-linecap="round" />

    <g class="reveal-sub">
      <text class="subtitle">
        <tspan x="0" y="140">{sub_line1}</tspan>
        <tspan x="0" y="176">{sub_line2}</tspan>
      </text>

      <g transform="translate(0, 230)">
        <rect width="390" height="56" rx="28" fill="{accent_color}" />
        <text x="176" y="35" class="cta-txt" text-anchor="middle">{cta_text}</text>
        <g class="cta-arrow" transform="translate(342, 0)">
          <text x="0" y="35" class="cta-txt" font-size="18">➔</text>
        </g>
        <text x="415" y="35" class="note-txt">{footer_note}</text>
      </g>
    </g>
  </g>
</svg>"""


def main():
    print("🎬 Compilando Plan Maestro Secuencial (Capítulos #01 al #14) + Motor 4:5 (1080x1350) y 9:16 (1080x1920)...")

    logo_uri = get_official_logo_uri()

    # Enriquecer cada uno de los 14 capítulos con su Data URI fotográfica real
    enriched_chapters = []
    for ch in CHAPTERS_14:
        photo_path = WEB_ARTICLES_ASSETS / ch["photoFile"]
        img_uri = get_image_data_uri(photo_path)
        pal = PALETTES[ch["paletteId"]]
        ch_copy = dict(ch)
        ch_copy["imgUri"] = img_uri
        ch_copy["palette"] = pal
        enriched_chapters.append(ch_copy)

    # Guardar el Plan Maestro JSON (sin los megabytes de base64 para lectura limpia en repo)
    clean_plan_for_json = []
    for ch in CHAPTERS_14:
        clean_ch = dict(ch)
        clean_ch["palette"] = PALETTES[ch["paletteId"]]
        clean_plan_for_json.append(clean_ch)

    PLAN_JSON_PATH.write_text(
        json.dumps(
            {
                "version": "PF-2027-Sequential-Master-Plan",
                "totalChapters": len(clean_plan_for_json),
                "formats": {
                    "instagram_tiktok_carousel": "4:5 (1080x1350 px) • 5 Láminas por Capítulo",
                    "tiktok_reels_video": "9:16 (1080x1920 px) • Micro-Motion 60fps & Guión Lou",
                },
                "palettes": PALETTES,
                "chapters": clean_plan_for_json,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"✔ Plan Maestro de 14 Capítulos guardado en: {PLAN_JSON_PATH.name}")

    # Los 4 posts destacados para las tarjetas rápidas (ahora representan los 4 pilares en 4:5 1080x1350)
    # Post 1: Cap #01 (Nutrición • Menta), Post 2: Cap #02 (Etología • Durazno),
    # Post 3: Cap #11 (Biomecánica • Contraste), Post 4: Cap #14 (Salud • Glacial)
    featured_map = [
        ("post_01", "post_01_animado_dermatologia.svg", enriched_chapters[13]),  # Cap 14 (Salud Glacial)
        ("post_02", "post_02_animado_nutricion.svg", enriched_chapters[0]),      # Cap 01 (Nutrición Menta)
        ("post_03", "post_03_animado_etologia.svg", enriched_chapters[1]),       # Cap 02 (Etología Durazno)
        ("post_04", "post_04_animado_lou.svg", enriched_chapters[10]),           # Cap 11 (Biomecánica Nocturno)
    ]

    posts_payload = []
    for post_id, svg_name, ch in featured_map:
        pal = ch["palette"]
        cov = ch["cover"]
        svg_code = build_clean_editorial_svg_45(
            img_uri=ch["imgUri"],
            logo_uri=logo_uri,
            scrim_id=f"scrim_{post_id}",
            scrim_color=pal["scrimHex"],
            badge_text=cov["badge"],
            kicker_text=cov["kicker"],
            kicker_is_italic=cov["kickerItalic"],
            title_line1=cov["title1"],
            title_line2=cov["title2"],
            accent_color=pal["coverAccent"],
            sub_line1=cov["sub1"],
            sub_line2=cov["sub2"],
            cta_text=cov["cta"],
            footer_note=cov["note"],
            underline_width=cov["underlineW"],
        )
        (ARTES_DIR / svg_name).write_text(svg_code, encoding="utf-8")
        (STUDIO_ASSETS / svg_name).write_text(svg_code, encoding="utf-8")
        print(f"✔ SVG 4:5 (1080x1350) compilado: {svg_name}")

        posts_payload.append({
            "id": post_id,
            "chapterNum": ch["chapterNum"],
            "imgUri": ch["imgUri"],
            "scrimRgb": pal["scrimRgb"],
            "badge": cov["badge"],
            "kicker": cov["kicker"],
            "kickerItalic": cov["kickerItalic"],
            "title1": cov["title1"],
            "title2": cov["title2"],
            "accent": pal["coverAccent"],
            "sub1": cov["sub1"],
            "sub2": cov["sub2"],
            "cta": cov["cta"],
            "note": cov["note"],
            "underlineW": cov["underlineW"],
            "focusX": ch["focusX"],
            "focusY": ch["focusY"],
        })

    # Generar bundle JS completo para el Studio (incluye los 14 capítulos con sus 5 láminas y las 4 paletas)
    canvas_payload = {
        "logoUri": logo_uri,
        "palettes": PALETTES,
        "chapters": enriched_chapters,
        "posts": posts_payload,
    }

    js_bundle_path = STUDIO_ASSETS / "motion_assets_data.js"
    js_content = (
        "// Generado automáticamente por generar_arte_animado.py — 14 Capítulos en Orden + 4 Paletas PF-2027\n"
        f"window.PF_MOTION_DATA = {json.dumps(canvas_payload, ensure_ascii=False)};\n"
    )
    js_bundle_path.write_text(js_content, encoding="utf-8")
    print(f"✔ Bundle Studio generado: {js_bundle_path} ({js_bundle_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

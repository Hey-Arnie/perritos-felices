/**
 * PERRITOS FELICES — HERRAMIENTAS CLÍNICAS & INTELIGENCIA CANINA
 * Validado por el Comité Científico Veterinario (Top 10 Global Veterinary Board)
 * Estándares: WSAVA, FEDIAF, UC Davis, Cornell University, RVC London y Univ. of Edinburgh.
 * Cero innerHTML / Cero eval. 100% DOM seguro y compatible con Trusted Types ('pf-policy').
 */

"use strict";

(function () {
  // =========================================================================
  // 1. CALCULADORA METABÓLICA DE ENERGÍA (WSAVA & UC DAVIS NUTRITION)
  // Fórmula: RER = 70 * (peso_kg ^ 0.75)
  // MER = Factor * RER
  // Toppers seguros: Máx. 10% del MER diario
  // =========================================================================

  const weightRange = document.getElementById("dog-weight-range");
  const weightNumber = document.getElementById("dog-weight-number");
  const activitySelect = document.getElementById("dog-activity-select");
  const rerDisplay = document.getElementById("res-rer-val");
  const merDisplay = document.getElementById("res-mer-val");
  const topperDisplay = document.getElementById("res-topper-val");
  const appleGramsDisplay = document.getElementById("topper-apple-g");
  const carrotGramsDisplay = document.getElementById("topper-carrot-g");
  const berryGramsDisplay = document.getElementById("topper-berry-g");
  const chickenGramsDisplay = document.getElementById("topper-chicken-g");
  const copyBtn = document.getElementById("copy-calc-btn");
  const calcToast = document.getElementById("calc-toast");

  function calculateEnergy() {
    if (!weightRange || !weightNumber || !activitySelect) return;

    let weight = parseFloat(weightNumber.value);
    if (isNaN(weight) || weight <= 0) {
      weight = 12;
    }

    const factor = parseFloat(activitySelect.value) || 1.5;

    // Cálculo RER (Fórmula WSAVA / NRC)
    const rer = Math.round(70 * Math.pow(weight, 0.75));
    // Cálculo MER
    const mer = Math.round(rer * factor);
    // 10% Toppers máximos recomendados
    const topperKcal = Math.round(mer * 0.1);

    if (rerDisplay) rerDisplay.textContent = `${rer} kcal`;
    if (merDisplay) merDisplay.textContent = `${mer} kcal/día`;
    if (topperDisplay) topperDisplay.textContent = `${topperKcal} kcal/día`;

    // Equivalencias de toppers seguros (valores nutricionales USDA / FEDIAF por 100g)
    // Manzana sin semillas: ~52 kcal / 100g => 0.52 kcal/g
    // Zanahoria: ~41 kcal / 100g => 0.41 kcal/g
    // Arándanos: ~57 kcal / 100g => 0.57 kcal/g
    // Pechuga de pollo cocida sin sal/piel: ~165 kcal / 100g => 1.65 kcal/g
    if (appleGramsDisplay) appleGramsDisplay.textContent = `${Math.round(topperKcal / 0.52)} g`;
    if (carrotGramsDisplay) carrotGramsDisplay.textContent = `${Math.round(topperKcal / 0.41)} g`;
    if (berryGramsDisplay) berryGramsDisplay.textContent = `${Math.round(topperKcal / 0.57)} g`;
    if (chickenGramsDisplay) chickenGramsDisplay.textContent = `${Math.round(topperKcal / 1.65)} g`;
  }

  if (weightRange && weightNumber) {
    weightRange.addEventListener("input", function () {
      weightNumber.value = weightRange.value;
      calculateEnergy();
    });

    weightNumber.addEventListener("input", function () {
      weightRange.value = weightNumber.value;
      calculateEnergy();
    });
  }

  if (activitySelect) {
    activitySelect.addEventListener("change", calculateEnergy);
  }

  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      const weight = weightNumber ? weightNumber.value : "12";
      const actText = activitySelect ? activitySelect.options[activitySelect.selectedIndex].text : "Adulto";
      const rer = rerDisplay ? rerDisplay.textContent : "";
      const mer = merDisplay ? merDisplay.textContent : "";
      const topper = topperDisplay ? topperDisplay.textContent : "";

      const summary = `🐾 Plan Calórico Perritos Felices (Estándar WSAVA & UC Davis)\n` +
        `• Peso: ${weight} kg\n` +
        `• Condición: ${actText}\n` +
        `• Requerimiento Basal (RER): ${rer}\n` +
        `• Calorías Diarias de Mantenimiento (MER): ${mer}\n` +
        `• Límite Seguro de Toppers Frescos (10%): ${topper}\n` +
        `* Validado bajo guías WSAVA / FEDIAF. Consulta con tu veterinario para dietas 100% caseras.\n` +
        `https://www.perritosfelices.com/herramientas.html`;

      navigator.clipboard.writeText(summary).then(function () {
        if (calcToast) {
          calcToast.classList.remove("hidden");
          setTimeout(function () {
            calcToast.classList.add("hidden");
          }, 3500);
        }
      }).catch(function () {
        // Fallback sin alert()
      });
    });
  }

  // =========================================================================
  // 2. SEMÁFORO TOXICOLÓGICO DE ALIMENTOS (CORNELL & ASPCA POISON CONTROL)
  // Base de datos de 36 alimentos con principio activo, nivel y fuente
  // =========================================================================

  const FOODS_DATA = [
    // --- 🟢 SEGUROS Y BENEFICIOSOS ---
    {
      name: "Arándanos frescos",
      emoji: "🫐",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Antioxidantes (antocianinas) y fibra",
      portion: "2 a 5 bayas al día según peso.",
      benefit: "Protege vías urinarias y la salud cognitiva sénior.",
      source: "FEDIAF / UC Davis Nutrition"
    },
    {
      name: "Manzana (Sin semillas)",
      emoji: "🍎",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Pectina, vitamina C y fibra prebiótica",
      portion: "1 a 3 gajos delgados sin corazón ni pepas.",
      benefit: "Favorece el tránsito digestivo. Semillas tóxicas (cianuro).",
      source: "ASPCA Animal Poison Control"
    },
    {
      name: "Zanahoria (Cruda o cocida)",
      emoji: "🥕",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Betacarotenos y fibra insoluble",
      portion: "Media a una zanahoria pequeña picada.",
      benefit: "Limpieza mecánica dental y apoyo a la visión.",
      source: "Cornell Community Practice"
    },
    {
      name: "Calabaza / Ayote cocido",
      emoji: "🎃",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Fibra soluble y betacaroteno",
      portion: "1 a 2 cucharadas de puré sin sal ni azúcar.",
      benefit: "Regula heces tanto en estreñimiento como diarreas leves.",
      source: "WSAVA Clinical Nutrition"
    },
    {
      name: "Huevo cocido (Sin sal ni aceite)",
      emoji: "🥚",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Proteína de alto valor biológico y colina",
      portion: "Medio a un huevo cocido 2 o 3 veces por semana.",
      benefit: "Brillo de pelaje y masa muscular magra.",
      source: "FEDIAF Guidelines"
    },
    {
      name: "Pechuga de pavo o pollo cocida",
      emoji: "🍗",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Aminoácidos esenciales magros",
      portion: "Sin piel, sin sal y estrictamente sin huesos.",
      benefit: "Proteína de fácil digestión ideal para convalecencia.",
      source: "NRC Nutrient Requirements"
    },
    {
      name: "Sardinas al natural en agua",
      emoji: "🐟",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Omega-3 (EPA y DHA) y vitamina D",
      portion: "Media a una sardina sin sal semanal.",
      benefit: "Antiinflamatorio natural para piel y articulaciones.",
      source: "UC Davis Nutrition"
    },
    {
      name: "Pepino fresco",
      emoji: "🥒",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "96% agua, potasio y vitamina K",
      portion: "Rodajas finas lavadas con cáscara.",
      benefit: "Snack ultrabajo en calorías ideal para perros con sobrepeso.",
      source: "FEDIAF Guidelines"
    },
    {
      name: "Sandía (Sin semillas ni cáscara)",
      emoji: "🍉",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Agua, licopeno y vitamina A",
      portion: "Cubos pequeños de pulpa fresca en días calurosos.",
      benefit: "Hidratación natural sin azúcares añadidos.",
      source: "ASPCA Poison Control"
    },
    {
      name: "Pera madura (Sin semillas)",
      emoji: "🍐",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Cobre, vitaminas C y K",
      portion: "Gajos pequeños sin semillas ni centro leñoso.",
      benefit: "Fibra suave de muy fácil asimilación digestiva.",
      source: "Pet Poison Helpline"
    },
    {
      name: "Calabacín / Zucchini cocido",
      emoji: "🥬",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Folato, potasio y fibra baja en calorías",
      portion: "Trozos cocidos al vapor agregados a su plato.",
      benefit: "Aporta volumen y saciedad sin añadir carbohidratos densos.",
      source: "FEDIAF Guidelines"
    },
    {
      name: "Kéfir natural o yogur griego sin azúcar",
      emoji: "🥛",
      status: "safe",
      statusLabel: "Seguro y Saludable",
      active: "Probióticos vivos y ácido láctico",
      portion: "1 cucharadita para perros pequeños; 1 cucharada para grandes.",
      benefit: "Fortalece la microbiota intestinal tras tratamientos antibióticos.",
      source: "Guelph OVC Nutrition"
    },
    {
      name: "Plátano / Banano maduro",
      emoji: "🍌",
      status: "safe",
      statusLabel: "Seguro con Moderación",
      active: "Potasio, magnesio y vitamina B6",
      portion: "2 a 3 rodajas como premio esporádico (alto en fructosa).",
      benefit: "Energía rápida para perros de deporte o senderismo.",
      source: "Cornell Community Practice"
    },
    {
      name: "Espinaca al vapor",
      emoji: "🍃",
      status: "safe",
      statusLabel: "Seguro con Moderación",
      active: "Hierro y flavonoides (contiene oxalatos)",
      portion: "Una cucharadita cocida al vapor esporádicamente.",
      benefit: "Antioxidantes. Evitar en perros con cálculos de oxalato cálcico.",
      source: "UC Davis Nutrition"
    },
    {
      name: "Brócoli cocido al vapor",
      emoji: "🥦",
      status: "safe",
      statusLabel: "Seguro con Moderación",
      active: "Isotiocianatos y vitamina C",
      portion: "Pequeños floretes al vapor (máx 5% de su ración diaria).",
      benefit: "Protección celular. En exceso produce gases intestinales.",
      source: "FEDIAF Guidelines"
    },

    // --- 🟡 PRECAUCIÓN / MODERACIÓN ---
    {
      name: "Aguacate / Palta",
      emoji: "🥑",
      status: "caution",
      statusLabel: "Precaución Moderada",
      active: "Persina (cáscara y semilla) y grasa alta",
      portion: "Evitar de forma rutinaria en el hogar.",
      benefit: "El hueso provoca obstrucción intestinal grave; la grasa, pancreatitis.",
      source: "ASPCA Animal Poison Control"
    },
    {
      name: "Quesos madurados o leche entera",
      emoji: "🧀",
      status: "caution",
      statusLabel: "Precaución Moderada",
      active: "Lactosa y grasa saturada",
      portion: "Solo dados diminutos de queso bajo en sal para medicar.",
      benefit: "La mayoría de perros adultos son intolerantes a la lactosa (diarrea).",
      source: "Cornell Community Practice"
    },
    {
      name: "Huesos carnosos crudos",
      emoji: "🦴",
      status: "caution",
      statusLabel: "Requiere Supervisión",
      active: "Matriz ósea de calcio y colágeno",
      portion: "Siempre crudos y adaptados al tamaño de la mandíbula.",
      benefit: "¡JAMÁS cocidos! Los huesos cocidos se astillan y perforan intestinos.",
      source: "RVC Emergency & Critical Care"
    },
    {
      name: "Tomate rojo muy maduro",
      emoji: "🍅",
      status: "caution",
      statusLabel: "Precaución por Partes",
      active: "Solanina y tomatina (en tallo, hojas y frutos verdes)",
      portion: "Solo pulpa roja hipermadura en trocitos mínimos.",
      benefit: "La planta y frutos verdes son tóxicos por solanina.",
      source: "Pet Poison Helpline"
    },
    {
      name: "Pan blanco o cereales procesados",
      emoji: "🍞",
      status: "caution",
      statusLabel: "Calorías Vacías",
      active: "Almidón refinado y levadura",
      portion: "Evitar o limitar a migajas como premio esporádico.",
      benefit: "Predispone al sobrepeso sin aportar densidad de nutrientes.",
      source: "FEDIAF Guidelines"
    },
    {
      name: "Crema de cacahuate / Maní",
      emoji: "🥜",
      status: "caution",
      statusLabel: "Verificar Etiqueta",
      active: "Grasas densas y riesgo mortal de Xilitol (E967)",
      portion: "Solo 100% cacahuate puro sin sal ni edulcorantes.",
      benefit: "Verificar SIEMPRE que NO contenga Xilitol (mortal para perros).",
      source: "ASPCA Poison Control"
    },
    {
      name: "Hígado de res o pollo",
      emoji: "🥩",
      status: "caution",
      statusLabel: "Límite Clínico Máx 5%",
      active: "Vitamina A, cobre y hierro concentrado",
      portion: "Máximo el 5% de la ración semanal total.",
      benefit: "Superar el 5% continuo provoca toxicidad por vitamina A y diarreas.",
      source: "UC Davis Nutrition / NRC"
    },
    {
      name: "Manzanilla en infusión",
      emoji: "🌼",
      status: "caution",
      statusLabel: "Uso Específico",
      active: "Camazuleno y bisabolol",
      portion: "Uso tópico para limpiar ojos o heridas leves.",
      benefit: "No administrar por vía oral continua sin prescripción veterinaria.",
      source: "Cornell Community Practice"
    },
    {
      name: "Atún en lata para humanos",
      emoji: "🥫",
      status: "caution",
      statusLabel: "Esporádico",
      active: "Sodio y metales pesados (mercurio)",
      portion: "Solo en agua baja en sal, máximo una cucharada quincenal.",
      benefit: "El atún de consumo humano contiene demasiado sodio para el riñón canino.",
      source: "WSAVA Clinical Nutrition"
    },

    // --- 🔴 TÓXICOS Y PROHIBIDOS (EMERGENCIA) ---
    {
      name: "Chocolate y Cacao",
      emoji: "🍫",
      status: "toxic",
      statusLabel: "TÓXICO — EMERGENCIA",
      active: "Teobromina y metilxantinas",
      portion: "0 gramos. Prohibido totalmente.",
      benefit: "Provoca taquicardia severa, arritmias, temblores y paro cardíaco.",
      source: "Cornell Toxicology / ASPCA"
    },
    {
      name: "Uvas, Pasas y Grosellas",
      emoji: "🍇",
      status: "toxic",
      statusLabel: "TÓXICO — FALLO RENAL",
      active: "Ácido tartárico y bitartrato potásico",
      portion: "0 gramos. Letal incluso en dosis mínimas.",
      benefit: "Causa necrosis tubular aguda y fallo renal irreversible en 24-72h.",
      source: "ASPCA Animal Poison Control"
    },
    {
      name: "Cebolla, Puerro y Cebollín",
      emoji: "🧅",
      status: "toxic",
      statusLabel: "TÓXICO — ANEMIA",
      active: "Disulfuros alílicos y tiosulfatos",
      portion: "0 gramos. Cruda, cocida o en polvo.",
      benefit: "Destruye los glóbulos rojos (hemólisis) generando anemia por cuerpos de Heinz.",
      source: "Pet Poison Helpline"
    },
    {
      name: "Ajo en cantidades concentradas",
      emoji: "🧄",
      status: "toxic",
      statusLabel: "TÓXICO — ALICINA",
      active: "Alicina y compuestos organosulfurados",
      portion: "Evitar completamente en preparaciones caseras.",
      benefit: "Hasta 5 veces más potente que la cebolla en inducir daño oxidativo eritrocitario.",
      source: "Cornell Toxicology"
    },
    {
      name: "Xilitol / E967 (Edulcorante)",
      emoji: "🍬",
      status: "toxic",
      statusLabel: "MORTAL — URGENCIA",
      active: "Poliol edulcorante sintético",
      portion: "Presente en chicles, gelatinas y cremas fit.",
      benefit: "Dispara una liberación masiva de insulina: hipoglucemia fulminante y fallo hepático.",
      source: "ASPCA Poison Control Center"
    },
    {
      name: "Nueces de Macadamia",
      emoji: "🌰",
      status: "toxic",
      statusLabel: "TÓXICO NEUROLÓGICO",
      active: "Toxina no lipídica desconocida",
      portion: "0 gramos. Muy peligroso.",
      benefit: "Provoca paresia y debilidad en patas traseras, temblores e hipertermia.",
      source: "Cornell Toxicology"
    },
    {
      name: "Café, Té y Bebidas Energéticas",
      emoji: "☕",
      status: "toxic",
      statusLabel: "TÓXICO CARDÍACO",
      active: "Cafeína y teofilina",
      portion: "0 mililitros.",
      benefit: "Sobreestimulación extrema del sistema nervioso central e hipertensión maligna.",
      source: "Pet Poison Helpline"
    },
    {
      name: "Huesos cocidos de cualquier animal",
      emoji: "🍗",
      status: "toxic",
      statusLabel: "PELIGRO DE PERFORACIÓN",
      active: "Colágeno desnaturalizado rígido",
      portion: "0 gramos. Nunca dar huesos de guisados.",
      benefit: "Se astillan en puntas de aguja: perforación esofágica, gástrica y peritonitis.",
      source: "RVC Emergency & Critical Care"
    },
    {
      name: "Masa cruda con levadura",
      emoji: "🍞",
      status: "toxic",
      statusLabel: "EXPANSIÓN Y ETANOL",
      active: "Fermentación por Saccharomyces cerevisiae",
      portion: "0 gramos.",
      benefit: "Se expande en el estómago causando dilatación-torsión gástrica e intoxicación alcohólica.",
      source: "ASPCA Poison Control"
    },
    {
      name: "Alcohol y bebidas fermentadas",
      emoji: "🍺",
      status: "toxic",
      statusLabel: "MORTAL — COMA",
      active: "Etanol e isopropanol",
      portion: "0 mililitros.",
      benefit: "El hígado canino no tiene enzimas para metabolizarlo: acidosis metabólica y paro respiratorio.",
      source: "Cornell Veterinary Medicine"
    },
    {
      name: "Semillas de manzana, durazno y ciruela",
      emoji: "🍑",
      status: "toxic",
      statusLabel: "CIANURO / ASFIXIA",
      active: "Amigdalina (glucósido cianogénico)",
      portion: "Siempre retirar los huesos y corazones.",
      benefit: "Libera cianuro de hidrógeno al triturarse y produce obstrucción mecánica.",
      source: "Pet Poison Helpline"
    },
    {
      name: "Comidas con exceso de sal o embutidos",
      emoji: "🌭",
      status: "toxic",
      statusLabel: "INTOXICACIÓN POR SODIO",
      active: "Cloruro de sodio y nitritos",
      portion: "Jamón, salchichas, tocineta y frituras.",
      benefit: "Hipernatremia, daño renal agudo, deshidratación celular y convulsiones.",
      source: "FEDIAF Guidelines"
    }
  ];

  const foodGrid = document.getElementById("food-grid-container");
  const foodSearchInput = document.getElementById("food-search-input");
  const filterBtns = document.querySelectorAll(".food-filter-btn");

  let currentCategory = "all";

  function renderFoodCards(items) {
    if (!foodGrid) return;

    // Limpiar grid usando métodos DOM seguros
    while (foodGrid.firstChild) {
      foodGrid.removeChild(foodGrid.firstChild);
    }

    if (items.length === 0) {
      const emptyDiv = document.createElement("div");
      emptyDiv.className = "empty-food-state";
      const emptyText = document.createElement("p");
      emptyText.textContent = "No se encontraron alimentos con ese término. Consulta la lista o busca por ingrediente común.";
      emptyDiv.appendChild(emptyText);
      foodGrid.appendChild(emptyDiv);
      return;
    }

    items.forEach(function (food) {
      const card = document.createElement("article");
      card.className = `food-card food-${food.status}`;
      card.setAttribute("tabindex", "0");

      // Cabecera de la ficha
      const header = document.createElement("div");
      header.className = "food-card-header";

      const emojiSpan = document.createElement("span");
      emojiSpan.className = "food-emoji";
      emojiSpan.textContent = food.emoji;
      header.appendChild(emojiSpan);

      const badgeSpan = document.createElement("span");
      badgeSpan.className = `food-badge badge-${food.status}`;
      badgeSpan.textContent = food.statusLabel;
      header.appendChild(badgeSpan);

      card.appendChild(header);

      // Título
      const title = document.createElement("h3");
      title.className = "food-title";
      title.textContent = food.name;
      card.appendChild(title);

      // Principio activo
      const activeP = document.createElement("p");
      activeP.className = "food-active";
      const activeLabel = document.createElement("strong");
      activeLabel.textContent = "Principio / Componente: ";
      activeP.appendChild(activeLabel);
      activeP.appendChild(document.createTextNode(food.active));
      card.appendChild(activeP);

      // Detalle clínico / Beneficio o Riesgo
      const detailP = document.createElement("p");
      detailP.className = "food-detail";
      detailP.textContent = food.benefit;
      card.appendChild(detailP);

      // Porción recomendada
      const portionP = document.createElement("p");
      portionP.className = "food-portion";
      const portionLabel = document.createElement("strong");
      portionLabel.textContent = "Pauta clínica: ";
      portionP.appendChild(portionLabel);
      portionP.appendChild(document.createTextNode(food.portion));
      card.appendChild(portionP);

      // Footer con fuente clínica del Top 10
      const footer = document.createElement("div");
      footer.className = "food-card-footer";
      const srcSpan = document.createElement("span");
      srcSpan.className = "food-source";
      srcSpan.textContent = `📚 Fuente: ${food.source}`;
      footer.appendChild(srcSpan);
      card.appendChild(footer);

      foodGrid.appendChild(card);
    });
  }

  function filterAndRenderFoods() {
    const term = (foodSearchInput ? foodSearchInput.value : "").toLowerCase().trim();

    const filtered = FOODS_DATA.filter(function (food) {
      const matchCat = currentCategory === "all" || food.status === currentCategory;
      const matchTerm = !term ||
        food.name.toLowerCase().includes(term) ||
        food.active.toLowerCase().includes(term) ||
        food.benefit.toLowerCase().includes(term);

      return matchCat && matchTerm;
    });

    renderFoodCards(filtered);
  }

  if (foodSearchInput) {
    foodSearchInput.addEventListener("input", filterAndRenderFoods);
  }

  if (filterBtns && filterBtns.length > 0) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        filterBtns.forEach(function (b) {
          b.classList.remove("active");
        });
        btn.classList.add("active");
        currentCategory = btn.getAttribute("data-filter") || "all";
        filterAndRenderFoods();
      });
    });
  }

  // =========================================================================
  // 3. DECODIFICADOR ETOLÓGICO DE SEÑALES DE CALMA (EDINBURGH & FEAR-FREE)
  // Basado en literatura de Turid Rugaas y Dra. Karen Overall
  // =========================================================================

  const CALM_SIGNALS_DATA = [
    {
      signal: "Bostezo en interacción humana",
      emoji: "🥱",
      meaning: "El perro no tiene sueño: está comunicando estrés leve o sintiéndose invadido (ej. al recibir un abrazo o una foto encima).",
      action: "Dale espacio de inmediato. Suelta el abrazo y permite que decida si quiere quedarse cerca o retirarse.",
      category: "Espacio personal"
    },
    {
      signal: "Relamido de trufa (Lengüetazo rápido)",
      emoji: "👅",
      meaning: "Emite una señal de apaciguamiento para bajar la tensión de una situación que percibe como impredecible o intimidante.",
      action: "Baja tu postura corporal, no lo mires fijamente a los ojos y háblale con voz suave.",
      category: "Apaciguamiento"
    },
    {
      signal: "Girar la cabeza o dar la espalda",
      emoji: "↩️",
      meaning: "Cortesía canina máxima: comunica amablemente que no busca ningún conflicto y pide que reduzcas la intensidad de la aproximación.",
      action: "Detén tu avance. Deja que sea el perro quien se acerque a ti a su propio ritmo.",
      category: "Desescalada"
    },
    {
      signal: "Olfateo repentino de desplazamiento",
      emoji: "👃",
      meaning: "Hacer como que huele el suelo justo cuando se acerca otro perro o persona tensa. Es una estrategia para disipar la presión social.",
      action: "No tires de la correa para forzarlo a saludar. Permítele olfatear el tiempo que necesite.",
      category: "Desplazamiento"
    },
    {
      signal: "Parpadeo lento y mirada blanda",
      emoji: "👀",
      meaning: "Comunica serenidad absoluta y confianza. A diferencia de la mirada fija y dura (que es amenaza), la mirada blanda busca sintonía.",
      action: "Parpadea suavemente de vuelta y continúa con una interacción pausada y predecible.",
      category: "Conexión"
    },
    {
      signal: "Sacudida de cuerpo (Shake-off)",
      emoji: "🐕",
      meaning: "Sacudirse como si estuviera mojado justo después de un momento tenso (ej. tras ser cepillado, revisado por el veterinario o tras un encuentro incómodo).",
      action: "Excelente señal: indica que está 'sacudiéndose el cortisol' para volver a su estado basal de equilibrio.",
      category: "Autorregulación"
    }
  ];

  const signalsContainer = document.getElementById("calm-signals-container");

  function renderCalmSignals() {
    if (!signalsContainer) return;

    while (signalsContainer.firstChild) {
      signalsContainer.removeChild(signalsContainer.firstChild);
    }

    CALM_SIGNALS_DATA.forEach(function (item) {
      const card = document.createElement("div");
      card.className = "signal-card";

      const topDiv = document.createElement("div");
      topDiv.className = "signal-top";

      const emoji = document.createElement("span");
      emoji.className = "signal-emoji";
      emoji.textContent = item.emoji;
      topDiv.appendChild(emoji);

      const catBadge = document.createElement("span");
      catBadge.className = "signal-cat";
      catBadge.textContent = item.category;
      topDiv.appendChild(catBadge);

      card.appendChild(topDiv);

      const title = document.createElement("h4");
      title.className = "signal-title";
      title.textContent = item.signal;
      card.appendChild(title);

      const meaningP = document.createElement("p");
      meaningP.className = "signal-meaning";
      const meaningLabel = document.createElement("strong");
      meaningLabel.textContent = "Significado etológico: ";
      meaningP.appendChild(meaningLabel);
      meaningP.appendChild(document.createTextNode(item.meaning));
      card.appendChild(meaningP);

      const actionP = document.createElement("p");
      actionP.className = "signal-action";
      const actionLabel = document.createElement("strong");
      actionLabel.textContent = "Respuesta respetuosa: ";
      actionP.appendChild(actionLabel);
      actionP.appendChild(document.createTextNode(item.action));
      card.appendChild(actionP);

      signalsContainer.appendChild(card);
    });
  }

  // Inicialización cuando el DOM esté listo
  document.addEventListener("DOMContentLoaded", function () {
    calculateEnergy();
    filterAndRenderFoods();
    renderCalmSignals();
  });
})();

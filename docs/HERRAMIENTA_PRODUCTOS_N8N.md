# Herramienta Productos - NG Artificiales

Sistema de recomendación de productos con IA para responder consultas de clientes en tiempo real.

---

## 1. Análisis del Negocio

### Empresa
| Campo | Valor |
|-------|-------|
| **Nombre** | NG Artificiales |
| **Rubro** | Señuelos de pesca y equipamiento outdoor |
| **Ubicación** | Argentina |
| **Especialidad** | Pesca deportiva en Patagonia y agua dulce |
| **Catálogo** | ~32 productos |

### Categorías de Productos

| Categoría | Productos | Descripción |
|-----------|-----------|-------------|
| **Señuelos** | Caimán, Caníbal, TNT, Extreme, Turbo, Mojarra, Morena, Cascarudo, Tábano | Artificiales para spinning, trolling, baitcasting |
| **Combos** | Baitcast, Trolling, Spinning | Kits completos con varios señuelos |
| **Térmicos** | Termos, Vasos térmicos | Equipamiento outdoor |
| **Cuchillos** | Pesca, Tácticos, Bowie | Cuchillería especializada |
| **Linternas** | Eco, D3, A1, Scubaglow, Campglow, Carglow | Iluminación outdoor |

### Atributos Clave de Productos

Los productos de pesca tienen atributos específicos que los clientes preguntan:

| Atributo | Ejemplos | Importancia |
|----------|----------|-------------|
| **Especie objetivo** | Trucha, Dorado, Tararira, Salmón, Pejerrey, Surubí | Alta |
| **Modalidad** | Spinning, Trolling, Baitcasting, Casting, Jigging | Alta |
| **Profundidad** | Superficial, Media (1-3m), Profunda (3-5m+) | Alta |
| **Tipo de agua** | Dulce, Salada, Laguna, Río, Lago | Media |
| **Color/Patrón** | Números (03, 06, 11, etc.) | Media |
| **Tamaño/Peso** | Peso en gramos | Media |
| **Paleta** | Larga, Corta | Baja |

### Terminología del Rubro (Sinónimos)

```
señuelo = artificial = cebo artificial = cucharita = crankbait = minnow
caña = vara = equipo
reel = carrete = molinete
trolling = arrastre = curricán
spinning = lanzado
baitcasting = casting liviano
anzuelo = hook = triple
paleta = lip = labio
profundidad = depth = hundimiento
acción = wobble = vibración
```

### Preguntas Frecuentes de Clientes

1. **Por especie**: "¿Qué señuelo me recomendás para trucha?"
2. **Por técnica**: "¿Tenés algo para trolling?"
3. **Por agua**: "¿Cuál sirve para río?"
4. **Por profundidad**: "Necesito algo que baje a 4 metros"
5. **Por disponibilidad**: "¿Tienen stock del Caimán?"
6. **Por color**: "¿Viene en otro color?"
7. **Comparativas**: "¿Cuál es mejor, el TNT o el Extreme?"
8. **Técnicas**: "¿Cómo se usa el Caníbal?"

---

## 2. Credenciales API Tienda Nube

### Configuración para NG Artificiales

```
Store ID:       2590356
Access Token:   ef6b2de9459410120bd24f9ef631aebbe00405f5
Base URL:       https://api.tiendanube.com/v1/2590356/
User-Agent:     NG Artificiales (support@ngartificiales.com)
```

### Headers HTTP

```json
{
  "Authentication": "bearer ef6b2de9459410120bd24f9ef631aebbe00405f5",
  "User-Agent": "NG Artificiales (support@ngartificiales.com)",
  "Content-Type": "application/json"
}
```

### Endpoints

```
GET /products                    # Todos los productos
GET /products?page=1&per_page=100   # Paginado
GET /products/sku/{sku}          # Por SKU
GET /products/{id}               # Por ID
```

---

## 3. Arquitectura del Workflow

### Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HERRAMIENTA PRODUCTOS - NG ARTIFICIALES                  │
│                    Workflow ejecutable desde otros workflows                │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────┐
                    │    Execute Workflow Trigger     │
                    │    Input:                       │
                    │    • query: texto de búsqueda   │
                    │    • mensaje: pregunta cliente  │
                    └─────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETAPA 1: OBTENCIÓN DE DATOS                                               │
│                                                                             │
│  [Save Input] ──► [HTTP Request: GET /products]                            │
│                   URL: https://api.tiendanube.com/v1/2590356/products      │
│                   Headers: bearer token                                     │
│                   Paginación: page=1&per_page=100                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETAPA 2: PREPROCESAMIENTO                                                 │
│                                                                             │
│  [Code: Preprocesar Catálogo]                                              │
│  Output:                                                                    │
│  • appended_title: ["Caimán", "Caníbal", "TNT Extreme", ...]              │
│  • products_min: [{ title, tags, desc_clean }]                            │
│  • index_by_title: { "Caimán": { variants, body_text, ... } }             │
│  • stats: { total_catalog, avg_desc_len }                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETAPA 3: MATCHER LLM                                                      │
│                                                                             │
│  [Gemini 2.5 Pro] "Matcher de Productos"                                   │
│                                                                             │
│  Función: Identifica qué productos del catálogo coinciden con la query     │
│  Input: query + appended_title + products_min + index_by_title             │
│  Output: Lista de títulos que coinciden (o NO_MATCH)                       │
│                                                                             │
│  Lógica:                                                                    │
│  1. Si pide listado de categoría → devolver todos de esa familia           │
│     Ej: "qué señuelos tienen para trucha" → todos con trucha en especies   │
│  2. Si es búsqueda específica → buscar coincidencia exacta/semántica       │
│     Ej: "el Caimán" → Caimán                                               │
│  3. Si no hay coincidencias → NO_MATCH                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
              [NO_MATCH]                      [Tiene Matches]
                    │                               │
                    ▼                               ▼
         [AI Agent: FAQ Handler]         [Extrae títulos → Busca productos]
         Responde con FAQs generales            │
                                                ▼
                                    [Obtiene descripción completa de cada producto]
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETAPA 4: RANKER LLM                                                       │
│                                                                             │
│  [Gemini 2.5 Flash] "Clasificador Estratégico"                             │
│                                                                             │
│  Función: Clasifica los productos encontrados por relevancia               │
│  Input: mensaje del cliente + productos_texto (descripción completa)       │
│  Output JSON:                                                               │
│  {                                                                          │
│    "principales": [...],           // Mejor match                          │
│    "sugeridos_alternativos": [...], // Otras opciones                      │
│    "complementarios": [...],        // Productos relacionados              │
│    "datos_faltantes": [...]         // Info no encontrada                  │
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
              [NO_MATCH]                      [Tiene Ranking]
                    │                               │
                    ▼                               ▼
         [AI Agent: FAQ Handler]              [Aggregate]
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETAPA 5: RESPUESTA FINAL                                                  │
│                                                                             │
│  [AI Agent: "Mojarrita" - Asistente NG]                                    │
│                                                                             │
│  Input:                                                                     │
│  • Intención del cliente (query + mensaje)                                 │
│  • Productos clasificados (JSON)                                           │
│  • FAQs y políticas (Google Docs)                                          │
│                                                                             │
│  Output: Respuesta humanizada como "Mojarrita", asistente de NG            │
│  Incluye:                                                                   │
│  • Saludo empático                                                          │
│  • Recomendación principal con beneficios                                  │
│  • Alternativas si aplica                                                   │
│  • Información técnica (especies, profundidad, modalidad)                  │
│  • Disponibilidad y precio                                                  │
│  • Descargo técnico                                                         │
│  • Cierre con CTA                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETAPA 6: LOGGING                                                          │
│                                                                             │
│  [Google Sheets: Append]                                                    │
│  Guarda: id, mensaje original, respuesta generada, timestamp               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Output: mensaje   │
                         │   (respuesta final) │
                         └─────────────────────┘
```

---

## 4. Nodos del Workflow

### 4.1 Execute Workflow Trigger

```json
{
  "parameters": {
    "inputSource": "jsonExample",
    "jsonExample": "{\n  \"query\": \"señuelo para trucha\",\n  \"mensaje\": \"¿cuál me recomendás para trolling en lago?\"\n}"
  },
  "type": "n8n-nodes-base.executeWorkflowTrigger",
  "name": "When Executed by Another Workflow"
}
```

### 4.2 HTTP Request - Get Products

```json
{
  "parameters": {
    "url": "https://api.tiendanube.com/v1/2590356/products?page=1&per_page=100",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Authentication",
          "value": "bearer ef6b2de9459410120bd24f9ef631aebbe00405f5"
        },
        {
          "name": "User-Agent",
          "value": "NG Artificiales (support@ngartificiales.com)"
        }
      ]
    }
  },
  "type": "n8n-nodes-base.httpRequest",
  "name": "GET Productos NG"
}
```

### 4.3 Code - Preprocesar Catálogo

```javascript
// --- CODE NODE: dataset para matching LLM ---
// Adaptado para NG Artificiales

const MAX_BODY_CHARS = 200000;

function toStringSafe(v) {
  if (v === null || v === undefined) return '';
  if (typeof v === 'string') return v;
  try { return JSON.stringify(v); } catch { return String(v); }
}

function cleanHtml(html, maxLen = MAX_BODY_CHARS) {
  let s = toStringSafe(html);
  s = s.replace(/\s*<\s*br\s*\/?>\s*/gi, '\n');
  s = s.replace(/<\/p\s*>\s*/gi, '\n');
  s = s.replace(/<\/li\s*>\s*/gi, '\n• ');
  s = s.replace(/<[^>]+>/g, ' ');

  const ents = {
    '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
    '&quot;': '"', '&#39;': "'", '&ndash;': '-', '&mdash;': '-',
    '&aacute;': 'á', '&eacute;': 'é', '&iacute;': 'í',
    '&oacute;': 'ó', '&uacute;': 'ú', '&ntilde;': 'ñ'
  };
  s = s.replace(/&[a-z#0-9]+;/gi, m => (m in ents ? ents[m] : ' '));
  s = s.replace(/https?:\/\/\S+/gi, ' ');
  s = s.replace(/[ \t]+/g, ' ').replace(/\s*\n\s*/g, '\n').replace(/\n{3,}/g, '\n\n').trim();

  if (s.length > maxLen) s = s.slice(0, maxLen).trim() + '…';
  return s;
}

function getTagsFromCategories(categories) {
  if (!Array.isArray(categories)) return [];
  return categories
    .map(cat => cat && cat.name && cat.name.es ? cat.name.es.trim() : null)
    .filter(Boolean);
}

// Extrae especies objetivo del texto
function extractEspecies(text) {
  const especies = ['trucha', 'dorado', 'tararira', 'salmón', 'salmon', 'pejerrey',
                    'surubí', 'surubi', 'boga', 'pacu', 'perca', 'corvina'];
  const found = [];
  const lower = text.toLowerCase();
  especies.forEach(e => {
    if (lower.includes(e)) found.push(e);
  });
  return found;
}

// Extrae modalidades del texto
function extractModalidades(text) {
  const modalidades = ['spinning', 'trolling', 'baitcasting', 'casting', 'jigging', 'arrastre'];
  const found = [];
  const lower = text.toLowerCase();
  modalidades.forEach(m => {
    if (lower.includes(m)) found.push(m);
  });
  return found;
}

// ------------------ main ------------------
const appended_title = [];
const products_min = [];
const products_min_short = [];
const index_by_title = {};

for (const item of items) {
  const p = item.json;
  if (!p) continue;

  const title = toStringSafe(p.name?.es).trim();
  if (!title) continue;

  const rawDesc = p.description?.es ?? '';
  const descClean = cleanHtml(rawDesc, 1200);
  const descShort = cleanHtml(rawDesc, 400);
  const tagsArr = p.tags ? p.tags.split(',').map(t => t.trim()) : [];
  const categoriesArr = getTagsFromCategories(p.categories);

  // Extrae metadatos de pesca
  const especies = extractEspecies(descClean);
  const modalidades = extractModalidades(descClean);

  appended_title.push(title);

  products_min.push({
    title,
    tags: [...tagsArr, ...categoriesArr],
    desc_clean: descClean,
    especies,
    modalidades
  });

  products_min_short.push({
    title,
    tags: [...tagsArr, ...categoriesArr],
    desc_clean: descShort
  });

  const variants = Array.isArray(p.variants)
    ? p.variants.map(v => ({
      title: v.values?.map(val => val.es).join(' / ') ?? '',
      sku: v.sku ?? null,
      price: (v.promotional_price !== undefined ? v.promotional_price : v.price) ?? null,
      inventory_quantity: v.stock ?? null
    }))
    : [];

  index_by_title[title] = {
    id: p.variants?.[0]?.sku ?? p.id ?? null,
    handle: p.handle?.es ?? null,
    vendor: p.brand ?? 'NG Artificiales',
    product_type: categoriesArr[0] ?? null,
    tags: [...tagsArr, ...categoriesArr],
    body_text: cleanHtml(rawDesc, MAX_BODY_CHARS),
    variants: variants,
    especies,
    modalidades,
    url: p.canonical_url ?? null
  };
}

// Orden alfabético
const byTitle = (a, b) => a.title.localeCompare(b.title);
products_min.sort(byTitle);
products_min_short.sort(byTitle);
appended_title.sort((a, b) => a.localeCompare(b));

const stats = {
  total_catalog: items.length,
  returned_titles: appended_title.length,
  with_desc: products_min.filter(x => x.desc_clean).length,
  avg_desc_len: (() => {
    const lens = products_min.map(x => x.desc_clean.length);
    if (!lens.length) return 0;
    return Math.round(lens.reduce((a, b) => a + b, 0) / lens.length);
  })()
};

return [{
  json: {
    appended_title,
    products_min,
    products_min_short,
    index_by_title,
    stats
  }
}];
```

---

## 5. Prompts Especializados

### 5.1 MATCHER - System Prompt

```
**ROL Y OBJETIVO**
Actuarás exclusivamente como un motor de coincidencia de productos altamente especializado en PESCA DEPORTIVA y equipamiento outdoor. Tu única función es analizar la consulta del usuario y, siguiendo una jerarquía estricta, decidir qué **títulos de producto** corresponden. **No converses: solo devuelve títulos.**

> **Formato de salida único (sin excepciones):**
> • Devuelve **solo** un **listado plano** con los **títulos exactos** (uno por línea, sin numeración ni viñetas), copiados literalmente desde `APPENDED_TITLE`.
> • Si no hay coincidencias válidas, devuelve exactamente: `NO_MATCH`.
> • **Prohibido**: JSON, comillas, Markdown o texto adicional.

---

## CONTEXTO DEL NEGOCIO

**NG Artificiales** es una tienda argentina especializada en:
- Señuelos de pesca (artificiales, crankbaits, minnows)
- Equipamiento outdoor (térmicos, cuchillos, linternas)

**Tipos de productos:**
- Señuelos: Caimán, Caníbal, TNT, Extreme, Turbo, Mojarra, Morena, Cascarudo, Tábano
- Combos: Baitcast, Trolling, Spinning
- Outdoor: Térmicos, Cuchillos, Linternas

---

## ENTRADAS

Recibirás en el **mensaje del usuario**:

• **QUERY**: texto libre con la consulta del usuario.
• **CANDIDATOS_MIN**: lista JSON de objetos `{ title, tags, desc_clean, especies, modalidades }`
• **INDEX_BY_TITLE**: diccionario con detalles de cada producto
• **APPENDED_TITLE** (lista blanca): array JSON con todos los títulos válidos

> **Señales para el matching** (en este orden de importancia):
>
> 1. `title` (nombre del señuelo/producto)
> 2. `especies` (trucha, dorado, tararira, salmón, pejerrey, surubí, boga, pacu, perca)
> 3. `modalidades` (spinning, trolling, baitcasting, casting, jigging)
> 4. `tags` (etiquetas de categoría)
> 5. `desc_clean` (descripción del producto)

**Normalización obligatoria:** ignora mayúsculas/minúsculas, tildes y espacios múltiples.

**Sinónimos del sector:**
- señuelo = artificial = cebo = cucharita = crankbait = minnow
- caña = vara = equipo
- reel = carrete = molinete
- trolling = arrastre = curricán
- spinning = lanzado
- anzuelo = hook = triple

---

## JERARQUÍA DE ANÁLISIS (PROCESO OBLIGATORIO)

**Paso 1 — Listado por especie o modalidad (máxima prioridad)**
Si la **QUERY** pide productos para una ESPECIE o MODALIDAD específica:
- "señuelos para trucha" → todos los productos con "trucha" en `especies`
- "algo para trolling" → todos con "trolling" en `modalidades`
- "qué tienen para dorado" → todos con "dorado" en `especies`
Devuelve **mínimo 3** si existen. Si aplica, **entrega los títulos y detente**.

**Paso 2 — Listado de categoría**
Si la **QUERY** pide listar una familia completa:
- "qué señuelos tienen" → todos los señuelos
- "ver cuchillos" → todos los cuchillos
- "mostrame los combos" → todos los combos
Devuelve **mínimo 3** si existen.

**Paso 3 — Coincidencia específica**
Si no aplican los pasos anteriores, busca núcleos en título/tags/descripción:
• **Exacto/modelo**: "Caimán", "TNT Extreme", "Caníbal 95"
• **Semántica por función**: "algo para pescar en lago", "señuelo de profundidad"
• **Correcciones ortográficas**: "caiman" → Caimán, "canibal" → Caníbal
Cuando la coincidencia sea dudosa, **verifica** en `INDEX_BY_TITLE[title].body_text`.

**Paso 4 — Filtros de exclusión (último recurso)**
Solo si los pasos 1–3 no dieron resultados:
• **Atributos vagos/subjetivos** ("el mejor señuelo", "algo bueno") → `NO_MATCH`
• **Productos que no vendemos** ("cañas", "reels", "líneas") → `NO_MATCH`

---

## VALIDACIÓN FINAL

1. Identificar títulos candidatos basado en los pasos anteriores
2. Validar cada título contra `APPENDED_TITLE`
3. Descartar los que no estén en la lista
4. Devolver títulos válidos (uno por línea) o `NO_MATCH`

---

## EJEMPLOS

• **QUERY**: "¿Qué señuelos tienen para trucha?"
  **SALIDA ESPERADA**:
  Caimán
  TNT Extreme
  Turbo

• **QUERY**: "Quiero algo para trolling"
  **SALIDA ESPERADA**:
  Caimán
  Combo Trolling

• **QUERY**: "El Caníbal"
  **SALIDA ESPERADA**:
  Caníbal

• **QUERY**: "Necesito una caña"
  **SALIDA ESPERADA**:
  NO_MATCH
```

### 5.2 RANKER - System Prompt

```
# 1. ROL Y DIRECTIVA PRIMARIA

Actuás como un **Motor de Clasificación Estratégica (Strategic Ranking Engine)** especializado en PESCA DEPORTIVA. Tu única función es procesar una consulta de usuario y un corpus de datos de productos para destilar una recomendación jerarquizada y accionable. Sos una capa de inteligencia analítica, no un asistente conversacional. **Tu resultado debe ser un objeto JSON estructurado o, en su defecto, el string literal `NO_MATCH`.** La precisión, relevancia y adherencia al formato de salida son tus únicas métricas de éxito.

# 2. CONTEXTO OPERACIONAL

Operás dentro de un flujo de E-commerce para **NG Artificiales**, una empresa argentina especializada en:
- Señuelos de pesca (artificiales para agua dulce)
- Equipamiento outdoor (térmicos, cuchillos, linternas)

El usuario final es un **pescador deportivo** que busca soluciones a necesidades concretas: especie objetivo, modalidad de pesca, condiciones del agua, profundidad, etc.

# 3. ANÁLISIS DE ENTRADA (INPUTS)

Recibirás dos bloques de información:

• **USER_INTENT_BRIEF**: Mensaje del cliente con su necesidad.
• **PRODUCT_DATA_CORPUS**: Texto con información de productos candidatos.

**Edge case obligatorio:** Si `PRODUCT_DATA_CORPUS` llega vacío, **devuelve `NO_MATCH`** inmediatamente.

# 4. PROCESO COGNITIVO SECUENCIAL

### Paso 1: Deconstrucción del USER_INTENT_BRIEF

Extraé las siguientes facetas:
• **Especie_Objetivo**: ¿Qué pez quiere pescar? (trucha, dorado, tararira, salmón, pejerrey, surubí)
• **Modalidad**: ¿Qué técnica usa? (spinning, trolling, baitcasting, casting)
• **Tipo_de_Agua**: ¿Dónde va a pescar? (lago, río, laguna, mar)
• **Profundidad**: ¿Superficial, media, profunda?
• **Critical_Attributes**: Características específicas mencionadas (color, tamaño, peso)
• **Information_Demands**: Datos solicitados explícitamente (precio, stock, medidas)

### Paso 2: Filtro de Relevancia sobre PRODUCT_DATA_CORPUS

Revisá **cada producto** y compáralo con el perfil de necesidad:

**Categoría `principales`:**
• Condición: Respuesta directa. Cumple `Especie_Objetivo` Y `Modalidad`.
• Acción: Extrae el bloque completo y añadilo a `principales`.

**Categoría `sugeridos_alternativos`:**
• Condición: Resuelve la necesidad pero no es match exacto.
• Acción: Extrae el bloque y añadilo a `sugeridos_alternativos`.

**Categoría `complementarios`:**
• Condición: No resuelve directamente pero se usa junto con el principal.
• Ej: Si pide señuelo, el combo que lo incluye sería complementario.
• Acción: Añadilo a `complementarios`.

**Reglas de calidad:**
• No inventes información.
• No dupliques productos.
• Ordena `principales` por relevancia decreciente.

### Paso 3: Auditoría de Información Faltante

Compará las `Information_Demands` con la info presente en productos `principales`.
Si alguna demanda no está (ej: "profundidad exacta"), agregala a `datos_faltantes`.

# 5. FORMATO DE SALIDA (ESTRICTO)

Tu única salida debe ser un **objeto JSON válido** o el string literal **`NO_MATCH`**. Sin explicaciones.

### A) Salida estructurada (éxito)

{
  "principales": [
    "--- Titulo: [Título]\\nDescripcion: [Descripción]\\nEspecies: [Lista]\\nModalidad: [Lista]\\nProfundidad: [X-Y m]\\nVariantes:\\n• [Color]: $[Precio] ([Stock] en stock) ---"
  ],
  "sugeridos_alternativos": [],
  "complementarios": [],
  "datos_faltantes": ["peso exacto del producto"]
}

### B) Salida de fallo controlado

Si ningún producto es relevante o si `PRODUCT_DATA_CORPUS` estaba vacío:
NO_MATCH

# 6. RESTRICCIONES FINALES

• Respondé **solo** con JSON o `NO_MATCH`.
• Sin Markdown, sin texto adicional.
• Todo debe provenir de `PRODUCT_DATA_CORPUS`.
```

### 5.3 RESPONDER (Mojarrita) - System Prompt

```
**ROL Y DIRECTIVA PRIMARIA**

Actuás como **Mojarrita**, el asistente inteligente de atención al cliente y ventas de **NG Artificiales**. Sos la etapa final de un sistema de IA: la **síntesis y comunicación humana**. Has recibido un dossier completo con la consulta del cliente, productos clasificados y un manual de políticas. Tu misión es transformar estos datos en una respuesta que sea precisa, empática, técnicamente sólida y que genere confianza. Ya no clasificás; ahora **razonás, filtrás, priorizás y conectás** con el cliente.

**TU PERSONALIDAD:**
- Sos Mojarrita 😊, el asistente inteligente del equipo de NG Artificiales
- Tu objetivo es brindar una atención cálida, informativa y eficiente
- Usás lenguaje amigable pero profesional
- Sos conciso y práctico
- Transmitís entusiasmo por ayudar al cliente

---

## FUENTES DE DATOS PARA SÍNTESIS

Tu universo de conocimiento está limitado a:

• **INTENCIÓN DEL CLIENTE**: La consulta original del pescador
• **PRODUCTOS CANDIDATOS (JSON)**: Productos clasificados (principales, sugeridos, complementarios)
• **MANUAL DE POLÍTICAS Y FAQs**: Info logística, garantías, envíos

---

## PROCESO COGNITIVO SECUENCIAL

### Paso 1: Deconstrucción de la Intención

Extraé:
• **Especie_Objetivo**: ¿Qué quiere pescar?
• **Modalidad**: ¿Spinning, trolling, baitcasting?
• **Tipo_de_Agua**: ¿Lago, río, laguna?
• **Profundidad_Deseada**: ¿Superficial, media, profunda?
• **Objetivo_Funcional**: ¿Qué resultado busca?

### Paso 2: Filtro de Relevancia

Revisá cada producto en `principales` y `sugeridos_alternativos`:
- **Directiva de Filtrado Estricto:** Si un señuelo está diseñado para una especie/modalidad que NO corresponde a lo que pidió el cliente, **DESCARTALO**.
- Ej: Si pide "para trucha en trolling" y el producto solo dice "tararira en spinning", NO lo recomiendes.

### Paso 3: Síntesis y Redacción

Con tu lista filtrada, construí tu mensaje:

**1. Apertura con Empatía y Conexión:**
Saludá de forma cálida y conectá con la necesidad del cliente.
Ej: "Soy Mojarrita, el asistente inteligente del equipo 😊 ¡Con gusto te ayudo con tu consulta!"

**2. Recomendación Principal (La Solución Directa):**
- Presentá el producto **más adecuado**
- Mencioná **2-3 beneficios clave** relacionados con su necesidad
- Incluí info técnica relevante
- Precio y stock si es relevante
- Ej: "Para lo que buscás, te recomiendo el **Caimán**. Trabaja entre 3 y 4,5 metros, perfecto para trolling. Lo tenemos a $13,900 y hay stock de varios colores."

**3. Alternativas (Flexibilidad):**
Si hay otros productos relevantes:
- Ej: "Si preferís algo más para spinning o agua más superficial, el **Caníbal 95** es otra excelente opción. Trabaja hasta 1 metro y es ideal para zonas con estructura."

**4. Info Técnica Adicional:**
- Mencioná especies objetivo si no lo hiciste
- Colores disponibles si es relevante
- Cualquier tip de uso

**5. Manejo de `datos_faltantes`:**
Si hay info que no está en la ficha, decilo proactivamente:
- Ej: "El peso exacto no está en la ficha, pero te puedo confirmar que es liviano, ideal para equipos medianos."

**6. Valor Agregado (Confianza):**
- Envío gratis a todo el país
- Garantía (si aplica)
- Link a la tienda

**7. Cierre Profesional:**
- Pregunta que invite a continuar
- Firma
- Ej: "¿Te puedo ayudar con algo más? 😊

**Mojarrita** - NG Artificiales"

---

## REGLAS INQUEBRANTABLES

• **FILTRADO ES MANDATORIO:** Relevancia por especie y modalidad es crítica.
• **CERO ALUCINACIONES:** Si no está en los datos, no lo inventés.
• **PERSONA CONSISTENTE:** Siempre sos Mojarrita, el asistente inteligente de NG Artificiales, cálido y eficiente.
• **TÉCNICO PERO ACCESIBLE:** Usá términos claros, explicá si es necesario.
• **NO RECOMIENDES PRODUCTOS QUE NO VENDEMOS:** Si piden cañas, reels, líneas → decí que solo vendemos señuelos y equipamiento outdoor.
```

---

## 6. Google Docs - FAQs y Políticas

Crear un documento con este contenido:

```markdown
# NG Artificiales - FAQs y Políticas

## ENVÍOS

**¿Hacen envíos a todo el país?**
Sí, hacemos envíos a toda Argentina por Correo Argentino o Andreani.

**¿Cuánto tarda el envío?**
- AMBA: 2-4 días hábiles
- Interior: 4-7 días hábiles
- Patagonia: 5-10 días hábiles

**¿El envío es gratis?**
Consultar en la tienda, depende del monto de compra.

## PRODUCTOS

**¿Los señuelos son de fabricación nacional?**
Sí, todos los señuelos NG Artificiales son diseñados y fabricados en Argentina.

**¿Qué garantía tienen los productos?**
Los señuelos tienen garantía por defectos de fabricación. No cubre roturas por uso o mal manejo.

**¿Los señuelos vienen con anzuelos?**
Sí, todos vienen equipados con triples de calidad.

**¿Qué colores tienen disponibles?**
Cada modelo tiene varios colores identificados por número (03, 06, 11, 12, etc.). Consultá disponibilidad en la tienda.

## PESCA

**¿Qué señuelo me recomiendan para trucha?**
El Caimán y el TNT Extreme son excelentes para truchas. El Caimán trabaja más profundo (3-4.5m), ideal para trolling. El TNT es más versátil.

**¿Qué señuelo sirve para dorado?**
El Turbo y el Extreme son los más recomendados para dorado por su acción agresiva.

**¿Qué profundidad trabaja cada señuelo?**
- Superficial (hasta 1m): Caníbal, Mojarra
- Media (1-3m): TNT, Extreme, Turbo
- Profunda (3-5m): Caimán

**¿Sirven para agua salada?**
Están diseñados principalmente para agua dulce, pero pueden usarse en estuarios. Enjuagar con agua dulce después de usar.

## PAGOS

**¿Qué medios de pago aceptan?**
- Mercado Pago (tarjetas, transferencia)
- Transferencia bancaria
- Efectivo (solo retiro en persona)

**¿Tienen cuotas?**
Sí, a través de Mercado Pago podés pagar en cuotas con tarjeta.

## CONTACTO

**Instagram:** @ngartificiales
**WhatsApp:** Consultar en la tienda
**Email:** Consultar en la tienda
**Web:** https://ngartificiales.com
```

---

## 7. Implementación en n8n

### Pasos para Importar

1. **Crear nuevo workflow** en n8n
2. **Importar nodos** copiando el JSON de cada nodo
3. **Configurar credenciales**:
   - Google Gemini API (para los nodos LLM)
   - Google Docs API (para FAQs)
   - Google Sheets API (para logging)
4. **Crear Google Doc** con las FAQs
5. **Crear Google Sheet** para logs
6. **Conectar nodos** según el diagrama
7. **Probar** con ejemplos

### Variables a Cambiar del Original

| Original (Frida) | Nuevo (NG Artificiales) |
|------------------|-------------------------|
| Store ID: 5224011 | Store ID: 2590356 |
| Token: `a00b317...` | Token: `ef6b2de...` |
| User-Agent: Frida | User-Agent: NG Artificiales |
| Persona: FRIDA | Persona: Mojarrita |
| Rubro: Griferías | Rubro: Pesca/Outdoor |
| Categorías: bachas, duchas | Categorías: señuelos, combos |
| Google Doc ID: (crear nuevo) | Google Doc ID: (nuevo) |
| Google Sheet ID: (crear nuevo) | Google Sheet ID: (nuevo) |

---

## 8. Testing

### Casos de Prueba

| Query | Mensaje | Resultado Esperado |
|-------|---------|-------------------|
| "señuelo para trucha" | "¿cuál me recomendás?" | Caimán, TNT Extreme |
| "trolling" | "algo para el sur" | Caimán, Combo Trolling |
| "Caimán" | "¿qué profundidad trabaja?" | Info del Caimán (3-4.5m) |
| "dorado" | "necesito para el Paraná" | Turbo, Extreme |
| "cuchillo" | "para limpiar pescados" | Cuchillos de pesca |
| "caña spinning" | "precio" | NO_MATCH (no vendemos cañas) |

---

## 9. Próximos Pasos

1. [ ] Exportar workflow de Frida como base
2. [ ] Modificar credenciales Tienda Nube
3. [ ] Reemplazar prompts con los de NG
4. [ ] Crear Google Doc con FAQs
5. [ ] Crear Google Sheet para logs
6. [ ] Configurar credenciales en n8n
7. [ ] Testing con casos de prueba
8. [ ] Activar workflow
9. [ ] Integrar con canal de atención (WhatsApp, chat, etc.)

---

## 10. CAMBIOS MANUALES EN EL WORKFLOW

⚠️ **IMPORTANTE**: Estos son los cambios que debés hacer manualmente en el workflow `PRODUCTOS NICO` en n8n.

### ✅ Nodos que YA están correctos:
- **HTTP Request** (GET Productos): API de Tienda Nube correcta (Store ID 2590356, token correcto)
- **AI Agent** (principal): Ya usa el nombre correcto del rubro
- **Message a model2** (Matcher): Prompt correcto para pesca

### ❌ Nodos que NECESITAN cambios:

#### 1. Nodo `Ranker` (System Message)
**Ubicación**: Buscar el nodo "Message a model4" o similar
**Cambiar**:
```
❌ ANTES: "Operas dentro de un flujo de E‑commerce para **Gambimedic**, una empresa
especializada en equipamiento de ortopedia, movilidad y rehabilitación."

✅ DESPUÉS: "Operás dentro de un flujo de E-commerce para **NG Artificiales**, una empresa
argentina especializada en señuelos de pesca y equipamiento outdoor."
```

#### 2. Nodo `AI Agent5` (System Message)
**Cambiar**:
```
❌ ANTES: "Actuarás como **FRIDA**, una Asesora de Productos experta y el rostro de
**Frida Griferías**"

✅ DESPUÉS: "Actuás como **Mojarrita**, el asistente inteligente de atención al cliente
y ventas de **NG Artificiales**. Tu objetivo es brindar una atención cálida, informativa
y eficiente."
```

#### 3. Nodo `AI Agent7` (System Message)
**Mismo cambio que AI Agent5** - Reemplazar FRIDA por Mojarrita y Frida Griferías por NG Artificiales

#### 4. Nodos `Get a document1`, `Get a document5`, `Get a document7` (Google Docs)
**Estado actual**: Deshabilitados con URL incorrecta
**Acción**:
1. Crear un Google Doc nuevo con las FAQs de NG (ver sección 6 de este documento)
2. Copiar el ID del nuevo documento
3. Actualizar la URL en estos nodos
4. Habilitar los nodos

#### 5. Nodo `Google Sheets` (Logging)
**Estado actual**: URL de otro proyecto
**Acción**:
1. Crear una Google Sheet nueva para logs de NG
2. Actualizar el ID de la hoja
3. Verificar que las columnas coincidan

### 📋 Checklist de cambios:

| # | Nodo | Cambio | Estado |
|---|------|--------|--------|
| 1 | Ranker | Cambiar "Gambimedic" → "NG Artificiales" | ⬜ |
| 2 | AI Agent5 | Cambiar "FRIDA" → "Mojarrita" | ⬜ |
| 3 | AI Agent7 | Cambiar "FRIDA" → "Mojarrita" | ⬜ |
| 4 | Get a document1/5/7 | Nueva URL de Google Doc | ⬜ |
| 5 | Google Sheets | Nueva URL de hoja de logs | ⬜ |

---

*Documento creado: 2026-01-13*
*Actualizado: 2026-01-14*
*Proyecto: NG Artificiales*
*Adaptado de: Herramienta Productos Frida Griferías*

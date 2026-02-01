# Plan Dashboard de Ventas - NG Artificiales

Este documento define el plan completo para crear un dashboard de ventas moderno para NG Artificiales.

---

## 1. Información del Cliente

### Empresa
| Campo | Valor |
|-------|-------|
| **Nombre** | NG Artificiales |
| **Rubro** | Señuelos de pesca y equipamiento outdoor |
| **País** | Argentina |
| **Moneda** | ARS (Pesos Argentinos) |
| **Website** | https://ngartificiales.com |
| **Tienda** | ngartificiales2.mitiendanube.com |
| **Redes** | Instagram (@ngartificiales), Facebook, WhatsApp |

### Catálogo de Productos (~32 productos)

**Señuelos de Pesca:**
- Combos (Baitcast, Trolling, Spinning)
- Modelos: Mojarra, Canibal, TNT, Extreme, Turbo, Morena, Cascarudo, Tabano, Caimán

**Equipamiento Outdoor:**
- Térmicos (termos, vasos térmicos)
- Cuchillos (pesca, tácticos, Bowie)
- Linternas (Eco, D3, A1, Scubaglow, Campglow, Carglow)

**Rango de precios:** $13,700 - $19,900 ARS

---

## 2. Credenciales Tienda Nube

### API Principal (App ID: 24843)
```
Client ID:      24843
Client Secret:  110e52535428ba4d607f60303ad0b90cd318a061ac4d373c
Access Token:   ef6b2de9459410120bd24f9ef631aebbe00405f5
User ID:        2590356
```

### Permisos Disponibles
```
read_content, write_content
read_products, write_products
read_coupons, write_coupons
read_customers, write_customers
read_orders, write_orders
read_shipping, write_shipping
read_discounts, write_discounts
read_draft_orders, write_draft_orders
write_scripts
read_locations, write_locations
read_fulfillment_orders, write_fulfillment_orders
read_domains, write_domains
read_subscriptions, write_subscriptions
read_email_templates, write_email_templates
read_logistic, write_logistic
write_charges, write_plans
```

### Endpoints Base
```
API Base:    https://api.tiendanube.com/v1/{user_id}/
Webhook:     https://paneln8n.traid.business/webhook/nicoan
```

---

## 3. Arquitectura del Dashboard

### Stack Tecnológico
```
Frontend:    Next.js 14 + TypeScript
UI:          Tailwind CSS + shadcn/ui
Gráficos:    Recharts
Estado:      React Query (TanStack Query)
Backend:     API Routes de Next.js
Base datos:  Supabase (cache y datos históricos)
Deploy:      Vercel
```

### Estructura de Carpetas
```
ngartificiales/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Dashboard principal
│   │   ├── ventas/page.tsx       # Detalle ventas
│   │   ├── productos/page.tsx    # Análisis productos
│   │   ├── clientes/page.tsx     # Análisis clientes
│   │   └── api/
│   │       └── tiendanube/       # Proxy a Tienda Nube
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── KPICard.tsx
│   │   │   ├── SalesChart.tsx
│   │   │   ├── TopProducts.tsx
│   │   │   ├── RecentOrders.tsx
│   │   │   └── CustomerMap.tsx
│   │   └── ui/                   # shadcn components
│   ├── lib/
│   │   ├── tiendanube.ts         # Cliente API
│   │   └── utils.ts
│   └── types/
│       └── tiendanube.ts         # Tipos TypeScript
├── docs/
│   └── PLAN_DASHBOARD_VENTAS.md
└── .env.local                    # Credenciales
```

---

## 4. Módulos del Dashboard

### 4.1 Panel Principal (Home)

**KPIs en tiempo real:**
- Ventas del día/semana/mes
- Cantidad de órdenes
- Ticket promedio
- Comparativa vs período anterior (%)

**Gráficos:**
- Ventas últimos 30 días (línea)
- Ventas por categoría (dona)
- Órdenes por estado (barras)

**Tablas:**
- Últimas 10 órdenes
- Top 5 productos del mes

### 4.2 Análisis de Ventas

**Filtros:**
- Rango de fechas
- Categoría de producto
- Estado de orden
- Método de pago

**Visualizaciones:**
- Evolución de ventas (línea con área)
- Ventas por día de la semana (heatmap)
- Horarios pico de compra
- Métodos de pago preferidos

**Métricas:**
- Ventas totales
- Cantidad de órdenes
- Ticket promedio
- Tasa de conversión

### 4.3 Análisis de Productos

**Top productos:**
- Por cantidad vendida
- Por ingresos generados
- Por margen (si hay datos de costo)

**Performance por categoría:**
- Señuelos vs Outdoor
- Subcategorías

**Alertas:**
- Stock bajo
- Productos sin ventas (últimos 30 días)

### 4.4 Análisis de Clientes

**Métricas:**
- Total clientes
- Clientes nuevos vs recurrentes
- Frecuencia de compra
- Valor de vida del cliente (LTV)

**Segmentación:**
- Por ubicación geográfica
- Por valor de compra
- Por frecuencia

**Mapa:**
- Distribución geográfica de clientes en Argentina

### 4.5 Operaciones

**Estados de órdenes:**
- Pendientes de pago
- Pendientes de envío
- En tránsito
- Entregadas
- Canceladas

**Tiempos:**
- Tiempo promedio de fulfillment
- Tiempo promedio de entrega

---

## 5. Integraciones

### 5.1 Tienda Nube API

**Endpoints a consumir:**
```
GET /orders                    # Órdenes
GET /orders/{id}              # Detalle orden
GET /products                 # Productos
GET /products/{id}            # Detalle producto
GET /customers                # Clientes
GET /customers/{id}           # Detalle cliente
```

**Headers requeridos:**
```
Authentication: bearer {access_token}
User-Agent: NG Artificiales Dashboard (support@ngartificiales.com)
Content-Type: application/json
```

### 5.2 Supabase (Cache y Datos Históricos)

**Tablas:**
```sql
-- Órdenes sincronizadas
orders (
  id, tiendanube_id, customer_id, total, status,
  payment_status, shipping_status, created_at, synced_at
)

-- Productos
products (
  id, tiendanube_id, name, category, price, stock, synced_at
)

-- Clientes
customers (
  id, tiendanube_id, email, name, total_orders,
  total_spent, first_order_at, last_order_at, synced_at
)

-- Métricas diarias (agregado)
daily_metrics (
  date, total_sales, order_count, avg_ticket, new_customers
)
```

### 5.3 n8n (Sincronización)

**Workflows:**
1. **Sync Orders** - Cada 15 min, sincroniza órdenes nuevas
2. **Sync Products** - Cada hora, actualiza stock y precios
3. **Daily Metrics** - Diario 00:05, calcula métricas del día anterior
4. **Webhook Orders** - Tiempo real, procesa nuevas órdenes

---

## 6. Diseño UI/UX

### Paleta de Colores
```css
--primary:    #2563eb  /* Azul - acciones principales */
--success:    #22c55e  /* Verde - métricas positivas */
--warning:    #f59e0b  /* Amarillo - alertas */
--danger:     #ef4444  /* Rojo - métricas negativas */
--neutral:    #64748b  /* Gris - texto secundario */
--background: #f8fafc  /* Fondo claro */
--card:       #ffffff  /* Tarjetas */
```

### Componentes Principales

**KPI Card:**
- Valor principal grande
- Comparativa período anterior con flecha y %
- Icono representativo
- Sparkline opcional

**Gráfico de Ventas:**
- Línea con área gradiente
- Tooltip con detalle
- Zoom por período

**Tabla de Órdenes:**
- Paginación
- Filtros inline
- Estado con badge de color
- Acciones rápidas

### Responsive
- Desktop: Grid 4 columnas para KPIs
- Tablet: Grid 2 columnas
- Mobile: Stack vertical, gráficos simplificados

---

## 7. Plan de Implementación

### Fase 1: Setup y Estructura (Día 1)
- [ ] Crear proyecto Next.js
- [ ] Configurar Tailwind + shadcn/ui
- [ ] Configurar variables de entorno
- [ ] Crear cliente API Tienda Nube
- [ ] Crear tipos TypeScript

### Fase 2: Dashboard Principal (Día 2)
- [ ] Layout con sidebar
- [ ] KPI Cards
- [ ] Gráfico de ventas últimos 30 días
- [ ] Tabla últimas órdenes

### Fase 3: Páginas Secundarias (Día 3)
- [ ] Página de Ventas con filtros
- [ ] Página de Productos
- [ ] Página de Clientes

### Fase 4: Supabase + Sync (Día 4)
- [ ] Crear tablas en Supabase
- [ ] Implementar sincronización inicial
- [ ] Workflows n8n para sync continuo

### Fase 5: Polish y Deploy (Día 5)
- [ ] Optimización de queries
- [ ] Loading states y error handling
- [ ] Deploy a Vercel
- [ ] Documentación

---

## 8. Variables de Entorno

```env
# Tienda Nube
TIENDANUBE_CLIENT_ID=24843
TIENDANUBE_CLIENT_SECRET=110e52535428ba4d607f60303ad0b90cd318a061ac4d373c
TIENDANUBE_ACCESS_TOKEN=ef6b2de9459410120bd24f9ef631aebbe00405f5
TIENDANUBE_USER_ID=2590356

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# n8n
N8N_WEBHOOK_URL=https://paneln8n.traid.business/webhook/nicoan
```

---

## 9. Próximos Pasos

1. **Confirmar** este plan con el cliente
2. **Crear proyecto** en Supabase
3. **Iniciar desarrollo** del dashboard
4. **Configurar workflows** en n8n
5. **Deploy** y entrega

---

*Documento creado: 2025-01-09*
*Cliente: NG Artificiales*
*Responsable: Traid Business*

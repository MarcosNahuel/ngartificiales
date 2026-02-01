# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dashboard de ventas para **NG Artificiales** - tienda de señuelos de pesca y equipamiento outdoor en Argentina. Integrado con Tienda Nube API.

## Commands

```bash
# Dashboard (Next.js)
cd dashboard
npm run dev       # http://localhost:3000
npm run build     # Build produccion
npm run lint      # ESLint

# Analytics (Python)
cd analytics
python extract_and_analyze.py   # Extrae datos de Tienda Nube API
python full_analysis.py         # Genera analisis y data.json
```

## Architecture

```
ngartificiales/
├── dashboard/          # Next.js 16 + React 19 + TypeScript
│   ├── app/
│   │   ├── page.tsx             # Dashboard principal
│   │   ├── ventas/              # Analisis de ventas
│   │   ├── productos/           # Analisis de productos
│   │   ├── clientes/            # Segmentacion RFM
│   │   ├── forecasting/         # Predicciones ML
│   │   ├── components/          # Componentes reutilizables
│   │   └── lib/utils.ts         # Formatters (currency, date, etc)
│   └── public/data.json         # Datos estaticos del analisis
│
├── analytics/          # Scripts Python para ETL y analisis
│   ├── extract_and_analyze.py   # Extraccion desde Tienda Nube
│   └── full_analysis.py         # Analisis descriptivo, ML, forecasting
│
└── docs/               # Documentacion del proyecto
```

## Tech Stack

- **Frontend**: Next.js 16.1.1, React 19, TypeScript, Tailwind CSS 4
- **Charts**: Recharts
- **Icons**: Lucide React
- **Analytics**: Python (pandas, numpy)
- **Deploy**: Vercel

## Data Flow

1. `analytics/extract_and_analyze.py` obtiene datos de Tienda Nube API
2. `analytics/full_analysis.py` genera analisis (RFM, forecasting, regresion)
3. Output se guarda en `dashboard/public/data.json`
4. Dashboard consume `data.json` como datos estaticos

## Key Data Structure (data.json)

```typescript
{
  descriptive: {
    kpis: { total_revenue, total_orders, avg_ticket, unique_customers }
    monthly_sales, top_products, weekday_sales, province_sales, payment_methods
  },
  forecasting: {
    summary: { forecast_30d_total, trend_percentage, quarterly_projection }
    historical, forecasts, weekly_pattern
  },
  segmentation: {
    segments: [{ segment, count, percentage, revenue }]  // Champions, Loyal, Potential, At Risk, Lost
    customer_details: [{ customer_id, recency, frequency, monetary, segment }]
  },
  regression: { linear_regression, predictions_30d }
}
```

## Tienda Nube API

- Base URL: `https://api.tiendanube.com/v1/2590356/`
- Auth: `Authentication: bearer {ACCESS_TOKEN}`
- Endpoints: `/orders`, `/products`, `/customers`
- Credenciales en `docs/PLAN_DASHBOARD_VENTAS.md`

## Utilities

`app/lib/utils.ts` contiene:
- `formatCurrency(n)` - Formato ARS ($1.234.567)
- `formatNumber(n)` - Formato numerico es-AR
- `formatPercent(n)` - Formato +10.5%
- `cn(...classes)` - Merge Tailwind classes

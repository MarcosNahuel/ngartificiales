'use client'

import { Header } from '../components/Header'
import { formatCurrency, formatNumber } from '../lib/utils'
import advancedData from '../../public/advanced_analysis.json'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  AreaChart, Area, BarChart, Bar, Cell, ComposedChart, ReferenceLine
} from 'recharts'
import { ChartContainer } from '../components/ChartContainer'

export default function AnalisisPage() {
  const { weekly_analysis, cycles, forecasting, pareto } = advancedData

  // Datos para serie semanal con forecast
  const weeklyWithForecast = [
    ...forecasting.historical.slice(-26).map((h: { date: string; sales: number; sma_4: number | null }) => ({
      week: h.date.slice(5),
      sales: h.sales,
      sma: h.sma_4,
      type: 'historical'
    })),
    ...forecasting.forecasts.map((f: { date: string; forecast: number; lower_bound: number; upper_bound: number }) => ({
      week: f.date.slice(5),
      forecast: f.forecast,
      lower: f.lower_bound,
      upper: f.upper_bound,
      type: 'forecast'
    }))
  ]

  // Datos para autocorrelacion
  const autocorrData = cycles.autocorrelation.slice(0, 12).map((a: { lag: number; correlation: number }) => ({
    lag: `${a.lag}s`,
    correlation: a.correlation,
    significant: Math.abs(a.correlation) > 0.3
  }))

  // Datos para Pareto
  const paretoData = pareto.products.slice(0, 15).map((p: { name: string; revenue: number; cumulative_pct: number; rank: number }) => ({
    name: p.name.slice(0, 15),
    fullName: p.name,
    revenue: p.revenue,
    cumulative: p.cumulative_pct,
    is80: p.cumulative_pct <= 80
  }))

  // Patron mensual
  const monthlyPattern = Object.entries(cycles.monthly_pattern).map(([month, avg]) => ({
    month: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'][parseInt(month) - 1],
    avg: avg as number
  }))

  return (
    <div>
      <Header
        title="Analisis Avanzado"
        subtitle="Series temporales, ciclos y analisis Pareto"
      />

      {/* KPIs Serie Semanal */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <div className="bg-card rounded-2xl p-5 shadow-sm border border-card">
          <p className="text-xs text-muted mb-1">Semanas Analizadas</p>
          <p className="text-2xl font-bold text-foreground">{weekly_analysis.stats.total_weeks}</p>
        </div>
        <div className="bg-card rounded-2xl p-5 shadow-sm border border-card">
          <p className="text-xs text-muted mb-1">Prom. Semanal</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(weekly_analysis.stats.avg_weekly_sales)}</p>
        </div>
        <div className="bg-card rounded-2xl p-5 shadow-sm border border-card">
          <p className="text-xs text-muted mb-1">Coef. Variacion</p>
          <p className="text-2xl font-bold text-orange-600">{weekly_analysis.stats.cv.toFixed(0)}%</p>
        </div>
        <div className="bg-card rounded-2xl p-5 shadow-sm border border-card">
          <p className="text-xs text-muted mb-1">Semanas Activas</p>
          <p className="text-2xl font-bold text-foreground">{weekly_analysis.stats.weeks_with_sales}</p>
          <p className="text-xs text-gray-400">{((weekly_analysis.stats.weeks_with_sales / weekly_analysis.stats.total_weeks) * 100).toFixed(0)}%</p>
        </div>
        <div className="bg-card rounded-2xl p-5 shadow-sm border border-card">
          <p className="text-xs text-muted mb-1">Tendencia</p>
          <p className={`text-2xl font-bold ${cycles.trend_direction === 'growing' ? 'text-green-600' : 'text-red-600'}`}>
            {cycles.trend_direction === 'growing' ? 'CRECIENTE' : 'DECRECIENTE'}
          </p>
          <p className="text-xs text-gray-400">+{formatCurrency(cycles.trend_slope)}/sem</p>
        </div>
      </div>

      {/* Serie Temporal con Forecast */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card mb-8">
        <h3 className="text-lg font-semibold text-foreground mb-2">Serie Temporal Semanal con Forecast</h3>
        <p className="text-sm text-muted mb-4">Ultimas 26 semanas + 12 semanas de proyeccion</p>
        <div className="h-80">
          <ChartContainer>
            <ComposedChart data={weeklyWithForecast}>
              <defs>
                <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="week" tick={{ fontSize: 10 }} stroke="#9ca3af" interval={2} />
              <YAxis
                tick={{ fontSize: 10 }}
                stroke="#9ca3af"
                tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`}
              />
              <Tooltip formatter={(value) => formatCurrency(Number(value) || 0)} />
              <Area type="monotone" dataKey="sales" stroke="#3b82f6" fill="url(#colorSales)" strokeWidth={2} name="Ventas" />
              <Line type="monotone" dataKey="sma" stroke="#f59e0b" strokeWidth={2} dot={false} name="SMA-4" />
              <Area type="monotone" dataKey="upper" stroke="none" fill="#bbf7d0" name="Banda Sup." />
              <Area type="monotone" dataKey="lower" stroke="none" fill="#ffffff" />
              <Line type="monotone" dataKey="forecast" stroke="#22c55e" strokeWidth={3} strokeDasharray="5 5" dot={false} name="Forecast" />
              <ReferenceLine x="12-15" stroke="#9ca3af" strokeDasharray="3 3" label={{ value: 'Hoy', fontSize: 10 }} />
            </ComposedChart>
          </ChartContainer>
        </div>
        <div className="flex gap-6 mt-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-blue-500"></div>
            <span className="text-gray-600">Ventas Reales</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-amber-500"></div>
            <span className="text-gray-600">Media Movil 4 sem</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-green-500" style={{ borderTop: '2px dashed #22c55e' }}></div>
            <span className="text-gray-600">Forecast 12 sem</span>
          </div>
        </div>
      </div>

      {/* Ciclos y Patron Mensual */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Autocorrelacion */}
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <h3 className="text-lg font-semibold text-foreground mb-2">Identificacion de Ciclos</h3>
          <p className="text-sm text-muted mb-4">Autocorrelacion por lag (semanas)</p>
          <div className="h-64">
            <ChartContainer>
              <BarChart data={autocorrData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" domain={[-0.5, 1]} tick={{ fontSize: 10 }} />
                <YAxis dataKey="lag" type="category" tick={{ fontSize: 10 }} width={30} />
                <Tooltip formatter={(value) => (Number(value) || 0).toFixed(3)} />
                <ReferenceLine x={0.3} stroke="#22c55e" strokeDasharray="3 3" label={{ value: 'Sig.', fontSize: 9 }} />
                <ReferenceLine x={-0.3} stroke="#ef4444" strokeDasharray="3 3" />
                <Bar dataKey="correlation" name="Correlacion">
                  {autocorrData.map((entry: { significant: boolean }, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.significant ? '#3b82f6' : '#d1d5db'} />
                  ))}
                </Bar>
              </BarChart>
            </ChartContainer>
          </div>
          <div className="mt-4 p-4 bg-blue-50 rounded-xl">
            <p className="text-sm text-blue-800 font-medium">Ciclos Detectados:</p>
            <ul className="text-sm text-blue-700 mt-2">
              {cycles.significant_cycles.map((c: { lag: number; correlation: number }) => (
                <li key={c.lag}>Ciclo de {c.lag} semana(s): r={c.correlation.toFixed(2)}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* Patron Mensual */}
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <h3 className="text-lg font-semibold text-foreground mb-2">Patron Estacional Mensual</h3>
          <p className="text-sm text-muted mb-4">Promedio de ventas por mes</p>
          <div className="h-64">
            <ChartContainer>
              <BarChart data={monthlyPattern}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`} />
                <Tooltip formatter={(value) => formatCurrency(Number(value) || 0)} />
                <Bar dataKey="avg" name="Promedio" fill="#8b5cf6" radius={[4, 4, 0, 0]}>
                  {monthlyPattern.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.avg > 100000 ? '#22c55e' : entry.avg > 50000 ? '#3b82f6' : '#d1d5db'} />
                  ))}
                </Bar>
              </BarChart>
            </ChartContainer>
          </div>
          <div className="mt-4 p-4 bg-green-50 rounded-xl">
            <p className="text-sm text-green-800">
              <span className="font-medium">Mejor mes:</span> Marzo (${formatNumber(Math.max(...Object.values(cycles.monthly_pattern) as number[]))})
            </p>
          </div>
        </div>
      </div>

      {/* Analisis Pareto 80/20 */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card mb-8">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-foreground">Analisis Pareto 80/20</h3>
            <p className="text-sm text-muted">Los productos que generan el 80% del revenue (costo estimado: 60%)</p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-blue-600">{pareto.summary.products_80_count} productos</p>
            <p className="text-sm text-muted">de {pareto.summary.total_products} generan el 80%</p>
          </div>
        </div>
        <div className="h-80">
          <ChartContainer>
            <ComposedChart data={paretoData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{ fontSize: 9 }} height={60} />
              <YAxis yAxisId="left" tick={{ fontSize: 10 }} tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`} />
              <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 10 }} tickFormatter={(value) => `${value}%`} domain={[0, 100]} />
              <Tooltip
                formatter={(value, name) =>
                  name === 'cumulative' ? `${(Number(value) || 0).toFixed(1)}%` : formatCurrency(Number(value) || 0)
                }
                labelFormatter={(label, payload) => payload?.[0]?.payload?.fullName || label}
              />
              <ReferenceLine yAxisId="right" y={80} stroke="#ef4444" strokeDasharray="3 3" label={{ value: '80%', fontSize: 10, fill: '#ef4444' }} />
              <Bar yAxisId="left" dataKey="revenue" name="Revenue">
                {paretoData.map((entry: { is80: boolean }, index: number) => (
                  <Cell key={`cell-${index}`} fill={entry.is80 ? '#3b82f6' : '#d1d5db'} />
                ))}
              </Bar>
              <Line yAxisId="right" type="monotone" dataKey="cumulative" stroke="#ef4444" strokeWidth={2} dot name="% Acumulado" />
            </ComposedChart>
          </ChartContainer>
        </div>
      </div>

      {/* KPIs Pareto */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6">
          <p className="text-sm text-blue-600 mb-1">Top 1 Producto</p>
          <p className="text-3xl font-bold text-blue-900">{pareto.summary.top_1_pct.toFixed(0)}%</p>
          <p className="text-xs text-blue-700 mt-1">del revenue total</p>
        </div>
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6">
          <p className="text-sm text-green-600 mb-1">Top 3 Productos</p>
          <p className="text-3xl font-bold text-green-900">{pareto.summary.top_3_pct.toFixed(0)}%</p>
          <p className="text-xs text-green-700 mt-1">del revenue total</p>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6">
          <p className="text-sm text-purple-600 mb-1">Margen Estimado</p>
          <p className="text-3xl font-bold text-purple-900">{formatCurrency(pareto.summary.total_margin)}</p>
          <p className="text-xs text-purple-700 mt-1">40% sobre ventas</p>
        </div>
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-6">
          <p className="text-sm text-orange-600 mb-1">Concentracion HHI</p>
          <p className="text-3xl font-bold text-orange-900">{pareto.summary.hhi.toFixed(0)}</p>
          <p className="text-xs text-orange-700 mt-1">{pareto.summary.concentration}</p>
        </div>
      </div>

      {/* Tabla de productos 80% */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
        <h3 className="text-lg font-semibold text-foreground mb-4">Productos que Generan el 80% del Revenue</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-sm font-medium text-muted">#</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted">Producto</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Unidades</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Revenue</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">% Individual</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">% Acumulado</th>
              </tr>
            </thead>
            <tbody>
              {pareto.products.slice(0, 8).map((p: { rank: number; name: string; quantity: number; revenue: number; revenue_pct: number; cumulative_pct: number }) => (
                <tr key={p.rank} className="border-b border-gray-50 hover:bg-blue-50">
                  <td className="py-3 px-4 text-sm font-bold text-blue-600">{p.rank}</td>
                  <td className="py-3 px-4 text-sm text-foreground">{p.name.slice(0, 45)}</td>
                  <td className="py-3 px-4 text-sm text-foreground text-right">{p.quantity}</td>
                  <td className="py-3 px-4 text-sm text-foreground text-right font-semibold">{formatCurrency(p.revenue)}</td>
                  <td className="py-3 px-4 text-sm text-foreground text-right">{p.revenue_pct.toFixed(1)}%</td>
                  <td className="py-3 px-4 text-sm text-right">
                    <span className={`font-semibold ${p.cumulative_pct <= 80 ? 'text-blue-600' : 'text-gray-400'}`}>
                      {p.cumulative_pct.toFixed(1)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

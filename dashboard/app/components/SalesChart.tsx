'use client'

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'
import { formatCurrency } from '@/app/lib/utils'
import { ChartContainer } from './ChartContainer'

interface SalesChartProps {
  data: Array<{
    date: string
    actual: number
    sma_7?: number
  }>
  forecasts?: Array<{
    date: string
    forecast: number
    lower_bound: number
    upper_bound: number
  }>
}

// Agrupar datos por semana
function groupByWeek(data: Array<{ date: string; actual: number; sma_7?: number }>) {
  const weeks: Record<string, { total: number; count: number; weekLabel: string }> = {}

  data.forEach(d => {
    const date = new Date(d.date)
    const year = date.getFullYear()
    const weekNum = Math.ceil((((date.getTime() - new Date(year, 0, 1).getTime()) / 86400000) + new Date(year, 0, 1).getDay() + 1) / 7)
    const weekKey = `${year}-W${weekNum.toString().padStart(2, '0')}`
    const weekLabel = `${d.date.slice(5, 10)}`

    if (!weeks[weekKey]) {
      weeks[weekKey] = { total: 0, count: 0, weekLabel }
    }
    weeks[weekKey].total += d.actual
    weeks[weekKey].count += 1
  })

  return Object.entries(weeks)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([week, data]) => ({
      week: data.weekLabel,
      weekKey: week,
      sales: data.total
    }))
}

export function SalesChart({ data, forecasts }: SalesChartProps) {
  // Agrupar por semana y tomar ultimas 20 semanas
  const weeklyData = groupByWeek(data).slice(-20)

  // Agrupar forecasts por semana (cada 7 dias)
  const weeklyForecasts = forecasts ?
    forecasts.reduce((acc: Array<{ week: string; forecast: number }>, f, i) => {
      if (i % 7 === 0) {
        const weekTotal = forecasts.slice(i, i + 7).reduce((sum, x) => sum + x.forecast, 0)
        acc.push({ week: f.date.slice(5, 10), forecast: weekTotal })
      }
      return acc
    }, []).slice(0, 4) : []

  const chartData = [
    ...weeklyData.map(d => ({
      date: d.week,
      sales: d.sales
    })),
    ...weeklyForecasts.map(f => ({
      date: f.week,
      forecast: f.forecast
    }))
  ]

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold mb-1">Ventas Semanales</h3>
      <p className="text-sm text-muted mb-4">Ultimas 20 semanas + proyeccion 4 semanas</p>
      <div className="h-80">
        <ChartContainer>
          <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 11 }}
              stroke="#9ca3af"
              tickLine={false}
              interval={1}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              stroke="#9ca3af"
              tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              formatter={(value) => [formatCurrency(Number(value) || 0), '']}
              contentStyle={{
                borderRadius: '12px',
                border: 'none',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
              }}
            />
            <Legend />
            <Area
              type="monotone"
              dataKey="sales"
              stroke="#3b82f6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorActual)"
              name="Ventas Semanales"
            />
            <Area
              type="monotone"
              dataKey="forecast"
              stroke="#22c55e"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorForecast)"
              name="Proyeccion Semanal"
            />
          </AreaChart>
        </ChartContainer>
      </div>
    </div>
  )
}

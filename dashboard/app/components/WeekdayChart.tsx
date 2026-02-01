'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts'
import { formatCurrency } from '@/app/lib/utils'
import { ChartContainer } from './ChartContainer'

interface WeekdayChartProps {
  data: Array<{
    day: string
    day_index: number
    revenue: number
  }>
}

const COLORS = ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', '#22c55e', '#86efac']

export function WeekdayChart({ data }: WeekdayChartProps) {
  const chartData = data.map(d => ({
    ...d,
    dayShort: d.day.slice(0, 3)
  }))

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold mb-4">Ventas por Dia de la Semana</h3>
      <div className="h-64">
        <ChartContainer>
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
            <XAxis
              dataKey="dayShort"
              tick={{ fontSize: 12 }}
              stroke="#9ca3af"
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              stroke="#9ca3af"
              tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              formatter={(value: number | string) => [formatCurrency(Number(value) || 0), 'Ventas']}
              contentStyle={{
                borderRadius: '12px',
                border: 'none',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
              }}
            />
            <Bar dataKey="revenue" radius={[8, 8, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ChartContainer>
      </div>
    </div>
  )
}

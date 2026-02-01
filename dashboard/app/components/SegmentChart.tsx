'use client'

import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts'
import { formatCurrency, formatNumber } from '@/app/lib/utils'
import { ChartContainer } from './ChartContainer'

interface SegmentChartProps {
  segments: Array<{
    segment: string
    count: number
    percentage: number
    revenue: number
  }>
}

const COLORS = {
  'Champions': '#22c55e',
  'Loyal': '#3b82f6',
  'Potential': '#f59e0b',
  'At Risk': '#f97316',
  'Lost': '#ef4444'
}

export function SegmentChart({ segments }: SegmentChartProps) {
  const data = segments.map(s => ({
    name: s.segment,
    value: s.count,
    revenue: s.revenue,
    percentage: s.percentage
  }))

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold mb-4">Segmentacion de Clientes (RFM)</h3>
      <div className="h-64">
        <ChartContainer>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={2}
              dataKey="value"
            >
              {data.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={COLORS[entry.name as keyof typeof COLORS]}
                  stroke="none"
                />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number | string, name: string | number, props: { payload?: { revenue?: number } }) => [
                `${formatNumber(Number(value) || 0)} clientes - ${formatCurrency(props?.payload?.revenue || 0)}`,
                String(name)
              ]}
              contentStyle={{
                borderRadius: '12px',
                border: 'none',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
              }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => <span className="text-sm text-gray-600">{value}</span>}
            />
          </PieChart>
        </ChartContainer>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2">
        {segments.slice(0, 4).map(seg => (
          <div key={seg.segment} className="flex items-center gap-2 text-sm">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: COLORS[seg.segment as keyof typeof COLORS] }}
            />
            <span className="text-muted">{seg.segment}:</span>
            <span className="font-semibold">{seg.count}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

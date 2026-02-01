'use client'

import { formatCurrency } from '@/app/lib/utils'

interface ProvinceChartProps {
  data: Array<{
    province: string
    revenue: number
  }>
}

export function ProvinceChart({ data }: ProvinceChartProps) {
  const maxRevenue = Math.max(...data.map(d => d.revenue))

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold mb-4">Ventas por Provincia</h3>
      <div className="space-y-3">
        {data.slice(0, 8).map((item, index) => (
          <div key={item.province} className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted">{item.province}</span>
              <span className="font-semibold">{formatCurrency(item.revenue)}</span>
            </div>
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${(item.revenue / maxRevenue) * 100}%`,
                  backgroundColor: `hsl(${220 - index * 15}, 70%, ${50 + index * 5}%)`
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

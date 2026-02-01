'use client'

import { formatCurrency, formatNumber } from '@/app/lib/utils'

interface TopProductsProps {
  products: Array<{
    id: number
    name: string
    revenue: number
    quantity: number
  }>
}

export function TopProducts({ products }: TopProductsProps) {
  const maxRevenue = Math.max(...products.map(p => p.revenue))

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold mb-4">Top Productos</h3>
      <div className="space-y-4">
        {products.slice(0, 8).map((product, index) => (
          <div key={product.id} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-blue-500/20 text-blue-500 text-xs font-bold">
                  {index + 1}
                </span>
                <span className="text-sm font-medium truncate max-w-[180px]">
                  {product.name}
                </span>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold">{formatCurrency(product.revenue)}</p>
                <p className="text-xs text-muted">{formatNumber(product.quantity)} uds</p>
              </div>
            </div>
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-blue-400 rounded-full transition-all duration-500"
                style={{ width: `${(product.revenue / maxRevenue) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

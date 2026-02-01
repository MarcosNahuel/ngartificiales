'use client'

import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Users, Package } from 'lucide-react'
import { cn, formatCurrency, formatNumber } from '@/app/lib/utils'

interface KPICardProps {
  title: string
  value: number
  change?: number
  type: 'currency' | 'number' | 'percent'
  icon: 'revenue' | 'orders' | 'customers' | 'products'
}

const icons = {
  revenue: DollarSign,
  orders: ShoppingCart,
  customers: Users,
  products: Package
}

const colors = {
  revenue: 'bg-blue-500',
  orders: 'bg-green-500',
  customers: 'bg-purple-500',
  products: 'bg-orange-500'
}

export function KPICard({ title, value, change, type, icon }: KPICardProps) {
  const Icon = icons[icon]
  const isPositive = change !== undefined && change >= 0

  const formattedValue = type === 'currency'
    ? formatCurrency(value)
    : type === 'percent'
    ? `${value.toFixed(1)}%`
    : formatNumber(value)

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className={cn("p-3 rounded-xl", colors[icon])}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {change !== undefined && (
          <div className={cn(
            "flex items-center gap-1 text-sm font-medium px-2.5 py-1 rounded-full",
            isPositive ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"
          )}>
            {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            {Math.abs(change).toFixed(1)}%
          </div>
        )}
      </div>
      <div className="space-y-1">
        <p className="text-2xl font-bold">{formattedValue}</p>
        <p className="text-muted text-sm">{title}</p>
      </div>
    </div>
  )
}

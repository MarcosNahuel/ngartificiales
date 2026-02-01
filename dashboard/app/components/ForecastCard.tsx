'use client'

import { TrendingUp, Target, Calendar, ArrowUpRight } from 'lucide-react'
import { formatCurrency } from '@/app/lib/utils'

interface ForecastCardProps {
  summary: {
    daily_avg: number
    forecast_30d_total: number
    monthly_projection: number
    quarterly_projection: number
    trend_percentage: number
  }
}

export function ForecastCard({ summary }: ForecastCardProps) {
  const isPositive = summary.trend_percentage >= 0

  return (
    <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-6 text-white">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="w-5 h-5" />
        <h3 className="text-lg font-semibold">Proyeccion de Ventas</h3>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white/10 rounded-xl p-4">
          <div className="flex items-center gap-2 text-blue-200 text-sm mb-1">
            <Calendar className="w-4 h-4" />
            <span>Proximo Mes</span>
          </div>
          <p className="text-2xl font-bold">{formatCurrency(summary.monthly_projection)}</p>
        </div>
        <div className="bg-white/10 rounded-xl p-4">
          <div className="flex items-center gap-2 text-blue-200 text-sm mb-1">
            <Target className="w-4 h-4" />
            <span>Trimestre</span>
          </div>
          <p className="text-2xl font-bold">{formatCurrency(summary.quarterly_projection)}</p>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-white/20">
        <div>
          <p className="text-sm text-blue-200">Tendencia</p>
          <div className="flex items-center gap-1">
            <ArrowUpRight className={`w-4 h-4 ${isPositive ? 'text-green-400' : 'text-red-400 rotate-90'}`} />
            <span className={`font-semibold ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
              {isPositive ? '+' : ''}{summary.trend_percentage.toFixed(1)}%
            </span>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-blue-200">Promedio Diario</p>
          <p className="font-semibold">{formatCurrency(summary.daily_avg)}</p>
        </div>
      </div>
    </div>
  )
}

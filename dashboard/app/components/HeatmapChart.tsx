'use client'

import { useState, useEffect } from 'react'

interface HeatmapChartProps {
  hourlyData: Array<{ hour: number; orders: number }>
  weekdayData: Array<{ day: string; day_index: number; revenue: number }>
}

const DAYS = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
const HOURS = Array.from({ length: 24 }, (_, i) => i)

function getColor(value: number, max: number): string {
  if (value === 0) return 'bg-gray-100'
  const intensity = value / max
  if (intensity > 0.8) return 'bg-blue-600'
  if (intensity > 0.6) return 'bg-blue-500'
  if (intensity > 0.4) return 'bg-blue-400'
  if (intensity > 0.2) return 'bg-blue-300'
  return 'bg-blue-200'
}

export function HeatmapChart({ hourlyData, weekdayData }: HeatmapChartProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // Crear matriz de datos día x hora
  // Distribuir órdenes proporcionalmente basado en patrones de día y hora
  const totalRevenue = weekdayData.reduce((sum, d) => sum + d.revenue, 0)
  const totalOrders = hourlyData.reduce((sum, h) => sum + h.orders, 0)

  const hourlyMap = new Map(hourlyData.map(h => [h.hour, h.orders]))
  const weekdayWeights = weekdayData.map(d => d.revenue / totalRevenue)

  // Generar matriz combinada
  const matrix: number[][] = DAYS.map((_, dayIndex) => {
    return HOURS.map(hour => {
      const hourOrders = hourlyMap.get(hour) || 0
      const dayWeight = weekdayWeights[dayIndex] || 1/7
      // Aproximar órdenes para este día/hora
      return Math.round(hourOrders * dayWeight * 10) / 10
    })
  })

  // Encontrar máximo para escala de color
  const maxValue = Math.max(...matrix.flat())

  if (!mounted) {
    return <div className="h-80" />
  }

  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold text-foreground mb-2">Mapa de Calor - Horas Pico</h3>
      <p className="text-sm text-muted mb-4">Distribución de actividad por día y hora</p>

      <div className="overflow-x-auto">
        <div className="min-w-[600px]">
          {/* Header con horas */}
          <div className="flex">
            <div className="w-12 shrink-0" />
            {HOURS.filter(h => h % 2 === 0).map(hour => (
              <div key={hour} className="flex-1 text-center text-xs text-muted">
                {hour}h
              </div>
            ))}
          </div>

          {/* Filas por día */}
          {DAYS.map((day, dayIndex) => (
            <div key={day} className="flex items-center gap-0.5 mb-0.5">
              <div className="w-12 shrink-0 text-xs font-medium text-muted">{day}</div>
              {HOURS.map(hour => {
                const value = matrix[dayIndex][hour]
                return (
                  <div
                    key={hour}
                    className={`flex-1 h-6 rounded-sm ${getColor(value, maxValue)} transition-colors hover:ring-2 hover:ring-blue-400 cursor-pointer`}
                    title={`${day} ${hour}:00 - ${value.toFixed(1)} órdenes`}
                  />
                )
              })}
            </div>
          ))}

          {/* Leyenda */}
          <div className="flex items-center justify-end gap-2 mt-4">
            <span className="text-xs text-muted">Menos</span>
            <div className="flex gap-0.5">
              <div className="w-4 h-4 rounded-sm bg-gray-100" />
              <div className="w-4 h-4 rounded-sm bg-blue-200" />
              <div className="w-4 h-4 rounded-sm bg-blue-300" />
              <div className="w-4 h-4 rounded-sm bg-blue-400" />
              <div className="w-4 h-4 rounded-sm bg-blue-500" />
              <div className="w-4 h-4 rounded-sm bg-blue-600" />
            </div>
            <span className="text-xs text-muted">Más</span>
          </div>
        </div>
      </div>
    </div>
  )
}

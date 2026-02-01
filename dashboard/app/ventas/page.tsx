'use client'

import { Header } from '../components/Header'
import { SalesChart } from '../components/SalesChart'
import { WeekdayChart } from '../components/WeekdayChart'
import { PaymentMethods } from '../components/PaymentMethods'
import { HeatmapChart } from '../components/HeatmapChart'
import { formatCurrency } from '../lib/utils'
import data from '../../public/data.json'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { ChartContainer } from '../components/ChartContainer'

export default function VentasPage() {
  const { descriptive, forecasting } = data

  const monthlyData = descriptive.monthly_sales?.map((m: { month: string; revenue: number; orders: number }) => ({
    month: m.month.slice(2),
    revenue: m.revenue,
    orders: m.orders
  })) || []

  return (
    <div>
      <Header
        title="Analisis de Ventas"
        subtitle="Detalle completo de ventas y metricas"
      />

      {/* Metricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Ingresos Totales</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(descriptive.kpis.total_revenue)}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Total Ordenes</p>
          <p className="text-2xl font-bold text-foreground">{descriptive.kpis.total_orders}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Ticket Promedio</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(descriptive.kpis.avg_ticket)}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Tendencia</p>
          <p className="text-2xl font-bold text-green-600">
            +{forecasting.summary?.trend_percentage?.toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Ventas por mes */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card mb-8">
        <h3 className="text-lg font-semibold text-foreground mb-4">Ventas Mensuales</h3>
        <div className="h-80">
          <ChartContainer>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} stroke="#9ca3af" />
              <YAxis
                tick={{ fontSize: 12 }}
                stroke="#9ca3af"
                tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`}
              />
              <Tooltip
                formatter={(value: number | string) => [formatCurrency(Number(value) || 0), 'Ventas']}
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              />
              <Bar dataKey="revenue" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ChartContainer>
        </div>
      </div>

      {/* Graficos secundarios */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <SalesChart data={forecasting.historical || []} forecasts={forecasting.forecasts} />
        <WeekdayChart data={descriptive.weekday_sales || []} />
      </div>

      {/* Heatmap de horas pico */}
      <div className="mb-8">
        <HeatmapChart
          hourlyData={descriptive.hourly_distribution || []}
          weekdayData={descriptive.weekday_sales || []}
        />
      </div>

      {/* Metodos de pago */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PaymentMethods data={descriptive.payment_methods || []} />
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Resumen por Hora</h3>
          <div className="space-y-3">
            {descriptive.hourly_distribution?.slice(0, 10).map((h: { hour: number; orders: number }) => (
              <div key={h.hour} className="flex items-center gap-4">
                <span className="text-sm font-medium text-muted w-20">{h.hour}:00 hs</span>
                <div className="flex-1 h-4 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full"
                    style={{ width: `${(h.orders / Math.max(...descriptive.hourly_distribution.map((x: { orders: number }) => x.orders))) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold text-foreground">{h.orders}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

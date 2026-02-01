'use client'

import { Header } from '../components/Header'
import { SegmentChart } from '../components/SegmentChart'
import { ProvinceChart } from '../components/ProvinceChart'
import { formatCurrency, formatNumber } from '../lib/utils'
import data from '../../public/data.json'

export default function ClientesPage() {
  const { descriptive, segmentation } = data

  return (
    <div>
      <Header
        title="Analisis de Clientes"
        subtitle="Segmentacion RFM y metricas de clientes"
      />

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Total Clientes</p>
          <p className="text-2xl font-bold text-foreground">{segmentation.metrics?.total_customers || 0}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Ticket Promedio</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(segmentation.metrics?.avg_ticket || 0)}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Frecuencia Promedio</p>
          <p className="text-2xl font-bold text-foreground">{(segmentation.metrics?.avg_frequency || 0).toFixed(1)} ordenes</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">LTV Estimado</p>
          <p className="text-2xl font-bold text-green-600">{formatCurrency(segmentation.metrics?.estimated_ltv || 0)}</p>
        </div>
      </div>

      {/* Graficos principales */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <SegmentChart segments={segmentation.segments || []} />
        <ProvinceChart data={descriptive.province_sales || []} />
      </div>

      {/* Detalle de segmentos */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card mb-8">
        <h3 className="text-lg font-semibold text-foreground mb-4">Detalle de Segmentacion RFM</h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {segmentation.segments?.map((seg: { segment: string; count: number; percentage: number; revenue: number }) => {
            const colors: Record<string, string> = {
              'Champions': 'bg-green-500',
              'Loyal': 'bg-blue-500',
              'Potential': 'bg-yellow-500',
              'At Risk': 'bg-orange-500',
              'Lost': 'bg-red-500'
            }
            return (
              <div key={seg.segment} className="bg-gray-50 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-3">
                  <div className={`w-3 h-3 rounded-full ${colors[seg.segment]}`} />
                  <span className="font-semibold text-foreground">{seg.segment}</span>
                </div>
                <div className="space-y-1 text-sm">
                  <p className="text-muted">Clientes: <span className="font-semibold text-foreground">{seg.count}</span></p>
                  <p className="text-muted">Porcentaje: <span className="font-semibold text-foreground">{seg.percentage.toFixed(1)}%</span></p>
                  <p className="text-muted">Revenue: <span className="font-semibold text-foreground">{formatCurrency(seg.revenue)}</span></p>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Tabla de clientes top */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
        <h3 className="text-lg font-semibold text-foreground mb-4">Top Clientes por Valor</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-sm font-medium text-muted">Cliente ID</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Recencia (dias)</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Frecuencia</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Valor Total</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted">Segmento</th>
              </tr>
            </thead>
            <tbody>
              {segmentation.customer_details?.slice(0, 10).map((c: { customer_id: number; recency: number; frequency: number; monetary: number; segment: string }) => {
                const segColors: Record<string, string> = {
                  'Champions': 'bg-green-100 text-green-700',
                  'Loyal': 'bg-blue-100 text-blue-700',
                  'Potential': 'bg-yellow-100 text-yellow-700',
                  'At Risk': 'bg-orange-100 text-orange-700',
                  'Lost': 'bg-red-100 text-red-700'
                }
                return (
                  <tr key={c.customer_id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm text-foreground">#{c.customer_id}</td>
                    <td className="py-3 px-4 text-sm text-foreground text-right">{c.recency}</td>
                    <td className="py-3 px-4 text-sm text-foreground text-right">{c.frequency}</td>
                    <td className="py-3 px-4 text-sm text-foreground text-right">{formatCurrency(c.monetary)}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${segColors[c.segment]}`}>
                        {c.segment}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

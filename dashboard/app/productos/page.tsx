'use client'

import { Header } from '../components/Header'
import { TopProducts } from '../components/TopProducts'
import { formatCurrency, formatNumber } from '../lib/utils'
import data from '../../public/data.json'
import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts'
import { ChartContainer } from '../components/ChartContainer'

export default function ProductosPage() {
  const { descriptive, products } = data

  // Agrupar por categoria
  const categoryData = descriptive.top_products?.reduce((acc: Record<string, number>, p: { name: string; revenue: number }) => {
    const category = p.name.includes('Combo') ? 'Combos' :
                     p.name.includes('Mojarra') ? 'Mojarra' :
                     p.name.includes('Extreme') ? 'Extreme' :
                     p.name.includes('Termo') ? 'Termicos' :
                     p.name.includes('Canibal') ? 'Canibal' :
                     p.name.includes('Tabano') ? 'Tabano' : 'Otros'
    acc[category] = (acc[category] || 0) + p.revenue
    return acc
  }, {}) || {}

  const pieData = Object.entries(categoryData).map(([name, value]) => ({ name, value }))
  const COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#6366f1']

  return (
    <div>
      <Header
        title="Analisis de Productos"
        subtitle="Performance y metricas de productos"
      />

      {/* KPIs de productos */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Total Productos</p>
          <p className="text-2xl font-bold text-foreground">{products?.length || 0}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Productos Vendidos</p>
          <p className="text-2xl font-bold text-foreground">
            {descriptive.top_products?.reduce((sum: number, p: { quantity: number }) => sum + p.quantity, 0) || 0}
          </p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Top Producto</p>
          <p className="text-lg font-bold text-foreground truncate">
            {descriptive.top_products?.[0]?.name?.slice(0, 20) || 'N/A'}
          </p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Ingresos Top 10</p>
          <p className="text-2xl font-bold text-foreground">
            {formatCurrency(descriptive.top_products?.reduce((sum: number, p: { revenue: number }) => sum + p.revenue, 0) || 0)}
          </p>
        </div>
      </div>

      {/* Graficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <TopProducts products={descriptive.top_products || []} />

        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Ventas por Categoria</h3>
          <div className="h-72">
            <ChartContainer>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                >
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number | string) => formatCurrency(Number(value) || 0)} />
                <Legend />
              </PieChart>
            </ChartContainer>
          </div>
        </div>
      </div>

      {/* Tabla de productos */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
        <h3 className="text-lg font-semibold text-foreground mb-4">Catalogo de Productos</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-sm font-medium text-muted">Producto</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Precio</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Stock</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted">Variantes</th>
              </tr>
            </thead>
            <tbody>
              {products?.slice(0, 15).map((p: { id: number; name: string; price: number; stock: number; variants: number }) => (
                <tr key={p.id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-3 px-4 text-sm text-foreground">{p.name?.slice(0, 40)}</td>
                  <td className="py-3 px-4 text-sm text-foreground text-right">{formatCurrency(p.price)}</td>
                  <td className="py-3 px-4 text-sm text-foreground text-right">{formatNumber(p.stock)}</td>
                  <td className="py-3 px-4 text-sm text-foreground text-right">{p.variants}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

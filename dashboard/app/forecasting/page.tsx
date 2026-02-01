'use client'

import { Header } from '../components/Header'
import { ForecastCard } from '../components/ForecastCard'
import { SalesChart } from '../components/SalesChart'
import { formatCurrency } from '../lib/utils'
import data from '../../public/data.json'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Area, AreaChart } from 'recharts'
import { ChartContainer } from '../components/ChartContainer'

export default function ForecastingPage() {
  const { forecasting, regression } = data

  const forecastData = forecasting.forecasts?.map((f: { date: string; forecast: number; lower_bound: number; upper_bound: number }) => ({
    date: f.date.slice(5),
    forecast: f.forecast,
    lower: f.lower_bound,
    upper: f.upper_bound
  })) || []

  const regressionData = regression.daily_data?.map((d: { date: string; actual: number; predicted: number }) => ({
    date: d.date.slice(5),
    actual: d.actual,
    predicted: d.predicted
  })) || []

  return (
    <div>
      <Header
        title="Forecasting y Predicciones"
        subtitle="Proyecciones de ventas basadas en ML y regresion"
      />

      {/* KPIs de forecasting */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Proyeccion 30 dias</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(forecasting.summary?.forecast_30d_total || 0)}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Promedio Diario</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(forecasting.summary?.forecast_30d_avg || 0)}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Proyeccion Trimestral</p>
          <p className="text-2xl font-bold text-foreground">{formatCurrency(forecasting.summary?.quarterly_projection || 0)}</p>
        </div>
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <p className="text-sm text-muted mb-1">Tendencia</p>
          <p className={`text-2xl font-bold ${(forecasting.summary?.trend_percentage || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {forecasting.summary?.trend_percentage >= 0 ? '+' : ''}{forecasting.summary?.trend_percentage?.toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Grafico de forecast principal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <SalesChart data={forecasting.historical || []} forecasts={forecasting.forecasts} />
        </div>
        <ForecastCard summary={forecasting.summary} />
      </div>

      {/* Predicciones detalladas */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card mb-8">
        <h3 className="text-lg font-semibold text-foreground mb-4">Prediccion Proximos 30 Dias (con Bandas de Confianza)</h3>
        <div className="h-80">
          <ChartContainer>
            <AreaChart data={forecastData}>
              <defs>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="#9ca3af" />
              <YAxis
                tick={{ fontSize: 11 }}
                stroke="#9ca3af"
                tickFormatter={(value) => `$${(value/1000).toFixed(0)}K`}
              />
              <Tooltip formatter={(value: number | string) => formatCurrency(Number(value) || 0)} />
              <Area type="monotone" dataKey="upper" stroke="none" fill="#bbf7d0" />
              <Area type="monotone" dataKey="lower" stroke="none" fill="#ffffff" />
              <Line type="monotone" dataKey="forecast" stroke="#22c55e" strokeWidth={3} dot={false} />
            </AreaChart>
          </ChartContainer>
        </div>
      </div>

      {/* Regresion */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Modelo de Regresion Lineal</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-xl">
              <span className="text-gray-600">Ecuacion</span>
              <span className="font-mono font-semibold">
                y = {regression.linear_regression?.slope?.toFixed(2)}x + {regression.linear_regression?.intercept?.toFixed(0)}
              </span>
            </div>
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-xl">
              <span className="text-gray-600">R-squared</span>
              <span className="font-semibold">{(regression.linear_regression?.r_squared * 100)?.toFixed(2)}%</span>
            </div>
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-xl">
              <span className="text-gray-600">Tendencia</span>
              <span className={`font-semibold ${regression.linear_regression?.trend === 'growing' ? 'text-green-600' : 'text-red-600'}`}>
                {regression.linear_regression?.trend === 'growing' ? 'CRECIENTE' : 'DECRECIENTE'}
              </span>
            </div>
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-xl">
              <span className="text-gray-600">Cambio Diario</span>
              <span className="font-semibold">{formatCurrency(regression.linear_regression?.daily_change || 0)}/dia</span>
            </div>
          </div>
        </div>

        <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Patron Semanal</h3>
          <div className="space-y-3">
            {forecasting.weekly_pattern?.map((d: { day: string; avg_sales: number }) => {
              const maxSales = Math.max(...(forecasting.weekly_pattern?.map((x: { avg_sales: number }) => x.avg_sales) || [1]))
              return (
                <div key={d.day} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">{d.day}</span>
                    <span className="font-semibold">{formatCurrency(d.avg_sales)}</span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500 rounded-full"
                      style={{ width: `${(d.avg_sales / maxSales) * 100}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Predicciones de regresion */}
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
        <h3 className="text-lg font-semibold text-foreground mb-4">Proyeccion 30 Dias (Regresion)</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6">
            <p className="text-sm text-blue-600 mb-1">Total Proyectado</p>
            <p className="text-3xl font-bold text-blue-900">{formatCurrency(regression.predictions_30d?.total || 0)}</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6">
            <p className="text-sm text-green-600 mb-1">Promedio Diario</p>
            <p className="text-3xl font-bold text-green-900">{formatCurrency(regression.predictions_30d?.daily_avg || 0)}</p>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6">
            <p className="text-sm text-purple-600 mb-1">Confianza del Modelo</p>
            <p className="text-3xl font-bold text-purple-900">{((regression.linear_regression?.r_squared || 0) * 100).toFixed(1)}%</p>
          </div>
        </div>
      </div>
    </div>
  )
}

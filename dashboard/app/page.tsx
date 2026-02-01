import { Header } from './components/Header'
import { KPICard } from './components/KPICard'
import { SalesChart } from './components/SalesChart'
import { TopProducts } from './components/TopProducts'
import { SegmentChart } from './components/SegmentChart'
import { WeekdayChart } from './components/WeekdayChart'
import { ProvinceChart } from './components/ProvinceChart'
import { PaymentMethods } from './components/PaymentMethods'
import { ForecastCard } from './components/ForecastCard'
import data from '../public/data.json'

export default function Dashboard() {
  const { descriptive, forecasting, segmentation } = data

  return (
    <div>
      <Header
        title="Dashboard Principal"
        subtitle={`Ultima actualizacion: ${new Date(data.generated_at).toLocaleDateString('es-AR')}`}
      />

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <KPICard
          title="Ingresos Totales"
          value={descriptive.kpis.total_revenue}
          change={forecasting.summary?.trend_percentage}
          type="currency"
          icon="revenue"
        />
        <KPICard
          title="Total Ordenes"
          value={descriptive.kpis.total_orders}
          type="number"
          icon="orders"
        />
        <KPICard
          title="Ticket Promedio"
          value={descriptive.kpis.avg_ticket}
          type="currency"
          icon="products"
        />
        <KPICard
          title="Clientes Unicos"
          value={descriptive.kpis.unique_customers}
          type="number"
          icon="customers"
        />
      </div>

      {/* Grafico principal + Forecast */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <SalesChart
            data={forecasting.historical || []}
            forecasts={forecasting.forecasts}
          />
        </div>
        <div>
          <ForecastCard summary={forecasting.summary} />
        </div>
      </div>

      {/* Segunda fila */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <TopProducts products={descriptive.top_products || []} />
        <SegmentChart segments={segmentation.segments || []} />
        <WeekdayChart data={descriptive.weekday_sales || []} />
      </div>

      {/* Tercera fila */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ProvinceChart data={descriptive.province_sales || []} />
        <PaymentMethods data={descriptive.payment_methods || []} />
      </div>
    </div>
  )
}

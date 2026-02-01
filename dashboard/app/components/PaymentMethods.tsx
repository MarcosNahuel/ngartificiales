'use client'

import { formatCurrency } from '@/app/lib/utils'
import { CreditCard, Building2, Wallet, Banknote } from 'lucide-react'

interface PaymentMethodsProps {
  data: Array<{
    method: string
    revenue: number
    percentage: number
  }>
}

const icons: Record<string, typeof CreditCard> = {
  'Mercado Pago': Wallet,
  'Transferencia': Building2,
  'Transferencia Bancaria': Building2,
  'Tarjeta': CreditCard,
  'Efectivo': Banknote,
  'A convenir': Wallet
}

const colors: Record<string, string> = {
  'Mercado Pago': 'bg-blue-500',
  'Transferencia': 'bg-green-500',
  'Transferencia Bancaria': 'bg-green-500',
  'Tarjeta': 'bg-purple-500',
  'Efectivo': 'bg-orange-500',
  'A convenir': 'bg-gray-500'
}

export function PaymentMethods({ data }: PaymentMethodsProps) {
  return (
    <div className="bg-card rounded-2xl p-6 shadow-sm border border-card">
      <h3 className="text-lg font-semibold mb-4">Metodos de Pago</h3>
      <div className="space-y-4">
        {data.map((item) => {
          const Icon = icons[item.method] || Wallet
          const color = colors[item.method] || 'bg-gray-500'

          return (
            <div key={item.method} className="flex items-center gap-4">
              <div className={`p-2.5 rounded-xl ${color}`}>
                <Icon className="w-5 h-5 text-white" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium">{item.method}</span>
                  <span className="text-sm font-semibold">{formatCurrency(item.revenue)}</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${color}`}
                    style={{ width: `${item.percentage}%` }}
                  />
                </div>
                <p className="text-xs text-muted mt-1">{item.percentage.toFixed(1)}% del total</p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  ShoppingCart,
  Package,
  Users,
  TrendingUp,
  Settings,
  Fish,
  BarChart3,
  Moon,
  Sun
} from 'lucide-react'
import { cn } from '@/app/lib/utils'
import { useTheme } from './ThemeProvider'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Ventas', href: '/ventas', icon: ShoppingCart },
  { name: 'Productos', href: '/productos', icon: Package },
  { name: 'Clientes', href: '/clientes', icon: Users },
  { name: 'Forecasting', href: '/forecasting', icon: TrendingUp },
  { name: 'Analisis', href: '/analisis', icon: BarChart3 },
]

export function Sidebar() {
  const pathname = usePathname()
  const { theme, toggleTheme } = useTheme()

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-gray-900 text-white flex flex-col z-50">
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-xl">
            <Fish className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg">NG Artificiales</h1>
            <p className="text-xs text-gray-400">Dashboard de Ventas</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-gray-400 hover:text-white hover:bg-gray-800"
              )}
            >
              <item.icon className="w-5 h-5" />
              {item.name}
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t border-gray-800 space-y-1">
        {/* Toggle Dark Mode */}
        <button
          onClick={toggleTheme}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
        >
          {theme === 'dark' ? (
            <>
              <Sun className="w-5 h-5" />
              Modo Claro
            </>
          ) : (
            <>
              <Moon className="w-5 h-5" />
              Modo Oscuro
            </>
          )}
        </button>

        <Link
          href="/settings"
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
        >
          <Settings className="w-5 h-5" />
          Configuracion
        </Link>
      </div>
    </aside>
  )
}

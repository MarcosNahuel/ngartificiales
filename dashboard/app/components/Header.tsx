'use client'

import { Bell, Search, RefreshCw } from 'lucide-react'

interface HeaderProps {
  title: string
  subtitle?: string
}

export function Header({ title, subtitle }: HeaderProps) {
  return (
    <header className="flex items-center justify-between mb-8">
      <div>
        <h1 className="text-2xl font-bold">{title}</h1>
        {subtitle && <p className="text-muted mt-1">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2.5 bg-card rounded-xl border border-card hover:opacity-80 transition-opacity">
          <Search className="w-5 h-5 text-muted" />
        </button>
        <button className="p-2.5 bg-card rounded-xl border border-card hover:opacity-80 transition-opacity">
          <RefreshCw className="w-5 h-5 text-muted" />
        </button>
        <button className="p-2.5 bg-card rounded-xl border border-card hover:opacity-80 transition-opacity relative">
          <Bell className="w-5 h-5 text-muted" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>
      </div>
    </header>
  )
}

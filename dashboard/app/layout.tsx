import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "./components/Sidebar";
import { ThemeProvider } from "./components/ThemeProvider";

export const metadata: Metadata = {
  title: "NG Artificiales - Dashboard de Ventas",
  description: "Dashboard de analisis de ventas para NG Artificiales - Senhuelos de pesca y equipamiento outdoor",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className="antialiased">
        <ThemeProvider>
          <Sidebar />
          <main className="ml-64 min-h-screen p-8 bg-[var(--background)] text-[var(--foreground)]">
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}

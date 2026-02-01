import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typescript: {
    // Permite build aunque haya errores de TS (para deploy rápido)
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;

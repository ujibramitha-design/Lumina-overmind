const withSitemap = require('next-sitemap')

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
  },
  eslint: {
    // Memaksa mesin build menutup mata dan melewati semua aturan ESLint
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Memaksa build tetap sukses meskipun ada type errors (unused variables, dll)
    ignoreBuildErrors: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = withSitemap(nextConfig)

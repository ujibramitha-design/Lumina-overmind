import type { Metadata } from 'next'
import './globals.css'
import { Toaster } from '@/components/ui/toaster'
import { BrandingProvider } from '@/components/BrandingProvider'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { getBrandingConfig } from './config/branding'
import { initPostHog } from '@/lib/posthog'
import { ReactQueryProvider } from '@/lib/react-query-provider'
import { useEffect } from 'react'

// Get dynamic branding configuration
const branding = getBrandingConfig()

export const metadata: Metadata = {
  title: branding.title,
  description: branding.description,
  authors: [{ name: branding.author }],
  icons: {
    icon: branding.faviconUrl || '/favicon.ico',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    initPostHog()
  }, [])

  return (
    <ErrorBoundary>
      <html lang="en" suppressHydrationWarning>
        <body className="font-sans">
          <ReactQueryProvider>
            <BrandingProvider>
              <div className="min-h-screen bg-black text-zinc-100">
                {children}
                <Toaster />
              </div>
            </BrandingProvider>
          </ReactQueryProvider>
        </body>
      </html>
    </ErrorBoundary>
  )
}

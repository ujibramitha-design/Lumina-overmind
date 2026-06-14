import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'
import { locales } from '@/i18n'
import '../globals.css'
import { Toaster } from '@/components/ui/toaster'
import { BrandingProvider } from '@/components/BrandingProvider'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { getBrandingConfig } from '../config/branding'
import { initPostHog } from '@/lib/posthog'
import { ReactQueryProvider } from '@/lib/react-query-provider'

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

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }))
}

export default async function RootLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  // Validate locale
  if (!locales.includes(locale as any)) {
    notFound()
  }

  // Get messages for the locale
  const messages = await getMessages()

  return (
    <html lang={locale} suppressHydrationWarning>
      <body className="font-sans">
        <NextIntlClientProvider messages={messages}>
          <ErrorBoundary>
            <ReactQueryProvider>
              <BrandingProvider>
                <div className="min-h-screen bg-black text-zinc-100">
                  {children}
                  <Toaster />
                </div>
              </BrandingProvider>
            </ReactQueryProvider>
          </ErrorBoundary>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}

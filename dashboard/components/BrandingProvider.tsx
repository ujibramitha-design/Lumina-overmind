'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { getBrandingConfig, type BrandingConfig } from '@/app/config/branding'

interface BrandingContextType {
  branding: BrandingConfig
  updateBranding: (newBranding: Partial<BrandingConfig>) => void
  isWhiteLabel: boolean
}

const BrandingContext = createContext<BrandingContextType | undefined>(undefined)

export function useBranding() {
  const context = useContext(BrandingContext)
  if (!context) {
    throw new Error('useBranding must be used within BrandingProvider')
  }
  return context
}

interface BrandingProviderProps {
  children: React.ReactNode
  initialBranding?: Partial<BrandingConfig>
}

export function BrandingProvider({ children, initialBranding }: BrandingProviderProps) {
  const [branding, setBranding] = useState<BrandingConfig>(() => {
    const config = getBrandingConfig()
    return { ...config, ...initialBranding }
  })

  const updateBranding = (newBranding: Partial<BrandingConfig>) => {
    setBranding(prev => ({ ...prev, ...newBranding }))
  }

  // Apply CSS variables when branding changes
  useEffect(() => {
    const root = document.documentElement

    // Apply branding CSS variables
    root.style.setProperty('--brand-primary', branding.primaryColor)
    root.style.setProperty('--brand-secondary', branding.secondaryColor)
    root.style.setProperty('--brand-accent', branding.accentColor)
    root.style.setProperty('--brand-background', branding.backgroundColor)
    root.style.setProperty('--brand-text', branding.textColor)

    // Apply content variables
    root.style.setProperty('--app-name', `"${branding.appName}"`)
    root.style.setProperty('--company-name', `"${branding.company}"`)
    root.style.setProperty('--tagline', `"${branding.tagline}"`)

    // Update page title
    if (typeof window !== 'undefined') {
      document.title = branding.title
    }

    // Update favicon if provided
    if (branding.faviconUrl && typeof window !== 'undefined') {
      const favicon = document.querySelector('link[rel="icon"]') as HTMLLinkElement
      if (favicon) {
        favicon.href = branding.faviconUrl
      }
    }
  }, [branding])

  const isWhiteLabel = branding.enableWhiteLabel

  return (
    <BrandingContext.Provider value={{ branding, updateBranding, isWhiteLabel }}>{children}</BrandingContext.Provider>
  )
}

// Brand-aware Component HOC
export function withBranding<P extends object>(Component: React.ComponentType<P>) {
  return function BrandingComponent(props: P) {
    const { branding } = useBranding()
    return <Component {...props} branding={branding} />
  }
}

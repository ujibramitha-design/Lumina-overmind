/**
 * WHITE-LABEL BRANDING CONFIGURATION
 * Centralized branding configuration for white-label deployment
 */

export interface BrandingConfig {
  // Application Identity
  appName: string
  company: string
  tagline: string

  // Visual Branding
  primaryColor: string
  secondaryColor: string
  accentColor: string
  backgroundColor: string
  textColor: string

  // Logo & Icons
  logoUrl?: string
  faviconUrl?: string
  iconPack: string

  // Metadata
  title: string
  description: string
  author: string

  // Contact & Support
  supportEmail: string
  supportPhone?: string
  websiteUrl?: string

  // Legal
  copyright: string
  privacyPolicyUrl?: string
  termsOfServiceUrl?: string

  // Feature Flags
  enableWhiteLabel: boolean
  showBranding: boolean
  allowCustomLogo: boolean
}

// Default LUMINA OS Branding
export const defaultBranding: BrandingConfig = {
  appName: 'LUMINA OS',
  company: 'Lumina Technologies',
  tagline: 'AI-Powered Real Estate Intelligence Platform',

  primaryColor: '#ef4444', // Red
  secondaryColor: '#1f2937', // Dark Gray
  accentColor: '#10b981', // Emerald
  backgroundColor: '#000000', // Black
  textColor: '#f3f4f6', // Light Gray

  iconPack: 'lucide-react',

  title: 'LUMINA OS - AI Real Estate Intelligence',
  description: 'Advanced AI-powered real estate lead generation and intelligence platform',
  author: 'Lumina Technologies',

  supportEmail: 'support@lumina.tech',
  websiteUrl: 'https://lumina.devproflow.com',

  copyright: '© 2024 Lumina Technologies. All rights reserved.',

  enableWhiteLabel: false,
  showBranding: true,
  allowCustomLogo: true,
}

// White-Label Client Configurations (Examples)
export const clientBrandingExamples = {
  // Example: Real Estate Agency
  realEstateAgency: {
    ...defaultBranding,
    appName: 'PropIntel Pro',
    company: 'Elite Realty Group',
    tagline: 'Intelligent Property Marketing Platform',

    primaryColor: '#3b82f6', // Blue
    secondaryColor: '#1e40af', // Dark Blue
    accentColor: '#f59e0b', // Amber

    title: 'PropIntel Pro - Real Estate Marketing Platform',
    description: 'AI-powered real estate marketing and lead generation platform',
    author: 'Elite Realty Group',

    supportEmail: 'support@propintel.com',
    websiteUrl: 'https://propintel.com',

    copyright: '© 2024 Elite Realty Group. All rights reserved.',

    enableWhiteLabel: true,
    showBranding: true,
    allowCustomLogo: true,
  },

  // Example: Property Developer
  propertyDeveloper: {
    ...defaultBranding,
    appName: 'DevFlow Intelligence',
    company: 'Urban Development Corp',
    tagline: 'Smart Development Analytics Platform',

    primaryColor: '#8b5cf6', // Purple
    secondaryColor: '#6d28d9', // Dark Purple
    accentColor: '#ec4899', // Pink

    title: 'DevFlow Intelligence - Development Analytics',
    description: 'AI-powered property development analytics and market intelligence',
    author: 'Urban Development Corp',

    supportEmail: 'support@devflow.ai',
    websiteUrl: 'https://devflow.ai',

    copyright: '© 2024 Urban Development Corp. All rights reserved.',

    enableWhiteLabel: true,
    showBranding: true,
    allowCustomLogo: true,
  },

  // Example: Investment Firm
  investmentFirm: {
    ...defaultBranding,
    appName: 'InvestIQ Analytics',
    company: 'Capital Intelligence Partners',
    tagline: 'Real Estate Investment Intelligence Platform',

    primaryColor: '#059669', // Emerald
    secondaryColor: '#047857', // Dark Emerald
    accentColor: '#fbbf24', // Yellow

    title: 'InvestIQ Analytics - Investment Intelligence',
    description: 'AI-powered real estate investment analytics and market intelligence',
    author: 'Capital Intelligence Partners',

    supportEmail: 'support@investiq.ai',
    websiteUrl: 'https://investiq.ai',

    copyright: '© 2024 Capital Intelligence Partners. All rights reserved.',

    enableWhiteLabel: true,
    showBranding: true,
    allowCustomLogo: true,
  },
}

// Dynamic Branding Loader
export function getBrandingConfig(): BrandingConfig {
  // In production, this would load from SystemConfig or environment variables
  // For now, we'll use environment variables with fallback to default

  if (typeof window !== 'undefined') {
    // Client-side: Load from window or API
    const windowBranding = (window as any).__BRANDING_CONFIG__
    if (windowBranding) {
      return windowBranding
    }
  }

  // Server-side or fallback: Check environment variables
  const envBranding: Partial<BrandingConfig> = {
    appName: process.env.NEXT_PUBLIC_APP_NAME || defaultBranding.appName,
    company: process.env.NEXT_PUBLIC_COMPANY_NAME || defaultBranding.company,
    tagline: process.env.NEXT_PUBLIC_TAGLINE || defaultBranding.tagline,

    primaryColor: process.env.NEXT_PUBLIC_PRIMARY_COLOR || defaultBranding.primaryColor,
    secondaryColor: process.env.NEXT_PUBLIC_SECONDARY_COLOR || defaultBranding.secondaryColor,
    accentColor: process.env.NEXT_PUBLIC_ACCENT_COLOR || defaultBranding.accentColor,

    title: process.env.NEXT_PUBLIC_APP_TITLE || defaultBranding.title,
    description: process.env.NEXT_PUBLIC_APP_DESCRIPTION || defaultBranding.description,
    author: process.env.NEXT_PUBLIC_APP_AUTHOR || defaultBranding.author,

    supportEmail: process.env.NEXT_PUBLIC_SUPPORT_EMAIL || defaultBranding.supportEmail,
    websiteUrl: process.env.NEXT_PUBLIC_WEBSITE_URL || defaultBranding.websiteUrl,

    copyright: process.env.NEXT_PUBLIC_COPYRIGHT || defaultBranding.copyright,

    enableWhiteLabel: process.env.NEXT_PUBLIC_ENABLE_WHITE_LABEL === 'true',
    showBranding: process.env.NEXT_PUBLIC_SHOW_BRANDING !== 'false',
    allowCustomLogo: process.env.NEXT_PUBLIC_ALLOW_CUSTOM_LOGO !== 'false',
  }

  return { ...defaultBranding, ...envBranding }
}

// CSS Variables Generator
export function generateCSSVariables(branding: BrandingConfig): string {
  return `
    :root {
      --color-primary: ${branding.primaryColor};
      --color-secondary: ${branding.secondaryColor};
      --color-accent: ${branding.accentColor};
      --color-background: ${branding.backgroundColor};
      --color-text: ${branding.textColor};
      
      --app-name: "${branding.appName}";
      --company-name: "${branding.company}";
      --tagline: "${branding.tagline}";
    }
  `
}

// Tailwind CSS Config Generator
export function generateTailwindConfig(branding: BrandingConfig) {
  return {
    theme: {
      extend: {
        colors: {
          primary: branding.primaryColor,
          secondary: branding.secondaryColor,
          accent: branding.accentColor,
          background: branding.backgroundColor,
          text: branding.textColor,
        },
        fontFamily: {
          brand: ['Inter', 'sans-serif'],
        },
      },
    },
  }
}

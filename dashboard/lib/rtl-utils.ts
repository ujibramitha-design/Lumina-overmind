/**
 * Utilitas untuk RTL (Right-to-Left) support
 * Mendukung bahasa Arab, Hebrew, dan bahasa RTL lainnya
 */

export interface RTLConfig {
  locale: string
  direction: 'ltr' | 'rtl'
  isRTL: boolean
}

// Daftar locale yang menggunakan RTL
export const RTL_LOCALES = [
  'ar', // Arabic
  'he', // Hebrew
  'fa', // Persian (Farsi)
  'ur', // Urdu
  'yi', // Yiddish
  'ps', // Pashto
  'sd', // Sindhi
  'ckb', // Central Kurdish (Sorani)
  'dv', // Divehi
  'ha', // Hausa
  'ks', // Kashmiri
  'ku', // Kurdish
  'ms_Arab', // Malay (Jawi script)
  'pa_Arab', // Punjabi (Shahmukhi script)
  'uz_Arab', // Uzbek (Arabic script)
  'yi' // Yiddish
]

/**
 * Cek apakah locale menggunakan RTL
 * @param locale - Locale code (contoh: 'ar', 'he', 'en')
 * @returns Boolean
 */
export function isRTL(locale: string): boolean {
  return RTL_LOCALES.includes(locale)
}

/**
 * Mendapatkan konfigurasi RTL untuk locale
 * @param locale - Locale code
 * @returns RTL configuration
 */
export function getRTLConfig(locale: string): RTLConfig {
  const isRTLValue = isRTL(locale)
  
  return {
    locale,
    direction: isRTLValue ? 'rtl' : 'ltr',
    isRTL: isRTLValue
  }
}

/**
 * Mengubah direction HTML element
 * @param locale - Locale code
 */
export function setDocumentDirection(locale: string): void {
  if (typeof document !== 'undefined') {
    const config = getRTLConfig(locale)
    document.documentElement.dir = config.direction
    document.documentElement.lang = locale
  }
}

/**
 * Mendapatkan CSS untuk RTL support
 * @param locale - Locale code
 * @returns CSS string
 */
export function getRTLCSS(locale: string): string {
  const config = getRTLConfig(locale)
  
  if (!config.isRTL) {
    return ''
  }
  
  return `
    /* RTL Support */
    [dir="rtl"] {
      direction: rtl;
      text-align: right;
    }
    
    [dir="rtl"] .flex-row {
      flex-direction: row-reverse;
    }
    
    [dir="rtl"] .ml-auto {
      margin-left: auto;
      margin-right: 0;
    }
    
    [dir="rtl"] .mr-auto {
      margin-right: auto;
      margin-left: 0;
    }
    
    [dir="rtl"] .pl-4 {
      padding-left: 0;
      padding-right: 1rem;
    }
    
    [dir="rtl"] .pr-4 {
      padding-right: 0;
      padding-left: 1rem;
    }
    
    [dir="rtl"] .text-left {
      text-align: right;
    }
    
    [dir="rtl"] .text-right {
      text-align: left;
    }
    
    [dir="rtl"] .border-l {
      border-left: none;
      border-right: 1px solid;
    }
    
    [dir="rtl"] .border-r {
      border-right: none;
      border-left: 1px solid;
    }
    
    /* Icon flipping for RTL */
    [dir="rtl"] .icon-flip {
      transform: scaleX(-1);
    }
    
    /* Navigation menu RTL */
    [dir="rtl"] .nav-item {
      margin-right: 0;
      margin-left: 0.5rem;
    }
    
    /* Table RTL */
    [dir="rtl"] table {
      direction: rtl;
    }
    
    [dir="rtl"] th,
    [dir="rtl"] td {
      text-align: right;
    }
    
    /* Form RTL */
    [dir="rtl"] input,
    [dir="rtl"] textarea,
    [dir="rtl"] select {
      text-align: right;
    }
    
    /* Button RTL */
    [dir="rtl"] button {
      text-align: center;
    }
    
    /* Card RTL */
    [dir="rtl"] .card {
      text-align: right;
    }
    
    /* Sidebar RTL */
    [dir="rtl"] .sidebar {
      right: 0;
      left: auto;
    }
    
    /* Pagination RTL */
    [dir="rtl"] .pagination {
      direction: rtl;
    }
  `
}

/**
 * Mendapatkan class Tailwind untuk RTL
 * @param locale - Locale code
 * @returns Tailwind classes
 */
export function getRTLClasses(locale: string): string {
  const config = getRTLConfig(locale)
  
  if (!config.isRTL) {
    return ''
  }
  
  return 'rtl'
}

/**
 * Mengubah icon untuk RTL
 * @param iconName - Nama icon
 * @returns Nama icon yang sudah di-flip (jika perlu)
 */
export function getRTLIcon(iconName: string): string {
  // Icon yang perlu di-flip untuk RTL
  const iconsToFlip = [
    'arrow-left',
    'arrow-right',
    'chevron-left',
    'chevron-right',
    'arrow-back',
    'arrow-forward',
    'arrow-circle-left',
    'arrow-circle-right',
    'skip-back',
    'skip-forward',
    'fast-forward',
    'rewind',
    'first-page',
    'last-page',
    'navigate-before',
    'navigate-next',
    'arrow-ios-back',
    'arrow-ios-forward',
    'arrow-back-ios',
    'arrow-forward-ios'
  ]
  
  if (iconsToFlip.includes(iconName)) {
    return iconName.replace('left', 'right').replace('right', 'left')
      .replace('back', 'forward').replace('forward', 'back')
      .replace('before', 'next').replace('next', 'before')
  }
  
  return iconName
}

/**
 * Mendapatkan font family untuk RTL
 * @param locale - Locale code
 * @returns Font family string
 */
export function getRTLFontFamily(locale: string): string {
  const fontFamilies: Record<string, string> = {
    'ar': 'Noto Sans Arabic, Arial, sans-serif',
    'he': 'Noto Sans Hebrew, Arial, sans-serif',
    'fa': 'Vazirmatn, Arial, sans-serif',
    'ur': 'Noto Nastaliq Urdu, Arial, sans-serif',
    'yi': 'Noto Sans Yiddish, Arial, sans-serif',
    'ps': 'Noto Sans Pashto, Arial, sans-serif',
    'sd': 'Noto Sans Sindhi, Arial, sans-serif',
    'ckb': 'Noto Sans Arabic, Arial, sans-serif',
    'dv': 'Noto Sans Divehi, Arial, sans-serif',
    'ha': 'Noto Sans Hausa, Arial, sans-serif',
    'ks': 'Noto Sans Kashmiri, Arial, sans-serif',
    'ku': 'Noto Sans Arabic, Arial, sans-serif',
    'ms_Arab': 'Noto Sans Arabic, Arial, sans-serif',
    'pa_Arab': 'Noto Sans Arabic, Arial, sans-serif',
    'uz_Arab': 'Noto Sans Arabic, Arial, sans-serif'
  }
  
  return fontFamilies[locale] || 'Inter, Arial, sans-serif'
}

/**
 * Mendapatkan number format untuk RTL
 * @param locale - Locale code
 * @param number - Number untuk format
 * @returns Formatted number string
 */
export function formatNumberRTL(locale: string, number: number): string {
  const config = getRTLConfig(locale)
  
  if (!config.isRTL) {
    return number.toLocaleString('en-US')
  }
  
  // Format number dengan locale RTL
  const rtlLocales: Record<string, string> = {
    'ar': 'ar-SA',
    'he': 'he-IL',
    'fa': 'fa-IR',
    'ur': 'ur-PK',
    'yi': 'yi-US',
    'ps': 'ps-AF',
    'sd': 'sd-PK',
    'ckb': 'ckb-IQ',
    'dv': 'dv-MV',
    'ha': 'ha-NG',
    'ks': 'ks-IN',
    'ku': 'ku-IQ',
    'ms_Arab': 'ms-MY',
    'pa_Arab': 'pa-PK',
    'uz_Arab': 'uz-UZ'
  }
  
  const numberLocale = rtlLocales[locale] || 'ar-SA'
  return number.toLocaleString(numberLocale)
}

/**
 * Mendapatkan currency format untuk RTL
 * @param locale - Locale code
 * @param amount - Amount
 * @param currency - Currency code
 * @returns Formatted currency string
 */
export function formatCurrencyRTL(locale: string, amount: number, currency: string = 'USD'): string {
  const config = getRTLConfig(locale)
  
  if (!config.isRTL) {
    return amount.toLocaleString('en-US', { style: 'currency', currency })
  }
  
  const rtlLocales: Record<string, string> = {
    'ar': 'ar-SA',
    'he': 'he-IL',
    'fa': 'fa-IR',
    'ur': 'ur-PK',
    'yi': 'yi-US',
    'ps': 'ps-AF',
    'sd': 'sd-PK',
    'ckb': 'ckb-IQ',
    'dv': 'dv-MV',
    'ha': 'ha-NG',
    'ks': 'ks-IN',
    'ku': 'ku-IQ',
    'ms_Arab': 'ms-MY',
    'pa_Arab': 'pa-PK',
    'uz_Arab': 'uz-UZ'
  }
  
  const numberLocale = rtlLocales[locale] || 'ar-SA'
  return amount.toLocaleString(numberLocale, { style: 'currency', currency })
}

/**
 * Mendapatkan date format untuk RTL
 * @param locale - Locale code
 * @param date - Date
 * @returns Formatted date string
 */
export function formatDateRTL(locale: string, date: Date): string {
  const config = getRTLConfig(locale)
  
  if (!config.isRTL) {
    return date.toLocaleDateString('en-US')
  }
  
  const rtlLocales: Record<string, string> = {
    'ar': 'ar-SA',
    'he': 'he-IL',
    'fa': 'fa-IR',
    'ur': 'ur-PK',
    'yi': 'yi-US',
    'ps': 'ps-AF',
    'sd': 'sd-PK',
    'ckb': 'ckb-IQ',
    'dv': 'dv-MV',
    'ha': 'ha-NG',
    'ks': 'ks-IN',
    'ku': 'ku-IQ',
    'ms_Arab': 'ms-MY',
    'pa_Arab': 'pa-PK',
    'uz_Arab': 'uz-UZ'
  }
  
  const dateLocale = rtlLocales[locale] || 'ar-SA'
  return date.toLocaleDateString(dateLocale)
}

/**
 * Hook untuk menggunakan RTL di React components
 * @param locale - Locale code
 * @returns RTL utilities
 */
export function useRTL(locale: string) {
  const config = getRTLConfig(locale)
  
  return {
    isRTL: config.isRTL,
    direction: config.direction,
    setDirection: () => setDocumentDirection(locale),
    getIcon: (iconName: string) => getRTLIcon(iconName),
    getFontFamily: () => getRTLFontFamily(locale),
    formatNumber: (number: number) => formatNumberRTL(locale, number),
    formatCurrency: (amount: number, currency?: string) => formatCurrencyRTL(locale, amount, currency),
    formatDate: (date: Date) => formatDateRTL(locale, date)
  }
}

/**
 * Utilitas untuk Multi-Currency Support
 * Mendukung berbagai mata uang Asia dan global
 */

import { format, parseISO } from 'date-fns'

export interface CurrencyInfo {
  code: string
  symbol: string
  name: string
  region: string
  decimalPlaces: number
  thousandsSeparator: string
  decimalSeparator: string
  symbolPosition: 'before' | 'after'
  spaceBetween: boolean
}

export interface ExchangeRate {
  from: string
  to: string
  rate: number
  lastUpdated: Date
}

// Daftar mata uang yang didukung (fokus Asia)
export const SUPPORTED_CURRENCIES: CurrencyInfo[] = [
  {
    code: 'IDR',
    symbol: 'Rp',
    name: 'Indonesian Rupiah',
    region: 'Indonesia',
    decimalPlaces: 0,
    thousandsSeparator: '.',
    decimalSeparator: ',',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'SGD',
    symbol: 'S$',
    name: 'Singapore Dollar',
    region: 'Singapore',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'MYR',
    symbol: 'RM',
    name: 'Malaysian Ringgit',
    region: 'Malaysia',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'THB',
    symbol: '฿',
    name: 'Thai Baht',
    region: 'Thailand',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'VND',
    symbol: '₫',
    name: 'Vietnamese Dong',
    region: 'Vietnam',
    decimalPlaces: 0,
    thousandsSeparator: '.',
    decimalSeparator: ',',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'PHP',
    symbol: '₱',
    name: 'Philippine Peso',
    region: 'Philippines',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'JPY',
    symbol: '¥',
    name: 'Japanese Yen',
    region: 'Japan',
    decimalPlaces: 0,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'KRW',
    symbol: '₩',
    name: 'South Korean Won',
    region: 'South Korea',
    decimalPlaces: 0,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'CNY',
    symbol: '¥',
    name: 'Chinese Yuan',
    region: 'China',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'HKD',
    symbol: 'HK$',
    name: 'Hong Kong Dollar',
    region: 'Hong Kong',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'AED',
    symbol: 'د.إ',
    name: 'UAE Dirham',
    region: 'UAE',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: true
  },
  {
    code: 'SAR',
    symbol: '﷼',
    name: 'Saudi Riyal',
    region: 'Saudi Arabia',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: true
  },
  {
    code: 'INR',
    symbol: '₹',
    name: 'Indian Rupee',
    region: 'India',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'USD',
    symbol: '$',
    name: 'US Dollar',
    region: 'Global',
    decimalPlaces: 2,
    thousandsSeparator: ',',
    decimalSeparator: '.',
    symbolPosition: 'before',
    spaceBetween: false
  },
  {
    code: 'EUR',
    symbol: '€',
    name: 'Euro',
    region: 'Europe',
    decimalPlaces: 2,
    thousandsSeparator: '.',
    decimalSeparator: ',',
    symbolPosition: 'after',
    spaceBetween: false
  }
]

// Mock exchange rates (base: USD)
const MOCK_EXCHANGE_RATES: Record<string, number> = {
  USD: 1.0,
  IDR: 16500.0,
  SGD: 1.35,
  MYR: 4.75,
  THB: 36.5,
  VND: 25400.0,
  PHP: 56.5,
  JPY: 155.0,
  KRW: 1350.0,
  CNY: 7.25,
  HKD: 7.82,
  AED: 3.67,
  SAR: 3.75,
  INR: 83.5,
  EUR: 0.92
}

/**
 * Mendapatkan informasi mata uang
 * @param code - Currency code (contoh: 'IDR', 'USD')
 * @returns Currency info
 */
export function getCurrencyInfo(code: string): CurrencyInfo {
  const currency = SUPPORTED_CURRENCIES.find(c => c.code === code)
  return currency || SUPPORTED_CURRENCIES[0] // Default to IDR
}

/**
 * Mendapatkan mata uang default berdasarkan region
 * @param region - Region (contoh: 'Indonesia', 'Singapore')
 * @returns Currency code
 */
export function getDefaultCurrency(region: string = 'Indonesia'): string {
  const currency = SUPPORTED_CURRENCIES.find(c => c.region === region)
  return currency?.code || 'IDR'
}

/**
 * Format angka ke format mata uang
 * @param amount - Amount
 * @param currencyCode - Currency code
 * @returns Formatted currency string
 */
export function formatCurrency(amount: number, currencyCode: string = 'IDR'): string {
  const info = getCurrencyInfo(currencyCode)
  
  // Round to decimal places
  const roundedAmount = Math.round(amount * Math.pow(10, info.decimalPlaces)) / Math.pow(10, info.decimalPlaces)
  
  // Format number with separators
  const parts = roundedAmount.toFixed(info.decimalPlaces).split('.')
  const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, info.thousandsSeparator)
  const decimalPart = parts[1] || ''
  
  let formatted = integerPart
  if (decimalPart) {
    formatted += info.decimalSeparator + decimalPart
  }
  
  // Add symbol
  if (info.symbolPosition === 'before') {
    formatted = info.symbol + (info.spaceBetween ? ' ' : '') + formatted
  } else {
    formatted = formatted + (info.spaceBetween ? ' ' : '') + info.symbol
  }
  
  return formatted
}

/**
 * Konversi mata uang
 * @param amount - Amount
 * @param fromCurrency - Source currency code
 * @param toCurrency - Target currency code
 * @returns Converted amount
 */
export function convertCurrency(
  amount: number,
  fromCurrency: string,
  toCurrency: string
): number {
  if (fromCurrency === toCurrency) {
    return amount
  }
  
  const fromRate = MOCK_EXCHANGE_RATES[fromCurrency] || 1.0
  const toRate = MOCK_EXCHANGE_RATES[toCurrency] || 1.0
  
  // Convert to USD first, then to target currency
  const amountInUSD = amount / fromRate
  const convertedAmount = amountInUSD * toRate
  
  return convertedAmount
}

/**
 * Mendapatkan exchange rate
 * @param fromCurrency - Source currency code
 * @param toCurrency - Target currency code
 * @returns Exchange rate
 */
export function getExchangeRate(fromCurrency: string, toCurrency: string): ExchangeRate {
  const fromRate = MOCK_EXCHANGE_RATES[fromCurrency] || 1.0
  const toRate = MOCK_EXCHANGE_RATES[toCurrency] || 1.0
  
  const rate = toRate / fromRate
  
  return {
    from: fromCurrency,
    to: toCurrency,
    rate,
    lastUpdated: new Date()
  }
}

/**
 * Parse currency string ke number
 * @param currencyString - Formatted currency string
 * @param currencyCode - Currency code
 * @returns Parsed number
 */
export function parseCurrency(currencyString: string, currencyCode: string = 'IDR'): number {
  const info = getCurrencyInfo(currencyCode)
  
  // Remove symbol and spaces
  let cleanString = currencyString.replace(info.symbol, '').replace(/\s/g, '')
  
  // Replace separators with standard format
  cleanString = cleanString.replace(new RegExp(`\\${info.thousandsSeparator}`, 'g'), '')
  cleanString = cleanString.replace(info.decimalSeparator, '.')
  
  return parseFloat(cleanString) || 0
}

/**
 * Mendapatkan semua mata uang yang didukung
 * @returns Array of currency info
 */
export function getAllCurrencies(): CurrencyInfo[] {
  return SUPPORTED_CURRENCIES
}

/**
 * Mendapatkan mata uang berdasarkan region
 * @param region - Region
 * @returns Array of currency info
 */
export function getCurrenciesByRegion(region: string): CurrencyInfo[] {
  return SUPPORTED_CURRENCIES.filter(c => c.region === region)
}

/**
 * Mendapatkan mata uang populer
 * @returns Array of popular currency codes
 */
export function getPopularCurrencies(): string[] {
  return ['IDR', 'USD', 'SGD', 'MYR', 'THB', 'JPY', 'CNY', 'HKD']
}

/**
 * Format harga dengan currency code
 * @param amount - Amount
 * @param currencyCode - Currency code
 * @param showCode - Show currency code
 * @returns Formatted price string
 */
export function formatPrice(amount: number, currencyCode: string = 'IDR', showCode: boolean = false): string {
  const formatted = formatCurrency(amount, currencyCode)
  
  if (showCode) {
    return `${formatted} ${currencyCode}`
  }
  
  return formatted
}

/**
 * Hitung persentase perubahan harga
 * @param oldPrice - Old price
 * @param newPrice - New price
 * @returns Percentage change
 */
export function calculatePriceChange(oldPrice: number, newPrice: number): number {
  if (oldPrice === 0) return 0
  return ((newPrice - oldPrice) / oldPrice) * 100
}

/**
 * Format persentase perubahan harga
 * @param oldPrice - Old price
 * @param newPrice - New price
 * @param currencyCode - Currency code
 * @returns Formatted price change string
 */
export function formatPriceChange(oldPrice: number, newPrice: number, currencyCode: string = 'IDR'): string {
  const change = calculatePriceChange(oldPrice, newPrice)
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(2)}%`
}

/**
 * Hook untuk menggunakan currency di React components
 * @param currencyCode - Currency code
 * @returns Currency utilities
 */
export function useCurrency(currencyCode: string = 'IDR') {
  const info = getCurrencyInfo(currencyCode)
  
  return {
    info,
    format: (amount: number) => formatCurrency(amount, currencyCode),
    convert: (amount: number, toCurrency: string) => convertCurrency(amount, currencyCode, toCurrency),
    parse: (currencyString: string) => parseCurrency(currencyString, currencyCode),
    getExchangeRate: (toCurrency: string) => getExchangeRate(currencyCode, toCurrency),
    formatPrice: (amount: number, showCode?: boolean) => formatPrice(amount, currencyCode, showCode)
  }
}

// Simplified financial utilities for Indonesian Rupiah
// Using basic number operations to avoid dinero.js API complexity

// Format currency to Indonesian Rupiah
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

// Parse currency string to number
export function parseCurrency(value: string): number {
  const cleanValue = value.replace(/[Rp\s.]/g, '').replace(',', '.')
  return parseFloat(cleanValue) || 0
}

// Add two currency amounts
export function addCurrency(a: number, b: number): number {
  return a + b
}

// Subtract two currency amounts
export function subtractCurrency(a: number, b: number): number {
  return a - b
}

// Multiply currency by percentage
export function multiplyCurrency(amount: number, percentage: number): number {
  return amount * (percentage / 100)
}

// Allocate amount among ratios
export function allocateCurrency(amount: number, ratios: number[]): number[] {
  const total = ratios.reduce((sum, r) => sum + r, 0)
  return ratios.map(r => (amount * r) / total)
}

// Calculate commission
export function calculateCommission(salePrice: number, commissionRate: number): number {
  return multiplyCurrency(salePrice, commissionRate)
}

// Calculate discount
export function calculateDiscount(price: number, discountRate: number): number {
  return multiplyCurrency(price, discountRate)
}

// Calculate final price after discount
export function calculateFinalPrice(price: number, discountRate: number): number {
  const discount = calculateDiscount(price, discountRate)
  return subtractCurrency(price, discount)
}

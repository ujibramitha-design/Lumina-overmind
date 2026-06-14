import { describe, it, expect } from 'vitest'
import {
  formatCurrency,
  parseCurrency,
  addCurrency,
  subtractCurrency,
  multiplyCurrency,
  allocateCurrency,
  calculateCommission,
  calculateDiscount,
  calculateFinalPrice,
} from '../financial-utils'

describe('financial-utils', () => {
  describe('formatCurrency', () => {
    it('should format number to Indonesian Rupiah', () => {
      expect(formatCurrency(1000000)).toBe('Rp1.000.000')
      expect(formatCurrency(5000000)).toBe('Rp5.000.000')
      expect(formatCurrency(0)).toBe('Rp0')
    })

    it('should handle decimal values', () => {
      expect(formatCurrency(1500.5)).toBe('Rp1.501')
    })
  })

  describe('parseCurrency', () => {
    it('should parse currency string to number', () => {
      expect(parseCurrency('Rp1.000.000')).toBe(1000000)
      expect(parseCurrency('Rp5.000.000')).toBe(5000000)
      expect(parseCurrency('1.000.000')).toBe(1000000)
    })

    it('should handle empty string', () => {
      expect(parseCurrency('')).toBe(0)
    })

    it('should handle invalid string', () => {
      expect(parseCurrency('invalid')).toBe(0)
    })
  })

  describe('addCurrency', () => {
    it('should add two currency amounts', () => {
      expect(addCurrency(1000000, 500000)).toBe(1500000)
      expect(addCurrency(0, 0)).toBe(0)
    })
  })

  describe('subtractCurrency', () => {
    it('should subtract two currency amounts', () => {
      expect(subtractCurrency(1000000, 500000)).toBe(500000)
      expect(subtractCurrency(500000, 1000000)).toBe(-500000)
    })
  })

  describe('multiplyCurrency', () => {
    it('should multiply currency by percentage', () => {
      expect(multiplyCurrency(1000000, 10)).toBe(100000)
      expect(multiplyCurrency(500000, 20)).toBe(100000)
    })

    it('should handle 0 percentage', () => {
      expect(multiplyCurrency(1000000, 0)).toBe(0)
    })
  })

  describe('allocateCurrency', () => {
    it('should allocate amount among ratios', () => {
      const result = allocateCurrency(1000000, [1, 1, 1])
      expect(result).toHaveLength(3)
      expect(result[0]).toBeCloseTo(333333.33, 2)
      expect(result[1]).toBeCloseTo(333333.33, 2)
      expect(result[2]).toBeCloseTo(333333.33, 2)
    })

    it('should handle different ratios', () => {
      const result = allocateCurrency(1000000, [2, 1])
      expect(result[0]).toBeCloseTo(666666.67, 2)
      expect(result[1]).toBeCloseTo(333333.33, 2)
    })
  })

  describe('calculateCommission', () => {
    it('should calculate commission from sale price', () => {
      expect(calculateCommission(1000000, 5)).toBe(50000)
      expect(calculateCommission(5000000, 10)).toBe(500000)
    })
  })

  describe('calculateDiscount', () => {
    it('should calculate discount from price', () => {
      expect(calculateDiscount(1000000, 10)).toBe(100000)
      expect(calculateDiscount(500000, 20)).toBe(100000)
    })
  })

  describe('calculateFinalPrice', () => {
    it('should calculate final price after discount', () => {
      expect(calculateFinalPrice(1000000, 10)).toBe(900000)
      expect(calculateFinalPrice(500000, 20)).toBe(400000)
    })

    it('should handle 0 discount', () => {
      expect(calculateFinalPrice(1000000, 0)).toBe(1000000)
    })
  })
})

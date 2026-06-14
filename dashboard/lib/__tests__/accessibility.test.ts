import { describe, it, expect, vi, beforeEach } from 'vitest'
import { runAccessibilityScan, getAccessibilitySummary, checkWCAGCompliance, getAccessibilityRecommendations } from '../accessibility'

// Mock @axe-core/react
vi.mock('@axe-core/react', () => ({
  default: vi.fn()
}))

describe('Accessibility Utilities', () => {
  beforeEach(() => {
    // Mock window object
    Object.defineProperty(global, 'window', {
      value: {
        location: {
          pathname: '/test'
        }
      },
      writable: true
    })
  })

  it('should throw error when runAccessibilityScan is called in non-browser environment', async () => {
    // Mock window as undefined
    Object.defineProperty(global, 'window', {
      value: undefined,
      writable: true
    })

    await expect(runAccessibilityScan()).rejects.toThrow('Accessibility scan hanya bisa dijalankan di browser')
  })

  it('should return accessibility report with violations', async () => {
    const mockAxe = await import('@axe-core/react')
    ;(mockAxe.default as any).mockResolvedValue({
      violations: [
        {
          id: 'color-contrast',
          impact: 'serious',
          description: 'Elements must have sufficient color contrast',
          help: 'Ensure color contrast is at least 4.5:1',
          helpUrl: 'https://dequeuniversity.com/rules/axe/4.9/color-contrast',
          nodes: []
        }
      ],
      passes: [{ id: 'pass-1' }],
      incomplete: [],
      inapplicable: []
    })

    const report = await runAccessibilityScan()
    
    expect(report.violations).toHaveLength(1)
    expect(report.violations[0].id).toBe('color-contrast')
    expect(report.passes).toBe(1)
    expect(report.timestamp).toBeDefined()
  })

  it('should generate accessibility summary', () => {
    const mockReport = {
      violations: [
        { id: 'v1', impact: 'critical' as const, description: 'Critical issue', help: 'Fix it', helpUrl: 'https://example.com', nodes: [] },
        { id: 'v2', impact: 'serious' as const, description: 'Serious issue', help: 'Fix it', helpUrl: 'https://example.com', nodes: [] }
      ],
      passes: 10,
      incomplete: 2,
      inapplicable: 5,
      timestamp: '2024-01-01T00:00:00Z'
    }

    const summary = getAccessibilitySummary(mockReport)
    
    expect(summary).toContain('Total Violations: 2')
    expect(summary).toContain('Critical: 1')
    expect(summary).toContain('Serious: 1')
    expect(summary).toContain('Passed: 10')
  })

  it('should check WCAG compliance - FAIL level with critical issues', () => {
    const mockReport = {
      violations: [
        { id: 'v1', impact: 'critical' as const, description: 'Critical issue', help: 'Fix it', helpUrl: 'https://example.com', nodes: [] }
      ],
      passes: 10,
      incomplete: 0,
      inapplicable: 0,
      timestamp: '2024-01-01T00:00:00Z'
    }

    const compliance = checkWCAGCompliance(mockReport)
    
    expect(compliance.level).toBe('FAIL')
    expect(compliance.compliant).toBe(false)
    expect(compliance.issues).toHaveLength(1)
  })

  it('should check WCAG compliance - A level with serious issues', () => {
    const mockReport = {
      violations: [
        { id: 'v1', impact: 'serious' as const, description: 'Serious issue', help: 'Fix it', helpUrl: 'https://example.com', nodes: [] }
      ],
      passes: 10,
      incomplete: 0,
      inapplicable: 0,
      timestamp: '2024-01-01T00:00:00Z'
    }

    const compliance = checkWCAGCompliance(mockReport)
    
    expect(compliance.level).toBe('A')
    expect(compliance.compliant).toBe(true)
  })

  it('should check WCAG compliance - AAA level with no issues', () => {
    const mockReport = {
      violations: [],
      passes: 10,
      incomplete: 0,
      inapplicable: 0,
      timestamp: '2024-01-01T00:00:00Z'
    }

    const compliance = checkWCAGCompliance(mockReport)
    
    expect(compliance.level).toBe('AAA')
    expect(compliance.compliant).toBe(true)
    expect(compliance.issues).toHaveLength(0)
  })

  it('should provide accessibility recommendations', () => {
    const mockReport = {
      violations: [
        { id: 'v1', impact: 'serious' as const, description: 'Serious issue', help: 'Fix the contrast', helpUrl: 'https://example.com', nodes: [] }
      ],
      passes: 10,
      incomplete: 0,
      inapplicable: 0,
      timestamp: '2024-01-01T00:00:00Z'
    }

    const recommendations = getAccessibilityRecommendations(mockReport)
    
    expect(recommendations).toHaveLength(1)
    expect(recommendations[0]).toContain('Fix the contrast')
    expect(recommendations[0]).toContain('https://example.com')
  })
})

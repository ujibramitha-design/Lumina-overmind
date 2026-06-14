/**
 * Utilitas untuk accessibility testing dengan axe-core
 */

export interface AccessibilityViolation {
  id: string
  impact: 'critical' | 'serious' | 'moderate' | 'minor'
  description: string
  help: string
  helpUrl: string
  nodes: any[]
}

export interface AccessibilityReport {
  violations: AccessibilityViolation[]
  passes: number
  incomplete: number
  inapplicable: number
  timestamp: string
}

/**
 * Fungsi untuk menjalankan accessibility scan
 * @param container - Element container untuk di-scan
 * @returns Accessibility report
 */
export async function runAccessibilityScan(container: HTMLElement | null = null): Promise<AccessibilityReport> {
  if (typeof window === 'undefined') {
    throw new Error('Accessibility scan hanya bisa dijalankan di browser')
  }

  const axe = (await import('@axe-core/react')).default
  
  // @ts-ignore - axe.run parameter type issue
  const results: any = await axe(container || document.body, {
    runOnly: {
      type: 'tag',
      values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
    }
  })

  const violations: AccessibilityViolation[] = results.violations.map((violation: any) => ({
    id: violation.id,
    impact: violation.impact as any,
    description: violation.description,
    help: violation.help,
    helpUrl: violation.helpUrl,
    nodes: violation.nodes
  }))

  return {
    violations,
    passes: results.passes.length,
    incomplete: results.incomplete.length,
    inapplicable: results.inapplicable.length,
    timestamp: new Date().toISOString()
  }
}

/**
 * Fungsi untuk mendapatkan ringkasan accessibility
 * @param report - Accessibility report
 * @returns Ringkasan dalam format string
 */
export function getAccessibilitySummary(report: AccessibilityReport): string {
  const criticalCount = report.violations.filter(v => v.impact === 'critical').length
  const seriousCount = report.violations.filter(v => v.impact === 'serious').length
  const moderateCount = report.violations.filter(v => v.impact === 'moderate').length
  const minorCount = report.violations.filter(v => v.impact === 'minor').length

  return `
📊 Accessibility Report
========================
Total Violations: ${report.violations.length}
Critical: ${criticalCount}
Serious: ${seriousCount}
Moderate: ${moderateCount}
Minor: ${minorCount}

Passed: ${report.passes}
Incomplete: ${report.incomplete}
Inapplicable: ${report.inapplicable}

Timestamp: ${report.timestamp}
  `
}

/**
 * Fungsi untuk memeriksa WCAG compliance
 * @param report - Accessibility report
 * @returns Status compliance
 */
export function checkWCAGCompliance(report: AccessibilityReport): {
  level: 'A' | 'AA' | 'AAA' | 'FAIL'
  compliant: boolean
  issues: string[]
} {
  const criticalIssues = report.violations.filter(v => v.impact === 'critical')
  const seriousIssues = report.violations.filter(v => v.impact === 'serious')

  if (criticalIssues.length > 0) {
    return {
      level: 'FAIL',
      compliant: false,
      issues: criticalIssues.map(v => `${v.id}: ${v.description}`)
    }
  }

  if (seriousIssues.length > 0) {
    return {
      level: 'A',
      compliant: true,
      issues: seriousIssues.map(v => `${v.id}: ${v.description}`)
    }
  }

  const moderateIssues = report.violations.filter(v => v.impact === 'moderate')
  if (moderateIssues.length > 0) {
    return {
      level: 'AA',
      compliant: true,
      issues: moderateIssues.map(v => `${v.id}: ${v.description}`)
    }
  }

  return {
    level: 'AAA',
    compliant: true,
    issues: []
  }
}

/**
 * Fungsi untuk mendapatkan rekomendasi perbaikan
 * @param report - Accessibility report
 * @returns Rekomendasi perbaikan
 */
export function getAccessibilityRecommendations(report: AccessibilityReport): string[] {
  const recommendations: string[] = []

  report.violations.forEach(violation => {
    recommendations.push(`- ${violation.help} (${violation.helpUrl})`)
  })

  return recommendations
}

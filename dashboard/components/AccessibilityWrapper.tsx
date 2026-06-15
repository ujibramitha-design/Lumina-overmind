'use client'

/**
 * Accessibility Wrapper Component
 * Provides accessibility features and monitoring for wrapped components
 */

import { useEffect, useRef } from 'react'
import { runAccessibilityScan, getAccessibilitySummary, checkWCAGCompliance } from '@/lib/accessibility'

interface AccessibilityWrapperProps {
  children: React.ReactNode
  enableMonitoring?: boolean
  onViolation?: (violations: any[]) => void
  className?: string
}

export function AccessibilityWrapper({
  children,
  enableMonitoring = false,
  onViolation,
  className = ''
}: AccessibilityWrapperProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!enableMonitoring || typeof window === 'undefined') return

    // Run accessibility scan after component mounts
    const timer = setTimeout(async () => {
      try {
        const report = await runAccessibilityScan(containerRef.current)
        
        if (report.violations.length > 0) {
          console.warn('Accessibility violations detected:', getAccessibilitySummary(report))
          
          if (onViolation) {
            onViolation(report.violations)
          }
        }
        
        const compliance = checkWCAGCompliance(report)
        console.log('WCAG Compliance Level:', compliance.level)
      } catch (error) {
        console.error('Accessibility scan failed:', error)
      }
    }, 1000) // Delay to ensure DOM is fully rendered

    return () => clearTimeout(timer)
  }, [enableMonitoring, onViolation])

  return (
    <div
      ref={containerRef}
      className={className}
      role="main"
      tabIndex={-1}
    >
      {children}
    </div>
  )
}

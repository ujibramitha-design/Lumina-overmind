'use client'

/**
 * Skip to Main Content Link
 * WCAG 2.1.1 - Keyboard accessible skip link for screen readers
 */

import { useEffect, useState } from 'react'

export function SkipLink() {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <a
      href="#main-content"
      className={`
        fixed top-0 left-0 z-50 p-4 bg-emerald-600 text-white font-semibold
        transform -translate-y-full focus:translate-y-0 transition-transform
        ${isFocused ? 'translate-y-0' : ''}
      `}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
    >
      Skip to main content
    </a>
  )
}

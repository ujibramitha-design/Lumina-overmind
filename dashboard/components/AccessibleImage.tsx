'use client'

/**
 * Accessible Image Component
 * Enforces alt text for WCAG compliance
 */

import * as React from 'react'
import { cn } from '@/lib/utils'

interface AccessibleImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  alt: string // Required alt text for accessibility
  decorative?: boolean // If true, adds aria-hidden and empty alt
  loading?: 'lazy' | 'eager'
}

const AccessibleImage = React.forwardRef<HTMLImageElement, AccessibleImageProps>(
  ({ className, alt, decorative = false, loading = 'lazy', ...props }, ref) => {
    const finalAlt = decorative ? '' : alt
    const ariaHidden = decorative ? 'true' : undefined

    return (
      <img
        ref={ref}
        alt={finalAlt}
        aria-hidden={ariaHidden}
        loading={loading}
        className={cn('object-cover', className)}
        {...props}
      />
    )
  }
)
AccessibleImage.displayName = 'AccessibleImage'

export { AccessibleImage }

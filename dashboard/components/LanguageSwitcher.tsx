'use client'

/**
 * Language Switcher Component
 * Allows users to switch between English and Indonesian
 */

import { useLocale } from 'next-intl'
import { useRouter, usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Languages } from 'lucide-react'
import { locales, type Locale } from '@/i18n'

export function LanguageSwitcher() {
  const locale = useLocale()
  const router = useRouter()
  const pathname = usePathname()

  const switchLocale = (newLocale: Locale) => {
    // Remove the current locale from the pathname and add the new one
    const segments = pathname.split('/')
    segments[1] = newLocale
    const newPath = segments.join('/')
    router.push(newPath)
  }

  return (
    <div className="flex items-center gap-2">
      <Languages className="h-4 w-4 text-zinc-400" />
      {locales.map((loc) => (
        <Button
          key={loc}
          variant={locale === loc ? 'default' : 'ghost'}
          size="sm"
          onClick={() => switchLocale(loc)}
          className="text-xs"
          aria-label={`Switch to ${loc === 'en' ? 'English' : 'Indonesian'}`}
        >
          {loc.toUpperCase()}
        </Button>
      ))}
    </div>
  )
}

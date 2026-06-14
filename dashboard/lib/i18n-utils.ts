import {useTranslations} from 'next-intl'

/**
 * Hook untuk menggunakan terjemahan
 * @param namespace - Namespace dari terjemahan (contoh: 'common', 'leads', 'projects')
 * @returns Hook useTranslations
 */
export function useTranslationsHook(namespace: string) {
  return useTranslations(namespace)
}

/**
 * Fungsi helper untuk mendapatkan locale saat ini
 * @returns Locale saat ini ('en' atau 'id')
 */
export function getCurrentLocale(): string {
  if (typeof window !== 'undefined') {
    const path = window.location.pathname
    const locale = path.split('/')[1]
    return ['en', 'id'].includes(locale) ? locale : 'en'
  }
  return 'en'
}

/**
 * Fungsi helper untuk mengganti locale
 * @param locale - Locale baru ('en' atau 'id')
 */
export function changeLocale(locale: string) {
  if (typeof window !== 'undefined') {
    const currentPath = window.location.pathname
    const currentLocale = getCurrentLocale()
    const newPath = currentPath.replace(`/${currentLocale}`, `/${locale}`)
    window.location.href = newPath
  }
}

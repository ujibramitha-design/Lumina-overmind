'use client'

import { useSearchParams } from 'next/navigation'
import DashboardWorkspace from '@/components/DashboardWorkspace'
import UnauthorizedAlert from '@/components/UnauthorizedAlert'

export default function DashboardPage() {
  const searchParams = useSearchParams()
  const error = searchParams.get('error')

  if (error) {
    return <UnauthorizedAlert />
  }

  return <DashboardWorkspace />
}

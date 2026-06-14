'use client'

import React from 'react'
import { useSearchParams } from 'next/navigation'
import { AlertTriangle, Shield, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

const UnauthorizedAlert = () => {
  const searchParams = useSearchParams()
  const error = searchParams.get('error')
  const message = searchParams.get('message')

  const getErrorContent = (errorType: string | null) => {
    switch (errorType) {
      case 'unauthorized':
        return {
          icon: Shield,
          title: 'Access Denied',
          description: message || 'You require administrator privileges to access the Classified Vault.',
          color: 'red',
        }
      case 'token_expired':
        return {
          icon: AlertTriangle,
          title: 'Session Expired',
          description: 'Your session has expired. Please log in again.',
          color: 'yellow',
        }
      case 'invalid_token':
        return {
          icon: AlertTriangle,
          title: 'Invalid Session',
          description: 'Your session is invalid. Please log in again.',
          color: 'red',
        }
      default:
        return {
          icon: AlertTriangle,
          title: 'Access Error',
          description: 'An error occurred while accessing this resource.',
          color: 'gray',
        }
    }
  }

  const errorContent = getErrorContent(error)
  const Icon = errorContent.icon

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-8">
      <div className="max-w-md w-full">
        <div className={`bg-gray-800 rounded-lg p-8 border-2 border-${errorContent.color}-500`}>
          <div className="flex items-center justify-center w-16 h-16 bg-gray-700 rounded-full mx-auto mb-6">
            <Icon className={`w-8 h-8 text-${errorContent.color}-500`} />
          </div>

          <h1 className={`text-2xl font-bold text-center mb-4 text-${errorContent.color}-500`}>{errorContent.title}</h1>

          <p className="text-gray-300 text-center mb-8">{errorContent.description}</p>

          <div className="space-y-4">
            <Link
              href="/dashboard"
              className="flex items-center justify-center w-full bg-gray-700 hover:bg-gray-600 px-6 py-3 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Return to Dashboard
            </Link>

            {error === 'unauthorized' && (
              <Link
                href="/login"
                className="flex items-center justify-center w-full bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg transition-colors"
              >
                <Shield className="w-5 h-5 mr-2" />
                Login as Administrator
              </Link>
            )}
          </div>

          <div className="mt-8 pt-6 border-t border-gray-700">
            <p className="text-xs text-gray-500 text-center">
              🔐 CLASSIFIED VAULT - Level 5 Security Clearance Required
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UnauthorizedAlert

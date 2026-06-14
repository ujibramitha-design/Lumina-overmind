import posthog from 'posthog-js'

// Initialize PostHog
export const initPostHog = () => {
  if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_POSTHOG_KEY) {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
      capture_pageview: true,
      capture_pageleave: true,
      autocapture: true,
      persistence: 'localStorage',
    })
  }
}

// Track custom events
export const trackEvent = (eventName: string, properties?: Record<string, any>) => {
  if (typeof window !== 'undefined') {
    posthog.capture(eventName, properties)
  }
}

// Track page views
export const trackPageView = (pageName: string, properties?: Record<string, any>) => {
  if (typeof window !== 'undefined') {
    posthog.capture('$pageview', {
      $current_url: window.location.href,
      page_name: pageName,
      ...properties,
    })
  }
}

// Identify user
export const identifyUser = (userId: string, properties?: Record<string, any>) => {
  if (typeof window !== 'undefined') {
    posthog.identify(userId, properties)
  }
}

// Reset user
export const resetUser = () => {
  if (typeof window !== 'undefined') {
    posthog.reset()
  }
}

export default posthog

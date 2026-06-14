/**
 * LUMINA OVERMIND SYSTEM - Dynamic Component Loading
 *
 * Implements code splitting for heavy components to improve initial load performance
 */

import dynamic from 'next/dynamic'
import { ComponentType } from 'react'

// Loading component for all dynamic imports
const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
    <span className="ml-2 text-zinc-400">Loading...</span>
  </div>
)

// Error fallback component
const ErrorFallback = ({ error }: { error?: Error }) => (
  <div className="flex flex-col items-center justify-center p-8 text-center">
    <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mb-4">
      <span className="text-red-500 text-2xl">⚠️</span>
    </div>
    <h3 className="text-lg font-medium text-zinc-100 mb-2">Failed to load component</h3>
    <p className="text-zinc-400 text-sm">{error?.message || 'An error occurred while loading this component.'}</p>
  </div>
)

// Chart components (heavy)
export const DynamicChart = dynamic(
  () => import('@/components/charts/PerformanceChart').then(mod => ({ default: mod.PerformanceChart })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicLeadChart = dynamic(
  () => import('@/components/charts/LeadChart').then(mod => ({ default: mod.LeadChart })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicRevenueChart = dynamic(
  () => import('@/components/charts/RevenueChart').then(mod => ({ default: mod.RevenueChart })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Table components (large datasets)
export const DynamicVirtualizedTable = dynamic(
  () => import('@/components/ui/VirtualizedTable').then(mod => ({ default: mod.VirtualizedTable })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicLeadsTable = dynamic(
  () => import('@/components/ui/VirtualizedTable').then(mod => ({ default: mod.VirtualizedLeadsTable })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Form components (complex validation)
export const DynamicLeadForm = dynamic(
  () => import('@/components/forms/LeadForm').then(mod => ({ default: mod.LeadForm })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicUserForm = dynamic(
  () => import('@/components/forms/UserForm').then(mod => ({ default: mod.UserForm })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Modal components (overlays)
export const DynamicWorkflowModal = dynamic(
  () => import('@/components/modals/WorkflowModal').then(mod => ({ default: mod.WorkflowModal })),
  {
    loading: () => null, // Modals should not show loading state
    ssr: false,
  }
)

export const DynamicSettingsModal = dynamic(
  () => import('@/components/modals/SettingsModal').then(mod => ({ default: mod.SettingsModal })),
  {
    loading: () => null,
    ssr: false,
  }
)

// Dashboard components (heavy computations)
export const DynamicDashboard = dynamic(
  () => import('@/components/Dashboard').then(mod => ({ default: mod.Dashboard })),
  {
    loading: LoadingSpinner,
    ssr: true, // Dashboard should be server-side rendered
  }
)

export const DynamicAnalytics = dynamic(
  () => import('@/components/Analytics').then(mod => ({ default: mod.Analytics })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Workflow components (ReactFlow)
export const DynamicWorkflowBuilder = dynamic(
  () => import('@/components/workflows/WorkflowBuilder').then(mod => ({ default: mod.WorkflowBuilder })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicWorkflowNode = dynamic(
  () => import('@/components/workflows/WorkflowNode').then(mod => ({ default: mod.WorkflowNode })),
  {
    loading: () => null,
    ssr: false,
  }
)

// Map components (external libraries)
export const DynamicMap = dynamic(
  () => import('@/components/maps/PropertyMap').then(mod => ({ default: mod.PropertyMap })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicLocationPicker = dynamic(
  () => import('@/components/maps/LocationPicker').then(mod => ({ default: mod.LocationPicker })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// File upload components
export const DynamicFileUploader = dynamic(
  () => import('@/components/upload/FileUploader').then(mod => ({ default: mod.FileUploader })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicImageEditor = dynamic(
  () => import('@/components/editors/ImageEditor').then(mod => ({ default: mod.ImageEditor })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Rich text editor
export const DynamicRichTextEditor = dynamic(
  () => import('@/components/editors/RichTextEditor').then(mod => ({ default: mod.RichTextEditor })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Advanced components
export const DynamicAdvancedFilters = dynamic(
  () => import('@/components/filters/AdvancedFilters').then(mod => ({ default: mod.AdvancedFilters })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

export const DynamicDataExporter = dynamic(
  () => import('@/components/export/DataExporter').then(mod => ({ default: mod.DataExporter })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
)

// Utility function for creating dynamic components with error handling
export const createDynamicComponent = <T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T } | { [key: string]: T }>,
  options: {
    loading?: ComponentType
    error?: ComponentType<{ error?: Error }>
    ssr?: boolean
    exportName?: string
  } = {}
) => {
  const { loading = LoadingSpinner, error = ErrorFallback, ssr = false, exportName } = options

  return dynamic(
    async () => {
      try {
        const module = await importFunc()

        if (exportName && typeof module === 'object' && module !== null) {
          const component = (module as any)[exportName]
          if (!component) {
            throw new Error(`Export '${exportName}' not found in module`)
          }
          return { default: component }
        }

        if ('default' in module) {
          return module
        }

        throw new Error('No default export found')
      } catch (err) {
        console.error('Dynamic import error:', err)
        throw err
      }
    },
    {
      loading,
      ssr,
    }
  )
}

// Preloading utilities
export const preloadComponent = (importFunc: () => Promise<any>) => {
  if (typeof window !== 'undefined') {
    importFunc()
  }
}

// Preload critical components
export const preloadCriticalComponents = () => {
  // Preload dashboard components
  preloadComponent(() => import('@/components/Dashboard'))

  // Preload charts if user likely to view them
  if (typeof window !== 'undefined') {
    const pathname = window.location.pathname
    if (pathname.includes('/dashboard') || pathname.includes('/analytics')) {
      preloadComponent(() => import('@/components/charts/PerformanceChart'))
      preloadComponent(() => import('@/components/charts/LeadChart'))
    }
  }
}

export default {
  DynamicChart,
  DynamicLeadChart,
  DynamicRevenueChart,
  DynamicVirtualizedTable,
  DynamicLeadsTable,
  DynamicLeadForm,
  DynamicUserForm,
  DynamicWorkflowModal,
  DynamicSettingsModal,
  DynamicDashboard,
  DynamicAnalytics,
  DynamicWorkflowBuilder,
  DynamicWorkflowNode,
  DynamicMap,
  DynamicLocationPicker,
  DynamicFileUploader,
  DynamicImageEditor,
  DynamicRichTextEditor,
  DynamicAdvancedFilters,
  DynamicDataExporter,
  createDynamicComponent,
  preloadComponent,
  preloadCriticalComponents,
}

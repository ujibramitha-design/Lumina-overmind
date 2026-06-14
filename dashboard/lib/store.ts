import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

export interface RunnerCard {
  id: string
  runnerId: string
  name: string
  description: string
  icon: React.ElementType
  status: 'running' | 'idle'
  lastScan: string
  systemLoad: number
  successRate: number
  pid?: number
  cpuPercent?: number
  memoryPercent?: number
}

export interface SystemMetrics {
  systemLoad: number
  activeRunners: number
  totalRunners: number
  apiRateLimit: 'Normal' | 'Warning' | 'Critical'
}

export interface User {
  id: string
  email: string
  username: string
  firstName: string
  lastName: string
  role: 'ADMIN' | 'USER' | 'OPERATOR' | 'VIEWER'
  isActive: boolean
  permissions: string[]
}

export interface AppState {
  // System state
  runners: RunnerCard[]
  systemMetrics: SystemMetrics
  loadingStates: Record<string, boolean>
  apiError: string | null
  lastSync: Date

  // UI state
  sidebarOpen: boolean
  notificationsOpen: boolean

  // User state
  user: User | null
  isAuthenticated: boolean

  // Actions
  setRunners: (runners: RunnerCard[]) => void
  updateRunner: (id: string, updates: Partial<RunnerCard>) => void
  setSystemMetrics: (metrics: SystemMetrics) => void
  setLoadingState: (id: string, loading: boolean) => void
  setApiError: (error: string | null) => void
  setLastSync: (date: Date) => void
  setSidebarOpen: (open: boolean) => void
  setNotificationsOpen: (open: boolean) => void

  // User actions
  setUser: (user: User | null) => void
  setAuthenticated: (authenticated: boolean) => void

  // Computed
  getActiveRunners: () => RunnerCard[]
  getRunnerById: (id: string) => RunnerCard | undefined
  isRunnerLoading: (id: string) => boolean
}

export const useAppStore = create<AppState>()(
  devtools(
    (set, get) => ({
      // Initial state
      runners: [],
      systemMetrics: {
        systemLoad: 45,
        activeRunners: 0,
        totalRunners: 6,
        apiRateLimit: 'Normal',
      },
      loadingStates: {},
      apiError: null,
      lastSync: new Date(),
      sidebarOpen: true,
      notificationsOpen: false,

      // User state
      user: null,
      isAuthenticated: false,

      // Actions
      setRunners: runners => set({ runners }),

      updateRunner: (id, updates) =>
        set(state => ({
          runners: state.runners.map(runner =>
            runner.id === id ? { ...runner, ...updates } : runner
          ),
        })),

      setSystemMetrics: metrics => set({ systemMetrics: metrics }),

      setLoadingState: (id, loading) =>
        set(state => ({
          loadingStates: { ...state.loadingStates, [id]: loading },
        })),

      setApiError: error => set({ apiError: error }),

      setLastSync: date => set({ lastSync: date }),

      setSidebarOpen: open => set({ sidebarOpen: open }),

      setNotificationsOpen: open => set({ notificationsOpen: open }),

      // User actions
      setUser: user => set({ user }),
      setAuthenticated: authenticated => set({ isAuthenticated: authenticated }),

      // Computed getters
      getActiveRunners: () => get().runners.filter(runner => runner.status === 'running'),

      getRunnerById: id => get().runners.find(runner => runner.id === id),

      isRunnerLoading: id => get().loadingStates[id] || false,
    }),
    {
      name: 'lumina-overmind-store',
    }
  )
)

// Selectors for optimized re-renders
export const useRunners = () => useAppStore(state => state.runners)
export const useSystemMetrics = () => useAppStore(state => state.systemMetrics)
export const useApiError = () => useAppStore(state => state.apiError)
export const useLoadingStates = () => useAppStore(state => state.loadingStates)
export const useSidebarOpen = () => useAppStore(state => state.sidebarOpen)
export const useNotificationsOpen = () => useAppStore(state => state.notificationsOpen)

// User selectors
export const useUser = () => useAppStore(state => state.user)
export const useIsAuthenticated = () => useAppStore(state => state.isAuthenticated)
export const useUserRole = () => useAppStore(state => state.user?.role)
export const useIsAdmin = () => useAppStore(state => state.user?.role === 'ADMIN')

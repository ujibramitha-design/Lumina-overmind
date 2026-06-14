/**
 * LUMINA OS - Authentication Utilities
 * ===================================
 *
 * JWT token management and authentication utilities
 */

import React from 'react'

export interface User {
  id: string
  username: string
  full_name: string
  email: string
  role: 'ADMIN' | 'USER' | 'OPERATOR'
  active: boolean
}

export interface AuthToken {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

const TOKEN_KEY = 'lumina_auth_token'
const USER_KEY = 'lumina_auth_user'

export class AuthManager {
  private static instance: AuthManager
  private token: string | null = null
  private user: User | null = null
  private listeners: Set<(state: AuthState) => void> = new Set()

  private constructor() {
    this.loadFromStorage()
  }

  static getInstance(): AuthManager {
    if (!AuthManager.instance) {
      AuthManager.instance = new AuthManager()
    }
    return AuthManager.instance
  }

  private loadFromStorage() {
    if (typeof window !== 'undefined') {
      try {
        const storedToken = localStorage.getItem(TOKEN_KEY)
        const storedUser = localStorage.getItem(USER_KEY)

        if (storedToken && storedUser) {
          this.token = storedToken
          this.user = JSON.parse(storedUser)

          // Validate token expiration
          if (this.isTokenExpired(storedToken)) {
            this.logout()
          }
        }
      } catch (error) {
        console.error('Error loading auth from storage:', error)
        this.logout()
      }
    }
  }

  private saveToStorage() {
    if (typeof window !== 'undefined') {
      try {
        if (this.token && this.user) {
          localStorage.setItem(TOKEN_KEY, this.token)
          localStorage.setItem(USER_KEY, JSON.stringify(this.user))
        } else {
          localStorage.removeItem(TOKEN_KEY)
          localStorage.removeItem(USER_KEY)
        }
      } catch (error) {
        console.error('Error saving auth to storage:', error)
      }
    }
  }

  private isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp
      if (!exp) return false

      return Date.now() >= exp * 1000
    } catch {
      return true
    }
  }

  private notifyListeners() {
    const state = this.getAuthStatePublic()
    this.listeners.forEach(listener => listener(state))
  }

  getAuthStatePublic(): AuthState {
    return {
      user: this.user,
      token: this.token,
      isAuthenticated: !!this.token && !!this.user,
      isLoading: false,
      error: null,
    }
  }

  async login(email: string, password: string): Promise<AuthToken> {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const authData: AuthToken = await response.json()

      this.token = authData.access_token
      this.user = authData.user
      this.saveToStorage()
      this.notifyListeners()

      return authData
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  logout(): void {
    this.token = null
    this.user = null
    this.saveToStorage()
    this.notifyListeners()
  }

  getToken(): string | null {
    return this.token
  }

  getUser(): User | null {
    return this.user
  }

  isAuthenticated(): boolean {
    return !!this.token && !!this.user && !this.isTokenExpired(this.token)
  }

  hasRole(role: string): boolean {
    return this.user?.role === role
  }

  hasPermission(permission: string): boolean {
    if (!this.user) return false

    // Simple permission system based on roles
    const permissions = {
      ADMIN: ['read', 'write', 'delete', 'admin'],
      OPERATOR: ['read', 'write', 'operate'],
      USER: ['read'],
    }

    const userPermissions = permissions[this.user.role] || []
    return userPermissions.includes(permission)
  }

  getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {}

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    return headers
  }

  subscribe(listener: (state: AuthState) => void): () => void {
    this.listeners.add(listener)

    // Immediately call listener with current state
    listener(this.getAuthStatePublic())

    // Return unsubscribe function
    return () => {
      this.listeners.delete(listener)
    }
  }

  async refreshToken(): Promise<void> {
    if (!this.token) return

    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: this.getAuthHeaders(),
      })

      if (!response.ok) {
        throw new Error('Token refresh failed')
      }

      const authData: AuthToken = await response.json()

      this.token = authData.access_token
      this.user = authData.user
      this.saveToStorage()
      this.notifyListeners()
    } catch (error) {
      console.error('Token refresh error:', error)
      this.logout()
      throw error
    }
  }

  async validateToken(): Promise<boolean> {
    if (!this.token) return false

    try {
      const response = await fetch('/api/auth/verify', {
        method: 'GET',
        headers: this.getAuthHeaders(),
      })

      return response.ok
    } catch {
      return false
    }
  }
}

// Export singleton instance
export const authManager = AuthManager.getInstance()

// Export hooks for React components
export const useAuth = () => {
  const [authState, setAuthState] = React.useState<AuthState>(authManager.getAuthStatePublic())

  React.useEffect(() => {
    const unsubscribe = authManager.subscribe(setAuthState)
    return unsubscribe
  }, [])

  return {
    ...authState,
    login: authManager.login.bind(authManager),
    logout: authManager.logout.bind(authManager),
    refreshToken: authManager.refreshToken.bind(authManager),
    validateToken: authManager.validateToken.bind(authManager),
    hasRole: authManager.hasRole.bind(authManager),
    hasPermission: authManager.hasPermission.bind(authManager),
    getAuthHeaders: authManager.getAuthHeaders.bind(authManager),
  }
}

// Export fetch wrapper with auth headers
export const authFetch = async (url: string, options: RequestInit = {}): Promise<Response> => {
  const authHeaders = authManager.getAuthHeaders()

  return fetch(url, {
    ...options,
    headers: {
      ...authHeaders,
      ...options.headers,
    },
  })
}

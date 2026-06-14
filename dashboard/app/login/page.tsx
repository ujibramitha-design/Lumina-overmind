'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Shield, Terminal, Eye, EyeOff, AlertCircle, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface LoginResponse {
  success: boolean
  message: string
  data?: {
    access_token: string
    token_type: string
    expires_in: number
    user: {
      id: number
      name: string
      email: string
      role: string
    }
  }
}

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Note: Authentication is now handled by middleware with HTTP-only cookies
  // No need to check localStorage as middleware will handle redirects

  // Animated grid background effect
  useEffect(() => {
    const createGridBackground = () => {
      const grid = document.createElement('div')
      grid.className = 'absolute inset-0 opacity-20'
      grid.style.background = `
        linear-gradient(rgba(16,185,129,0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(16,185,129,0.1) 1px, transparent 1px)
      `
      grid.style.backgroundSize = '50px 50px'
      grid.style.animation = 'pulse 4s ease-in-out infinite'
      return grid
    }

    const background = createGridBackground()
    document.body.appendChild(background)

    return () => {
      document.body.removeChild(background)
    }
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,
      })

      const result: LoginResponse = await response.json()

      if (result.success && result.data) {
        // Authentication is handled by HTTP-only cookies set by the server
        // No need to store in localStorage

        setIsAuthenticated(true)

        // Redirect after successful authentication
        setTimeout(() => {
          router.push('/')
        }, 1500)
      } else {
        setError(result.message || 'Authentication failed')
      }
    } catch (err) {
      setError('Connection error. Please try again.')
      console.error('Login error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  if (isAuthenticated) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="mb-8">
            <Shield className="w-16 h-16 text-emerald-500 mx-auto animate-pulse" />
          </div>
          <h1 className="text-2xl font-bold text-emerald-500 mb-2">AUTHENTICATION SUCCESSFUL</h1>
          <p className="text-zinc-400">Initializing secure connection...</p>
          <div className="mt-6">
            <Loader2 className="w-8 h-8 text-emerald-500 mx-auto animate-spin" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center relative overflow-hidden dark">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-black via-zinc-950 to-black" />

        {/* Grid overlay */}
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `
              linear-gradient(rgba(16,185,129,0.3) 1px, transparent 1px),
              linear-gradient(90deg, rgba(16,185,129,0.3) 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
            animation: 'pulse 4s ease-in-out infinite',
          }}
        />

        {/* Glow effect */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="w-96 h-96 bg-emerald-500 rounded-full blur-3xl opacity-5 animate-pulse" />
        </div>
      </div>

      {/* Login card */}
      <div className="relative z-10 w-full max-w-md mx-auto px-4">
        <Card className="bg-zinc-950 border border-emerald-500/20 shadow-[0_0_25px_rgba(16,185,129,0.15)]">
          <CardHeader className="text-center pb-6">
            <div className="flex justify-center mb-4">
              <div className="relative">
                <Shield className="w-12 h-12 text-emerald-500" />
                <div className="absolute -inset-1 bg-emerald-500 rounded-full blur-sm opacity-30 animate-pulse" />
              </div>
            </div>

            <CardTitle className="text-2xl font-bold text-emerald-500 mb-2 tracking-widest">LUMINA</CardTitle>

            <div className="flex items-center justify-center space-x-2 text-zinc-400">
              <Terminal className="w-4 h-4" />
              <span className="text-xs font-mono tracking-wider">AUTHORIZED PERSONNEL ONLY</span>
            </div>

            <div className="mt-4 text-xs text-zinc-500 font-mono">LUMINA OVERMIND SYSTEM v1.0</div>
          </CardHeader>

          <CardContent className="pt-0">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email input */}
              <div className="space-y-2">
                <label className="text-xs font-mono text-zinc-400 uppercase tracking-wider">Security Clearance</label>
                <div className="relative">
                  <Input
                    name="email"
                    type="email"
                    placeholder="admin@lumina.os"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    className="!bg-zinc-900 !border-zinc-800 text-zinc-300 placeholder:text-zinc-700 focus:!border-emerald-500/30 focus:ring-1 focus:ring-emerald-500/10 font-mono transition-all"
                    required
                    disabled={isLoading}
                  />
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-500/5 to-transparent pointer-events-none opacity-0 focus-within:opacity-100 transition-opacity duration-300" />
                </div>
              </div>

              {/* Password input */}
              <div className="space-y-2">
                <label className="text-xs font-mono text-zinc-400 uppercase tracking-wider">Access Code</label>
                <div className="relative">
                  <Input
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    className="!bg-zinc-900 !border-zinc-800 text-zinc-300 placeholder:text-zinc-700 focus:!border-emerald-500/30 focus:ring-1 focus:ring-emerald-500/10 font-mono pr-10 transition-all"
                    required
                    disabled={isLoading}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-zinc-600 hover:text-emerald-500 transition-colors"
                    disabled={isLoading}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-500/5 to-transparent pointer-events-none opacity-0 focus-within:opacity-100 transition-opacity duration-300" />
                </div>
              </div>

              {/* Error message */}
              {error && (
                <div className="flex items-center space-x-2 p-3 bg-red-950/50 border border-red-500/20 rounded-lg">
                  <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                  <span className="text-red-500 text-xs font-mono">{error}</span>
                </div>
              )}

              {/* Submit button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-emerald-500 hover:bg-emerald-600 text-black font-bold py-3 transition-all duration-300 border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.3)] hover:shadow-[0_0_25px_rgba(16,185,129,0.5)]"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>AUTHENTICATING...</span>
                  </div>
                ) : (
                  <span className="font-mono tracking-wider">INITIALIZE SYSTEM</span>
                )}
              </Button>
            </form>

            {/* System status */}
            <div className="mt-6 pt-6 border-t border-zinc-800">
              <div className="flex items-center justify-between text-xs text-zinc-500 font-mono">
                <span>SYSTEM STATUS</span>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                  <span>ONLINE</span>
                </div>
              </div>

              <div className="mt-2 text-xs text-zinc-600 font-mono">
                <div>SECURE PROTOCOL: TLS 1.3</div>
                <div>ENCRYPTION: AES-256</div>
                <div>AUTHENTICATION: JWT</div>
              </div>
            </div>

            {/* Footer */}
            <div className="mt-6 text-center">
              <p className="text-xs text-zinc-600 font-mono">&copy; 2026 Lumina Central Intelligence</p>
              <p className="text-xs text-zinc-700 font-mono mt-1">CLASSIFIED // TOP SECRET</p>
              <p className="text-xs text-zinc-500 font-mono mt-1">By BramsRV&trade;</p>
            </div>
          </CardContent>
        </Card>

        {/* Floating particles effect */}
        <div className="absolute inset-0 pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-emerald-500 rounded-full opacity-30 animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 3}s`,
              }}
            />
          ))}
        </div>
      </div>

      {/* Custom styles */}
      <style jsx global>{`
        :root {
          color-scheme: dark;
        }

        @keyframes pulse {
          0%,
          100% {
            opacity: 0.1;
          }
          50% {
            opacity: 0.2;
          }
        }

        /* Ultra Aggressive Fix for browser autofill */
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus,
        input:-webkit-autofill:active {
          transition: background-color 600000s ease-in-out 0s !important;
          -webkit-text-fill-color: #10b981 !important;
          box-shadow: 0 0 0px 1000px #18181b inset !important;
          caret-color: #10b981 !important;
        }

        /* The 'Nuclear' Option - Force transparency on autofill background */
        input:-webkit-autofill {
          filter: none !important;
        }

        input {
          color-scheme: dark !important;
        }
      `}</style>
    </div>
  )
}

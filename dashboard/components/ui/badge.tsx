import * as React from 'react'
import { cn } from '@/lib/utils'

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'hot' | 'warm' | 'cold'
}

function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  const variantClasses = {
    default: 'border-transparent bg-emerald-500 text-black hover:bg-emerald-600',
    secondary: 'border-transparent bg-zinc-800 text-zinc-100 hover:bg-zinc-700',
    destructive: 'border-transparent bg-red-500 text-zinc-100 hover:bg-red-600',
    outline: 'text-zinc-100 border-zinc-700',
    hot: 'border-transparent bg-emerald-500 text-black font-bold',
    warm: 'border-transparent bg-yellow-500 text-black font-semibold',
    cold: 'border-transparent bg-red-500 text-white font-semibold',
  }

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2',
        variantClasses[variant],
        className
      )}
      {...props}
    />
  )
}

export { Badge }

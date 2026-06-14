'use client'

import * as React from 'react'
import { cn } from '@/lib/utils'

interface SwitchProps extends React.InputHTMLAttributes<HTMLInputElement> {
  checked?: boolean
  onCheckedChange?: (checked: boolean) => void
}

const Switch = React.forwardRef<HTMLInputElement, SwitchProps>(
  ({ className, checked, onCheckedChange, ...props }, ref) => {
    const [isChecked, setIsChecked] = React.useState(checked || false)

    React.useEffect(() => {
      setIsChecked(checked || false)
    }, [checked])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setIsChecked(e.target.checked)
      onCheckedChange?.(e.target.checked)
    }

    return (
      <div className="relative">
        <input type="checkbox" ref={ref} checked={isChecked} onChange={handleChange} className="sr-only" {...props} />
        <button
          type="button"
          onClick={() => {
            const newState = !isChecked
            setIsChecked(newState)
            onCheckedChange?.(newState)
          }}
          className={cn(
            'peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-950 disabled:cursor-not-allowed disabled:opacity-50',
            isChecked ? 'bg-emerald-500' : 'bg-zinc-700',
            className
          )}
        >
          <span
            className={cn(
              'pointer-events-none block h-5 w-5 rounded-full bg-zinc-100 shadow-lg ring-0 transition-transform',
              isChecked ? 'translate-x-5' : 'translate-x-0'
            )}
          />
        </button>
      </div>
    )
  }
)
Switch.displayName = 'Switch'

export { Switch }

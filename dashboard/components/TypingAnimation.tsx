'use client'

import { useEffect, useState } from 'react'

interface TypingAnimationProps {
  text: string
  speed?: number
  onComplete?: () => void
}

export default function TypingAnimation({ text, speed = 30, onComplete }: TypingAnimationProps) {
  const [displayedText, setDisplayedText] = useState('')
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    let index = 0
    setDisplayedText('')
    setIsComplete(false)

    const timer = setInterval(() => {
      if (index < text.length) {
        setDisplayedText(prev => prev + text.charAt(index))
        index++
      } else {
        clearInterval(timer)
        setIsComplete(true)
        onComplete?.()
      }
    }, speed)

    return () => clearInterval(timer)
  }, [text, speed, onComplete])

  return (
    <span>
      {displayedText}
      {!isComplete && <span className="inline-block w-2 h-4 bg-emerald-400 ml-1 animate-pulse" />}
    </span>
  )
}

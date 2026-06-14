'use client'

import { useEffect, useRef, useState } from 'react'
import { Mic, MicOff } from 'lucide-react'

interface VoiceWaveformProps {
  isRecording: boolean
  onRecordingChange?: (isRecording: boolean) => void
  onTranscript?: (transcript: string) => void
}

export default function VoiceWaveform({ isRecording, onRecordingChange, onTranscript }: VoiceWaveformProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isListening, setIsListening] = useState(false)
  const audioContextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null)
  const animationRef = useRef<number | null>(null)
  const recognitionRef = useRef<any>(null)

  useEffect(() => {
    if (isRecording && !isListening) {
      startRecording()
    } else if (!isRecording && isListening) {
      stopRecording()
    }

    return () => {
      if (isListening) {
        stopRecording()
      }
    }
  }, [isRecording])

  const startRecording = async () => {
    try {
      // Initialize Audio Context
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)()
      analyserRef.current = audioContextRef.current.createAnalyser()
      analyserRef.current.fftSize = 256

      // Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      sourceRef.current = audioContextRef.current.createMediaStreamSource(stream)
      sourceRef.current.connect(analyserRef.current)

      setIsListening(true)
      onRecordingChange?.(true)

      // Start visualization
      drawWaveform()

      // Start speech recognition
      startSpeechRecognition()
    } catch (error) {
      console.error('Error accessing microphone:', error)
      setIsListening(false)
      onRecordingChange?.(false)
    }
  }

  const stopRecording = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current)
    }

    if (sourceRef.current) {
      sourceRef.current.disconnect()
    }

    if (audioContextRef.current) {
      audioContextRef.current.close()
    }

    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }

    setIsListening(false)
    onRecordingChange?.(false)
  }

  const drawWaveform = () => {
    const canvas = canvasRef.current
    const analyser = analyserRef.current
    if (!canvas || !analyser) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    const draw = () => {
      animationRef.current = requestAnimationFrame(draw)
      analyser.getByteFrequencyData(dataArray)

      ctx.fillStyle = 'rgba(0, 0, 0, 0.2)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      const barWidth = (canvas.width / bufferLength) * 2.5
      let barHeight
      let x = 0

      for (let i = 0; i < bufferLength; i++) {
        barHeight = dataArray[i] / 2

        // Create gradient
        const gradient = ctx.createLinearGradient(0, canvas.height - barHeight, 0, canvas.height)
        gradient.addColorStop(0, '#10b981')
        gradient.addColorStop(0.5, '#3b82f6')
        gradient.addColorStop(1, '#8b5cf6')

        ctx.fillStyle = gradient
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)

        x += barWidth + 1
      }
    }

    draw()
  }

  const startSpeechRecognition = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = true
      recognitionRef.current.interimResults = true
      recognitionRef.current.lang = 'id-ID'

      let finalTranscript = ''

      recognitionRef.current.onresult = (event: any) => {
        let interimTranscript = ''

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript
          } else {
            interimTranscript += event.results[i][0].transcript
          }
        }

        if (finalTranscript) {
          onTranscript?.(finalTranscript)
        }
      }

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error)
        stopRecording()
      }

      recognitionRef.current.onend = () => {
        if (isListening) {
          recognitionRef.current.start()
        }
      }

      recognitionRef.current.start()
    }
  }

  return (
    <div className="relative w-full h-24 bg-black/35 rounded-lg border border-zinc-800 overflow-hidden">
      <canvas
        ref={canvasRef}
        width={600}
        height={96}
        className="w-full h-full"
      />
      <div className="absolute bottom-2 left-2 flex items-center gap-2">
        {isListening ? (
          <>
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            <span className="text-xs text-emerald-400">Recording...</span>
          </>
        ) : (
          <>
            <MicOff className="h-4 w-4 text-zinc-500" />
            <span className="text-xs text-zinc-500">Not recording</span>
          </>
        )}
      </div>
    </div>
  )
}

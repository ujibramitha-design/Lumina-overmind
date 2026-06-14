'use client'

import React from 'react'

export default function SimpleDashboard() {
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Elite Hunter Dashboard</h1>
        <p className="text-xl text-gray-400">Dashboard is working!</p>
        <div className="mt-8">
          <div className="inline-block bg-green-500 text-white px-6 py-3 rounded-lg">✅ System Online</div>
        </div>
      </div>
    </div>
  )
}

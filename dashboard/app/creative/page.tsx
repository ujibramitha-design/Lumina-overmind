'use client'

import React, { useState } from 'react'
import { FileText, Image, Video, Globe, Download, ArrowRight } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface CreativeAsset {
  id: string
  title: string
  type: 'brochure' | 'social' | 'video' | 'landing'
  createdDate: string
  thumbnail?: string
  icon: React.ReactNode
}

const dummyAssets: CreativeAsset[] = [
  {
    id: '1',
    title: 'Promo Banten Q3',
    type: 'brochure',
    createdDate: '2026-05-28',
    icon: <FileText className="h-4 w-4" />,
  },
  {
    id: '2',
    title: 'Instagram Campaign - Summer Sale',
    type: 'social',
    createdDate: '2026-05-27',
    icon: <Image className="h-4 w-4" />,
  },
  {
    id: '3',
    title: 'Property Tour Video',
    type: 'video',
    createdDate: '2026-05-26',
    icon: <Video className="h-4 w-4" />,
  },
  {
    id: '4',
    title: 'Luxury Landing Page',
    type: 'landing',
    createdDate: '2026-05-25',
    icon: <Globe className="h-4 w-4" />,
  },
  {
    id: '5',
    title: 'Cluster Cipocok Brochure',
    type: 'brochure',
    createdDate: '2026-05-24',
    icon: <FileText className="h-4 w-4" />,
  },
  {
    id: '6',
    title: 'Facebook Ad Campaign',
    type: 'social',
    createdDate: '2026-05-23',
    icon: <Image className="h-4 w-4" />,
  },
  {
    id: '7',
    title: 'Virtual Reality Tour',
    type: 'video',
    createdDate: '2026-05-22',
    icon: <Video className="h-4 w-4" />,
  },
  {
    id: '8',
    title: 'Investment Landing Page',
    type: 'landing',
    createdDate: '2026-05-21',
    icon: <Globe className="h-4 w-4" />,
  },
  {
    id: '9',
    title: 'Serang City Brochure',
    type: 'brochure',
    createdDate: '2026-05-20',
    icon: <FileText className="h-4 w-4" />,
  },
  {
    id: '10',
    title: 'Twitter Campaign',
    type: 'social',
    createdDate: '2026-05-19',
    icon: <Image className="h-4 w-4" />,
  },
  {
    id: '11',
    title: 'Drone Footage Video',
    type: 'video',
    createdDate: '2026-05-18',
    icon: <Video className="h-4 w-4" />,
  },
  {
    id: '12',
    title: 'E-commerce Landing Page',
    type: 'landing',
    createdDate: '2026-05-17',
    icon: <Globe className="h-4 w-4" />,
  },
]

export default function CreativePage() {
  const [activeTab, setActiveTab] = useState('all')
  const [filteredAssets, setFilteredAssets] = useState(dummyAssets)

  const handleTabChange = (value: string) => {
    setActiveTab(value)
    if (value === 'all') {
      setFilteredAssets(dummyAssets)
    } else {
      setFilteredAssets(dummyAssets.filter(asset => asset.type === value))
    }
  }

  const handleGenerateNew = () => {
    // Placeholder for generate new brochure functionality
    console.log('Generate new brochure clicked')
  }

  const handleDownload = (assetId: string) => {
    // Placeholder for download functionality
    console.log(`Download asset ${assetId}`)
  }

  const handleDeploy = (assetId: string) => {
    // Placeholder for deploy to ads functionality
    console.log(`Deploy asset ${assetId} to ads`)
  }

  return (
    <div className="min-h-screen bg-black p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-zinc-100 mb-2">AI Creative Studio</h1>
            <p className="text-lg text-zinc-400">Generate and manage your marketing content with AI</p>
          </div>
          <Button
            onClick={handleGenerateNew}
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium px-6 py-3 transition-colors"
          >
            Generate New Brochure
          </Button>
        </div>
      </div>

      {/* Filter Tabs */}
      <Tabs value={activeTab} onValueChange={handleTabChange} className="mb-8">
        <TabsList className="grid w-full grid-cols-5 bg-zinc-900 border border-zinc-800 rounded-lg p-1">
          <TabsTrigger
            value="all"
            className="data-[state=active]:bg-zinc-800 text-zinc-300 hover:text-white transition-colors px-4 py-2 rounded-md"
          >
            All Assets
          </TabsTrigger>
          <TabsTrigger
            value="brochure"
            className="data-[state=active]:bg-zinc-800 text-zinc-300 hover:text-white transition-colors px-4 py-2 rounded-md"
          >
            Brochures
          </TabsTrigger>
          <TabsTrigger
            value="social"
            className="data-[state=active]:bg-zinc-800 text-zinc-300 hover:text-white transition-colors px-4 py-2 rounded-md"
          >
            Social Media
          </TabsTrigger>
          <TabsTrigger
            value="video"
            className="data-[state=active]:bg-zinc-800 text-zinc-300 hover:text-white transition-colors px-4 py-2 rounded-md"
          >
            Videos
          </TabsTrigger>
          <TabsTrigger
            value="landing"
            className="data-[state=active]:bg-zinc-800 text-zinc-300 hover:text-white transition-colors px-4 py-2 rounded-md"
          >
            Landing Pages
          </TabsTrigger>
        </TabsList>
      </Tabs>

      {/* Content Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredAssets.map(asset => (
          <Card
            key={asset.id}
            className="bg-zinc-900 border-zinc-800 hover:border-zinc-700 transition-all duration-200 group"
          >
            <CardHeader className="p-0">
              {/* Thumbnail with hover zoom effect */}
              <div className="relative aspect-video bg-zinc-800 rounded-t-lg overflow-hidden group-hover:scale-105 transition-transform duration-200">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-zinc-600">{asset.icon}</div>
                </div>
                {/* Optional: Add placeholder image overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-zinc-900/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
              </div>
            </CardHeader>

            <CardContent className="p-4">
              {/* Asset Title */}
              <div className="mb-3">
                <h3 className="text-zinc-100 font-semibold text-lg mb-1">{asset.title}</h3>
                <p className="text-zinc-500 text-sm">Created: {asset.createdDate}</p>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDownload(asset.id)}
                  className="flex-1 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>

                {asset.type === 'social' && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDeploy(asset.id)}
                    className="flex-1 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors"
                  >
                    <ArrowRight className="h-4 w-4 mr-2" />
                    Deploy
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredAssets.length === 0 && (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="text-zinc-500 text-center">
            <div className="mb-4">
              <FileText className="h-12 w-12 mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-zinc-400 mb-2">No assets found</h3>
            <p className="text-zinc-600 mb-6">Try changing the filter or generate new content</p>
            <Button onClick={handleGenerateNew} className="bg-emerald-600 hover:bg-emerald-500 text-white">
              Generate New Content
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}

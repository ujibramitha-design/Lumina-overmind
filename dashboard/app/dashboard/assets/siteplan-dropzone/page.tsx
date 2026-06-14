'use client'

import React, { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Upload,
  File,
  Image,
  Video,
  FileText,
  Box,
  CheckCircle,
  AlertCircle,
  Clock,
  Play,
  Download,
  Trash2,
  RefreshCw,
  Eye,
  Filter,
} from 'lucide-react'

interface SiteplanAsset {
  id: string
  project_name: string
  file_type: string
  file_size?: number
  status: string
  uploaded_at: string
  processed_at?: string
  completed_at?: string
  file_url?: string
}

interface UploadProgress {
  id: string
  project_name: string
  progress: number
  status: 'uploading' | 'processing' | 'completed' | 'error'
  error?: string
}

const SiteplanDropzone = () => {
  const [assets, setAssets] = useState<SiteplanAsset[]>([])
  const [uploadProgress, setUploadProgress] = useState<UploadProgress[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const [_selectedFiles, setSelectedFiles] = useState<FileList | null>(null)
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterType, setFilterType] = useState<string>('all')
  const [isLoading, setIsLoading] = useState(false)

  // Fetch assets on component mount
  React.useEffect(() => {
    fetchAssets()
  }, [])

  const fetchAssets = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/assets/siteplans')
      if (response.ok) {
        const data = await response.json()
        setAssets(data)
      }
    } catch (error) {
      console.error('Failed to fetch assets:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      setSelectedFiles(files)
      handleFileUpload(files)
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      setSelectedFiles(files)
      handleFileUpload(files)
    }
  }

  const handleFileUpload = async (files: FileList) => {
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      const progressId = `upload-${Date.now()}-${i}`

      // Add progress tracker
      setUploadProgress(prev => [
        ...prev,
        {
          id: progressId,
          project_name: file.name,
          progress: 0,
          status: 'uploading',
        },
      ])

      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('project_name', file.name.replace(/\.[^/.]+$/, ''))

        // Simulate progress
        const progressInterval = setInterval(() => {
          setUploadProgress(prev =>
            prev.map(p => (p.id === progressId ? { ...p, progress: Math.min(p.progress + 10, 90) } : p))
          )
        }, 200)

        const response = await fetch('/api/assets/upload-siteplan', {
          method: 'POST',
          body: formData,
        })

        clearInterval(progressInterval)

        if (response.ok) {
          await response.json()

          setUploadProgress(prev =>
            prev.map(p => (p.id === progressId ? { ...p, progress: 100, status: 'completed' } : p))
          )

          // Refresh assets list
          fetchAssets()

          // Remove progress after delay
          setTimeout(() => {
            setUploadProgress(prev => prev.filter(p => p.id !== progressId))
          }, 2000)
        } else {
          throw new Error('Upload failed')
        }
      } catch (error) {
        setUploadProgress(prev =>
          prev.map(p => (p.id === progressId ? { ...p, status: 'error', error: 'Upload failed' } : p))
        )

        setTimeout(() => {
          setUploadProgress(prev => prev.filter(p => p.id !== progressId))
        }, 3000)
      }
    }
  }

  const triggerVFXProcessing = async (assetId: string) => {
    try {
      const response = await fetch(`/api/assets/siteplans/${assetId}/process`, {
        method: 'POST',
      })

      if (response.ok) {
        fetchAssets() // Refresh to show updated status
      }
    } catch (error) {
      console.error('Failed to trigger VFX processing:', error)
    }
  }

  const deleteAsset = async (assetId: string) => {
    if (!confirm('Are you sure you want to delete this asset?')) return

    try {
      const response = await fetch(`/api/assets/siteplans/${assetId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        fetchAssets() // Refresh to show updated list
      }
    } catch (error) {
      console.error('Failed to delete asset:', error)
    }
  }

  const downloadAsset = async (assetId: string) => {
    try {
      const response = await fetch(`/api/assets/siteplans/${assetId}/download`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `siteplan-${assetId}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
      }
    } catch (error) {
      console.error('Failed to download asset:', error)
    }
  }

  const getFileIcon = (fileType: string) => {
    switch (fileType) {
      case 'IMAGE':
        return <Image className="w-5 h-5" />
      case 'VIDEO':
        return <Video className="w-5 h-5" />
      case 'PDF':
        return <FileText className="w-5 h-5" />
      case '3D_MODEL':
        return <Box className="w-5 h-5" />
      default:
        return <File className="w-5 h-5" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'READY_FOR_VFX':
        return 'text-blue-500 bg-blue-500/20'
      case 'RENDERING':
        return 'text-yellow-500 bg-yellow-500/20'
      case 'PUBLISHED':
        return 'text-green-500 bg-green-500/20'
      case 'FAILED':
        return 'text-red-500 bg-red-500/20'
      default:
        return 'text-gray-500 bg-gray-500/20'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'READY_FOR_VFX':
        return <Clock className="w-4 h-4" />
      case 'RENDERING':
        return <RefreshCw className="w-4 h-4 animate-spin" />
      case 'PUBLISHED':
        return <CheckCircle className="w-4 h-4" />
      case 'FAILED':
        return <AlertCircle className="w-4 h-4" />
      default:
        return <Clock className="w-4 h-4" />
    }
  }

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'Unknown'
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i]
  }

  const filteredAssets = assets.filter(asset => {
    if (filterStatus !== 'all' && asset.status !== filterStatus) return false
    if (filterType !== 'all' && asset.file_type !== filterType) return false
    return true
  })

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">🚁 Siteplan Dropzone</h1>
          <p className="text-gray-400">Import completed siteplans from Archidep system for VFX processing</p>
        </div>

        {/* Upload Area */}
        <div className="mb-8">
          <motion.div
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
              isDragging ? 'border-blue-500 bg-blue-500/10' : 'border-gray-600 bg-gray-800/50 hover:border-gray-500'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <h3 className="text-xl font-semibold mb-2">
              {isDragging ? 'Drop files here' : 'Drag & Drop Siteplan Files'}
            </h3>
            <p className="text-gray-400 mb-4">or click to browse files</p>
            <input
              type="file"
              multiple
              accept=".jpg,.jpeg,.png,.gif,.bmp,.webp,.pdf,.obj,.fbx,.dae,.3ds,.blend,.mp4,.mov,.avi"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg cursor-pointer transition-colors"
            >
              <Upload className="w-5 h-5 mr-2" />
              Browse Files
            </label>
            <p className="text-sm text-gray-500 mt-4">Supported formats: Images, 3D Models, PDFs, Videos (Max 100MB)</p>
          </motion.div>
        </div>

        {/* Upload Progress */}
        <AnimatePresence>
          {uploadProgress.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mb-8"
            >
              <h3 className="text-lg font-semibold mb-4">Upload Progress</h3>
              <div className="space-y-3">
                {uploadProgress.map(progress => (
                  <motion.div
                    key={progress.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-gray-800 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">{progress.project_name}</span>
                      <span
                        className={`text-sm ${
                          progress.status === 'completed'
                            ? 'text-green-500'
                            : progress.status === 'error'
                              ? 'text-red-500'
                              : 'text-blue-500'
                        }`}
                      >
                        {progress.status === 'uploading' && `${progress.progress}%`}
                        {progress.status === 'processing' && 'Processing...'}
                        {progress.status === 'completed' && 'Completed'}
                        {progress.status === 'error' && 'Error'}
                      </span>
                    </div>
                    {progress.status === 'uploading' && (
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <motion.div
                          className="bg-blue-500 h-2 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${progress.progress}%` }}
                          transition={{ duration: 0.3 }}
                        />
                      </div>
                    )}
                    {progress.error && <p className="text-red-500 text-sm mt-2">{progress.error}</p>}
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Filters */}
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={filterStatus}
                onChange={e => setFilterStatus(e.target.value)}
                className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white"
              >
                <option value="all">All Status</option>
                <option value="READY_FOR_VFX">Ready for VFX</option>
                <option value="RENDERING">Rendering</option>
                <option value="PUBLISHED">Published</option>
                <option value="FAILED">Failed</option>
              </select>
            </div>
            <select
              value={filterType}
              onChange={e => setFilterType(e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white"
            >
              <option value="all">All Types</option>
              <option value="IMAGE">Images</option>
              <option value="3D_MODEL">3D Models</option>
              <option value="PDF">PDFs</option>
              <option value="VIDEO">Videos</option>
            </select>
          </div>
          <button
            onClick={fetchAssets}
            className="flex items-center px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <RefreshCw className="w-5 h-5 mr-2" />
            Refresh
          </button>
        </div>

        {/* Assets Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? (
            <div className="col-span-full text-center py-12">
              <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-gray-400" />
              <p className="text-gray-400">Loading assets...</p>
            </div>
          ) : filteredAssets.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <Box className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p className="text-gray-400">No assets found</p>
              <p className="text-gray-500 text-sm mt-2">Upload your first siteplan to get started</p>
            </div>
          ) : (
            filteredAssets.map(asset => (
              <motion.div
                key={asset.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-gray-800 rounded-lg p-6 border border-gray-700"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${getStatusColor(asset.status)}`}>
                      {getFileIcon(asset.file_type)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-white">{asset.project_name}</h3>
                      <p className="text-sm text-gray-400">{asset.file_type}</p>
                    </div>
                  </div>
                  <div
                    className={`px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(asset.status)}`}
                  >
                    {getStatusIcon(asset.status)}
                    <span>{asset.status.replace('_', ' ')}</span>
                  </div>
                </div>

                <div className="space-y-2 text-sm text-gray-400 mb-4">
                  <div className="flex justify-between">
                    <span>Size:</span>
                    <span>{formatFileSize(asset.file_size)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Uploaded:</span>
                    <span>{new Date(asset.uploaded_at).toLocaleDateString()}</span>
                  </div>
                  {asset.processed_at && (
                    <div className="flex justify-between">
                      <span>Processed:</span>
                      <span>{new Date(asset.processed_at).toLocaleDateString()}</span>
                    </div>
                  )}
                </div>

                <div className="flex space-x-2">
                  {asset.status === 'READY_FOR_VFX' && (
                    <button
                      onClick={() => triggerVFXProcessing(asset.id)}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded text-sm transition-colors flex items-center justify-center"
                    >
                      <Play className="w-4 h-4 mr-1" />
                      Process
                    </button>
                  )}
                  {asset.status === 'PUBLISHED' && (
                    <button
                      onClick={() => downloadAsset(asset.id)}
                      className="flex-1 bg-green-600 hover:bg-green-700 px-3 py-2 rounded text-sm transition-colors flex items-center justify-center"
                    >
                      <Download className="w-4 h-4 mr-1" />
                      Download
                    </button>
                  )}
                  <button
                    onClick={() => downloadAsset(asset.id)}
                    className="flex-1 bg-gray-700 hover:bg-gray-600 px-3 py-2 rounded text-sm transition-colors flex items-center justify-center"
                  >
                    <Eye className="w-4 h-4 mr-1" />
                    View
                  </button>
                  <button
                    onClick={() => deleteAsset(asset.id)}
                    className="bg-red-600 hover:bg-red-700 px-3 py-2 rounded text-sm transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default SiteplanDropzone

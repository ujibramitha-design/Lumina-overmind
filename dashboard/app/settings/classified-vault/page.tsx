// @ts-nocheck
'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Shield, Key, Eye, EyeOff, Lock, Unlock, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react'

// Types
interface ConfigKey {
  id: string
  key_name: string
  description: string | null
  category: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface FormData {
  key_name: string
  key_value: string
  description: string
  category: string
}

const ClassifiedVault = () => {
  const [keys, setKeys] = useState<ConfigKey[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingKey, setEditingKey] = useState<ConfigKey | null>(null)
  const [showValues, setShowValues] = useState<{ [key: string]: boolean }>({})
  const [formData, setFormData] = useState<FormData>({
    key_name: '',
    key_value: '',
    description: '',
    category: 'API_KEYS',
  })
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null)

  // Predefined API keys
  const predefinedKeys = [
    { name: 'OPENAI_API_KEY', description: 'OpenAI GPT API Key for AI processing', category: 'API_KEYS' },
    { name: 'GEMINI_API_KEY', description: 'Google Gemini API Key for AI sentiment analysis', category: 'API_KEYS' },
    { name: 'TELEGRAM_BOT_TOKEN', description: 'Telegram Bot Token for notifications', category: 'API_KEYS' },
    { name: 'TELEGRAM_CHAT_ID', description: 'Telegram Chat ID for message routing', category: 'API_KEYS' },
    { name: 'TWILIO_ACCOUNT_SID', description: 'Twilio Account SID for WhatsApp Gateway', category: 'API_KEYS' },
    { name: 'TWILIO_AUTH_TOKEN', description: 'Twilio Auth Token for WhatsApp Gateway', category: 'API_KEYS' },
    { name: 'TWILIO_WHATSAPP_NUMBER', description: 'Twilio WhatsApp Number for messaging', category: 'API_KEYS' },
    { name: 'EXA_API_KEY', description: 'Exa.ai Search API Key for web search', category: 'API_KEYS' },
    { name: 'FIRECRAWL_API_KEY', description: 'Firecrawl API Key for web scraping', category: 'API_KEYS' },
    { name: 'ENCRYPTION_KEY', description: 'Data encryption key for sensitive data', category: 'SECURITY' },
  ]

  useEffect(() => {
    fetchKeys()
  }, [])

  const fetchKeys = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/config-vault/keys')
      if (response.ok) {
        const data = await response.json()
        setKeys(data)
      } else {
        showNotification('error', 'Failed to fetch keys')
      }
    } catch (error) {
      showNotification('error', 'Network error')
    } finally {
      setLoading(false)
    }
  }

  const showNotification = (type: 'success' | 'error', message: string) => {
    setNotification({ type, message })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const url = editingKey ? `/api/config-vault/keys/${editingKey.key_name}` : '/api/config-vault/keys'

      const method = editingKey ? 'PUT' : 'POST'
      const payload = editingKey ? { key_value: formData.key_value, description: formData.description } : formData

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        showNotification('success', editingKey ? 'Key updated successfully' : 'Key created successfully')
        setShowForm(false)
        setEditingKey(null)
        setFormData({ key_name: '', key_value: '', description: '', category: 'API_KEYS' })
        fetchKeys()
      } else {
        const error = await response.json()
        showNotification('error', error.detail || 'Operation failed')
      }
    } catch (error) {
      showNotification('error', 'Network error')
    }
  }

  const handleEdit = (key: ConfigKey) => {
    setEditingKey(key)
    setFormData({
      key_name: key.key_name,
      key_value: '',
      description: key.description || '',
      category: key.category,
    })
    setShowForm(true)
  }

  const handleDelete = async (keyName: string) => {
    if (!confirm(`Are you sure you want to delete ${keyName}?`)) return

    try {
      const response = await fetch(`/api/config-vault/keys/${keyName}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        showNotification('success', 'Key deleted successfully')
        fetchKeys()
      } else {
        showNotification('error', 'Failed to delete key')
      }
    } catch (error) {
      showNotification('error', 'Network error')
    }
  }

  const handleTest = async (keyName: string) => {
    try {
      const response = await fetch(`/api/config-vault/keys/${keyName}/test`, {
        method: 'POST',
      })

      if (response.ok) {
        const result = await response.json()
        showNotification('success', result.message)
      } else {
        showNotification('error', 'Key test failed')
      }
    } catch (error) {
      showNotification('error', 'Network error')
    }
  }

  const toggleShowValue = (keyId: string) => {
    setShowValues(prev => ({ ...prev, [keyId]: !prev[keyId] }))
  }

  const fillPredefinedKey = (predefined: (typeof predefinedKeys)[0]) => {
    setFormData({
      key_name: predefined.name,
      key_value: '',
      description: predefined.description,
      category: predefined.category,
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4" />
          <p>Loading Classified Vault...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-red-600 rounded-lg">
              <Shield className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-red-500">CLASSIFIED VAULT</h1>
              <p className="text-gray-400">Secure API Key Management System</p>
            </div>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors"
          >
            <Key className="w-5 h-5" />
            <span>Add New Key</span>
          </button>
        </div>

        {/* Notification */}
        <AnimatePresence>
          {notification && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              // @ts-ignore - Framer Motion className type issue
              className={`mb-6 p-4 rounded-lg flex items-center space-x-3 ${
                notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'
              }`}
            >
              {notification.type === 'success' ? (
                <CheckCircle className="w-5 h-5" />
              ) : (
                <AlertTriangle className="w-5 h-5" />
              )}
              <span>{notification.message}</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Keys Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {keys.map(key => (
            <motion.div
              key={key.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              // @ts-ignore - Framer Motion className type issue
              className="bg-gray-800 rounded-lg p-6 border border-gray-700"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Key className="w-5 h-5 text-red-500" />
                  <h3 className="font-semibold">{key.key_name}</h3>
                </div>
                <div className={`px-2 py-1 rounded text-xs ${key.is_active ? 'bg-green-600' : 'bg-gray-600'}`}>
                  {key.is_active ? 'Active' : 'Inactive'}
                </div>
              </div>

              <p className="text-gray-400 text-sm mb-4">{key.description}</p>

              <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
                <span>{key.category}</span>
                <span>{new Date(key.created_at).toLocaleDateString()}</span>
              </div>

              <div className="flex space-x-2">
                <button
                  onClick={() => handleEdit(key)}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded text-sm transition-colors"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleTest(key.key_name)}
                  className="flex-1 bg-green-600 hover:bg-green-700 px-3 py-2 rounded text-sm transition-colors"
                >
                  Test
                </button>
                <button
                  onClick={() => handleDelete(key.key_name)}
                  className="flex-1 bg-red-600 hover:bg-red-700 px-3 py-2 rounded text-sm transition-colors"
                >
                  Delete
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Add/Edit Form Modal */}
        <AnimatePresence>
          {(showForm || editingKey) && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-8 z-50"
              // @ts-ignore - Framer Motion className type issue
            >
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.95, opacity: 0 }}
                className="bg-gray-800 rounded-lg p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
                // @ts-ignore - Framer Motion className type issue
              >
                <h2 className="text-2xl font-bold mb-6 text-red-500">
                  {editingKey ? 'Edit API Key' : 'Add New API Key'}
                </h2>

                {/* Predefined Keys */}
                {!editingKey && (
                  <div className="mb-6">
                    <label className="block text-sm font-medium mb-2">Quick Fill (Predefined Keys)</label>
                    <div className="grid grid-cols-2 gap-2">
                      {predefinedKeys.map(predefined => (
                        <button
                          key={predefined.name}
                          onClick={() => fillPredefinedKey(predefined)}
                          className="text-left bg-gray-700 hover:bg-gray-600 p-2 rounded text-sm transition-colors"
                        >
                          <div className="font-medium">{predefined.name}</div>
                          <div className="text-xs text-gray-400">{predefined.description}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">Key Name</label>
                    <input
                      type="text"
                      value={formData.key_name}
                      onChange={e => setFormData({ ...formData, key_name: e.target.value })}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-red-500"
                      required
                      disabled={!!editingKey}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Key Value</label>
                    <div className="relative">
                      <input
                        type="password"
                        value={formData.key_value}
                        onChange={e => setFormData({ ...formData, key_value: e.target.value })}
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 pr-12 focus:outline-none focus:border-red-500"
                        required
                        placeholder="••••••••••••••••"
                      />
                      <div className="absolute right-3 top-2.5 text-gray-400">
                        <Lock className="w-5 h-5" />
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 mt-1">Key value will be encrypted before storage</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Description</label>
                    <textarea
                      value={formData.description}
                      onChange={e => setFormData({ ...formData, description: e.target.value })}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-red-500"
                      rows={3}
                      placeholder="Describe the purpose of this API key..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Category</label>
                    <select
                      value={formData.category}
                      onChange={e => setFormData({ ...formData, category: e.target.value })}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-red-500"
                    >
                      <option value="API_KEYS">API Keys</option>
                      <option value="SECURITY">Security</option>
                      <option value="VISUAL_CONFIG">Visual Config</option>
                      <option value="VR_CONFIG">VR Config</option>
                    </select>
                  </div>

                  <div className="flex space-x-4">
                    <button
                      type="submit"
                      className="flex-1 bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg transition-colors"
                    >
                      {editingKey ? 'Update Key' : 'Create Key'}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setShowForm(false)
                        setEditingKey(null)
                        setFormData({ key_name: '', key_value: '', description: '', category: 'API_KEYS' })
                      }}
                      className="flex-1 bg-gray-600 hover:bg-gray-700 px-6 py-3 rounded-lg transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default ClassifiedVault

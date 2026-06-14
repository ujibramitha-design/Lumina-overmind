'use client'

import React, { useState, useEffect } from 'react'
import {
  Phone,
  Building,
  Crown,
  Shield,
  ArrowRight,
  CheckCircle,
  MapPin,
  Users,
  Target,
  TrendingUp,
  Bot,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'

interface Project {
  id: string
  nama_proyek: string
  tipe_proyek: 'KOMERSIL' | 'SUBSIDI'
  lokasi: string
  harga_start: number
  target_market: string
}

export default function LandingPage() {
  const { toast } = useToast()
  const [projects, setProjects] = useState<Project[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form state
  const [formData, setFormData] = useState({
    nama: '',
    nomor_hp: '',
    project_id: '',
    project_type: 'KOMERSIL' as 'KOMERSIL' | 'SUBSIDI',
  })

  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await fetch('/api/projects?is_active=true')
      if (!response.ok) throw new Error('Failed to fetch projects')

      const data = await response.json()
      setProjects(data.data || [])
    } catch (error) {
      console.error('Error fetching projects:', error)
      setProjects([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus('idle')

    try {
      // Validate form
      if (!formData.nama.trim()) {
        toast({
          title: 'Error',
          description: 'Nama harus diisi',
          variant: 'destructive',
        })
        return
      }

      if (!formData.nomor_hp.trim()) {
        toast({
          title: 'Error',
          description: 'Nomor HP harus diisi',
          variant: 'destructive',
        })
        return
      }

      if (!formData.project_id) {
        toast({
          title: 'Error',
          description: 'Pilih proyek terlebih dahulu',
          variant: 'destructive',
        })
        return
      }

      // Submit to public webhook
      const response = await fetch('/api/leads/public-submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nama: formData.nama,
          nomor_hp: formData.nomor_hp,
          project_id: formData.project_id,
          project_type: formData.project_type,
          source: 'landing_page_public',
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to submit lead')
      }

      await response.json()

      setSubmitStatus('success')
      toast({
        title: 'Berhasil!',
        description: 'Data Anda telah kami terima. Tim kami akan segera menghubungi Anda.',
      })

      // Reset form
      setFormData({
        nama: '',
        nomor_hp: '',
        project_id: '',
        project_type: 'KOMERSIL',
      })
    } catch (error) {
      console.error('Error submitting lead:', error)
      setSubmitStatus('error')
      toast({
        title: 'Error',
        description: 'Terjadi kesalahan saat mengirim data. Silakan coba lagi.',
        variant: 'destructive',
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const getProjectIcon = (type: 'KOMERSIL' | 'SUBSIDI') => {
    return type === 'KOMERSIL' ? <Crown className="h-5 w-5" /> : <Shield className="h-5 w-5" />
  }

  const getProjectColor = (type: 'KOMERSIL' | 'SUBSIDI') => {
    return type === 'KOMERSIL'
      ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
      : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
  }

  const getProjectBgColor = (type: 'KOMERSIL' | 'SUBSIDI') => {
    return type === 'KOMERSIL'
      ? 'bg-gradient-to-r from-yellow-600/20 to-orange-600/20 border-yellow-500/30'
      : 'bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border-blue-500/30'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-pink-600/20"></div>
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="p-3 bg-gradient-to-r from-emerald-500 to-blue-600 rounded-2xl">
                <Building className="h-8 w-8 text-white" />
              </div>
            </div>

            <h1 className="text-4xl font-bold text-white mb-6">
              HUNTER AGENT AI
              <span className="text-2xl font-light block mt-2">Marketing Intelligence Platform</span>
            </h1>

            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Platform AI cerdas untuk mengidentifikasi prospek berkualitas tinggi melalui teknologi advanced scouting
              dan analisis data real-time.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3"
                onClick={() => document.getElementById('lead-form')?.scrollIntoView({ behavior: 'smooth' })}
              >
                <Users className="mr-2 h-5 w-5" />
                Mulai Sekarang
                <ArrowRight className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>

        {/* Animated background elements */}
        <div className="absolute top-0 left-0 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000"></div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-slate-800/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Fitur Unggulan</h2>
            <p className="text-gray-300 text-lg">Teknologi AI yang mengubah cara Anda menemukan prospek</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-emerald-500/20 rounded-lg">
                    <Target className="h-6 w-6 text-emerald-400" />
                  </div>
                  <CardTitle className="text-emerald-400">AI Scouting</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  Identifikasi prospek berkualitas tinggi dengan teknologi AI yang canggih dan akurat.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-gray-400">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-emerald-400" />
                    <span>Analisis intent otomatis</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-emerald-400" />
                    <span>Platform infiltration</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-emerald-400" />
                    <span>Data enrichment</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <TrendingUp className="h-6 w-6 text-blue-400" />
                  </div>
                  <CardTitle className="text-blue-400">Market Intelligence</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  Analisis pasar real-time dan insight kompetitif untuk strategi marketing yang lebih baik.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-gray-400">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-blue-400" />
                    <span>Trend analysis</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-blue-400" />
                    <span>Competitor monitoring</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-blue-400" />
                    <span>Market insights</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-500/20 rounded-lg">
                    <Bot className="h-6 w-6 text-purple-400" />
                  </div>
                  <CardTitle className="text-purple-400">AI Automation</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  Otomatisasi prospek nurturing dan follow-up dengan AI yang cerdas dan personal.
                </p>
                <ul className="mt-4 space-y-2 text-sm text-gray-400">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-purple-400" />
                    <span>Smart follow-up</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-purple-400" />
                    <span>Personal messaging</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-purple-400" />
                    <span>Conversion tracking</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Projects Showcase */}
      <div className="py-16 bg-slate-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Proyek Tersedia</h2>
            <p className="text-gray-300 text-lg">Pilih proyek yang sesuai dengan kebutuhan Anda</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map(project => (
              <Card
                key={project.id}
                className={`border-slate-700 overflow-hidden transition-all duration-300 hover:border-emerald-500/50 hover:shadow-2xl hover:shadow-emerald-500/20`}
              >
                <div className={`h-2 ${getProjectBgColor(project.tipe_proyek)}`}></div>
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {getProjectIcon(project.tipe_proyek)}
                      <CardTitle className="text-white">{project.nama_proyek}</CardTitle>
                    </div>
                    <Badge className={getProjectColor(project.tipe_proyek)}>{project.tipe_proyek}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-gray-400">
                      <MapPin className="h-4 w-4" />
                      <span className="text-sm">{project.lokasi}</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-400">
                      <Target className="h-4 w-4" />
                      <span className="text-sm">{project.target_market}</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-400">
                      <span className="text-sm font-mono">Rp {project.harga_start.toLocaleString('id-ID')}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}

            {projects.length === 0 && !isLoading && (
              <div className="col-span-full text-center py-12">
                <div className="text-gray-400">
                  <Building className="h-12 w-12 mx-auto mb-4" />
                  <p>Belum ada proyek tersedia</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Lead Capture Form */}
      <div id="lead-form" className="py-16 bg-slate-800/50 backdrop-blur-sm">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Tertarik Minat</h2>
            <p className="text-gray-300 text-lg">
              Isi data Anda dan tim kami akan segera menghubungi Anda untuk konsultasi lebih lanjut.
            </p>
          </div>

          <Card className="bg-slate-900/50 backdrop-blur-sm border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Phone className="h-5 w-5 text-emerald-400" />
                Form Tangkap Prospek
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="nama" className="block text-sm font-medium text-gray-300 mb-2">
                    Nama Lengkap
                  </label>
                  <Input
                    id="nama"
                    name="nama"
                    type="text"
                    placeholder="Masukkan nama lengkap Anda"
                    value={formData.nama}
                    onChange={handleInputChange}
                    className="bg-slate-800 border-slate-600 text-white placeholder:text-gray-400"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="nomor_hp" className="block text-sm font-medium text-gray-300 mb-2">
                    Nomor HP / WhatsApp
                  </label>
                  <Input
                    id="nomor_hp"
                    name="nomor_hp"
                    type="tel"
                    placeholder="Contoh: 08123456789"
                    value={formData.nomor_hp}
                    onChange={handleInputChange}
                    className="bg-slate-800 border-slate-600 text-white placeholder:text-gray-400"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="project_id" className="block text-sm font-medium text-gray-300 mb-2">
                    Pilih Proyek
                  </label>
                  <select
                    id="project_id"
                    name="project_id"
                    value={formData.project_id}
                    onChange={handleInputChange}
                    className="w-full bg-slate-800 border-slate-600 text-white rounded-lg px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500/20 focus:border-emerald-500"
                    required
                  >
                    <option value="">-- Pilih Proyek --</option>
                    {projects.map(project => (
                      <option key={project.id} value={project.id}>
                        {project.nama_proyek} - {project.tipe_proyek}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="project_type" className="block text-sm font-medium text-gray-300 mb-2">
                    Tipe Proyek
                  </label>
                  <select
                    id="project_type"
                    name="project_type"
                    value={formData.project_type}
                    onChange={handleInputChange}
                    className="w-full bg-slate-800 border-slate-600 text-white rounded-lg px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500/20 focus:border-emerald-500"
                    required
                  >
                    <option value="KOMERSIL">Komersil</option>
                    <option value="SUBSIDI">Subsidi</option>
                  </select>
                </div>

                <div className="flex gap-4">
                  <Button
                    type="submit"
                    disabled={isSubmitting}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-50"
                  >
                    {isSubmitting ? 'Mengirim...' : 'Kirim Data'}
                  </Button>

                  {submitStatus === 'success' && (
                    <div className="flex items-center gap-2 text-emerald-400">
                      <CheckCircle className="h-5 w-5" />
                      <span>Berhasil dikirim!</span>
                    </div>
                  )}

                  {submitStatus === 'error' && (
                    <div className="flex items-center gap-2 text-red-400">
                      <span>Gagal mengirim</span>
                    </div>
                  )}
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-slate-900/50 backdrop-blur-sm border-t border-slate-800 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-gray-400">
            <p>&copy; 2026 HUNTER AGENT AI. All rights reserved.</p>
            <p className="text-sm text-gray-500 mt-2">Platform AI Marketing Intelligence yang canggih dan inovatif.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

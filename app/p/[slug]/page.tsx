'use client'

/**
 * LUMINA OS - Sniper Web Dynamic Landing Page
 * ===========================================
 * 
 * Hyper-personalized landing page for each prospect
 * Premium Hacker/Dark Mode design with Emerald accents
 * Mobile-responsive with WhatsApp integration
 */

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Head from 'next/head'
import Link from 'next/link'
import { 
  Phone, 
  MapPin, 
  Home, 
  TrendingUp, 
  Clock, 
  CheckCircle,
  ArrowRight,
  Star,
  Shield,
  Zap,
  Target,
  Award,
  Building,
  DollarSign,
  Calendar,
  Users,
  MessageCircle,
  Lock,
  CreditCard,
  AlertCircle,
  Check
} from 'lucide-react'

interface LinkData {
  slug: string
  lead_id?: number
  lead_name: string
  budget?: string
  location?: string
  contact_info?: string
  created_at: string
  updated_at: string
  view_count: number
  status: string
  metadata?: string
}

interface PropertyData {
  title: string
  price: string
  location: string
  features: string[]
  specs: {
    bedrooms: number
    bathrooms: number
    land_area: string
    building_area: string
  }
  amenities: string[]
  investment: {
    roi: string
    appreciation: string
    timeline: string
  }
}

export default function SniperLandingPage() {
  const params = useParams()
  const slug = params.slug as string
  
  const [linkData, setLinkData] = useState<LinkData | null>(null)
  const [propertyData, setPropertyData] = useState<PropertyData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showWhatsApp, setShowWhatsApp] = useState(false)
  const [bookingLoading, setBookingLoading] = useState(false)
  const [bookingSuccess, setBookingSuccess] = useState(false)
  const [bookingError, setBookingError] = useState<string | null>(null)
  const [qrisUrl, setQrisUrl] = useState<string | null>(null)

  // Fetch personalized data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        
        // Fetch link data
        const linkResponse = await fetch(`/api/sniper-links/${slug}`)
        if (!linkResponse.ok) {
          throw new Error('Link tidak ditemukan atau sudah kadaluarsa')
        }
        
        const data: LinkData = await linkResponse.json()
        setLinkData(data)
        
        // Generate property data based on prospect info
        const property = generatePropertyData(data)
        setPropertyData(property)
        
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Terjadi kesalahan')
      } finally {
        setLoading(false)
      }
    }
    
    if (slug) {
      fetchData()
    }
  }, [slug])

  // Generate property data based on prospect information
  const generatePropertyData = (data: LinkData): PropertyData => {
    const name = data.lead_name
    const budget = data.budget || '300-500jt'
    const location = data.location || 'Serang'
    
    return {
      title: `Hunian Eksklusif ${location}`,
      price: `Rp ${budget}`,
      location: location,
      features: [
        'Lokasi Strategis dekat Pusat Kota',
        'Akses Tol dan Transportasi Publik',
        'Keamanan 24/7 dengan CCTV',
        'Taman Hijau dan Fasilitas Olahraga',
        'Smart Home System',
        'Solar Panel Ready'
      ],
      specs: {
        bedrooms: 3,
        bathrooms: 2,
        land_area: '120 m²',
        building_area: '90 m²'
      },
      amenities: [
        'Clubhouse Premium',
        'Kolam Renang',
        'Fitness Center',
        'Children Playground',
        'Commercial Area',
        'Jogging Track'
      ],
      investment: {
        roi: '12-15% per tahun',
        appreciation: '8-10% YoY',
        timeline: '3-5 tahun breakeven'
      }
    }
  }

  // WhatsApp message generator
  const generateWhatsAppMessage = () => {
    if (!linkData || !propertyData) return ''
    
    const message = `Halo, saya ${linkData.lead_name} tertarik dengan informasi properti di ${propertyData.location}. Mohon info lebih lanjut.`
    return encodeURIComponent(message)
  }

  const whatsappUrl = `https://wa.me/62812345678?text=${generateWhatsAppMessage()}`
  
  // Handle booking payment
  const handleBookingPayment = async () => {
    if (!linkData) return
    
    setBookingLoading(true)
    setBookingError(null)
    setQrisUrl(null)
    
    try {
      const response = await fetch('/api/payments/generate-qris', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lead_id: linkData.lead_id || slug,
          customer_name: linkData.lead_name,
          customer_email: linkData.contact_info?.includes('@') ? linkData.contact_info : undefined,
          customer_phone: linkData.contact_info?.match(/\d+/)?.[0] || undefined,
          nominal: 1000000, // Rp 1,000,000 booking fee
        }),
      })
      
      if (!response.ok) {
        throw new Error('Gagal membuat QRIS booking')
      }
      
      const result = await response.json()
      
      if (result.success) {
        setQrisUrl(result.qris_url)
        setBookingSuccess(true)
      } else {
        throw new Error(result.error || 'Gagal membuat QRIS')
      }
      
    } catch (err) {
      setBookingError(err instanceof Error ? err.message : 'Terjadi kesalahan')
    } finally {
      setBookingLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-emerald-400 text-lg">Memuat penawaran eksklusif...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <Target className="w-8 h-8 text-red-500" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">Link Tidak Valid</h1>
          <p className="text-gray-400 mb-6">{error}</p>
          <Link 
            href="/" 
            className="inline-flex items-center px-6 py-3 bg-emerald-500 text-black font-semibold rounded-lg hover:bg-emerald-400 transition-colors"
          >
            Kembali ke Beranda
          </Link>
        </div>
      </div>
    )
  }

  if (!linkData || !propertyData) {
    return null
  }

  return (
    <>
      <Head>
        <title>Penawaran Eksklusif Khusus untuk {linkData.lead_name} - Lumina OS</title>
        <meta name="description" content={`Penawaran hunian eksklusif khusus untuk ${linkData.lead_name} di ${propertyData.location}`} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-black text-white">
        {/* Header */}
        <header className="bg-gradient-to-r from-emerald-500/10 to-emerald-600/10 border-b border-emerald-500/20">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
                  <Home className="w-5 h-5 text-black" />
                </div>
                <span className="text-xl font-bold">Lumina OS</span>
              </div>
              <div className="flex items-center space-x-4 text-sm text-gray-400">
                <span>ID: {linkData.slug}</span>
                <span>•</span>
                <span>Dibuat: {new Date(linkData.created_at).toLocaleDateString('id-ID')}</span>
              </div>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/20 via-transparent to-purple-500/20"></div>
          <div className="relative container mx-auto px-4 py-16">
            <div className="text-center mb-12">
              <div className="inline-flex items-center px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-full mb-6">
                <Star className="w-4 h-4 text-emerald-400 mr-2" />
                <span className="text-emerald-400 text-sm font-medium">Penawaran Eksklusif</span>
              </div>
              
              <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-emerald-400 to-white bg-clip-text text-transparent">
                Penawaran Eksklusif Khusus untuk<br />
                <span className="text-5xl md:text-7xl">{linkData.lead_name}</span>
              </h1>
              
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Hunian premium di {propertyData.location} yang dirancang khusus untuk Anda
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={handleBookingPayment}
                  disabled={bookingLoading}
                  className="inline-flex items-center px-12 py-6 bg-gradient-to-r from-yellow-400 to-yellow-600 text-black font-bold rounded-lg hover:from-yellow-300 hover:to-yellow-500 transition-all transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {bookingLoading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin mr-3"></div>
                      Memproses...
                    </>
                  ) : (
                    <>
                      <Lock className="w-6 h-6 mr-3" />
                      🔒 AMANKAN UNIT - BAYAR BOOKING FEE SEKARANG
                    </>
                  )}
                </button>
                <a
                  href={whatsappUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-8 py-4 bg-emerald-500 text-black font-bold rounded-lg hover:bg-emerald-400 transition-all transform hover:scale-105"
                >
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Hubungi Konsultan
                </a>
              </div>
              
              {showWhatsApp && (
                <div className="mt-4 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
                  <p className="text-emerald-400 font-medium">WhatsApp: +62 812-3456-7890</p>
                  <p className="text-gray-400 text-sm mt-1">Konsultan siap membantu Anda 24/7</p>
                </div>
              )}
              
              {/* Booking Status Messages */}
              {bookingSuccess && qrisUrl && (
                <div className="mt-6 p-6 bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 border border-yellow-500/30 rounded-lg">
                  <div className="flex items-center mb-4">
                    <Check className="w-6 h-6 text-yellow-400 mr-3" />
                    <h3 className="text-xl font-bold text-yellow-400">Booking Fee QRIS Generated!</h3>
                  </div>
                  <p className="text-gray-300 mb-4">
                    Scan QRIS di bawah ini untuk membayar booking fee Rp 1.000.000 dan mengamankan unit Anda.
                  </p>
                  <div className="bg-white p-4 rounded-lg mb-4">
                    <div className="w-48 h-48 bg-gray-200 rounded flex items-center justify-center mx-auto">
                      <div className="text-center">
                        <CreditCard className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-500 text-sm">QRIS Code</p>
                        <p className="text-gray-400 text-xs mt-1">Scan to pay</p>
                      </div>
                    </div>
                  </div>
                  <a
                    href={qrisUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-6 py-3 bg-yellow-500 text-black font-semibold rounded-lg hover:bg-yellow-400 transition-colors"
                  >
                    <CreditCard className="w-5 h-5 mr-2" />
                    Buka QRIS di Browser
                  </a>
                </div>
              )}
              
              {bookingError && (
                <div className="mt-6 p-6 bg-red-500/10 border border-red-500/30 rounded-lg">
                  <div className="flex items-center mb-2">
                    <AlertCircle className="w-6 h-6 text-red-400 mr-3" />
                    <h3 className="text-xl font-bold text-red-400">Booking Error</h3>
                  </div>
                  <p className="text-gray-300">{bookingError}</p>
                  <button
                    onClick={handleBookingPayment}
                    className="mt-4 px-6 py-2 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors"
                  >
                    Coba Lagi
                  </button>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Property Details */}
        <section className="py-16 bg-gradient-to-b from-black to-gray-900">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-2 gap-12">
              {/* Left Column */}
              <div>
                <h2 className="text-3xl font-bold mb-6 text-emerald-400">{propertyData.title}</h2>
                
                <div className="mb-8">
                  <div className="flex items-center mb-4">
                    <DollarSign className="w-5 h-5 text-emerald-400 mr-2" />
                    <span className="text-2xl font-bold text-white">{propertyData.price}</span>
                  </div>
                  <div className="flex items-center mb-4">
                    <MapPin className="w-5 h-5 text-emerald-400 mr-2" />
                    <span className="text-gray-300">{propertyData.location}</span>
                  </div>
                  <div className="flex items-center">
                    <Calendar className="w-5 h-5 text-emerald-400 mr-2" />
                    <span className="text-gray-300">Ready Stock</span>
                  </div>
                </div>

                <div className="mb-8">
                  <h3 className="text-xl font-semibold mb-4 text-emerald-400">Spesifikasi</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                      <div className="text-2xl font-bold text-emerald-400">{propertyData.specs.bedrooms}</div>
                      <div className="text-gray-400 text-sm">Kamar Tidur</div>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                      <div className="text-2xl font-bold text-emerald-400">{propertyData.specs.bathrooms}</div>
                      <div className="text-gray-400 text-sm">Kamar Mandi</div>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                      <div className="text-2xl font-bold text-emerald-400">{propertyData.specs.land_area}</div>
                      <div className="text-gray-400 text-sm">Luas Tanah</div>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                      <div className="text-2xl font-bold text-emerald-400">{propertyData.specs.building_area}</div>
                      <div className="text-gray-400 text-sm">Luas Bangunan</div>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-4 text-emerald-400">Fitur Unggulan</h3>
                  <ul className="space-y-2">
                    {propertyData.features.map((feature, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="w-5 h-5 text-emerald-400 mr-3 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-300">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Right Column */}
              <div>
                <div className="bg-gradient-to-br from-emerald-500/10 to-purple-500/10 border border-emerald-500/30 rounded-2xl p-8 mb-8">
                  <h3 className="text-2xl font-bold mb-6 text-emerald-400">Investment Opportunity</h3>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">ROI Tahunan</span>
                      <span className="text-xl font-bold text-emerald-400">{propertyData.investment.roi}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Appresiasi</span>
                      <span className="text-xl font-bold text-emerald-400">{propertyData.investment.appreciation}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Breakeven</span>
                      <span className="text-xl font-bold text-emerald-400">{propertyData.investment.timeline}</span>
                    </div>
                  </div>
                  
                  <div className="mt-6 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
                    <div className="flex items-center mb-2">
                      <TrendingUp className="w-5 h-5 text-emerald-400 mr-2" />
                      <span className="text-emerald-400 font-medium">Market Analysis</span>
                    </div>
                    <p className="text-gray-300 text-sm">
                      Area {propertyData.location} menunjukkan pertumbuhan nilai properti 15% YoY dengan infrastruktur baru yang akan selesai 2024.
                    </p>
                  </div>
                </div>

                <div className="bg-gray-800/50 border border-gray-700 rounded-2xl p-8">
                  <h3 className="text-xl font-semibold mb-6 text-emerald-400">Fasilitas Premium</h3>
                  <div className="grid grid-cols-2 gap-4">
                    {propertyData.amenities.map((amenity, index) => (
                      <div key={index} className="flex items-center">
                        <Shield className="w-4 h-4 text-emerald-400 mr-2" />
                        <span className="text-gray-300 text-sm">{amenity}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-emerald-500/20 to-purple-500/20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Siap untuk Langkah Selanjutnya?</h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Konsultan properti kami siap membantu Anda mewujudkan hunian impian di {propertyData.location}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href={whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-8 py-4 bg-emerald-500 text-black font-bold rounded-lg hover:bg-emerald-400 transition-all transform hover:scale-105"
              >
                <MessageCircle className="w-5 h-5 mr-2" />
                Mulai Konsultasi Sekarang
              </a>
              <button className="inline-flex items-center px-8 py-4 border border-emerald-500 text-emerald-400 font-semibold rounded-lg hover:bg-emerald-500/10 transition-all">
                <Calendar className="w-5 h-5 mr-2" />
                Jadwalkan Survey Lokasi
              </button>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-8 bg-black border-t border-gray-800">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center justify-between">
              <div className="flex items-center space-x-2 mb-4 md:mb-0">
                <div className="w-6 h-6 bg-emerald-500 rounded-lg flex items-center justify-center">
                  <Home className="w-4 h-4 text-black" />
                </div>
                <span className="text-white font-semibold">Lumina OS</span>
              </div>
              <div className="text-gray-400 text-sm">
                © 2024 Lumina OS. Penawaran eksklusif untuk {linkData.lead_name}
              </div>
            </div>
          </div>
        </footer>

        {/* Floating WhatsApp Button */}
        <div className="fixed bottom-6 right-6 z-50">
          <a
            href={whatsappUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-emerald-500 text-black p-4 rounded-full shadow-lg hover:bg-emerald-400 transition-all transform hover:scale-110"
          >
            <MessageCircle className="w-6 h-6" />
          </a>
        </div>
      </div>
    </>
  )
}

'use client'

import dynamic from 'next/dynamic'

// Dynamic import to avoid SSR issues with Leaflet
const MapContainer = dynamic(
  () => import('react-leaflet').then((mod) => mod.MapContainer),
  { ssr: false }
)
const TileLayer = dynamic(
  () => import('react-leaflet').then((mod) => mod.TileLayer),
  { ssr: false }
)
const Marker = dynamic(
  () => import('react-leaflet').then((mod) => mod.Marker),
  { ssr: false }
)
const Popup = dynamic(
  () => import('react-leaflet').then((mod) => mod.Popup),
  { ssr: false }
)

interface Property {
  id: string
  name: string
  location: string
  lat: number
  lng: number
  price?: number
  leadsCount?: number
}

interface PropertyMapProps {
  properties: Property[]
  center?: [number, number]
  zoom?: number
  height?: string
}

export function PropertyMap({
  properties,
  center = [-6.2088, 106.8456], // Default: Jakarta
  zoom = 12,
  height = '400px',
}: PropertyMapProps) {
  return (
    <div style={{ height, width: '100%' }}>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {properties.map((property) => (
          <Marker
            key={property.id}
            position={[property.lat, property.lng]}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-bold text-sm">{property.name}</h3>
                <p className="text-xs text-gray-600">{property.location}</p>
                {property.price && (
                  <p className="text-xs font-semibold">
                    Price: Rp{property.price.toLocaleString()}
                  </p>
                )}
                {property.leadsCount !== undefined && (
                  <p className="text-xs">Leads: {property.leadsCount}</p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}

// @ts-nocheck - react-leaflet type definitions issue
'use client'

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

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
      {/* @ts-ignore - react-leaflet type definitions issue */}
      {/* @ts-ignore - center prop type issue */}
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

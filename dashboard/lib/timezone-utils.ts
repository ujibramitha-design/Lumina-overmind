/**
 * Utilitas untuk timezone support
 * Mendukung multi-timezone untuk operasi Asia
 */

import { format, toZonedTime, fromZonedTime } from 'date-fns-tz'

export interface TimezoneInfo {
  id: string
  name: string
  offset: string
  region: string
}

export interface ScheduledEvent {
  id: string
  title: string
  startDateTime: Date
  endDateTime: Date
  timezone: string
  attendees: string[]
}

// Daftar timezone yang didukung (fokus Asia)
export const SUPPORTED_TIMEZONES: TimezoneInfo[] = [
  {
    id: 'Asia/Jakarta',
    name: 'Jakarta (WIB)',
    offset: 'UTC+7',
    region: 'Indonesia'
  },
  {
    id: 'Asia/Makassar',
    name: 'Makassar (WITA)',
    offset: 'UTC+8',
    region: 'Indonesia'
  },
  {
    id: 'Asia/Jayapura',
    name: 'Jayapura (WIT)',
    offset: 'UTC+9',
    region: 'Indonesia'
  },
  {
    id: 'Asia/Singapore',
    name: 'Singapore',
    offset: 'UTC+8',
    region: 'Singapore'
  },
  {
    id: 'Asia/Kuala_Lumpur',
    name: 'Kuala Lumpur',
    offset: 'UTC+8',
    region: 'Malaysia'
  },
  {
    id: 'Asia/Bangkok',
    name: 'Bangkok',
    offset: 'UTC+7',
    region: 'Thailand'
  },
  {
    id: 'Asia/Ho_Chi_Minh',
    name: 'Ho Chi Minh City',
    offset: 'UTC+7',
    region: 'Vietnam'
  },
  {
    id: 'Asia/Manila',
    name: 'Manila',
    offset: 'UTC+8',
    region: 'Philippines'
  },
  {
    id: 'Asia/Tokyo',
    name: 'Tokyo',
    offset: 'UTC+9',
    region: 'Japan'
  },
  {
    id: 'Asia/Seoul',
    name: 'Seoul',
    offset: 'UTC+9',
    region: 'South Korea'
  },
  {
    id: 'Asia/Shanghai',
    name: 'Shanghai',
    offset: 'UTC+8',
    region: 'China'
  },
  {
    id: 'Asia/Hong_Kong',
    name: 'Hong Kong',
    offset: 'UTC+8',
    region: 'Hong Kong'
  },
  {
    id: 'Asia/Dubai',
    name: 'Dubai',
    offset: 'UTC+4',
    region: 'UAE'
  },
  {
    id: 'Asia/Riyadh',
    name: 'Riyadh',
    offset: 'UTC+3',
    region: 'Saudi Arabia'
  },
  {
    id: 'Asia/Mumbai',
    name: 'Mumbai',
    offset: 'UTC+5:30',
    region: 'India'
  }
]

/**
 * Mendapatkan timezone default berdasarkan region
 * @param region - Region (contoh: 'Indonesia', 'Singapore')
 * @returns Timezone ID
 */
export function getDefaultTimezone(region: string = 'Indonesia'): string {
  const timezone = SUPPORTED_TIMEZONES.find(tz => tz.region === region)
  return timezone?.id || 'Asia/Jakarta'
}

/**
 * Konversi datetime dari UTC ke timezone tertentu
 * @param date - Date dalam UTC
 * @param timezone - Timezone target
 * @returns Date dalam timezone target
 */
export function convertToTimezone(date: Date, timezone: string): Date {
  return toZonedTime(date, timezone)
}

/**
 * Konversi datetime dari timezone tertentu ke UTC
 * @param date - Date dalam timezone source
 * @param timezone - Timezone source
 * @returns Date dalam UTC
 */
export function convertToUTC(date: Date, timezone: string): Date {
  return fromZonedTime(date, timezone)
}

/**
 * Format datetime dengan timezone
 * @param date - Date
 * @param timezone - Timezone
 * @param formatString - Format string (date-fns)
 * @returns Formatted datetime string
 */
export function formatWithTimezone(
  date: Date,
  timezone: string,
  formatString: string = 'yyyy-MM-dd HH:mm:ss'
): string {
  const zonedDate = toZonedTime(date, timezone)
  return format(zonedDate, formatString, { timeZone: timezone })
}

/**
 * Mendapatkan offset timezone dalam format string
 * @param timezone - Timezone ID
 * @returns Offset string (contoh: 'UTC+7')
 */
export function getTimezoneOffset(timezone: string): string {
  const tzInfo = SUPPORTED_TIMEZONES.find(tz => tz.id === timezone)
  return tzInfo?.offset || 'UTC+0'
}

/**
 * Cek apakah dua datetime dalam timezone yang sama
 * @param date1 - Date pertama
 * @param date2 - Date kedua
 * @param timezone - Timezone untuk perbandingan
 * @returns Boolean
 */
export function isSameTimezone(date1: Date, date2: Date, timezone: string): boolean {
  const zoned1 = formatWithTimezone(date1, timezone, 'yyyy-MM-dd HH:mm')
  const zoned2 = formatWithTimezone(date2, timezone, 'yyyy-MM-dd HH:mm')
  return zoned1 === zoned2
}

/**
 * Mendapatkan overlap waktu antara dua timezone
 * @param startTime - Start time
 * @param endTime - End time
 * @param timezone1 - Timezone pertama
 * @param timezone2 - Timezone kedua
 * @returns Overlap information
 */
export function getTimezoneOverlap(
  startTime: Date,
  endTime: Date,
  timezone1: string,
  timezone2: string
): {
  overlapStart: Date
  overlapEnd: Date
  hasOverlap: boolean
} {
  const start1 = convertToTimezone(startTime, timezone1)
  const end1 = convertToTimezone(endTime, timezone1)
  const start2 = convertToTimezone(startTime, timezone2)
  const end2 = convertToTimezone(endTime, timezone2)
  
  const overlapStart = start1 > start2 ? start1 : start2
  const overlapEnd = end1 < end2 ? end1 : end2
  const hasOverlap = overlapStart < overlapEnd
  
  return {
    overlapStart,
    overlapEnd,
    hasOverlap
  }
}

/**
 * Mendapatkan jam kerja yang overlap antara dua timezone
 * @param timezone1 - Timezone pertama
 * @param timezone2 - Timezone kedua
 * @returns Overlap working hours
 */
export function getWorkingHoursOverlap(
  timezone1: string,
  timezone2: string
): {
  overlapStart: string
  overlapEnd: string
  overlapHours: number
} {
  // Asumsi jam kerja 09:00 - 17:00
  const workingHours = {
    start: 9,
    end: 17
  }
  
  const offset1 = parseInt(getTimezoneOffset(timezone1).replace('UTC+', '').replace('UTC-', ''))
  const offset2 = parseInt(getTimezoneOffset(timezone2).replace('UTC+', '').replace('UTC-', ''))
  
  const start1 = workingHours.start + offset1
  const end1 = workingHours.end + offset1
  const start2 = workingHours.start + offset2
  const end2 = workingHours.end + offset2
  
  const overlapStart = Math.max(start1, start2)
  const overlapEnd = Math.min(end1, end2)
  const overlapHours = Math.max(0, overlapEnd - overlapStart)
  
  return {
    overlapStart: `${Math.floor(overlapStart % 24)}:${String((overlapStart % 1) * 60).padStart(2, '0')}`,
    overlapEnd: `${Math.floor(overlapEnd % 24)}:${String((overlapEnd % 1) * 60).padStart(2, '0')}`,
    overlapHours
  }
}

/**
 * Jadwalkan event dengan timezone awareness
 * @param event - Event data
 * @param targetTimezone - Timezone target untuk display
 * @returns Event dengan timezone yang dikonversi
 */
export function scheduleEventWithTimezone(
  event: ScheduledEvent,
  targetTimezone: string
): ScheduledEvent {
  const startInTarget = convertToTimezone(event.startDateTime, targetTimezone)
  const endInTarget = convertToTimezone(event.endDateTime, targetTimezone)
  
  return {
    ...event,
    startDateTime: startInTarget,
    endDateTime: endInTarget,
    timezone: targetTimezone
  }
}

/**
 * Mendapatkan rekomendasi waktu meeting terbaik
 * @param timezones - Daftar timezone yang terlibat
 * @returns Rekomendasi waktu meeting
 */
export function getBestMeetingTime(timezones: string[]): {
  recommendedTime: string
  reason: string
  alternatives: string[]
} {
  if (timezones.length === 0) {
    return {
      recommendedTime: '09:00 UTC',
      reason: 'No timezones provided',
      alternatives: []
    }
  }
  
  if (timezones.length === 1) {
    const tz = timezones[0]
    const offset = getTimezoneOffset(tz)
    return {
      recommendedTime: `09:00 ${offset}`,
      reason: `Single timezone: ${tz}`,
      alternatives: []
    }
  }
  
  // Cari overlap terbaik
  let maxOverlap = 0
  let bestTime = '09:00 UTC'
  
  for (let hour = 0; hour < 24; hour++) {
    let overlapCount = 0
    
    for (const tz of timezones) {
      const offset = parseInt(getTimezoneOffset(tz).replace('UTC+', '').replace('UTC-', ''))
      const localHour = (hour + offset + 24) % 24
      
      // Cek apakah dalam jam kerja (09:00 - 17:00)
      if (localHour >= 9 && localHour < 17) {
        overlapCount++
      }
    }
    
    if (overlapCount > maxOverlap) {
      maxOverlap = overlapCount
      bestTime = `${String(hour).padStart(2, '0')}:00 UTC`
    }
  }
  
  const alternatives = []
  for (let hour = 0; hour < 24; hour++) {
    if (hour !== parseInt(bestTime.split(':')[0])) {
      alternatives.push(`${String(hour).padStart(2, '0')}:00 UTC`)
    }
  }
  
  return {
    recommendedTime: bestTime,
    reason: `Best overlap for ${maxOverlap}/${timezones.length} timezones`,
    alternatives: alternatives.slice(0, 3)
  }
}

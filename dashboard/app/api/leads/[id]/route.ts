import { NextRequest, NextResponse } from 'next/server'
import sqlite3 from 'sqlite3'
import { open } from 'sqlite'
import path from 'path'

// Interface untuk lead data
interface Lead {
  id: number
  business_name: string
  contact: string
  phone?: string
  email?: string
  url?: string
  keywords?: string
  source?: string
  score?: number
  location?: string
  city?: string
  status?: string
  priority?: string
  property_type?: string
  price_range?: string
  bedrooms?: number
  bathrooms?: number
  land_size?: number
  building_size?: number
  year_built?: number
  description?: string
  date_found?: string
  last_contacted?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

// Interface untuk AI Reasoning (Radar Chart)
interface AIReasoning {
  intent: number
  budget: number
  urgency: number
  fit: number
  authority: number
}

// Interface untuk Timeline Activity
interface TimelineActivity {
  id: string
  activity: string
  timestamp: string
  type: 'discovery' | 'validation' | 'extraction' | 'analysis' | 'contact'
  details?: string
}

// Interface untuk complete response
interface LeadDetailResponse {
  success: boolean
  data: Lead & {
    ai_reasoning: AIReasoning
    timeline: TimelineActivity[]
  }
  message?: string
}

export async function GET(_request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const leadId = params.id

    // Validate ID parameter
    if (!leadId || isNaN(Number(leadId))) {
      return NextResponse.json(
        {
          success: false,
          message: 'Invalid lead ID parameter',
        },
        { status: 400 }
      )
    }

    // Database path - adjust according to your actual structure
    const dbPath = path.join(process.cwd(), 'data', 'leads.db')

    // Open database connection
    const db = await open({
      filename: dbPath,
      driver: sqlite3.Database,
    })

    // Query lead by ID
    const lead = await db.get(
      `SELECT 
        id, business_name, contact, phone, email, url, keywords, source, 
        score, location, city, status, priority, property_type, price_range, 
        bedrooms, bathrooms, land_size, building_size, year_built, 
        description, date_found, last_contacted, notes, created_at, updated_at
      FROM leads 
      WHERE id = ?`,
      [Number(leadId)]
    )

    // Close database connection
    await db.close()

    // Check if lead exists
    if (!lead) {
      return NextResponse.json(
        {
          success: false,
          message: `Lead with ID ${leadId} not found`,
        },
        { status: 404 }
      )
    }

    // Generate mock AI Reasoning data (Radar Chart values)
    const aiReasoning: AIReasoning = {
      intent: Math.floor(Math.random() * 30) + 70, // 70-100
      budget: Math.floor(Math.random() * 25) + 75, // 75-100
      urgency: Math.floor(Math.random() * 35) + 65, // 65-100
      fit: Math.floor(Math.random() * 20) + 80, // 80-100
      authority: Math.floor(Math.random() * 30) + 70, // 70-100
    }

    // Generate mock timeline data
    const generateTimeline = (): TimelineActivity[] => {
      const now = new Date()
      const timeline: TimelineActivity[] = []

      // Lead Discovered
      timeline.push({
        id: '1',
        activity: 'Lead Discovered',
        timestamp: new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 7 days ago
        type: 'discovery',
        details: `Found ${lead.business_name} through ${lead.source || 'web scraping'}`,
      })

      // AI Validation Passed
      timeline.push({
        id: '2',
        activity: 'AI Validation Passed',
        timestamp: new Date(now.getTime() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
        type: 'validation',
        details: `Lead scored ${lead.score}/10 with high confidence`,
      })

      // Contact Info Extracted
      timeline.push({
        id: '3',
        activity: 'Contact Information Extracted',
        timestamp: new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
        type: 'extraction',
        details: `Extracted phone: ${lead.phone}, email: ${lead.email}`,
      })

      // Market Analysis Completed
      if (lead.score && lead.score > 8) {
        timeline.push({
          id: '4',
          activity: 'Market Analysis Completed',
          timestamp: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
          type: 'analysis',
          details: `High-value lead identified in ${lead.location} market`,
        })
      }

      // Contact Attempt (if recent)
      if (lead.last_contacted) {
        timeline.push({
          id: '5',
          activity: 'Contact Attempt Initiated',
          timestamp: new Date(lead.last_contacted).toISOString(),
          type: 'contact',
          details: 'Automated outreach email sent',
        })
      }

      return timeline.sort(
        (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      )
    }

    // Construct complete response
    const response: LeadDetailResponse = {
      success: true,
      data: {
        ...lead,
        ai_reasoning: aiReasoning,
        timeline: generateTimeline(),
      },
    }

    // Return successful response
    return NextResponse.json(response, {
      status: 200,
      headers: {
        'Cache-Control': 'no-store, max-age=0',
        'Content-Type': 'application/json',
      },
    })
  } catch (error) {
    console.error('Error fetching lead details:', error)

    // Handle database connection errors
    if (error instanceof Error) {
      if (error.message.includes('SQLITE_CANTOPEN')) {
        return NextResponse.json(
          {
            success: false,
            message: 'Database connection failed. Please try again later.',
          },
          { status: 500 }
        )
      }

      if (error.message.includes('no such table')) {
        return NextResponse.json(
          {
            success: false,
            message: 'Database schema error. Leads table not found.',
          },
          { status: 500 }
        )
      }
    }

    // Generic error response
    return NextResponse.json(
      {
        success: false,
        message: 'Internal server error occurred while fetching lead details',
      },
      { status: 500 }
    )
  }
}

// Optional: Add other HTTP methods if needed
export async function PUT(_request: NextRequest, { params: _params }: { params: { id: string } }) {
  // Placeholder for PUT method (updating lead)
  return NextResponse.json(
    {
      success: false,
      message: 'PUT method not implemented yet',
    },
    { status: 501 }
  )
}

export async function DELETE(
  _request: NextRequest,
  { params: _params }: { params: { id: string } }
) {
  // Placeholder for DELETE method (deleting lead)
  return NextResponse.json(
    {
      success: false,
      message: 'DELETE method not implemented yet',
    },
    { status: 501 }
  )
}

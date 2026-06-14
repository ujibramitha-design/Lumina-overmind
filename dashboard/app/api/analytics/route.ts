import { NextResponse } from 'next/server'
import sqlite3 from 'sqlite3'
import { join } from 'path'

export async function GET(): Promise<NextResponse> {
  try {
    // Path to database file - adjust path to point to the correct location
    const dbPath = join(process.cwd(), '..', 'data', 'database', 'leads.db')

    // Open database connection
    const db = new sqlite3.Database(dbPath)

    return new Promise<NextResponse>(resolve => {
      // Query to get analytics data
      const queries = {
        totalLeads: 'SELECT COUNT(*) as count FROM leads',
        hotLeads: 'SELECT COUNT(*) as count FROM leads WHERE lead_score >= 80',
        averageScore: 'SELECT AVG(lead_score) as avg_score FROM leads',
      }

      const analyticsData: any = {
        totalLeads: 0,
        hotLeads: 0,
        averageScore: 0,
        activeScrapers: 3, // Static value as requested
      }

      let completedQueries = 0
      const totalQueries = Object.keys(queries).length

      // Execute each query
      Object.entries(queries).forEach(([key, query]) => {
        db.get(query, [], (err, row: any) => {
          if (err) {
            console.error(`Database query error for ${key}:`, err)
            // Continue with other queries even if one fails
          } else {
            if (key === 'averageScore') {
              analyticsData[key] = row.avg_score ? Math.round(row.avg_score * 10) / 10 : 0
            } else {
              analyticsData[key] = row.count || 0
            }
          }

          completedQueries++

          // When all queries are complete, return the response
          if (completedQueries === totalQueries) {
            // Close database connection
            db.close()

            const response = NextResponse.json({
              success: true,
              data: analyticsData,
              message: 'Analytics data retrieved successfully',
            })

            resolve(response)
          }
        })
      })
    })
  } catch (error) {
    console.error('Analytics API Route Error:', error)

    // Handle database file not found error specifically
    if (error instanceof Error && error.message.includes('ENOENT')) {
      console.log('Database file not found, returning dummy data')
      // Return dummy fallback data as requested
      return NextResponse.json({
        success: true,
        data: {
          totalLeads: 0,
          hotLeads: 0,
          averageScore: 0,
          activeScrapers: 3,
        },
        message: 'Database not found, returning dummy data',
      })
    }

    // Handle other errors - still return dummy data to prevent UI breakage
    return NextResponse.json({
      success: true,
      data: {
        totalLeads: 0,
        hotLeads: 0,
        averageScore: 0,
        activeScrapers: 3,
      },
      message: 'Error occurred, returning dummy data',
      error: error instanceof Error ? error.message : 'Unknown error',
    })
  }
}

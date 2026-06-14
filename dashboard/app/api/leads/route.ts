import { NextResponse } from 'next/server'
import sqlite3 from 'sqlite3'
import { join } from 'path'

export async function GET(): Promise<NextResponse> {
  try {
    // Path to database file
    const dbPath = join(process.cwd(), '..', 'data', 'database', 'leads.db')

    // Open database connection
    const db = new sqlite3.Database(dbPath)

    return new Promise<NextResponse>((resolve, reject) => {
      // Query to get leads ordered by score descending
      const query = `
        SELECT 
          id,
          business_name,
          contact,
          url,
          keywords,
          source,
          score as lead_score,
          location,
          status,
          date_found
        FROM leads 
        ORDER BY lead_score DESC 
        LIMIT 1000
      `

      db.all(query, [], (err, rows: any[]) => {
        // Close database connection
        db.close()

        if (err) {
          console.error('Database query error:', err)
          reject(
            new NextResponse(
              JSON.stringify({
                error: 'Database query failed',
                details: err.message,
              }),
              {
                status: 500,
                headers: { 'Content-Type': 'application/json' },
              }
            )
          )
          return
        }

        // Process keywords field (assuming it's stored as JSON string)
        const processedRows = rows.map(row => ({
          ...row,
          keywords:
            typeof row.keywords === 'string' ? JSON.parse(row.keywords) : row.keywords || [],
          date_found: row.date_found || new Date().toISOString(),
        }))

        const response = NextResponse.json({
          success: true,
          data: processedRows,
          count: processedRows.length,
          message: `Successfully retrieved ${processedRows.length} leads`,
        })

        resolve(response)
      })
    })
  } catch (error) {
    console.error('API Route Error:', error)

    // Handle specific database file not found error
    if (error instanceof Error && error.message.includes('ENOENT')) {
      return NextResponse.json(
        {
          error: 'Database file not found',
          details: 'The leads.db database file was not found at the expected location',
          path: join(process.cwd(), '..', 'data', 'database', 'leads.db'),
        },
        { status: 500 }
      )
    }

    // Handle other errors
    return NextResponse.json(
      {
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error occurred',
      },
      { status: 500 }
    )
  }
}

import * as XLSX from 'exceljs'

// Export data to Excel file
export async function exportToExcel(
  data: any[],
  filename: string,
  sheetName: string = 'Sheet1'
) {
  const workbook = new XLSX.Workbook()
  const worksheet = workbook.addWorksheet(sheetName)

  // Add headers from first object keys
  if (data.length > 0) {
    const headers = Object.keys(data[0])
    worksheet.columns = headers.map(header => ({
      header: header.charAt(0).toUpperCase() + header.slice(1),
      key: header,
      width: 20,
    }))

    // Add data rows
    worksheet.addRows(data)

    // Style header row
    const headerRow = worksheet.getRow(1)
    headerRow.font = { bold: true, color: { argb: 'FFFFFFFF' } }
    headerRow.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FF4472C4' },
    }
  }

  // Generate buffer
  const buffer = await workbook.xlsx.writeBuffer()

  // Create download link
  const blob = new Blob([buffer], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${filename}.xlsx`
  link.click()
  URL.revokeObjectURL(url)
}

// Export leads to Excel
export function exportLeadsToExcel(leads: any[]) {
  const formattedLeads = leads.map(lead => ({
    businessName: lead.business_name,
    contact: lead.contact,
    phone: lead.nomor_hp || '',
    area: lead.area || '',
    status: lead.status,
    priority: lead.priority,
    score: lead.score || 0,
    source: lead.source,
    dateFound: lead.date_found || new Date().toISOString(),
  }))

  exportToExcel(formattedLeads, 'leads-export', 'Leads')
}

// Export projects to Excel
export function exportProjectsToExcel(projects: any[]) {
  const formattedProjects = projects.map(project => ({
    name: project.name,
    type: project.type,
    location: project.location,
    price: project.price || 0,
    leadsCount: project.leadsCount || 0,
    hotLeadsCount: project.hotLeadsCount || 0,
    status: project.isActive ? 'Active' : 'Inactive',
  }))

  exportToExcel(formattedProjects, 'projects-export', 'Projects')
}

// Export growth data to Excel
export function exportGrowthToExcel(data: any[]) {
  exportToExcel(data, 'growth-report', 'Growth Data')
}

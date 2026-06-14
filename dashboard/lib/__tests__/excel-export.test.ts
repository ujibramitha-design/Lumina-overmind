import { describe, it, expect, vi, beforeEach } from 'vitest'
import { exportToExcel, exportLeadsToExcel, exportProjectsToExcel } from '../excel-export'

// Mock document methods
global.document = {
  createElement: vi.fn(),
} as any

global.URL = {
  createObjectURL: vi.fn(),
  revokeObjectURL: vi.fn(),
} as any

describe('excel-export', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('exportToExcel', () => {
    it('should export data to Excel file', async () => {
      const data = [
        { name: 'Test 1', value: 100 },
        { name: 'Test 2', value: 200 },
      ]
      const mockLink = {
        href: '',
        download: '',
        click: vi.fn(),
      }
      vi.mocked(document.createElement).mockReturnValue(mockLink as any)
      vi.mocked(URL.createObjectURL).mockReturnValue('mock-url')

      await exportToExcel(data, 'test-export', 'TestSheet')

      expect(document.createElement).toHaveBeenCalledWith('a')
      expect(mockLink.click).toHaveBeenCalled()
    })

    it('should handle empty data', async () => {
      const data: any[] = []
      const mockLink = {
        href: '',
        download: '',
        click: vi.fn(),
      }
      vi.mocked(document.createElement).mockReturnValue(mockLink as any)
      vi.mocked(URL.createObjectURL).mockReturnValue('mock-url')

      await exportToExcel(data, 'test-export', 'TestSheet')

      expect(document.createElement).toHaveBeenCalledWith('a')
    })
  })

  describe('exportLeadsToExcel', () => {
    it('should format and export leads data', async () => {
      const leads = [
        {
          id: '1',
          business_name: 'Business 1',
          contact: 'Contact 1',
          nomor_hp: '08123456789',
          area: 'Jakarta',
          status: 'new',
          priority: 'high',
          score: 85,
          source: 'manual',
          date_found: '2024-01-01',
        },
      ]
      const mockLink = {
        href: '',
        download: '',
        click: vi.fn(),
      }
      vi.mocked(document.createElement).mockReturnValue(mockLink as any)
      vi.mocked(URL.createObjectURL).mockReturnValue('mock-url')

      await exportLeadsToExcel(leads)

      expect(document.createElement).toHaveBeenCalledWith('a')
      expect(mockLink.download).toBe('leads-export.xlsx')
    })
  })

  describe('exportProjectsToExcel', () => {
    it('should format and export projects data', async () => {
      const projects = [
        {
          id: '1',
          name: 'Project 1',
          type: 'Residential',
          location: 'Jakarta',
          price: 1000000000,
          leadsCount: 50,
          hotLeadsCount: 10,
          isActive: true,
        },
      ]
      const mockLink = {
        href: '',
        download: '',
        click: vi.fn(),
      }
      vi.mocked(document.createElement).mockReturnValue(mockLink as any)
      vi.mocked(URL.createObjectURL).mockReturnValue('mock-url')

      await exportProjectsToExcel(projects)

      expect(document.createElement).toHaveBeenCalledWith('a')
      expect(mockLink.download).toBe('projects-export.xlsx')
    })
  })
})

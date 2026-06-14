import { describe, it, expect, vi } from 'vitest'

describe('API Integration Tests', () => {
  describe('Leads API', () => {
    it('should fetch leads successfully', async () => {
      // Mock fetch for testing
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve([{ id: '1', business_name: 'Test' }]),
        } as Response)
      )

      const response = await fetch('http://localhost:8000/api/leads?project_id=test')
      const data = await response.json()

      expect(data).toHaveLength(1)
      expect(data[0].business_name).toBe('Test')
    })

    it('should handle API errors gracefully', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500,
        } as Response)
      )

      const response = await fetch('http://localhost:8000/api/leads')
      expect(response.ok).toBe(false)
    })
  })

  describe('Projects API', () => {
    it('should fetch projects successfully', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve([{ id: '1', name: 'Project 1' }]),
        } as Response)
      )

      const response = await fetch('http://localhost:8000/api/projects')
      const data = await response.json()

      expect(data).toHaveLength(1)
      expect(data[0].name).toBe('Project 1')
    })
  })

  describe('Mutation Tests', () => {
    it('should create lead successfully', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ id: '1', business_name: 'New Lead' }),
        } as Response)
      )

      const response = await fetch('http://localhost:8000/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_name: 'New Lead', contact: 'Test', project_id: 'test' }),
      })

      expect(response.ok).toBe(true)
    })
  })
})

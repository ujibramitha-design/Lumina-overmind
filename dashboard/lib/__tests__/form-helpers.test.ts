import { describe, it, expect } from 'vitest'
import { leadSchema, projectSchema, type LeadFormData, type ProjectFormData } from '../form-helpers'

describe('form-helpers', () => {
  describe('leadSchema', () => {
    it('should validate valid lead data', () => {
      const validData = {
        business_name: 'Test Business',
        contact: 'John Doe',
        project_id: 'project-123',
        status: 'new',
        priority: 'medium',
      }
      const result = leadSchema.safeParse(validData)
      expect(result.success).toBe(true)
    })

    it('should require business_name', () => {
      const invalidData = {
        business_name: '',
        contact: 'John Doe',
        project_id: 'project-123',
      }
      const result = leadSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should require contact', () => {
      const invalidData = {
        business_name: 'Test Business',
        contact: '',
        project_id: 'project-123',
      }
      const result = leadSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should require project_id', () => {
      const invalidData = {
        business_name: 'Test Business',
        contact: 'John Doe',
        project_id: '',
      }
      const result = leadSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should validate status enum', () => {
      const validStatuses = ['new', 'contacted', 'qualified', 'closed']
      validStatuses.forEach(status => {
        const data = {
          business_name: 'Test Business',
          contact: 'John Doe',
          project_id: 'project-123',
          status,
        }
        const result = leadSchema.safeParse(data)
        expect(result.success).toBe(true)
      })
    })

    it('should validate priority enum', () => {
      const validPriorities = ['low', 'medium', 'high', 'urgent']
      validPriorities.forEach(priority => {
        const data = {
          business_name: 'Test Business',
          contact: 'John Doe',
          project_id: 'project-123',
          priority,
        }
        const result = leadSchema.safeParse(data)
        expect(result.success).toBe(true)
      })
    })

    it('should validate URL format', () => {
      const data = {
        business_name: 'Test Business',
        contact: 'John Doe',
        project_id: 'project-123',
        url: 'https://example.com',
      }
      const result = leadSchema.safeParse(data)
      expect(result.success).toBe(true)
    })

    it('should reject invalid URL', () => {
      const data = {
        business_name: 'Test Business',
        contact: 'John Doe',
        project_id: 'project-123',
        url: 'not-a-url',
      }
      const result = leadSchema.safeParse(data)
      expect(result.success).toBe(false)
    })
  })

  describe('projectSchema', () => {
    it('should validate valid project data', () => {
      const validData = {
        name: 'Test Project',
        type: 'Residential',
        location: 'Jakarta',
        price: 1000000000,
      }
      const result = projectSchema.safeParse(validData)
      expect(result.success).toBe(true)
    })

    it('should require name', () => {
      const invalidData = {
        name: '',
        type: 'Residential',
        location: 'Jakarta',
        price: 1000000000,
      }
      const result = projectSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should require type', () => {
      const invalidData = {
        name: 'Test Project',
        type: '',
        location: 'Jakarta',
        price: 1000000000,
      }
      const result = projectSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should require location', () => {
      const invalidData = {
        name: 'Test Project',
        type: 'Residential',
        location: '',
        price: 1000000000,
      }
      const result = projectSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should require positive price', () => {
      const invalidData = {
        name: 'Test Project',
        type: 'Residential',
        location: 'Jakarta',
        price: -1000,
      }
      const result = projectSchema.safeParse(invalidData)
      expect(result.success).toBe(false)
    })

    it('should allow zero price', () => {
      const data = {
        name: 'Test Project',
        type: 'Residential',
        location: 'Jakarta',
        price: 0,
      }
      const result = projectSchema.safeParse(data)
      expect(result.success).toBe(true)
    })
  })
})

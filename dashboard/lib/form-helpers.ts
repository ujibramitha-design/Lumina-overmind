import { useForm } from 'react-hook-form'
import { z } from 'zod'

// Common validation schemas
export const leadSchema = z.object({
  business_name: z.string().min(1, 'Business name is required').max(255),
  contact: z.string().min(1, 'Contact is required').max(255),
  url: z.string().url().optional().or(z.literal('')),
  keywords: z.array(z.string()).default([]),
  source: z.string().default('manual'),
  area: z.string().optional(),
  project_id: z.string().min(1, 'Project ID is required'),
  score: z.number().min(0).max(100).optional(),
  status: z.enum(['new', 'contacted', 'qualified', 'closed']).default('new'),
  priority: z.enum(['low', 'medium', 'high', 'urgent']).default('medium'),
  nomor_hp: z.string().optional(),
  notes: z.string().max(1000).optional(),
})

export const projectSchema = z.object({
  name: z.string().min(1, 'Project name is required').max(255),
  type: z.string().min(1, 'Project type is required'),
  location: z.string().min(1, 'Location is required'),
  price: z.number().min(0, 'Price must be positive'),
  description: z.string().max(1000).optional(),
})

export type LeadFormData = z.infer<typeof leadSchema>
export type ProjectFormData = z.infer<typeof projectSchema>

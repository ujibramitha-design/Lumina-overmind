/**
 * Twin-Dragon Engine - Project Management Store
 * Global state management for multi-tenant property projects
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface Project {
  id: string
  nama_proyek: string
  tipe_proyek: 'KOMERSIL' | 'SUBSIDI'
  lokasi: string
  harga_start: number
  target_market: string
  config?: Record<string, any>
  ai_prompt_style?: string
  dorking_targets: string[]
  is_active: boolean
  leads_count: number
  hot_leads_count: number
  conversion_rate: number
  created_at: string
  updated_at: string
}

interface ProjectStore {
  // State
  projects: Project[]
  activeProjectId: string | null
  activeProject: Project | null
  isLoading: boolean
  error: string | null

  // Actions
  setProjects: (projects: Project[]) => void
  setActiveProject: (projectId: string | null) => void
  addProject: (project: Project) => void
  updateProject: (projectId: string, updates: Partial<Project>) => void
  deleteProject: (projectId: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  clearError: () => void

  // Computed
  getActiveProjectType: () => 'KOMERSIL' | 'SUBSIDI' | null
  getProjectById: (id: string) => Project | undefined
  getProjectsByType: (type: 'KOMERSIL' | 'SUBSIDI') => Project[]
  getActiveProjectTheme: () => 'komersil' | 'subsidi' | null
}

export const useProjectStore = create<ProjectStore>()(
  persist(
    (set, get) => ({
      // Initial State
      projects: [],
      activeProjectId: null,
      activeProject: null,
      isLoading: false,
      error: null,

      // Actions
      setProjects: projects => {
        set({ projects })
        // Update active project if it exists
        const { activeProjectId } = get()
        if (activeProjectId) {
          const activeProject = projects.find(p => p.id === activeProjectId)
          set({ activeProject: activeProject || null })
        }
      },

      setActiveProject: projectId => {
        const { projects } = get()
        const activeProject = projectId ? projects.find(p => p.id === projectId) || null : null
        set({
          activeProjectId: projectId,
          activeProject,
          error: projectId && !activeProject ? 'Project not found' : null,
        })
      },

      addProject: project => {
        set(state => ({
          projects: [...state.projects, project],
        }))
      },

      updateProject: (projectId, updates) => {
        set(state => ({
          projects: state.projects.map(p =>
            p.id === projectId ? { ...p, ...updates, updated_at: new Date().toISOString() } : p
          ),
          activeProject:
            state.activeProject?.id === projectId
              ? { ...state.activeProject, ...updates, updated_at: new Date().toISOString() }
              : state.activeProject,
        }))
      },

      deleteProject: projectId => {
        set(state => ({
          projects: state.projects.filter(p => p.id !== projectId),
          activeProject: state.activeProject?.id === projectId ? null : state.activeProject,
          activeProjectId: state.activeProjectId === projectId ? null : state.activeProjectId,
        }))
      },

      setLoading: loading => set({ isLoading: loading }),

      setError: error => set({ error }),

      clearError: () => set({ error: null }),

      // Computed
      getActiveProjectType: () => {
        const { activeProject } = get()
        return activeProject?.tipe_proyek || null
      },

      getProjectById: id => {
        const { projects } = get()
        return projects.find(p => p.id === id)
      },

      getProjectsByType: type => {
        const { projects } = get()
        return projects.filter(p => p.tipe_proyek === type)
      },

      getActiveProjectTheme: () => {
        const { activeProject } = get()
        if (!activeProject) return null
        return activeProject.tipe_proyek.toLowerCase() as 'komersil' | 'subsidi'
      },
    }),
    {
      name: 'project-store',
      partialize: state => ({
        activeProjectId: state.activeProjectId,
        // Don't persist projects, error, and loading states
      }),
    }
  )
)

// Theme utilities
export const getProjectThemeColors = (projectType: 'KOMERSIL' | 'SUBSIDI') => {
  if (projectType === 'KOMERSIL') {
    return {
      primary: '#D4AF37', // Gold
      secondary: '#B8860B', // Dark Gold
      accent: '#FFD700', // Bright Gold
      background: '#1A1A1A',
      text: '#FFFFFF',
      border: '#D4AF37',
      icon: 'crown', // Crown/Star icon theme
    }
  } else {
    return {
      primary: '#2563EB', // Blue
      secondary: '#1E40AF', // Dark Blue
      accent: '#10B981', // Green
      background: '#0F172A',
      text: '#FFFFFF',
      border: '#2563EB',
      icon: 'shield', // Shield icon theme
    }
  }
}

// Hook for fetching projects from API
export const useProjects = () => {
  const store = useProjectStore()

  const fetchProjects = async () => {
    store.setLoading(true)
    store.clearError()

    try {
      const response = await fetch('/api/projects')
      if (!response.ok) {
        throw new Error('Failed to fetch projects')
      }

      const projects = await response.json()
      store.setProjects(projects)
    } catch (error) {
      store.setError(error instanceof Error ? error.message : 'Unknown error')
    } finally {
      store.setLoading(false)
    }
  }

  const createProject = async (
    projectData: Omit<
      Project,
      'id' | 'leads_count' | 'hot_leads_count' | 'conversion_rate' | 'created_at' | 'updated_at'
    >
  ) => {
    store.setLoading(true)
    store.clearError()

    try {
      const response = await fetch('/api/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData),
      })

      if (!response.ok) {
        throw new Error('Failed to create project')
      }

      const newProject = await response.json()
      store.addProject(newProject)
      return newProject
    } catch (error) {
      store.setError(error instanceof Error ? error.message : 'Unknown error')
      throw error
    } finally {
      store.setLoading(false)
    }
  }

  const updateProject = async (projectId: string, updates: Partial<Project>) => {
    store.setLoading(true)
    store.clearError()

    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      })

      if (!response.ok) {
        throw new Error('Failed to update project')
      }

      const updatedProject = await response.json()
      store.updateProject(projectId, updatedProject)
      return updatedProject
    } catch (error) {
      store.setError(error instanceof Error ? error.message : 'Unknown error')
      throw error
    } finally {
      store.setLoading(false)
    }
  }

  const deleteProject = async (projectId: string) => {
    store.setLoading(true)
    store.clearError()

    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error('Failed to delete project')
      }

      store.deleteProject(projectId)
    } catch (error) {
      store.setError(error instanceof Error ? error.message : 'Unknown error')
      throw error
    } finally {
      store.setLoading(false)
    }
  }

  return {
    ...store,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  }
}

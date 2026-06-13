# UI System

## Visual Direction

Canonical dashboard style:
- dark tactical
- emerald accent
- dense enterprise layout
- data-first and operational
- minimal decorative noise

## UI Tech Stack (Best-in-Class)

### Core Framework
- **Next.js 14** → Target: Upgrade to 15 with Turbopack
- **React 18** with Server Components
- **TypeScript** strict mode enabled

### Styling System
- **TailwindCSS 3.3.0** → Target: Upgrade to 4
- **PostCSS** for CSS processing
- **CSS Variables** for theming (HSL-based)
- **Dark Mode** class-based implementation

### Component Library
- **shadcn/ui** - Headless components with Radix UI primitives
- **Radix UI** - Accessible unstyled components
- **Lucide React** - Icon library

### State & Data
- **Zustand** - Global state management
- **@tanstack/react-query** (to be added) - Server state management
- **react-hook-form + Zod** (to be added) - Form validation

### Visualization
- **Recharts** - Charting library
- **TanStack Table** - Data grid with virtualization
- **ReactFlow** - Flow diagrams and workflows
- **react-leaflet** (to be added) - GIS/Mapping

### Animation & 3D
- **Framer Motion** - Production-ready animations
- **GSAP** - Complex animations
- **Three.js + React Three Fiber** - 3D graphics
- **@react-three/drei** - 3D helpers

### Utilities
- **date-fns** - Date manipulation
- **clsx + tailwind-merge** - Conditional classes
- **class-variance-authority** - Component variants

## Shell Rules

All dashboard pages should use the same core shell:
- left sidebar
- sticky top header
- dark background with subtle depth
- card-based panels
- tight spacing and clear hierarchy

## Component Rules

### Use these for common UI actions
- icon buttons for tools and actions
- tabs for mode switching
- toggles for binary settings
- segmented controls or button groups for narrow mode choices
- tables or grids for operational records
- cards only for contained items, not for full page sections

### Typography
- reserve large headings for true entry surfaces
- keep dashboard headings compact inside panels
- avoid oversized marketing typography

### Color Use
- emerald is the main accent
- zinc/black is the base
- use blue, amber, red only for state signaling
- avoid one-tone palettes and avoid unnecessary gradients

## Page Patterns

### Command Center
- metric cards
- recent activity
- system state
- global search

### Data Workspace
- search/filter bar
- table/grid
- summary stats
- detail drawer or split panel

### Intelligence Workspace
- geo canvas or map
- status cards
- layer summary
- drill-down panel

### Detail Workspace
- summary header
- timeline
- related records
- actions panel

## Empty States

Empty states should:
- explain the state briefly
- show the next action
- keep the same shell and tone


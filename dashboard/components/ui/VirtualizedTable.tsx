/**
 * LUMINA OVERMIND SYSTEM - Virtualized Table Component
 *
 * High-performance table component using @tanstack/react-virtual
 * Handles large datasets without performance degradation
 */

import React, { useRef, useMemo, useCallback } from 'react'
import { useVirtualizer } from '@tanstack/react-virtual'
import { cn } from '@/lib/utils'

interface Column<T> {
  key: keyof T
  label: string
  width?: number | string
  className?: string
  render?: (value: any, row: T, index: number) => React.ReactNode
}

interface VirtualizedTableProps<T> {
  data: T[]
  columns: Column<T>[]
  className?: string
  rowHeight?: number
  maxHeight?: number
  onRowClick?: (row: T, index: number) => void
  emptyMessage?: string
  loading?: boolean
}

export function VirtualizedTable<T extends Record<string, any>>({
  data,
  columns,
  className,
  rowHeight = 48,
  maxHeight = 400,
  onRowClick,
  emptyMessage = 'No data available',
  loading = false,
}: VirtualizedTableProps<T>) {
  const parentRef = useRef<HTMLDivElement>(null)

  // Calculate column widths
  const columnWidths = useMemo(() => {
    const totalWidth = parentRef.current?.clientWidth || 800
    const flexibleColumns = columns.filter(col => !col.width)
    const fixedWidth = columns
      .filter(col => typeof col.width === 'number')
      .reduce((sum, col) => sum + (col.width as number), 0)

    const flexibleWidth = flexibleColumns.length > 0 ? (totalWidth - fixedWidth) / flexibleColumns.length : 100

    return columns.map(col => ({
      ...col,
      width: col.width || flexibleWidth,
    }))
  }, [columns])

  // Virtualizer configuration
  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => rowHeight,
    overscan: 5,
  })

  // Handle row click
  const handleRowClick = useCallback(
    (row: T, index: number) => {
      onRowClick?.(row, index)
    },
    [onRowClick]
  )

  // Render cell content
  const renderCell = useCallback((column: Column<T>, row: T, rowIndex: number) => {
    const value = row[column.key]

    if (column.render) {
      return column.render(value, row, rowIndex)
    }

    // Default rendering
    if (value === null || value === undefined) {
      return <span className="text-zinc-500">-</span>
    }

    if (typeof value === 'boolean') {
      return (
        <span
          className={cn(
            'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
            value ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
          )}
        >
          {value ? 'Active' : 'Inactive'}
        </span>
      )
    }

    if (typeof value === 'number') {
      return <span className="font-mono">{value.toLocaleString()}</span>
    }

    return <span>{String(value)}</span>
  }, [])

  if (loading) {
    return (
      <div className={cn('flex items-center justify-center p-8', className)}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
        <span className="ml-2 text-zinc-400">Loading...</span>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className={cn('flex items-center justify-center p-8', className)}>
        <span className="text-zinc-500">{emptyMessage}</span>
      </div>
    )
  }

  return (
    <div className={cn('border border-zinc-800 rounded-lg overflow-hidden', className)}>
      {/* Header */}
      <div className="bg-zinc-900 border-b border-zinc-800">
        <div className="flex">
          {columnWidths.map(column => (
            <div
              key={String(column.key)}
              className={cn(
                'px-4 py-3 text-sm font-medium text-zinc-300 border-r border-zinc-800 last:border-r-0',
                column.className
              )}
              style={{ width: column.width }}
            >
              {column.label}
            </div>
          ))}
        </div>
      </div>

      {/* Virtualized body */}
      <div ref={parentRef} className="relative overflow-auto" style={{ height: maxHeight }}>
        <div
          style={{
            height: `${virtualizer.getTotalSize()}px`,
            width: '100%',
            position: 'relative',
          }}
        >
          {virtualizer.getVirtualItems().map(virtualRow => {
            const row = data[virtualRow.index]

            return (
              <div
                key={virtualRow.index}
                className={cn(
                  'absolute left-0 right-0 flex border-b border-zinc-800 hover:bg-zinc-800/50 transition-colors',
                  onRowClick && 'cursor-pointer'
                )}
                style={{
                  height: `${rowHeight}px`,
                  transform: `translateY(${virtualRow.start}px)`,
                }}
                onClick={() => handleRowClick(row, virtualRow.index)}
              >
                {columnWidths.map(column => (
                  <div
                    key={String(column.key)}
                    className={cn(
                      'px-4 py-3 text-sm text-zinc-300 border-r border-zinc-800 last:border-r-0 flex items-center',
                      column.className
                    )}
                    style={{ width: column.width }}
                  >
                    {renderCell(column, row, virtualRow.index)}
                  </div>
                ))}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

// Specific virtualized components for common use cases
export const VirtualizedLeadsTable = ({
  leads,
  onLeadClick,
  loading,
}: {
  leads: any[]
  onLeadClick?: (lead: any) => void
  loading?: boolean
}) => {
  const columns = useMemo(
    () => [
      {
        key: 'name' as const,
        label: 'Name',
        width: 200,
        render: (value: string, lead: any) => (
          <div>
            <div className="font-medium">{value}</div>
            <div className="text-xs text-zinc-500">{lead.email}</div>
          </div>
        ),
      },
      {
        key: 'status' as const,
        label: 'Status',
        width: 120,
        render: (value: string) => (
          <span
            className={cn(
              'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
              value === 'hot'
                ? 'bg-red-500/20 text-red-400'
                : value === 'warm'
                  ? 'bg-yellow-500/20 text-yellow-400'
                  : 'bg-blue-500/20 text-blue-400'
            )}
          >
            {value?.toUpperCase()}
          </span>
        ),
      },
      {
        key: 'score' as const,
        label: 'Score',
        width: 80,
        render: (value: number) => (
          <div className="text-center">
            <div className="font-mono font-medium">{value}</div>
            <div className="w-full bg-zinc-700 rounded-full h-1 mt-1">
              <div className="bg-emerald-500 h-1 rounded-full" style={{ width: `${Math.min(value, 100)}%` }}></div>
            </div>
          </div>
        ),
      },
      {
        key: 'createdAt' as const,
        label: 'Created',
        width: 150,
        render: (value: string) => (
          <div className="text-xs">
            {new Date(value).toLocaleDateString()}
            <div className="text-zinc-500">{new Date(value).toLocaleTimeString()}</div>
          </div>
        ),
      },
    ],
    []
  )

  return (
    <VirtualizedTable
      data={leads}
      columns={columns}
      rowHeight={56}
      maxHeight={500}
      onRowClick={onLeadClick}
      loading={loading}
      emptyMessage="No leads found"
    />
  )
}

export default VirtualizedTable

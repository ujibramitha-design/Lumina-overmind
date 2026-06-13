# ⚡ AI Workflow Builder - Documentation

## Overview
Advanced visual workflow builder using ReactFlow library for creating and managing automated business processes with dark theme and neon styling.

## 🎯 Page Features

### Dynamic Routing
- **Path**: `/workflows/page.tsx`
- **URL**: `http://localhost:3000/workflows`
- **Full Page Application**: Complete workflow builder experience

### Technology Stack
- **ReactFlow**: Visual node-based editor
- **TypeScript**: Type-safe implementation
- **Dark Theme**: Pitch-black with neon accents
- **Custom Nodes**: Inline styled components

## 🏗️ Layout Structure

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ AI Workflow Orchestrator    3 nodes • 2 connections    [Deploy Workflow] │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- Page title with lightning icon
- Node and connection statistics
- Deploy workflow button with loading state

### Main Canvas Area
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  [Lead Score > 80] ───► [Generate Pitch Deck]              │
│        │                                                    │
│        └──► [Send WhatsApp Alert]                          │
│                                                             │
│                ReactFlow Canvas                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📊 ReactFlow Configuration

### Canvas Setup
```typescript
<ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={onConnect}
  nodeTypes={nodeTypes}
  fitView
  style={{
    background: '#000000',
    width: '100%',
    height: '100%'
  }}
>
  <Background 
    color="#27272a" 
    gap={16}
    size={1}
  />
  <Controls 
    style={{
      background: '#18181b',
      border: '1px solid #27272a',
      borderRadius: '8px'
    }}
  />
</ReactFlow>
```

### Background Configuration
- **Color**: `#27272a` (zinc-800)
- **Gap**: 16px
- **Size**: 1px
- **Theme**: Dark with subtle grid

### Controls Styling
- **Background**: `#18181b` (zinc-900)
- **Border**: `#27272a` (zinc-800)
- **Border Radius**: 8px
- **Interactive**: Disabled for clean look

## 🔧 Node Configuration

### Custom Node Component
```typescript
const CustomNode = ({ data, selected }) => {
  const getNodeStyle = (type) => {
    switch (type) {
      case 'trigger':
        return {
          background: '#000000',
          color: '#ffffff',
          border: selected ? '#10b981' : '#10b981',
          borderWidth: '2px',
          borderRadius: '8px',
          boxShadow: selected ? '0 0 20px rgba(16, 185, 129, 0.5)' : '0 0 10px rgba(16, 185, 129, 0.3)'
        }
      // ... other types
    }
  }
}
```

### Node Types & Styling

#### Node 1 - Trigger (Lead Score > 80)
- **Border Color**: Emerald (`#10b981`)
- **Icon**: ⚡ Lightning
- **Type**: `trigger`
- **Position**: (250, 100)
- **Styling**: Black background, white text, emerald border

#### Node 2 - Action (Generate Pitch Deck)
- **Border Color**: Blue (`#3b82f6`)
- **Icon**: ⚙️ Gear
- **Type**: `action`
- **Position**: (100, 250)
- **Styling**: Black background, white text, blue border

#### Node 3 - Action (Send WhatsApp Alert)
- **Border Color**: Green (`#22c55e`)
- **Icon**: 📱 Phone
- **Type**: `notification`
- **Position**: (400, 250)
- **Styling**: Black background, white text, green border

## 🔗 Edge Configuration

### Animated Edges
```typescript
const initialEdges: Edge[] = [
  {
    id: 'e1-2',
    source: '1',
    target: '2',
    animated: true,
    style: { 
      stroke: '#10b981', 
      strokeWidth: 2,
      filter: 'drop-shadow(0 0 6px rgba(16, 185, 129, 0.8))'
    },
    markerEnd: {
      type: 'arrowclosed',
      color: '#10b981',
      strokeWidth: 2,
    }
  },
  // ... second edge
]
```

### Edge Features
- **Animation**: `animated: true` for flowing effect
- **Color**: Neon green (`#10b981`)
- **Stroke Width**: 2px
- **Drop Shadow**: Glowing effect
- **Arrow Markers**: Directional indicators

## 🎨 Visual Design

### Color Palette
- **Background**: `#000000` (pure black)
- **Node Background**: `#000000` (black)
- **Node Text**: `#ffffff` (white)
- **Trigger Border**: `#10b981` (emerald)
- **Action Border**: `#3b82f6` (blue)
- **Notification Border**: `#22c55e` (green)
- **Edge Color**: `#10b981` (emerald)
- **Grid Color**: `#27272a` (zinc-800)

### Typography
- **Node Labels**: 14px, 600 weight, white
- **Header**: 24px, bold, white
- **Statistics**: 14px, zinc-500
- **Button**: 14px, 600 weight

### Effects
- **Node Selection**: Glow effect with increased shadow
- **Edge Animation**: Continuous flowing animation
- **Hover States**: Smooth color transitions
- **Drop Shadows**: Neon glow effects

## 🔌 State Management

### React Hooks
```typescript
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
const [isDeploying, setIsDeploying] = useState(false)
```

### Event Handlers
```typescript
// Connection handling
const onConnect = useCallback(
  (params) => setEdges((eds) => addEdge({ 
    ...params, 
    animated: true, 
    style: { stroke: '#10b981', strokeWidth: 2 } 
  }, eds)),
  [setEdges]
)

// Deploy workflow
const onDeploy = useCallback(() => {
  setIsDeploying(true)
  setTimeout(() => {
    setIsDeploying(false)
    alert('Workflow deployed successfully!')
  }, 2000)
}, [])
```

## 🚀 Workflow Functionality

### Deploy Workflow Button
- **Text**: "Deploy Workflow"
- **Action**: Simulates deployment process
- **Loading State**: Spinner animation
- **Success Feedback**: Alert notification

### Workflow Statistics Panel
- **Active Triggers**: Count and description
- **Actions**: Number of action nodes
- **Connections**: Active connections count
- **Visual Indicators**: Color-coded status dots

### Node Interaction
- **Selection**: Click to select nodes
- **Visual Feedback**: Glow effect on selection
- **Drag & Drop**: Reposition nodes
- **Connection**: Drag to create edges

## 🎯 Business Use Cases

### Lead Management Workflow
1. **Trigger**: Lead Score > 80
2. **Action**: Generate Pitch Deck
3. **Notification**: Send WhatsApp Alert

### Automation Benefits
- **Real-time Processing**: Instant trigger evaluation
- **Multi-channel Output**: WhatsApp, email, etc.
- **Visual Monitoring**: See workflow flow
- **Easy Configuration**: Drag-and-drop interface

### Scalability
- **Custom Nodes**: Add new node types
- **Complex Workflows**: Multi-step processes
- **Integration**: Connect to external APIs
- **Monitoring**: Real-time status tracking

## 🧪 Testing

### Automated Testing
```bash
# Run test script
node test_workflow_page.js
```

**Test Coverage:**
- Page accessibility and rendering
- ReactFlow integration validation
- Visual styling verification
- Workflow functionality testing

### Manual Testing Checklist
- [ ] Page loads correctly at `/workflows`
- [ ] ReactFlow canvas displays with dark theme
- [ ] 3 nodes appear with proper styling
- [ ] Animated edges flow with neon green color
- [ ] Pan and zoom controls work smoothly
- [ ] Node selection shows glow effect
- [ ] Deploy workflow button functions
- [ ] Statistics panel updates correctly
- [ ] Background grid displays properly

## 📱 Responsive Design

### Desktop (Primary)
- **Full Canvas**: 80vh height, full width
- **Interactive Controls**: Mouse-based pan/zoom
- **Node Manipulation**: Drag and drop
- **Edge Creation**: Visual connection tools

### Mobile (Limited)
- **View Only**: Simplified controls
- **Touch Support**: Basic pan/zoom
- **Reduced Features**: Limited editing
- **Optimized Layout**: Smaller controls

## 🔮 Future Enhancements

### Advanced Features
- [ ] Custom node library
- [ ] Conditional routing
- [ ] Parallel execution
- [ ] Error handling nodes
- [ ] Integration APIs
- [ ] Workflow templates

### Visual Improvements
- [ ] More animation effects
- [ ] Custom themes
- [ ] Node grouping
- [ ] Minimap navigation
- [ ] Keyboard shortcuts
- [ ] Undo/redo functionality

### Business Logic
- [ ] Real-time execution
- [ ] Performance monitoring
- [ ] Error tracking
- [ ] Audit logging
- [ ] User permissions
- [ ] Workflow analytics

---

## 🚀 Quick Start

1. **Ensure Dependencies**: ReactFlow installed
2. **Start Server**: `npm run dev`
3. **Navigate**: `http://localhost:3000/workflows`
4. **Test**: `node test_workflow_page.js`

## 📁 File Structure
```
dashboard/
├── app/workflows/page.tsx          # Main workflow page
├── test_workflow_page.js           # Test script
├── WORKFLOW_DOCUMENTATION.md        # This documentation
└── package.json                    # ReactFlow dependency
```

## 🎯 Key Features Summary

### ReactFlow Integration
- **Visual Editor**: Drag-and-drop node editor
- **Custom Nodes**: Inline styled components
- **Animated Edges**: Flowing data visualization
- **Dark Theme**: Consistent with app design

### Workflow Management
- **Node Configuration**: Trigger, action, notification types
- **Edge Connections**: Visual workflow connections
- **Deploy Functionality**: Workflow deployment simulation
- **Statistics Panel**: Real-time workflow metrics

### User Experience
- **Intuitive Interface**: Visual workflow building
- **Real-time Feedback**: Immediate visual updates
- **Professional Design**: Dark theme with neon accents
- **Responsive Layout**: Works on different screen sizes

---

*Last updated: May 30, 2026*

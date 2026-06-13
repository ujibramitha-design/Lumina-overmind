# 📋 Lead 360° Intelligence Profile - Documentation

## Overview
Dynamic Next.js page for displaying comprehensive lead intelligence with AI reasoning, activity timeline, and action controls in a pitch-black dark mode design.

## 🎯 Page Features

### Dynamic Routing
- **Path**: `/leads/[id]/page.tsx`
- **URL Example**: `http://localhost:3000/leads/1`
- **Parameter**: `id` (lead ID from database)

### Design System
- **Theme**: Pitch-black dark mode
- **Colors**: Black background (`bg-black`) with zinc accents (`border-zinc-800`, `bg-zinc-950/50`)
- **Accent**: Emerald neon (`text-emerald-400`, `border-emerald-500/30`)
- **Typography**: Clean, modern with proper hierarchy

## 🏗️ Layout Structure

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Command Center    Lead Name    HOT • 9.2/10  ID: #1 │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- Navigation link back to home
- Lead business name (large, bold)
- Score badge (HOT/WARM/COLD with score)
- Lead ID indicator

### Main Grid Layout (3 Columns)
```
┌─────────────┬─────────────┬─────────────┐
│ Intelligence │   AI        │  Activity   │
│    Desk      │ Reasoning   │  Timeline   │
│             │             │             │
│ Contact     │ Radar Chart │ Timeline    │
│ Details     │             │ Items       │
│             │             │             │
│ Action Desk │             │             │
│             │             │             │
│ 3 Buttons   │             │             │
└─────────────┴─────────────┴─────────────┘
```

## 📊 Column Details

### Left Column - Intelligence Desk

#### Contact Details Card
**Icons + Information:**
- 📞 Phone: `+62812345678`
- 📧 Email: `contact@example.com`
- 📍 Location: `Jakarta Selatan`
- 🌐 Source: `website_inquiry`
- 🎯 Property Type: `apartment`
- 📈 Price Range: `2M-5M`

#### Action Desk Card
**3 Neon Buttons:**
1. **Generate Pitch Deck** - Creates presentation
2. **Send Auto-Email** - Automated outreach
3. **Handover to Closer** - Transfer to sales

**Button Style:**
```css
bg-emerald-500/10 border border-emerald-500/30 text-emerald-400
hover:bg-emerald-500/20 transition-colors
```

### Middle Column - AI Reasoning

#### Radar Chart
**Data Visualization:**
- 5-axis radar chart (Intent, Budget, Urgency, Fit, Authority)
- Dark theme styling
- Emerald green colors
- Semi-transparent fill

**Chart Configuration:**
```javascript
<RadarChart data={radarData}>
  <PolarGrid stroke="#27272a" strokeDasharray="3 3" />
  <PolarAngleAxis tick={{ fill: "#71717a", fontSize: 12 }} />
  <PolarRadiusAxis tick={{ fill: "#52525b", fontSize: 10 }} />
  <Radar stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
</RadarChart>
```

#### AI Metrics Grid
**2x2 Grid Display:**
- Intent: `90`
- Budget: `85`
- Urgency: `75`
- Fit: `95`
- Authority: `80`

### Right Column - Activity Timeline

#### Timeline Items
**Visual Design:**
- Neon green dots on the left
- Vertical connecting lines (`border-l border-zinc-800`)
- Activity icons and descriptions
- Timestamps in relative format

**Timeline Structure:**
```javascript
<div className="relative pl-6 pb-6">
  <div className="absolute left-2 top-6 bottom-0 w-px border-l border-zinc-800"></div>
  <div className="absolute left-0 top-2 w-4 h-4 bg-emerald-500 rounded-full">
    <div className="w-2 h-2 bg-black rounded-full"></div>
  </div>
  <div className="ml-6">
    <div className="flex items-center gap-2">
      <Icon className="text-emerald-400" />
      <span className="text-zinc-100">Activity Name</span>
    </div>
    <div className="text-zinc-500 text-sm">Timestamp</div>
  </div>
</div>
```

## 🎨 Design Elements

### Loading Animation
**Hacker-Style Loading:**
```javascript
<div className="text-emerald-400 font-mono text-lg">
  ACCESSING LEAD INTELLIGENCE...
</div>
<div className="text-zinc-500 font-mono text-sm">
  Decrypting 360° profile data...
</div>
<div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
```

### Score Badges
**Dynamic Color Coding:**
- **HOT** (8-10): `bg-emerald-500/20 text-emerald-400 border-emerald-500/30`
- **WARM** (6-7): `bg-amber-500/20 text-amber-400 border-amber-500/30`
- **COLD** (0-5): `bg-blue-500/20 text-blue-400 border-blue-500/30`

### Card Styling
**Consistent Card Design:**
```css
bg-zinc-950/50 border border-zinc-800 rounded-lg p-6
```

## 🔧 Technical Implementation

### Data Fetching
```javascript
async function fetchLead() {
  const response = await fetch(`/api/leads/${params.id}`)
  const data = await response.json()
  
  if (data.success) {
    setLead(data.data)
  } else {
    setError(data.message)
  }
}
```

### Type Safety
**TypeScript Interfaces:**
```typescript
interface Lead {
  id: number
  business_name: string
  contact: string
  phone?: string
  email?: string
  score?: number
  // ... more fields
}

interface AIReasoning {
  intent: number
  budget: number
  urgency: number
  fit: number
  authority: number
}

interface TimelineActivity {
  id: string
  activity: string
  timestamp: string
  type: 'discovery' | 'validation' | 'extraction' | 'analysis' | 'contact'
  details?: string
}
```

### Error Handling
**Comprehensive Error States:**
- Loading animation during fetch
- Error message display for failed requests
- 404 handling for non-existent leads
- Network error handling

## 🧪 Testing

### Automated Testing
```bash
# Run test script
node test_lead_page.js
```

**Test Coverage:**
- Page accessibility
- Component rendering
- API integration
- Error scenarios
- Loading states

### Manual Testing Checklist
- [ ] Loading animation displays
- [ ] Header navigation works
- [ ] 3-column layout responsive
- [ ] Radar chart renders correctly
- [ ] Timeline items display properly
- [ ] Action buttons are clickable
- [ ] Score badges show correct colors
- [ ] Dark mode styling consistent
- [ ] Mobile responsiveness
- [ ] Error states display correctly

## 📱 Responsive Design

### Desktop (md+)
- 3-column grid layout
- Full radar chart display
- Horizontal timeline items

### Mobile (sm)
- Single column stack
- Compact radar chart
- Vertical timeline items

## 🚀 Usage Examples

### Navigation
```javascript
// From dashboard or list page
<Link href={`/leads/${lead.id}`}>
  View Lead Profile
</Link>

// Programmatic navigation
router.push(`/leads/${leadId}`)
```

### Data Integration
```javascript
// Custom hook for lead data
export function useLeadDetail(leadId: string) {
  const [lead, setLead] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchLead()
  }, [leadId])
  
  return { lead, loading, error }
}
```

## 🎯 Business Value

### User Experience
- **Comprehensive View**: All lead data in one place
- **Visual Intelligence**: Radar chart for quick assessment
- **Action-Oriented**: Clear next steps with action buttons
- **Professional Design**: Modern, clean interface

### Operational Efficiency
- **Quick Assessment**: AI reasoning at a glance
- **Historical Context**: Timeline of all activities
- **Easy Navigation**: Back to command center
- **Mobile-Friendly**: Access on any device

### Data Visualization
- **Radar Chart**: 5-dimensional lead scoring
- **Timeline**: Activity history visual progression
- **Score Badges**: Quick lead quality identification
- **Icons**: Intuitive information hierarchy

## 🔮 Future Enhancements

### Interactive Features
- [ ] Edit lead information inline
- [ ] Real-time updates via WebSocket
- [ ] Export lead profile to PDF
- [ ] Share lead profile via link

### Advanced Analytics
- [ ] Compare multiple leads
- [ ] Lead scoring trends
- [ ] Conversion probability
- [ ] Market insights integration

### Automation
- [ ] Auto-generate pitch decks
- [ ] Schedule email sequences
- [ ] Automated handover workflows
- [ ] CRM integration

---

## 🚀 Quick Start

1. **Ensure Database**: Run `python data/database_forge.py`
2. **Start Server**: `npm run dev`
3. **Navigate**: `http://localhost:3000/leads/1`
4. **Test**: `node test_lead_page.js`

---

*Last updated: May 30, 2026*

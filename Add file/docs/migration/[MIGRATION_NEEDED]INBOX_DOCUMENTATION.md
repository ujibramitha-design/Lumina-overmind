# 📱 Omni-Channel Inbox & Closer Desk - Documentation

## Overview
Advanced multi-channel inbox system for managing customer conversations across WhatsApp, Telegram, Email, and Web with AI-powered assistance and smart reply suggestions.

## 🎯 Page Features

### Dynamic Routing
- **Path**: `/inbox/page.tsx`
- **URL**: `http://localhost:3000/inbox`
- **Full Page Application**: Complete inbox experience without navigation

### Design System
- **Theme**: Pitch-black dark mode with hacker aesthetic
- **Colors**: Black background (`bg-black`) with zinc accents (`border-zinc-800`, `bg-zinc-950`)
- **Accent**: Emerald neon (`text-emerald-400`, `bg-emerald-500/10`)
- **Typography**: Clean, modern with proper hierarchy

## 🏗️ Layout Structure

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│ 💬 Closer Desk & AI Inbox            ● AI Assistant: Active │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- Page title with message icon
- AI status indicator with pulsing animation
- Real-time status display

### Main Grid Layout (3 Columns)
```
┌─────────────┬─────────────┬─────────────┐
│   Active    │   Chat      │   AI        │
│   Leads     │   Room      │   Copilot   │
│  (span-3)   │  (span-6)   │  (span-3)   │
│             │             │             │
│ Lead List   │ Messages    │ Smart       │
│             │             │ Replies     │
│             │ Input Area  │ Insights    │
└─────────────┴─────────────┴─────────────┘
```

## 📊 Column Details

### Left Column - Active Leads (span-3)
**Grid Position**: `col-span-3`
**Background**: `bg-zinc-950`

#### Lead List Features:
- **Lead Information**: Name, last message preview, timestamp
- **Source Badges**: WhatsApp (green), Telegram (blue), Email (purple), Web (orange)
- **Unread Indicators**: Green dots for unread messages
- **Active State**: Emerald left border when selected
- **Hover Effects**: Background change and cursor pointer

**Lead Data Structure:**
```typescript
interface Lead {
  id: string
  name: string
  lastMessage: string
  source: 'whatsapp' | 'telegram' | 'email' | 'web'
  timestamp: string
  unread: boolean
  isActive: boolean
}
```

**Sample Leads:**
1. **Budi Santoso - PT. Maju Bersama** (WhatsApp) - "Apakah ada unit 3BR di Jakarta Selatan?"
2. **Siti Nurhaliza** (Telegram) - "Saya tertarik dengan cluster di Tangerang"
3. **Ahmad Fauzi** (Email) - "Bisa kirim pricelist untuk tipe 36?"
4. **Dewi Lestari** (Web) - "Kapan bisa survei lokasi?"

### Middle Column - Chat Room (span-6)
**Grid Position**: `col-span-6`
**Background**: `bg-black`

#### Chat Features:
- **Message Bubbles**: Different styling for lead vs agent vs AI messages
- **Real-time Typing**: Animated dots when AI is typing
- **Message Status**: Sent, delivered, read indicators
- **Auto-scroll**: Automatic scroll to latest messages
- **Timestamps**: Localized time display

**Message Styling:**
```css
/* Lead Messages (Left) */
.bg-zinc-900 text-zinc-100

/* Agent Messages (Right) */
.bg-zinc-800 text-zinc-100

/* AI Messages (Right) */
.bg-emerald-900/50 border border-emerald-500/30 text-emerald-100
```

#### Input Area:
- **Premium Design**: Dark theme with emerald accents
- **Attachment Button**: Paperclip icon
- **Send Button**: Emerald background with Send icon
- **Keyboard Support**: Enter to send functionality
- **Placeholder**: "Type your message..."

### Right Column - AI Copilot (span-3)
**Grid Position**: `col-span-3`
**Background**: `bg-zinc-950` with left border

#### AI Smart Replies:
**3 Contextual Suggestions:**
1. **Kirim Pricelist** - Target icon (pricing category)
2. **Tawarkan Diskon KPR** - TrendingUp icon (promotion category)
3. **Ajak Survei Lokasi** - Globe icon (action category)

**Button Design:**
```css
border-zinc-700 hover:border-emerald-500 hover:bg-emerald-500/10
```

#### AI Insights Panel:
- **Lead Intent Analysis**: High purchase intent detection
- **Best Contact Time**: Optimal follow-up timing
- **Interest Preferences**: Property type preferences
- **Visual Indicators**: Color-coded insight dots

## 🎨 Design Elements

### Color Palette
- **Background**: `bg-black` (pitch-black)
- **Surfaces**: `bg-zinc-950` (dark panels)
- **Borders**: `border-zinc-800` (subtle dividers)
- **Text**: `text-zinc-100` (primary), `text-zinc-500` (secondary)
- **Accent**: `text-emerald-400` (neon green)
- **Hover**: `hover:bg-emerald-500/10` (subtle emerald)

### Typography
- **Headers**: `text-2xl font-bold` (page title), `text-lg font-semibold` (section headers)
- **Content**: `text-zinc-100` (primary text)
- **Meta**: `text-zinc-500 text-sm` (timestamps, counts)
- **Placeholders**: `placeholder-zinc-500`

### Animations
- **AI Status**: `animate-pulse` for active indicator
- **Typing**: Bouncing dots animation
- **Transitions**: `transition-all duration-200` for smooth interactions
- **Hover Effects**: Background and border color changes

## 🔧 Technical Implementation

### State Management
```typescript
const [selectedLead, setSelectedLead] = useState<Lead | null>(null)
const [messages, setMessages] = useState<Message[]>([])
const [inputMessage, setInputMessage] = useState('')
const [isTyping, setIsTyping] = useState(false)
const [activeLeads, setActiveLeads] = useState<Lead[]>([])
```

### Event Handlers
```typescript
// Lead selection
const handleLeadSelect = (lead: Lead) => {
  setSelectedLead(lead)
  setMessages(messagesData[lead.id] || [])
}

// Message sending
const handleSendMessage = () => {
  // Add message to chat
  // Simulate AI response
  // Update typing indicator
}

// Smart reply selection
const handleSmartReply = (reply: SmartReply) => {
  setInputMessage(reply.text)
}
```

### Auto-scroll Implementation
```typescript
const messagesEndRef = useRef<HTMLDivElement>(null)

useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
}, [messages])
```

### Source Badge System
```typescript
const getSourceInfo = (source: Lead['source']) => {
  switch (source) {
    case 'whatsapp':
      return { icon: MessageCircle, color: 'bg-green-500/20 text-green-400' }
    case 'telegram':
      return { icon: Send, color: 'bg-blue-500/20 text-blue-400' }
    case 'email':
      return { icon: Mail, color: 'bg-purple-500/20 text-purple-400' }
    case 'web':
      return { icon: Globe, color: 'bg-orange-500/20 text-orange-400' }
  }
}
```

## 📱 Responsive Design

### Desktop (md+)
- **3-column layout**: 3-6-3 span distribution
- **Full height**: `h-[80vh]` for main area
- **Optimal spacing**: Proper padding and margins

### Mobile (sm)
- **Single column**: Stack layout
- **Compact view**: Optimized for touch
- **Full width**: Each column takes full width

## 🤖 AI Integration Features

### Smart Reply System
- **Contextual Suggestions**: Based on conversation history
- **Category-based**: Pricing, promotion, action categories
- **One-click Insert**: Auto-fill input field
- **Icon Support**: Visual category indicators

### AI Insights
- **Lead Scoring**: Purchase intent analysis
- **Timing Optimization**: Best contact time recommendations
- **Preference Detection**: Property type and feature preferences
- **Visual Analytics**: Color-coded insight indicators

### Typing Indicators
- **Real-time Feedback**: Animated dots when AI is responding
- **Natural Delays**: Realistic typing simulation
- **Status Updates**: Clear indication of AI activity

## 🧪 Testing

### Automated Testing
```bash
# Run test script
node test_inbox_page.js
```

**Test Coverage:**
- Page accessibility and rendering
- Component structure validation
- UI/UX element verification
- Feature functionality testing

### Manual Testing Checklist
- [ ] Page loads correctly at `/inbox`
- [ ] 3-column layout displays properly
- [ ] Lead selection works and switches conversations
- [ ] Message sending functionality works
- [ ] AI typing indicators appear
- [ ] Smart reply buttons auto-fill input
- [ ] Hover effects and transitions work
- [ ] Responsive design on mobile
- [ ] Dark mode styling is consistent
- [ ] Scroll areas work properly

## 🚀 Usage Examples

### Navigation
```typescript
// From dashboard or navigation
<Link href="/inbox">
  Omni-Channel Inbox
</Link>

// Programmatic navigation
router.push('/inbox')
```

### Message Handling
```typescript
// Send message
const handleSendMessage = () => {
  if (!inputMessage.trim() || !selectedLead) return
  
  const newMessage: Message = {
    id: Date.now().toString(),
    content: inputMessage,
    sender: 'agent',
    timestamp: new Date().toLocaleTimeString('id-ID', { 
      hour: '2-digit', 
      minute: '2-digit' 
    }),
    status: 'sent'
  }
  
  setMessages(prev => [...prev, newMessage])
  setInputMessage('')
  setIsTyping(true)
  
  // Simulate AI response
  setTimeout(() => {
    const aiResponse: Message = {
      id: (Date.now() + 1).toString(),
      content: 'Terima kasih atas pesannya. Saya akan segera memproses permintaan Anda.',
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString('id-ID', { 
        hour: '2-digit', 
        minute: '2-digit' 
      }),
      status: 'sent'
    }
    setMessages(prev => [...prev, aiResponse])
    setIsTyping(false)
  }, 1500)
}
```

## 🎯 Business Value

### User Experience
- **Unified Inbox**: All channels in one interface
- **AI Assistance**: Smart replies and insights
- **Real-time Communication**: Instant messaging experience
- **Professional Design**: Modern, clean interface

### Operational Efficiency
- **Multi-channel Support**: WhatsApp, Telegram, Email, Web
- **Smart Automation**: AI-powered responses and suggestions
- **Lead Management**: Easy conversation switching
- **Time Optimization**: Best contact time recommendations

### Sales Performance
- **Faster Response**: Quick reply suggestions
- **Better Conversion**: AI insights for lead qualification
- **Improved Tracking**: Message status and read receipts
- **Enhanced Productivity**: Reduced response time

## 🔮 Future Enhancements

### Advanced Features
- [ ] Voice message support
- [ ] File attachment handling
- [ ] Message templates
- [ ] Auto-assignment rules
- [ ] Analytics dashboard
- [ ] Integration with CRM

### AI Improvements
- [ ] Natural language processing
- [ ] Sentiment analysis
- [ ] Lead scoring algorithms
- [ ] Predictive responses
- [ ] Multi-language support

### Communication Channels
- [ ] Instagram Direct
- [ ] Facebook Messenger
- [ ] SMS integration
- [ ] WeChat support
- [ ] Custom channel APIs

---

## 🚀 Quick Start

1. **Ensure Dependencies**: All packages installed including ReactFlow
2. **Start Server**: `npm run dev`
3. **Navigate**: `http://localhost:3000/inbox`
4. **Test**: `node test_inbox_page.js`

## 📁 File Structure
```
dashboard/
├── app/inbox/page.tsx              # Main inbox page
├── components/ui/scroll-area.tsx   # Scroll area component
├── test_inbox_page.js              # Test script
└── INBOX_DOCUMENTATION.md          # This documentation
```

---

*Last updated: May 30, 2026*

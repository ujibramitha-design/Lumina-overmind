# JARVIS Mobile Command Center

Mobile application for JARVIS AI System - HUD-style interface with real-time system monitoring, chat, and code exploration capabilities.

## 📁 Structure

```
jarvis-mobile/
├── screens/
│   ├── Dashboard.js           # Main HUD dashboard
│   ├── Chat.js                # Real-time chat interface
│   └── CodeExplorer.js        # Codebase exploration
├── services/
│   └── auth.js                # Service token authentication
├── theme.js                   # HUD theme configuration
├── package.json               # Dependencies
├── app.json                   # Expo configuration
└── build-android.js          # APK build script
```

## 🎨 Design Philosophy

**HUD-Style Interface:**
- Futuristic dark theme
- Glassmorphism effects
- Neon green accent borders (#10b981)
- Glowing elements
- Clean typography
- High-tech aesthetic

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd jarvis-mobile
npm install
```

### 2. Configure Environment

Create `.env` file:

```bash
API_BASE_URL=http://localhost:8000
JARVIS_SERVICE_TOKEN=your_service_token_here
```

### 3. Run Development

```bash
# Start Expo development server
npm start

# Run on Android
npm run android

# Run on iOS
npm run ios
```

### 4. Build APK

```bash
# Install EAS CLI globally
npm install -g eas-cli

# Run build script
node build-android.js

# Or use EAS directly
eas build --platform android --profile preview
```

## 📱 Screens

### Dashboard
- Real-time system metrics (CPU, Memory, Disk, Network)
- Connection status (WhatsApp, Telegram, WebSocket)
- JARVIS thought process visualization
- Quick stats and actions

### Chat
- Real-time bi-directional chat via WebSocket
- Typing indicators
- Quick command suggestions
- Message history

### Code Explorer
- Search codebase with JARVIS awareness
- File explanations
- Function documentation
- Dependency information

## 🔐 Authentication

Uses Service Token authentication for secure communication:

```javascript
import authService from './services/auth';

// Initialize auth
await authService.initialize();

// Set service token
await authService.setToken('your_token_here');

// Make authenticated request
const metrics = await authService.getMetrics();
```

## 🌐 Backend Integration

Mobile app connects to Lumina Overmind backend via:

**API Endpoints:**
- `GET /api/jarvis-mobile/health` - Health check
- `GET /api/jarvis-mobile/metrics` - System metrics
- `GET /api/jarvis-mobile/connections` - Connection status
- `GET /api/jarvis-mobile/thought-process` - JARVIS thought process
- `POST /api/jarvis-mobile/code/search` - Search codebase
- `GET /api/jarvis-mobile/code/explain/{file}` - Explain code

**WebSocket:**
- `WS /api/jarvis-mobile/ws` - Real-time communication

## 🎨 Theme Configuration

Theme is defined in `theme.js`:

```javascript
import { colors, spacing, borderRadius, shadows } from './theme';

// Use in components
<View style={styles.glassCard}>
  <Text style={styles.neonText}>JARVIS</Text>
</View>
```

**Color Palette:**
- Background: `#000000`
- Neon Green: `#10b981`
- Glass: `rgba(20, 20, 20, 0.7)`
- Text: `#ffffff`

## 📦 Dependencies

```json
{
  "expo": "~50.0.0",
  "react": "18.2.0",
  "react-native": "0.73.0",
  "@react-navigation/native": "^6.1.9",
  "react-native-linear-gradient": "^2.8.3",
  "react-native-websocket": "^1.0.2",
  "axios": "^1.6.0"
}
```

## 🔧 Build Configuration

### EAS Build Profiles

**Preview (Testing):**
```json
{
  "build": {
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      }
    }
  }
}
```

**Production (Release):**
```json
{
  "build": {
    "production": {
      "distribution": "store",
      "android": {
        "buildType": "apk"
      }
    }
  }
}
```

## 📊 Features

### Real-Time Updates
- WebSocket connection for live data
- Auto-refresh metrics
- Connection status monitoring

### Codebase Awareness
- Search files and functions
- Get code explanations
- View dependencies
- Understand system architecture

### JARVIS Integration
- Direct chat interface
- Thought process visualization
- Proactive notifications
- Command execution

## 🚨 Troubleshooting

### Build Fails
- Check EAS CLI installation
- Verify `.env` configuration
- Ensure dependencies are installed
- Check Expo dashboard for build logs

### WebSocket Connection Issues
- Verify backend is running
- Check API_BASE_URL in .env
- Ensure service token is valid
- Check network connectivity

### Theme Not Loading
- Verify theme.js is imported correctly
- Check color palette configuration
- Ensure styles are applied

## 📝 Development

### Adding New Screens

1. Create screen in `screens/` folder
2. Apply theme styles
3. Add to navigation
4. Test on device/emulator

### Updating Theme

Edit `theme.js` to modify:
- Color palette
- Typography
- Spacing
- Shadows
- Glassmorphism effects

### Backend Integration

Add new endpoints in `api/endpoints/jarvis_mobile.py`:
```python
@router.get("/new-endpoint")
async def new_endpoint(jarvis = Depends(verify_jarvis_token)):
    return {"data": "response"}
```

## 🚀 Deployment

### Google Play Store

1. Build production APK
2. Sign with release key
3. Upload to Play Console
4. Fill store listing
5. Submit for review

### Internal Distribution

1. Build preview APK
2. Distribute via email/link
3. Install on test devices
4. Gather feedback

## 📄 License

Part of Lumina Overmind Enterprise

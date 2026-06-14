# JARVIS Absolute Resilience Documentation

Complete guide for JARVIS's absolute resilience, shapeshifting UI, and physical world actuation.

## Overview

JARVIS has been pushed to the absolute limit of computing with:
- **Bunker Protocol**: Local LLM fallback for 100% uptime without internet
- **Generative UI**: Shapeshifting dashboard with LLM-generated React components
- **Physical Actuation**: IoT/Hardware bridge for physical world control

## Bunker Protocol (Local LLM Fallback)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Bunker Protocol (Failover)                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Primary Provider (Gemini)                            │
│     ├── Google Generative AI                              │
│     ├── Gemini 1.5 Pro model                              │
│     ├── Internet required                                 │
│     ├── High quality responses                            │
│     └── 10-second timeout                                 │
│                                                          │
│  2. Fallback Provider (Ollama)                            │
│     ├── Local Llama3 instance                             │
│     ├── Ollama Node.js library                            │
│     ├── No internet required                              │
│     ├── 100% offline capability                           │
│     └── Fast-failover mechanism                           │
│                                                          │
│  3. Failover Logic                                       │
│     ├── Automatic timeout detection                        │
│     ├── Error detection (500 errors)                       │
│     ├── Instant provider switch                            │
│     ├── Status tracking                                   │
│     └── Failover logging                                 │
│                                                          │
│  4. Health Monitoring                                    │
│     ├── Provider availability checks                      │
│     ├── Automatic provider testing                         │
│     ├── Health status reporting                           │
│     └── Manual provider switching                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Brain Service Implementation

**Location:** `jarvis-system/intelligence/brainService.js`

**Key Methods:**

```javascript
class BrainService {
  // Generate response with automatic failover
  async generateResponse(systemPrompt, userPrompt, options)
  
  // Generate with Gemini (primary)
  async _generateWithGemini(systemPrompt, userPrompt, options)
  
  // Generate with Ollama (fallback)
  async _generateWithOllama(systemPrompt, userPrompt, options)
  
  // Failover to alternative provider
  async _failover(systemPrompt, userPrompt, options, failedProvider)
  
  // Force switch to specific provider
  async switchProvider(provider)
  
  // Get provider status
  getProviderStatus()
  
  // Health check
  async healthCheck()
}
```

### Failover Logic

```javascript
async generateResponse(systemPrompt, userPrompt, options = {}) {
  const provider = this.providerStatus.currentProvider;
  
  try {
    if (provider === 'gemini') {
      return await this._generateWithGemini(systemPrompt, userPrompt, options);
    } else {
      return await this._generateWithOllama(systemPrompt, userPrompt, options);
    }
  } catch (error) {
    console.error(`❌ Error with ${provider} provider:`, error.message);
    
    // Attempt failover
    return await this._failover(systemPrompt, userPrompt, options, provider);
  }
}

async _failover(systemPrompt, userPrompt, options, failedProvider) {
  console.log(`🔄 Attempting failover from ${failedProvider}...`);
  
  const fallbackProvider = failedProvider === 'gemini' ? 'ollama' : 'gemini';
  
  // Check if fallback is available
  if (this.providerStatus[fallbackProvider] === 'unavailable') {
    throw new Error(`Both providers unavailable. Cannot failover.`);
  }
  
  try {
    this.providerStatus.currentProvider = fallbackProvider;
    this.providerStatus.lastFailover = new Date().toISOString();
    this.providerStatus.failoverCount++;
    
    console.log(`🔄 Failing over to ${fallbackProvider}...`);
    
    if (fallbackProvider === 'gemini') {
      return await this._generateWithGemini(systemPrompt, userPrompt, options);
    } else {
      return await this._generateWithOllama(systemPrompt, userPrompt, options);
    }
  } catch (error) {
    console.error(`❌ Failover to ${fallbackProvider} failed:`, error.message);
    
    // Revert to original provider
    this.providerStatus.currentProvider = failedProvider;
    
    throw new Error(`Failover failed: ${error.message}`);
  }
}
```

### Usage Example

```javascript
const { getBrainService } = require('./intelligence/brainService');

const brainService = getBrainService({
  geminiApiKey: process.env.GEMINI_API_KEY,
  ollamaHost: 'http://localhost:11434',
  ollamaModel: 'llama3',
  timeout: 10000,
});

// Generate response (automatic failover)
const result = await brainService.generateResponse(
  systemPrompt,
  userPrompt
);

console.log('Response:', result.response);
console.log('Provider:', result.provider);  // 'gemini' or 'ollama'
console.log('Model:', result.model);
```

### Provider Status

```javascript
const status = brainService.getProviderStatus();

console.log('Current Provider:', status.currentProvider);
console.log('Gemini Status:', status.gemini);
console.log('Ollama Status:', status.ollama);
console.log('Last Failover:', status.lastFailover);
console.log('Failover Count:', status.failoverCount);
```

## Generative UI (Shapeshifting Dashboard)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Generative UI (Shapeshifting Dashboard)           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. LLM Component Generation                             │
│     ├── React component code generation                    │
│     ├── Tailwind CSS styling                              │
│     ├── Data visualization components                      │
│     ├── Interactive elements                               │
│     └── JSON/React code output                           │
│                                                          │
│  2. Dynamic Renderer                                      │
│     ├── Safe component rendering                          │
│     ├── Code sanitization                                 │
│     ├── Component caching                                 │
│     ├── Error boundaries                                  │
│     └── Performance optimization                          │
│                                                          │
│  3. WebSocket UI Push                                    │
│     ├── Real-time component delivery                      │
│     ├── Bi-directional communication                      │
│     ├── Component versioning                              │
│     ├── Update streaming                                  │
│     └── Connection management                            │
│                                                          │
│  4. Mobile Command Center                                │
│     ├── Component display                                 │
│     ├── User interaction                                  │
│     ├── State management                                  │
│     ├── Performance monitoring                            │
│     └── Error handling                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### React Component Renderer (Mobile App)

**Component Structure:**

```javascript
// DynamicComponentRenderer.tsx
import React, { useState, useEffect } from 'react';
import { WebSocket } from 'react-native-websocket';

interface GeneratedComponent {
  id: string;
  code: string;
  type: 'chart' | 'table' | 'card' | 'form' | 'custom';
  props: Record<string, any>;
  timestamp: string;
}

export const DynamicComponentRenderer: React.FC = () => {
  const [components, setComponents] = useState<GeneratedComponent[]>([]);
  const [wsConnected, setWsConnected] = useState(false);
  
  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:3001/ui/stream');
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setWsConnected(true);
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'component') {
          // Safe component rendering
          const safeComponent = sanitizeComponent(data);
          setComponents(prev => [...prev, safeComponent]);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setWsConnected(false);
    };
    
    return () => {
      ws.close();
    };
  }, []);
  
  const sanitizeComponent = (component: any): GeneratedComponent => {
    // Sanitize code to prevent XSS
    const sanitizedCode = component.code
      .replace(/<script[^>]*>.*?<\/script>/gi, '')
      .replace(/javascript:/gi, '')
      .replace(/on\w+="[^"]*"/gi, '');
    
    return {
      id: component.id,
      code: sanitizedCode,
      type: component.type,
      props: component.props || {},
      timestamp: component.timestamp,
    };
  };
  
  const renderComponent = (component: GeneratedComponent) => {
    try {
      // Use Function constructor for safe evaluation
      const ComponentFunction = new Function('React', component.code);
      const Component = ComponentFunction(React);
      
      return <Component {...component.props} />;
    } catch (error) {
      console.error('Error rendering component:', error);
      return <ErrorComponent error={error} />;
    }
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>JARVIS Command Center</Text>
        <View style={[styles.status, wsConnected ? styles.connected : styles.disconnected]}>
          <Text style={styles.statusText}>
            {wsConnected ? '● Connected' : '○ Disconnected'}
          </Text>
        </View>
      </View>
      
      <ScrollView style={styles.componentList}>
        {components.map(component => (
          <View key={component.id} style={styles.componentWrapper}>
            {renderComponent(component)}
          </View>
        ))}
      </ScrollView>
    </View>
  );
};

const ErrorComponent: React.FC<{ error: any }> = ({ error }) => (
  <View style={styles.error}>
    <Text style={styles.errorText}>Component Error</Text>
    <Text style={styles.errorDetail}>{error.message}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  title: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  status: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  connected: {
    backgroundColor: '#22c55e',
  },
  disconnected: {
    backgroundColor: '#ef4444',
  },
  statusText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
  componentList: {
    flex: 1,
    padding: 16,
  },
  componentWrapper: {
    marginBottom: 16,
    borderRadius: 8,
    overflow: 'hidden',
  },
  error: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#ef4444',
  },
  errorText: {
    color: '#ef4444',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  errorDetail: {
    color: '#94a3b8',
    fontSize: 14,
  },
});
```

### LLM Component Generation

**System Prompt for Component Generation:**

```
You are a UI Component Generator for JARVIS Command Center.

**Your Role:**
- Generate React/Tailwind components for data visualization
- Create interactive and responsive UI elements
- Use modern design patterns and best practices
- Ensure accessibility and performance

**Component Types:**
- Charts: Line, bar, pie, scatter charts using recharts
- Tables: Data tables with sorting and filtering
- Cards: Information cards with stats and metrics
- Forms: Input forms with validation
- Custom: Any custom component as requested

**Output Format:**
Return JSON with:
{
  "type": "component_type",
  "code": "React component code",
  "props": { "data": [...] },
  "timestamp": "ISO timestamp"
}

**Guidelines:**
- Use functional components with hooks
- Use Tailwind CSS for styling
- Include proper TypeScript types
- Handle loading and error states
- Make components responsive
- Keep code under 200 lines
```

### WebSocket UI Push

**Server-Side Implementation:**

```javascript
// In jarvis-system/index.js
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 3002 });

wss.on('connection', (ws) => {
  console.log('📱 Mobile client connected');
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      
      if (data.type === 'request_ui') {
        // Generate component
        const component = await generateComponent(data.request);
        
        // Push to client
        ws.send(JSON.stringify({
          type: 'component',
          component: component,
        }));
      }
    } catch (error) {
      console.error('Error handling WebSocket message:', error);
    }
  });
});

async function generateComponent(request) {
  const brainService = getBrainService();
  
  const prompt = `
Generate a React component for: ${request}

Output format: JSON with type, code, props, timestamp
`;
  
  const result = await brainService.generateResponse(
    componentSystemPrompt,
    prompt
  );
  
  return JSON.parse(result.response);
}
```

## Physical Actuation (IoT/Hardware Bridge)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│            Physical Actuation (IoT Bridge)                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. MQTT Protocol                                       │
│     ├── Real-time device communication                    │
│     ├── Pub/sub messaging                                │
│     ├── Device state tracking                            │
│     ├── Bidirectional control                            │
│     └── Auto-reconnection                               │
│                                                          │
│  2. HTTP Protocol                                       │
│     ├── REST API device control                          │
│     ├── Request/response pattern                         │
│     ├── Timeout handling                                 │
│     ├── Error retry logic                                │
│     └── Status polling                                   │
│                                                          │
│  3. Device Management                                    │
│     ├── Device registration                              │
│     ├── Device configuration                             │
│     ├── State monitoring                                 │
│     ├── Health checks                                    │
│     └── Device unregistration                            │
│                                                          │
│  4. Physical Hard Reboot                                 │
│     ├── Smart relay control                               │
│     ├── Power cycle management                            │
│     ├── Emergency shutdown                               │
|     ├── Automatic recovery                               │
│     └── Safety protocols                                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### IoT Bridge Implementation

**Location:** `jarvis-system/hardware/iotBridge.js`

**Key Methods:**

```javascript
class IoTBridge {
  // Send command via MQTT
  async sendMQTTCommand(topic, payload)
  
  // Send command via HTTP
  async sendHTTPCommand(endpoint, payload, method)
  
  // Control device (auto-detect protocol)
  async controlDevice(deviceId, command, payload)
  
  // Physical Hard Reboot via smart relay
  async physicalHardReboot(relayDeviceId, delay)
  
  // Emergency shutdown via relay
  async emergencyShutdown(relayDeviceId)
  
  // Get device status
  async getDeviceStatus(deviceId)
  
  // Register device
  registerDevice(deviceId, config)
  
  // Unregister device
  unregisterDevice(deviceId)
  
  // Get bridge status
  getBridgeStatus()
  
  // Health check
  async healthCheck()
}
```

### Physical Hard Reboot

```javascript
const { getIoTBridge } = require('./hardware/iotBridge');

const iotBridge = getIoTBridge({
  mqttBroker: 'mqtt://localhost:1883',
  mqttUsername: process.env.MQTT_USERNAME,
  mqttPassword: process.env.MQTT_PASSWORD,
});

// Register smart relay device
iotBridge.registerDevice('server_relay', {
  protocol: 'mqtt',
  topic: 'jarvis/devices/server_relay',
  type: 'relay',
});

// Execute physical hard reboot
const result = await iotBridge.physicalHardReboot('server_relay', 5000);

console.log('Hard Reboot Result:', result);
// Output:
// {
//   success: true,
//   message: 'Physical Hard Reboot completed successfully',
//   deviceId: 'server_relay',
//   delay: 5000,
//   completedAt: '2024-01-15T10:00:00Z'
// }
```

### Device Configuration

```javascript
// MQTT Device
iotBridge.registerDevice('esp32_sensor', {
  protocol: 'mqtt',
  topic: 'jarvis/devices/esp32_sensor',
  type: 'sensor',
});

// HTTP Device
iotBridge.registerDevice 'raspberry_pi_camera', {
  protocol: 'http',
  endpoint: 'http://192.168.1.100:8080/control',
  type: 'camera',
});

// Smart Relay
iotBridge.registerDevice('server_relay', {
  protocol: 'mqtt',
  topic: 'jarvis/devices/server_relay',
  type: 'relay',
});
```

## Configuration

### Environment Variables

```bash
# Bunker Protocol
GEMINI_API_KEY=your_gemini_api_key
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
BRAIN_TIMEOUT=10000

# Generative UI
UI_WEBSOCKET_PORT=3002
UI_COMPONENT_CACHE_SIZE=100

# IoT Bridge
MQTT_BROKER=mqtt://localhost:1883
MQTT_USERNAME=jarvis
MQTT_PASSWORD=secure_password
HTTP_TIMEOUT=5000
```

### Brain Service Configuration

```javascript
const config = {
  primaryProvider: 'gemini',
  fallbackProvider: 'ollama',
  geminiApiKey: process.env.GEMINI_API_KEY,
  ollamaHost: 'http://localhost:11434',
  ollamaModel: 'llama3',
  geminiModel: 'gemini-1.5-pro',
  timeout: 10000,
  maxRetries: 3,
};
```

### IoT Bridge Configuration

```javascript
const config = {
  mqttBroker: 'mqtt://localhost:1883',
  mqttUsername: 'jarvis',
  mqttPassword: 'secure_password',
  httpTimeout: 5000,
  devices: {
    server_relay: {
      protocol: 'mqtt',
      topic: 'jarvis/devices/server_relay',
      type: 'relay',
    },
  },
};
```

## Best Practices

### For Bunker Protocol

1. **Test Both Providers**: Regularly test both Gemini and Ollama
2. **Monitor Failover**: Track failover events and frequency
3. **Set Appropriate Timeouts**: Balance between responsiveness and reliability
4. **Local LLM Setup**: Ensure Ollama is properly configured
5. **Network Redundancy**: Have backup internet connection if possible

### For Generative UI

1. **Sanitize All Code**: Prevent XSS attacks
2. **Use Error Boundaries**: Handle component rendering errors
3. **Cache Components**: Reduce generation overhead
4. **Limit Component Size**: Keep components under 200 lines
5. **Test on Multiple Devices**: Ensure cross-platform compatibility

### For IoT Bridge

1. **Secure MQTT**: Use authentication and encryption
2. **Monitor Device Health**: Regular health checks
3. **Implement Timeouts**: Prevent hanging requests
4. **Log All Actions**: Maintain audit trail
5. **Test Emergency Procedures**: Regular emergency shutdown tests

## Troubleshooting

### Bunker Protocol Issues

**Failover Not Working:**
```javascript
// Check provider status
const status = brainService.getProviderStatus();
console.log('Status:', status);

// Test providers individually
const health = await brainService.healthCheck();
console.log('Health:', health);

// Manual provider switch
await brainService.switchProvider('ollama');
```

**Ollama Not Responding:**
```bash
# Check Ollama status
ollama list

# Start Ollama
ollama serve

# Pull model
ollama pull llama3
```

### Generative UI Issues

**Component Not Rendering:**
```javascript
// Check WebSocket connection
console.log('Connected:', wsConnected);

// Check component sanitization
const sanitized = sanitizeComponent(component);
console.log('Sanitized:', sanitized);

// Test component rendering
try {
  const Component = new Function('React', component.code)(React);
  console.log('Component:', Component);
} catch (error) {
  console.error('Render error:', error);
}
```

### IoT Bridge Issues

**MQTT Not Connecting:**
```javascript
// Check broker status
const status = iotBridge.getBridgeStatus();
console.log('MQTT Connected:', status.mqttConnected);

// Test connection manually
const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://localhost:1883');
```

**Device Not Responding:**
```javascript
// Check device status
const deviceStatus = await iotBridge.getDeviceStatus('server_relay');
console.log('Device Status:', deviceStatus);

// Test device control
const result = await iotBridge.controlDevice('server_relay', 'status');
console.log('Control Result:', result);
```

## Security Considerations

### Bunker Protocol Security

1. **API Key Protection**: Secure Gemini API key
2. **Local LLM Security**: Secure Ollama installation
3. **Network Security**: Use VPN for remote access
4. **Access Control**: Limit brain service access
5. **Audit Logging**: Log all provider switches

### Generative UI Security

1. **Code Sanitization**: Prevent XSS attacks
2. **Component Validation**: Validate component structure
3. **Resource Limits**: Limit component size and complexity
4. **User Permissions**: Control who can generate UI
5. **Audit Trail**: Log all component generations

### IoT Bridge Security

1. **MQTT Authentication**: Use username/password
2. **TLS Encryption**: Use MQTT over TLS
3. **Device Authentication**: Authenticate IoT devices
4. **Network Segmentation**: Separate IoT network
5. **Physical Security**: Secure physical access to devices

## Performance Considerations

### Bunker Protocol Performance

- **Gemini Latency**: ~1-3 seconds
- **Ollama Latency**: ~2-5 seconds
- **Failover Time**: <1 second
- **Total Response Time**: ~3-8 seconds
- **Memory Usage**: ~500MB for Ollama

### Generative UI Performance

- **Component Generation**: ~2-5 seconds
- **WebSocket Latency**: <100ms
- **Component Rendering**: ~100-500ms
- **Total UI Update**: ~3-6 seconds
- **Memory Usage**: ~100MB per component

### IoT Bridge Performance

- **MQTT Latency**: <50ms
- **HTTP Latency**: ~100-500ms
- **Device Response**: ~50-200ms
- **Total Command Time**: ~200-700ms
- **Memory Usage**: ~50MB

## Monitoring

### Bunker Protocol Monitoring

```javascript
// Provider status
const status = brainService.getProviderStatus();
console.log('Current Provider:', status.currentProvider);
console.log('Failover Count:', status.failoverCount);

// Health check
const health = await brainService.healthCheck();
console.log('Healthy:', health.healthy);
console.log('Providers:', health.providers);
```

### Generative UI Monitoring

```javascript
// WebSocket status
console.log('Connected:', wsConnected);
console.log('Components:', components.length);

// Component performance
const renderTime = performance.now() - startTime;
console.log('Render Time:', renderTime);
```

### IoT Bridge Monitoring

```javascript
// Bridge status
const status = iotBridge.getBridgeStatus();
console.log('MQTT Connected:', status.mqttConnected);
console.log('Devices:', status.registeredDevices);

// Device health
const health = await iotBridge.healthCheck();
console.log('Healthy:', health.healthy);
console.log('Device Status:', health.devices);
```

## Future Enhancements

### Planned Features

- **Multiple Fallback Providers**: Add more LLM providers
- **Component Library**: Pre-built component templates
- **Device Automation**: Automated device control sequences
- **Predictive Failover**: Predict provider failures
- **Component Versioning**: Track component versions
- **Device Groups**: Group devices for batch control
- **Performance Optimization**: Optimize all systems
- **Enhanced Security**: Add more security layers

### Community Contributions

Contributions welcome for:
- More LLM providers
- Better component rendering
- More device protocols
- Performance optimizations
- Security enhancements
- Documentation improvements

## Support

For issues or questions:
- Check provider status
- Verify Ollama installation
- Test WebSocket connection
- Check MQTT broker
- Review device configuration
- Monitor system logs

## License

This feature is part of JARVIS AI System.
See main project license for details.

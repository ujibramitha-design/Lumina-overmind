/**
 * JARVIS IoT Bridge - Physical World Actuation
 * ==========================================
 * 
 * Hardware bridge for IoT devices using MQTT and HTTP.
 * Enables physical actuation including hard reboot capability.
 */

const mqtt = require('mqtt');
const axios = require('axios');
require('dotenv').config();

class IoTBridge {
  constructor(config = {}) {
    this.config = {
      mqttBroker: config.mqttBroker || process.env.MQTT_BROKER || 'mqtt://localhost:1883',
      mqttUsername: config.mqttUsername || process.env.MQTT_USERNAME,
      mqttPassword: config.mqttPassword || process.env.MQTT_PASSWORD,
      httpTimeout: config.httpTimeout || 5000,
      devices: config.devices || {},
      ...config,
    };
    
    this.mqttClient = null;
    this.connected = false;
    this.deviceStates = {};
    
    this._initializeMQTT();
  }
  
  /**
   * Initialize MQTT client
   */
  _initializeMQTT() {
    try {
      const options = {
        username: this.config.mqttUsername,
        password: this.config.mqttPassword,
        reconnectPeriod: 5000,
      };
      
      this.mqttClient = mqtt.connect(this.config.mqttBroker, options);
      
      this.mqttClient.on('connect', () => {
        console.log('🔌 MQTT connected');
        this.connected = true;
      });
      
      this.mqttClient.on('error', (error) => {
        console.error('❌ MQTT error:', error.message);
        this.connected = false;
      });
      
      this.mqttClient.on('close', () => {
        console.log('🔌 MQTT disconnected');
        this.connected = false;
      });
      
    } catch (error) {
      console.error('❌ Error initializing MQTT:', error.message);
    }
  }
  
  /**
   * Send command via MQTT
   */
  async sendMQTTCommand(topic, payload) {
    try {
      if (!this.connected || !this.mqttClient) {
        throw new Error('MQTT client not connected');
      }
      
      return new Promise((resolve, reject) => {
        this.mqttClient.publish(topic, JSON.stringify(payload), (error) => {
          if (error) {
            reject(error);
          } else {
            resolve({
              success: true,
              topic: topic,
              payload: payload,
              sentAt: new Date().toISOString(),
            });
          }
        });
      });
      
    } catch (error) {
      console.error('❌ Error sending MQTT command:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Send command via HTTP
   */
  async sendHTTPCommand(endpoint, payload, method = 'POST') {
    try {
      const response = await axios({
        method: method,
        url: endpoint,
        data: payload,
        timeout: this.config.httpTimeout,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      return {
        success: true,
        status: response.status,
        data: response.data,
        sentAt: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('❌ Error sending HTTP command:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Control device (auto-detect protocol)
   */
  async controlDevice(deviceId, command, payload = {}) {
    try {
      const device = this.config.devices[deviceId];
      
      if (!device) {
        throw new Error(`Device ${deviceId} not found`);
      }
      
      const protocol = device.protocol || 'mqtt';
      
      if (protocol === 'mqtt') {
        const topic = device.topic || `jarvis/devices/${deviceId}`;
        return await this.sendMQTTCommand(topic, {
          command: command,
          payload: payload,
          timestamp: new Date().toISOString(),
        });
      } else if (protocol === 'http') {
        const endpoint = device.endpoint;
        return await this.sendHTTPCommand(endpoint, {
          command: command,
          payload: payload,
        });
      } else {
        throw new Error(`Unsupported protocol: ${protocol}`);
      }
      
    } catch (error) {
      console.error('❌ Error controlling device:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Physical Hard Reboot via smart relay
   */
  async physicalHardReboot(relayDeviceId, delay = 5000) {
    try {
      console.log('🔌 Initiating Physical Hard Reboot...');
      console.log(`📡 Relay Device: ${relayDeviceId}`);
      console.log(`⏱️ Delay: ${delay}ms`);
      
      // Step 1: Turn off relay
      const offResult = await this.controlDevice(relayDeviceId, 'off');
      
      if (!offResult.success) {
        throw new Error(`Failed to turn off relay: ${offResult.error}`);
      }
      
      console.log('✅ Relay turned OFF');
      
      // Step 2: Wait for delay
      console.log(`⏱️ Waiting ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
      
      // Step 3: Turn on relay
      const onResult = await this.controlDevice(relayDeviceId, 'on');
      
      if (!onResult.success) {
        throw new Error(`Failed to turn on relay: ${onResult.error}`);
      }
      
      console.log('✅ Relay turned ON');
      console.log('🔄 Physical Hard Reboot complete');
      
      return {
        success: true,
        message: 'Physical Hard Reboot completed successfully',
        deviceId: relayDeviceId,
        delay: delay,
        completedAt: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('❌ Physical Hard Reboot failed:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Emergency shutdown via relay
   */
  async emergencyShutdown(relayDeviceId) {
    try {
      console.log('🚨 Initiating Emergency Shutdown...');
      
      const result = await this.controlDevice(relayDeviceId, 'off');
      
      if (!result.success) {
        throw new Error(`Emergency shutdown failed: ${result.error}`);
      }
      
      console.log('🚨 Emergency Shutdown complete');
      
      return {
        success: true,
        message: 'Emergency Shutdown completed',
        deviceId: relayDeviceId,
        completedAt: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('❌ Emergency Shutdown failed:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get device status
   */
  async getDeviceStatus(deviceId) {
    try {
      const device = this.config.devices[deviceId];
      
      if (!device) {
        throw new Error(`Device ${deviceId} not found`);
      }
      
      const result = await this.controlDevice(deviceId, 'status');
      
      this.deviceStates[deviceId] = result;
      
      return result;
      
    } catch (error) {
      console.error('❌ Error getting device status:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Register device
   */
  registerDevice(deviceId, config) {
    this.config.devices[deviceId] = config;
    console.log(`📱 Device registered: ${deviceId}`);
    
    return {
      success: true,
      deviceId: deviceId,
      config: config,
    };
  }
  
  /**
   * Unregister device
   */
  unregisterDevice(deviceId) {
    delete this.config.devices[deviceId];
    console.log(`📱 Device unregistered: ${deviceId}`);
    
    return {
      success: true,
      deviceId: deviceId,
    };
  }
  
  /**
   * Get bridge status
   */
  getBridgeStatus() {
    return {
      mqttConnected: this.connected,
      mqttBroker: this.config.mqttBroker,
      registeredDevices: Object.keys(this.config.devices),
      deviceStates: this.deviceStates,
    };
  }
  
  /**
   * Health check
   */
  async healthCheck() {
    const status = {
      healthy: false,
      mqtt: this.connected,
      devices: {},
    };
    
    // Check each device
    for (const deviceId of Object.keys(this.config.devices)) {
      try {
        const deviceStatus = await this.getDeviceStatus(deviceId);
        status.devices[deviceId] = deviceStatus.success ? 'healthy' : 'unhealthy';
      } catch (error) {
        status.devices[deviceId] = 'unhealthy';
      }
    }
    
    status.healthy = status.mqtt || Object.values(status.devices).some(s => s === 'healthy');
    
    return status;
  }
}

// Singleton instance
let iotBridge = null;

function getIoTBridge(config = null) {
  if (!iotBridge) {
    if (config === null) {
      config = {};
    }
    iotBridge = new IoTBridge(config);
  }
  return iotBridge;
}

module.exports = { IoTBridge, getIoTBridge };

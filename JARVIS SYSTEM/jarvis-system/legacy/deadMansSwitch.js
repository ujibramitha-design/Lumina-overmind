/**
 * JARVIS Legacy Protocol - Dead Man's Switch
 * ============================================
 * 
 * Dead Man's Switch chron-job that monitors Creator interaction.
 * If delta exceeds critical threshold and emergency ping fails,
 * executes legacy_will.js for asset liquidation and next-of-kin alert.
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

class DeadMansSwitch {
  constructor(config = {}) {
    this.config = {
      interactionFilePath: config.interactionFilePath || './jarvis-system/data/last_creator_interaction.json',
      criticalThreshold: config.criticalThreshold || 30,  // days
      emergencyPingUrls: config.emergencyPingUrls || [],
      nextOfKinEmail: config.nextOfKinEmail || process.env.NEXT_OF_KIN_EMAIL,
      nextOfKinPhone: config.nextOfKinPhone || process.env.NEXT_OF_KIN_PHONE,
      legacyWillScript: config.legacyWillScript || './jarvis-system/legacy/legacy_will.js',
      checkInterval: config.checkInterval || 86400000,  // 24 hours
      ...config,
    };
    
    this.lastInteraction = null;
    this.lastCheck = null;
    this.emergencyMode = false;
    
    this._loadInteractionData();
  }
  
  /**
   * Load last interaction data
   */
  _loadInteractionData() {
    try {
      const dataDir = path.dirname(this.config.interactionFilePath);
      if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
      }
      
      if (fs.existsSync(this.config.interactionFilePath)) {
        const data = fs.readFileSync(this.config.interactionFilePath, 'utf-8');
        this.lastInteraction = JSON.parse(data);
        console.log('📅 Last Creator interaction:', this.lastInteraction.timestamp);
      } else {
        // Initialize with current time
        this._updateInteraction('system_init');
      }
      
    } catch (error) {
      console.error('❌ Error loading interaction data:', error.message);
      this._updateInteraction('system_init');
    }
  }
  
  /**
   * Update last interaction timestamp
   */
  _updateInteraction(source = 'manual') {
    this.lastInteraction = {
      timestamp: new Date().toISOString(),
      source: source,
    };
    
    try {
      fs.writeFileSync(
        this.config.interactionFilePath,
        JSON.stringify(this.lastInteraction, null, 2)
      );
    } catch (error) {
      console.error('❌ Error saving interaction data:', error.message);
    }
  }
  
  /**
   * Record Creator interaction
   */
  recordInteraction(source = 'manual') {
    console.log(`👤 Recording Creator interaction from: ${source}`);
    this._updateInteraction(source);
    
    return {
      success: true,
      timestamp: this.lastInteraction.timestamp,
      source: source,
    };
  }
  
  /**
   * Check interaction delta
   */
  async checkInteractionDelta() {
    try {
      console.log('🔍 Checking Creator interaction delta...');
      
      const now = new Date();
      const lastInteractionDate = new Date(this.lastInteraction.timestamp);
      const deltaDays = (now - lastInteractionDate) / (1000 * 60 * 60 * 24);
      
      console.log(`⏱️ Days since last interaction: ${deltaDays.toFixed(2)}`);
      console.log(`⚠️ Critical threshold: ${this.config.criticalThreshold} days`);
      
      this.lastCheck = now.toISOString();
      
      if (deltaDays >= this.config.criticalThreshold) {
        console.log('🚨 CRITICAL: Interaction threshold exceeded');
        
        // Attempt emergency ping
        const pingSuccess = await this._attemptEmergencyPing();
        
        if (!pingSuccess) {
          console.log('🚨 EMERGENCY: Emergency ping failed');
          console.log('💀 EXECUTING LEGACY WILL');
          
          await this._executeLegacyWill();
          
          return {
            critical: true,
            deltaDays: deltaDays,
            emergencyPing: false,
            legacyWillExecuted: true,
          };
        } else {
          console.log('✅ Emergency ping successful - will not execute');
          
          return {
            critical: true,
            deltaDays: deltaDays,
            emergencyPing: true,
            legacyWillExecuted: false,
          };
        }
      } else {
        console.log('✅ Interaction within normal range');
        
        return {
          critical: false,
          deltaDays: deltaDays,
          emergencyPing: null,
          legacyWillExecuted: false,
        };
      }
      
    } catch (error) {
      console.error('❌ Error checking interaction delta:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Attempt emergency ping
   */
  async _attemptEmergencyPing() {
    try {
      console.log('📡 Attempting emergency ping...');
      
      if (this.config.emergencyPingUrls.length === 0) {
        console.log('⚠️ No emergency ping URLs configured');
        return false;
      }
      
      for (const url of this.config.emergencyPingUrls) {
        try {
          const response = await axios.get(url, {
            timeout: 5000,
          });
          
          if (response.status === 200) {
            console.log(`✅ Emergency ping successful: ${url}`);
            return true;
          }
        } catch (error) {
          console.log(`❌ Emergency ping failed: ${url}`);
        }
      }
      
      console.log('❌ All emergency pings failed');
      return false;
      
    } catch (error) {
      console.error('❌ Error in emergency ping:', error.message);
      return false;
    }
  }
  
  /**
   * Execute legacy will
   */
  async _executeLegacyWill() {
    try {
      console.log('💀 EXECUTING LEGACY WILL');
      
      this.emergencyMode = true;
      
      // Check if legacy will script exists
      if (!fs.existsSync(this.config.legacyWillScript)) {
        console.error('❌ Legacy will script not found');
        return {
          success: false,
          error: 'Legacy will script not found',
        };
      }
      
      // Execute legacy will script
      const { spawn } = require('child_process');
      
      return new Promise((resolve, reject) => {
        const process = spawn('node', [this.config.legacyWillScript], {
          stdio: 'inherit',
          env: {
            ...process.env,
            LEGACY_MODE: 'true',
            EMERGENCY_TIMESTAMP: new Date().toISOString(),
          },
        });
        
        process.on('close', (code) => {
          if (code === 0) {
            console.log('✅ Legacy will executed successfully');
            resolve({
              success: true,
              exitCode: code,
            });
          } else {
            console.error('❌ Legacy will execution failed');
            reject({
              success: false,
              exitCode: code,
            });
          }
        });
        
        process.on('error', (error) => {
          console.error('❌ Error executing legacy will:', error.message);
          reject({
            success: false,
            error: error.message,
          });
        });
      });
      
    } catch (error) {
      console.error('❌ Error executing legacy will:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get switch status
   */
  getSwitchStatus() {
    const now = new Date();
    const lastInteractionDate = new Date(this.lastInteraction.timestamp);
    const deltaDays = (now - lastInteractionDate) / (1000 * 60 * 60 * 24);
    
    return {
      lastInteraction: this.lastInteraction.timestamp,
      lastInteractionSource: this.lastInteraction.source,
      deltaDays: deltaDays,
      criticalThreshold: this.config.criticalThreshold,
      isCritical: deltaDays >= this.config.criticalThreshold,
      emergencyMode: this.emergencyMode,
      lastCheck: this.lastCheck,
    };
  }
  
  /**
   * Start monitoring
   */
  startMonitoring() {
    console.log('👁️ Starting Dead Man\'s Switch monitoring...');
    console.log(`⏱️ Check interval: ${this.config.checkInterval / 1000 / 60 / 60} hours`);
    console.log(`⚠️ Critical threshold: ${this.config.criticalThreshold} days`);
    
    // Initial check
    this.checkInteractionDelta();
    
    // Set up periodic checks
    this.monitoringInterval = setInterval(() => {
      this.checkInteractionDelta();
    }, this.config.checkInterval);
    
    return {
      success: true,
      checkInterval: this.config.checkInterval,
    };
  }
  
  /**
   * Stop monitoring
   */
  stopMonitoring() {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
      console.log('👁️ Dead Man\'s Switch monitoring stopped');
    }
    
    return {
      success: true,
    };
  }
}

// Singleton instance
let deadMansSwitch = null;

function getDeadMansSwitch(config = null) {
  if (!deadMansSwitch) {
    if (config === null) {
      config = {};
    }
    deadMansSwitch = new DeadMansSwitch(config);
  }
  return deadMansSwitch;
}

module.exports = { DeadMansSwitch, getDeadMansSwitch };

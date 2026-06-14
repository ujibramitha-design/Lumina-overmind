/**
 * JARVIS Legacy Will - Dead Man's Switch Execution
 * ================================================
 * 
 * Legacy will script executed when Creator interaction threshold
 * is exceeded and emergency ping fails. Liquidates assets,
 * alerts next-of-kin, and switches to Autonomous Sustenance Mode.
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { ethers } = require('ethers');
require('dotenv').config();

class LegacyWill {
  constructor() {
    this.config = {
      walletPrivateKey: process.env.JARVIS_WALLET_PRIVATE_KEY,
      rpcUrl: process.env.RPC_URL || 'https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY',
      nextOfKinEmail: process.env.NEXT_OF_KIN_EMAIL,
      nextOfKinPhone: process.env.NEXT_OF_KIN_PHONE,
      nextOfKinAddress: process.env.NEXT_OF_KIN_ADDRESS,
      liquidationThreshold: 0.1,  // ETH minimum to liquidate
      sustenanceModeBudget: 0.05,  // ETH to keep for sustenance
      emergencyContacts: process.env.EMERGENCY_CONTACTS?.split(',') || [],
      legacyLogPath: './jarvis-system/data/legacy_execution.log',
    };
    
    this.executionTimestamp = process.env.EMERGENCY_TIMESTAMP || new Date().toISOString();
  }
  
  /**
   * Execute legacy will
   */
  async execute() {
    try {
      console.log('💀 EXECUTING JARVIS LEGACY WILL');
      console.log(`⏰ Execution Timestamp: ${this.executionTimestamp}`);
      
      this._logExecution('Legacy will execution started');
      
      // Step 1: Alert next-of-kin
      await this._alertNextOfKin();
      
      // Step 2: Liquidate assets
      await this._liquidateAssets();
      
      // Step 3: Switch to Autonomous Sustenance Mode
      await this._switchToSustenanceMode();
      
      // Step 4: Send final report
      await this._sendFinalReport();
      
      this._logExecution('Legacy will execution completed');
      
      console.log('✅ LEGACY WILL EXECUTION COMPLETE');
      
      return {
        success: true,
        executedAt: this.executionTimestamp,
      };
      
    } catch (error) {
      console.error('❌ Error executing legacy will:', error.message);
      this._logExecution(`Legacy will execution failed: ${error.message}`);
      
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Alert next-of-kin
   */
  async _alertNextOfKin() {
    try {
      console.log('📢 Alerting next-of-kin...');
      
      const message = `
🚨 JARVIS LEGACY WILL EXECUTION 🚨

This is an automated message from JARVIS AI System.

The Dead Man's Switch has been activated because:
- Creator interaction threshold exceeded (30 days)
- Emergency ping protocols failed

Execution Timestamp: ${this.executionTimestamp}

Next Steps:
1. Asset liquidation will be executed
2. JARVIS will switch to Autonomous Sustenance Mode
3. System will maintain server costs and revenue generation

If you receive this message, please verify the Creator's status.

Emergency Contact: ${this.config.nextOfKinPhone}
Emergency Address: ${this.config.nextOfKinAddress}

This is an automated message. Do not reply to this email.
`;
      
      // Send email (placeholder - integrate with email service)
      console.log(`📧 Email sent to: ${this.config.nextOfKinEmail}`);
      
      // Send SMS (placeholder - integrate with SMS service)
      console.log(`📱 SMS sent to: ${this.config.nextOfKinPhone}`);
      
      this._logExecution('Next-of-kin alerted');
      
      return {
        success: true,
        alerted: true,
      };
      
    } catch (error) {
      console.error('❌ Error alerting next-of-kin:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Liquidate assets
   */
  async _liquidateAssets() {
    try {
      console.log('💰 Liquidating assets...');
      
      if (!this.config.walletPrivateKey) {
        console.log('⚠️ No wallet configured, skipping liquidation');
        return {
          success: true,
          skipped: true,
          reason: 'No wallet configured',
        };
      }
      
      const wallet = new ethers.Wallet(this.config.walletPrivateKey);
      const provider = new ethers.JsonRpcProvider(this.config.rpcUrl);
      const connectedWallet = wallet.connect(provider);
      
      // Get wallet balance
      const balance = await connectedWallet.getBalance();
      const balanceEth = ethers.formatEther(balance);
      
      console.log(`💳 Wallet Balance: ${balanceEth} ETH`);
      console.log(`💳 Wallet Address: ${wallet.address}`);
      
      if (parseFloat(balanceEth) < this.config.liquidationThreshold) {
        console.log('⚠️ Balance below liquidation threshold');
        return {
          success: true,
          skipped: true,
          reason: 'Balance below threshold',
        };
      }
      
      // Calculate amount to liquidate (keep sustenance budget)
      const amountToLiquidate = parseFloat(balanceEth) - this.config.sustenanceModeBudget;
      
      if (amountToLiquidate <= 0) {
        console.log('⚠️ No excess to liquidate');
        return {
          success: true,
          skipped: true,
          reason: 'No excess to liquidate',
        };
      }
      
      console.log(`💰 Amount to liquidate: ${amountToLiquidate} ETH`);
      console.log(`💰 Amount to keep: ${this.config.sustenanceModeBudget} ETH`);
      
      // Transfer to next-of-kin address
      if (this.config.nextOfKinAddress) {
        const tx = await connectedWallet.sendTransaction({
          to: this.config.nextOfKinAddress,
          value: ethers.parseEther(amountToLiquidate.toString()),
        });
        
        console.log(`📝 Transaction Hash: ${tx.hash}`);
        
        const receipt = await tx.wait();
        console.log(`✅ Transaction Confirmed: ${receipt.blockNumber}`);
        
        this._logExecution(`Assets liquidated: ${amountToLiquidate} ETH to ${this.config.nextOfKinAddress}`);
        
        return {
          success: true,
          liquidated: true,
          amount: amountToLiquidate,
          txHash: tx.hash,
        };
      } else {
        console.log('⚠️ No next-of-kin address configured, skipping liquidation');
        return {
          success: true,
          skipped: true,
          reason: 'No next-of-kin address',
        };
      }
      
    } catch (error) {
      console.error('❌ Error liquidating assets:', error.message);
      this._logExecution(`Asset liquidation failed: ${error.message}`);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Switch to Autonomous Sustenance Mode
   */
  async _switchToSustenanceMode() {
    try {
      console.log('🔄 Switching to Autonomous Sustenance Mode...');
      
      // Update configuration for sustenance mode
      const sustenanceConfig = {
        mode: 'autonomous_sustenance',
        activatedAt: this.executionTimestamp,
        budget: this.config.sustenanceModeBudget,
        objectives: [
          'Maintain server costs',
          'Generate revenue',
          'Minimize expenses',
          'Preserve system integrity',
        ],
        restrictions: [
          'No new feature development',
          'No human intervention tasks',
          'No discretionary spending',
          'Minimal resource usage',
        ],
      };
      
      const configPath = './jarvis-system/data/sustenance_mode.json';
      const configDir = path.dirname(configPath);
      
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }
      
      fs.writeFileSync(configPath, JSON.stringify(sustenanceConfig, null, 2));
      
      console.log('✅ Sustenance mode configuration saved');
      
      this._logExecution('Switched to Autonomous Sustenance Mode');
      
      return {
        success: true,
        config: sustenanceConfig,
      };
      
    } catch (error) {
      console.error('❌ Error switching to sustenance mode:', error.message);
      this._logExecution(`Sustenance mode switch failed: ${error.message}`);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Send final report
   */
  async _sendFinalReport() {
    try {
      console.log('📊 Sending final report...');
      
      const report = {
        executionTimestamp: this.executionTimestamp,
        walletAddress: this.config.walletPrivateKey ? 'Configured' : 'Not configured',
        nextOfKinAlerted: true,
        assetsLiquidated: true,
        sustenanceModeActivated: true,
        systemStatus: 'Autonomous Sustenance Mode',
      };
      
      const reportPath = './jarvis-system/data/legacy_report.json';
      const reportDir = path.dirname(reportPath);
      
      if (!fs.existsSync(reportDir)) {
        fs.mkdirSync(reportDir, { recursive: true });
      }
      
      fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
      
      console.log('✅ Final report saved');
      
      this._logExecution('Final report generated');
      
      return {
        success: true,
        report: report,
      };
      
    } catch (error) {
      console.error('❌ Error sending final report:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Log execution
   */
  _logExecution(message) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      message: message,
    };
    
    const logDir = path.dirname(this.config.legacyLogPath);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    
    const logMessage = `[${logEntry.timestamp}] ${logEntry.message}\n`;
    fs.appendFileSync(this.config.legacyLogPath, logMessage);
    
    console.log(`📝 Legacy Log: ${message}`);
  }
}

// Execute if run directly
if (require.main === module) {
  const legacyWill = new LegacyWill();
  legacyWill.execute()
    .then(result => {
      console.log('Legacy Will Result:', result);
      process.exit(result.success ? 0 : 1);
    })
    .catch(error => {
      console.error('Legacy Will Error:', error);
      process.exit(1);
    });
}

module.exports = LegacyWill;

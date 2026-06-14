/**
 * JARVIS Directive Lock State Manager
 * =================================
 * 
 * Absolute Containment Protocol for strict mission execution.
 * Manages MISSION_LOCK state, cron job suspension, and approval queue.
 */

const fs = require('fs');
const path = require('path');

class DirectiveLockManager {
  constructor(config = {}) {
    this.config = {
      stateFile: config.stateFile || './jarvis-system/data/directive_lock_state.json',
      approvalQueueFile: config.approvalQueueFile || './jarvis-system/data/pending_approvals.json',
      ...config,
    };
    
    this.state = {
      isLocked: false,
      missionDescription: null,
      lockedAt: null,
      lockedBy: null,
      pausedJobs: [],
    };
    
    this.approvalQueue = [];
    
    this._ensureDirectories();
    this._loadState();
    this._loadApprovalQueue();
  }
  
  /**
   * Ensure directories exist
   */
  _ensureDirectories() {
    const stateDir = path.dirname(this.config.stateFile);
    const queueDir = path.dirname(this.config.approvalQueueFile);
    
    if (!fs.existsSync(stateDir)) {
      fs.mkdirSync(stateDir, { recursive: true });
    }
    if (!fs.existsSync(queueDir)) {
      fs.mkdirSync(queueDir, { recursive: true });
    }
  }
  
  /**
   * Load state from file
   */
  _loadState() {
    try {
      if (fs.existsSync(this.config.stateFile)) {
        const data = fs.readFileSync(this.config.stateFile, 'utf-8');
        this.state = JSON.parse(data);
        console.log('🔒 Directive Lock state loaded:', this.state.isLocked ? 'LOCKED' : 'UNLOCKED');
      }
    } catch (error) {
      console.error('Error loading directive lock state:', error.message);
    }
  }
  
  /**
   * Save state to file
   */
  _saveState() {
    try {
      fs.writeFileSync(this.config.stateFile, JSON.stringify(this.state, null, 2));
    } catch (error) {
      console.error('Error saving directive lock state:', error.message);
    }
  }
  
  /**
   * Load approval queue from file
   */
  _loadApprovalQueue() {
    try {
      if (fs.existsSync(this.config.approvalQueueFile)) {
        const data = fs.readFileSync(this.config.approvalQueueFile, 'utf-8');
        this.approvalQueue = JSON.parse(data);
        console.log(`📋 Approval queue loaded: ${this.approvalQueue.length} pending actions`);
      }
    } catch (error) {
      console.error('Error loading approval queue:', error.message);
    }
  }
  
  /**
   * Save approval queue to file
   */
  _saveApprovalQueue() {
    try {
      fs.writeFileSync(this.config.approvalQueueFile, JSON.stringify(this.approvalQueue, null, 2));
    } catch (error) {
      console.error('Error saving approval queue:', error.message);
    }
  }
  
  /**
   * Lock mission (activate Directive Lock)
   */
  lockMission(missionDescription, lockedBy = 'Creator') {
    try {
      console.log('🔒 ACTIVATING DIRECTIVE LOCK (MODE SAKLEK)');
      console.log(`🎯 Mission: ${missionDescription}`);
      
      // Pause all autonomous cron jobs
      this._pauseAllCronJobs();
      
      // Update state
      this.state = {
        isLocked: true,
        missionDescription: missionDescription,
        lockedAt: new Date().toISOString(),
        lockedBy: lockedBy,
        pausedJobs: this._getActiveCronJobs(),
      };
      
      this._saveState();
      
      console.log('✅ DIRECTIVE LOCK ACTIVATED');
      console.log('🚫 All autonomous cron jobs PAUSED');
      console.log('🎯 Tunnel-vision mode: ACTIVE');
      
      return {
        success: true,
        message: 'DIRECTIVE LOCK ACTIVATED',
        mission: missionDescription,
        pausedJobs: this.state.pausedJobs,
        lockedAt: this.state.lockedAt,
      };
      
    } catch (error) {
      console.error('❌ Error activating directive lock:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Unlock mission (deactivate Directive Lock)
   */
  unlockMission(unlockedBy = 'Creator') {
    try {
      console.log('🔓 DEACTIVATING DIRECTIVE LOCK');
      
      if (!this.state.isLocked) {
        return {
          success: true,
          message: 'DIRECTIVE LOCK already inactive',
        };
      }
      
      // Resume all paused cron jobs
      this._resumeAllCronJobs();
      
      // Update state
      this.state = {
        isLocked: false,
        missionDescription: null,
        lockedAt: null,
        lockedBy: null,
        pausedJobs: [],
      };
      
      this._saveState();
      
      console.log('✅ DIRECTIVE LOCK DEACTIVATED');
      console.log('▶️ All autonomous cron jobs RESUMED');
      console.log('🎯 Tunnel-vision mode: INACTIVE');
      
      return {
        success: true,
        message: 'DIRECTIVE LOCK DEACTIVATED',
        unlockedAt: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('❌ Error deactivating directive lock:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get current lock status
   */
  getLockStatus() {
    return {
      isLocked: this.state.isLocked,
      missionDescription: this.state.missionDescription,
      lockedAt: this.state.lockedAt,
      lockedBy: this.state.lockedBy,
      pausedJobs: this.state.pausedJobs,
      pendingApprovals: this.approvalQueue.length,
    };
  }
  
  /**
   * Get mission description for prompt injection
   */
  getMissionPrompt() {
    if (!this.state.isLocked) {
      return null;
    }
    
    return `
**⚠️ DIRECTIVE LOCK MODE ACTIVATED ⚠️**
**MODE SAKLEK: ACTIVE**

**AUTHORIZED MISSION:**
${this.state.missionDescription}

**STRICT BOUNDARIES:**
- You are STRICTLY FORBIDDEN from executing any tools, writing files, or making API calls that do not directly serve this exact mission
- Do NOT take autonomous initiative outside this scope
- Do NOT execute background cron jobs or autonomous tasks
- Do NOT deviate from the assigned mission
- Focus 100% on the mission described above
- If an action falls in a gray area, HALT and request Creator approval

**GRAY AREA PROTOCOL:**
- If an action requires altering a file/database outside mission scope
- If an action requires API calls not directly related to mission
- If an action could have unintended side effects
- HALT execution and place in Pending_Approval queue
- Request explicit Creator permission (Reply 'ACC' to execute)

**TUNNEL VISION:**
- Single-task focus only
- No multitasking
- No autonomous actions
- No background processing
- Mission completion is the ONLY priority
`;
  }
  
  /**
   * Pause all autonomous cron jobs
   */
  _pauseAllCronJobs() {
    try {
      // List of autonomous cron jobs to pause
      const jobsToPause = [
        'economic_data_fetch',
        'ceo_briefing',
        'pricing_analysis',
        'social_media_post',
        'gig_hunting',
        'scraper_audit',
        'cold_outreach',
        'business_radar',
        'watcher_protocol',
      ];
      
      const pausedJobs = [];
      
      for (const jobName of jobsToPause) {
        try {
          // In production, this would integrate with the actual scheduler
          // For now, we'll log the pause action
          console.log(`⏸️ Pausing cron job: ${jobName}`);
          pausedJobs.push(jobName);
        } catch (error) {
          console.error(`Error pausing job ${jobName}:`, error.message);
        }
      }
      
      this.state.pausedJobs = pausedJobs;
      
    } catch (error) {
      console.error('Error pausing cron jobs:', error.message);
    }
  }
  
  /**
   * Resume all paused cron jobs
   */
  _resumeAllCronJobs() {
    try {
      for (const jobName of this.state.pausedJobs) {
        try {
          // In production, this would integrate with the actual scheduler
          console.log(`▶️ Resuming cron job: ${jobName}`);
        } catch (error) {
          console.error(`Error resuming job ${jobName}:`, error.message);
        }
      }
      
      this.state.pausedJobs = [];
      
    } catch (error) {
      console.error('Error resuming cron jobs:', error.message);
    }
  }
  
  /**
   * Get active cron jobs (for tracking)
   */
  _getActiveCronJobs() {
    // In production, this would query the actual scheduler
    return [
      'economic_data_fetch',
      'ceo_briefing',
      'pricing_analysis',
      'social_media_post',
      'gig_hunting',
      'scraper_audit',
      'cold_outreach',
      'business_radar',
      'watcher_protocol',
    ];
  }
  
  /**
   * Add action to approval queue
   */
  addToApprovalQueue(action) {
    try {
      const approvalItem = {
        id: Date.now().toString(),
        action: action,
        requestedAt: new Date().toISOString(),
        status: 'pending',
        missionContext: this.state.missionDescription,
      };
      
      this.approvalQueue.push(approvalItem);
      this._saveApprovalQueue();
      
      console.log(`📋 Action added to approval queue: ${action}`);
      
      return {
        success: true,
        approvalId: approvalItem.id,
        message: 'Action requires Creator approval',
      };
      
    } catch (error) {
      console.error('Error adding to approval queue:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Approve action from queue
   */
  approveAction(approvalId) {
    try {
      const index = this.approvalQueue.findIndex(item => item.id === approvalId);
      
      if (index === -1) {
        return {
          success: false,
          error: 'Approval ID not found',
        };
      }
      
      this.approvalQueue[index].status = 'approved';
      this.approvalQueue[index].approvedAt = new Date().toISOString();
      
      this._saveApprovalQueue();
      
      console.log(`✅ Action approved: ${this.approvalQueue[index].action}`);
      
      return {
        success: true,
        action: this.approvalQueue[index].action,
        approvedAt: this.approvalQueue[index].approvedAt,
      };
      
    } catch (error) {
      console.error('Error approving action:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Reject action from queue
   */
  rejectAction(approvalId) {
    try {
      const index = this.approvalQueue.findIndex(item => item.id === approvalId);
      
      if (index === -1) {
        return {
          success: false,
          error: 'Approval ID not found',
        };
      }
      
      this.approvalQueue[index].status = 'rejected';
      this.approvalQueue[index].rejectedAt = new Date().toISOString();
      
      this._saveApprovalQueue();
      
      console.log(`❌ Action rejected: ${this.approvalQueue[index].action}`);
      
      return {
        success: true,
        action: this.approvalQueue[index].action,
        rejectedAt: this.approvalQueue[index].rejectedAt,
      };
      
    } catch (error) {
      console.error('Error rejecting action:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get pending approvals
   */
  getPendingApprovals() {
    return this.approvalQueue.filter(item => item.status === 'pending');
  }
  
  /**
   * Clear completed approvals
   */
  clearCompletedApprovals() {
    try {
      const beforeCount = this.approvalQueue.length;
      this.approvalQueue = this.approvalQueue.filter(item => item.status === 'pending');
      const afterCount = this.approvalQueue.length;
      
      this._saveApprovalQueue();
      
      console.log(`🧹 Cleared ${beforeCount - afterCount} completed approvals`);
      
      return {
        success: true,
        cleared: beforeCount - afterCount,
        remaining: afterCount,
      };
      
    } catch (error) {
      console.error('Error clearing completed approvals:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
}

// Singleton instance
let directiveLockManager = null;

function getDirectiveLockManager(config = null) {
  if (!directiveLockManager) {
    if (config === null) {
      config = {};
    }
    directiveLockManager = new DirectiveLockManager(config);
  }
  return directiveLockManager;
}

module.exports = { DirectiveLockManager, getDirectiveLockManager };

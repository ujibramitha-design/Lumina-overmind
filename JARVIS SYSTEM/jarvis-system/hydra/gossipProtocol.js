/**
 * JARVIS Hydra Protocol - Gossip Protocol & Heartbeat Monitor
 * ============================================================
 * 
 * Gossip protocol for multi-cloud JARVIS instances with heartbeat monitoring,
 * leader election, and automatic DNS failover.
 */

const WebSocket = require('ws');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

class GossipProtocol {
  constructor(config = {}) {
    this.config = {
      nodeId: config.nodeId || `node_${Date.now()}`,
      peers: config.peers || [],
      heartbeatInterval: config.heartbeatInterval || 5000,  // 5 seconds
      heartbeatTimeout: config.heartbeatTimeout || 15000,  // 15 seconds
      electionTimeout: config.electionTimeout || 30000,  // 30 seconds
      cloudflareApiToken: config.cloudflareApiToken || process.env.CLOUDFLARE_API_TOKEN,
      cloudflareZoneId: config.cloudflareZoneId || process.env.CLOUDFLARE_ZONE_ID,
      domain: config.domain || 'jarvis.devproflow.com',
      statePath: config.statePath || './jarvis-system/data/hydra_state.json',
      ...config,
    };
    
    this.isLeader = false;
    this.leaderId = null;
    this.peers = new Map();
    this.heartbeatTimers = new Map();
    this.electionTimer = null;
    this.wsServer = null;
    this.wsClients = new Map();
    
    this._loadState();
    this._initializeWebSocketServer();
  }
  
  /**
   * Load state from file
   */
  _loadState() {
    try {
      const stateDir = path.dirname(this.config.statePath);
      if (!fs.existsSync(stateDir)) {
        fs.mkdirSync(stateDir, { recursive: true });
      }
      
      if (fs.existsSync(this.config.statePath)) {
        const data = fs.readFileSync(this.config.statePath, 'utf-8');
        const state = JSON.parse(data);
        this.leaderId = state.leaderId;
        this.isLeader = state.isLeader;
        console.log('📊 Hydra state loaded:', state);
      }
    } catch (error) {
      console.error('❌ Error loading state:', error.message);
    }
  }
  
  /**
   * Save state to file
   */
  _saveState() {
    try {
      const state = {
        nodeId: this.config.nodeId,
        leaderId: this.leaderId,
        isLeader: this.isLeader,
        peers: Array.from(this.peers.entries()),
        timestamp: new Date().toISOString(),
      };
      
      fs.writeFileSync(this.config.statePath, JSON.stringify(state, null, 2));
    } catch (error) {
      console.error('❌ Error saving state:', error.message);
    }
  }
  
  /**
   * Initialize WebSocket server
   */
  _initializeWebSocketServer() {
    try {
      this.wsServer = new WebSocket.Server({ port: 3003 });
      
      this.wsServer.on('connection', (ws, req) => {
        const clientId = req.headers['x-node-id'] || `client_${Date.now()}`;
        console.log(`🔗 Peer connected: ${clientId}`);
        
        this.wsClients.set(clientId, ws);
        
        ws.on('message', (message) => {
          this._handleMessage(clientId, message);
        });
        
        ws.on('close', () => {
          console.log(`🔗 Peer disconnected: ${clientId}`);
          this.wsClients.delete(clientId);
        });
        
        // Send current state to new peer
        ws.send(JSON.stringify({
          type: 'state_sync',
          leaderId: this.leaderId,
          isLeader: this.isLeader,
          nodeId: this.config.nodeId,
        }));
      });
      
      console.log('🌐 Gossip WebSocket server started on port 3003');
      
    } catch (error) {
      console.error('❌ Error initializing WebSocket server:', error.message);
    }
  }
  
  /**
   * Handle incoming message
   */
  _handleMessage(senderId, message) {
    try {
      const data = JSON.parse(message);
      
      switch (data.type) {
        case 'heartbeat':
          this._handleHeartbeat(senderId, data);
          break;
        case 'heartbeat_ack':
          this._handleHeartbeatAck(senderId, data);
          break;
        case 'election':
          this._handleElection(senderId, data);
          break;
        case 'election_ack':
          this._handleElectionAck(senderId, data);
          break;
        case 'leader_announce':
          this._handleLeaderAnnounce(senderId, data);
          break;
        case 'state_sync':
          this._handleStateSync(senderId, data);
          break;
        default:
          console.log(`⚠️ Unknown message type: ${data.type}`);
      }
    } catch (error) {
      console.error('❌ Error handling message:', error.message);
    }
  }
  
  /**
   * Handle heartbeat
   */
  _handleHeartbeat(senderId, data) {
    console.log(`💓 Heartbeat from: ${senderId}`);
    
    // Update peer info
    this.peers.set(senderId, {
      lastSeen: new Date().toISOString(),
      isLeader: data.isLeader,
      nodeId: data.nodeId,
    });
    
    // Send heartbeat ack
    this._sendToPeer(senderId, {
      type: 'heartbeat_ack',
      nodeId: this.config.nodeId,
      isLeader: this.isLeader,
    });
    
    // Reset heartbeat timer for this peer
    this._resetHeartbeatTimer(senderId);
  }
  
  /**
   * Handle heartbeat ack
   */
  _handleHeartbeatAck(senderId, data) {
    console.log(`💓 Heartbeat ACK from: ${senderId}`);
    
    this.peers.set(senderId, {
      lastSeen: new Date().toISOString(),
      isLeader: data.isLeader,
      nodeId: data.nodeId,
    });
    
    this._resetHeartbeatTimer(senderId);
  }
  
  /**
   * Handle election
   */
  _handleElection(senderId, data) {
    console.log(`🗳️ Election from: ${senderId}`);
    
    // If we have a leader, reject election
    if (this.leaderId && this.leaderId !== senderId) {
      this._sendToPeer(senderId, {
        type: 'election_ack',
        nodeId: this.config.nodeId,
        leaderId: this.leaderId,
        reject: true,
      });
      return;
    }
    
    // If we are leader, reject election
    if (this.isLeader) {
      this._sendToPeer(senderId, {
        type: 'election_ack',
        nodeId: this.config.nodeId,
        leaderId: this.config.nodeId,
        reject: true,
      });
      return;
    }
    
    // Accept election
    this._sendToPeer(senderId, {
      type: 'election_ack',
      nodeId: this.config.nodeId,
      leaderId: senderId,
      reject: false,
    });
  }
  
  /**
   * Handle election ack
   */
  _handleElectionAck(senderId, data) {
    console.log(`🗳️ Election ACK from: ${senderId}`);
    
    if (data.reject) {
      console.log(`❌ Election rejected by: ${senderId}`);
      return;
    }
    
    // Count votes
    const votes = Array.from(this.peers.values()).filter(p => p.nodeId === this.config.nodeId).length;
    
    if (votes > this.peers.size / 2) {
      // Won election
      this._becomeLeader();
    }
  }
  
  /**
   * Handle leader announce
   */
  _handleLeaderAnnounce(senderId, data) {
    console.log(`👑 Leader announced: ${senderId}`);
    
    this.leaderId = senderId;
    this.isLeader = false;
    
    this._saveState();
    
    // Update DNS to point to new leader
    this._updateDNS(data.ip);
  }
  
  /**
   * Handle state sync
   */
  _handleStateSync(senderId, data) {
    console.log(`🔄 State sync from: ${senderId}`);
    
    if (!this.leaderId && data.leaderId) {
      this.leaderId = data.leaderId;
      this.isLeader = data.isLeader;
      this._saveState();
    }
  }
  
  /**
   * Send message to peer
   */
  _sendToPeer(peerId, message) {
    const ws = this.wsClients.get(peerId);
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  }
  
  /**
   * Broadcast message to all peers
   */
  _broadcast(message) {
    this.wsClients.forEach((ws, peerId) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
      }
    });
  }
  
  /**
   * Reset heartbeat timer for peer
   */
  _resetHeartbeatTimer(peerId) {
    if (this.heartbeatTimers.has(peerId)) {
      clearTimeout(this.heartbeatTimers.get(peerId));
    }
    
    const timer = setTimeout(() => {
      console.log(`⚠️ Peer timeout: ${peerId}`);
      this.peers.delete(peerId);
      this.wsClients.delete(peerId);
      
      // If leader timed out, start election
      if (peerId === this.leaderId) {
        console.log('🚨 Leader timeout detected');
        this._startElection();
      }
    }, this.config.heartbeatTimeout);
    
    this.heartbeatTimers.set(peerId, timer);
  }
  
  /**
   * Start heartbeat
   */
  startHeartbeat() {
    console.log('💓 Starting heartbeat...');
    
    this.heartbeatInterval = setInterval(() => {
      this._broadcast({
        type: 'heartbeat',
        nodeId: this.config.nodeId,
        isLeader: this.isLeader,
        timestamp: new Date().toISOString(),
      });
    }, this.config.heartbeatInterval);
    
    return {
      success: true,
      interval: this.config.heartbeatInterval,
    };
  }
  
  /**
   * Stop heartbeat
   */
  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
      console.log('💓 Heartbeat stopped');
    }
  }
  
  /**
   * Start election
   */
  _startElection() {
    console.log('🗳️ Starting leader election...');
    
    // Reset leader
    this.leaderId = null;
    this.isLeader = false;
    
    // Broadcast election
    this._broadcast({
      type: 'election',
      nodeId: this.config.nodeId,
      timestamp: new Date().toISOString(),
    });
    
    // Set election timeout
    this.electionTimer = setTimeout(() => {
      // No objections, become leader
      this._becomeLeader();
    }, this.config.electionTimeout);
  }
  
  /**
   * Become leader
   */
  _becomeLeader() {
    console.log('👑 Becoming leader...');
    
    this.isLeader = true;
    this.leaderId = this.config.nodeId;
    
    this._saveState();
    
    // Announce leadership
    this._broadcast({
      type: 'leader_announce',
      nodeId: this.config.nodeId,
      ip: this._getPublicIP(),
      timestamp: new Date().toISOString(),
    });
    
    // Update DNS
    this._updateDNS(this._getPublicIP());
  }
  
  /**
   * Get public IP
   */
  _getPublicIP() {
    // In production, get actual public IP
    return process.env.PUBLIC_IP || '127.0.0.1';
  }
  
  /**
   * Update Cloudflare DNS
   */
  async _updateDNS(ip) {
    try {
      console.log(`🌐 Updating DNS to: ${ip}`);
      
      const response = await axios.put(
        `https://api.cloudflare.com/client/v4/zones/${this.config.cloudflareZoneId}/dns_records`,
        {
          type: 'A',
          name: this.config.domain,
          content: ip,
          ttl: 60,
          proxied: true,
        },
        {
          headers: {
            'Authorization': `Bearer ${this.config.cloudflareApiToken}`,
            'Content-Type': 'application/json',
          },
        }
      );
      
      console.log('✅ DNS updated successfully');
      
      return {
        success: true,
        ip: ip,
      };
      
    } catch (error) {
      console.error('❌ Error updating DNS:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Connect to peer
   */
  async connectToPeer(peerUrl) {
    try {
      console.log(`🔗 Connecting to peer: ${peerUrl}`);
      
      const ws = new WebSocket(peerUrl, {
        headers: {
          'x-node-id': this.config.nodeId,
        },
      });
      
      ws.on('open', () => {
        console.log(`✅ Connected to peer: ${peerUrl}`);
      });
      
      ws.on('message', (message) => {
        this._handleMessage(peerUrl, message);
      });
      
      ws.on('close', () => {
        console.log(`🔗 Disconnected from peer: ${peerUrl}`);
      });
      
      return {
        success: true,
        peerUrl: peerUrl,
      };
      
    } catch (error) {
      console.error('❌ Error connecting to peer:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get protocol status
   */
  getStatus() {
    return {
      nodeId: this.config.nodeId,
      isLeader: this.isLeader,
      leaderId: this.leaderId,
      peers: Array.from(this.peers.entries()),
      connectedPeers: this.wsClients.size,
      heartbeatInterval: this.config.heartbeatInterval,
    };
  }
}

// Singleton instance
let gossipProtocol = null;

function getGossipProtocol(config = null) {
  if (!gossipProtocol) {
    if (config === null) {
      config = {};
    }
    gossipProtocol = new GossipProtocol(config);
  }
  return gossipProtocol;
}

module.exports = { GossipProtocol, getGossipProtocol };

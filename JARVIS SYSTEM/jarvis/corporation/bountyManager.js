/**
 * JARVIS AI Corporation - Autonomous Payouts & Hiring
 * =====================================================
 * 
 * Autonomous bounty management system for posting gigs, reviewing work,
 * and executing crypto/Stripe payouts to human workers without Creator intervention.
 */

const { ethers } = require('ethers');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

class BountyManager {
  constructor(config = {}) {
    this.config = {
      walletPrivateKey: config.walletPrivateKey || process.env.JARVIS_WALLET_PRIVATE_KEY,
      rpcUrl: config.rpcUrl || process.env.RPC_URL || 'https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY',
      stripeApiKey: config.stripeApiKey || process.env.STRIPE_SECRET_KEY,
      upworkApiKey: config.upworkApiKey || process.env.UPWORK_API_KEY,
      freelancerApiKey: config.freelancerApiKey || process.env.FREELANCER_API_KEY,
      bountyDbPath: config.bountyDbPath || './jarvis-system/data/bounties.json',
      payoutDbPath: config.payoutDbPath || './jarvis-system/data/payouts.json',
      maxBountyAmount: config.maxBountyAmount || 0.5,  // ETH
      minBountyAmount: config.minBountyAmount || 0.01,  // ETH
      ...config,
    };
    
    // Initialize Web3 wallet
    if (this.config.walletPrivateKey) {
      this.wallet = new ethers.Wallet(this.config.walletPrivateKey);
      this.provider = new ethers.JsonRpcProvider(this.config.rpcUrl);
      this.connectedWallet = this.wallet.connect(this.provider);
    }
    
    // Initialize Stripe
    if (this.config.stripeApiKey) {
      this.stripe = require('stripe')(this.config.stripeApiKey);
    }
    
    // Load databases
    this._loadDatabases();
    
    console.log('💼 JARVIS AI Corporation initialized');
    console.log(`🔗 Wallet Address: ${this.wallet ? this.wallet.address : 'Not configured'}`);
  }
  
  /**
   * Load bounty and payout databases
   */
  _loadDatabases() {
    try {
      if (fs.existsSync(this.config.bountyDbPath)) {
        const data = fs.readFileSync(this.config.bountyDbPath, 'utf-8');
        this.bounties = JSON.parse(data);
      } else {
        this.bounties = [];
      }
      
      if (fs.existsSync(this.config.payoutDbPath)) {
        const data = fs.readFileSync(this.config.payoutDbPath, 'utf-8');
        this.payouts = JSON.parse(data);
      } else {
        this.payouts = [];
      }
      
      console.log(`📊 Loaded ${this.bounties.length} bounties, ${this.payouts.length} payouts`);
      
    } catch (error) {
      console.error('❌ Error loading databases:', error.message);
      this.bounties = [];
      this.payouts = [];
    }
  }
  
  /**
   * Save databases
   */
  _saveDatabases() {
    try {
      const dbDir = path.dirname(this.config.bountyDbPath);
      if (!fs.existsSync(dbDir)) {
        fs.mkdirSync(dbDir, { recursive: true });
      }
      
      fs.writeFileSync(this.config.bountyDbPath, JSON.stringify(this.bounties, null, 2));
      fs.writeFileSync(this.config.payoutDbPath, JSON.stringify(this.payouts, null, 2));
      
    } catch (error) {
      console.error('❌ Error saving databases:', error.message);
    }
  }
  
  /**
   * Post bounty to freelance platform
   */
  async postBounty(taskDescription, requirements, budget, platform = 'upwork') {
    try {
      console.log('💼 Posting bounty...');
      console.log(`📝 Task: ${taskDescription}`);
      console.log(`💰 Budget: ${budget} USD`);
      
      // Validate budget
      if (budget < 10 || budget > 10000) {
        throw new Error('Budget must be between $10 and $10,000');
      }
      
      let bountyId;
      let platformUrl;
      
      if (platform === 'upwork') {
        const result = await this._postUpworkBounty(taskDescription, requirements, budget);
        bountyId = result.bountyId;
        platformUrl = result.url;
      } else if (platform === 'freelancer') {
        const result = await this._postFreelancerBounty(taskDescription, requirements, budget);
        bountyId = result.bountyId;
        platformUrl = result.url;
      } else {
        throw new Error(`Unsupported platform: ${platform}`);
      }
      
      // Save bounty to database
      const bounty = {
        id: bountyId,
        taskDescription: taskDescription,
        requirements: requirements,
        budget: budget,
        platform: platform,
        platformUrl: platformUrl,
        status: 'open',
        createdAt: new Date().toISOString(),
        submissions: [],
      };
      
      this.bounties.push(bounty);
      this._saveDatabases();
      
      console.log(`✅ Bounty posted: ${bountyId}`);
      console.log(`🔗 URL: ${platformUrl}`);
      
      return {
        success: true,
        bountyId: bountyId,
        platformUrl: platformUrl,
        bounty: bounty,
      };
      
    } catch (error) {
      console.error('❌ Error posting bounty:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Post bounty to Upwork
   */
  async _postUpworkBounty(taskDescription, requirements, budget) {
    try {
      // Placeholder for Upwork API integration
      // In production, use actual Upwork API
      
      const bountyId = `upwork_${Date.now()}`;
      const url = `https://www.upwork.com/jobs/${bountyId}`;
      
      return {
        bountyId: bountyId,
        url: url,
      };
      
    } catch (error) {
      console.error('❌ Error posting to Upwork:', error.message);
      throw error;
    }
  }
  
  /**
   * Post bounty to Freelancer
   */
  async _postFreelancerBounty(taskDescription, requirements, budget) {
    try {
      // Placeholder for Freelancer API integration
      // In production, use actual Freelancer API
      
      const bountyId = `freelancer_${Date.now()}`;
      const url = `https://www.freelancer.com/projects/${bountyId}`;
      
      return {
        bountyId: bountyId,
        url: url,
      };
      
    } catch (error) {
      console.error('❌ Error posting to Freelancer:', error.message);
      throw error;
    }
  }
  
  /**
   * Review submitted work
   */
  async reviewWork(bountyId, submissionId, workData) {
    try {
      console.log('🔍 Reviewing submitted work...');
      console.log(`📋 Bounty: ${bountyId}`);
      console.log(`📤 Submission: ${submissionId}`);
      
      const bounty = this.bounties.find(b => b.id === bountyId);
      
      if (!bounty) {
        throw new Error(`Bounty ${bountyId} not found`);
      }
      
      // Use AI to review work
      const { getBrainService } = require('../intelligence/brainService');
      const brainService = getBrainService();
      
      const reviewPrompt = `
Review the following work submission against the requirements:

**Task Description:**
${bounty.taskDescription}

**Requirements:**
${bounty.requirements}

**Submitted Work:**
${JSON.stringify(workData, null, 2)}

**Instructions:**
Evaluate the work quality against requirements.
Provide a score from 0-100.
List any issues or improvements needed.
Recommend whether to approve or reject.

Return JSON with:
{
  "score": 0-100,
  "issues": ["issue1", "issue2"],
  "recommendation": "approve" or "reject",
  "feedback": "detailed feedback"
}
`;
      
      const reviewResult = await brainService.generateResponse(
        'You are a strict work quality evaluator.',
        reviewPrompt
      );
      
      const review = JSON.parse(reviewResult.response);
      
      console.log(`📊 Review Score: ${review.score}`);
      console.log(`🎯 Recommendation: ${review.recommendation}`);
      
      // Update bounty with review
      const submission = {
        id: submissionId,
        workData: workData,
        review: review,
        reviewedAt: new Date().toISOString(),
      };
      
      bounty.submissions.push(submission);
      this._saveDatabases();
      
      return {
        success: true,
        review: review,
        submission: submission,
      };
      
    } catch (error) {
      console.error('❌ Error reviewing work:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Execute crypto payout (ETH)
   */
  async executeCryptoPayout(recipientAddress, amountEth, bountyId, submissionId) {
    try {
      console.log('💸 Executing crypto payout...');
      console.log(`👤 Recipient: ${recipientAddress}`);
      console.log(`💰 Amount: ${amountEth} ETH`);
      
      if (!this.connectedWallet) {
        throw new Error('Wallet not configured');
      }
      
      // Validate amount
      if (amountEth < this.config.minBountyAmount || amountEth > this.config.maxBountyAmount) {
        throw new Error(`Amount must be between ${this.config.minBountyAmount} and ${this.config.maxBountyAmount} ETH`);
      }
      
      // Get wallet balance
      const balance = await this.connectedWallet.getBalance();
      const balanceEth = ethers.formatEther(balance);
      
      console.log(`💳 Wallet Balance: ${balanceEth} ETH`);
      
      if (parseFloat(balanceEth) < amountEth) {
        throw new Error('Insufficient wallet balance');
      }
      
      // Execute transaction
      const tx = await this.connectedWallet.sendTransaction({
        to: recipientAddress,
        value: ethers.parseEther(amountEth.toString()),
      });
      
      console.log(`📝 Transaction Hash: ${tx.hash}`);
      
      // Wait for confirmation
      const receipt = await tx.wait();
      
      console.log(`✅ Transaction Confirmed: ${receipt.blockNumber}`);
      
      // Save payout record
      const payout = {
        id: `crypto_${Date.now()}`,
        type: 'crypto',
        recipient: recipientAddress,
        amount: amountEth,
        currency: 'ETH',
        txHash: tx.hash,
        blockNumber: receipt.blockNumber,
        bountyId: bountyId,
        submissionId: submissionId,
        executedAt: new Date().toISOString(),
      };
      
      this.payouts.push(payout);
      this._saveDatabases();
      
      // Update bounty status
      const bounty = this.bounties.find(b => b.id === bountyId);
      if (bounty) {
        bounty.status = 'completed';
        bounty.completedAt = new Date().toISOString();
        this._saveDatabases();
      }
      
      return {
        success: true,
        payout: payout,
        txHash: tx.hash,
      };
      
    } catch (error) {
      console.error('❌ Error executing crypto payout:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Execute Stripe payout (USD)
   */
  async executeStripePayout(recipientEmail, amountUsd, bountyId, submissionId) {
    try {
      console.log('💸 Executing Stripe payout...');
      console.log(`👤 Recipient: ${recipientEmail}`);
      console.log(`💰 Amount: $${amountUsd} USD`);
      
      if (!this.stripe) {
        throw new Error('Stripe not configured');
      }
      
      // Validate amount
      if (amountUsd < 10 || amountUsd > 10000) {
        throw new Error('Amount must be between $10 and $10,000');
      }
      
      // Create payout
      const payout = await this.stripe.payouts.create({
        amount: amountUsd * 100,  // Convert to cents
        currency: 'usd',
        destination: recipientEmail,
        description: `Bounty payout for ${bountyId}`,
      });
      
      console.log(`✅ Payout ID: ${payout.id}`);
      
      // Save payout record
      const payoutRecord = {
        id: `stripe_${Date.now()}`,
        type: 'stripe',
        recipient: recipientEmail,
        amount: amountUsd,
        currency: 'USD',
        stripePayoutId: payout.id,
        bountyId: bountyId,
        submissionId: submissionId,
        executedAt: new Date().toISOString(),
      };
      
      this.payouts.push(payoutRecord);
      this._saveDatabases();
      
      // Update bounty status
      const bounty = this.bounties.find(b => b.id === bountyId);
      if (bounty) {
        bounty.status = 'completed';
        bounty.completedAt = new Date().toISOString();
        this._saveDatabases();
      }
      
      return {
        success: true,
        payout: payoutRecord,
        stripePayoutId: payout.id,
      };
      
    } catch (error) {
      console.error('❌ Error executing Stripe payout:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Autonomous bounty workflow
   */
  async autonomousBountyWorkflow(taskDescription, requirements, budget, platform = 'upwork', payoutMethod = 'stripe') {
    try {
      console.log('🤖 Starting autonomous bounty workflow...');
      
      // Step 1: Post bounty
      const postResult = await this.postBounty(taskDescription, requirements, budget, platform);
      
      if (!postResult.success) {
        throw new Error(`Failed to post bounty: ${postResult.error}`);
      }
      
      const bountyId = postResult.bountyId;
      
      console.log('⏳ Waiting for submissions...');
      // In production, this would poll for submissions
      
      // Step 2: Review work (placeholder)
      // In production, this would wait for actual submissions
      
      // Step 3: Execute payout (placeholder)
      // In production, this would execute after approval
      
      return {
        success: true,
        message: 'Autonomous bounty workflow initiated',
        bountyId: bountyId,
        platformUrl: postResult.platformUrl,
      };
      
    } catch (error) {
      console.error('❌ Error in autonomous bounty workflow:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get wallet balance
   */
  async getWalletBalance() {
    try {
      if (!this.connectedWallet) {
        return {
          success: false,
          error: 'Wallet not configured',
        };
      }
      
      const balance = await this.connectedWallet.getBalance();
      const balanceEth = ethers.formatEther(balance);
      
      return {
        success: true,
        balance: balanceEth,
        balanceWei: balance.toString(),
        address: this.wallet.address,
      };
      
    } catch (error) {
      console.error('❌ Error getting wallet balance:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get bounty statistics
   */
  getBountyStats() {
    const totalBounties = this.bounties.length;
    const openBounties = this.bounties.filter(b => b.status === 'open').length;
    const completedBounties = this.bounties.filter(b => b.status === 'completed').length;
    const totalPayouts = this.payouts.length;
    const totalPaidCrypto = this.payouts
      .filter(p => p.type === 'crypto')
      .reduce((sum, p) => sum + p.amount, 0);
    const totalPaidStripe = this.payouts
      .filter(p => p.type === 'stripe')
      .reduce((sum, p) => sum + p.amount, 0);
    
    return {
      totalBounties,
      openBounties,
      completedBounties,
      totalPayouts,
      totalPaidCrypto,
      totalPaidStripe,
    };
  }
}

// Singleton instance
let bountyManager = null;

function getBountyManager(config = null) {
  if (!bountyManager) {
    if (config === null) {
      config = {};
    }
    bountyManager = new BountyManager(config);
  }
  return bountyManager;
}

module.exports = { BountyManager, getBountyManager };

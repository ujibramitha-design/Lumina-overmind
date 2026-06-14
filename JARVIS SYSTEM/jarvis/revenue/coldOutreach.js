/**
 * JARVIS Cold Outreach Module (The Closer Pipeline)
 * ==================================================
 * 
 * Email automation module for personalized cold outreach.
 * Handles lead processing, email drafting, and sequential sending with human-like delays.
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class ColdOutreachModule {
  constructor(config = {}) {
    this.config = {
      smtp: {
        host: config.smtpHost || process.env.SMTP_HOST,
        port: config.smtpPort || 587,
        secure: config.smtpSecure === true,
        user: config.smtpUser || process.env.SMTP_USER,
        password: config.smtpPassword || process.env.SMTP_PASSWORD,
      },
      sender: {
        name: config.senderName || 'Your Name',
        email: config.senderEmail || process.env.SENDER_EMAIL,
      },
      timing: {
        minDelay: config.minDelay || 300000,  // 5 minutes
        maxDelay: config.maxDelay || 900000,  // 15 minutes
        batchSize: config.batchSize || 10,
        dailyLimit: config.dailyLimit || 50,
      },
      personalization: {
        enabled: config.personalizationEnabled !== false,
        useAIDA: config.useAIDA !== false,
        usePAS: config.usePAS !== false,
      },
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.emailGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getEmailGeneratorPrompt(),
    });
    
    this.transporter = null;
    this.sentCount = 0;
    this.lastResetDate = new Date().toDateString();
    
    this._initializeSMTP();
  }
  
  /**
   * Email generator system prompt
   */
  _getEmailGeneratorPrompt() {
    return `You are an elite cold email copywriter specializing in high-conversion outreach.

**Your Role:**
- Write personalized cold emails that convert
- Apply psychological frameworks (AIDA, PAS)
- Create compelling subject lines
- Build rapport and trust
- Focus on value propositions
- Include clear call-to-actions

**AIDA Framework:**
- Attention: Hook the reader immediately
- Interest: Build curiosity and engagement
- Desire: Create want and need
- Action: Clear call-to-action

**PAS Framework:**
- Problem: Identify the pain point
- Agitation: Make the problem feel urgent
- Solution: Present your solution

**Email Structure:**
1. Compelling subject line (under 50 characters)
2. Personalized opening
3. Value proposition
4. Social proof (if available)
5. Clear call-to-action
6. Professional signature

**Guidelines:**
- Keep emails under 200 words
- Use power words and emotional triggers
- Avoid spam triggers (all caps, excessive exclamation)
- Personalize based on lead data
- Be authentic and genuine
- Focus on benefits, not features

**Output Format:**
Return JSON with:
- subject: email subject line
- body: email body
- confidence: conversion confidence (0-1)`;
  }
  
  /**
   * Initialize SMTP transporter
   */
  _initializeSMTP() {
    try {
      this.transporter = nodemailer.createTransport({
        host: this.config.smtp.host,
        port: this.config.smtp.port,
        secure: this.config.smtp.secure,
        auth: {
          user: this.config.smtp.user,
          pass: this.config.smtp.password,
        },
      });
      
      console.log('✅ SMTP transporter initialized');
    } catch (error) {
      console.error('❌ Error initializing SMTP:', error.message);
    }
  }
  
  /**
   * Generate personalized email
   */
  async generateEmail(lead, context = {}) {
    try {
      console.log(`📝 Generating email for: ${lead.email}`);
      
      const prompt = `
**Lead Data:**
${JSON.stringify(lead, null, 2)}

**Context:**
${JSON.stringify(context, null, 2)}

**Instructions:**
Generate a personalized cold email using the ${this.config.personalization.useAIDA ? 'AIDA' : 'PAS'} framework.
- Personalize based on lead's company, role, and interests
- Reference specific details from their profile
- Focus on value proposition
- Include clear call-to-action
- Keep under 200 words

Return as JSON with subject and body.`;
      
      const result = await this.emailGenerator.generateContent(prompt);
      const email = JSON.parse(result.response.text());
      
      return {
        success: true,
        subject: email.subject,
        body: email.body,
        confidence: email.confidence || 0.7,
      };
      
    } catch (error) {
      console.error('❌ Error generating email:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Send email
   */
  async sendEmail(to, subject, body) {
    try {
      // Check daily limit
      if (this.lastResetDate !== new Date().toDateString()) {
        this.sentCount = 0;
        this.lastResetDate = new Date().toDateString();
      }
      
      if (this.sentCount >= this.config.timing.dailyLimit) {
        console.log('⚠️ Daily email limit reached');
        return {
          success: false,
          error: 'Daily limit reached',
        };
      }
      
      const mailOptions = {
        from: `"${this.config.sender.name}" <${this.config.sender.email}>`,
        to: to,
        subject: subject,
        text: body,
      };
      
      const info = await this.transporter.sendMail(mailOptions);
      this.sentCount++;
      
      console.log(`📧 Email sent to ${to}: ${info.messageId}`);
      
      return {
        success: true,
        messageId: info.messageId,
      };
      
    } catch (error) {
      console.error('❌ Error sending email:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Human-like delay
   */
  async humanDelay() {
    const minDelay = this.config.timing.minDelay;
    const maxDelay = this.config.timing.maxDelay;
    const delay = Math.random() * (maxDelay - minDelay) + minDelay;
    
    console.log(`⏳ Waiting ${Math.round(delay / 1000)} seconds before next email...`);
    
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  /**
   * Process leads sequentially
   */
  async processLeads(leads, context = {}) {
    try {
      console.log(`🚀 Processing ${leads.length} leads...`);
      
      const results = [];
      const batchSize = this.config.timing.batchSize;
      
      for (let i = 0; i < leads.length; i += batchSize) {
        const batch = leads.slice(i, i + batchSize);
        
        console.log(`\n📦 Processing batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(leads.length / batchSize)}`);
        
        for (const lead of batch) {
          // Generate personalized email
          const emailResult = await this.generateEmail(lead, context);
          
          if (!emailResult.success) {
            results.push({
              lead: lead.email,
              success: false,
              error: emailResult.error,
            });
            continue;
          }
          
          // Send email
          const sendResult = await this.sendEmail(
            lead.email,
            emailResult.subject,
            emailResult.body
          );
          
          results.push({
            lead: lead.email,
            success: sendResult.success,
            messageId: sendResult.messageId,
            confidence: emailResult.confidence,
          });
          
          // Human-like delay between emails
          if (batch.indexOf(lead) < batch.length - 1) {
            await this.humanDelay();
          }
        }
        
        // Longer delay between batches
        if (i + batchSize < leads.length) {
          console.log(`\n⏸️ Pausing between batches...`);
          await this.humanDelay();
        }
      }
      
      const successCount = results.filter(r => r.success).length;
      
      console.log(`\n✅ Outreach complete: ${successCount}/${leads.length} emails sent`);
      
      return {
        success: true,
        total: leads.length,
        sent: successCount,
        failed: leads.length - successCount,
        results: results,
      };
      
    } catch (error) {
      console.error('❌ Error processing leads:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Load leads from file
   */
  loadLeads(filepath) {
    try {
      const data = fs.readFileSync(filepath, 'utf-8');
      const leads = JSON.parse(data);
      
      console.log(`📂 Loaded ${leads.length} leads from ${filepath}`);
      
      return leads;
    } catch (error) {
      console.error('❌ Error loading leads:', error.message);
      return [];
    }
  }
  
  /**
   * Save results to file
   */
  saveResults(results, filename) {
    try {
      const dir = './jarvis/revenue/outreach_results';
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      const filepath = path.join(dir, filename);
      fs.writeFileSync(filepath, JSON.stringify(results, null, 2));
      
      console.log(`💾 Results saved to ${filepath}`);
      
      return filepath;
    } catch (error) {
      console.error('❌ Error saving results:', error.message);
      return null;
    }
  }
  
  /**
   * Get outreach statistics
   */
  getStats() {
    return {
      sentCount: this.sentCount,
      dailyLimit: this.config.timing.dailyLimit,
      lastResetDate: this.lastResetDate,
      remaining: this.config.timing.dailyLimit - this.sentCount,
    };
  }
  
  /**
   * Reset daily counter
   */
  resetDailyCounter() {
    this.sentCount = 0;
    this.lastResetDate = new Date().toDateString();
    console.log('🔄 Daily counter reset');
  }
}

// Singleton instance
let coldOutreachModule = null;

function getColdOutreachModule(config = null) {
  if (!coldOutreachModule) {
    if (config === null) {
      config = {};
    }
    coldOutreachModule = new ColdOutreachModule(config);
  }
  return coldOutreachModule;
}

module.exports = { ColdOutreachModule, getColdOutreachModule };

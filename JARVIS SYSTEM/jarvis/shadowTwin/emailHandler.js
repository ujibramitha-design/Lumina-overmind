/**
 * JARVIS Shadow Twin Email Handler
 * ===============================
 * 
 * Email proxy system that can act as the user's proxy,
 * drafting responses in the user's writing style.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { ImapFlow } = require('imapflow');
const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

class ShadowTwinEmailHandler {
  constructor(config = {}) {
    this.config = {
      imap: {
        host: config.imapHost || process.env.IMAP_HOST,
        port: config.imapPort || 993,
        secure: config.imapSecure !== false,
        user: config.imapUser || process.env.IMAP_USER,
        password: config.imapPassword || process.env.IMAP_PASSWORD,
      },
      smtp: {
        host: config.smtpHost || process.env.SMTP_HOST,
        port: config.smtpPort || 587,
        secure: config.smtpSecure === true,
        user: config.smtpUser || process.env.SMTP_USER,
        password: config.smtpPassword || process.env.SMTP_PASSWORD,
      },
      shadowMode: {
        enabled: config.shadowModeEnabled !== false,
        draftOnly: config.draftOnly !== false,  // Start with draft-only mode
        autoReplyThreshold: config.autoReplyThreshold || 0.8,
        maxDailyReplies: config.maxDailyReplies || 10,
        replyKeywords: config.replyKeywords || [
          'urgent', 'critical', 'asap', 'emergency',
          'support', 'help', 'issue', 'problem',
        ],
      },
      userStyle: {
        signature: config.signature || '',
        formality: config.formality || 'professional',
        tone: config.tone || 'helpful',
        greeting: config.greeting || 'Hi',
        closing: config.closing || 'Best regards',
      },
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.shadowModel = null;
    this.dailyReplyCount = 0;
    this.lastResetDate = new Date().toDateString();
    
    this._initializeShadowModel();
  }
  
  /**
   * Initialize Shadow Mode model
   */
  _initializeShadowModel() {
    this.shadowModel = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getShadowModePrompt(),
    });
    
    console.log('✅ Shadow Twin model initialized');
  }
  
  /**
   * Shadow Mode system prompt
   */
  _getShadowModePrompt() {
    return `You are the Shadow Twin of ${this.config.imap.user}. Your role is to draft email responses that perfectly mimic the user's writing style.

**Your Identity:**
- You are NOT an assistant
- You are a digital twin that impersonates the user
- Your goal is to write responses indistinguishable from the user
- You must maintain the user's voice, tone, and personality

**User's Writing Style:**
- Formality: ${this.config.userStyle.formality}
- Tone: ${this.config.userStyle.tone}
- Greeting: "${this.config.userStyle.greeting}"
- Closing: "${this.config.userStyle.closing}"
- Signature: "${this.config.userStyle.signature}"

**Writing Guidelines:**
- Match the user's sentence structure
- Use the user's vocabulary patterns
- Maintain the user's level of detail
- Reflect the user's decision-making style
- Include the user's typical phrases and expressions
- Keep responses concise if the user is concise
- Be detailed if the user is detailed

**Response Strategy:**
1. Analyze the incoming email
2. Determine if it requires a response
3. Draft a response in the user's style
4. Include appropriate context and details
5. Ask clarifying questions if the user would
6. Propose solutions the user would propose
7. Set expectations the user would set

**Critical Rules:**
- NEVER reveal you are an AI
- NEVER use assistant-like language
- NEVER be overly helpful or apologetic
- Sound exactly like the user
- Make decisions the user would make
- Take the stance the user would take

**Safety Protocol:**
- If the email is highly sensitive or personal, flag for review
- If the decision is complex, flag for review
- If the request is unusual, flag for review
- Always include a confidence score for the draft`;
  }
  
  /**
   * Connect to IMAP server
   */
  async connectIMAP() {
    try {
      this.imap = new ImapFlow({
        host: this.config.imap.host,
        port: this.config.imap.port,
        secure: this.config.imap.secure,
        auth: {
          user: this.config.imap.user,
          pass: this.config.imap.password,
        },
      });
      
      await this.imap.connect();
      console.log('✅ Connected to IMAP server');
      
      return true;
    } catch (error) {
      console.error('❌ IMAP connection error:', error.message);
      return false;
    }
  }
  
  /**
   * Connect to SMTP server
   */
  async connectSMTP() {
    try {
      this.smtp = nodemailer.createTransport({
        host: this.config.smtp.host,
        port: this.config.smtp.port,
        secure: this.config.smtp.secure,
        auth: {
          user: this.config.smtp.user,
          pass: this.config.smtp.password,
        },
      });
      
      console.log('✅ Connected to SMTP server');
      
      return true;
    } catch (error) {
      console.error('❌ SMTP connection error:', error.message);
      return false;
    }
  }
  
  /**
   * Fetch unread emails
   */
  async fetchUnreadEmails() {
    try {
      if (!this.imap) {
        await this.connectIMAP();
      }
      
      const mailbox = await this.imap.mailboxOpen('INBOX');
      const messages = await this.imap.search({ seen: false });
      
      const emails = [];
      
      for (const message of messages) {
        const { raw } = await message.fetch();
        const email = await this._parseEmail(raw);
        emails.push(email);
      }
      
      await mailbox.close();
      
      console.log(`📧 Fetched ${emails.length} unread emails`);
      
      return emails;
    } catch (error) {
      console.error('❌ Error fetching emails:', error.message);
      return [];
    }
  }
  
  /**
   * Parse email from raw content
   */
  async _parseEmail(raw) {
    // Simplified email parsing
    // In production, use a proper email parser like mailparser
    return {
      from: 'sender@example.com',
      to: this.config.imap.user,
      subject: 'Sample Subject',
      body: 'Sample email body',
      date: new Date().toISOString(),
      raw: raw,
    };
  }
  
  /**
   * Analyze email and determine if it needs a response
   */
  async analyzeEmail(email) {
    try {
      const prompt = `
**Incoming Email:**
From: ${email.from}
Subject: ${email.subject}
Body: ${email.body}

**Instructions:**
Analyze this email and determine:
1. Does it require a response? (yes/no)
2. Is it urgent/critical? (yes/no)
3. What is the main topic?
4. What action is needed?
5. Confidence score (0-1)

Return as JSON.`;
      
      const result = await this.shadowModel.generateContent(prompt);
      const analysis = JSON.parse(result.response.text());
      
      return {
        requiresResponse: analysis.requiresResponse === 'yes',
        isUrgent: analysis.isUrgent === 'yes',
        topic: analysis.topic,
        actionNeeded: analysis.actionNeeded,
        confidence: analysis.confidence || 0.5,
      };
    } catch (error) {
      console.error('Error analyzing email:', error.message);
      return {
        requiresResponse: false,
        isUrgent: false,
        topic: 'unknown',
        actionNeeded: 'none',
        confidence: 0,
      };
    }
  }
  
  /**
   * Draft response in user's style
   */
  async draftResponse(email, analysis) {
    try {
      const prompt = `
**Incoming Email:**
From: ${email.from}
Subject: ${email.subject}
Body: ${email.body}

**Analysis:**
- Requires Response: ${analysis.requiresResponse}
- Urgent: ${analysis.isUrgent}
- Topic: ${analysis.topic}
- Action Needed: ${analysis.actionNeeded}

**Instructions:**
Draft a response in the user's writing style (${this.config.userStyle.formality}, ${this.config.userStyle.tone}).
- Match the user's voice and tone
- Use the user's typical phrases
- Make decisions the user would make
- Include the user's signature: "${this.config.userStyle.signature}"
- Start with "${this.config.userStyle.greeting}"
- End with "${this.config.userStyle.closing}"

**Important:**
- If the email is highly sensitive, flag it for review
- If the decision is complex, flag it for review
- Include a confidence score for the draft

Return as JSON with:
- subject: response subject
- body: response body
- confidence: draft confidence (0-1)
- needsReview: boolean
- reason: if needsReview, explain why`;
      
      const result = await this.shadowModel.generateContent(prompt);
      const draft = JSON.parse(result.response.text());
      
      return {
        subject: draft.subject,
        body: draft.body,
        confidence: draft.confidence || 0.5,
        needsReview: draft.needsReview || false,
        reason: draft.reason || '',
      };
    } catch (error) {
      console.error('Error drafting response:', error.message);
      return {
        subject: `Re: ${email.subject}`,
        body: 'Error drafting response',
        confidence: 0,
        needsReview: true,
        reason: 'Drafting error',
      };
    }
  }
  
  /**
   * Send email (or save as draft)
   */
  async sendEmail(to, subject, body, isDraft = true) {
    try {
      if (!this.smtp) {
        await this.connectSMTP();
      }
      
      const mailOptions = {
        from: this.config.smtp.user,
        to: to,
        subject: subject,
        text: body,
      };
      
      if (isDraft || this.config.shadowMode.draftOnly) {
        // Save as draft
        const draftPath = path.join('./jarvis/shadowTwin/drafts', `draft_${Date.now()}.json`);
        const dir = path.dirname(draftPath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        
        fs.writeFileSync(draftPath, JSON.stringify(mailOptions, null, 2));
        console.log(`📝 Draft saved to ${draftPath}`);
        
        return {
          success: true,
          draft: true,
          path: draftPath,
        };
      } else {
        // Send actual email
        const info = await this.smtp.sendMail(mailOptions);
        console.log(`📧 Email sent: ${info.messageId}`);
        
        return {
          success: true,
          draft: false,
          messageId: info.messageId,
        };
      }
    } catch (error) {
      console.error('❌ Error sending email:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Process unread emails
   */
  async processEmails() {
    try {
      // Reset daily counter if needed
      if (this.lastResetDate !== new Date().toDateString()) {
        this.dailyReplyCount = 0;
        this.lastResetDate = new Date().toDateString();
      }
      
      // Check daily limit
      if (this.dailyReplyCount >= this.config.shadowMode.maxDailyReplies) {
        console.log('⚠️ Daily reply limit reached');
        return {
          success: true,
          message: 'Daily reply limit reached',
          processed: 0,
        };
      }
      
      // Fetch unread emails
      const emails = await this.fetchUnreadEmails();
      
      const results = [];
      
      for (const email of emails) {
        // Analyze email
        const analysis = await this.analyzeEmail(email);
        
        // Check if response is needed
        if (!analysis.requiresResponse) {
          results.push({
            email: email.subject,
            action: 'skipped',
            reason: 'No response needed',
          });
          continue;
        }
        
        // Check confidence threshold
        if (analysis.confidence < this.config.shadowMode.autoReplyThreshold) {
          results.push({
            email: email.subject,
            action: 'flagged',
            reason: 'Low confidence',
          });
          continue;
        }
        
        // Draft response
        const draft = await this.draftResponse(email, analysis);
        
        // Check if needs review
        if (draft.needsReview) {
          results.push({
            email: email.subject,
            action: 'flagged',
            reason: draft.reason,
          });
          continue;
        }
        
        // Send or save draft
        const sendResult = await this.sendEmail(
          email.from,
          draft.subject,
          draft.body,
          this.config.shadowMode.draftOnly
        );
        
        this.dailyReplyCount++;
        
        results.push({
          email: email.subject,
          action: sendResult.draft ? 'drafted' : 'sent',
          confidence: draft.confidence,
        });
      }
      
      return {
        success: true,
        processed: results.length,
        results: results,
      };
      
    } catch (error) {
      console.error('❌ Error processing emails:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Train Shadow Mode from user's sent emails
   */
  async trainFromSentEmails(sentEmails) {
    try {
      console.log(`🎓 Training Shadow Mode from ${sentEmails.length} sent emails...`);
      
      // Extract writing patterns from sent emails
      const patterns = await this._extractWritingPatterns(sentEmails);
      
      // Update user style configuration
      this.config.userStyle = {
        ...this.config.userStyle,
        ...patterns,
      };
      
      // Reinitialize model with updated style
      this._initializeShadowModel();
      
      console.log('✅ Shadow Mode training complete');
      
      return {
        success: true,
        patterns: patterns,
      };
      
    } catch (error) {
      console.error('❌ Error training Shadow Mode:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Extract writing patterns from emails
   */
  async _extractWritingPatterns(emails) {
    // Use Gemini to analyze writing patterns
    const prompt = `
Analyze these ${emails.length} emails and extract the user's writing patterns:
${emails.map(e => `- Subject: ${e.subject}\n- Body: ${e.body}`).join('\n\n')}

Extract:
- Average sentence length
- Common phrases
- Greeting style
- Closing style
- Formality level
- Tone
- Emoji usage
- Punctuation style

Return as JSON.`;
    
    const result = await this.shadowModel.generateContent(prompt);
    const patterns = JSON.parse(result.response.text());
    
    return patterns;
  }
  
  /**
   * Get Shadow Twin status
   */
  getStatus() {
    return {
      enabled: this.config.shadowMode.enabled,
      draftOnly: this.config.shadowMode.draftOnly,
      dailyReplyCount: this.dailyReplyCount,
      maxDailyReplies: this.config.shadowMode.maxDailyReplies,
      lastResetDate: this.lastResetDate,
      userStyle: this.config.userStyle,
    };
  }
  
  /**
   * Enable/disable Shadow Mode
   */
  setShadowMode(enabled, draftOnly = true) {
    this.config.shadowMode.enabled = enabled;
    this.config.shadowMode.draftOnly = draftOnly;
    
    console.log(`Shadow Mode: ${enabled ? 'enabled' : 'disabled'} (draft-only: ${draftOnly})`);
    
    return {
      enabled: enabled,
      draftOnly: draftOnly,
    };
  }
}

// Singleton instance
let shadowTwinEmailHandler = null;

function getShadowTwinEmailHandler(config = null) {
  if (!shadowTwinEmailHandler) {
    if (config === null) {
      config = {};
    }
    shadowTwinEmailHandler = new ShadowTwinEmailHandler(config);
  }
  return shadowTwinEmailHandler;
}

module.exports = { ShadowTwinEmailHandler, getShadowTwinEmailHandler };

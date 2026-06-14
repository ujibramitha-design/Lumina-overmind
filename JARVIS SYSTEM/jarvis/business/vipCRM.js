/**
 * JARVIS VIP Personal CRM (The Mafia Network)
 * =========================================
 * 
 * VIP contact database system with automated news monitoring
 * and contextual message generation for relationship building.
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class VIPCRM {
  constructor(config = {}) {
    this.config = {
      dbPath: config.dbPath || './jarvis/data/vip_crm.db',
      newsCheckInterval: config.newsCheckInterval || 'weekly',
      notificationChannels: config.notificationChannels || ['telegram'],
      ...config,
    };
    
    this.db = null;
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.messageGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getMessageGeneratorPrompt(),
    });
    
    this._initializeDatabase();
  }
  
  /**
   * Message generator system prompt
   */
  _getMessageGeneratorPrompt() {
    return `You are an elite relationship manager specializing in high-net-worth networking.

**Your Role:**
- Generate contextual, personalized messages for VIP contacts
- Reference specific news, achievements, or milestones
- Maintain professional yet warm tone
- Focus on building genuine relationships
- Avoid generic congratulations

**Message Structure:**
1. Personalized opening (reference specific news)
2. Contextual acknowledgment (show understanding)
3. Genuine congratulations or insight
4. Value-add or offer to help
5. Professional closing

**Guidelines:**
- Reference specific news or achievements
- Be concise and respectful
- Focus on mutual value
- Avoid sales pitches
- Keep under 150 words
- Sound authentic and genuine

**Output Format:**
Return JSON with:
- message: the contextual message
- confidence: personalization confidence (0-1)
- references: array of specific references used`;
  }
  
  /**
   * Initialize SQLite database
   */
  _initializeDatabase() {
    try {
      const dbDir = path.dirname(this.config.dbPath);
      if (!require('fs').existsSync(dbDir)) {
        require('fs').mkdirSync(dbDir, { recursive: true });
      }
      
      this.db = new sqlite3.Database(this.config.dbPath);
      
      // Create tables
      this.db.serialize(() => {
        this.db.run(`
          CREATE TABLE IF NOT EXISTS vip_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            title TEXT,
            email TEXT,
            phone TEXT,
            linkedin TEXT,
            twitter TEXT,
            website TEXT,
            notes TEXT,
            tier TEXT DEFAULT 'silver',
            last_interaction_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
          )
        `);
        
        this.db.run(`
          CREATE TABLE IF NOT EXISTS company_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            news_title TEXT,
            news_link TEXT,
            news_date TEXT,
            news_type TEXT,
            processed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
          )
        `);
        
        this.db.run(`
          CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vip_id INTEGER,
            interaction_type TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vip_id) REFERENCES vip_contacts(id)
          )
        `);
        
        this.db.run(`
          CREATE TABLE IF NOT EXISTS message_drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vip_id INTEGER,
            news_id INTEGER,
            message TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            sent_at TEXT,
            FOREIGN KEY (vip_id) REFERENCES vip_contacts(id),
            FOREIGN KEY (news_id) REFERENCES company_news(id)
          )
        `);
      });
      
      console.log('✅ VIP CRM database initialized');
      
    } catch (error) {
      console.error('❌ Error initializing database:', error.message);
    }
  }
  
  /**
   * Add VIP contact
   */
  async addVIPContact(contact) {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          INSERT INTO vip_contacts (name, company, title, email, phone, linkedin, twitter, website, notes, tier)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;
        
        this.db.run(sql, [
          contact.name,
          contact.company || null,
          contact.title || null,
          contact.email || null,
          contact.phone || null,
          contact.linkedin || null,
          contact.twitter || null,
          contact.website || null,
          contact.notes || null,
          contact.tier || 'silver',
        ], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              id: this.lastID,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Get VIP contact by ID
   */
  async getVIPContact(id) {
    return new Promise((resolve, reject) => {
      try {
        const sql = 'SELECT * FROM vip_contacts WHERE id = ?';
        
        this.db.get(sql, [id], (err, row) => {
          if (err) {
            reject(err);
          } else {
            resolve(row);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Get all VIP contacts
   */
  async getAllVIPContacts() {
    return new Promise((resolve, reject) => {
      try {
        const sql = 'SELECT * FROM vip_contacts ORDER BY tier DESC, last_interaction_date DESC';
        
        this.db.all(sql, [], (err, rows) => {
          if (err) {
            reject(err);
          } else {
            resolve(rows);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Update VIP contact
   */
  async updateVIPContact(id, updates) {
    return new Promise((resolve, reject) => {
      try {
        const fields = [];
        const values = [];
        
        for (const [key, value] of Object.entries(updates)) {
          fields.push(`${key} = ?`);
          values.push(value);
        }
        
        fields.push('updated_at = CURRENT_TIMESTAMP');
        values.push(id);
        
        const sql = `UPDATE vip_contacts SET ${fields.join(', ')} WHERE id = ?`;
        
        this.db.run(sql, values, function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              changes: this.changes,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Update last interaction date
   */
  async updateLastInteraction(id) {
    return this.updateVIPContact(id, {
      last_interaction_date: new Date().toISOString(),
    });
  }
  
  /**
   * Add interaction record
   */
  async addInteraction(vipId, interactionType, notes = null) {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          INSERT INTO interactions (vip_id, interaction_type, notes)
          VALUES (?, ?, ?)
        `;
        
        this.db.run(sql, [vipId, interactionType, notes], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              id: this.lastID,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Check for company news
   */
  async checkCompanyNews(companyName) {
    try {
      console.log(`🔍 Checking news for: ${companyName}`);
      
      // Search for recent company news
      const searchQuery = encodeURIComponent(`${companyName} news recent funding launch`);
      const searchUrl = `https://www.google.com/search?q=${searchQuery}&tbm=nws`;
      
      const response = await axios.get(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
        timeout: 30000,
      });
      
      const $ = cheerio.load(response.data);
      const newsItems = [];
      
      $('div.g').each((i, element) => {
        if (i >= 5) return;  // Limit to 5 news items
        
        const title = $(element).find('h3').text().trim();
        const link = $(element).find('a').first().attr('href');
        const snippet = $(element).find('div.VwiC3b').text().trim();
        
        if (title && link) {
          // Determine news type
          let newsType = 'general';
          if (title.toLowerCase().includes('funding') || title.toLowerCase().includes('raise')) {
            newsType = 'funding';
          } else if (title.toLowerCase().includes('launch') || title.toLowerCase().includes('release')) {
            newsType = 'product_launch';
          } else if (title.toLowerCase().includes('acquisition') || title.toLowerCase().includes('buy')) {
            newsType = 'acquisition';
          } else if (title.toLowerCase().includes('partnership') || title.toLowerCase().includes('collabor')) {
            newsType = 'partnership';
          }
          
          newsItems.push({
            title,
            link,
            snippet,
            type: newsType,
            date: new Date().toISOString(),
          });
        }
      });
      
      // Store news in database
      for (const item of newsItems) {
        await this._storeCompanyNews(companyName, item);
      }
      
      console.log(`✅ Found ${newsItems.length} news items for ${companyName}`);
      
      return {
        success: true,
        company: companyName,
        newsItems: newsItems,
      };
      
    } catch (error) {
      console.error('❌ Error checking company news:', error.message);
      return {
        success: false,
        error: error.message,
        newsItems: [],
      };
    }
  }
  
  /**
   * Store company news in database
   */
  async _storeCompanyNews(company, newsItem) {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          INSERT INTO company_news (company, news_title, news_link, news_date, news_type)
          VALUES (?, ?, ?, ?, ?)
        `;
        
        this.db.run(sql, [
          company,
          newsItem.title,
          newsItem.link,
          newsItem.date,
          newsItem.type,
        ], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              id: this.lastID,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Get unprocessed news for company
   */
  async getUnprocessedNews(company) {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          SELECT * FROM company_news
          WHERE company = ? AND processed = 0
          ORDER BY created_at DESC
        `;
        
        this.db.all(sql, [company], (err, rows) => {
          if (err) {
            reject(err);
          } else {
            resolve(rows);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Mark news as processed
   */
  async markNewsAsProcessed(newsId) {
    return new Promise((resolve, reject) => {
      try {
        const sql = 'UPDATE company_news SET processed = 1 WHERE id = ?';
        
        this.db.run(sql, [newsId], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              changes: this.changes,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Generate contextual message
   */
  async generateContextualMessage(vipContact, newsItem) {
    try {
      console.log(`📝 Generating contextual message for ${vipContact.name}`);
      
      const prompt = `
**VIP Name:** ${vipContact.name}
**Company:** ${vipContact.company}
**Title:** ${vipContact.title}

**News Item:**
Title: ${newsItem.news_title}
Type: ${newsItem.news_type}
Link: ${newsItem.news_link}

**Instructions:**
Generate a contextual, personalized message:
- Reference the specific news item
- Show genuine interest in their success
- Offer value or help if appropriate
- Keep under 150 words
- Sound authentic and professional
- Avoid generic congratulations

Return as JSON with message, confidence, and references.`;
      
      const result = await this.messageGenerator.generateContent(prompt);
      const messageData = JSON.parse(result.response.text());
      
      return {
        success: true,
        message: messageData.message,
        confidence: messageData.confidence || 0.7,
        references: messageData.references || [],
      };
      
    } catch (error) {
      console.error('❌ Error generating message:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Create message draft
   */
  async createMessageDraft(vipId, newsId, message) {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          INSERT INTO message_drafts (vip_id, news_id, message, status)
          VALUES (?, ?, ?, 'pending')
        `;
        
        this.db.run(sql, [vipId, newsId, message], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              id: this.lastID,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Run weekly news check cycle
   */
  async runWeeklyNewsCheck() {
    try {
      console.log('🚀 Starting weekly news check cycle...');
      
      // Get all VIP contacts
      const contacts = await this.getAllVIPContacts();
      
      const results = [];
      
      for (const contact of contacts) {
        if (!contact.company) {
          continue;
        }
        
        // Check for company news
        const newsResult = await this.checkCompanyNews(contact.company);
        
        if (!newsResult.success || newsResult.newsItems.length === 0) {
          continue;
        }
        
        // Get unprocessed news
        const unprocessedNews = await this.getUnprocessedNews(contact.company);
        
        for (const news of unprocessedNews) {
          // Generate contextual message
          const messageResult = await this.generateContextualMessage(contact, news);
          
          if (!messageResult.success) {
            continue;
          }
          
          // Create message draft
          const draftResult = await this.createMessageDraft(
            contact.id,
            news.id,
            messageResult.message
          );
          
          results.push({
            vip: contact.name,
            company: contact.company,
            news: news.news_title,
            message: messageResult.message,
            draftId: draftResult.id,
          });
          
          // Mark news as processed
          await this.markNewsAsProcessed(news.id);
        }
      }
      
      console.log(`✅ Weekly news check complete: ${results.length} message drafts created`);
      
      return {
        success: true,
        draftsCreated: results.length,
        results: results,
      };
      
    } catch (error) {
      console.error('❌ Error in weekly news check:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get pending message drafts
   */
  async getPendingDrafts() {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          SELECT md.*, vc.name, vc.company, vc.email
          FROM message_drafts md
          JOIN vip_contacts vc ON md.vip_id = vc.id
          WHERE md.status = 'pending'
          ORDER BY md.created_at DESC
        `;
        
        this.db.all(sql, [], (err, rows) => {
          if (err) {
            reject(err);
          } else {
            resolve(rows);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Mark draft as sent
   */
  async markDraftAsSent(draftId) {
    return new Promise((resolve, reject) => {
      try {
        const sql = `
          UPDATE message_drafts
          SET status = 'sent', sent_at = CURRENT_TIMESTAMP
          WHERE id = ?
        `;
        
        this.db.run(sql, [draftId], function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              changes: this.changes,
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Get CRM statistics
   */
  async getStats() {
    return new Promise((resolve, reject) => {
      try {
        const stats = {};
        
        // Count VIP contacts
        this.db.get('SELECT COUNT(*) as count FROM vip_contacts', [], (err, row) => {
          if (err) {
            reject(err);
          } else {
            stats.vipCount = row.count;
            
            // Count pending drafts
            this.db.get('SELECT COUNT(*) as count FROM message_drafts WHERE status = "pending"', [], (err, row) => {
              if (err) {
                reject(err);
              } else {
                stats.pendingDrafts = row.count;
                
                // Count sent messages
                this.db.get('SELECT COUNT(*) as count FROM message_drafts WHERE status = "sent"', [], (err, row) => {
                  if (err) {
                    reject(err);
                  } else {
                    stats.sentMessages = row.count;
                    resolve(stats);
                  }
                });
              }
            });
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  
  /**
   * Close database connection
   */
  async close() {
    return new Promise((resolve, reject) => {
      try {
        this.db.close((err) => {
          if (err) {
            reject(err);
          } else {
            console.log('✅ Database connection closed');
            resolve(true);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }
}

// Singleton instance
let vipCRM = null;

function getVIPCRM(config = null) {
  if (!vipCRM) {
    if (config === null) {
      config = {};
    }
    vipCRM = new VIPCRM(config);
  }
  return vipCRM;
}

module.exports = { VIPCRM, getVIPCRM };

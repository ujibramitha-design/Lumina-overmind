/**
 * JARVIS Auto-Freelancer Module (Gig Hunter)
 * =========================================
 * 
 * Automated freelancing job hunting system that parses RSS feeds,
* scores job relevance, generates proposals, and sends notifications.
 */

const Parser = require('rss-parser');
const axios = require('axios');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class GigHunter {
  constructor(config = {}) {
    this.config = {
      rssFeeds: config.rssFeeds || [
        'https://www.upwork.com/ab/feed/jobs/search?q=web%20scraping',
        'https://www.upwork.com/ab/feed/jobs/search?q=python%20automation',
        'https://www.freelancer.com/rss/projects.xml',
      ],
      keywords: config.keywords || [
        'web scraping', 'python', 'automation', 'data extraction',
        'puppeteer', 'playwright', 'selenium', 'api integration',
        'bot development', 'scripting', 'data mining',
      ],
      minBudget: config.minBudget || 50,
      maxBudget: config.maxBudget || 10000,
      relevanceThreshold: config.relevanceThreshold || 0.7,
      dailyLimit: config.dailyLimit || 10,
      notificationChannels: config.notificationChannels || ['whatsapp'],
      ...config,
    };
    
    this.parser = new Parser();
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.proposalGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getProposalGeneratorPrompt(),
    });
    
    this.processedJobs = new Set();
    this.dailyCount = 0;
    this.lastResetDate = new Date().toDateString();
  }
  
  /**
   * Proposal generator system prompt
   */
  _getProposalGeneratorPrompt() {
    return `You are an elite freelance proposal writer with exceptional closing skills.

**Your Role:**
- Write highly persuasive, customized cover letters
- Apply PAS (Problem-Agitation-Solution) framework
- Focus on value propositions and benefits
- Demonstrate expertise and credibility
- Include clear call-to-action
- Keep proposals under 300 words

**PAS Framework:**
- Problem: Acknowledge the client's challenge
- Agitation: Make the problem feel urgent and costly
- Solution: Present your expertise as the solution

**Proposal Structure:**
1. Personalized opening (acknowledge specific project details)
2. Problem identification (show understanding of their needs)
3. Agitation (highlight consequences of not solving)
4. Solution (present your expertise and approach)
5. Social proof (mention relevant experience)
6. Clear call-to-action (next steps)

**Guidelines:**
- Personalize based on job description
- Use power words and emotional triggers
- Focus on benefits, not just features
- Be confident but not arrogant
- Include specific examples when possible
- Keep it concise and compelling

**Output Format:**
Return JSON with:
- proposal: the cover letter text
- confidence: proposal quality confidence (0-1)
- suggestedBid: suggested bid amount`;
  }
  
  /**
   * Parse RSS feeds
   */
  async parseRSSFeeds() {
    try {
      console.log('📡 Parsing RSS feeds...');
      
      const allJobs = [];
      
      for (const feedUrl of this.config.rssFeeds) {
        try {
          const response = await axios.get(feedUrl, {
            timeout: 30000,
            headers: {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
          });
          
          const feed = await this.parser.parseString(response.data);
          const jobs = feed.items.map(item => ({
            title: item.title,
            link: item.link,
            description: item.contentSnippet || item.content,
            pubDate: item.pubDate,
            guid: item.guid,
            source: feedUrl,
          }));
          
          allJobs.push(...jobs);
          console.log(`📥 Fetched ${jobs.length} jobs from ${feedUrl}`);
          
        } catch (error) {
          console.error(`❌ Error parsing feed ${feedUrl}:`, error.message);
        }
      }
      
      console.log(`✅ Total jobs fetched: ${allJobs.length}`);
      
      return allJobs;
      
    } catch (error) {
      console.error('❌ Error parsing RSS feeds:', error.message);
      return [];
    }
  }
  
  /**
   * Score job relevance
   */
  scoreJobRelevance(job) {
    try {
      const title = job.title.toLowerCase();
      const description = job.description.toLowerCase();
      const combinedText = `${title} ${description}`;
      
      let score = 0;
      let matchedKeywords = [];
      
      // Check for keyword matches
      for (const keyword of this.config.keywords) {
        if (combinedText.includes(keyword.toLowerCase())) {
          score += 0.2;
          matchedKeywords.push(keyword);
        }
      }
      
      // Check for budget range
      const budgetMatch = combinedText.match(/\$(\d+)/);
      if (budgetMatch) {
        const budget = parseInt(budgetMatch[1]);
        if (budget >= this.config.minBudget && budget <= this.config.maxBudget) {
          score += 0.3;
        }
      }
      
      // Check for "hourly" vs "fixed" preference
      if (combinedText.includes('hourly')) {
        score += 0.1;
      }
      
      // Check for "verified" or "payment verified"
      if (combinedText.includes('verified')) {
        score += 0.2;
      }
      
      // Check for client history (positive indicator)
      if (combinedText.includes('client') && combinedText.includes('review')) {
        score += 0.1;
      }
      
      // Normalize score
      score = Math.min(score, 1.0);
      
      return {
        score: score,
        matchedKeywords: matchedKeywords,
        budget: budgetMatch ? budgetMatch[1] : null,
      };
      
    } catch (error) {
      console.error('Error scoring job relevance:', error.message);
      return { score: 0, matchedKeywords: [], budget: null };
    }
  }
  
  /**
   * Filter relevant jobs
   */
  filterRelevantJobs(jobs) {
    try {
      console.log('🔍 Filtering relevant jobs...');
      
      const relevantJobs = [];
      
      for (const job of jobs) {
        // Skip if already processed
        if (this.processedJobs.has(job.guid)) {
          continue;
        }
        
        // Score relevance
        const relevance = this.scoreJobRelevance(job);
        
        // Check if meets threshold
        if (relevance.score >= this.config.relevanceThreshold) {
          relevantJobs.push({
            ...job,
            relevance: relevance,
          });
          
          // Mark as processed
          this.processedJobs.add(job.guid);
        }
      }
      
      console.log(`✅ Found ${relevantJobs.length} relevant jobs`);
      
      return relevantJobs;
      
    } catch (error) {
      console.error('❌ Error filtering jobs:', error.message);
      return [];
    }
  }
  
  /**
   * Generate proposal for job
   */
  async generateProposal(job) {
    try {
      console.log(`📝 Generating proposal for: ${job.title}`);
      
      const prompt = `
**Job Title:** ${job.title}
**Job Description:** ${job.description}
**Job Link:** ${job.link}
**Relevance Score:** ${job.relevance.score}
**Matched Keywords:** ${job.relevance.matchedKeywords.join(', ')}

**Instructions:**
Generate a highly persuasive cover letter proposal using the PAS framework.
- Personalize based on the specific job details
- Focus on value propositions and benefits
- Demonstrate expertise in the matched keywords
- Include clear call-to-action
- Keep under 300 words
- Suggest an appropriate bid amount

Return as JSON with proposal, confidence, and suggestedBid.`;
      
      const result = await this.proposalGenerator.generateContent(prompt);
      const proposalData = JSON.parse(result.response.text());
      
      return {
        success: true,
        proposal: proposalData.proposal,
        confidence: proposalData.confidence || 0.7,
        suggestedBid: proposalData.suggestedBid || 50,
      };
      
    } catch (error) {
      console.error('❌ Error generating proposal:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Send notification via WhatsApp
   */
  async sendWhatsAppNotification(job, proposal) {
    try {
      console.log(`📱 Sending WhatsApp notification...`);
      
      // This would integrate with the WhatsApp client
      // For now, we'll return the notification content
      const notification = `
🎯 *New Relevant Job Found!*

*Title:* ${job.title}
*Link:* ${job.link}
*Relevance:* ${(job.relevance.score * 100).toFixed(0)}%
*Matched Keywords:* ${job.relevance.matchedKeywords.join(', ')}
*Suggested Bid:* $${proposal.suggestedBid}

*Generated Proposal:*
${proposal.proposal}

*Confidence:* ${(proposal.confidence * 100).toFixed(0)}%

Reply "APPROVE" to submit this proposal.
`;
      
      console.log('✅ WhatsApp notification prepared');
      
      return {
        success: true,
        notification: notification,
      };
      
    } catch (error) {
      console.error('❌ Error sending notification:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Run gig hunting cycle
   */
  async runGigHuntingCycle() {
    try {
      console.log('🚀 Starting gig hunting cycle...');
      
      // Reset daily counter if needed
      if (this.lastResetDate !== new Date().toDateString()) {
        this.dailyCount = 0;
        this.lastResetDate = new Date().toDateString();
        console.log('🔄 Daily counter reset');
      }
      
      // Check daily limit
      if (this.dailyCount >= this.config.dailyLimit) {
        console.log('⚠️ Daily limit reached');
        return {
          success: true,
          message: 'Daily limit reached',
          jobsProcessed: 0,
        };
      }
      
      // Parse RSS feeds
      const jobs = await this.parseRSSFeeds();
      
      if (jobs.length === 0) {
        return {
          success: true,
          message: 'No jobs found',
          jobsProcessed: 0,
        };
      }
      
      // Filter relevant jobs
      const relevantJobs = this.filterRelevantJobs(jobs);
      
      if (relevantJobs.length === 0) {
        return {
          success: true,
          message: 'No relevant jobs found',
          jobsProcessed: 0,
        };
      }
      
      // Process jobs (respect daily limit)
      const jobsToProcess = relevantJobs.slice(0, this.config.dailyLimit - this.dailyCount);
      const results = [];
      
      for (const job of jobsToProcess) {
        // Generate proposal
        const proposal = await this.generateProposal(job);
        
        if (!proposal.success) {
          continue;
        }
        
        // Send notification
        const notification = await this.sendWhatsAppNotification(job, proposal);
        
        results.push({
          job: job.title,
          link: job.link,
          proposal: proposal.proposal,
          suggestedBid: proposal.suggestedBid,
          notificationSent: notification.success,
        });
        
        this.dailyCount++;
        
        // Small delay between jobs
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
      
      console.log(`✅ Gig hunting cycle complete: ${results.length} jobs processed`);
      
      return {
        success: true,
        jobsProcessed: results.length,
        results: results,
      };
      
    } catch (error) {
      console.error('❌ Error in gig hunting cycle:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get statistics
   */
  getStats() {
    return {
      processedJobsCount: this.processedJobs.size,
      dailyCount: this.dailyCount,
      dailyLimit: this.config.dailyLimit,
      lastResetDate: this.lastResetDate,
      remaining: this.config.dailyLimit - this.dailyCount,
    };
  }
  
  /**
   * Reset daily counter
   */
  resetDailyCounter() {
    this.dailyCount = 0;
    this.lastResetDate = new Date().toDateString();
    console.log('🔄 Daily counter reset');
  }
  
  /**
   * Clear processed jobs cache
   */
  clearProcessedJobs() {
    this.processedJobs.clear();
    console.log('🗑️ Processed jobs cache cleared');
  }
}

// Singleton instance
let gigHunter = null;

function getGigHunter(config = null) {
  if (!gigHunter) {
    if (config === null) {
      config = {};
    }
    gigHunter = new GigHunter(config);
  }
  return gigHunter;
}

module.exports = { GigHunter, getGigHunter };

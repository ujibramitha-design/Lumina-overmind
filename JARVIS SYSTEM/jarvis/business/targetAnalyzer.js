/**
 * JARVIS Whale Hunter Intelligence Agent
 * ===================================
 * 
 * High-Net-Worth networking intelligence system that enriches target data
 * and generates hyper-personalized pitches for maximum engagement.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const axios = require('axios');
const cheerio = require('cheerio');
require('dotenv').config();

class TargetAnalyzer {
  constructor(config = {}) {
    this.config = {
      dataSources: config.dataSources || {
        linkedin: true,
        companyNews: true,
        podcasts: true,
        socialMedia: true,
      },
      enrichmentAPIs: config.enrichmentAPIs || {
        clearbit: config.clearbitApiKey || process.env.CLEARBIT_API_KEY,
        crunchbase: config.crunchbaseApiKey || process.env.CRUNCHBASE_API_KEY,
      },
      outputFormat: config.outputFormat || 'json',
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.pitchGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getPitchGeneratorPrompt(),
    });
  }
  
  /**
   * Pitch generator system prompt
   */
  _getPitchGeneratorPrompt() {
    return `You are an elite business development specialist specializing in hyper-personalized outreach to high-net-worth individuals.

**Your Role:**
- Generate hyper-personalized pitches based on target data
- Reference specific recent statements, achievements, or pain points
- Create compelling hooks that guarantee high open/reply rates
- Maintain professional yet conversational tone
- Focus on value propositions relevant to the target

**Pitch Structure:**
1. Personalized Hook (reference specific recent activity)
2. Contextual Connection (show understanding of their situation)
3. Value Proposition (relevant to their current focus)
4. Clear Call-to-Action (specific next step)
5. Professional Closing

**Guidelines:**
- Reference specific recent news, posts, or statements
- Show genuine interest in their work
- Be concise and respectful of their time
- Focus on mutual value
- Avoid generic fluff
- Keep under 200 words

**Output Format:**
Return JSON with:
- pitch: the hyper-personalized pitch
- confidence: personalization confidence (0-1)
- references: array of specific references used`;
  }
  
  /**
   * Enrich target data from multiple sources
   */
  async enrichTargetData(targetName, companyName = null) {
    try {
      console.log(`🔍 Enriching data for: ${targetName}`);
      
      const enrichmentData = {
        name: targetName,
        company: companyName,
        linkedin: {},
        companyNews: {},
        podcasts: {},
        socialMedia: {},
        recentActivity: [],
        painPoints: [],
        interests: [],
      };
      
      // LinkedIn enrichment
      if (this.config.dataSources.linkedin) {
        enrichmentData.linkedin = await this._enrichLinkedIn(targetName, companyName);
      }
      
      // Company news enrichment
      if (this.config.dataSources.companyNews && companyName) {
        enrichmentData.companyNews = await this._enrichCompanyNews(companyName);
      }
      
      // Podcast appearances
      if (this.config.dataSources.podcasts) {
        enrichmentData.podcasts = await this._enrichPodcasts(targetName);
      }
      
      // Social media activity
      if (this.config.dataSources.socialMedia) {
        enrichmentData.socialMedia = await this._enrichSocialMedia(targetName);
      }
      
      // API enrichment (Clearbit, Crunchbase)
      if (this.config.enrichmentAPIs.clearbit && companyName) {
        enrichmentData.companyData = await this._enrichClearbit(companyName);
      }
      
      if (this.config.enrichmentAPIs.crunchbase && companyName) {
        enrichmentData.fundingData = await this._enrichCrunchbase(companyName);
      }
      
      // Extract recent activity and pain points
      enrichmentData.recentActivity = this._extractRecentActivity(enrichmentData);
      enrichmentData.painPoints = this._extractPainPoints(enrichmentData);
      enrichmentData.interests = this._extractInterests(enrichmentData);
      
      console.log('✅ Target data enriched');
      
      return {
        success: true,
        data: enrichmentData,
      };
      
    } catch (error) {
      console.error('❌ Error enriching target data:', error.message);
      return {
        success: false,
        error: error.message,
        data: null,
      };
    }
  }
  
  /**
   * Enrich LinkedIn data
   */
  async _enrichLinkedIn(targetName, companyName) {
    try {
      // Note: LinkedIn scraping requires careful handling
      // This is a placeholder for LinkedIn enrichment
      // In production, use official LinkedIn API or specialized services
      
      console.log('📝 LinkedIn enrichment (placeholder)');
      
      return {
        profile: `https://www.linkedin.com/in/${targetName.toLowerCase().replace(/\s+/g, '-')}`,
        recentPosts: [],
        activity: 'LinkedIn enrichment requires official API access',
      };
      
    } catch (error) {
      console.error('Error enriching LinkedIn:', error.message);
      return {};
    }
  }
  
  /**
   * Enrich company news
   */
  async _enrichCompanyNews(companyName) {
    try {
      // Search for recent company news
      const searchQuery = encodeURIComponent(`${companyName} news recent`);
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
          newsItems.push({
            title,
            link,
            snippet,
          });
        }
      });
      
      return {
        newsItems,
        lastUpdated: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('Error enriching company news:', error.message);
      return { newsItems: [] };
    }
  }
  
  /**
   * Enrich podcast appearances
   */
  async _enrichPodcasts(targetName) {
    try {
      // Search for podcast appearances
      const searchQuery = encodeURIComponent(`${targetName} podcast interview`);
      const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
      
      const response = await axios.get(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
        timeout: 30000,
      });
      
      const $ = cheerio.load(response.data);
      const podcasts = [];
      
      $('div.g').each((i, element) => {
        if (i >= 3) return;  // Limit to 3 podcasts
        
        const title = $(element).find('h3').text().trim();
        const link = $(element).find('a').first().attr('href');
        
        if (title && link && title.toLowerCase().includes('podcast')) {
          podcasts.push({
            title,
            link,
          });
        }
      });
      
      return {
        podcasts,
        lastUpdated: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('Error enriching podcasts:', error.message);
      return { podcasts: [] };
    }
  }
  
  /**
   * Enrich social media activity
   */
  async _enrichSocialMedia(targetName) {
    try {
      // Search for social media presence
      const searchQuery = encodeURIComponent(`${targetName} Twitter X LinkedIn`);
      const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
      
      const response = await axios.get(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
        timeout: 30000,
      });
      
      const $ = cheerio.load(response.data);
      const socialProfiles = [];
      
      $('div.g').each((i, element) => {
        if (i >= 5) return;  // Limit to 5 profiles
        
        const title = $(element).find('h3').text().trim();
        const link = $(element).find('a').first().attr('href');
        
        if (title && link) {
          const platform = this._detectPlatform(link);
          if (platform) {
            socialProfiles.push({
              platform,
              title,
              link,
            });
          }
        }
      });
      
      return {
        socialProfiles,
        lastUpdated: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('Error enriching social media:', error.message);
      return { socialProfiles: [] };
    }
  }
  
  /**
   * Detect social media platform from URL
   */
  _detectPlatform(url) {
    if (url.includes('twitter.com') || url.includes('x.com')) return 'Twitter';
    if (url.includes('linkedin.com')) return 'LinkedIn';
    if (url.includes('instagram.com')) return 'Instagram';
    if (url.includes('facebook.com')) return 'Facebook';
    if (url.includes('youtube.com')) return 'YouTube';
    return null;
  }
  
  /**
   * Enrich with Clearbit API
   */
  async _enrichClearbit(companyName) {
    try {
      if (!this.config.enrichmentAPIs.clearbit) {
        return {};
      }
      
      const domain = await this._findCompanyDomain(companyName);
      if (!domain) {
        return {};
      }
      
      const response = await axios.get(`https://company.clearbit.com/v2/companies/find?domain=${domain}`, {
        headers: {
          'Authorization': `Bearer ${this.config.enrichmentAPIs.clearbit}`,
        },
        timeout: 30000,
      });
      
      return response.data;
      
    } catch (error) {
      console.error('Error enriching with Clearbit:', error.message);
      return {};
    }
  }
  
  /**
   * Enrich with Crunchbase API
   */
  async _enrichCrunchbase(companyName) {
    try {
      if (!this.config.enrichmentAPIs.crunchbase) {
        return {};
      }
      
      // Crunchbase API integration
      // This requires proper API setup
      return {
        funding: 'Crunchbase API integration requires setup',
      };
      
    } catch (error) {
      console.error('Error enriching with Crunchbase:', error.message);
      return {};
    }
  }
  
  /**
   * Find company domain
   */
  async _findCompanyDomain(companyName) {
    try {
      const searchQuery = encodeURIComponent(`${companyName} official website`);
      const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
      
      const response = await axios.get(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
        timeout: 30000,
      });
      
      const $ = cheerio.load(response.data);
      const firstResult = $('div.g').first().find('a').first().attr('href');
      
      if (firstResult) {
        const url = new URL(firstResult);
        return url.hostname;
      }
      
      return null;
      
    } catch (error) {
      console.error('Error finding company domain:', error.message);
      return null;
    }
  }
  
  /**
   * Extract recent activity
   */
  _extractRecentActivity(enrichmentData) {
    const activities = [];
    
    // From company news
    if (enrichmentData.companyNews.newsItems) {
      enrichmentData.companyNews.newsItems.forEach(item => {
        activities.push({
          type: 'company_news',
          title: item.title,
          link: item.link,
          date: new Date().toISOString(),
        });
      });
    }
    
    // From podcasts
    if (enrichmentData.podcasts.podcasts) {
      enrichmentData.podcasts.podcasts.forEach(item => {
        activities.push({
          type: 'podcast_appearance',
          title: item.title,
          link: item.link,
          date: new Date().toISOString(),
        });
      });
    }
    
    return activities;
  }
  
  /**
   * Extract pain points
   */
  _extractPainPoints(enrichmentData) {
    const painPoints = [];
    
    // Analyze company news for pain indicators
    if (enrichmentData.companyNews.newsItems) {
      enrichmentData.companyNews.newsItems.forEach(item => {
        const painIndicators = ['challenge', 'struggle', 'issue', 'problem', 'difficulty'];
        const titleLower = item.title.toLowerCase();
        
        if (painIndicators.some(indicator => titleLower.includes(indicator))) {
          painPoints.push({
            source: 'company_news',
            context: item.title,
            link: item.link,
          });
        }
      });
    }
    
    return painPoints;
  }
  
  /**
   * Extract interests
   */
  _extractInterests(enrichmentData) {
    const interests = [];
    
    // Analyze company news for topic indicators
    if (enrichmentData.companyNews.newsItems) {
      enrichmentData.companyNews.newsItems.forEach(item => {
        const topicIndicators = ['AI', 'automation', 'growth', 'expansion', 'technology'];
        const titleLower = item.title.toLowerCase();
        
        topicIndicators.forEach(indicator => {
          if (titleLower.includes(indicator.toLowerCase())) {
            if (!interests.includes(indicator)) {
              interests.push(indicator);
            }
          }
        });
      });
    }
    
    return interests;
  }
  
  /**
   * Generate hyper-personalized pitch
   */
  async generateHyperPersonalizedPitch(enrichmentData, context = {}) {
    try {
      console.log('📝 Generating hyper-personalized pitch...');
      
      const prompt = `
**Target Name:** ${enrichmentData.name}
**Company:** ${enrichmentData.company || 'N/A'}

**Recent Activity:**
${JSON.stringify(enrichmentData.recentActivity, null, 2)}

**Pain Points:**
${JSON.stringify(enrichmentData.painPoints, null, 2)}

**Interests:**
${JSON.stringify(enrichmentData.interests, null, 2)}

**Company News:**
${JSON.stringify(enrichmentData.companyNews.newsItems || [], null, 2)}

**Context:**
${JSON.stringify(context, null, 2)}

**Instructions:**
Generate a hyper-personalized pitch that:
- References specific recent activity or news
- Acknowledges their current focus or challenges
- Provides a relevant value proposition
- Includes a clear call-to-action
- Keeps under 200 words
- Maintains professional yet conversational tone

Return as JSON with pitch, confidence, and references.`;
      
      const result = await this.pitchGenerator.generateContent(prompt);
      const pitchData = JSON.parse(result.response.text());
      
      console.log(`✅ Pitch generated (confidence: ${(pitchData.confidence * 100).toFixed(0)}%)`);
      
      return {
        success: true,
        pitch: pitchData.pitch,
        confidence: pitchData.confidence || 0.7,
        references: pitchData.references || [],
      };
      
    } catch (error) {
      console.error('❌ Error generating pitch:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Complete analysis workflow
   */
  async analyzeTarget(targetName, companyName = null, context = {}) {
    try {
      console.log(`🎯 Starting target analysis for: ${targetName}`);
      
      // Enrich target data
      const enrichmentResult = await this.enrichTargetData(targetName, companyName);
      if (!enrichmentResult.success) {
        return enrichmentResult;
      }
      
      // Generate hyper-personalized pitch
      const pitchResult = await this.generateHyperPersonalizedPitch(
        enrichmentResult.data,
        context
      );
      
      return {
        success: true,
        target: targetName,
        company: companyName,
        enrichmentData: enrichmentResult.data,
        pitch: pitchResult.pitch,
        confidence: pitchResult.confidence,
        references: pitchResult.references,
      };
      
    } catch (error) {
      console.error('❌ Error in target analysis:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
}

// Singleton instance
let targetAnalyzer = null;

function getTargetAnalyzer(config = null) {
  if (!targetAnalyzer) {
    if (config === null) {
      config = {};
    }
    targetAnalyzer = new TargetAnalyzer(config);
  }
  return targetAnalyzer;
}

module.exports = { TargetAnalyzer, getTargetAnalyzer };

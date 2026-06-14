/**
 * JARVIS Shadow CEO - Business Radar
 * =================================
 * 
 * Tiered business opportunity scanner that categorizes opportunities
 * by capital requirements and generates weekly CEO briefings.
 */

const axios = require('axios');
const cheerio = require('cheerio');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class BusinessRadar {
  constructor(config = {}) {
    this.config = {
      sources: {
        flippa: config.flippaEnabled !== false,
        upwork: config.upworkEnabled !== false,
        techNews: config.techNewsEnabled !== false,
        startupNews: config.startupNewsEnabled !== false,
      },
      rssFeeds: config.rssFeeds || [
        'https://www.flippa.com/blog/feed/',
        'https://techcrunch.com/feed/',
        'https://news.ycombinator.com/rss',
        'https://www.upwork.com/ab/feed/jobs/search?q=web%20development',
      ],
      tiers: {
        zeroCapital: {
          maxBudget: 0,
          keywords: ['freelance', 'arbitrage', 'consulting', 'service'],
          types: ['freelance', 'arbitrage', 'consulting'],
        },
        mediumCapital: {
          maxBudget: 50000,
          keywords: ['micro-saas', 'acquisition', 'buy', 'established'],
          types: ['micro-saas', 'acquisition', 'established business'],
        },
        highCapital: {
          maxBudget: Infinity,
          keywords: ['enterprise', 'b2b', 'partnership', 'investment'],
          types: ['enterprise', 'b2b', 'partnership', 'investment'],
        },
      },
      briefingDay: config.briefingDay || 'monday',
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.opportunityAnalyzer = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getOpportunityAnalyzerPrompt(),
    });
    
    this.briefingGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getBriefingGeneratorPrompt(),
    });
    
    this.opportunities = {
      zeroCapital: [],
      mediumCapital: [],
      highCapital: [],
    };
  }
  
  /**
   * Opportunity analyzer system prompt
   */
  _getOpportunityAnalyzerPrompt() {
    return `You are an elite business analyst specializing in opportunity assessment and categorization.

**Your Role:**
- Analyze business opportunities for viability
- Categorize by capital requirements
- Assess risk and reward potential
- Estimate time to ROI
- Identify execution requirements

**Capital Tiers:**
- Zero Capital: Freelance, arbitrage, consulting (no upfront investment)
- Medium Capital: Micro-SaaS acquisition ($0-$50K)
- High Capital: Enterprise B2B solutions, partnerships ($50K+)

**Analysis Structure:**
1. Opportunity Description
2. Capital Requirement Assessment
3. Risk Level (low/medium/high)
4. Estimated ROI
5. Time to ROI
6. Execution Complexity
7. Required Skills
8. Market Demand
9. Competition Level
10. Overall Score (0-100)

**Guidelines:**
- Be realistic about requirements
- Consider market conditions
- Assess competition honestly
- Estimate conservatively
- Focus on actionable insights
- Keep under 200 words

**Output Format:**
Return JSON with:
- tier: capital tier
- risk: risk level
- roi: estimated ROI
- timeToROI: time to ROI
- complexity: execution complexity
- score: overall score (0-100)
- analysis: brief analysis`;
  }
  
  /**
   * Briefing generator system prompt
   */
  _getBriefingGeneratorPrompt() {
    return `You are an elite CEO preparing executive briefings for strategic decision-making.

**Your Role:**
- Generate concise, actionable CEO briefings
- Prioritize opportunities by impact
- Provide step-by-step execution plans
- Consider resource allocation
- Focus on ROI and strategic alignment

**Briefing Structure:**
1. Executive Summary
2. Opportunity Overview
3. Market Analysis
4. Execution Plan (step-by-step)
5. Resource Requirements
6. Risk Assessment
7. Expected ROI
8. Strategic Fit
9. Recommendation

**Guidelines:**
- Be concise and actionable
- Focus on high-impact opportunities
- Provide clear next steps
- Consider resource constraints
- Balance risk and reward
- Keep under 300 words per opportunity

**Output Format:**
Return JSON with:
- executiveSummary: 2-3 sentence summary
- opportunityOverview: detailed description
- marketAnalysis: market conditions
- executionPlan: step-by-step plan
- resourceRequirements: resources needed
- riskAssessment: risks and mitigation
- expectedROI: ROI estimate
- strategicFit: alignment with business goals
- recommendation: go/no-go decision`;
  }
  
  /**
   * Scan RSS feeds for opportunities
   */
  async scanRSSFeeds() {
    try {
      console.log('📡 Scanning RSS feeds for opportunities...');
      
      const allOpportunities = [];
      
      for (const feedUrl of this.config.rssFeeds) {
        try {
          const response = await axios.get(feedUrl, {
            timeout: 30000,
            headers: {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
          });
          
          // Parse RSS/Atom feed
          const items = this._parseFeed(response.data, feedUrl);
          
          for (const item of items) {
            const opportunity = await this._analyzeOpportunity(item);
            if (opportunity) {
              allOpportunities.push(opportunity);
            }
          }
          
          console.log(`📥 Scanned ${items.length} items from ${feedUrl}`);
          
        } catch (error) {
          console.error(`Error scanning feed ${feedUrl}:`, error.message);
        }
      }
      
      console.log(`✅ Total opportunities found: ${allOpportunities.length}`);
      
      return {
        success: true,
        opportunities: allOpportunities,
      };
      
    } catch (error) {
      console.error('❌ Error scanning RSS feeds:', error.message);
      return {
        success: false,
        error: error.message,
        opportunities: [],
      };
    }
  }
  
  /**
   * Parse RSS/Atom feed
   */
  _parseFeed(xmlData, feedUrl) {
    try {
      const $ = cheerio.load(xmlData, { xmlMode: true });
      const items = [];
      
      // Try RSS format
      $('item').each((i, element) => {
        if (i >= 20) return;  // Limit to 20 items per feed
        
        const title = $(element).find('title').text().trim();
        const link = $(element).find('link').text().trim();
        const description = $(element).find('description').text().trim();
        const pubDate = $(element).find('pubDate').text().trim();
        
        if (title && link) {
          items.push({
            title,
            link,
            description,
            pubDate,
            source: feedUrl,
          });
        }
      });
      
      // Try Atom format if no items found
      if (items.length === 0) {
        $('entry').each((i, element) => {
          if (i >= 20) return;
          
          const title = $(element).find('title').text().trim();
          const link = $(element).find('link').attr('href');
          const description = $(element).find('summary').text().trim();
          const pubDate = $(element).find('published').text().trim();
          
          if (title && link) {
            items.push({
              title,
              link,
              description,
              pubDate,
              source: feedUrl,
            });
          }
        });
      }
      
      return items;
      
    } catch (error) {
      console.error('Error parsing feed:', error.message);
      return [];
    }
  }
  
  /**
   * Analyze opportunity
   */
  async _analyzeOpportunity(item) {
    try {
      const prompt = `
**Opportunity:**
Title: ${item.title}
Description: ${item.description}
Link: ${item.link}
Source: ${item.source}

**Instructions:**
Analyze this opportunity and categorize it by capital tier:
- Zero Capital: Freelance, arbitrage, consulting (no upfront investment)
- Medium Capital: Micro-SaaS acquisition ($0-$50K)
- High Capital: Enterprise B2B solutions, partnerships ($50K+)

Assess risk, ROI, time to ROI, complexity, and provide an overall score.

Return as JSON with tier, risk, roi, timeToROI, complexity, score, and analysis.`;
      
      const result = await this.opportunityAnalyzer.generateContent(prompt);
      const analysis = JSON.parse(result.response.text());
      
      return {
        ...item,
        ...analysis,
        scannedAt: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('Error analyzing opportunity:', error.message);
      return null;
    }
  }
  
  /**
   * Categorize opportunities by tier
   */
  categorizeOpportunities(opportunities) {
    const categorized = {
      zeroCapital: [],
      mediumCapital: [],
      highCapital: [],
    };
    
    for (const opportunity of opportunities) {
      const tier = opportunity.tier?.toLowerCase().replace(/\s+/g, '');
      
      if (tier === 'zerocapital' || tier === 'zero_capital') {
        categorized.zeroCapital.push(opportunity);
      } else if (tier === 'mediumcapital' || tier === 'medium_capital') {
        categorized.mediumCapital.push(opportunity);
      } else if (tier === 'highcapital' || tier === 'high_capital') {
        categorized.highCapital.push(opportunity);
      } else {
        // Default to zero capital if unclear
        categorized.zeroCapital.push(opportunity);
      }
    }
    
    // Sort by score
    categorized.zeroCapital.sort((a, b) => (b.score || 0) - (a.score || 0));
    categorized.mediumCapital.sort((a, b) => (b.score || 0) - (a.score || 0));
    categorized.highCapital.sort((a, b) => (b.score || 0) - (a.score || 0));
    
    this.opportunities = categorized;
    
    return categorized;
  }
  
  /**
   * Generate CEO Briefing
   */
  async generateCEOBriefing() {
    try {
      console.log('📊 Generating CEO Briefing...');
      
      const briefing = {
        generatedAt: new Date().toISOString(),
        summary: {},
        opportunities: {},
      };
      
      // Get top opportunity from each tier
      const topZero = this.opportunities.zeroCapital[0];
      const topMedium = this.opportunities.mediumCapital[0];
      const topHigh = this.opportunities.highCapital[0];
      
      if (topZero) {
        const briefingData = await this._generateBriefingForOpportunity(topZero, 'Zero Capital');
        briefing.opportunities.zeroCapital = briefingData;
      }
      
      if (topMedium) {
        const briefingData = await this._generateBriefingForOpportunity(topMedium, 'Medium Capital');
        briefing.opportunities.mediumCapital = briefingData;
      }
      
      if (topHigh) {
        const briefingData = await this._generateBriefingForOpportunity(topHigh, 'High Capital');
        briefing.opportunities.highCapital = briefingData;
      }
      
      // Generate summary
      briefing.summary = {
        totalOpportunities: 
          this.opportunities.zeroCapital.length +
          this.opportunities.mediumCapital.length +
          this.opportunities.highCapital.length,
        zeroCapitalCount: this.opportunities.zeroCapital.length,
        mediumCapitalCount: this.opportunities.mediumCapital.length,
        highCapitalCount: this.opportunities.highCapital.length,
        topRecommendation: this._getTopRecommendation(briefing.opportunities),
      };
      
      console.log('✅ CEO Briefing generated');
      
      return {
        success: true,
        briefing: briefing,
      };
      
    } catch (error) {
      console.error('❌ Error generating CEO Briefing:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate briefing for specific opportunity
   */
  async _generateBriefingForOpportunity(opportunity, tier) {
    try {
      const prompt = `
**Opportunity:**
Title: ${opportunity.title}
Description: ${opportunity.description}
Link: ${opportunity.link}
Tier: ${tier}
Score: ${opportunity.score}
Risk: ${opportunity.risk}
ROI: ${opportunity.roi}
Time to ROI: ${opportunity.timeToROI}

**Instructions:**
Generate a CEO briefing for this opportunity with:
- Executive summary (2-3 sentences)
- Opportunity overview
- Market analysis
- Step-by-step execution plan
- Resource requirements
- Risk assessment with mitigation
- Expected ROI
- Strategic fit
- Recommendation (go/no-go)

Keep under 300 words.

Return as JSON with all briefing sections.`;
      
      const result = await this.briefingGenerator.generateContent(prompt);
      const briefing = JSON.parse(result.response.text());
      
      return {
        opportunity: opportunity,
        briefing: briefing,
      };
      
    } catch (error) {
      console.error('Error generating briefing for opportunity:', error.message);
      return null;
    }
  }
  
  /**
   * Get top recommendation
   */
  _getTopRecommendation(opportunities) {
    const scores = [];
    
    if (opportunities.zeroCapital) {
      scores.push({ tier: 'Zero Capital', score: opportunities.zeroCapital.opportunity?.score || 0 });
    }
    if (opportunities.mediumCapital) {
      scores.push({ tier: 'Medium Capital', score: opportunities.mediumCapital.opportunity?.score || 0 });
    }
    if (opportunities.highCapital) {
      scores.push({ tier: 'High Capital', score: opportunities.highCapital.opportunity?.score || 0 });
    }
    
    scores.sort((a, b) => b.score - a.score);
    
    return scores[0]?.tier || 'No recommendations';
  }
  
  /**
   * Run weekly business radar cycle
   */
  async runWeeklyCycle() {
    try {
      console.log('🚀 Starting weekly business radar cycle...');
      
      // Scan RSS feeds
      const scanResult = await this.scanRSSFeeds();
      
      if (!scanResult.success) {
        return scanResult;
      }
      
      // Categorize opportunities
      const categorized = this.categorizeOpportunities(scanResult.opportunities);
      
      console.log(`📊 Categorized opportunities:`);
      console.log(`  Zero Capital: ${categorized.zeroCapital.length}`);
      console.log(`  Medium Capital: ${categorized.mediumCapital.length}`);
      console.log(`  High Capital: ${categorized.highCapital.length}`);
      
      // Generate CEO Briefing
      const briefingResult = await this.generateCEOBriefing();
      
      return {
        success: true,
        opportunities: categorized,
        briefing: briefingResult.briefing,
      };
      
    } catch (error) {
      console.error('❌ Error in weekly cycle:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get current opportunities
   */
  getOpportunities() {
    return this.opportunities;
  }
  
  /**
   * Get statistics
   */
  getStats() {
    return {
      zeroCapitalCount: this.opportunities.zeroCapital.length,
      mediumCapitalCount: this.opportunities.mediumCapital.length,
      highCapitalCount: this.opportunities.highCapital.length,
      totalOpportunities: 
        this.opportunities.zeroCapital.length +
        this.opportunities.mediumCapital.length +
        this.opportunities.highCapital.length,
      lastScan: new Date().toISOString(),
    };
  }
}

// Singleton instance
let businessRadar = null;

function getBusinessRadar(config = null) {
  if (!businessRadar) {
    if (config === null) {
      config = {};
    }
    businessRadar = new BusinessRadar(config);
  }
  return businessRadar;
}

module.exports = { BusinessRadar, getBusinessRadar };

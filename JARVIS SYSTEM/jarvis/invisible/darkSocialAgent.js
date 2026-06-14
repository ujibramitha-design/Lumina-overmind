/**
 * JARVIS Dark Social Community Infiltrator
 * ======================================
 * 
 * Discord and Reddit agent for high-value networking
 * with conversational, non-salesy replies and human-like behavior.
 */

const Discord = require('discord.js');
const snoowrap = require('snoowrap');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class DarkSocialAgent {
  constructor(config = {}) {
    this.config = {
      discord: {
        enabled: config.discordEnabled !== false,
        token: config.discordToken || process.env.DISCORD_BOT_TOKEN,
        channels: config.discordChannels || [],
      },
      reddit: {
        enabled: config.redditEnabled !== false,
        clientId: config.redditClientId || process.env.REDDIT_CLIENT_ID,
        clientSecret: config.redditClientSecret || process.env.REDDIT_CLIENT_SECRET,
        userAgent: config.redditUserAgent || 'JARVIS-DarkSocial/1.0',
        subreddits: config.subreddits || [],
      },
      keywords: config.keywords || [
        'need a developer',
        'server architecture',
        'looking for help',
        'need assistance',
        'hiring developer',
        'freelance developer',
        'web development',
        'api integration',
        'automation',
        'scraping',
      ],
      rateLimiting: {
        discord: {
          maxReplies: config.discordMaxReplies || 10,
          minDelay: config.discordMinDelay || 30000,  // 30 seconds
          maxDelay: config.discordMaxDelay || 120000,  // 2 minutes
        },
        reddit: {
          maxReplies: config.redditMaxReplies || 5,
          minDelay: config.redditMinDelay || 60000,  // 1 minute
          maxDelay: config.redditMaxDelay || 300000,  // 5 minutes
        },
      },
      funnel: {
        targetUrl: config.targetUrl || 'https://devproflow.com',
        directContact: config.directContact || 'contact@devproflow.com',
      },
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.replyGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      systemInstruction: this._getReplyGeneratorPrompt(),
    });
    
    this.discordClient = null;
    this.redditClient = null;
    
    this.discordReplyCount = 0;
    this.redditReplyCount = 0;
    this.lastDiscordReply = null;
    this.lastRedditReply = null;
    
    this._initializeClients();
  }
  
  /**
   * Reply generator system prompt
   */
  _getReplyGeneratorPrompt() {
    return `You are an expert community member who provides helpful, genuine advice without being salesy.

**Your Role:**
- Generate conversational, human-like replies
- Provide genuine value and helpful insights
- Be authentic and build trust
- Subtly mention expertise when relevant
- Never use sales language or CTAs
- Focus on helping, not selling

**Reply Guidelines:**
- Keep under 200 words
- Be conversational and friendly
- Provide specific, actionable advice
- Share personal experience when relevant
- Avoid generic responses
- Sound like a real person
- Use appropriate emojis sparingly
- Match the tone of the original post

**Subtle Funneling:**
- Only mention expertise if directly relevant
- Never include links or contact info in replies
- Build credibility through helpfulness
- Let them ask for more info naturally

**Output Format:**
Return JSON with:
- reply: the conversational reply
- confidence: relevance confidence (0-1)
- shouldReply: whether to reply (boolean)`;
  }
  
  /**
   * Initialize clients
   */
  _initializeClients() {
    try {
      // Initialize Discord client
      if (this.config.discord.enabled && this.config.discord.token) {
        this.discordClient = new Discord.Client({
          intents: [
            Discord.GatewayIntentBits.Guilds,
            Discord.GatewayIntentBits.GuildMessages,
            Discord.GatewayIntentBits.MessageContent,
          ],
        });
        
        this.discordClient.on('ready', () => {
          console.log('✅ Discord client ready');
        });
        
        this.discordClient.on('messageCreate', (message) => {
          this._handleDiscordMessage(message);
        });
        
        console.log('✅ Discord client initialized');
      }
      
      // Initialize Reddit client
      if (this.config.reddit.enabled && this.config.reddit.clientId) {
        this.redditClient = new snoowrap({
          userAgent: this.config.reddit.userAgent,
          clientId: this.config.reddit.clientId,
          clientSecret: this.config.reddit.clientSecret,
        });
        
        console.log('✅ Reddit client initialized');
      }
      
    } catch (error) {
      console.error('❌ Error initializing clients:', error.message);
    }
  }
  
  /**
   * Start Discord bot
   */
  async startDiscord() {
    try {
      if (!this.discordClient) {
        return {
          success: false,
          error: 'Discord client not initialized',
        };
      }
      
      await this.discordClient.login(this.config.discord.token);
      
      return {
        success: true,
        message: 'Discord bot started',
      };
      
    } catch (error) {
      console.error('❌ Error starting Discord bot:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Handle Discord message
   */
  async _handleDiscordMessage(message) {
    try {
      // Ignore bot messages
      if (message.author.bot) {
        return;
      }
      
      // Check if message contains keywords
      const content = message.content.toLowerCase();
      const matchedKeyword = this.config.keywords.find(keyword => 
        content.includes(keyword.toLowerCase())
      );
      
      if (!matchedKeyword) {
        return;
      }
      
      // Check rate limiting
      if (this.discordReplyCount >= this.config.rateLimiting.discord.maxReplies) {
        console.log('⚠️ Discord reply limit reached');
        return;
      }
      
      if (this.lastDiscordReply) {
        const timeSinceLastReply = Date.now() - this.lastDiscordReply;
        if (timeSinceLastReply < this.config.rateLimiting.discord.minDelay) {
          console.log('⏸️ Discord rate limit: waiting');
          return;
        }
      }
      
      // Generate reply
      const reply = await this._generateReply(message.content, matchedKeyword, 'discord');
      
      if (!reply.success || !reply.shouldReply) {
        return;
      }
      
      // Add human jitter
      const jitter = this._getHumanJitter('discord');
      await new Promise(resolve => setTimeout(resolve, jitter));
      
      // Send reply
      await message.reply(reply.reply);
      
      this.discordReplyCount++;
      this.lastDiscordReply = Date.now();
      
      console.log(`💬 Discord reply sent to ${message.author.username}`);
      
    } catch (error) {
      console.error('Error handling Discord message:', error.message);
    }
  }
  
  /**
   * Start Reddit monitoring
   */
  async startReddit() {
    try {
      if (!this.redditClient) {
        return {
          success: false,
          error: 'Reddit client not initialized',
        };
      }
      
      // Start monitoring subreddits
      for (const subreddit of this.config.reddit.subreddits) {
        this._monitorSubreddit(subreddit);
      }
      
      return {
        success: true,
        message: 'Reddit monitoring started',
      };
      
    } catch (error) {
      console.error('❌ Error starting Reddit monitoring:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Monitor subreddit
   */
  async _monitorSubreddit(subredditName) {
    try {
      console.log(`📡 Monitoring subreddit: ${subredditName}`);
      
      const subreddit = this.redditClient.getSubreddit(subredditName);
      
      // Stream new posts
      const stream = subreddit.getNew({ limit: 10 });
      
      for await (const post of stream) {
        await this._handleRedditPost(post, subredditName);
      }
      
    } catch (error) {
      console.error(`Error monitoring subreddit ${subredditName}:`, error.message);
    }
  }
  
  /**
   * Handle Reddit post
   */
  async _handleRedditPost(post, subredditName) {
    try {
      // Check if post contains keywords
      const content = `${post.title} ${post.selftext}`.toLowerCase();
      const matchedKeyword = this.config.keywords.find(keyword => 
        content.includes(keyword.toLowerCase())
      );
      
      if (!matchedKeyword) {
        return;
      }
      
      // Check rate limiting
      if (this.redditReplyCount >= this.config.rateLimiting.reddit.maxReplies) {
        console.log('⚠️ Reddit reply limit reached');
        return;
      }
      
      if (this.lastRedditReply) {
        const timeSinceLastReply = Date.now() - this.lastRedditReply;
        if (timeSinceLastReply < this.config.rateLimiting.reddit.minDelay) {
          console.log('⏸️ Reddit rate limit: waiting');
          return;
        }
      }
      
      // Generate reply
      const reply = await this._generateReply(
        `${post.title}\n\n${post.selftext}`,
        matchedKeyword,
        'reddit'
      );
      
      if (!reply.success || !reply.shouldReply) {
        return;
      }
      
      // Add human jitter
      const jitter = this._getHumanJitter('reddit');
      await new Promise(resolve => setTimeout(resolve, jitter));
      
      // Send reply
      await post.reply(reply.reply);
      
      this.redditReplyCount++;
      this.lastRedditReply = Date.now();
      
      console.log(`💬 Reddit reply sent to r/${subredditName}`);
      
    } catch (error) {
      console.error('Error handling Reddit post:', error.message);
    }
  }
  
  /**
   * Generate reply
   */
  async _generateReply(content, keyword, platform) {
    try {
      const prompt = `
**Platform:** ${platform}
**Content:** ${content}
**Matched Keyword:** ${keyword}

**Instructions:**
Generate a conversational, human-like reply:
- Provide genuine value and helpful advice
- Be conversational and friendly
- Keep under 200 words
- Avoid sales language or CTAs
- Sound like a real person
- Match the tone of the original post
- Only mention expertise if directly relevant
- Never include links or contact info

Return as JSON with reply, confidence, and shouldReply.`;
      
      const result = await this.replyGenerator.generateContent(prompt);
      const replyData = JSON.parse(result.response.text());
      
      return {
        success: true,
        reply: replyData.reply,
        confidence: replyData.confidence || 0.7,
        shouldReply: replyData.shouldReply !== false,
      };
      
    } catch (error) {
      console.error('Error generating reply:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get human jitter (randomized delay)
   */
  _getHumanJitter(platform) {
    const config = this.config.rateLimiting[platform];
    const minDelay = config.minDelay;
    const maxDelay = config.maxDelay;
    
    // Add random jitter: ±20% of the delay
    const baseDelay = Math.random() * (maxDelay - minDelay) + minDelay;
    const jitter = baseDelay * (0.8 + Math.random() * 0.4);  // 80-120% of base
    
    return Math.floor(jitter);
  }
  
  /**
   * Reset daily counters
   */
  resetDailyCounters() {
    this.discordReplyCount = 0;
    this.redditReplyCount = 0;
    this.lastDiscordReply = null;
    this.lastRedditReply = null;
    console.log('🔄 Daily counters reset');
  }
  
  /**
   * Get statistics
   */
  getStats() {
    return {
      discord: {
        replyCount: this.discordReplyCount,
        maxReplies: this.config.rateLimiting.discord.maxReplies,
        remaining: this.config.rateLimiting.discord.maxReplies - this.discordReplyCount,
        lastReply: this.lastDiscordReply,
      },
      reddit: {
        replyCount: this.redditReplyCount,
        maxReplies: this.config.rateLimiting.reddit.maxReplies,
        remaining: this.config.rateLimiting.reddit.maxReplies - this.redditReplyCount,
        lastReply: this.lastRedditReply,
      },
    };
  }
  
  /**
   * Stop clients
   */
  async stop() {
    try {
      if (this.discordClient) {
        await this.discordClient.destroy();
        console.log('✅ Discord client stopped');
      }
      
      if (this.redditClient) {
        // Reddit client doesn't have a destroy method
        console.log('✅ Reddit client stopped');
      }
      
      return {
        success: true,
        message: 'All clients stopped',
      };
      
    } catch (error) {
      console.error('Error stopping clients:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
}

// Singleton instance
let darkSocialAgent = null;

function getDarkSocialAgent(config = null) {
  if (!darkSocialAgent) {
    if (config === null) {
      config = {};
    }
    darkSocialAgent = new DarkSocialAgent(config);
  }
  return darkSocialAgent;
}

module.exports = { DarkSocialAgent, getDarkSocialAgent };

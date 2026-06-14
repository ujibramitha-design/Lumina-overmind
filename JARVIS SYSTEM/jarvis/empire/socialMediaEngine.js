/**
 * JARVIS Autonomous Social Media Engine (The Viral Machine)
 * ========================================================
 * 
 * Automated social media management system for organic growth.
 * Handles trending research, viral post generation, and engagement.
 */

const { TwitterApi } = require('twitter-api-v2');
const axios = require('axios');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class SocialMediaEngine {
  constructor(config = {}) {
    this.config = {
      twitter: {
        enabled: config.twitterEnabled !== false,
        apiKey: config.twitterApiKey || process.env.TWITTER_API_KEY,
        apiSecret: config.twitterApiSecret || process.env.TWITTER_API_SECRET,
        accessToken: config.twitterAccessToken || process.env.TWITTER_ACCESS_TOKEN,
        accessSecret: config.twitterAccessSecret || process.env.TWITTER_ACCESS_SECRET,
        bearerToken: config.twitterBearerToken || process.env.TWITTER_BEARER_TOKEN,
      },
      instagram: {
        enabled: config.instagramEnabled !== false,
        accessToken: config.instagramAccessToken || process.env.INSTAGRAM_ACCESS_TOKEN,
        userId: config.instagramUserId || process.env.INSTAGRAM_USER_ID,
      },
      posting: {
        dailyLimit: config.dailyLimit || 3,
        minInterval: config.minInterval || 3600000,  // 1 hour
        maxInterval: config.maxInterval || 7200000,  // 2 hours
      },
      engagement: {
        autoReply: config.autoReply !== false,
        replyDelay: config.replyDelay || 300000,  // 5 minutes
        dailyReplyLimit: config.dailyReplyLimit || 20,
      },
      topics: config.topics || [
        'AI automation', 'web scraping', 'Python development',
        'tech trends', 'business automation', 'productivity hacks',
      ],
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.topicResearcher = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getTopicResearcherPrompt(),
    });
    
    this.postGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getPostGeneratorPrompt(),
    });
    
    this.replyGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      systemInstruction: this._getReplyGeneratorPrompt(),
    });
    
    this.twitterClient = null;
    this.instagramClient = null;
    
    this.dailyPostCount = 0;
    this.dailyReplyCount = 0;
    this.lastResetDate = new Date().toDateString();
    this.lastPostTime = null;
    
    this._initializeClients();
  }
  
  /**
   * Topic researcher system prompt
   */
  _getTopicResearcherPrompt() {
    return `You are a trend researcher specializing in tech and business topics.

**Your Role:**
- Research trending topics in tech and business
- Identify viral-worthy content opportunities
- Find angles that resonate with target audience
- Provide context and supporting information

**Research Areas:**
- AI and automation trends
- Web scraping and data extraction
- Python development
- Business automation
- Productivity hacks
- Tech industry news

**Output Format:**
Return JSON with:
- topic: main topic
- trend: why it's trending
- angle: unique angle for content
- context: supporting information
- hashtags: relevant hashtags`;
  }
  
  /**
   * Post generator system prompt
   */
  _getPostGeneratorPrompt() {
    return `You are a viral social media content creator specializing in tech and business.

**Your Role:**
- Write viral-optimized social media posts
- Apply AIDA/PAS frameworks for engagement
- Use power words and emotional triggers
- Create compelling hooks and CTAs
- Optimize for platform-specific algorithms

**Frameworks:**
- AIDA: Attention, Interest, Desire, Action
- PAS: Problem, Agitation, Solution

**Post Structure:**
1. Viral hook (first line)
2. Value proposition
3. Supporting evidence
4. Clear call-to-action
5. Relevant hashtags

**Guidelines:**
- Keep posts under 280 characters (Twitter)
- Use emojis strategically
- Include power words
- Create curiosity
- Add clear CTA
- Use 3-5 relevant hashtags

**Output Format:**
Return JSON with:
- post: the social media post text
- confidence: viral potential confidence (0-1)
- hashtags: array of hashtags`;
  }
  
  /**
   * Reply generator system prompt
   */
  _getReplyGeneratorPrompt() {
    return `You are a friendly, engaging social media manager.

**Your Role:**
- Write human-like replies to comments
- Build engagement and community
- Be helpful and authentic
- Match the tone of the original comment

**Reply Guidelines:**
- Keep replies under 140 characters
- Be friendly and conversational
- Add value to the conversation
- Use appropriate emojis
- Avoid generic responses
- Be authentic and genuine

**Output Format:**
Return JSON with:
- reply: the reply text
- confidence: engagement confidence (0-1)`;
  }
  
  /**
   * Initialize API clients
   */
  _initializeClients() {
    try {
      // Initialize Twitter client
      if (this.config.twitter.enabled && this.config.twitter.bearerToken) {
        this.twitterClient = new TwitterApi(this.config.twitter.bearerToken);
        console.log('✅ Twitter client initialized');
      }
      
      // Instagram client would be initialized here
      // Note: Instagram Graph API requires additional setup
      if (this.config.instagram.enabled) {
        console.log('✅ Instagram client configuration loaded');
      }
      
    } catch (error) {
      console.error('❌ Error initializing clients:', error.message);
    }
  }
  
  /**
   * Research trending topic
   */
  async researchTrendingTopic() {
    try {
      console.log('🔍 Researching trending topic...');
      
      const randomTopic = this.config.topics[Math.floor(Math.random() * this.config.topics.length)];
      
      const prompt = `
**Topic:** ${randomTopic}

**Instructions:**
Research this topic and identify:
- Why it's currently trending
- Unique angle for viral content
- Supporting context
- Relevant hashtags

Return as JSON with topic, trend, angle, context, and hashtags.`;
      
      const result = await this.topicResearcher.generateContent(prompt);
      const research = JSON.parse(result.response.text());
      
      console.log(`✅ Researched topic: ${research.topic}`);
      
      return {
        success: true,
        topic: research.topic,
        trend: research.trend,
        angle: research.angle,
        context: research.context,
        hashtags: research.hashtags,
      };
      
    } catch (error) {
      console.error('❌ Error researching topic:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate viral post
   */
  async generateViralPost(research) {
    try {
      console.log('📝 Generating viral post...');
      
      const prompt = `
**Topic:** ${research.topic}
**Trend:** ${research.trend}
**Angle:** ${research.angle}
**Context:** ${research.context}
**Hashtags:** ${research.hashtags.join(', ')}

**Instructions:**
Generate a viral-optimized social media post using the AIDA framework.
- Create a compelling hook
- Provide value proposition
- Include clear call-to-action
- Keep under 280 characters
- Use emojis strategically
- Include 3-5 relevant hashtags

Return as JSON with post, confidence, and hashtags.`;
      
      const result = await this.postGenerator.generateContent(prompt);
      const postData = JSON.parse(result.response.text());
      
      console.log(`✅ Generated post (confidence: ${(postData.confidence * 100).toFixed(0)}%)`);
      
      return {
        success: true,
        post: postData.post,
        confidence: postData.confidence || 0.7,
        hashtags: postData.hashtags || research.hashtags,
      };
      
    } catch (error) {
      console.error('❌ Error generating post:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Post to Twitter
   */
  async postToTwitter(post) {
    try {
      if (!this.twitterClient) {
        return {
          success: false,
          error: 'Twitter client not initialized',
        };
      }
      
      console.log('🐦 Posting to Twitter...');
      
      const tweet = await this.twitterClient.v2.tweet(post);
      
      console.log(`✅ Tweet posted: ${tweet.data.id}`);
      
      return {
        success: true,
        tweetId: tweet.data.id,
        platform: 'twitter',
      };
      
    } catch (error) {
      console.error('❌ Error posting to Twitter:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Post to Instagram
   */
  async postToInstagram(post, image = null) {
    try {
      // Instagram Graph API integration
      // This would require additional setup and authentication
      console.log('📸 Instagram posting requires Graph API setup');
      
      return {
        success: false,
        error: 'Instagram Graph API requires additional setup',
      };
      
    } catch (error) {
      console.error('❌ Error posting to Instagram:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate reply to comment
   */
  async generateReply(comment) {
    try {
      console.log('💬 Generating reply...');
      
      const prompt = `
**Comment:** ${comment.text}
**Author:** ${comment.author}

**Instructions:**
Generate a friendly, human-like reply to this comment.
- Keep under 140 characters
- Be helpful and conversational
- Add value to the conversation
- Use appropriate emojis
- Be authentic and genuine

Return as JSON with reply and confidence.`;
      
      const result = await this.replyGenerator.generateContent(prompt);
      const replyData = JSON.parse(result.response.text());
      
      return {
        success: true,
        reply: replyData.reply,
        confidence: replyData.confidence || 0.7,
      };
      
    } catch (error) {
      console.error('❌ Error generating reply:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Reply to comment on Twitter
   */
  async replyToTwitterComment(tweetId, reply) {
    try {
      if (!this.twitterClient) {
        return {
          success: false,
          error: 'Twitter client not initialized',
        };
      }
      
      console.log('💬 Replying to comment...');
      
      const tweet = await this.twitterClient.v2.reply(reply, tweetId);
      
      console.log(`✅ Reply posted: ${tweet.data.id}`);
      
      return {
        success: true,
        replyId: tweet.data.id,
      };
      
    } catch (error) {
      console.error('❌ Error replying to comment:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Fetch recent comments from Twitter
   */
  async fetchTwitterComments(tweetId) {
    try {
      if (!this.twitterClient) {
        return {
          success: false,
          error: 'Twitter client not initialized',
        };
      }
      
      console.log('📥 Fetching comments...');
      
      const tweets = await this.twitterClient.v2.search(`conversation_id:${tweetId}`, {
        max_results: 10,
      });
      
      const comments = tweets.data.data.map(tweet => ({
        id: tweet.id,
        text: tweet.text,
        author: tweet.author_id,
      }));
      
      console.log(`✅ Fetched ${comments.length} comments`);
      
      return {
        success: true,
        comments: comments,
      };
      
    } catch (error) {
      console.error('❌ Error fetching comments:', error.message);
      return {
        success: false,
        error: error.message,
        comments: [],
      };
    }
  }
  
  /**
   * Run social media posting cycle
   */
  async runPostingCycle() {
    try {
      console.log('🚀 Starting social media posting cycle...');
      
      // Reset daily counter if needed
      if (this.lastResetDate !== new Date().toDateString()) {
        this.dailyPostCount = 0;
        this.dailyReplyCount = 0;
        this.lastResetDate = new Date().toDateString();
        console.log('🔄 Daily counters reset');
      }
      
      // Check daily limit
      if (this.dailyPostCount >= this.config.posting.dailyLimit) {
        console.log('⚠️ Daily posting limit reached');
        return {
          success: true,
          message: 'Daily posting limit reached',
        };
      }
      
      // Check interval since last post
      if (this.lastPostTime) {
        const timeSinceLastPost = Date.now() - this.lastPostTime;
        if (timeSinceLastPost < this.config.posting.minInterval) {
          console.log('⏸️ Minimum interval not reached');
          return {
            success: true,
            message: 'Minimum interval not reached',
          };
        }
      }
      
      // Research trending topic
      const research = await this.researchTrendingTopic();
      if (!research.success) {
        return research;
      }
      
      // Generate viral post
      const post = await this.generateViralPost(research);
      if (!post.success) {
        return post;
      }
      
      // Post to Twitter
      const twitterResult = await this.postToTwitter(post.post);
      
      if (twitterResult.success) {
        this.dailyPostCount++;
        this.lastPostTime = Date.now();
        
        // Schedule comment replies
        if (this.config.engagement.autoReply) {
          setTimeout(() => {
            this.runEngagementCycle(twitterResult.tweetId);
          }, this.config.engagement.replyDelay);
        }
      }
      
      return {
        success: twitterResult.success,
        platform: 'twitter',
        tweetId: twitterResult.tweetId,
        post: post.post,
        confidence: post.confidence,
      };
      
    } catch (error) {
      console.error('❌ Error in posting cycle:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Run engagement cycle (reply to comments)
   */
  async runEngagementCycle(tweetId) {
    try {
      console.log('💬 Starting engagement cycle...');
      
      // Reset daily counter if needed
      if (this.lastResetDate !== new Date().toDateString()) {
        this.dailyReplyCount = 0;
        this.lastResetDate = new Date().toDateString();
      }
      
      // Check daily limit
      if (this.dailyReplyCount >= this.config.engagement.dailyReplyLimit) {
        console.log('⚠️ Daily reply limit reached');
        return {
          success: true,
          message: 'Daily reply limit reached',
        };
      }
      
      // Fetch comments
      const commentsResult = await this.fetchTwitterComments(tweetId);
      if (!commentsResult.success) {
        return commentsResult;
      }
      
      // Reply to comments
      const results = [];
      for (const comment of commentsResult.comments) {
        if (this.dailyReplyCount >= this.config.engagement.dailyReplyLimit) {
          break;
        }
        
        // Generate reply
        const reply = await this.generateReply(comment);
        if (!reply.success) {
          continue;
        }
        
        // Post reply
        const replyResult = await this.replyToTwitterComment(comment.id, reply.reply);
        
        if (replyResult.success) {
          this.dailyReplyCount++;
          results.push({
            commentId: comment.id,
            replyId: replyResult.replyId,
          });
        }
        
        // Small delay between replies
        await new Promise(resolve => setTimeout(resolve, 30000));  // 30 seconds
      }
      
      console.log(`✅ Engagement cycle complete: ${results.length} replies sent`);
      
      return {
        success: true,
        repliesSent: results.length,
        results: results,
      };
      
    } catch (error) {
      console.error('❌ Error in engagement cycle:', error.message);
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
      dailyPostCount: this.dailyPostCount,
      dailyReplyCount: this.dailyReplyCount,
      dailyPostLimit: this.config.posting.dailyLimit,
      dailyReplyLimit: this.config.engagement.dailyReplyLimit,
      lastResetDate: this.lastResetDate,
      lastPostTime: this.lastPostTime,
      remainingPosts: this.config.posting.dailyLimit - this.dailyPostCount,
      remainingReplies: this.config.engagement.dailyReplyLimit - this.dailyReplyCount,
    };
  }
  
  /**
   * Reset daily counters
   */
  resetDailyCounters() {
    this.dailyPostCount = 0;
    this.dailyReplyCount = 0;
    this.lastResetDate = new Date().toDateString();
    console.log('🔄 Daily counters reset');
  }
}

// Singleton instance
let socialMediaEngine = null;

function getSocialMediaEngine(config = null) {
  if (!socialMediaEngine) {
    if (config === null) {
      config = {};
    }
    socialMediaEngine = new SocialMediaEngine(config);
  }
  return socialMediaEngine;
}

module.exports = { SocialMediaEngine, getSocialMediaEngine };

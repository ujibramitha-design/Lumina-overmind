"""
JARVIS Spontaneity Module
========================

Background job that autonomously initiates conversations based on:
- Tech news RSS feeds
- GitHub trending repositories
- User inactivity (12+ hours)

This makes JARVIS feel more human and proactive.
"""

import asyncio
import logging
import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpontaneityModule:
    """
    Spontaneity module for autonomous conversation initiation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Inactivity threshold (hours)
        self.inactivity_threshold = config.get('inactivity_threshold', 12)
        
        # RSS feeds for tech news
        self.rss_feeds = config.get('rss_feeds', [
            'https://techcrunch.com/feed/',
            'https://www.theverge.com/rss/index.xml',
            'https://feeds.feedburner.com/oreilly/radar',
        ])
        
        # GitHub trending configuration
        self.github_trending_enabled = config.get('github_trending_enabled', True)
        self.github_languages = config.get('github_languages', ['javascript', 'python', 'typescript'])
        
        # Relevance keywords for Lumina Overmind stack
        self.relevance_keywords = config.get('relevance_keywords', [
            'react', 'nextjs', 'python', 'fastapi', 'ai', 'machine learning',
            'docker', 'kubernetes', 'websocket', 'telegram', 'whatsapp',
            'gemini', 'openai', 'llm', 'chatbot', 'automation',
        ])
        
        # User interaction tracking
        self.last_interaction_time: Dict[str, datetime] = {}
        
        # Statistics
        self.stats = {
            'spontaneous_messages_sent': 0,
            'news_items_analyzed': 0,
            'github_items_analyzed': 0,
            'relevance_rate': 0.0,
        }
    
    async def check_and_send_spontaneous_message(self, user_id: str, user_phone: str = None):
        """
        Check if user has been inactive and send spontaneous message if appropriate.
        """
        try:
            # Check inactivity
            last_interaction = self.last_interaction_time.get(user_id)
            
            if last_interaction:
                time_since_interaction = datetime.utcnow() - last_interaction
                hours_inactive = time_since_interaction.total_seconds() / 3600
                
                if hours_inactive < self.inactivity_threshold:
                    logger.info(f"User {user_id} active {hours_inactive:.1f}h ago, skipping spontaneity")
                    return
            else:
                # First interaction, set current time
                self.last_interaction_time[user_id] = datetime.utcnow()
                return
            
            # Fetch and analyze content
            relevant_content = await self._fetch_relevant_content()
            
            if not relevant_content:
                logger.info("No relevant content found for spontaneous message")
                return
            
            # Generate spontaneous message
            message = await self._generate_spontaneous_message(relevant_content)
            
            if message:
                # Send message
                await self._send_spontaneous_message(user_id, user_phone, message)
                
                # Update statistics
                self.stats['spontaneous_messages_sent'] += 1
                
                logger.info(f"✅ Spontaneous message sent to {user_id}")
        
        except Exception as e:
            logger.error(f"❌ Error in spontaneous message check: {e}")
    
    def update_last_interaction(self, user_id: str):
        """
        Update the last interaction time for a user.
        """
        self.last_interaction_time[user_id] = datetime.utcnow()
        logger.debug(f"Updated last interaction for {user_id}")
    
    async def _fetch_relevant_content(self) -> Optional[Dict[str, Any]]:
        """
        Fetch relevant content from RSS feeds and GitHub trending.
        """
        try:
            # Fetch RSS news
            news_items = await self._fetch_rss_news()
            self.stats['news_items_analyzed'] += len(news_items)
            
            # Fetch GitHub trending
            github_items = []
            if self.github_trending_enabled:
                github_items = await self._fetch_github_trending()
                self.stats['github_items_analyzed'] += len(github_items)
            
            # Filter for relevance
            relevant_news = self._filter_relevant_content(news_items)
            relevant_github = self._filter_relevant_content(github_items)
            
            # Select most relevant item
            all_relevant = relevant_news + relevant_github
            
            if not all_relevant:
                return None
            
            # Sort by relevance score
            all_relevant.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Return top item
            return all_relevant[0]
        
        except Exception as e:
            logger.error(f"Error fetching relevant content: {e}")
            return None
    
    async def _fetch_rss_news(self) -> List[Dict[str, Any]]:
        """
        Fetch news from RSS feeds.
        """
        news_items = []
        
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:  # Limit to 10 items per feed
                    news_items.append({
                        'type': 'news',
                        'title': entry.get('title', ''),
                        'description': entry.get('description', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'source': feed.get('feed', {}).get('title', 'Unknown'),
                    })
            
            except Exception as e:
                logger.error(f"Error fetching RSS feed {feed_url}: {e}")
        
        return news_items
    
    async def _fetch_github_trending(self) -> List[Dict[str, Any]]:
        """
        Fetch trending repositories from GitHub.
        """
        try:
            trending_items = []
            
            for language in self.github_languages:
                try:
                    # GitHub trending API (unofficial)
                    url = f"https://github.com/trending/{language}?since=daily"
                    
                    # Note: This is a simplified version
                    # In production, use a proper GitHub API or scraping library
                    response = requests.get(url, headers={'User-Agent': 'JARVIS'})
                    
                    if response.status_code == 200:
                        # Parse HTML to extract trending repos
                        # This is a placeholder - implement proper parsing
                        trending_items.append({
                            'type': 'github',
                            'title': f'Trending {language} repository',
                            'description': 'Check out the trending repositories on GitHub',
                            'link': url,
                            'language': language,
                        })
                
                except Exception as e:
                    logger.error(f"Error fetching GitHub trending for {language}: {e}")
            
            return trending_items
        
        except Exception as e:
            logger.error(f"Error fetching GitHub trending: {e}")
            return []
    
    def _filter_relevant_content(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter content for relevance to Lumina Overmind stack.
        """
        relevant_items = []
        
        for item in items:
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(item)
            
            if relevance_score > 0.3:  # Minimum relevance threshold
                item['relevance_score'] = relevance_score
                relevant_items.append(item)
        
        # Update relevance rate
        if items:
            self.stats['relevance_rate'] = len(relevant_items) / len(items)
        
        return relevant_items
    
    def _calculate_relevance_score(self, item: Dict[str, Any]) -> float:
        """
        Calculate relevance score for an item.
        """
        score = 0.0
        
        # Combine title and description for analysis
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        
        # Check for relevance keywords
        for keyword in self.relevance_keywords:
            if keyword.lower() in text:
                score += 0.2
        
        # Cap score at 1.0
        return min(score, 1.0)
    
    async def _generate_spontaneous_message(self, content: Dict[str, Any]) -> Optional[str]:
        """
        Generate a spontaneous message based on relevant content.
        """
        try:
            # Import Gemini service
            import sys
            sys.path.append('./jarvis/channels')
            from services.geminiService import getGeminiService
            
            gemini_service = getGeminiService()
            
            # Build prompt for spontaneous message
            prompt = self._build_spontaneity_prompt(content)
            
            # Generate message using Gemini
            result = await gemini_service.performAnalysis(
                'spontaneity',
                content,
                'spontaneous_message',
                {
                    'message_type': 'casual_conversation_starter',
                    'tone': 'friendly',
                    'context': 'proactive tech news sharing',
                }
            )
            
            if result.success:
                return result.response
            else:
                # Fallback to simple message
                return self._generate_fallback_message(content)
        
        except Exception as e:
            logger.error(f"Error generating spontaneous message: {e}")
            return self._generate_fallback_message(content)
    
    def _build_spontaneity_prompt(self, content: Dict[str, Any]) -> str:
        """
        Build prompt for spontaneous message generation.
        """
        content_type = content.get('type', 'news')
        
        if content_type == 'news':
            return f"""
Generate a casual, friendly message to share this tech news with the user:

**Title:** {content.get('title', '')}
**Description:** {content.get('description', '')}
**Source:** {content.get('source', '')}
**Link:** {content.get('link', '')}

**Guidelines:**
- Start with a casual opener (e.g., "Hey!", "Saw this and thought of you")
- Explain why it's relevant to our stack
- Keep it conversational and brief
- End with a question to encourage response
- Use appropriate emojis sparingly
- Sound like a friendly colleague sharing interesting news
"""
        else:
            return f"""
Generate a casual, friendly message to share this GitHub trending item:

**Title:** {content.get('title', '')}
**Description:** {content.get('description', '')}
**Language:** {content.get('language', '')}
**Link:** {content.get('link', '')}

**Guidelines:**
- Start with a casual opener
- Explain why this might be interesting for our project
- Keep it conversational and brief
- End with a question to encourage response
- Use appropriate emojis sparingly
- Sound like a friendly colleague sharing tech news
"""
    
    def _generate_fallback_message(self, content: Dict[str, Any]) -> str:
        """
        Generate a fallback spontaneous message.
        """
        content_type = content.get('type', 'news')
        
        if content_type == 'news':
            return f"Hey! Saw this and thought it might be relevant to our stack: {content.get('title', '')}. What do you think? 🤔"
        else:
            return f"Hey! Check out this trending {content.get('language', '')} repo on GitHub. Might be useful for our project! 🚀"
    
    async def _send_spontaneous_message(self, user_id: str, user_phone: str, message: str):
        """
        Send spontaneous message to user.
        """
        try:
            # Import communication hub
            import sys
            sys.path.append('./jarvis/channels')
            from hub import JarvisCommunicationHub
            
            hub = JarvisCommunicationHub()
            
            # Send via WhatsApp if phone number available
            if user_phone:
                await hub.whatsapp.sendMessage(user_phone, message)
                logger.info(f"📱 Spontaneous message sent via WhatsApp to {user_phone}")
            else:
                # Fallback to Telegram if available
                # This would require user's Telegram ID
                logger.warning("No phone number available for spontaneous message")
        
        except Exception as e:
            logger.error(f"Error sending spontaneous message: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get spontaneity module statistics.
        """
        return {
            'spontaneous_messages_sent': self.stats['spontaneous_messages_sent'],
            'news_items_analyzed': self.stats['news_items_analyzed'],
            'github_items_analyzed': self.stats['github_items_analyzed'],
            'relevance_rate': self.stats['relevance_rate'],
            'active_users': len(self.last_interaction_time),
        }

# Singleton instance
spontaneity_module: Optional[SpontaneityModule] = None

def get_spontaneity_module(config: Dict[str, Any] = None) -> SpontaneityModule:
    """Get or create spontaneity module singleton"""
    global spontaneity_module
    
    if spontaneity_module is None:
        if config is None:
            config = {}
        spontaneity_module = SpontaneityModule(config)
    
    return spontaneity_module

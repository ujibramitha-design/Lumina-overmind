"""
Industry Insider - Macro Analyst Module
Sistem untuk memantau berita industri dan kebijakan asosiasi properti
"""

import json
import requests
import feedparser
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IndustryInsider:
    """
    Macro Analyst untuk memantau berita industri dan kebijakan properti
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'industry_insider.db (SQLite - removed))
        
        # RSS Feed configurations
        self.news_sources = {
            'kompas_properti': {
                'url': 'https://properti.kompas.com/feed',
                'name': 'Kompas Properti',
                'category': 'property_news'
            },
            'bisnis_properti': {
                'url': 'https://ekonomi.bisnis.com/properti/feed',
                'name': 'Bisnis.com Properti',
                'category': 'business_news'
            },
            'kontan_properti': {
                'url': 'https://www.kontan.co.id/feed/properti',
                'name': 'Kontan Properti',
                'category': 'financial_news'
            },
            'rei_official': {
                'url': 'https://rei.or.id/feed',
                'name': 'REI Official',
                'category': 'association_news'
            }
        }
        
        # Target keywords untuk monitoring
        self.target_keywords = [
            'Suku bunga BI',
            'Regulasi properti',
            'Insentif PPN DTP',
            'Kebijakan KPR',
            'Tren harga rumah',
            'BI rate',
            'Kebijakan moneter',
            'Subsidi perumahan',
            'Tax incentive',
            'PPN DTP',
            'KPR subsidi',
            'Harga properti',
            'Daya beli',
            'Inflasi',
            'OJK properti'
        ]
        
        # Market sentiment thresholds
        self.sentiment_thresholds = {
            'very_negative': -0.7,
            'negative': -0.3,
            'neutral': 0.3,
            'positive': 0.7,
            'very_positive': 1.0
        }
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database untuk industry insider"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create news articles table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS news_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    source TEXT,
                    category TEXT,
                    url TEXT UNIQUE,
                    published_date DATETIME,
                    sentiment TEXT DEFAULT 'neutral',
                    impact TEXT DEFAULT 'low',
                    actionable_insight TEXT,
                    macro_score REAL DEFAULT 0.0,
                    processed BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create market sentiment table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS market_sentiment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE UNIQUE,
                    overall_sentiment REAL DEFAULT 0.0,
                    sentiment_score REAL DEFAULT 0.0,
                    news_count INTEGER DEFAULT 0,
                    key_events TEXT,
                    market_modifier REAL DEFAULT 1.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create policy tracking table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS policy_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    policy_name TEXT NOT NULL,
                    policy_type TEXT,
                    effective_date DATE,
                    impact_level TEXT,
                    description TEXT,
                    source TEXT,
                    status TEXT DEFAULT 'active',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_news_source ON news_articles(source)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_news_sentiment ON news_articles(sentiment)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_news_processed ON news_articles(processed)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_sentiment_date ON market_sentiment(date)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_policy_status ON policy_tracking(status)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Industry insider database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing industry insider database: {e}")
    
    def aggregate_news(self, source_filter: List[str] = None) -> Dict:
        """
        Aggregate news dari RSS feeds
        """
        try:
            self.logger.info("Starting news aggregation...")
            
            sources_to_monitor = self.news_sources
            if source_filter:
                sources_to_monitor = {k: v for k, v in self.news_sources.items() if k in source_filter}
            
            aggregated_news = []
            processing_stats = {}
            
            for source_key, source_config in sources_to_monitor.items():
                self.logger.info(f"Processing {source_config['name']}...")
                
                try:
                    # Fetch RSS feed
                    feed_data = self._fetch_rss_feed(source_config['url'])
                    
                    if feed_data:
                        # Process articles
                        processed_articles = self._process_rss_articles(feed_data, source_config)
                        aggregated_news.extend(processed_articles)
                        
                        processing_stats[source_key] = {
                            'status': 'success',
                            'articles_found': len(feed_data),
                            'articles_processed': len(processed_articles)
                        }
                    else:
                        processing_stats[source_key] = {
                            'status': 'failed',
                            'articles_found': 0,
                            'articles_processed': 0
                        }
                
                except Exception as e:
                    self.logger.error(f"Error processing {source_config['name']}: {e}")
                    processing_stats[source_key] = {
                        'status': 'error',
                        'error': str(e),
                        'articles_found': 0,
                        'articles_processed': 0
                    }
                
                # Rate limiting
                time.sleep(2)
            
            # Filter articles with target keywords
            relevant_articles = self._filter_relevant_articles(aggregated_news)
            
            # Save to database
            saved_count = self._save_news_articles(relevant_articles)
            
            self.logger.info(f"News aggregation completed. Found {len(relevant_articles)} relevant articles")
            
            return {
                'status': 'success',
                'sources_monitored': len(sources_to_monitor),
                'total_articles_found': sum(stats.get('articles_found', 0) for stats in processing_stats.values()),
                'relevant_articles': len(relevant_articles),
                'articles_saved': saved_count,
                'processing_stats': processing_stats,
                'aggregation_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in news aggregation: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'aggregation_timestamp': datetime.now().isoformat()
            }
    
    def _fetch_rss_feed(self, url: str) -> List[Dict]:
        """Fetch RSS feed dari URL"""
        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                self.logger.warning(f"RSS feed parsing warning for {url}: {feed.bozo}")
            
            articles = []
            
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'published_date': self._parse_date(entry.get('published')),
                    'summary': entry.get('summary', ''),
                    'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                }
                
                # Get full content if summary is empty
                if not article['summary'] and article['url']:
                    article['content'] = self._scrape_article_content(article['url'])
                
                articles.append(article)
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed from {url}: {e}")
            return []
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string ke datetime object"""
        try:
            if not date_str:
                return datetime.now()
            
            # Try different date formats
            date_formats = [
                '%a, %d %b %Y %H:%M:%S %Z',
                '%a, %d %b %Y %H:%M:%S %z',
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Fallback to current date
            return datetime.now()
            
        except Exception:
            return datetime.now()
    
    def _scrape_article_content(self, url: str) -> str:
        """Scrape full article content dari URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try different content selectors
            content_selectors = [
                '.read__content',
                '.article__content',
                '.post-content',
                '.entry-content',
                'article',
                '.content'
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(strip=True)
                    break
            
            # Fallback to body text
            if not content:
                content = soup.get_text(strip=True)
            
            # Clean up content
            content = re.sub(r'\s+', ' ', content)
            content = content[:2000]  # Limit to 2000 characters
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error scraping article content from {url}: {e}")
            return ""
    
    def _process_rss_articles(self, articles: List[Dict], source_config: Dict) -> List[Dict]:
        """Process RSS articles dengan source configuration"""
        processed_articles = []
        
        for article in articles:
            processed_article = {
                **article,
                'source': source_config['name'],
                'category': source_config['category'],
                'content': article.get('content', article.get('summary', '')),
                'processed': False
            }
            
            processed_articles.append(processed_article)
        
        return processed_articles
    
    def _filter_relevant_articles(self, articles: List[Dict]) -> List[Dict]:
        """Filter articles yang mengandung target keywords"""
        relevant_articles = []
        
        for article in articles:
            content_text = f"{article.get('title', '')} {article.get('content', '')}".lower()
            
            # Check for target keywords
            keyword_matches = []
            for keyword in self.target_keywords:
                if keyword.lower() in content_text:
                    keyword_matches.append(keyword)
            
            if keyword_matches:
                article['matched_keywords'] = keyword_matches
                article['relevance_score'] = len(keyword_matches)
                relevant_articles.append(article)
        
        # Sort by relevance score
        relevant_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return relevant_articles
    
    def _save_news_articles(self, articles: List[Dict]) -> int:
        """Save news articles ke database"""
        try:
            saved_count = 0
            
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                for article in articles:
                    try:
                        # cursor.execute() removed'''
                            INSERT OR IGNORE INTO news_articles 
                            (title, content, source, category, url, published_date, processed)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            article.get('title', ''),
                            article.get('content', ''),
                            article.get('source', ''),
                            article.get('category', ''),
                            article.get('url', ''),
                            article.get('published_date', datetime.now()),
                            False
                        ))
                        
                        if cursor.rowcount > 0:
                            saved_count += 1
                    
                    except Exception as e:
                        self.logger.error(f"Error saving article: {e}")
                
                # conn.commit() removed
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"Error saving news articles: {e}")
            return 0
    
    def extract_macro_insights(self, limit: int = 50) -> Dict:
        """
        Extract macro insights dari news articles menggunakan LLM
        """
        try:
            self.logger.info("Starting macro insight extraction...")
            
            # Get unprocessed articles
            unprocessed_articles = self._get_unprocessed_articles(limit)
            
            if not unprocessed_articles:
                self.logger.info("No unprocessed articles found")
                return {
                    'status': 'success',
                    'articles_analyzed': 0,
                    'insights_extracted': 0,
                    'message': 'No unprocessed articles found'
                }
            
            insights_extracted = 0
            analysis_results = []
            
            for article in unprocessed_articles:
                try:
                    # Analyze article with LLM
                    insight = self._analyze_article_with_llm(article)
                    
                    if insight:
                        # Update article with insight
                        self._update_article_insight(article['id'], insight)
                        insights_extracted += 1
                        
                        analysis_results.append({
                            'article_id': article['id'],
                            'title': article['title'][:50] + '...',
                            'sentiment': insight['sentiment'],
                            'impact': insight['impact'],
                            'actionable_insight': insight['actionable_insight']
                        })
                    
                    # Mark as processed
                    self._mark_article_processed(article['id'])
                    
                except Exception as e:
                    self.logger.error(f"Error analyzing article {article['id']}: {e}")
                    self._mark_article_processed(article['id'])  # Mark as processed to avoid retry
            
            # Update market sentiment
            if insights_extracted > 0:
                self._update_market_sentiment()
            
            self.logger.info(f"Macro insight extraction completed. Analyzed {len(unprocessed_articles)} articles")
            
            return {
                'status': 'success',
                'articles_analyzed': len(unprocessed_articles),
                'insights_extracted': insights_extracted,
                'analysis_results': analysis_results,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in macro insight extraction: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'extraction_timestamp': datetime.now().isoformat()
            }
    
    def _analyze_article_with_llm(self, article: Dict) -> Optional[Dict]:
        """Analyze article dengan LLM untuk macro insights"""
        try:
            # Check if OpenAI is available
            try:
                import openai
                OPENAI_AVAILABLE = True
            except ImportError:
                OPENAI_AVAILABLE = False
                openai = None
            
            if not OPENAI_AVAILABLE:
                # Fallback to keyword-based analysis
                return self._analyze_article_with_keywords(article)
            
            # Prepare content for analysis
            content = f"Title: {article.get('title', '')}\n\nContent: {article.get('content', '')}"
            
            # LLM prompt
            prompt = f"""
            Analisis berita properti ini dan berikan insight dalam format JSON:
            
            Berita: {content}
            
            Pertanyaan:
            1. Apakah ini berita positif atau negatif bagi pengembang properti?
            2. Apakah ada kebijakan baru yang akan mempermudah/mempersulit closing dalam 6 bulan ke depan?
            3. Seberapa besar dampaknya terhadap pasar properti?
            
            Response format JSON:
            {{
                "sentiment": "positive/negative/neutral",
                "impact": "high/medium/low",
                "actionable_insight": "Ringkasan insight yang dapat ditindaklanjuti",
                "key_factors": ["faktor1", "faktor2"],
                "time_horizon": "short_term/medium_term/long_term"
            }}
            """
            
            client = openai.OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a macro-economic analyst specializing in Indonesian real estate market."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            llm_response = response.choices[0].message.content
            
            # Parse JSON response
            try:
                insight = json.loads(llm_response)
                
                # Validate required fields
                required_fields = ['sentiment', 'impact', 'actionable_insight']
                for field in required_fields:
                    if field not in insight:
                        insight[field] = 'unknown'
                
                return insight
                
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse LLM response as JSON: {llm_response}")
                return self._analyze_article_with_keywords(article)
                
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {e}")
            return self._analyze_article_with_keywords(article)
    
    def _analyze_article_with_keywords(self, article: Dict) -> Dict:
        """Fallback keyword-based analysis"""
        try:
            content = f"{article.get('title', '')} {article.get('content', '')}".lower()
            
            # Sentiment analysis based on keywords
            positive_keywords = ['turun', 'subsidi', 'insentif', 'bantuan', 'kemudahan', 'promo', 'diskon', 'ppn dtp']
            negative_keywords = ['naik', 'mahal', 'sulit', 'ketat', 'batasan', 'limit', 'biaya', 'beban']
            
            positive_score = sum(1 for kw in positive_keywords if kw in content)
            negative_score = sum(1 for kw in negative_keywords if kw in content)
            
            # Determine sentiment
            if positive_score > negative_score:
                sentiment = 'positive'
            elif negative_score > positive_score:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Determine impact based on keywords
            high_impact_keywords = ['suku bunga', 'kebijakan', 'regulasi', 'ppn', 'subsidi']
            impact = 'high' if any(kw in content for kw in high_impact_keywords) else 'medium'
            
            # Generate actionable insight
            if sentiment == 'positive':
                if 'subsidi' in content or 'insentif' in content:
                    insight_text = "Ada insentif baru yang dapat dimanfaatkan untuk meningkatkan closing"
                else:
                    insight_text = "Kondisi pasar mendukung untuk peningkatan aktivitas penjualan"
            elif sentiment == 'negative':
                if 'suku bunga' in content:
                    insight_text = "Suku bunga naik, perlu strategi harga yang lebih kompetitif"
                else:
                    insight_text = "Perlu menyesuaikan strategi penjualan dengan kondisi pasar"
            else:
                insight_text = "Monitor perkembangan lebih lanjut untuk dampak terhadap penjualan"
            
            return {
                'sentiment': sentiment,
                'impact': impact,
                'actionable_insight': insight_text,
                'key_factors': [],
                'time_horizon': 'medium_term'
            }
            
        except Exception as e:
            self.logger.error(f"Error in keyword analysis: {e}")
            return {
                'sentiment': 'neutral',
                'impact': 'low',
                'actionable_insight': 'Analysis error',
                'key_factors': [],
                'time_horizon': 'medium_term'
            }
    
    def _get_unprocessed_articles(self, limit: int) -> List[Dict]:
        """Get unprocessed articles dari database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT * FROM news_articles 
                    WHERE processed = 0
                    ORDER BY published_date DESC
                    LIMIT ?
                ''', (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                articles = []
                
                for row in cursor.fetchall():
                    article = dict(zip(columns, row))
                    articles.append(article)
                
                return articles
                
        except Exception as e:
            self.logger.error(f"Error getting unprocessed articles: {e}")
            return []
    
    def _update_article_insight(self, article_id: int, insight: Dict):
        """Update article dengan insight analysis"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    UPDATE news_articles 
                    SET sentiment = ?, impact = ?, actionable_insight = ?, macro_score = ?
                    WHERE id = ?
                ''', (
                    insight.get('sentiment', 'neutral'),
                    insight.get('impact', 'low'),
                    insight.get('actionable_insight', ''),
                    self._calculate_macro_score(insight),
                    article_id
                ))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error updating article insight: {e}")
    
    def _calculate_macro_score(self, insight: Dict) -> float:
        """Calculate macro score dari insight"""
        try:
            sentiment = insight.get('sentiment', 'neutral')
            impact = insight.get('impact', 'low')
            
            # Base score
            score = 0.0
            
            # Sentiment scoring
            if sentiment == 'positive':
                score += 0.5
            elif sentiment == 'negative':
                score -= 0.5
            
            # Impact scoring
            if impact == 'high':
                score += 0.3
            elif impact == 'medium':
                score += 0.1
            
            # Normalize to -1 to 1
            return max(-1.0, min(1.0, score))
            
        except Exception as e:
            self.logger.error(f"Error calculating macro score: {e}")
            return 0.0
    
    def _mark_article_processed(self, article_id: int):
        """Mark article sebagai processed"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                # cursor.execute() removed'UPDATE news_articles SET processed = 1 WHERE id = ?', (article_id,))
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error marking article as processed: {e}")
    
    def _update_market_sentiment(self):
        """Update market sentiment berdasarkan recent articles"""
        try:
            # Get recent articles (last 7 days)
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT AVG(macro_score) as avg_score, COUNT(*) as count
                    FROM news_articles 
                    WHERE processed = 1 
                    AND published_date >= date('now', '-7 days')
                ''')
                
                result = cursor.fetchone()
                avg_score = result[0] if result[0] else 0.0
                news_count = result[1] if result[1] else 0
            
            # Calculate market modifier
            market_modifier = self._calculate_market_modifier(avg_score)
            
            # Save market sentiment
            today = datetime.now().date()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO market_sentiment 
                (date, overall_sentiment, sentiment_score, news_count, market_modifier)
                VALUES (?, ?, ?, ?, ?)
            ''', (today, avg_score, avg_score, news_count, market_modifier))
            
            # conn.commit() removed
            
        except Exception as e:
            self.logger.error(f"Error updating market sentiment: {e}")
    
    def _calculate_market_modifier(self, sentiment_score: float) -> float:
        """Calculate market modifier berdasarkan sentiment score"""
        try:
            # Map sentiment score to market modifier
            if sentiment_score > 0.7:
                return 1.2  # Very positive - increase urgency
            elif sentiment_score > 0.3:
                return 1.1  # Positive - slight increase
            elif sentiment_score > -0.3:
                return 1.0  # Neutral - no change
            elif sentiment_score > -0.7:
                return 0.9  # Negative - decrease urgency
            else:
                return 0.8  # Very negative - significant decrease
                
        except Exception as e:
            self.logger.error(f"Error calculating market modifier: {e}")
            return 1.0
    
    def adjust_market_sentiment(self, lead_data: Dict) -> Dict:
        """
        Adjust market sentiment untuk lead scoring
        """
        try:
            # Get current market sentiment
            market_sentiment = self._get_current_market_sentiment()
            
            if not market_sentiment:
                return {
                    'status': 'no_data',
                    'original_score': lead_data.get('score', 0),
                    'adjusted_score': lead_data.get('score', 0),
                    'market_modifier': 1.0
                }
            
            market_modifier = market_sentiment.get('market_modifier', 1.0)
            original_score = lead_data.get('score', 0)
            
            # Apply market modifier
            adjusted_score = original_score * market_modifier
            
            # Ensure score stays within valid range
            adjusted_score = max(0, min(10, adjusted_score))
            
            # Determine adjustment reason
            if market_modifier > 1.0:
                adjustment_reason = "Market conditions positive - score increased"
            elif market_modifier < 1.0:
                adjustment_reason = "Market conditions negative - score decreased"
            else:
                adjustment_reason = "Market conditions neutral - no adjustment"
            
            return {
                'status': 'success',
                'original_score': original_score,
                'adjusted_score': adjusted_score,
                'market_modifier': market_modifier,
                'market_sentiment': market_sentiment.get('overall_sentiment', 0),
                'adjustment_reason': adjustment_reason,
                'adjustment_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error adjusting market sentiment: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'original_score': lead_data.get('score', 0),
                'adjusted_score': lead_data.get('score', 0)
            }
    
    def _get_current_market_sentiment(self) -> Optional[Dict]:
        """Get current market sentiment"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT * FROM market_sentiment 
                    ORDER BY date DESC 
                    LIMIT 1
                ''')
                
                row = cursor.fetchone()
                
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    sentiment = dict(zip(columns, row))
                    return sentiment
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting current market sentiment: {e}")
            return None
    
    def generate_industry_briefing(self) -> Dict:
        """
        Generate industry briefing untuk weekly report
        """
        try:
            self.logger.info("Generating industry briefing...")
            
            # Get top policies
            top_policies = self._get_top_policies()
            
            # Get market sentiment
            market_sentiment = self._get_current_market_sentiment()
            
            # Get key events
            key_events = self._get_key_events()
            
            # Generate strategic recommendations
            recommendations = self._generate_strategic_recommendations(market_sentiment, key_events)
            
            # Create briefing content
            briefing_content = self._create_briefing_content(
                top_policies, market_sentiment, key_events, recommendations
            )
            
            # Save briefing to file
            briefing_file = self._save_briefing_to_file(briefing_content)
            
            self.logger.info(f"Industry briefing generated: {briefing_file}")
            
            return {
                'status': 'success',
                'briefing_file': briefing_file,
                'top_policies': len(top_policies),
                'market_sentiment': market_sentiment.get('overall_sentiment', 0) if market_sentiment else 0,
                'key_events': len(key_events),
                'recommendations': len(recommendations),
                'briefing_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating industry briefing: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'briefing_timestamp': datetime.now().isoformat()
            }
    
    def _get_top_policies(self, limit: int = 3) -> List[Dict]:
        """Get top policies dari recent articles"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT title, actionable_insight, published_date, source, impact
                    FROM news_articles 
                    WHERE processed = 1 AND impact IN ('high', 'medium')
                    ORDER BY published_date DESC
                    LIMIT ?
                ''', (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                policies = []
                
                for row in cursor.fetchall():
                    policy = dict(zip(columns, row))
                    policies.append(policy)
                
                return policies
                
        except Exception as e:
            self.logger.error(f"Error getting top policies: {e}")
            return []
    
    def _get_key_events(self, limit: int = 5) -> List[Dict]:
        """Get key events dari recent articles"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT title, sentiment, impact, published_date, source
                    FROM news_articles 
                    WHERE processed = 1 
                    ORDER BY ABS(macro_score) DESC, published_date DESC
                    LIMIT ?
                ''', (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                events = []
                
                for row in cursor.fetchall():
                    event = dict(zip(columns, row))
                    events.append(event)
                
                return events
                
        except Exception as e:
            self.logger.error(f"Error getting key events: {e}")
            return []
    
    def _generate_strategic_recommendations(self, market_sentiment: Dict, key_events: List[Dict]) -> List[str]:
        """Generate strategic recommendations berdasarkan market conditions"""
        try:
            recommendations = []
            
            # Market sentiment based recommendations
            if market_sentiment:
                sentiment = market_sentiment.get('overall_sentiment', 0)
                
                if sentiment > 0.5:
                    recommendations.append("Market positif - tingkatkan target penjualan dan agresif follow up leads")
                    recommendations.append("Manfaatkan momentum positif untuk menawarkan premium products")
                elif sentiment < -0.5:
                    recommendations.append("Market negatif - fokus pada value proposition dan harga kompetitif")
                    recommendations.append("Prioritaskan leads dengan daya beli tinggi dan segmen yang tidak terdampak")
                else:
                    recommendations.append("Market netral - pertahankan strategi existing dengan fokus efisiensi")
            
            # Key events based recommendations
            high_impact_events = [e for e in key_events if e.get('impact') == 'high']
            
            if high_impact_events:
                recommendations.append("Monitor dampak kebijakan high-impact terhadap pipeline penjualan")
                recommendations.append("Siapkan strategi respons cepat untuk perubahan regulasi")
            
            # General recommendations
            recommendations.append("Review dan optimalkan lead qualification criteria berdasarkan kondisi pasar")
            recommendations.append("Tingkatkan komunikasi dengan existing leads tentang kondisi pasar terkini")
            
            return recommendations[:5]  # Limit to 5 recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating strategic recommendations: {e}")
            return ["Error generating recommendations"]
    
    def _create_briefing_content(self, policies: List[Dict], sentiment: Dict, events: List[Dict], recommendations: List[str]) -> str:
        """Create briefing content dalam markdown format"""
        try:
            current_date = datetime.now().strftime("%d %B %Y")
            
            content = f"""# INDUSTRY BRIEFING - {current_date}
============================================================

## 📊 SENTIMEN PASAR

"""
            
            # Market sentiment section
            if sentiment:
                sentiment_score = sentiment.get('overall_sentiment', 0)
                market_modifier = sentiment.get('market_modifier', 1.0)
                
                if sentiment_score > 0.5:
                    market_status = "🟢 BULLISH"
                elif sentiment_score < -0.5:
                    market_status = "🔴 BEARISH"
                else:
                    market_status = "🟡 NEUTRAL"
                
                content += f"""**Status Pasar:** {market_status}
**Sentiment Score:** {sentiment_score:.2f}
**Market Modifier:** {market_modifier:.2f}
**News Analyzed:** {sentiment.get('news_count', 0)}

"""
            else:
                content += """**Status Pasar:** 🟡 TIDAK ADA DATA
**Sentiment Score:** N/A
**Market Modifier:** 1.00

"""
            
            # Top 3 policies section
            content += """## 🏛️ TOP 3 KEBIJAKAN BARU

"""
            
            for i, policy in enumerate(policies[:3], 1):
                content += f"""### {i}. {policy.get('title', 'Unknown Policy')}

**Sumber:** {policy.get('source', 'Unknown')}
**Dampak:** {policy.get('impact', 'low').title()}
**Tanggal:** {policy.get('published_date', 'Unknown')}

**Insight:** {policy.get('actionable_insight', 'No insight available')}

"""
            
            # Key events section
            content += """## 📰 KEY EVENTS

"""
            
            for i, event in enumerate(events[:5], 1):
                sentiment_emoji = "🟢" if event.get('sentiment') == 'positive' else "🔴" if event.get('sentiment') == 'negative' else "🟡"
                
                content += f"""### {i}. {sentiment_emoji} {event.get('title', 'Unknown Event')}

**Sentiment:** {event.get('sentiment', 'unknown').title()}
**Dampak:** {event.get('impact', 'low').title()}
**Sumber:** {event.get('source', 'Unknown')}
**Tanggal:** {event.get('published_date', 'Unknown')}

"""
            
            # Strategic recommendations section
            content += """## 🎯 REKOMENDASI STRATEGIS

"""
            
            for i, rec in enumerate(recommendations, 1):
                content += f"""### {i}. {rec}

"""
            
            # Footer
            content += f"""
============================================================
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source:** Industry Insider - Macro Analyst System
**Next Briefing:** {(datetime.now() + timedelta(days=7)).strftime("%d %B %Y")}
"""
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error creating briefing content: {e}")
            return f"Error creating briefing content: {str(e)}"
    
    def _save_briefing_to_file(self, content: str) -> str:
        """Save briefing ke file"""
        try:
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            briefing_file = os.path.join(reports_dir, 'macro_briefing.md')
            
            with open(briefing_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return briefing_file
            
        except Exception as e:
            self.logger.error(f"Error saving briefing to file: {e}")
            return ""

# Global industry insider instance
industry_insider = IndustryInsider()

# Convenience functions
def aggregate_news(source_filter: List[str] = None) -> Dict:
    """Aggregate news dari RSS feeds"""
    return industry_insider.aggregate_news(source_filter)

def extract_macro_insights(limit: int = 50) -> Dict:
    """Extract macro insights dari news articles"""
    return industry_insider.extract_macro_insights(limit)

def adjust_market_sentiment(lead_data: Dict) -> Dict:
    """Adjust market sentiment untuk lead scoring"""
    return industry_insider.adjust_market_sentiment(lead_data)

def generate_industry_briefing() -> Dict:
    """Generate industry briefing"""
    return industry_insider.generate_industry_briefing()

if __name__ == "__main__":
    # Test Industry Insider
    logging.basicConfig(level=logging.INFO)
    
    print("=== Industry Insider Test ===")
    
    # Test news aggregation
    print("\n📰 Testing News Aggregation...")
    aggregation_result = aggregate_news()
    print(f"Aggregation status: {aggregation_result['status']}")
    print(f"Sources monitored: {aggregation_result['sources_monitored']}")
    print(f"Relevant articles: {aggregation_result['relevant_articles']}")
    
    # Test macro insight extraction
    print("\n🧠 Testing Macro Insight Extraction...")
    insight_result = extract_macro_insights()
    print(f"Insight extraction status: {insight_result['status']}")
    print(f"Articles analyzed: {insight_result['articles_analyzed']}")
    print(f"Insights extracted: {insight_result['insights_extracted']}")
    
    # Test market sentiment adjustment
    print("\n📊 Testing Market Sentiment Adjustment...")
    test_lead = {'score': 8.5, 'title': 'Test Lead'}
    adjustment_result = adjust_market_sentiment(test_lead)
    print(f"Adjustment status: {adjustment_result['status']}")
    print(f"Original score: {adjustment_result['original_score']}")
    print(f"Adjusted score: {adjustment_result['adjusted_score']}")
    print(f"Market modifier: {adjustment_result['market_modifier']}")
    
    # Test industry briefing generation
    print("\n📋 Testing Industry Briefing Generation...")
    briefing_result = generate_industry_briefing()
    print(f"Briefing generation status: {briefing_result['status']}")
    print(f"Briefing file: {briefing_result.get('briefing_file', 'N/A')}")
    print(f"Top policies: {briefing_result.get('top_policies', 0)}")
    print(f"Recommendations: {briefing_result.get('recommendations', 0)}")
    
    print("\nIndustry Insider test completed!")

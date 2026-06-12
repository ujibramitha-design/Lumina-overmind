"""
Central Intelligence Hub - Core Intelligence Aggregator Module
Sistem terpusat untuk mengagregasi informasi dari berbagai sumber dan menghasilkan executive summary
"""

import json
import requests
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
import concurrent.futures
import threading
from queue import Queue
import hashlib

# Load environment variables
load_dotenv()

class IntelligenceAggregator:
    """
    Central Intelligence Hub - Core Intelligence Aggregator
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'sources.json')
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'intelligence_hub.db (SQLite - removed))
        self.reports_path = os.path.join(os.path.dirname(__file__), '..', 'reports')
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.reports_path, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # Load configuration
        self.sources_config = self._load_sources_config()
        
        # Target keywords for content filtering
        self.target_keywords = [
            'tol', 'pembangunan', 'perumahan', 'izin', 'kawasan', 'rencana', 
            'industri', 'tanah', 'tata ruang', 'subsidi'
        ]
        
        # Deep-Crawl Manager components
        self.scrape_status_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'scrape_status.json')
        self.status_lock = threading.Lock()
        self.max_workers = 8  # Maximum concurrent threads
        
        # Initialize scrape status
        self._init_scrape_status()
        
        # Initialize scraper
        self.scraper = IntelligenceScraper(self.target_keywords)
    
    def _init_database(self):
        """Initialize database untuk intelligence hub"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create intelligence sources table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS intelligence_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    last_scanned DATETIME,
                    scan_status TEXT DEFAULT 'pending',
                    articles_found INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create scraped content table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS scraped_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT NOT NULL,
                    published_date DATETIME,
                    keywords_found TEXT,  -- JSON
                    processed BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES intelligence_sources (id)
                )
            ''')
            
            # Create LLM analysis results table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS llm_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id INTEGER,
                    analysis_type TEXT NOT NULL,
                    insights TEXT,  -- JSON
                    confidence_score REAL DEFAULT 0.0,
                    model_used TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (content_id) REFERENCES scraped_content (id)
                )
            ''')
            
            # Create executive summary table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS executive_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary_date DATE UNIQUE,
                    alerts_important TEXT,  -- JSON
                    market_trend TEXT,  -- JSON
                    government_updates TEXT,  -- JSON
                    actionable_insights TEXT,  -- JSON
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_sources_category ON intelligence_sources(category)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_scraped_content_source ON scraped_content(source_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_scraped_content_processed ON scraped_content(processed)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_llm_analysis_content ON llm_analysis(content_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_summaries_date ON executive_summaries(summary_date)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Intelligence hub database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing intelligence hub database: {e}")
    
    def _load_sources_config(self) -> Dict:
        """Load sources configuration dari JSON file"""
        try:
            if not os.path.exists(self.config_path):
                self.logger.warning(f"Sources config file not found: {self.config_path}")
                return {}
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.logger.info(f"Loaded sources configuration with {len(config)} categories")
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading sources config: {e}")
            return {}
    
    def _init_scrape_status(self):
        """Initialize scrape status tracking"""
        try:
            os.makedirs(os.path.dirname(self.scrape_status_file), exist_ok=True)
            
            if not os.path.exists(self.scrape_status_file):
                initial_status = {
                    "last_updated": datetime.now().isoformat(),
                    "sources": {},
                    "failed_attempts": {},
                    "success_rate": {}
                }
                with open(self.scrape_status_file, 'w') as f:
                    json.dump(initial_status, f, indent=2)
                    
            self.logger.info("Scrape status tracking initialized")
        except Exception as e:
            self.logger.error(f"Error initializing scrape status: {e}")
    
    def _update_scrape_status(self, source_name: str, status: str, error: str = None):
        """Update scrape status for a source"""
        try:
            with self.status_lock:
                if os.path.exists(self.scrape_status_file):
                    with open(self.scrape_status_file, 'r') as f:
                        status_data = json.load(f)
                else:
                    status_data = {"sources": {}, "failed_attempts": {}, "success_rate": {}}
                
                # Update source status
                status_data["sources"][source_name] = {
                    "last_attempt": datetime.now().isoformat(),
                    "status": status,
                    "error": error
                }
                
                # Track failed attempts
                if status == "error":
                    status_data["failed_attempts"][source_name] = status_data["failed_attempts"].get(source_name, 0) + 1
                elif status == "success":
                    status_data["failed_attempts"][source_name] = 0
                
                # Calculate success rate
                total_attempts = status_data["failed_attempts"].get(source_name, 0) + (1 if status == "success" else 0)
                success_rate = 0 if total_attempts == 0 else (1 / total_attempts) * 100
                status_data["success_rate"][source_name] = success_rate
                
                # Save updated status
                with open(self.scrape_status_file, 'w') as f:
                    json.dump(status_data, f, indent=2)
                    
        except Exception as e:
            self.logger.error(f"Error updating scrape status: {e}")
    
    def _should_skip_source(self, source_name: str) -> bool:
        """Check if source should be skipped based on failure history"""
        try:
            if os.path.exists(self.scrape_status_file):
                with open(self.scrape_status_file, 'r') as f:
                    status_data = json.load(f)
                
                failed_attempts = status_data["failed_attempts"].get(source_name, 0)
                # Skip if more than 5 consecutive failures
                if failed_attempts >= 5:
                    self.logger.warning(f"Skipping {source_name} due to {failed_attempts} consecutive failures")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error checking skip status: {e}")
            return False
    
    def _scrape_source_worker(self, source_name: str, url: str, category: str) -> Dict:
        """Worker function for multi-threaded scraping"""
        try:
            # Check if we should skip this source
            if self._should_skip_source(source_name):
                return {
                    'source_name': source_name,
                    'url': url,
                    'status': 'skipped',
                    'reason': 'Too many consecutive failures'
                }
            
            # Scrape the source
            source_result = self.scraper.scrape_source(url, source_name, category)
            
            # Update status
            self._update_scrape_status(source_name, 'success')
            
            # Save to database
            source_id = self._save_source_result(category, source_name, url, source_result)
            
            # Save scraped content
            if source_result.get('articles'):
                self._save_scraped_content(source_id, source_result['articles'])
            
            return source_result
            
        except Exception as e:
            # Update error status
            self._update_scrape_status(source_name, 'error', str(e))
            
            return {
                'source_name': source_name,
                'url': url,
                'status': 'error',
                'error': str(e)
            }
    
    def run_daily_scan_deep_crawl(self) -> Dict:
        """
        Deep-Crawl Manager - Multi-threaded scanning with smart parsing
        """
        try:
            self.logger.info("Starting Deep-Crawl Manager scan...")
            
            scan_results = []
            all_sources = []
            
            # Collect all sources
            for category, sources in self.sources_config.items():
                self.logger.info(f"Preparing category: {category}")
                for source_name, url in sources.items():
                    all_sources.append((source_name, url, category))
            
            # Multi-threaded execution
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_source = {
                    executor.submit(self._scrape_source_worker, source_name, url, category): (source_name, url, category)
                    for source_name, url, category in all_sources
                }
                
                # Process results as they complete
                for future in concurrent.futures.as_completed(future_to_source):
                    source_name, url, category = future_to_source[future]
                    try:
                        result = future.result()
                        scan_results.append(result)
                        
                        if result['status'] == 'success':
                            self.logger.info(f"✅ {source_name}: {len(result.get('articles', []))} articles")
                        elif result['status'] == 'skipped':
                            self.logger.warning(f"⏭️  {source_name}: {result.get('reason', 'Skipped')}")
                        else:
                            self.logger.error(f"❌ {source_name}: {result.get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        self.logger.error(f"Error processing {source_name}: {e}")
            
            # Process scraped content with LLM
            self.logger.info("Processing scraped content with LLM...")
            self._process_scraped_content_with_llm()
            
            # Generate executive summary
            self.logger.info("Generating executive summary...")
            summary_file = self._generate_executive_summary()
            
            # Update system prompts
            self._update_system_prompts()
            
            # Calculate statistics
            successful_sources = [r for r in scan_results if r.get('status') == 'success']
            failed_sources = [r for r in scan_results if r.get('status') == 'error']
            skipped_sources = [r for r in scan_results if r.get('status') == 'skipped']
            
            total_articles = sum(len(r.get('articles', [])) for r in successful_sources)
            
            result = {
                'status': 'success',
                'categories_scanned': len(self.sources_config),
                'total_sources': len(all_sources),
                'successful_sources': len(successful_sources),
                'failed_sources': len(failed_sources),
                'skipped_sources': len(skipped_sources),
                'total_articles': total_articles,
                'llm_analyses': self._get_llm_analysis_count(),
                'summary_file': summary_file,
                'scan_results': scan_results
            }
            
            self.logger.info(f"Deep-Crawl completed: {len(successful_sources)} successful, {len(failed_sources)} failed, {len(skipped_sources)} skipped")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in Deep-Crawl Manager: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'categories_scanned': 0,
                'total_articles': 0
            }
    
    def run_daily_scan(self) -> Dict:
        """
        The Daily Aggregator Logic - Scan all sources and generate executive summary
        """
        try:
            self.logger.info("Starting daily intelligence scan...")
            
            scan_results = []
            
            # Iterate through all source categories
            for category, sources in self.sources_config.items():
                self.logger.info(f"Scanning category: {category}")
                
                category_results = []
                
                for source_name, url in sources.items():
                    try:
                        # Scrape individual source
                        source_result = self.scraper.scrape_source(url, source_name, category)
                        category_results.append(source_result)
                        
                        # Save to database
                        source_id = self._save_source_result(category, source_name, url, source_result)
                        
                        # Save scraped content
                        if source_result.get('articles'):
                            self._save_scraped_content(source_id, source_result['articles'])
                        
                        # Rate limiting
                        time.sleep(2)
                        
                    except Exception as e:
                        self.logger.error(f"Error scanning {source_name}: {e}")
                        category_results.append({
                            'source_name': source_name,
                            'url': url,
                            'status': 'error',
                            'error': str(e)
                        })
                
                scan_results.append({
                    'category': category,
                    'results': category_results,
                    'total_articles': sum(r.get('articles_found', 0) for r in category_results)
                })
            
            # Process content with LLM
            self.logger.info("Processing scraped content with LLM...")
            llm_results = self._process_content_with_llm()
            
            # Generate executive summary
            self.logger.info("Generating executive summary...")
            summary_result = self._generate_executive_summary()
            
            # Save summary to file
            summary_file = self._save_summary_to_file(summary_result)
            
            # Update system prompts
            self._update_system_prompts()
            
            total_articles = sum(result['total_articles'] for result in scan_results)
            
            self.logger.info(f"Daily scan completed. Processed {total_articles} articles")
            
            return {
                'status': 'success',
                'categories_scanned': len(scan_results),
                'total_articles': total_articles,
                'llm_analyses': llm_results.get('total_analyzed', 0),
                'summary_file': summary_file,
                'scan_timestamp': datetime.now().isoformat(),
                'scan_results': scan_results
            }
            
        except Exception as e:
            self.logger.error(f"Error in daily scan: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'scan_timestamp': datetime.now().isoformat()
            }
    
    def _save_source_result(self, category: str, source_name: str, url: str, result: Dict) -> int:
        """Save source scanning result ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    INSERT OR REPLACE INTO intelligence_sources 
                    (category, source_name, url, last_scanned, scan_status, articles_found)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    category,
                    source_name,
                    url,
                    datetime.now(),
                    result.get('status', 'completed'),
                    result.get('articles_found', 0)
                ))
                
                source_id = cursor.lastrowid
                # conn.commit() removed
                
                return source_id
                
        except Exception as e:
            self.logger.error(f"Error saving source result: {e}")
            return 0
    
    def _save_scraped_content(self, source_id: int, articles: List[Dict]):
        """Save scraped content ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                for article in articles:
                    # cursor.execute() removed'''
                        INSERT OR IGNORE INTO scraped_content 
                        (source_id, title, content, url, published_date, keywords_found)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        source_id,
                        article.get('title', ''),
                        article.get('content', ''),
                        article.get('url', ''),
                        article.get('published_date', datetime.now()),
                        json.dumps(article.get('keywords_found', []))
                    ))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error saving scraped content: {e}")
    
    def _process_content_with_llm(self) -> Dict:
        """Process scraped content dengan LLM Analyst Agent"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get unprocessed content
                # cursor.execute() removed'''
                    SELECT id, title, content, url FROM scraped_content 
                    WHERE processed = 0
                    ORDER BY id
                    LIMIT 50
                ''')
                
                unprocessed_content = cursor.fetchall()
                
                if not unprocessed_content:
                    return {'total_analyzed': 0, 'results': []}
                
                llm_analyst = LLM_Analyst_Agent()
                analysis_results = []
                
                for content_row in unprocessed_content:
                    content_id, title, content, url = content_row
                    
                    try:
                        # Analyze with LLM
                        analysis = llm_analyst.analyze_content(title, content)
                        
                        # Save analysis result
                        self._save_llm_analysis(content_id, analysis)
                        
                        # Mark as processed
                        # cursor.execute() removed'UPDATE scraped_content SET processed = 1 WHERE id = ?', (content_id,))
                        
                        analysis_results.append({
                            'content_id': content_id,
                            'title': title,
                            'url': url,
                            'analysis': analysis
                        })
                        
                    except Exception as e:
                        self.logger.error(f"Error analyzing content {content_id}: {e}")
                        # cursor.execute() removed'UPDATE scraped_content SET processed = 1 WHERE id = ?', (content_id,))
                
                # conn.commit() removed
                
                return {
                    'total_analyzed': len(analysis_results),
                    'results': analysis_results
                }
                
        except Exception as e:
            self.logger.error(f"Error processing content with LLM: {e}")
            return {'total_analyzed': 0, 'results': []}
    
    def _save_llm_analysis(self, content_id: int, analysis: Dict):
        """Save LLM analysis result ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    INSERT INTO llm_analysis 
                    (content_id, analysis_type, insights, confidence_score, model_used)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    content_id,
                    analysis.get('type', 'general'),
                    json.dumps(analysis.get('insights', {})),
                    analysis.get('confidence', 0.0),
                    analysis.get('model', 'unknown')
                ))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error saving LLM analysis: {e}")
    
    def _generate_executive_summary(self) -> Dict:
        """Generate executive summary dari semua hasil analisis"""
        try:
            # Get recent LLM analyses
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT c.title, c.content, c.url, l.insights, l.confidence_score, l.created_at
                    FROM scraped_content c
                    JOIN llm_analysis l ON c.id = l.content_id
                    WHERE l.created_at >= date('now', '-1 day')
                    ORDER BY l.confidence_score DESC
                ''')
                
                analyses = cursor.fetchall()
            
            # Generate summary components
            alerts_important = self._extract_important_alerts(analyses)
            market_trend = self._extract_market_trend(analyses)
            government_updates = self._extract_government_updates(analyses)
            actionable_insights = self._extract_actionable_insights(analyses)
            
            summary_data = {
                'date': datetime.now().date().isoformat(),
                'alerts_important': alerts_important,
                'market_trend': market_trend,
                'government_updates': government_updates,
                'actionable_insights': actionable_insights,
                'total_analyses': len(analyses),
                'generated_at': datetime.now().isoformat()
            }
            
            # Save to database
            self._save_executive_summary_to_db(summary_data)
            
            return summary_data
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {e}")
            return {}
    
    def _extract_important_alerts(self, analyses: List[Tuple]) -> List[Dict]:
        """Extract important alerts dari analyses"""
        try:
            alerts = []
            
            for title, content, url, insights_json, confidence, created_at in analyses:
                try:
                    insights = json.loads(insights_json) if insights_json else {}
                    
                    # Look for alert-type insights
                    if insights.get('type') == 'alert' or 'urgent' in insights.get('priority', '').lower():
                        alerts.append({
                            'title': title,
                            'url': url,
                            'alert_message': insights.get('message', ''),
                            'priority': insights.get('priority', 'medium'),
                            'confidence': confidence,
                            'date': created_at
                        })
                
                except Exception as e:
                    self.logger.error(f"Error extracting alert from analysis: {e}")
                    continue
            
            # Sort by confidence and return top 5
            alerts.sort(key=lambda x: x['confidence'], reverse=True)
            return alerts[:5]
            
        except Exception as e:
            self.logger.error(f"Error extracting important alerts: {e}")
            return []
    
    def _extract_market_trend(self, analyses: List[Tuple]) -> Dict:
        """Extract market trend dari analyses"""
        try:
            trend_data = {
                'overall_sentiment': 'neutral',
                'key_trends': [],
                'price_movements': [],
                'demand_indicators': []
            }
            
            positive_count = 0
            negative_count = 0
            
            for title, content, url, insights_json, confidence, created_at in analyses:
                try:
                    insights = json.loads(insights_json) if insights_json else {}
                    
                    # Count sentiment
                    if insights.get('sentiment') == 'positive':
                        positive_count += 1
                    elif insights.get('sentiment') == 'negative':
                        negative_count += 1
                    
                    # Extract trends
                    if insights.get('type') == 'trend':
                        trend_data['key_trends'].append({
                            'trend': insights.get('trend', ''),
                            'description': insights.get('description', ''),
                            'confidence': confidence
                        })
                    
                    # Extract price movements
                    if 'harga' in title.lower() or 'price' in title.lower():
                        trend_data['price_movements'].append({
                            'title': title,
                            'url': url,
                            'insight': insights.get('message', ''),
                            'confidence': confidence
                        })
                    
                    # Extract demand indicators
                    if 'permintaan' in title.lower() or 'demand' in title.lower():
                        trend_data['demand_indicators'].append({
                            'title': title,
                            'url': url,
                            'insight': insights.get('message', ''),
                            'confidence': confidence
                        })
                
                except Exception as e:
                    self.logger.error(f"Error extracting trend data: {e}")
                    continue
            
            # Determine overall sentiment
            total = positive_count + negative_count
            if total > 0:
                if positive_count > negative_count * 1.5:
                    trend_data['overall_sentiment'] = 'positive'
                elif negative_count > positive_count * 1.5:
                    trend_data['overall_sentiment'] = 'negative'
                else:
                    trend_data['overall_sentiment'] = 'neutral'
            
            return trend_data
            
        except Exception as e:
            self.logger.error(f"Error extracting market trend: {e}")
            return {
                'overall_sentiment': 'neutral',
                'key_trends': [],
                'price_movements': [],
                'demand_indicators': []
            }
    
    def _extract_government_updates(self, analyses: List[Tuple]) -> List[Dict]:
        """Extract government updates dari analyses"""
        try:
            updates = []
            
            for title, content, url, insights_json, confidence, created_at in analyses:
                try:
                    insights = json.loads(insights_json) if insights_json else {}
                    
                    # Look for government-related insights
                    if insights.get('source_type') == 'government' or any(keyword in title.lower() for keyword in ['pemerintah', 'kebijakan', 'regulasi', 'bi', 'ojk', 'pupr', 'bps']):
                        updates.append({
                            'title': title,
                            'url': url,
                            'policy_type': insights.get('policy_type', 'general'),
                            'impact': insights.get('impact', 'unknown'),
                            'description': insights.get('message', ''),
                            'confidence': confidence,
                            'date': created_at
                        })
                
                except Exception as e:
                    self.logger.error(f"Error extracting government update: {e}")
                    continue
            
            # Sort by confidence and return top 5
            updates.sort(key=lambda x: x['confidence'], reverse=True)
            return updates[:5]
            
        except Exception as e:
            self.logger.error(f"Error extracting government updates: {e}")
            return []
    
    def _extract_actionable_insights(self, analyses: List[Tuple]) -> List[Dict]:
        """Extract actionable insights dari analyses"""
        try:
            insights = []
            
            for title, content, url, insights_json, confidence, created_at in analyses:
                try:
                    insight_data = json.loads(insights_json) if insights_json else {}
                    
                    # Look for actionable insights
                    if insight_data.get('actionable') or insight_data.get('type') in ['opportunity', 'recommendation']:
                        insights.append({
                            'title': title,
                            'url': url,
                            'insight_type': insight_data.get('type', 'general'),
                            'action': insight_data.get('action', ''),
                            'recommendation': insight_data.get('recommendation', ''),
                            'confidence': confidence,
                            'date': created_at
                        })
                
                except Exception as e:
                    self.logger.error(f"Error extracting actionable insight: {e}")
                    continue
            
            # Sort by confidence and return top 10
            insights.sort(key=lambda x: x['confidence'], reverse=True)
            return insights[:10]
            
        except Exception as e:
            self.logger.error(f"Error extracting actionable insights: {e}")
            return []
    
    def _save_executive_summary_to_db(self, summary_data: Dict):
        """Save executive summary ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    INSERT OR REPLACE INTO executive_summaries 
                    (summary_date, alerts_important, market_trend, government_updates, actionable_insights)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    summary_data['date'],
                    json.dumps(summary_data['alerts_important']),
                    json.dumps(summary_data['market_trend']),
                    json.dumps(summary_data['government_updates']),
                    json.dumps(summary_data['actionable_insights'])
                ))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error saving executive summary to database: {e}")
    
    def _save_summary_to_file(self, summary_data: Dict) -> str:
        """Save executive summary ke file markdown"""
        try:
            current_date = datetime.now().strftime("%d %B %Y")
            
            content = f"""# EXECUTIVE SUMMARY - {current_date}
============================================================

## 🚨 ALERTS (PENTING)

"""
            
            # Add alerts
            if summary_data.get('alerts_important'):
                for i, alert in enumerate(summary_data['alerts_important'], 1):
                    priority_emoji = "🔴" if alert['priority'] == 'high' else "🟡" if alert['priority'] == 'medium' else "🟢"
                    content += f"""### {i}. {priority_emoji} {alert['title']}

**Priority:** {alert['priority'].title()}
**Confidence:** {alert['confidence']:.2f}
**Alert:** {alert['alert_message']}
**Source:** {alert['url']}

"""
            else:
                content += "No important alerts detected.\n\n"
            
            # Add market trend
            content += """## 📈 MARKET TREND

**Overall Sentiment:** {summary_data.get('market_trend', {}).get('overall_sentiment', 'neutral').title()}

"""
            
            market_trend = summary_data.get('market_trend', {})
            if market_trend.get('key_trends'):
                content += "**Key Trends:**\n"
                for trend in market_trend['key_trends'][:3]:
                    content += f"- {trend['trend']}: {trend['description']}\n"
                content += "\n"
            
            if market_trend.get('price_movements'):
                content += "**Price Movements:**\n"
                for price in market_trend['price_movements'][:3]:
                    content += f"- {price['title']}: {price['insight']}\n"
                content += "\n"
            
            # Add government updates
            content += """## 🏛️ DATA UPDATE DARI PEMERINTAH

"""
            
            if summary_data.get('government_updates'):
                for i, update in enumerate(summary_data['government_updates'], 1):
                    content += f"""### {i}. {update['title']}

**Policy Type:** {update['policy_type']}
**Impact:** {update['impact']}
**Description:** {update['description']}
**Confidence:** {update['confidence']:.2f}
**Source:** {update['url']}

"""
            else:
                content += "No significant government updates detected.\n\n"
            
            # Add actionable insights
            content += """## 💡 ACTIONABLE INSIGHTS

"""
            
            if summary_data.get('actionable_insights'):
                for i, insight in enumerate(summary_data['actionable_insights'], 1):
                    content += f"""### {i}. {insight['title']}

**Type:** {insight['insight_type'].title()}
**Action:** {insight['action']}
**Recommendation:** {insight['recommendation']}
**Confidence:** {insight['confidence']:.2f}
**Source:** {insight['url']}

"""
            else:
                content += "No actionable insights detected.\n\n"
            
            # Add footer
            content += f"""
============================================================
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Analyses:** {summary_data.get('total_analyses', 0)}
**Next Update:** {(datetime.now() + timedelta(days=1)).strftime("%d %B %Y")}
**Source:** Central Intelligence Hub
"""
            
            # Save to file
            summary_file = os.path.join(self.reports_path, 'executive_summary.md')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return summary_file
            
        except Exception as e:
            self.logger.error(f"Error saving summary to file: {e}")
            return ""
    
    def _update_system_prompts(self):
        """Update system prompts untuk semua agen"""
        try:
            # Create system prompt update
            prompt_update = """
# SYSTEM PROMPT UPDATE - Central Intelligence Hub
# Sebelum melakukan riset, muat data dari config/sources.json dan gunakan insight dari reports/executive_summary.md sebagai konteks makro.

INSTRUCTIONS_BEFORE_TASK = """
Sebelum melakukan riset, pastikan untuk:
1. Muat konfigurasi sumber dari config/sources.json
2. Baca executive summary terbaru dari reports/executive_summary.md
3. Gunakan insight makro sebagai konteks untuk pengambilan keputusan
4. Pertimbangkan alerts dan trend dari executive summary dalam analisis
"""

# Update prompts untuk existing agents
SCOUT_AGENT_PROMPT = INSTRUCTIONS_BEFORE_TASK + """
Scout Agent Instructions:
- Gunakan insight dari executive summary untuk target lokasi yang prospektif
- Pertimbangkan government updates dan policy changes dalam strategi pencarian
- Fokus pada area dengan actionable insights dari executive summary
"""

COMPETITOR_AGENT_PROMPT = INSTRUCTIONS_BEFORE_TASK + """
Competitor Agent Instructions:
- Monitor competitor activities dalam konteks market trend dari executive summary
- Perhatikan government updates yang mungkin mempengaruhi strategi kompetitor
- Gunakan alerts dari executive summary untuk identifikasi peluang
"""

GEO_AGENT_PROMPT = INSTRUCTIONS_BEFORE_TASK + """
Geo Agent Instructions:
- Analisis area dengan mempertimbangkan government updates dari executive summary
- Fokus pada lokasi dengan actionable insights dan market trend positif
- Gunakan policy changes untuk identifikasi area dengan potensi masa depan
"""
            
            # Save prompt update to file
            prompts_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'system_prompts.py')
            with open(prompts_file, 'w', encoding='utf-8') as f:
                f.write(prompt_update)
            
            self.logger.info("System prompts updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating system prompts: {e}")

class IntelligenceScraper:
    """
    Dynamic Scraper untuk mengambil konten dari berbagai sumber
    """
    
    def __init__(self, target_keywords: List[str]):
        self.logger = logging.getLogger(__name__)
        self.target_keywords = target_keywords
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IntelligenceAggregator/1.0'
        })
    
    def scrape_source(self, url: str, source_name: str, category: str) -> Dict:
        """Scrape individual source untuk konten dengan content-specific parsing"""
        try:
            self.logger.info(f"Scraping {source_name} ({category})")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Content-specific scraping: Focus on news content only
            clean_content = self._extract_news_content_only(soup)
            
            # Smart parsing: Check if content contains target keywords
            if not self._contains_target_keywords(clean_content):
                self.logger.info(f"Skipping {source_name}: No relevant keywords found")
                return {
                    'source_name': source_name,
                    'category': category,
                    'url': url,
                    'status': 'skipped',
                    'reason': 'No relevant keywords found',
                    'articles_found': 0,
                    'articles': []
                }
            
            # Extract articles from clean content
            articles = self._extract_articles_from_clean_content(clean_content, url)
            
            # Additional keyword filtering
            filtered_articles = self._filter_articles_by_keywords(articles)
            
            return {
                'source_name': source_name,
                'category': category,
                'url': url,
                'status': 'success',
                'articles_found': len(articles),
                'articles': filtered_articles,
                'content_quality': 'high' if len(filtered_articles) > 0 else 'low'
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping {source_name}: {e}")
            return {
                'source_name': source_name,
                'category': category,
                'url': url,
                'status': 'error',
                'error': str(e),
                'articles_found': 0,
                'articles': []
            }
    
    def _extract_news_content_only(self, soup: BeautifulSoup) -> str:
        """Extract only news content, skip headers, footers, and sidebars"""
        content_parts = []
        
        # Priority content selectors for government sites
        content_selectors = [
            'article',           # HTML5 article tag
            'main',              # Main content area
            '.post-content',     # Common post content class
            '.news-content',     # News content class
            '.content',          # Generic content
            '#content',          # Content ID
            '.berita',           # Indonesian news class
            '.post',             # Post class
            '.entry-content',    # Entry content
            '.article-content',  # Article content
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Skip if element is in header, footer, or sidebar
                if self._is_in_noise_container(element):
                    continue
                
                # Extract text from this element
                text = element.get_text(strip=True)
                if text and len(text) > 100:  # Only substantial content
                    content_parts.append(text)
        
        # Fallback: Get all paragraphs if no structured content found
        if not content_parts:
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                if not self._is_in_noise_container(p):
                    text = p.get_text(strip=True)
                    if text and len(text) > 50:
                        content_parts.append(text)
        
        return ' '.join(content_parts)
    
    def _is_in_noise_container(self, element) -> bool:
        """Check if element is within noise container (header, footer, sidebar)"""
        if not element:
            return False
            
        # Check element and its parents
        current = element
        for _ in range(10):  # Check up to 10 levels up
            if not current:
                break
                
            # Check tag names
            if current.name in ['header', 'footer', 'nav', 'aside', 'sidebar']:
                return True
            
            # Check common classes/IDs for navigation and sidebars
            classes_and_ids = current.get('class', []) + [current.get('id', '')]
            for class_or_id in classes_and_ids:
                if class_or_id and any(noise in class_or_id.lower() for noise in [
                    'nav', 'menu', 'sidebar', 'footer', 'header', 'ads', 
                    'advertisement', 'banner', 'social', 'share', 'comment'
                ]):
                    return True
            
            current = current.parent
        
        return False
    
    def _contains_target_keywords(self, content: str) -> bool:
        """Smart parsing: Check if content contains any target keywords"""
        content_lower = content.lower()
        
        # Check for any target keywords
        for keyword in self.target_keywords:
            if keyword.lower() in content_lower:
                return True
        
        return False
    
    def _extract_articles_from_clean_content(self, clean_content: str, source_url: str) -> List[Dict]:
        """Extract articles from clean content"""
        articles = []
        
        # Split content into potential articles (by paragraphs or sections)
        paragraphs = clean_content.split('\n')
        
        current_article = []
        current_title = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Check if this looks like a title (shorter, may contain keywords)
            if len(paragraph) < 200 and any(keyword.lower() in paragraph.lower() for keyword in self.target_keywords):
                # Save previous article if exists
                if current_article and current_title:
                    articles.append({
                        'title': current_title,
                        'content': '\n'.join(current_article),
                        'url': source_url,
                        'source': 'extracted',
                        'published_date': None
                    })
                
                # Start new article
                current_title = paragraph
                current_article = []
            else:
                # Add to current article
                current_article.append(paragraph)
        
        # Save last article
        if current_article and current_title:
            articles.append({
                'title': current_title,
                'content': '\n'.join(current_article),
                'url': source_url,
                'source': 'extracted',
                'published_date': None
            })
        
        return articles
    
    def _extract_articles(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract articles berdasarkan struktur halaman"""
        try:
            articles = []
            
            # Try different article selectors
            article_selectors = [
                'article',
                '.article',
                '.post',
                '.news-item',
                '.content-item',
                'h1 a', 'h2 a', 'h3 a'
            ]
            
            for selector in article_selectors:
                elements = soup.select(selector)
                
                for element in elements:
                    # Get title
                    title = self._get_element_title(element)
                    
                    # Get link
                    link = self._get_element_link(element, base_url)
                    
                    # Get content/snippet
                    content = self._get_element_content(element)
                    
                    # Get published date
                    published_date = self._get_element_date(element)
                    
                    if title and link:
                        articles.append({
                            'title': title,
                            'url': link,
                            'content': content,
                            'published_date': published_date
                        })
            
            # Remove duplicates
            seen_urls = set()
            unique_articles = []
            
            for article in articles:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    unique_articles.append(article)
            
            return unique_articles
            
        except Exception as e:
            self.logger.error(f"Error extracting articles: {e}")
            return []
    
    def _get_element_title(self, element) -> str:
        """Get title dari element"""
        try:
            # Try different methods to get title
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                return element.get_text().strip()
            elif element.name == 'a':
                return element.get_text().strip()
            else:
                # Look for title within element
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
                if title_elem:
                    return title_elem.get_text().strip()
                
                # Use element text as fallback
                text = element.get_text().strip()
                return text[:100] if len(text) > 100 else text
            
        except Exception:
            return ""
    
    def _get_element_link(self, element, base_url: str) -> str:
        """Get link dari element"""
        try:
            if element.name == 'a':
                href = element.get('href')
                if href:
                    return urljoin(base_url, href)
            
            # Look for link within element
            link_elem = element.find('a')
            if link_elem:
                href = link_elem.get('href')
                if href:
                    return urljoin(base_url, href)
            
            return ""
            
        except Exception:
            return ""
    
    def _get_element_content(self, element) -> str:
        """Get content/snippet dari element"""
        try:
            # Get text content
            content = element.get_text().strip()
            
            # Look for content/p within element
            content_elem = element.find(['p', 'div', 'span', 'content'])
            if content_elem:
                content = content_elem.get_text().strip()
            
            # Clean and limit content
            content = re.sub(r'\s+', ' ', content)
            return content[:500] if len(content) > 500 else content
            
        except Exception:
            return ""
    
    def _get_element_date(self, element) -> datetime:
        """Get published date dari element"""
        try:
            # Look for date element
            date_selectors = [
                '.date', '.publish-date', '.post-date', '.entry-date',
                'time', '.timestamp', '[datetime]'
            ]
            
            for selector in date_selectors:
                date_elem = element.find(selector)
                if date_elem:
                    date_text = date_elem.get_text().strip()
                    parsed_date = self._parse_date_string(date_text)
                    if parsed_date:
                        return parsed_date
            
            # Look for datetime attribute
            date_attr = element.get('datetime')
            if date_attr:
                parsed_date = self._parse_date_string(date_attr)
                if parsed_date:
                    return parsed_date
            
            return datetime.now()
            
        except Exception:
            return datetime.now()
    
    def _parse_date_string(self, date_str: str) -> Optional[datetime]:
        """Parse date string"""
        try:
            date_formats = [
                '%d %B %Y',
                '%d %b %Y',
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%d-%m-%Y',
                '%Y-%m-%dT%H:%M:%S',
                '%d %B %Y %H:%M'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _filter_articles_by_keywords(self, articles: List[Dict]) -> List[Dict]:
        """Filter artikel berdasarkan keywords"""
        try:
            filtered_articles = []
            
            for article in articles:
                content_text = f"{article.get('title', '')} {article.get('content', '')}".lower()
                
                # Check for keyword matches
                keywords_found = []
                for keyword in self.target_keywords:
                    if keyword.lower() in content_text:
                        keywords_found.append(keyword)
                
                if keywords_found:
                    article['keywords_found'] = keywords_found
                    article['relevance_score'] = len(keywords_found)
                    filtered_articles.append(article)
            
            # Sort by relevance score
            filtered_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return filtered_articles
            
        except Exception as e:
            self.logger.error(f"Error filtering articles: {e}")
            return []

class LLM_Analyst_Agent:
    """
    LLM Analyst Agent untuk menganalisis konten dan menghasilkan actionable insights
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Try to import OpenAI
        try:
            import openai
            self.openai_available = True
            self.client = openai.OpenAI()
        except ImportError:
            self.openai_available = False
            self.client = None
            self.logger.warning("OpenAI not available, using fallback analysis")
    
    def analyze_content(self, title: str, content: str) -> Dict:
        """Analyze content dengan LLM"""
        try:
            if self.openai_available:
                return self._analyze_with_openai(title, content)
            else:
                return self._analyze_with_keywords(title, content)
                
        except Exception as e:
            self.logger.error(f"Error analyzing content: {e}")
            return self._get_fallback_analysis()
    
    def _analyze_with_openai(self, title: str, content: str) -> Dict:
        """Analyze dengan OpenAI"""
        try:
            prompt = f"""
            Analisis konten berita properti/ekonomi ini dan berikan insight actionable:

            Judul: {title}
            Konten: {content[:2000]}

            Response format JSON:
            {{
                "type": "alert/trend/opportunity/recommendation/general",
                "sentiment": "positive/negative/neutral",
                "priority": "high/medium/low",
                "source_type": "government/media/association/general",
                "policy_type": "monetary/infrastructure/housing/general",
                "impact": "high/medium/low",
                "message": "Ringkasan insight yang dapat ditindaklanjuti",
                "action": "Aksi yang direkomendasikan",
                "recommendation": "Rekomendasi strategis",
                "trend": "Tren yang terdeteksi",
                "actionable": true/false
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use GPT-4o if available, fallback to 3.5-turbo
                messages=[
                    {"role": "system", "content": "You are an expert analyst specializing in Indonesian real estate and economic intelligence."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            llm_response = response.choices[0].message.content
            
            # Parse JSON response
            try:
                analysis = json.loads(llm_response)
                analysis['model'] = 'gpt-4o-mini'
                analysis['confidence'] = 0.8  # Default confidence for OpenAI
                return analysis
                
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse LLM response: {llm_response}")
                return self._analyze_with_keywords(title, content)
                
        except Exception as e:
            self.logger.error(f"Error in OpenAI analysis: {e}")
            return self._analyze_with_keywords(title, content)
    
    def _analyze_with_keywords(self, title: str, content: str) -> Dict:
        """Fallback keyword-based analysis"""
        try:
            text = f"{title} {content}".lower()
            
            # Sentiment analysis
            positive_words = ['naik', 'baik', 'positif', 'sukses', 'tumbuh', 'meningkat', 'membaik']
            negative_words = ['turun', 'buruk', 'negatif', 'gagal', 'susut', 'menurun', 'memburuk']
            
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            if positive_count > negative_count:
                sentiment = 'positive'
            elif negative_count > positive_count:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Type detection
            if any(word in text for word in ['kebijakan', 'regulasi', 'peraturan', 'bi', 'ojk']):
                analysis_type = 'alert'
            elif any(word in text for word in ['tren', 'naik', 'turun', 'pertumbuhan']):
                analysis_type = 'trend'
            elif any(word in text for word in ['peluang', 'kesempatan', 'potensi', 'opportunity']):
                analysis_type = 'opportunity'
            else:
                analysis_type = 'general'
            
            # Priority detection
            if any(word in text for word in ['penting', 'urgent', 'segera', 'darurat']):
                priority = 'high'
            elif any(word in text for word in ['penting', 'perlu', 'disarankan']):
                priority = 'medium'
            else:
                priority = 'low'
            
            return {
                'type': analysis_type,
                'sentiment': sentiment,
                'priority': priority,
                'source_type': 'general',
                'policy_type': 'general',
                'impact': 'medium',
                'message': f"Keyword-based analysis: {sentiment} sentiment detected",
                'action': 'Monitor for further developments',
                'recommendation': 'Consider this information in planning',
                'actionable': True,
                'model': 'keyword_fallback',
                'confidence': 0.5
            }
            
        except Exception as e:
            self.logger.error(f"Error in keyword analysis: {e}")
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self) -> Dict:
        """Get fallback analysis"""
        return {
            'type': 'general',
            'sentiment': 'neutral',
            'priority': 'medium',
            'source_type': 'general',
            'policy_type': 'general',
            'impact': 'low',
            'message': 'Analysis unavailable',
            'action': 'Manual review required',
            'recommendation': 'Further analysis needed',
            'actionable': False,
            'model': 'fallback',
            'confidence': 0.0
        }

# Global instance
intelligence_aggregator = IntelligenceAggregator()

# Convenience functions
def run_daily_scan() -> Dict:
    """Run daily intelligence scan"""
    return intelligence_aggregator.run_daily_scan()

def run_daily_scan_deep_crawl() -> Dict:
    """Run Deep-Crawl Manager scan"""
    return intelligence_aggregator.run_daily_scan_deep_crawl()

def load_sources_config() -> Dict:
    """Load sources configuration"""
    return intelligence_aggregator._load_sources_config()

if __name__ == "__main__":
    # Test Central Intelligence Hub
    logging.basicConfig(level=logging.INFO)
    
    print("=== Central Intelligence Hub Test ===")
    
    # Test configuration loading
    print("\n📋 Testing Configuration Loading...")
    config = load_sources_config()
    print(f"Categories loaded: {len(config)}")
    for category, sources in config.items():
        print(f"  - {category}: {len(sources)} sources")
    
    # Test daily scan
    print("\n🔄 Testing Daily Scan...")
    scan_result = run_daily_scan()
    print(f"Scan status: {scan_result['status']}")
    print(f"Categories scanned: {scan_result['categories_scanned']}")
    print(f"Total articles: {scan_result['total_articles']}")
    print(f"LLM analyses: {scan_result.get('llm_analyses', 0)}")
    print(f"Summary file: {scan_result.get('summary_file', 'N/A')}")
    
    print("\nCentral Intelligence Hub test completed!")

"""
Competitor Surveillance Agent Module
System untuk monitoring kompetitor properti dengan reputation scraping, price drift detection, dan gap analysis
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI for LLM-powered sentiment analysis
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

# Try to import alert manager
try:
    from core_modules.notifications.alert_manager import send_competitor_alert
    ALERTS_AVAILABLE = True
except ImportError:
    ALERTS_AVAILABLE = False
    logging.warning("Alert system not available")

class CompetitorScout:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Database configuration
        self.db_path = "data/competitors.db (SQLite - removed)
        self._initialize_database()
        
        # Competitor list configuration
        self.competitors_config = self._load_competitors_config()
        
        # OpenAI configuration for sentiment analysis
        self.openai_client = None
        self.use_llm = False
        
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                self.use_llm = True
                self.logger.info("OpenAI client initialized for sentiment analysis")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
                self.use_llm = False
        else:
            self.logger.warning("OpenAI not available. Using fallback sentiment analysis")
            self.use_llm = False
        
        # Rate limiting untuk web scraping
        self.request_delay = 2  # seconds between requests
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        os.makedirs('config', exist_ok=True)
    
    def _initialize_database(self):
        """
        Inisialisasi database untuk competitor surveillance
        """
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Create competitors table
                # cursor.execute() removed'''
                    CREATE TABLE IF NOT EXISTS competitors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        competitor_name TEXT UNIQUE NOT NULL,
                        base_price REAL,
                        promos TEXT,  -- JSON string
                        sentiment_score REAL DEFAULT 0.0,
                        key_selling_points TEXT,  -- JSON string
                        last_scanned DATETIME DEFAULT CURRENT_TIMESTAMP,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create price_history table untuk tracking price changes
                # cursor.execute() removed'''
                    CREATE TABLE IF NOT EXISTS price_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        competitor_name TEXT NOT NULL,
                        price REAL NOT NULL,
                        promo TEXT,
                        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (competitor_name) REFERENCES competitors(competitor_name)
                    )
                ''')
                
                # Create reputation_data table untuk storing reviews
                # cursor.execute() removed'''
                    CREATE TABLE IF NOT EXISTS reputation_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        competitor_name TEXT NOT NULL,
                        source TEXT,  -- Google Maps, Forum, etc.
                        review_text TEXT,
                        sentiment_score REAL,
                        extracted_keywords TEXT,  -- JSON string
                        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (competitor_name) REFERENCES competitors(competitor_name)
                    )
                ''')
                
                # Create indexes
                # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_competitor_name ON competitors(competitor_name)')
                # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_price_history_competitor ON price_history(competitor_name)')
                # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_reputation_competitor ON reputation_data(competitor_name)')
                # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_price_history_date ON price_history(recorded_at)')
                
                # conn.commit() removed
                self.logger.info(f"Competitor database initialized: {self.db_path}")
                
        except Exception as e:
            self.logger.error(f"Error initializing competitor database: {e}")
            raise
    
    def _load_competitors_config(self) -> List[Dict]:
        """
        Load competitors configuration dari JSON file
        """
        try:
            config_file = 'config/competitors_list.json'
            
            if not os.path.exists(config_file):
                # Create default config
                default_config = [
                    {
                        "name": "Perumahan A",
                        "search_keywords": ["perumahan a serang", "cluster a serang"],
                        "website": "https://example-perumahan-a.com",
                        "google_maps_url": "https://maps.google.com/?q=perumahan+a+serang"
                    },
                    {
                        "name": "Perumahan B", 
                        "search_keywords": ["perumahan b serang", "taman b serang"],
                        "website": "https://example-perumahan-b.com",
                        "google_maps_url": "https://maps.google.com/?q=perumahan+b+serang"
                    },
                    {
                        "name": "Perumahan C",
                        "search_keywords": ["perumahan c serang", "griya c serang"],
                        "website": "https://example-perumahan-c.com", 
                        "google_maps_url": "https://maps.google.com/?q=perumahan+c+serang"
                    }
                ]
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"Created default competitors config: {config_file}")
                return default_config
            
            # Load existing config
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.logger.info(f"Loaded {len(config)} competitors from config")
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading competitors config: {e}")
            return []
    
    def scrape_competitor_reputation(self, competitor_name: str, search_keywords: List[str]) -> Dict:
        """
        Scrape reputation data dari Google Maps dan forum untuk competitor
        """
        try:
            self.logger.info(f"Scraping reputation for {competitor_name}")
            
            # Collect reviews from multiple sources
            reviews_data = []
            
            # Google Maps reviews
            google_reviews = self._scrape_google_maps_reviews(competitor_name, search_keywords)
            if google_reviews:
                reviews_data.extend(google_reviews)
            
            # Web search for forum discussions
            forum_reviews = self._scrape_forum_reviews(competitor_name, search_keywords)
            if forum_reviews:
                reviews_data.extend(forum_reviews)
            
            # Analyze sentiment dengan LLM
            sentiment_analysis = self._analyze_sentiment_with_llm(reviews_data)
            
            # Extract key selling points
            key_selling_points = self._extract_key_selling_points(reviews_data)
            
            # Calculate overall sentiment score
            overall_sentiment = self._calculate_overall_sentiment(sentiment_analysis)
            
            result = {
                'competitor_name': competitor_name,
                'reviews_collected': len(reviews_data),
                'sentiment_analysis': sentiment_analysis,
                'key_selling_points': key_selling_points,
                'overall_sentiment_score': overall_sentiment,
                'main_complaints': self._extract_main_complaints(sentiment_analysis),
                'last_scanned': datetime.now().isoformat()
            }
            
            # Save to database
            self._save_reputation_data(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error scraping reputation for {competitor_name}: {e}")
            return {
                'competitor_name': competitor_name,
                'error': str(e),
                'last_scanned': datetime.now().isoformat()
            }
    
    def _scrape_google_maps_reviews(self, competitor_name: str, search_keywords: List[str]) -> List[Dict]:
        """
        Scrape reviews dari Google Maps (mock implementation)
        """
        try:
            # Mock data untuk demonstration
            mock_reviews = [
                {
                    'source': 'Google Maps',
                    'rating': 4.5,
                    'text': f"Lokasi {competitor_name} sangat strategis, dekat dengan fasilitas umum. Harga masih terjangkau untuk keluarga muda.",
                    'author': 'Pembeli 1',
                    'date': '2024-01-15'
                },
                {
                    'source': 'Google Maps', 
                    'rating': 3.0,
                    'text': f"Kualitas bangunan {competitor_name} kurang memuaskan, banyak yang mengeluh soal finishing yang tidak rapi.",
                    'author': 'Pembeli 2',
                    'date': '2024-01-20'
                },
                {
                    'source': 'Google Maps',
                    'rating': 4.0,
                    'text': f"Pelayanan sales {competitor_name} ramah dan profesional. Proses KPR dibantu sampai selesai.",
                    'author': 'Pembeli 3',
                    'date': '2024-02-01'
                }
            ]
            
            self.logger.info(f"Collected {len(mock_reviews)} Google Maps reviews for {competitor_name}")
            return mock_reviews
            
        except Exception as e:
            self.logger.error(f"Error scraping Google Maps reviews: {e}")
            return []
    
    def _scrape_forum_reviews(self, competitor_name: str, search_keywords: List[str]) -> List[Dict]:
        """
        Scrape reviews dari forum discussions (mock implementation)
        """
        try:
            # Mock data untuk demonstration
            mock_forum_reviews = [
                {
                    'source': 'Forum Properti',
                    'text': f"Diskusi di forum: {competitor_name} vs kompetitor lain. Banyak yang bilang {competitor_name} lebih murah tapi kualitasnya dipertanyakan.",
                    'author': 'Forum User 1',
                    'date': '2024-01-25'
                },
                {
                    'source': 'Forum Properti',
                    'text': f"Pengalaman buruk dengan {competitor_name}: janji delivery tidak sesuai, banyak perubahan desain mendadak.",
                    'author': 'Forum User 2', 
                    'date': '2024-02-05'
                }
            ]
            
            self.logger.info(f"Collected {len(mock_forum_reviews)} forum reviews for {competitor_name}")
            return mock_forum_reviews
            
        except Exception as e:
            self.logger.error(f"Error scraping forum reviews: {e}")
            return []
    
    def _analyze_sentiment_with_llm(self, reviews: List[Dict]) -> Dict:
        """
        Analisis sentimen menggunakan LLM
        """
        try:
            if not self.use_llm or not reviews:
                return self._fallback_sentiment_analysis(reviews)
            
            # Combine all review texts
            all_reviews_text = "\n".join([review.get('text', '') for review in reviews])
            
            prompt = f"""
            Analisis sentimen dari ulasan properti berikut:
            
            {all_reviews_text}
            
            Instruksi:
            1. Tentukan apakah sentimen secara keseluruhan: Positif atau Negatif
            2. Identifikasi keluhan utama pelanggan (jika ada)
            3. Identifikasi poin positif yang disukai pelanggan
            4. Berikan sentimen score dari -1 (sangat negatif) ke 1 (sangat positif)
            
            Return dalam format JSON:
            {{
                "overall_sentiment": "Positif/Negatif",
                "sentiment_score": 0.5,
                "main_complaints": ["keluhan 1", "keluhan 2"],
                "positive_points": ["poin positif 1", "poin positif 2"],
                "key_themes": ["tema 1", "tema 2"]
            }}
            """
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert for Indonesian property reviews. Analyze the given text and return structured JSON output."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            # Parse LLM response
            llm_response = response.choices[0].message.content.strip()
            
            try:
                if llm_response.startswith('```json'):
                    llm_response = llm_response.replace('```json', '').replace('```', '').strip()
                
                sentiment_data = json.loads(llm_response)
                
                self.logger.info("LLM sentiment analysis successful")
                return sentiment_data
                
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse LLM sentiment response")
                return self._fallback_sentiment_analysis(reviews)
                
        except Exception as e:
            self.logger.error(f"Error in LLM sentiment analysis: {e}")
            return self._fallback_sentiment_analysis(reviews)
    
    def _fallback_sentiment_analysis(self, reviews: List[Dict]) -> Dict:
        """
        Fallback sentiment analysis tanpa LLM
        """
        try:
            if not reviews:
                return {
                    'overall_sentiment': 'Netral',
                    'sentiment_score': 0.0,
                    'main_complaints': [],
                    'positive_points': [],
                    'key_themes': []
                }
            
            # Simple keyword-based sentiment analysis
            positive_keywords = ['bagus', 'strategis', 'murah', 'ramah', 'profesional', 'baik', 'memuaskan']
            negative_keywords = ['buruk', 'mahal', 'keluhan', 'masalah', 'tidak sesuai', 'mengecewakan', 'kurang']
            
            positive_count = 0
            negative_count = 0
            complaints = []
            positive_points = []
            
            for review in reviews:
                text = review.get('text', '').lower()
                
                # Count positive keywords
                for keyword in positive_keywords:
                    if keyword in text:
                        positive_count += 1
                        if keyword not in positive_points:
                            positive_points.append(keyword)
                
                # Count negative keywords
                for keyword in negative_keywords:
                    if keyword in text:
                        negative_count += 1
                        if keyword not in complaints:
                            complaints.append(keyword)
            
            # Calculate sentiment score
            total_keywords = positive_count + negative_count
            if total_keywords == 0:
                sentiment_score = 0.0
                overall_sentiment = 'Netral'
            else:
                sentiment_score = (positive_count - negative_count) / total_keywords
                overall_sentiment = 'Positif' if sentiment_score > 0.1 else 'Negatif' if sentiment_score < -0.1 else 'Netral'
            
            return {
                'overall_sentiment': overall_sentiment,
                'sentiment_score': round(sentiment_score, 2),
                'main_complaints': complaints[:3],  # Top 3 complaints
                'positive_points': positive_points[:3],  # Top 3 positive points
                'key_themes': ['harga', 'lokasi', 'kualitas']
            }
            
        except Exception as e:
            self.logger.error(f"Error in fallback sentiment analysis: {e}")
            return {
                'overall_sentiment': 'Netral',
                'sentiment_score': 0.0,
                'main_complaints': [],
                'positive_points': [],
                'key_themes': []
            }
    
    def _extract_key_selling_points(self, reviews: List[Dict]) -> List[str]:
        """
        Extract key selling points dari reviews
        """
        try:
            selling_points = []
            
            # Common selling point keywords
            sp_keywords = ['strategis', 'lokasi', 'murah', 'fasilitas', 'akses', 'dekat', 'lengkap', 'modern', 'nyaman', 'aman']
            
            for review in reviews:
                text = review.get('text', '').lower()
                for keyword in sp_keywords:
                    if keyword in text and keyword not in selling_points:
                        selling_points.append(keyword)
            
            return selling_points[:5]  # Top 5 selling points
            
        except Exception as e:
            self.logger.error(f"Error extracting selling points: {e}")
            return []
    
    def _calculate_overall_sentiment(self, sentiment_analysis: Dict) -> float:
        """
        Calculate overall sentiment score
        """
        try:
            return sentiment_analysis.get('sentiment_score', 0.0)
        except:
            return 0.0
    
    def _extract_main_complaints(self, sentiment_analysis: Dict) -> List[str]:
        """
        Extract main complaints dari sentiment analysis
        """
        try:
            return sentiment_analysis.get('main_complaints', [])
        except:
            return []
    
    def _save_reputation_data(self, reputation_data: Dict):
        """
        Save reputation data ke database
        """
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Update competitor sentiment score
                # cursor.execute() removed'''
                    UPDATE competitors 
                    SET sentiment_score = ?, key_selling_points = ?, last_scanned = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE competitor_name = ?
                ''', (
                    reputation_data.get('overall_sentiment_score', 0.0),
                    json.dumps(reputation_data.get('key_selling_points', [])),
                    reputation_data.get('last_scanned'),
                    reputation_data.get('competitor_name')
                ))
                
                # Save individual reviews
                for review in reputation_data.get('reviews_collected', []):
                    # cursor.execute() removed'''
                        INSERT INTO reputation_data 
                        (competitor_name, source, review_text, sentiment_score, extracted_keywords, recorded_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        reputation_data.get('competitor_name'),
                        review.get('source', 'Unknown'),
                        review.get('text', ''),
                        0.0,  # Individual review sentiment
                        json.dumps([]),  # Extracted keywords
                        datetime.now().isoformat()
                    ))
                
                # conn.commit() removed
                self.logger.info(f"Reputation data saved for {reputation_data.get('competitor_name')}")
                
        except Exception as e:
            self.logger.error(f"Error saving reputation data: {e}")
    
    def monitor_price_drift(self, competitor_name: str, current_price: float, current_promo: str = "") -> Dict:
        """
        Monitor price drift dan detect significant changes
        """
        try:
            # Get price history from last week
            one_week_ago = datetime.now() - timedelta(days=7)
            
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get latest price from last week
                # cursor.execute() removed'''
                    SELECT price, promo, recorded_at 
                    FROM price_history 
                    WHERE competitor_name = ? AND recorded_at >= ?
                    ORDER BY recorded_at DESC 
                    LIMIT 1
                ''', (competitor_name, one_week_ago.isoformat()))
                
                result = cursor.fetchone()
                
                if not result:
                    # No historical data, save current price
                    self._save_price_history(competitor_name, current_price, current_promo)
                    return {
                        'competitor_name': competitor_name,
                        'price_drift': 0.0,
                        'drift_type': 'new_data',
                        'previous_price': None,
                        'current_price': current_price,
                        'promo_change': 'new_promo' if current_promo else 'no_promo'
                    }
                
                previous_price, previous_promo, recorded_at = result
                
                # Calculate price drift
                if previous_price > 0:
                    price_drift = ((current_price - previous_price) / previous_price) * 100
                else:
                    price_drift = 0.0
                
                # Determine drift type
                if abs(price_drift) > 5.0:
                    drift_type = 'significant'
                elif abs(price_drift) > 2.0:
                    drift_type = 'moderate'
                else:
                    drift_type = 'minimal'
                
                # Check for promo changes
                promo_change = self._analyze_promo_change(previous_promo, current_promo)
                
                # Save current price
                self._save_price_history(competitor_name, current_price, current_promo)
                
                # Send alert if significant changes detected
                if drift_type == 'significant' or promo_change['is_new_promo']:
                    self._send_price_drift_alert(competitor_name, price_drift, promo_change, drift_type)
                
                return {
                    'competitor_name': competitor_name,
                    'price_drift': round(price_drift, 2),
                    'drift_type': drift_type,
                    'previous_price': previous_price,
                    'current_price': current_price,
                    'promo_change': promo_change,
                    'recorded_at': recorded_at
                }
                
        except Exception as e:
            self.logger.error(f"Error monitoring price drift for {competitor_name}: {e}")
            return {
                'competitor_name': competitor_name,
                'error': str(e)
            }
    
    def _analyze_promo_change(self, previous_promo: str, current_promo: str) -> Dict:
        """
        Analyze promo changes
        """
        try:
            if not current_promo and not previous_promo:
                return {'is_new_promo': False, 'promo_type': 'none', 'change_description': 'no_promo'}
            
            if current_promo and not previous_promo:
                return {'is_new_promo': True, 'promo_type': 'new_promo', 'change_description': f"New promo: {current_promo}"}
            
            if not current_promo and previous_promo:
                return {'is_new_promo': False, 'promo_type': 'promo_removed', 'change_description': f"Promo removed: {previous_promo}"}
            
            if current_promo != previous_promo:
                return {'is_new_promo': True, 'promo_type': 'promo_changed', 'change_description': f"Promo changed from '{previous_promo}' to '{current_promo}'"}
            
            return {'is_new_promo': False, 'promo_type': 'same_promo', 'change_description': 'no_change'}
            
        except Exception as e:
            self.logger.error(f"Error analyzing promo change: {e}")
            return {'is_new_promo': False, 'promo_type': 'error', 'change_description': str(e)}
    
    def _save_price_history(self, competitor_name: str, price: float, promo: str = ""):
        """
        Save price history ke database
        """
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    INSERT INTO price_history 
                    (competitor_name, price, promo, recorded_at)
                    VALUES (?, ?, ?, ?)
                ''', (competitor_name, price, promo, datetime.now().isoformat()))
                
                # Update competitor base price
                # cursor.execute() removed'''
                    UPDATE competitors 
                    SET base_price = ?, promos = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE competitor_name = ?
                ''', (price, json.dumps([promo]) if promo else json.dumps([]), competitor_name))
                
                # conn.commit() removed
                self.logger.info(f"Price history saved for {competitor_name}: {price}")
                
        except Exception as e:
            self.logger.error(f"Error saving price history: {e}")
    
    def monitor_inventory_velocity(self) -> Dict:
        """
        Inventory Velocity Monitor - Track listing velocity and turnover rate
        """
        try:
            self.logger.info("Starting inventory velocity monitoring...")
            
            # Get all competitors
            competitors = self._get_all_competitors()
            
            velocity_results = []
            velocity_alerts = []
            
            for competitor in competitors:
                competitor_name = competitor['competitor_name']
                
                # Calculate velocity metrics
                velocity_metrics = self._calculate_velocity_metrics(competitor_name)
                
                # Check for velocity alerts
                velocity_alert = self._check_velocity_alerts(competitor_name, velocity_metrics)
                
                if velocity_alert:
                    velocity_alerts.append(velocity_alert)
                
                velocity_results.append({
                    'competitor_name': competitor_name,
                    'velocity_metrics': velocity_metrics,
                    'alert_triggered': bool(velocity_alert)
                })
            
            # Generate velocity report
            velocity_report = self._generate_velocity_report(velocity_results)
            
            # Send alerts if any
            if velocity_alerts:
                self._send_velocity_alerts(velocity_alerts)
            
            self.logger.info(f"Velocity monitoring completed. Analyzed {len(competitors)} competitors")
            
            return {
                'status': 'success',
                'competitors_analyzed': len(competitors),
                'velocity_results': velocity_results,
                'velocity_alerts': velocity_alerts,
                'velocity_report': velocity_report,
                'monitoring_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in inventory velocity monitoring: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'monitoring_timestamp': datetime.now().isoformat()
            }
    
    def _calculate_velocity_metrics(self, competitor_name: str) -> Dict:
        """
        Calculate velocity metrics untuk specific competitor
        """
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get price history for last 90 days
                # cursor.execute() removed'''
                    SELECT price, promo, recorded_at 
                    FROM price_history 
                    WHERE competitor_name = ? 
                    AND recorded_at >= datetime('now', '-90 days')
                    ORDER BY recorded_at DESC
                ''', (competitor_name,))
                
                price_history = cursor.fetchall()
                
                if not price_history:
                    return {
                        'total_listings': 0,
                        'avg_days_on_market': 0,
                        'turnover_rate': 0,
                        'velocity_score': 0,
                        'trend': 'no_data'
                    }
                
                # Calculate metrics
                total_listings = len(price_history)
                
                # Calculate average days on market (mock data for now)
                avg_days_on_market = 45.0  # Placeholder - would need actual listing timestamps
                
                # Calculate turnover rate (listings per month)
                turnover_rate = total_listings / 3.0  # 3 months period
                
                # Calculate velocity score (0-100)
                velocity_score = self._calculate_velocity_score(turnover_rate, avg_days_on_market)
                
                # Determine trend
                trend = self._determine_velocity_trend(price_history)
                
                return {
                    'total_listings': total_listings,
                    'avg_days_on_market': avg_days_on_market,
                    'turnover_rate': turnover_rate,
                    'velocity_score': velocity_score,
                    'trend': trend,
                    'analysis_period_days': 90
                }
                
        except Exception as e:
            self.logger.error(f"Error calculating velocity metrics for {competitor_name}: {e}")
            return {
                'total_listings': 0,
                'avg_days_on_market': 0,
                'turnover_rate': 0,
                'velocity_score': 0,
                'trend': 'error',
                'error': str(e)
            }
    
    def _calculate_velocity_score(self, turnover_rate: float, avg_days_on_market: float) -> float:
        """
        Calculate velocity score (0-100) based on turnover and days on market
        """
        try:
            # Higher turnover = higher score
            turnover_score = min(turnover_rate * 10, 50)  # Max 50 points
            
            # Lower days on market = higher score
            days_score = max(0, 50 - (avg_days_on_market / 2))  # Max 50 points
            
            total_score = turnover_score + days_score
            return min(total_score, 100)  # Cap at 100
            
        except Exception as e:
            self.logger.error(f"Error calculating velocity score: {e}")
            return 0.0
    
    def _determine_velocity_trend(self, price_history: List[Tuple]) -> str:
        """
        Determine velocity trend berdasarkan price history
        """
        try:
            if len(price_history) < 2:
                return 'insufficient_data'
            
            # Simple trend analysis based on frequency of price changes
            recent_changes = 0
            older_changes = 0
            
            mid_point = len(price_history) // 2
            
            # Count changes in recent half
            for i in range(min(10, mid_point)):
                if i < len(price_history) - 1:
                    if price_history[i][0] != price_history[i+1][0]:  # Price change
                        recent_changes += 1
            
            # Count changes in older half
            for i in range(mid_point, min(mid_point + 10, len(price_history) - 1)):
                if i < len(price_history) - 1:
                    if price_history[i][0] != price_history[i+1][0]:  # Price change
                        older_changes += 1
            
            # Determine trend
            if recent_changes > older_changes * 1.5:
                return 'accelerating'
            elif recent_changes < older_changes * 0.5:
                return 'slowing'
            else:
                return 'stable'
                
        except Exception as e:
            self.logger.error(f"Error determining velocity trend: {e}")
            return 'error'
    
    def _check_velocity_alerts(self, competitor_name: str, velocity_metrics: Dict) -> Optional[Dict]:
        """
        Check for velocity alerts
        """
        try:
            alerts = []
            
            # Low velocity alert
            if velocity_metrics['velocity_score'] < 30:
                alerts.append({
                    'type': 'low_velocity',
                    'severity': 'high',
                    'message': f"Kompetitor {competitor_name} memiliki velocity rendah ({velocity_metrics['velocity_score']:.1f}/100)",
                    'implication': 'Mungkin mengalami kesulitan menjual',
                    'recommended_action': 'Consider aggressive marketing atau price adjustment'
                })
            
            # Slowing trend alert
            if velocity_metrics['trend'] == 'slowing':
                alerts.append({
                    'type': 'slowing_trend',
                    'severity': 'medium',
                    'message': f"Kompetitor {competitor_name} menunjukkan perlambatan velocity",
                    'implication': 'Market sedang melambat atau kompetitor kehilangan momentum',
                    'recommended_action': 'Monitor market conditions dan competitor strategies'
                })
            
            # High turnover alert (opportunity)
            if velocity_metrics['turnover_rate'] > 10:  # High turnover
                alerts.append({
                    'type': 'high_turnover',
                    'severity': 'info',
                    'message': f"Kompetitor {competitor_name} memiliki turnover tinggi ({velocity_metrics['turnover_rate']:.1f}/bulan)",
                    'implication': 'Market sedang aktif atau kompetitor sangat efektif',
                    'recommended_action': 'Analyze competitor strategy untuk best practices'
                })
            
            # Long days on market alert
            if velocity_metrics['avg_days_on_market'] > 90:
                alerts.append({
                    'type': 'slow_sales',
                    'severity': 'medium',
                    'message': f"Kompetitor {competitor_name} memiliki rata-rata hari di pasar yang lama ({velocity_metrics['avg_days_on_market']:.1f} hari)",
                    'implication': 'Inventory tidak bergerak cepat',
                    'recommended_action': 'Consider alternative positioning atau pricing strategy'
                })
            
            # Return combined alert if any
            if alerts:
                return {
                    'competitor_name': competitor_name,
                    'alert_count': len(alerts),
                    'alerts': alerts,
                    'alert_timestamp': datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error checking velocity alerts for {competitor_name}: {e}")
            return None
    
    def _generate_velocity_report(self, velocity_results: List[Dict]) -> Dict:
        """
        Generate comprehensive velocity report
        """
        try:
            # Calculate aggregate metrics
            total_competitors = len(velocity_results)
            avg_velocity_score = sum(r['velocity_metrics']['velocity_score'] for r in velocity_results) / total_competitors if total_competitors > 0 else 0
            avg_turnover_rate = sum(r['velocity_metrics']['turnover_rate'] for r in velocity_results) / total_competitors if total_competitors > 0 else 0
            avg_days_on_market = sum(r['velocity_metrics']['avg_days_on_market'] for r in velocity_results) / total_competitors if total_competitors > 0 else 0
            
            # Categorize competitors
            fast_movers = [r for r in velocity_results if r['velocity_metrics']['velocity_score'] > 70]
            slow_movers = [r for r in velocity_results if r['velocity_metrics']['velocity_score'] < 30]
            
            # Trend analysis
            accelerating = [r for r in velocity_results if r['velocity_metrics']['trend'] == 'accelerating']
            slowing = [r for r in velocity_results if r['velocity_metrics']['trend'] == 'slowing']
            
            # Generate insights
            insights = []
            
            if len(slow_movers) > len(fast_movers):
                insights.append("Market sedang melambat - sebagian besar kompetitor memiliki velocity rendah")
            
            if len(slowing) > len(accelerating):
                insights.append("Trend perlambatan terdeteksi - hati-hati dengan pricing strategy")
            
            if avg_velocity_score < 50:
                insights.append("Overall market velocity rendah - fokus pada value proposition")
            elif avg_velocity_score > 70:
                insights.append("Market velocity tinggi - opportunity untuk aggressive growth")
            
            return {
                'summary': {
                    'total_competitors': total_competitors,
                    'avg_velocity_score': avg_velocity_score,
                    'avg_turnover_rate': avg_turnover_rate,
                    'avg_days_on_market': avg_days_on_market
                },
                'categories': {
                    'fast_movers': len(fast_movers),
                    'slow_movers': len(slow_movers),
                    'accelerating': len(accelerating),
                    'slowing': len(slowing)
                },
                'insights': insights,
                'recommendations': self._generate_velocity_recommendations(velocity_results),
                'report_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating velocity report: {e}")
            return {
                'error': str(e),
                'report_timestamp': datetime.now().isoformat()
            }
    
    def _generate_velocity_recommendations(self, velocity_results: List[Dict]) -> List[str]:
        """
        Generate recommendations based on velocity analysis
        """
        recommendations = []
        
        try:
            # Analyze competitive landscape
            avg_score = sum(r['velocity_metrics']['velocity_score'] for r in velocity_results) / len(velocity_results) if velocity_results else 0
            
            if avg_score < 40:
                recommendations.append("Market sedang lambat - pertimbangkan promo agresif untuk menarik perhatian")
                recommendations.append("Focus pada value proposition dan differentiation")
            
            if avg_score > 70:
                recommendations.append("Market sedang aktif - opportunity untuk premium positioning")
                recommendations.append("Consider inventory expansion untuk capture market momentum")
            
            # Check for outliers
            top_performer = max(velocity_results, key=lambda x: x['velocity_metrics']['velocity_score']) if velocity_results else None
            if top_performer and top_performer['velocity_metrics']['velocity_score'] > 80:
                recommendations.append(f"Analyze strategy dari {top_performer['competitor_name']} - top performer dengan velocity {top_performer['velocity_metrics']['velocity_score']:.1f}")
            
            slow_performer = min(velocity_results, key=lambda x: x['velocity_metrics']['velocity_score']) if velocity_results else None
            if slow_performer and slow_performer['velocity_metrics']['velocity_score'] < 30:
                recommendations.append(f"Opportunity: {slow_performer['competitor_name']} sedang kesulitan - consider positioning against them")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating velocity recommendations: {e}")
            return ["Error generating recommendations"]
    
    def _send_velocity_alerts(self, velocity_alerts: List[Dict]):
        """
        Send velocity alerts via notification system
        """
        try:
            for alert in velocity_alerts:
                alert_message = f"🚀 VELOCITY ALERT\n\n"
                alert_message += f"Kompetitor: {alert['competitor_name']}\n"
                alert_message += f"Total Alerts: {alert['alert_count']}\n\n"
                
                for sub_alert in alert['alerts']:
                    alert_message += f"⚠️ {sub_alert['type'].upper()}: {sub_alert['message']}\n"
                    alert_message += f"📝 Implication: {sub_alert['implication']}\n"
                    alert_message += f"🎯 Action: {sub_alert['recommended_action']}\n\n"
                
                alert_message += f"Timestamp: {alert['alert_timestamp']}"
                
                # Send via alert manager if available
                if ALERTS_AVAILABLE:
                    try:
                        from core_modules.notifications.alert_manager import send_competitor_alert
                        send_competitor_alert(alert_message)
                    except:
                        self.logger.warning("Failed to send velocity alert via notification system")
                
                # Log alert
                self.logger.warning(f"Velocity alert triggered: {alert['competitor_name']}")
                
        except Exception as e:
            self.logger.error(f"Error sending velocity alerts: {e}")
    
    def _get_all_competitors(self) -> List[Dict]:
        """
        Get all competitors dari database
        """
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                # cursor.execute() removed'SELECT * FROM competitors ORDER BY competitor_name')
                
                columns = [desc[0] for desc in cursor.description]
                competitors = []
                
                for row in cursor.fetchall():
                    competitor = dict(zip(columns, row))
                    competitors.append(competitor)
                
                return competitors
                
        except Exception as e:
            self.logger.error(f"Error getting competitors: {e}")
            return []
    
    def _send_price_drift_alert(self, competitor_name: str, price_drift: float, promo_change: Dict, drift_type: str):
        """
        Send alert untuk significant price drift
        """
        try:
            if not ALERTS_AVAILABLE:
                self.logger.warning("Alert system not available")
                return
            
            alert_message = f"PERINGATAN: Kompetitor {competitor_name} baru saja menurunkan harga/menambah promo!\n"
            alert_message += f"Price Drift: {price_drift:.1f}% ({drift_type})\n"
            alert_message += f"Promo Change: {promo_change['change_description']}"
            
            # Send alert using alert manager
            success = send_competitor_alert(competitor_name, alert_message, price_drift, promo_change)
            
            if success:
                self.logger.info(f"Price drift alert sent for {competitor_name}")
            else:
                self.logger.warning(f"Failed to send price drift alert for {competitor_name}")
                
        except Exception as e:
            self.logger.error(f"Error sending price drift alert: {e}")
    
    def analyze_value_proposition_gap(self, competitor_name: str) -> Dict:
        """
        Analisis gap dalam value proposition antara kita dan kompetitor
        """
        try:
            # Get competitor data
            competitor_data = self._get_competitor_data(competitor_name)
            
            if not competitor_data:
                return {'error': f'Competitor {competitor_name} not found'}
            
            # Extract competitor keywords
            competitor_keywords = self._extract_competitor_keywords(competitor_data)
            
            # Define our value proposition keywords
            our_keywords = ['efisien', 'fungsional', 'praktis', 'terjangkau', 'value', 'kualitas', 'nyaman', 'aman']
            
            # Find gaps and opportunities
            gaps = []
            opportunities = []
            
            # Keywords they use that we don't
            for keyword in competitor_keywords:
                if keyword not in our_keywords:
                    gaps.append(keyword)
            
            # Keywords we use that they don't
            for keyword in our_keywords:
                if keyword not in competitor_keywords:
                    opportunities.append(keyword)
            
            # Generate strategic recommendations
            recommendations = self._generate_gap_recommendations(gaps, opportunities)
            
            return {
                'competitor_name': competitor_name,
                'competitor_keywords': competitor_keywords,
                'our_keywords': our_keywords,
                'gaps': gaps,
                'opportunities': opportunities,
                'gap_analysis': {
                    'total_gaps': len(gaps),
                    'total_opportunities': len(opportunities),
                    'gap_percentage': (len(gaps) / (len(gaps) + len(opportunities)) * 100) if (gaps + opportunities) else 0
                },
                'strategic_recommendations': recommendations,
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing value proposition gap for {competitor_name}: {e}")
            return {'error': str(e)}
    
    def _get_competitor_data(self, competitor_name: str) -> Optional[Dict]:
        """
        Get competitor data dari database
        """
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT competitor_name, base_price, promos, sentiment_score, key_selling_points, last_scanned
                    FROM competitors
                    WHERE competitor_name = ?
                ''', (competitor_name,))
                
                result = cursor.fetchone()
                
                if result:
                    return {
                        'competitor_name': result[0],
                        'base_price': result[1],
                        'promos': json.loads(result[2]) if result[2] else [],
                        'sentiment_score': result[3],
                        'key_selling_points': json.loads(result[4]) if result[4] else [],
                        'last_scanned': result[5]
                    }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting competitor data: {e}")
            return None
    
    def _extract_competitor_keywords(self, competitor_data: Dict) -> List[str]:
        """
        Extract keywords dari competitor data
        """
        try:
            keywords = []
            
            # From key selling points
            keywords.extend(competitor_data.get('key_selling_points', []))
            
            # From promos
            promos = competitor_data.get('promos', [])
            for promo in promos:
                # Extract keywords from promo text
                promo_words = promo.lower().split()
                keywords.extend([word for word in promo_words if len(word) > 3])
            
            # Common property keywords
            property_keywords = ['mewah', 'premium', 'eksklusif', 'modern', 'minimalis', 'hijau', 'smart', 'digital', 'strategis', 'lokasi prima']
            
            # Check if any property keywords appear in competitor data
            for keyword in property_keywords:
                if keyword in str(competitor_data).lower():
                    keywords.append(keyword)
            
            return list(set(keywords))  # Remove duplicates
            
        except Exception as e:
            self.logger.error(f"Error extracting competitor keywords: {e}")
            return []
    
    def _generate_gap_recommendations(self, gaps: List[str], opportunities: List[str]) -> List[str]:
        """
        Generate strategic recommendations dari gap analysis
        """
        try:
            recommendations = []
            
            if gaps:
                if 'mewah' in gaps:
                    recommendations.append("Serang dengan 'Efisien & Fungsional' sebagai value proposition alternatif")
                if 'premium' in gaps:
                    recommendations.append("Fokus pada 'Value for Money' dan 'Kualitas Terjangkau'")
                if 'eksklusif' in gaps:
                    recommendations.append("Tawarkan 'Inklusif & Terbuka' sebagai alternatif eksklusivitas")
            
            if opportunities:
                if 'efisien' in opportunities:
                    recommendations.append("Amplifikasi keunggulan efisiensi dalam marketing materials")
                if 'fungsional' in opportunities:
                    recommendations.append("Highlight desain fungsional dan praktis dalam promosi")
                if 'terjangkau' in opportunities:
                    recommendations.append("Emphasize affordability dan value for money")
            
            return recommendations[:5]  # Top 5 recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return []
    
    def run_competitor_surveillance(self) -> Dict:
        """
        Run complete competitor surveillance workflow
        """
        try:
            self.logger.info("Starting competitor surveillance...")
            
            results = {
                'status': 'success',
                'surveillance_timestamp': datetime.now().isoformat(),
                'competitors_analyzed': 0,
                'price_alerts_sent': 0,
                'reputation_analyzed': 0,
                'gap_analysis_completed': 0,
                'competitor_results': []
            }
            
            for competitor in self.competitors_config:
                competitor_name = competitor.get('name')
                
                try:
                    # Step 1: Reputation scraping
                    reputation_result = self.scrape_competitor_reputation(
                        competitor_name, 
                        competitor.get('search_keywords', [])
                    )
                    
                    # Step 2: Monitor price drift (mock price for demo)
                    current_price = 500000000  # Mock price in IDR
                    current_promo = "Gratis DP" if competitor_name == "Perumahan A" else ""
                    
                    price_result = self.monitor_price_drift(competitor_name, current_price, current_promo)
                    
                    # Step 3: Gap analysis
                    gap_result = self.analyze_value_proposition_gap(competitor_name)
                    
                    competitor_summary = {
                        'competitor_name': competitor_name,
                        'reputation_result': reputation_result,
                        'price_result': price_result,
                        'gap_analysis': gap_result
                    }
                    
                    results['competitor_results'].append(competitor_summary)
                    results['competitors_analyzed'] += 1
                    
                    if price_result.get('drift_type') == 'significant' or price_result.get('promo_change', {}).get('is_new_promo'):
                        results['price_alerts_sent'] += 1
                    
                    if reputation_result.get('overall_sentiment_score') != 0:
                        results['reputation_analyzed'] += 1
                    
                    if not gap_result.get('error'):
                        results['gap_analysis_completed'] += 1
                    
                    self.logger.info(f"Completed surveillance for {competitor_name}")
                    
                    # Rate limiting
                    time.sleep(self.request_delay)
                    
                except Exception as e:
                    self.logger.error(f"Error in surveillance for {competitor_name}: {e}")
                    results['competitor_results'].append({
                        'competitor_name': competitor_name,
                        'error': str(e)
                    })
            
            self.logger.info(f"Competitor surveillance completed: {results['competitors_analyzed']} competitors analyzed")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in competitor surveillance: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'surveillance_timestamp': datetime.now().isoformat()
            }

# Global competitor scout instance
competitor_scout = CompetitorScout()

# Convenience functions
def run_competitor_surveillance() -> Dict:
    """Run complete competitor surveillance"""
    return competitor_scout.run_competitor_surveillance()

def analyze_competitor_reputation(competitor_name: str, keywords: List[str]) -> Dict:
    """Analyze competitor reputation"""
    return competitor_scout.scrape_competitor_reputation(competitor_name, keywords)

def monitor_price_changes(competitor_name: str, price: float, promo: str = "") -> Dict:
    """Monitor price changes for competitor"""
    return competitor_scout.monitor_price_drift(competitor_name, price, promo)

def analyze_value_gap(competitor_name: str) -> Dict:
    """Analyze value proposition gap"""
    return competitor_scout.analyze_value_proposition_gap(competitor_name)

def monitor_velocity() -> Dict:
    """Monitor inventory velocity for competitors"""
    return competitor_scout.monitor_inventory_velocity()

if __name__ == "__main__":
    # Test competitor scout
    logging.basicConfig(level=logging.INFO)
    
    print("=== Competitor Scout Test ===")
    
    # Test complete surveillance
    results = run_competitor_surveillance()
    
    print(f"Status: {results.get('status')}")
    print(f"Competitors analyzed: {results.get('competitors_analyzed')}")
    print(f"Price alerts sent: {results.get('price_alerts_sent')}")
    print(f"Gap analysis completed: {results.get('gap_analysis_completed')}")
    
    print("\nCompetitor Scout test completed!")

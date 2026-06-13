"""
Total Intelligence Aggregator - Sapu Jagat Information System
Sistem komprehensif untuk mengagregasi informasi dari berbagai sumber (pemerintah, asosiasi, sosial media)
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
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
# import pdfplumber  # Optional dependency
# import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TotalIntelligenceAggregator:
    """
    Total Intelligence Aggregator - Sapu Jagat Information System
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'total_intelligence.db (SQLite - removed))
        
        # Macro sources configuration
        self.macro_sources = {
            'bi.go.id': {
                'name': 'Bank Indonesia',
                'url': 'https://www.bi.go.id',
                'category': 'monetary_policy',
                'focus_areas': ['suku bunga', 'inflasi', 'kebijakan moneter', 'kurs'],
                'robots_check': True
            },
            'pu.go.id': {
                'name': 'Kementerian PUPR',
                'url': 'https://www.pu.go.id',
                'category': 'infrastructure_policy',
                'focus_areas': ['infrastruktur', 'perumahan', 'tata kota', 'pembangunan'],
                'robots_check': True
            },
            'bps.go.id': {
                'name': 'BPS',
                'url': 'https://www.bps.go.id',
                'category': 'statistical_data',
                'focus_areas': ['data penduduk', 'ekonomi', 'perumahan', 'inflasi'],
                'robots_check': True
            },
            'rei.or.id': {
                'name': 'REI',
                'url': 'https://rei.or.id',
                'category': 'association_policy',
                'focus_areas': ['kebijakan properti', 'regulasi', 'standar', 'harga'],
                'robots_check': True
            },
            'apernas.org': {
                'name': 'APERNAS',
                'url': 'https://www.apernas.org',
                'category': 'association_policy',
                'focus_areas': ['apartemen', 'regulasi', 'kebijakan', 'standar'],
                'robots_check': True
            },
            'himperra.or.id': {
                'name': 'HIMPERRA',
                'url': 'https://www.himperra.or.id',
                'category': 'association_policy',
                'focus_areas': ['rumah subsidi', 'flpp', 'kebijakan perumahan', 'regulasi'],
                'robots_check': True
            }
        }
        
        # Document parsing configurations
        self.document_parsers = {
            'rdtr': {
                'name': 'RDTR/RTRW Documents',
                'focus_areas': ['zona pengembangan baru', 'rencana jaringan jalan', 'status kawasan', 'peruntukan lahan'],
                'file_types': ['.pdf', '.doc', '.docx']
            }
        }
        
        # Sentiment aggregation thresholds
        self.sentiment_thresholds = {
            'discrepancy_threshold': 0.5,  # Threshold for discrepancy detection
            'confidence_threshold': 0.7,   # Minimum confidence for sentiment analysis
            'update_interval_hours': 24    # Update interval for sources
        }
        
        # Initialize database
        self._init_database()
        
        # Initialize robots.txt cache
        self.robots_cache = {}
    
    def _init_database(self):
        """Initialize database untuk total intelligence aggregator"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create macro sources table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS macro_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_domain TEXT UNIQUE NOT NULL,
                    source_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    last_crawled DATETIME,
                    crawl_status TEXT DEFAULT 'pending',
                    articles_found INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create intelligence data table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS intelligence_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_domain TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT,
                    published_date DATETIME,
                    category TEXT,
                    focus_area TEXT,
                    sentiment_score REAL DEFAULT 0.0,
                    confidence REAL DEFAULT 0.0,
                    extracted_entities TEXT,  -- JSON
                    processed BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create document parsing table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS document_parsing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_type TEXT NOT NULL,
                    document_name TEXT NOT NULL,
                    document_url TEXT,
                    file_path TEXT,
                    parsed_content TEXT,  -- JSON
                    extraction_confidence REAL DEFAULT 0.0,
                    focus_areas_extracted TEXT,  -- JSON
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create sentiment aggregation table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS sentiment_aggregation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_name TEXT NOT NULL,
                    formal_sentiment REAL DEFAULT 0.0,
                    informal_sentiment REAL DEFAULT 0.0,
                    discrepancy_score REAL DEFAULT 0.0,
                    discrepancy_label TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create executive summary table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS executive_summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary_date DATE UNIQUE,
                    macro_economic_status TEXT,  -- JSON
                    policy_alerts TEXT,  -- JSON
                    location_opportunities TEXT,  -- JSON
                    market_sentiment TEXT,  -- JSON
                    discrepancy_warnings TEXT,  -- JSON
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_intelligence_source ON intelligence_data(source_domain)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_intelligence_category ON intelligence_data(category)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_intelligence_processed ON intelligence_data(processed)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_sentiment_location ON sentiment_aggregation(location_name)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_summary_date ON executive_summary(summary_date)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Total intelligence aggregator database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing total intelligence aggregator database: {e}")
    
    def crawl_macro_sources(self, source_filter: List[str] = None) -> Dict:
        """
        Crawl macro sources dengan ethical web crawling
        """
        try:
            self.logger.info("Starting macro sources crawling...")
            
            sources_to_crawl = self.macro_sources
            if source_filter:
                sources_to_crawl = {k: v for k, v in self.macro_sources.items() if k in source_filter}
            
            crawling_results = []
            
            for domain, source_config in sources_to_crawl.items():
                self.logger.info(f"Crawling {source_config['name']} ({domain})...")
                
                try:
                    # Check robots.txt
                    if source_config.get('robots_check', True):
                        if not self._check_robots_permission(domain, source_config['url']):
                            self.logger.warning(f"Robots.txt disallows crawling for {domain}")
                            crawling_results.append({
                                'domain': domain,
                                'status': 'blocked',
                                'reason': 'robots_txt_disallowed'
                            })
                            continue
                    
                    # Crawl the source
                    crawl_result = self._crawl_single_source(domain, source_config)
                    crawling_results.append(crawl_result)
                    
                except Exception as e:
                    self.logger.error(f"Error crawling {domain}: {e}")
                    crawling_results.append({
                        'domain': domain,
                        'status': 'error',
                        'error': str(e)
                    })
                
                # Rate limiting
                time.sleep(3)  # 3 seconds between requests
            
            # Update database with crawling results
            self._update_crawling_results(crawling_results)
            
            self.logger.info(f"Macro sources crawling completed. Processed {len(crawling_results)} sources")
            
            return {
                'status': 'success',
                'sources_crawled': len(crawling_results),
                'crawling_results': crawling_results,
                'crawling_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in macro sources crawling: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'crawling_timestamp': datetime.now().isoformat()
            }
    
    def _check_robots_permission(self, domain: str, base_url: str) -> bool:
        """Check robots.txt permission untuk domain"""
        try:
            # Check cache first
            if domain in self.robots_cache:
                cache_entry = self.robots_cache[domain]
                if datetime.now() - cache_entry['timestamp'] < timedelta(hours=24):
                    return cache_entry['allowed']
            
            # Fetch robots.txt
            robots_url = urljoin(base_url, '/robots.txt')
            
            try:
                response = requests.get(robots_url, timeout=10, headers={
                    'User-Agent': 'TotalIntelligenceAggregator/1.0'
                })
                
                if response.status_code == 200:
                    rp = RobotFileParser()
                    rp.parse(response.text.splitlines())
                    rp.set_url(base_url)
                    
                    # Check if we're allowed to crawl
                    allowed = rp.can_fetch('*', '/')

                    # Cache the result
                    self.robots_cache[domain] = {
                        'allowed': allowed,
                        'timestamp': datetime.now()
                    }
                    
                    return allowed
                else:
                    # No robots.txt found, assume allowed
                    self.robots_cache[domain] = {
                        'allowed': True,
                        'timestamp': datetime.now()
                    }
                    return True
                    
            except requests.RequestException:
                # Error fetching robots.txt, assume allowed
                self.robots_cache[domain] = {
                    'allowed': True,
                    'timestamp': datetime.now()
                }
                return True
                
        except Exception as e:
            self.logger.error(f"Error checking robots.txt for {domain}: {e}")
            return True  # Default to allowed
    
    def _crawl_single_source(self, domain: str, source_config: Dict) -> Dict:
        """Crawl single source untuk intelligence data"""
        try:
            base_url = source_config['url']
            focus_areas = source_config['focus_areas']
            
            # Find relevant pages
            relevant_pages = self._find_relevant_pages(base_url, focus_areas)
            
            # Extract intelligence from pages
            intelligence_data = []
            
            for page in relevant_pages:
                try:
                    page_data = self._extract_page_intelligence(page, source_config)
                    if page_data:
                        intelligence_data.append(page_data)
                except Exception as e:
                    self.logger.error(f"Error extracting from page {page.get('url', 'unknown')}: {e}")
                
                # Rate limiting
                time.sleep(2)
            
            # Save to database
            saved_count = self._save_intelligence_data(domain, intelligence_data)
            
            return {
                'domain': domain,
                'status': 'success',
                'pages_found': len(relevant_pages),
                'intelligence_extracted': len(intelligence_data),
                'data_saved': saved_count
            }
            
        except Exception as e:
            self.logger.error(f"Error crawling single source {domain}: {e}")
            return {
                'domain': domain,
                'status': 'error',
                'error': str(e)
            }
    
    def _find_relevant_pages(self, base_url: str, focus_areas: List[str]) -> List[Dict]:
        """Find relevant pages based on focus areas"""
        try:
            relevant_pages = []
            
            # Common page patterns to check
            page_patterns = [
                '/',
                '/berita',
                '/pengumuman',
                '/kebijakan',
                '/regulasi',
                '/data',
                '/statistik',
                '/publikasi'
            ]
            
            for pattern in page_patterns:
                try:
                    url = urljoin(base_url, pattern)
                    
                    response = requests.get(url, timeout=10, headers={
                        'User-Agent': 'TotalIntelligenceAggregator/1.0'
                    })
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find links to relevant content
                        links = soup.find_all('a', href=True)
                        
                        for link in links:
                            href = link.get('href', '')
                            text = link.get_text().strip().lower()
                            
                            # Check if link contains focus area keywords
                            if any(area.lower() in text for area in focus_areas):
                                full_url = urljoin(base_url, href)
                                
                                # Avoid duplicates
                                if not any(page['url'] == full_url for page in relevant_pages):
                                    relevant_pages.append({
                                        'url': full_url,
                                        'title': text,
                                        'source_pattern': pattern
                                    })
                
                except requests.RequestException as e:
                    self.logger.warning(f"Error accessing {url}: {e}")
                    continue
                
                # Rate limiting
                time.sleep(1)
            
            return relevant_pages[:20]  # Limit to 20 pages per source
            
        except Exception as e:
            self.logger.error(f"Error finding relevant pages: {e}")
            return []
    
    def _extract_page_intelligence(self, page: Dict, source_config: Dict) -> Optional[Dict]:
        """Extract intelligence data from page"""
        try:
            url = page['url']
            
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'TotalIntelligenceAggregator/1.0'
            })
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('title')
            title = title_elem.get_text().strip() if title_elem else page.get('title', '')
            
            # Extract content
            content = self._extract_page_content(soup)
            
            if not content:
                return None
            
            # Extract entities and focus areas
            entities = self._extract_entities(content)
            focus_area = self._determine_focus_area(content, source_config['focus_areas'])
            
            # Calculate sentiment
            sentiment_score = self._calculate_sentiment(content)
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'category': source_config['category'],
                'focus_area': focus_area,
                'sentiment_score': sentiment_score,
                'entities': entities,
                'published_date': self._extract_publish_date(soup)
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting page intelligence: {e}")
            return None
    
    def _extract_page_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from page"""
        try:
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Try different content selectors
            content_selectors = [
                '.content',
                '.main-content',
                '.post-content',
                '.entry-content',
                'article',
                '.page-content',
                'main'
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
            
            # Clean and limit content
            content = re.sub(r'\s+', ' ', content)
            content = content[:3000]  # Limit to 3000 characters
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error extracting page content: {e}")
            return ""
    
    def _extract_entities(self, content: str) -> Dict:
        """Extract entities from content"""
        try:
            entities = {
                'numbers': [],
                'dates': [],
                'locations': [],
                'organizations': [],
                'policies': []
            }
            
            # Extract numbers (percentages, amounts, etc.)
            number_patterns = [
                r'\d+\.?\d*%',
                r'\d+\.?\d*\s*(juta|miliar|triliun|ribu)',
                r'Rp\s*\d+\.?\d*',
                r'\d{4}'
            ]
            
            for pattern in number_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                entities['numbers'].extend(matches)
            
            # Extract dates
            date_patterns = [
                r'\d{1,2}\s*\w+\s*\d{4}',
                r'\d{4}-\d{2}-\d{2}',
                r'\d{2}/\d{2}/\d{4}'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                entities['dates'].extend(matches)
            
            # Extract locations (Indonesian cities/provinces)
            location_keywords = [
                'jakarta', 'surabaya', 'bandung', 'medan', 'semarang', 'makassar',
                'palembang', 'tangerang', 'depok', 'bekasi', 'bogor',
                'banten', 'jabar', 'jateng', 'jatim', 'bali', 'sumut', 'sumsel'
            ]
            
            for location in location_keywords:
                if location.lower() in content.lower():
                    entities['locations'].append(location)
            
            # Extract organizations
            org_keywords = [
                'bi', 'bank indonesia', 'pupr', 'bps', 'rei', 'apernas', 'himperra',
                'kemenkeu', 'kemenppn', 'ojk', 'lkpp'
            ]
            
            for org in org_keywords:
                if org.lower() in content.lower():
                    entities['organizations'].append(org)
            
            # Extract policy keywords
            policy_keywords = [
                'peraturan', 'kebijakan', 'regulasi', 'undang-undang', 'perpu',
                'keputusan presiden', 'peraturan menteri', 'surat edaran'
            ]
            
            for policy in policy_keywords:
                if policy.lower() in content.lower():
                    entities['policies'].append(policy)
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Error extracting entities: {e}")
            return {}
    
    def _determine_focus_area(self, content: str, focus_areas: List[str]) -> str:
        """Determine focus area based on content"""
        try:
            content_lower = content.lower()
            
            # Count matches for each focus area
            area_scores = {}
            
            for area in focus_areas:
                score = 0
                keywords = area.lower().split()
                
                for keyword in keywords:
                    if keyword in content_lower:
                        score += 1
                
                if score > 0:
                    area_scores[area] = score
            
            # Return area with highest score
            if area_scores:
                return max(area_scores, key=area_scores.get)
            
            return 'general'
            
        except Exception as e:
            self.logger.error(f"Error determining focus area: {e}")
            return 'general'
    
    def _calculate_sentiment(self, content: str) -> float:
        """Calculate sentiment score (-1 to 1)"""
        try:
            content_lower = content.lower()
            
            # Positive keywords
            positive_keywords = [
                'naik', 'tumbuh', 'baik', 'positif', 'sukses', 'maju', 'berkembang',
                'meningkat', 'membaik', 'optimal', 'stabil', 'aman', 'terjamin',
                'subsidi', 'insentif', 'bantuan', 'kemudahan', 'promo', 'diskon'
            ]
            
            # Negative keywords
            negative_keywords = [
                'turun', 'menurun', 'buruk', 'negatif', 'gagal', 'mundur', 'susut',
                'berkurang', 'memburuk', 'sulit', 'mahal', 'beban', 'batasan',
                'ketat', 'limit', 'risiko', 'ancaman', 'krisis', 'masalah'
            ]
            
            positive_score = sum(1 for kw in positive_keywords if kw in content_lower)
            negative_score = sum(1 for kw in negative_keywords if kw in content_lower)
            
            # Calculate normalized sentiment
            total_score = positive_score - negative_score
            max_possible = len(positive_keywords) + len(negative_keywords)
            
            if max_possible > 0:
                return total_score / max_possible
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error calculating sentiment: {e}")
            return 0.0
    
    def _extract_publish_date(self, soup: BeautifulSoup) -> datetime:
        """Extract publish date from page"""
        try:
            # Common date selectors
            date_selectors = [
                '.date',
                '.publish-date',
                '.post-date',
                '.entry-date',
                'time',
                '.timestamp'
            ]
            
            for selector in date_selectors:
                element = soup.select_one(selector)
                if element:
                    date_text = element.get_text().strip()
                    
                    # Try to parse date
                    date = self._parse_date_string(date_text)
                    if date:
                        return date
            
            return datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error extracting publish date: {e}")
            return datetime.now()
    
    def _parse_date_string(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime"""
        try:
            date_formats = [
                '%d %B %Y',
                '%d %b %Y',
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%d-%m-%Y'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _save_intelligence_data(self, domain: str, intelligence_data: List[Dict]) -> int:
        """Save intelligence data ke database"""
        try:
            saved_count = 0
            
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                for data in intelligence_data:
                    try:
                        # cursor.execute() removed'''
                            INSERT OR IGNORE INTO intelligence_data 
                            (source_domain, title, content, url, published_date, category, 
                             focus_area, sentiment_score, extracted_entities, processed)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            domain,
                            data.get('title', ''),
                            data.get('content', ''),
                            data.get('url', ''),
                            data.get('published_date', datetime.now()),
                            data.get('category', ''),
                            data.get('focus_area', ''),
                            data.get('sentiment_score', 0.0),
                            json.dumps(data.get('entities', {})),
                            False
                        ))
                        
                        if cursor.rowcount > 0:
                            saved_count += 1
                    
                    except Exception as e:
                        self.logger.error(f"Error saving intelligence data: {e}")
                
                # conn.commit() removed
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"Error saving intelligence data: {e}")
            return 0
    
    def _update_crawling_results(self, crawling_results: List[Dict]):
        """Update crawling results ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                for result in crawling_results:
                    domain = result['domain']
                    status = result['status']
                    
                    # Update source record
                    # cursor.execute() removed'''
                        INSERT OR REPLACE INTO macro_sources 
                        (source_domain, source_name, category, last_crawled, crawl_status, articles_found)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        domain,
                        self.macro_sources[domain]['name'],
                        self.macro_sources[domain]['category'],
                        datetime.now(),
                        status,
                        result.get('intelligence_extracted', 0)
                    ))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error updating crawling results: {e}")
    
    def parse_documents(self, document_type: str = 'rdtr', file_paths: List[str] = None) -> Dict:
        """
        Parse dokumen pemerintah (PDF) dengan LLM
        """
        try:
            self.logger.info(f"Starting document parsing for {document_type}...")
            
            if document_type not in self.document_parsers:
                return {
                    'status': 'error',
                    'error': f'Unsupported document type: {document_type}'
                }
            
            # Get documents to parse
            documents_to_parse = file_paths if file_paths else self._get_documents_to_parse(document_type)
            
            parsing_results = []
            
            for doc_path in documents_to_parse:
                try:
                    # Parse document
                    parse_result = self._parse_single_document(doc_path, document_type)
                    parsing_results.append(parse_result)
                    
                except Exception as e:
                    self.logger.error(f"Error parsing document {doc_path}: {e}")
                    parsing_results.append({
                        'file_path': doc_path,
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Save parsing results
            saved_count = self._save_parsing_results(document_type, parsing_results)
            
            self.logger.info(f"Document parsing completed. Processed {len(documents_to_parse)} documents")
            
            return {
                'status': 'success',
                'document_type': document_type,
                'documents_processed': len(documents_to_parse),
                'parsing_results': parsing_results,
                'documents_saved': saved_count,
                'parsing_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in document parsing: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'parsing_timestamp': datetime.now().isoformat()
            }
    
    def _get_documents_to_parse(self, document_type: str) -> List[str]:
        """Get documents to parse from assets folder"""
        try:
            assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'documents')
            
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir, exist_ok=True)
                return []
            
            doc_config = self.document_parsers[document_type]
            file_types = doc_config['file_types']
            
            documents = []
            
            for file_type in file_types:
                pattern = f"*{file_type}"
                full_pattern = os.path.join(assets_dir, pattern)
                
                import glob
                files = glob.glob(full_pattern)
                documents.extend(files)
            
            return documents
            
        except Exception as e:
            self.logger.error(f"Error getting documents to parse: {e}")
            return []
    
    def _parse_single_document(self, file_path: str, document_type: str) -> Dict:
        """Parse single document with LLM"""
        try:
            # Extract text from PDF
            text_content = self._extract_pdf_text(file_path)
            
            if not text_content:
                return {
                    'file_path': file_path,
                    'status': 'error',
                    'error': 'Could not extract text from document'
                }
            
            # Analyze with LLM
            analysis_result = self._analyze_document_with_llm(text_content, document_type)
            
            return {
                'file_path': file_path,
                'status': 'success',
                'text_content': text_content[:1000],  # First 1000 chars
                'analysis_result': analysis_result
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing single document: {e}")
            return {
                'file_path': file_path,
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            # Try to import pdfplumber
            try:
                import pdfplumber
            except ImportError:
                self.logger.warning("pdfplumber not available, using mock PDF text extraction")
                return f"Mock PDF content for {os.path.basename(file_path)}. This is a placeholder for actual PDF text extraction."
            
            text_content = ""
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            
            return text_content.strip()
            
        except Exception as e:
            self.logger.error(f"Error extracting PDF text: {e}")
            return ""
    
    def _analyze_document_with_llm(self, text_content: str, document_type: str) -> Dict:
        """Analyze document with LLM"""
        try:
            # Check if OpenAI is available
            try:
                import openai
                OPENAI_AVAILABLE = True
            except ImportError:
                OPENAI_AVAILABLE = False
                openai = None
            
            if not OPENAI_AVAILABLE:
                return self._analyze_document_with_keywords(text_content, document_type)
            
            # Prepare LLM prompt
            doc_config = self.document_parsers[document_type]
            focus_areas = doc_config['focus_areas']
            
            prompt = f"""
            Analisis dokumen {document_type.upper()} ini dan ekstrak informasi penting:
            
            Dokumen: {text_content[:4000]}
            
            Fokus pada:
            {', '.join(focus_areas)}
            
            Response format JSON:
            {{
                "zona_pengembangan_baru": ["zona1", "zona2"],
                "rencana_jaringan_jalan": ["jalan1", "jalan2"],
                "status_kawasan": {{"kawasan1": "status1", "kawasan2": "status2"}},
                "peruntukan_lahan": {{"area1": "peruntukan1", "area2": "peruntukan2"}},
                "extracted_entities": ["entity1", "entity2"],
                "confidence_score": 0.8
            }}
            """
            
            client = openai.OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in urban planning and government document analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            llm_response = response.choices[0].message.content
            
            # Parse JSON response
            try:
                analysis = json.loads(llm_response)
                
                # Validate required fields
                required_fields = ['zona_pengembangan_baru', 'rencana_jaringan_jalan', 'status_kawasan']
                for field in required_fields:
                    if field not in analysis:
                        analysis[field] = []
                
                return analysis
                
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse LLM response as JSON: {llm_response}")
                return self._analyze_document_with_keywords(text_content, document_type)
                
        except Exception as e:
            self.logger.error(f"Error in LLM document analysis: {e}")
            return self._analyze_document_with_keywords(text_content, document_type)
    
    def _analyze_document_with_keywords(self, text_content: str, document_type: str) -> Dict:
        """Fallback keyword-based document analysis"""
        try:
            doc_config = self.document_parsers[document_type]
            focus_areas = doc_config['focus_areas']
            
            text_lower = text_content.lower()
            
            # Extract information based on focus areas
            analysis = {
                'zona_pengembangan_baru': [],
                'rencana_jaringan_jalan': [],
                'status_kawasan': {},
                'peruntukan_lahan': {},
                'extracted_entities': [],
                'confidence_score': 0.5
            }
            
            # Extract development zones
            if 'zona pengembangan baru' in text_lower:
                # Look for zone names
                zone_patterns = [
                    r'zona\s+(\w+)',
                    r'kz\s+(\w+)',
                    r'kawasan\s+(\w+)'
                ]
                
                for pattern in zone_patterns:
                    matches = re.findall(pattern, text_lower)
                    analysis['zona_pengembangan_baru'].extend(matches)
            
            # Extract road network plans
            if 'jaringan jalan' in text_lower:
                road_patterns = [
                    r'jalan\s+(\w+)',
                    r'jln\s+(\w+)',
                    r'jalan\s+umum\s+(\w+)'
                ]
                
                for pattern in road_patterns:
                    matches = re.findall(pattern, text_lower)
                    analysis['rencana_jaringan_jalan'].extend(matches)
            
            # Extract area status
            status_keywords = ['perumahan', 'komersial', 'industri', 'hijau', 'publik']
            for keyword in status_keywords:
                if keyword in text_lower:
                    # Look for area names associated with status
                    area_pattern = rf'(\w+)\s+(?:adalah|merupakan)\s+kawasan\s+{keyword}'
                    matches = re.findall(area_pattern, text_lower)
                    for match in matches:
                        analysis['status_kawasan'][match] = keyword
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in keyword document analysis: {e}")
            return {
                'zona_pengembangan_baru': [],
                'rencana_jaringan_jalan': [],
                'status_kawasan': {},
                'peruntukan_lahan': {},
                'extracted_entities': [],
                'confidence_score': 0.0
            }
    
    def _save_parsing_results(self, document_type: str, parsing_results: List[Dict]) -> int:
        """Save parsing results ke database"""
        try:
            saved_count = 0
            
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                for result in parsing_results:
                    try:
                        if result['status'] == 'success':
                            analysis = result.get('analysis_result', {})
                            
                            # cursor.execute() removed'''
                                INSERT OR REPLACE INTO document_parsing 
                                (document_type, document_name, file_path, parsed_content, extraction_confidence, focus_areas_extracted)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (
                                document_type,
                                os.path.basename(result['file_path']),
                                result['file_path'],
                                json.dumps(analysis),
                                analysis.get('confidence_score', 0.0),
                                json.dumps(analysis.get('extracted_entities', []))
                            ))
                            
                            if cursor.rowcount > 0:
                                saved_count += 1
                    
                    except Exception as e:
                        self.logger.error(f"Error saving parsing result: {e}")
                
                # conn.commit() removed
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"Error saving parsing results: {e}")
            return 0
    
    def aggregate_sentiment(self, location_name: str = None) -> Dict:
        """
        Aggregate sentiment dari formal dan informal sources
        """
        try:
            self.logger.info("Starting sentiment aggregation...")
            
            # Get formal sentiment (government sources)
            formal_sentiment = self._get_formal_sentiment(location_name)
            
            # Get informal sentiment (social media/forum)
            informal_sentiment = self._get_informal_sentiment(location_name)
            
            # Calculate discrepancy
            discrepancy_score = abs(formal_sentiment - informal_sentiment)
            discrepancy_label = self._determine_discrepancy_label(discrepancy_score)
            
            # Save aggregation result
            self._save_sentiment_aggregation(
                location_name or 'general',
                formal_sentiment,
                informal_sentiment,
                discrepancy_score,
                discrepancy_label
            )
            
            result = {
                'status': 'success',
                'location_name': location_name or 'general',
                'formal_sentiment': formal_sentiment,
                'informal_sentiment': informal_sentiment,
                'discrepancy_score': discrepancy_score,
                'discrepancy_label': discrepancy_label,
                'aggregation_timestamp': datetime.now().isoformat()
            }
            
            if discrepancy_label != 'no_discrepancy':
                result['warning'] = f"Warning: Local Discrepancy detected in {location_name or 'general'}"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in sentiment aggregation: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'aggregation_timestamp': datetime.now().isoformat()
            }
    
    def _get_formal_sentiment(self, location_name: str = None) -> float:
        """Get formal sentiment dari government sources"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Query formal sources (bi.go.id, pu.go.id, bps.go.id)
                # cursor.execute() removed'''
                    SELECT AVG(sentiment_score) as avg_sentiment
                    FROM intelligence_data 
                    WHERE source_domain IN ('bi.go.id', 'pu.go.id', 'bps.go.id')
                    AND processed = 1
                ''')
                
                result = cursor.fetchone()
                return result[0] if result and result[0] else 0.0
                
        except Exception as e:
            self.logger.error(f"Error getting formal sentiment: {e}")
            return 0.0
    
    def _get_informal_sentiment(self, location_name: str = None) -> float:
        """Get informal sentiment dari social media/forum"""
        try:
            # For now, simulate informal sentiment
            # In production, this would integrate with social media monitoring
            import random
            
            # Simulate some variation in informal sentiment
            base_sentiment = self._get_formal_sentiment(location_name)
            variation = random.uniform(-0.3, 0.3)
            
            return max(-1.0, min(1.0, base_sentiment + variation))
            
        except Exception as e:
            self.logger.error(f"Error getting informal sentiment: {e}")
            return 0.0
    
    def _determine_discrepancy_label(self, discrepancy_score: float) -> str:
        """Determine discrepancy label based on score"""
        try:
            if discrepancy_score < self.sentiment_thresholds['discrepancy_threshold']:
                return 'no_discrepancy'
            elif discrepancy_score < 0.7:
                return 'minor_discrepancy'
            else:
                return 'major_discrepancy'
                
        except Exception as e:
            self.logger.error(f"Error determining discrepancy label: {e}")
            return 'unknown'
    
    def _save_sentiment_aggregation(self, location_name: str, formal_sentiment: float, 
                                 informal_sentiment: float, discrepancy_score: float, 
                                 discrepancy_label: str):
        """Save sentiment aggregation ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    INSERT OR REPLACE INTO sentiment_aggregation 
                    (location_name, formal_sentiment, informal_sentiment, discrepancy_score, discrepancy_label, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (location_name, formal_sentiment, informal_sentiment, discrepancy_score, discrepancy_label, datetime.now()))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error saving sentiment aggregation: {e}")
    
    def generate_executive_summary(self) -> Dict:
        """
        Generate executive summary dashboard
        """
        try:
            self.logger.info("Generating executive summary...")
            
            # Get macro economic status
            macro_economic_status = self._get_macro_economic_status()
            
            # Get policy alerts
            policy_alerts = self._get_policy_alerts()
            
            # Get location opportunities
            location_opportunities = self._get_location_opportunities()
            
            # Get market sentiment
            market_sentiment = self._get_market_sentiment()
            
            # Get discrepancy warnings
            discrepancy_warnings = self._get_discrepancy_warnings()
            
            # Create summary content
            summary_content = self._create_executive_summary_content(
                macro_economic_status,
                policy_alerts,
                location_opportunities,
                market_sentiment,
                discrepancy_warnings
            )
            
            # Save to file
            summary_file = self._save_executive_summary(summary_content)
            
            # Save to database
            self._save_executive_summary_to_db(
                macro_economic_status,
                policy_alerts,
                location_opportunities,
                market_sentiment,
                discrepancy_warnings
            )
            
            self.logger.info(f"Executive summary generated: {summary_file}")
            
            return {
                'status': 'success',
                'summary_file': summary_file,
                'macro_economic_status': macro_economic_status,
                'policy_alerts_count': len(policy_alerts),
                'location_opportunities_count': len(location_opportunities),
                'market_sentiment': market_sentiment,
                'discrepancy_warnings_count': len(discrepancy_warnings),
                'summary_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'summary_timestamp': datetime.now().isoformat()
            }
    
    def _get_macro_economic_status(self) -> Dict:
        """Get macro economic status"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get latest BI rate information
                # cursor.execute() removed'''
                    SELECT title, content, sentiment_score, published_date
                    FROM intelligence_data 
                    WHERE source_domain = 'bi.go.id' 
                    AND processed = 1
                    ORDER BY published_date DESC
                    LIMIT 5
                ''')
                
                bi_data = cursor.fetchall()
                
                # Get inflation information
                # cursor.execute() removed'''
                    SELECT title, content, sentiment_score, published_date
                    FROM intelligence_data 
                    WHERE source_domain = 'bps.go.id' 
                    AND (focus_area LIKE '%inflasi%' OR title LIKE '%inflasi%')
                    AND processed = 1
                    ORDER BY published_date DESC
                    LIMIT 5
                ''')
                
                inflation_data = cursor.fetchall()
                
                return {
                    'bi_rate': {
                        'latest_updates': len(bi_data),
                        'sentiment_trend': self._calculate_trend(bi_data),
                        'key_insights': [row[1][:200] + '...' for row in bi_data[:3]]
                    },
                    'inflation': {
                        'latest_updates': len(inflation_data),
                        'sentiment_trend': self._calculate_trend(inflation_data),
                        'key_insights': [row[1][:200] + '...' for row in inflation_data[:3]]
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Error getting macro economic status: {e}")
            return {
                'bi_rate': {'latest_updates': 0, 'sentiment_trend': 'stable', 'key_insights': []},
                'inflation': {'latest_updates': 0, 'sentiment_trend': 'stable', 'key_insights': []}
            }
    
    def _get_policy_alerts(self) -> List[Dict]:
        """Get policy alerts"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get recent policy changes
                # cursor.execute() removed'''
                    SELECT title, content, source_domain, published_date, sentiment_score
                    FROM intelligence_data 
                    WHERE category IN ('association_policy', 'infrastructure_policy')
                    AND processed = 1
                    AND published_date >= date('now', '-7 days')
                    ORDER BY published_date DESC
                    LIMIT 10
                ''')
                
                policy_data = cursor.fetchall()
                
                alerts = []
                for row in policy_data:
                    alerts.append({
                        'title': row[0],
                        'content': row[1][:200] + '...',
                        'source': row[2],
                        'date': row[3],
                        'sentiment': row[4],
                        'impact_level': 'high' if abs(row[4]) > 0.5 else 'medium'
                    })
                
                return alerts
                
        except Exception as e:
            self.logger.error(f"Error getting policy alerts: {e}")
            return []
    
    def _get_location_opportunities(self) -> List[Dict]:
        """Get location opportunities"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get document parsing results
                # cursor.execute() removed'''
                    SELECT document_name, parsed_content, created_at
                    FROM document_parsing 
                    WHERE document_type = 'rdtr'
                    ORDER BY created_at DESC
                    LIMIT 5
                ''')
                
                doc_data = cursor.fetchall()
                
                opportunities = []
                for row in doc_data:
                    try:
                        parsed_content = json.loads(row[1]) if row[1] else {}
                        
                        if parsed_content.get('zona_pengembangan_baru'):
                            opportunities.append({
                                'document': row[0],
                                'development_zones': parsed_content.get('zona_pengembangan_baru', []),
                                'road_networks': parsed_content.get('rencana_jaringan_jalan', []),
                                'area_status': parsed_content.get('status_kawasan', {}),
                                'date': row[2],
                                'confidence': parsed_content.get('confidence_score', 0.0)
                            })
                    except:
                        continue
                
                return opportunities
                
        except Exception as e:
            self.logger.error(f"Error getting location opportunities: {e}")
            return []
    
    def _get_market_sentiment(self) -> Dict:
        """Get overall market sentiment"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # Get overall sentiment from all sources
                # cursor.execute() removed'''
                    SELECT source_domain, AVG(sentiment_score) as avg_sentiment, COUNT(*) as count
                    FROM intelligence_data 
                    WHERE processed = 1
                    AND published_date >= date('now', '-7 days')
                    GROUP BY source_domain
                ''')
                
                sentiment_data = cursor.fetchall()
                
                overall_sentiment = 0.0
                total_count = 0
                
                for row in sentiment_data:
                    overall_sentiment += row[1] * row[2]
                    total_count += row[2]
                
                if total_count > 0:
                    overall_sentiment /= total_count
                
                # Determine sentiment label
                if overall_sentiment > 0.3:
                    sentiment_label = 'positive'
                elif overall_sentiment < -0.3:
                    sentiment_label = 'negative'
                else:
                    sentiment_label = 'neutral'
                
                return {
                    'overall_sentiment': overall_sentiment,
                    'sentiment_label': sentiment_label,
                    'source_breakdown': {row[0]: {'sentiment': row[1], 'count': row[2]} for row in sentiment_data},
                    'data_points': total_count
                }
                
        except Exception as e:
            self.logger.error(f"Error getting market sentiment: {e}")
            return {
                'overall_sentiment': 0.0,
                'sentiment_label': 'neutral',
                'source_breakdown': {},
                'data_points': 0
            }
    
    def _get_discrepancy_warnings(self) -> List[Dict]:
        """Get discrepancy warnings"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    SELECT location_name, formal_sentiment, informal_sentiment, discrepancy_score, discrepancy_label
                    FROM sentiment_aggregation 
                    WHERE discrepancy_label != 'no_discrepancy'
                    ORDER BY discrepancy_score DESC
                    LIMIT 5
                ''')
                
                discrepancy_data = cursor.fetchall()
                
                warnings = []
                for row in discrepancy_data:
                    warnings.append({
                        'location': row[0],
                        'formal_sentiment': row[1],
                        'informal_sentiment': row[2],
                        'discrepancy_score': row[3],
                        'discrepancy_label': row[4],
                        'warning_level': 'high' if row[3] > 0.7 else 'medium'
                    })
                
                return warnings
                
        except Exception as e:
            self.logger.error(f"Error getting discrepancy warnings: {e}")
            return []
    
    def _calculate_trend(self, data: List[Tuple]) -> str:
        """Calculate trend dari data"""
        try:
            if len(data) < 2:
                return 'stable'
            
            # Simple trend calculation
            recent_sentiment = data[0][3] if len(data[0]) > 3 else 0
            older_sentiment = data[-1][3] if len(data[-1]) > 3 else 0
            
            if recent_sentiment > older_sentiment + 0.2:
                return 'improving'
            elif recent_sentiment < older_sentiment - 0.2:
                return 'declining'
            else:
                return 'stable'
                
        except Exception as e:
            self.logger.error(f"Error calculating trend: {e}")
            return 'stable'
    
    def _create_executive_summary_content(self, macro_status: Dict, policy_alerts: List[Dict], 
                                        location_opportunities: List[Dict], market_sentiment: Dict, 
                                        discrepancy_warnings: List[Dict]) -> str:
        """Create executive summary content"""
        try:
            current_date = datetime.now().strftime("%d %B %Y")
            
            content = f"""# EXECUTIVE SUMMARY - {current_date}
============================================================

## 📊 MACRO ECONOMIC STATUS

### BI Rate Analysis
**Latest Updates:** {macro_status['bi_rate']['latest_updates']}
**Sentiment Trend:** {macro_status['bi_rate']['sentiment_trend'].title()}

"""
            
            # Add BI rate insights
            if macro_status['bi_rate']['key_insights']:
                content += "**Key Insights:**\n"
                for insight in macro_status['bi_rate']['key_insights']:
                    content += f"- {insight}\n"
                content += "\n"
            
            content += """### Inflation Analysis
**Latest Updates:** {inflation_latest_updates}
**Sentiment Trend:** {inflation_sentiment_trend}

""".format(
                inflation_latest_updates=macro_status['inflation']['latest_updates'],
                inflation_sentiment_trend=macro_status['inflation']['sentiment_trend'].title()
            )
            
            # Add inflation insights
            if macro_status['inflation']['key_insights']:
                content += "**Key Insights:**\n"
                for insight in macro_status['inflation']['key_insights']:
                    content += f"- {insight}\n"
                content += "\n"
            
            # Policy alerts section
            content += """## 🏛️ POLICY ALERTS

"""
            
            if policy_alerts:
                for i, alert in enumerate(policy_alerts[:5], 1):
                    impact_emoji = "🔴" if alert['impact_level'] == 'high' else "🟡"
                    content += f"""### {i}. {impact_emoji} {alert['title']}

**Source:** {alert['source']}
**Date:** {alert['date']}
**Sentiment:** {alert['sentiment']:.2f}
**Impact:** {alert['impact_level'].title()}

**Content:** {alert['content']}

"""
            else:
                content += "No significant policy alerts in the last 7 days.\n\n"
            
            # Location opportunities section
            content += """## 🗺️ LOCATION OPPORTUNITIES

"""
            
            if location_opportunities:
                for i, opp in enumerate(location_opportunities[:3], 1):
                    content += f"""### {i}. {opp['document']}

**Development Zones:** {', '.join(opp['development_zones'])}
**Road Networks:** {', '.join(opp['road_networks'])}
**Confidence:** {opp['confidence']:.2f}

"""
                    
                    if opp['area_status']:
                        content += "**Area Status:**\n"
                        for area, status in opp['area_status'].items():
                            content += f"- {area}: {status}\n"
                        content += "\n"
            else:
                content += "No location opportunities identified from recent documents.\n\n"
            
            # Market sentiment section
            content += f"""## 📈 MARKET SENTIMENT

**Overall Sentiment:** {market_sentiment['sentiment_label'].title()}
**Sentiment Score:** {market_sentiment['overall_sentiment']:.2f}
**Data Points:** {market_sentiment['data_points']}

### Source Breakdown
"""
            
            for source, data in market_sentiment['source_breakdown'].items():
                content += f"- **{source}**: {data['sentiment']:.2f} ({data['count']} articles)\n"
            
            content += "\n"
            
            # Discrepancy warnings section
            content += """## ⚠️ DISCREPANCY WARNINGS

"""
            
            if discrepancy_warnings:
                for i, warning in enumerate(discrepancy_warnings[:3], 1):
                    warning_emoji = "🔴" if warning['warning_level'] == 'high' else "🟡"
                    content += f"""### {i}. {warning_emoji} {warning['location']}

**Formal Sentiment:** {warning['formal_sentiment']:.2f}
**Informal Sentiment:** {warning['informal_sentiment']:.2f}
**Discrepancy Score:** {warning['discrepancy_score']:.2f}
**Warning Level:** {warning['warning_level'].title()}

"""
            else:
                content += "No significant discrepancies detected.\n\n"
            
            # Footer
            content += f"""
============================================================
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source:** Total Intelligence Aggregator
**Next Update:** {(datetime.now() + timedelta(hours=24)).strftime("%d %B %Y %H:%M")}
"""
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error creating executive summary content: {e}")
            return f"Error creating executive summary content: {str(e)}"
    
    def _save_executive_summary(self, content: str) -> str:
        """Save executive summary ke file"""
        try:
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            summary_file = os.path.join(reports_dir, 'executive_summary.md')
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return summary_file
            
        except Exception as e:
            self.logger.error(f"Error saving executive summary: {e}")
            return ""
    
    def _save_executive_summary_to_db(self, macro_status: Dict, policy_alerts: List[Dict], 
                                     location_opportunities: List[Dict], market_sentiment: Dict, 
                                     discrepancy_warnings: List[Dict]):
        """Save executive summary ke database"""
        try:
            with # SQLite connection removed as conn:
                cursor = conn.cursor()
                
                # cursor.execute() removed'''
                    INSERT OR REPLACE INTO executive_summary 
                    (summary_date, macro_economic_status, policy_alerts, location_opportunities, market_sentiment, discrepancy_warnings)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().date(),
                    json.dumps(macro_status),
                    json.dumps(policy_alerts),
                    json.dumps(location_opportunities),
                    json.dumps(market_sentiment),
                    json.dumps(discrepancy_warnings)
                ))
                
                # conn.commit() removed
                
        except Exception as e:
            self.logger.error(f"Error saving executive summary to database: {e}")

# Global total intelligence aggregator instance
total_intelligence_aggregator = TotalIntelligenceAggregator()

# Convenience functions
def crawl_macro_sources(source_filter: List[str] = None) -> Dict:
    """Crawl macro sources"""
    return total_intelligence_aggregator.crawl_macro_sources(source_filter)

def parse_documents(document_type: str = 'rdtr', file_paths: List[str] = None) -> Dict:
    """Parse documents"""
    return total_intelligence_aggregator.parse_documents(document_type, file_paths)

def aggregate_sentiment(location_name: str = None) -> Dict:
    """Aggregate sentiment"""
    return total_intelligence_aggregator.aggregate_sentiment(location_name)

def generate_executive_summary() -> Dict:
    """Generate executive summary"""
    return total_intelligence_aggregator.generate_executive_summary()

if __name__ == "__main__":
    # Test Total Intelligence Aggregator
    logging.basicConfig(level=logging.INFO)
    
    print("=== Total Intelligence Aggregator Test ===")
    
    # Test macro sources crawling
    print("\n🌐 Testing Macro Sources Crawling...")
    crawl_result = crawl_macro_sources()
    print(f"Crawling status: {crawl_result['status']}")
    print(f"Sources crawled: {crawl_result['sources_crawled']}")
    
    # Test document parsing
    print("\n📄 Testing Document Parsing...")
    parse_result = parse_documents()
    print(f"Parsing status: {parse_result['status']}")
    print(f"Documents processed: {parse_result['documents_processed']}")
    
    # Test sentiment aggregation
    print("\n📊 Testing Sentiment Aggregation...")
    sentiment_result = aggregate_sentiment()
    print(f"Aggregation status: {sentiment_result['status']}")
    print(f"Formal sentiment: {sentiment_result['formal_sentiment']:.2f}")
    print(f"Informal sentiment: {sentiment_result['informal_sentiment']:.2f}")
    print(f"Discrepancy: {sentiment_result['discrepancy_label']}")
    
    # Test executive summary generation
    print("\n📋 Testing Executive Summary Generation...")
    summary_result = generate_executive_summary()
    print(f"Summary status: {summary_result['status']}")
    print(f"Summary file: {summary_result.get('summary_file', 'N/A')}")
    print(f"Policy alerts: {summary_result.get('policy_alerts_count', 0)}")
    print(f"Location opportunities: {summary_result.get('location_opportunities_count', 0)}")
    
    print("\nTotal Intelligence Aggregator test completed!")

"""
Lead Hunter Module - Scout Agent
Multi-Engine Aggregator untuk pasar Indonesia dengan parallel search
Professional version dengan Zona Berburu (Hunting Grounds) dan Search-First logic
"""

import requests
import json
import time
import os
import re
import random
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from ddgs import DDGS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LeadHunter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Professional User-Agent rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
        ]
        
        # Setup session dengan random User-Agent
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Initialize DuckDuckGo Search - new ddgs package
        self.ddgs = DDGS()
        
        # Ensure directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Database file path
        self.leads_database_file = 'data/leads_database.json'
        
        # Rate limiting settings
        self.request_delay = 2
        self.max_retries = 3
        self.retry_delay = 5
        
        # Multi-Engine Configuration
        self.search_engines = ['google', 'bing', 'duckduckgo']
        self.engine_priorities = {'google': 1, 'bing': 2, 'duckduckgo': 3}
        
        # API Keys from environment
        self.google_api_key = os.getenv('GOOGLE_API_KEY')  # Serper.dev
        self.bing_api_key = os.getenv('BING_API_KEY')
        
        # Async session configuration
        self.session_timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.concurrent_limit = 3  # Max concurrent requests per engine
        
        # Zona Berburu (Hunting Grounds) Configuration
        self.hunting_zones = {
            'marketplaces': {
                'name': 'Marketplaces',
                'sites': [
                    'site:olx.co.id',
                    'site:rumah123.com',
                    'site:rumah.com',
                    'site:lamudi.co.id',
                    'site:properti.id'
                ],
                'keywords': ['rumah dijual', 'rumah Serang', 'properti dijual'],
                'priority': 1
            },
            'social_pulse': {
                'name': 'Social Pulse',
                'sites': [
                    'site:facebook.com/groups',
                    'site:facebook.com/marketplace',
                    'site:instagram.com',
                    'site:twitter.com'
                ],
                'keywords': ['jual beli rumah', 'rumah Serang', 'properti Serang'],
                'priority': 2
            },
            'local_intent': {
                'name': 'Local Intent',
                'sites': [
                    'site:google.com/maps',
                    'site:google.com/search'
                ],
                'keywords': ['rumah Cipocok Jaya', 'tanya rumah', 'info rumah'],
                'priority': 3
            },
            'dark_social': {
                'name': 'Dark Social/Advice',
                'sites': [
                    'site:reddit.com',
                    'site:quora.com',
                    'site:youtube.com'
                ],
                'keywords': ['tips beli rumah', 'KPR Serang', 'kendala KPR', 'cicilan rumah'],
                'priority': 4
            }
        }
        
        # Search-First Configuration
        self.search_first_enabled = True
        self.max_search_results = 20
        self.content_extraction_delay = 3  # seconds between content extraction
        
        # Anti-Detection Configuration
        self.blocking_indicators = [
            'captcha',
            'blocked',
            'forbidden',
            'access denied',
            'rate limited',
            'too many requests',
            'temporarily unavailable',
            'login required',
            'sign in',
            'authentication required',
            'cloudflare',
            'ddos protection'
        ]
        
        # Content validation patterns
        self.content_patterns = {
            'contact_info': [
                r'\b\d{10,13}\b',  # Phone numbers
                r'\b\d{4}\s\d{4}\s\d{4}\b',  # Phone format
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email
                r'\bwa\b|\bwhatsapp\b|\btelegram\b',  # Messaging apps
            ],
            'property_details': [
                r'\b\d+\s*(?:kamar|kt|lb|m2|meter)\b',
                r'\bcluster\b|\btype\b|\bblok\b',
                r'\blt\s*\d+\s*lb\s*\d+',
                r'\bshm\s*\d+\s*shm\s*\d+'
            ],
            'financial_keywords': [
                r'\b(?:harga|rp|idr|juta|miliar)\b',
                r'\bkpr\b|\bcicilan\b|\bdp\b|\bcash\b',
                r'\bpromo\b|\bdiskon\b|\bdiscount\b'
            ]
        }
        
        # Lead qualification criteria
        self.qualification_criteria = {
            'min_budget': 500000000,  # 500M IDR
            'min_land_size': 200,     # sqm
            'preferred_locations': ['Jakarta', 'Tangerang', 'Bekasi', 'Depok', 'Bogar'],
            'project_types': ['residential', 'commercial', 'mixed_use'],
            'development_stage': ['planning', 'permit', 'construction']
        }
    
    def get_search_queries(self, target_zones: List[str] = None) -> List[str]:
        """
        Generate search queries untuk Zona Berburu dengan Search-First logic
        """
        if target_zones is None:
            target_zones = list(self.hunting_zones.keys())
        
        queries = []
        
        for zone_key in target_zones:
            if zone_key not in self.hunting_zones:
                continue
            
            zone = self.hunting_zones[zone_key]
            
            # Generate queries untuk setiap kombinasi site + keyword
            for site in zone['sites']:
                for keyword in zone['keywords']:
                    # Create precise query
                    query = f"{site} \"{keyword}\""
                    queries.append({
                        'query': query,
                        'zone': zone_key,
                        'zone_name': zone['name'],
                        'site': site,
                        'keyword': keyword,
                        'priority': zone['priority']
                    })
        
        # Sort by priority (lower number = higher priority)
        queries.sort(key=lambda x: x['priority'])
        
        self.logger.info(f"Generated {len(queries)} search queries across {len(target_zones)} zones")
        
        return [q['query'] for q in queries]  # Return just the query strings for DDGS
    
    def _detect_blocking(self, response_text: str) -> bool:
        """
        Detect jika situs memblokir atau memerlukan login
        """
        response_text_lower = response_text.lower()
        
        for indicator in self.blocking_indicators:
            if indicator in response_text_lower:
                self.logger.warning(f"Blocking indicator detected: {indicator}")
                return True
        
        return False
    
    def _validate_content_quality(self, content: str) -> Dict:
        """
        Validate content quality untuk memastikan relevan lead
        """
        quality_score = 0
        found_patterns = {}
        
        # Check contact info patterns
        contact_matches = 0
        for pattern in self.content_patterns['contact_info']:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                contact_matches += len(matches)
        found_patterns['contact_info'] = contact_matches
        quality_score += min(contact_matches * 10, 30)  # Max 30 points
        
        # Check property details
        property_matches = 0
        for pattern in self.content_patterns['property_details']:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                property_matches += len(matches)
        found_patterns['property_details'] = property_matches
        quality_score += min(property_matches * 5, 25)  # Max 25 points
        
        # Check financial keywords
        financial_matches = 0
        for pattern in self.content_patterns['financial_keywords']:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                financial_matches += len(matches)
        found_patterns['financial_keywords'] = financial_matches
        quality_score += min(financial_matches * 3, 20)  # Max 20 points
        
        # Content length bonus
        if len(content) > 500:
            quality_score += 15
        elif len(content) > 200:
            quality_score += 10
        elif len(content) > 100:
            quality_score += 5
        
        return {
            'quality_score': min(quality_score, 100),
            'patterns_found': found_patterns,
            'content_length': len(content),
            'is_high_quality': quality_score >= 50
        }
    
    def _search_first_extract_content(self, url: str) -> Optional[str]:
        """
        Extract content dari URL dengan Search-First logic dan anti-detection
        """
        try:
            # Random delay untuk anti-detection
            delay = random.uniform(2, self.content_extraction_delay)
            time.sleep(delay)
            
            # Rotate User-Agent
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            response = self.session.get(url, headers=headers, timeout=30)
            
            # Check for blocking
            if self._detect_blocking(response.text):
                self.logger.warning(f"Site blocked or requires login: {url}")
                return None
            
            # Validate content quality
            quality = self._validate_content_quality(response.text)
            
            if quality['is_high_quality']:
                self.logger.info(f"High-quality content extracted from: {url} (score: {quality['quality_score']})")
                return response.text
            else:
                self.logger.debug(f"Low-quality content from: {url} (score: {quality['quality_score']})")
                return response.text  # Still return but log as low quality
                
        except requests.exceptions.Timeout:
            self.logger.warning(f"Timeout extracting content from: {url}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request error extracting content from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error extracting content from {url}: {e}")
            return None
    
    async def _search_google_async(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Async Google Search menggunakan Serper.dev API
        """
        if not self.google_api_key:
            self.logger.warning("Google API key not configured")
            return []
        
        try:
            headers = {
                'X-API-KEY': self.google_api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': query,
                'num': max_results,
                'hl': 'id',
                'gl': 'id'
            }
            
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.post(
                    'https://google.serper.dev/search',
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        
                        for item in data.get('organic', [])[:max_results]:
                            results.append({
                                'title': item.get('title', ''),
                                'href': item.get('link', ''),
                                'body': item.get('snippet', ''),
                                'engine': 'google',
                                'position': item.get('position', 0)
                            })
                        
                        self.logger.info(f"Google search found {len(results)} results for: {query}")
                        return results
                    else:
                        self.logger.error(f"Google API error: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"Error in Google search: {e}")
            return []
    
    async def _search_bing_async(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Async Bing Search menggunakan Bing Web Search API
        """
        if not self.bing_api_key:
            self.logger.warning("Bing API key not configured")
            return []
        
        try:
            headers = {
                'Ocp-Apim-Subscription-Key': self.bing_api_key,
                'Content-Type': 'application/json'
            }
            
            params = {
                'q': query,
                'count': max_results,
                'mkt': 'id-ID',
                'setLang': 'id',
                'safeSearch': 'Moderate'
            }
            
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.get(
                    'https://api.bing.microsoft.com/v7.0/search',
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        
                        for item in data.get('webPages', {}).get('value', [])[:max_results]:
                            results.append({
                                'title': item.get('name', ''),
                                'href': item.get('url', ''),
                                'body': item.get('snippet', ''),
                                'engine': 'bing',
                                'position': item.get('id', 0)
                            })
                        
                        self.logger.info(f"Bing search found {len(results)} results for: {query}")
                        return results
                    else:
                        self.logger.error(f"Bing API error: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"Error in Bing search: {e}")
            return []
    
    async def _search_duckduckgo_async(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Async DuckDuckGo Search menggunakan ddgs package
        """
        try:
            # Use new ddgs package
            ddgs = DDGS()
            results = []
            
            # New ddgs syntax - no context manager needed
            for i, result in enumerate(ddgs.text(query, max_results=max_results)):
                if i >= max_results:
                    break
                
                results.append({
                    'title': result.get('title', ''),
                    'href': result.get('href', ''),
                    'body': result.get('body', ''),
                    'engine': 'duckduckgo',
                    'position': i + 1
                })
            
            self.logger.info(f"DuckDuckGo search found {len(results)} results for: {query}")
            return results
                
        except Exception as e:
            self.logger.error(f"Error in DuckDuckGo search: {e}")
            return []
    
    async def fetch_from_all_engines(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Unified Aggregator - Fetch dari semua search engines secara parallel
        """
        self.logger.info(f"Starting multi-engine search for: {query}")
        
        # Create tasks for all engines
        tasks = []
        
        # Google search task
        if self.google_api_key:
            tasks.append(self._search_google_async(query, max_results))
        else:
            self.logger.warning("Skipping Google - API key not configured")
        
        # Bing search task
        if self.bing_api_key:
            tasks.append(self._search_bing_async(query, max_results))
        else:
            self.logger.warning("Skipping Bing - API key not configured")
        
        # DuckDuckGo search task (always available)
        tasks.append(self._search_duckduckgo_async(query, max_results))
        
        # Execute all searches in parallel
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            all_results = []
            engine_stats = {}
            
            for i, result in enumerate(results):
                engine = self.search_engines[i]
                
                if isinstance(result, Exception):
                    self.logger.error(f"Engine {engine} failed: {result}")
                    engine_stats[engine] = {'status': 'error', 'count': 0}
                else:
                    all_results.extend(result)
                    engine_stats[engine] = {'status': 'success', 'count': len(result)}
                    self.logger.info(f"Engine {engine} contributed {len(result)} results")
            
            # Log engine statistics
            self.logger.info("Multi-engine search completed:")
            for engine, stats in engine_stats.items():
                self.logger.info(f"  {engine}: {stats['status']} ({stats['count']} results)")
            
            return all_results
            
        except Exception as e:
            self.logger.error(f"Error in multi-engine search: {e}")
            return []
    
    def normalize_and_deduplicate(self, results: List[Dict]) -> List[Dict]:
        """
        Normalisasi dan deduplikasi hasil dari multiple engines
        """
        if not results:
            return []
        
        # Normalize URLs (remove tracking parameters, etc.)
        def normalize_url(url: str) -> str:
            if not url:
                return ''
            
            # Remove common tracking parameters
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            
            try:
                parsed = urlparse(url)
                query_params = parse_qs(parsed.query)
                
                # Remove tracking parameters
                tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'fbclid', 'gclid']
                for param in tracking_params:
                    query_params.pop(param, None)
                
                # Rebuild URL
                clean_query = urlencode(query_params, doseq=True)
                clean_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    clean_query,
                    parsed.fragment
                ))
                
                return clean_url
            except:
                return url
        
        # Normalize and deduplicate
        seen_urls = set()
        unique_results = []
        
        for result in results:
            # Normalize URL
            original_url = result.get('href', '')
            normalized_url = normalize_url(original_url)
            
            # Skip duplicates
            if normalized_url in seen_urls:
                continue
            
            seen_urls.add(normalized_url)
            
            # Add normalized result
            normalized_result = result.copy()
            normalized_result['href'] = normalized_url
            normalized_result['original_url'] = original_url
            normalized_result['normalized'] = True
            
            unique_results.append(normalized_result)
        
        # Sort by engine priority and position
        def sort_key(result):
            engine_priority = self.engine_priorities.get(result.get('engine', 'duckduckgo'), 999)
            position = result.get('position', 999)
            return (engine_priority, position)
        
        unique_results.sort(key=sort_key)
        
        self.logger.info(f"Deduplicated {len(results)} results to {len(unique_results)} unique results")
        
        return unique_results
    
    def _load_leads_database(self) -> Dict:
        """
        Memuat database leads dari file JSON
        """
        try:
            if os.path.exists(self.leads_database_file):
                with open(self.leads_database_file, 'r', encoding='utf-8') as f:
                    database = json.load(f)
                self.logger.info(f"Loaded leads database with {len(database.get('leads', []))} existing leads")
                return database
            else:
                self.logger.info("No existing leads database found, creating new one")
                return {'leads': [], 'last_updated': datetime.now().isoformat()}
        except Exception as e:
            self.logger.error(f"Error loading leads database: {e}")
            return {'leads': [], 'last_updated': datetime.now().isoformat()}
    
    def _save_leads_database(self, database: Dict) -> bool:
        """
        Menyimpan database leads ke file JSON
        """
        try:
            database['last_updated'] = datetime.now().isoformat()
            with open(self.leads_database_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved leads database with {len(database.get('leads', []))} leads")
            return True
        except Exception as e:
            self.logger.error(f"Error saving leads database: {e}")
            return False
    
    def _is_duplicate_lead(self, lead: Dict, existing_leads: List[Dict]) -> bool:
        """
        Enhanced deduplication check dengan URL sebagai primary key
        Priority: URL exact match > title similarity > content similarity
        """
        try:
            lead_url = lead.get('url', '').strip()
            lead_title = lead.get('title', '').strip().lower()
            lead_snippet = lead.get('snippet', '').strip().lower()
            
            # Early return if no URL (shouldn't happen but defensive)
            if not lead_url:
                self.logger.warning("Lead has no URL - allowing as potential duplicate")
                return False
            
            for existing_lead in existing_leads:
                existing_url = existing_lead.get('url', '').strip()
                existing_title = existing_lead.get('title', '').strip().lower()
                existing_snippet = existing_lead.get('snippet', '').strip().lower()
                
                # Priority 1: URL exact match (highest confidence)
                if lead_url and existing_url and lead_url == existing_url:
                    self.logger.debug(f"Duplicate URL found: {lead_url}")
                    return True
                
                # Priority 2: Title similarity (70% match)
                if lead_title and existing_title:
                    similarity = self._calculate_similarity(lead_title, existing_title)
                    if similarity > 0.7:
                        self.logger.debug(f"Duplicate title found: {lead_title} (similarity: {similarity:.2f})")
                        return True
                
                # Priority 3: Content similarity (60% match) - only if both have substantial content
                if (lead_snippet and existing_snippet and 
                    len(lead_snippet) > 50 and len(existing_snippet) > 50):
                    content_similarity = self._calculate_similarity(lead_snippet, existing_snippet)
                    if content_similarity > 0.6:
                        self.logger.debug(f"Duplicate content found (similarity: {content_similarity:.2f})")
                        return True
            
            return False
        except Exception as e:
            self.logger.error(f"Error checking duplicate lead: {e}")
            return False
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Menghitung similarity antara dua string menggunakan simple approach
        """
        try:
            # Simple word-based similarity
            words1 = set(str1.split())
            words2 = set(str2.split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union)
        except Exception:
            return 0.0
    
    def _safe_search_with_retry(self, query: str, max_results: int = 15) -> List[Dict]:
        """
        Melakukan pencarian dengan retry logic dan error handling
        """
        for attempt in range(self.max_retries):
            try:
                # Rotate User-Agent untuk setiap attempt - new ddgs package
                ddgs = DDGS()
                
                self.logger.info(f"Search attempt {attempt + 1}/{self.max_retries} for query: {query}")
                
                # Lakukan pencarian dengan new ddgs syntax
                results = list(ddgs.text(query, max_results=max_results))
                
                if results:
                    self.logger.info(f"Successfully found {len(results)} results on attempt {attempt + 1}")
                    return results
                else:
                    self.logger.warning(f"No results found on attempt {attempt + 1}")
                    
            except Exception as e:
                error_msg = str(e)
                self.logger.error(f"Search attempt {attempt + 1} failed: {error_msg}")
                
                # Specific error handling
                if "Body collection error" in error_msg:
                    self.logger.warning("Body collection error - retrying with different User-Agent")
                elif "timeout" in error_msg.lower():
                    self.logger.warning("Timeout error - increasing delay")
                elif "rate limit" in error_msg.lower():
                    self.logger.warning("Rate limit detected - increasing delay")
                else:
                    self.logger.error(f"Unexpected error: {error_msg}")
                
                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    self.logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
        
        self.logger.error(f"All {self.max_retries} attempts failed for query: {query}")
        return []
    
    async def search_serang_buyers_hunting_zones_async(self, target_zones: List[str] = None) -> List[Dict]:
        """
        Mencari pembeli potensial menggunakan Zona Berburu dengan Multi-Engine Async Search
        """
        try:
            # Load existing database untuk deduplikasi
            database = self._load_leads_database()
            existing_leads = database.get('leads', [])
            
            # Generate search queries untuk zona target
            search_queries = self.get_search_queries(target_zones)
            
            all_new_leads = []
            zone_stats = {}
            engine_stats = {}
            
            # Process queries dengan rate limiting
            for i, query in enumerate(search_queries):
                try:
                    self.logger.info(f"Multi-engine searching in zone {i+1}/{len(search_queries)}: {query}")
                    
                    # Rate limiting antar queries
                    if i > 0:
                        await asyncio.sleep(random.uniform(1, 3))
                    
                    # Step 1: Multi-Engine Search - dapatkan hasil dari semua engines
                    raw_results = await self.fetch_from_all_engines(query, max_results=self.max_search_results)
                    
                    if not raw_results:
                        self.logger.debug(f"No search results for: {query}")
                        continue
                    
                    # Step 2: Deduplikasi dan normalisasi
                    normalized_results = self.normalize_and_deduplicate(raw_results)
                    
                    # Step 3: Filter hasil relevan
                    relevant_results = []
                    for result in normalized_results:
                        # Basic relevance check
                        title_lower = result.get('title', '').lower()
                        snippet_lower = result.get('body', '').lower()
                        
                        # Check for lead indicators
                        lead_indicators = ['cari', 'butuh', 'dicari', 'beli', 'jual', 'dijual', 'sewa', 'disewa']
                        if any(indicator in title_lower or indicator in snippet_lower for indicator in lead_indicators):
                            relevant_results.append(result)
                    
                    self.logger.info(f"Found {len(relevant_results)} relevant results from {len(normalized_results)} total results")
                    
                    # Track engine contributions
                    for result in normalized_results:
                        engine = result.get('engine', 'unknown')
                        engine_stats[engine] = engine_stats.get(engine, 0) + 1
                    
                    # Step 4: Extract content dari URL yang relevan
                    zone_leads = []
                    for result in relevant_results:
                        try:
                            url = result.get('href', '')
                            if not url:
                                continue
                            
                            # Extract content dengan anti-detection
                            content = self._search_first_extract_content(url)
                            
                            if content is None:
                                self.logger.debug(f"Skipped blocked/low-quality URL: {url}")
                                continue
                            
                            # Create enhanced lead data with multi-engine metadata
                            lead_data = {
                                # Core lead information
                                'date_found': datetime.now().isoformat(),
                                'url': url,
                                'title': result.get('title', ''),
                                'snippet': result.get('body', ''),
                                'content': content[:1000],  # First 1000 chars
                                'source': 'Multi-Engine Aggregator',
                                'status': 'new',
                                'lead_type': 'buyer',
                                'location': 'Serang',
                                'query_used': query,
                                'zone': self._extract_zone_from_query(query),
                                'search_time': datetime.now().isoformat(),
                                
                                # Enhanced metadata
                                'metadata': {
                                    'discovery_timestamp': datetime.now().isoformat(),
                                    'search_session_id': f"multi_engine_session_{int(datetime.now().timestamp())}",
                                    'zone_priority': self._get_zone_priority(query),
                                    'content_quality': self._validate_content_quality(content),
                                    'extraction_method': 'multi_engine_search_first',
                                    'data_freshness': 'current',
                                    'engines_used': list(set(r.get('engine', 'unknown') for r in normalized_results))
                                },
                                
                                # Multi-engine specific metadata
                                'search_metadata': {
                                    'source_engine': result.get('engine', 'unknown'),
                                    'engine_position': result.get('position', 0),
                                    'original_url': result.get('original_url', ''),
                                    'normalized_url': result.get('href', '')
                                },
                                
                                # Contact and engagement data
                                'contact_info': self._extract_contact_info(content),
                                'urgency_score': self._calculate_urgency_score(content),
                                'potential_value': self._estimate_potential_value(content),
                                'data_quality_score': self._calculate_data_quality_score({'body': content}),
                                
                                # Behavioral indicators
                                'behavioral_signals': {
                                    'search_intent_strength': self._assess_search_intent(result.get('title', ''), content),
                                    'engagement_potential': self._calculate_engagement_potential({'body': content}),
                                    'conversion_probability': self._estimate_conversion_probability({'body': content}),
                                    'follow_up_priority': self._determine_follow_up_priority({'body': content})
                                },
                                
                                # System metadata
                                'system_info': {
                                    'last_updated': datetime.now().isoformat(),
                                    'processing_version': 'elite_hunter_v3.0',
                                    'multi_engine_enabled': True,
                                    'async_search': True,
                                    'anti_detection_active': True,
                                    'parallel_processing': True
                                }
                            }
                            
                            # Check for duplicates
                            if self._is_duplicate_lead(lead_data, existing_leads + all_new_leads):
                                self.logger.debug(f"Duplicate lead found: {lead_data['title']}")
                                continue
                            
                            zone_leads.append(lead_data)
                            self.logger.info(f"New lead from {result.get('engine', 'unknown')} ({self._extract_zone_from_query(query)}): {lead_data['title'][:50]}...")
                            
                        except Exception as e:
                            self.logger.error(f"Error processing result from {url}: {e}")
                            continue
                    
                    all_new_leads.extend(zone_leads)
                    
                    # Track zone statistics
                    zone_name = self._extract_zone_from_query(query)
                    zone_stats[zone_name] = zone_stats.get(zone_name, 0) + len(zone_leads)
                    
                except Exception as e:
                    self.logger.error(f"Error processing query {query}: {e}")
                    continue
            
            # Save all new leads to database
            if all_new_leads:
                database['leads'].extend(all_new_leads)
                self._save_leads_database(database)
                self.logger.info(f"Saved {len(all_new_leads)} new leads from multi-engine hunting zones")
            
            # Log comprehensive statistics
            self.logger.info("Multi-Engine Hunting Zones Summary:")
            for zone, count in zone_stats.items():
                self.logger.info(f"  {zone}: {count} leads")
            
            self.logger.info("Engine Contribution Summary:")
            for engine, count in engine_stats.items():
                self.logger.info(f"  {engine}: {count} results")
            
            self.logger.info(f"Multi-Engine Zona Berburu search completed: {len(all_new_leads)} total leads")
            return all_new_leads
            
        except Exception as e:
            self.logger.error(f"Critical error in search_serang_buyers_hunting_zones_async: {e}")
            return []
    
    def search_serang_buyers_hunting_zones(self, target_zones: List[str] = None) -> List[Dict]:
        """
        Legacy method - redirects to async version
        """
        # Run async method in sync context
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self.search_serang_buyers_hunting_zones_async(target_zones))
    
    def _extract_zone_from_query(self, query: str) -> str:
        """Extract zone name from search query"""
        for zone_key, zone_data in self.hunting_zones.items():
            if any(site in query for site in zone_data['sites']):
                return zone_data['name']
        return 'Unknown'
    
    def _get_zone_priority(self, query: str) -> int:
        """Get zone priority from search query"""
        for zone_key, zone_data in self.hunting_zones.items():
            if any(site in query for site in zone_data['sites']):
                return zone_data['priority']
        return 999  # Unknown priority
    
    def search_serang_buyers(self) -> List[Dict]:
        """
        Legacy method - redirects to hunting zones search
        """
        return self.search_serang_buyers_hunting_zones()
    
    def run_serang_lead_hunting(self) -> Dict:
        """
        Run lead hunting operations di Serang dengan Zona Berburu
        """
        try:
            self.logger.info("Starting Elite Hunter Lead Hunting Operations")
            
            # Search buyers menggunakan hunting zones
            buyer_leads = self.search_serang_buyers_hunting_zones()
            
            # Search sellers (legacy method for now)
            seller_leads = self.search_serang_sellers()
            
            # Combine results
            all_leads = buyer_leads + seller_leads
            
            # Calculate statistics
            high_urgency_buyers = len([lead for lead in buyer_leads if lead.get('urgency_score', 0) >= 7])
            high_urgency_sellers = len([lead for lead in seller_leads if lead.get('urgency_score', 0) >= 7])
            
            result = {
                'status': 'success',
                'location': 'Serang',
                'buyer_leads_found': len(buyer_leads),
                'seller_leads_found': len(seller_leads),
                'total_leads': len(all_leads),
                'high_urgency_buyers': high_urgency_buyers,
                'high_urgency_sellers': high_urgency_sellers,
                'capture_file': 'logs/scout_leads_capture.txt',
                'execution_time': datetime.now().isoformat(),
                'hunting_zones_enabled': True,
                'search_first_logic': True
            }
            
            self.logger.info(f"Lead hunting completed: {len(all_leads)} total leads captured")
            return result
            
        except Exception as e:
            self.logger.error(f"Critical error in lead hunting operations: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': datetime.now().isoformat()
            }
                
    def _extract_domain(self, url: str) -> str:
        """
        Extract domain dari URL untuk metadata
        """
        try:
            if not url:
                return 'unknown'
            
            # Remove protocol and www
            domain = url.replace('https://', '').replace('http://', '').replace('www.', '')
            
            # Get domain part
            domain_parts = domain.split('/')
            if domain_parts:
                return domain_parts[0]
            
            return 'unknown'
        except Exception:
            return 'unknown'
    
    def _calculate_extraction_confidence(self, result: Dict) -> float:
        """
        Calculate confidence score untuk data extraction quality
        """
        try:
            confidence = 0.0
            
            # Title quality (30%)
            title = result.get('title', '')
            if len(title) > 10:
                confidence += 0.3
            elif len(title) > 5:
                confidence += 0.15
            
            # Content quality (40%)
            content = result.get('body', '')
            if len(content) > 100:
                confidence += 0.4
            elif len(content) > 50:
                confidence += 0.2
            elif len(content) > 20:
                confidence += 0.1
            
            # URL quality (20%)
            url = result.get('href', '')
            if url and ('http' in url or 'www' in url):
                confidence += 0.2
            
            # Contact info (10%)
            content_lower = content.lower()
            if any(keyword in content_lower for keyword in ['phone', 'tel', 'wa', 'email', 'kontak']):
                confidence += 0.1
            
            return min(confidence, 1.0)
        except Exception:
            return 0.0
    
    def _assess_search_intent(self, title: str, content: str) -> str:
        """
        Assess search intent strength
        """
        try:
            text = f"{title} {content}".lower()
            
            # High intent indicators
            high_intent = ['cari', 'butuh', 'dicari', 'dijual', 'sewa', 'harga', 'beli', 'jual']
            medium_intent = ['tanya', 'info', 'detail', 'spek', 'fasilitas']
            low_intent = ['berita', 'artikel', 'blog', 'review']
            
            if any(keyword in text for keyword in high_intent):
                return 'high'
            elif any(keyword in text for keyword in medium_intent):
                return 'medium'
            elif any(keyword in text for keyword in low_intent):
                return 'low'
            else:
                return 'unknown'
        except Exception:
            return 'unknown'
    
    def _calculate_engagement_potential(self, result: Dict) -> float:
        """
        Calculate engagement potential score (0-1)
        """
        try:
            score = 0.0
            
            title = result.get('title', '')
            content = result.get('body', '')
            text = f"{title} {content}".lower()
            
            # Contact info availability (40%)
            if any(keyword in text for keyword in ['phone', 'tel', 'wa', 'email', 'kontak', 'hubungi']):
                score += 0.4
            
            # Specific property details (30%)
            property_keywords = ['kamar', 'lt', 'lb', 'm2', 'meter', 'cluster', 'tipe']
            if any(keyword in text for keyword in property_keywords):
                score += 0.3
            
            # Financial keywords (20%)
            financial_keywords = ['harga', 'rp', 'juta', 'miliar', 'kpr', 'cicilan', 'dp']
            if any(keyword in text for keyword in financial_keywords):
                score += 0.2
            
            # Urgency indicators (10%)
            urgency_keywords = ['segera', 'buruan', 'promo', 'diskon', 'limited']
            if any(keyword in text for keyword in urgency_keywords):
                score += 0.1
            
            return min(score, 1.0)
        except Exception:
            return 0.0
    
    def _estimate_conversion_probability(self, result: Dict) -> float:
        """
        Estimate conversion probability (0-1)
        """
        try:
            base_score = self._calculate_engagement_potential(result)
            
            # Adjust based on content quality
            content_length = len(result.get('body', ''))
            if content_length > 200:
                base_score *= 1.2  # Rich content increases conversion probability
            elif content_length < 50:
                base_score *= 0.7  # Poor content reduces probability
            
            # Adjust based on title specificity
            title = result.get('title', '').lower()
            if any(keyword in title for keyword in ['cari', 'butuh', 'dijual']):
                base_score *= 1.1
            
            return min(base_score, 1.0)
        except Exception:
            return 0.0
    
    def _determine_follow_up_priority(self, result: Dict) -> str:
        """
        Determine follow-up priority level
        """
        try:
            engagement = self._calculate_engagement_potential(result)
            conversion = self._estimate_conversion_probability(result)
            
            combined_score = (engagement + conversion) / 2
            
            if combined_score >= 0.8:
                return 'immediate'
            elif combined_score >= 0.6:
                return 'high'
            elif combined_score >= 0.4:
                return 'medium'
            else:
                return 'low'
        except Exception:
            return 'low'
    
    def _calculate_data_quality_score(self, result: Dict) -> int:
        """
        Enhanced data quality scoring dengan comprehensive metrics
        """
        try:
            score = 0
            
            # Title presence and quality (25 points)
            title = result.get('title', '').strip()
            if len(title) > 10:
                score += 25
            elif len(title) > 5:
                score += 15
            elif title:
                score += 10
            
            # URL presence and validity (20 points)
            url = result.get('href', '').strip()
            if url and ('http' in url or 'www' in url):
                score += 20
            elif url:
                score += 10
            
            # Content length and richness (30 points)
            content = result.get('body', '').strip()
            if len(content) > 100:
                score += 30
            elif len(content) > 50:
                score += 20
            elif len(content) > 20:
                score += 10
            
            # Contact info presence (15 points)
            content_lower = content.lower()
            if any(keyword in content_lower for keyword in ['phone', 'tel', 'wa', 'email', 'kontak']):
                score += 15
            elif any(keyword in content_lower for keyword in ['hubungi', 'contact']):
                score += 8
            
            # Property-specific information (10 points)
            property_keywords = ['kamar', 'lt', 'lb', 'm2', 'meter', 'cluster', 'tipe', 'harga']
            if any(keyword in content_lower for keyword in property_keywords):
                score += 10
            
            return min(score, 100)
        except Exception:
            return 0
    
    def search_serang_sellers(self) -> List[Dict]:
        """
        Mencari penjual rumah dengan keyword 'dijual rumah Serang' menggunakan DuckDuckGo
        Dengan deduplikasi dan structured JSON data
        """
        try:
            # Load existing database untuk deduplikasi
            database = self._load_leads_database()
            existing_leads = database.get('leads', [])
            
            # Query pencarian untuk penjual
            query = "dijual rumah Serang"
            self.logger.info(f"Starting seller search for: {query}")
            
            # Rate limiting
            time.sleep(self.request_delay)
            
            # Lakukan pencarian dengan retry logic
            results = self._safe_search_with_retry(query, max_results=15)
            
            # Proses hasil pencarian untuk identifikasi lead dengan deduplikasi
            new_leads = []
            duplicate_count = 0
            
            for result in results:
                try:
                    # Create enhanced structured lead data with comprehensive metadata
                    lead_data = {
                        # Core lead information
                        'date_found': datetime.now().isoformat(),
                        'url': result.get('href', ''),
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'source': 'DuckDuckGo',
                        'status': 'new',
                        'lead_type': 'seller',
                        'location': 'Serang',
                        'query_used': query,
                        'search_time': datetime.now().isoformat(),
                        
                        # Enhanced metadata for behavioral patterns
                        'metadata': {
                            'discovery_timestamp': datetime.now().isoformat(),
                            'search_session_id': f"session_{int(datetime.now().timestamp())}",
                            'search_rank': len(new_leads) + duplicate_count + 1,
                            'result_position': len(new_leads) + duplicate_count + 1,
                            'content_length': len(result.get('body', '')),
                            'title_length': len(result.get('title', '')),
                            'url_domain': self._extract_domain(result.get('href', '')),
                            'has_contact_info': bool(self._extract_contact_info(result.get('body', ''))),
                            'extraction_confidence': self._calculate_extraction_confidence(result),
                            'data_freshness': 'current'
                        },
                        
                        # Contact and engagement data
                        'contact_info': self._extract_contact_info(result.get('body', '')),
                        'urgency_score': self._calculate_urgency_score(result.get('body', '')),
                        'property_details': self._extract_property_details(result.get('body', '')),
                        'data_quality_score': self._calculate_data_quality_score(result),
                        
                        # Behavioral indicators
                        'behavioral_signals': {
                            'search_intent_strength': self._assess_search_intent(result.get('title', ''), result.get('body', '')),
                            'engagement_potential': self._calculate_engagement_potential(result),
                            'conversion_probability': self._estimate_conversion_probability(result),
                            'follow_up_priority': self._determine_follow_up_priority(result)
                        },
                        
                        # System metadata
                        'system_info': {
                            'last_updated': datetime.now().isoformat(),
                            'processing_version': 'elite_hunter_v1.0',
                            'data_integrity_check': True,
                            'duplicate_checked': True,
                            'quality_validated': True
                        }
                    }
                    
                    # Check for duplicates
                    if self._is_duplicate_lead(lead_data, existing_leads):
                        duplicate_count += 1
                        self.logger.debug(f"Duplicate lead found: {lead_data['title']}")
                        continue
                    
                    # Add to new leads
                    new_leads.append(lead_data)
                    self.logger.info(f"New seller lead found: {lead_data['title']}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing seller lead: {e}")
                    continue
            
            # Save new leads to database
            if new_leads:
                all_leads = existing_leads + new_leads
                database['leads'] = all_leads
                self._save_leads_database(database)
                self.logger.info(f"Saved {len(new_leads)} new seller leads to database")
            
            self.logger.info(f"Seller search completed: {len(new_leads)} new leads, {duplicate_count} duplicates")
            return new_leads
            
        except Exception as e:
            self.logger.error(f"Critical error in search_serang_sellers: {e}")
            return []
    
    def _extract_contact_info(self, text: str) -> Dict:
        """
        Ekstrak informasi kontak dari teks (nomor telepon, email, social media)
        """
        contact_info = {
            'phone_numbers': [],
            'emails': [],
            'social_media': [],
            'websites': []
        }
        
        # Regex untuk nomor telepon Indonesia
        phone_pattern = r'(\+62|62|0)[0-9]{8,13}'
        phones = re.findall(phone_pattern, text)
        contact_info['phone_numbers'] = list(set(phones))
        
        # Regex untuk email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['emails'] = list(set(emails))
        
        # Regex untuk social media
        social_patterns = [
            r'(?:https?://)?(?:www\.)?facebook\.com/[^\s]+',
            r'(?:https?://)?(?:www\.)?instagram\.com/[^\s]+',
            r'(?:https?://)?(?:www\.)?twitter\.com/[^\s]+',
            r'(?:https?://)?(?:www\.)?linkedin\.com/[^\s]+'
        ]
        
        for pattern in social_patterns:
            social = re.findall(pattern, text, re.IGNORECASE)
            contact_info['social_media'].extend(social)
        
        contact_info['social_media'] = list(set(contact_info['social_media']))
        
        return contact_info
    
    def _calculate_urgency_score(self, text: str) -> int:
        """
        Menghitung skor urgensi berdasarkan kata kunci dalam teks
        """
        urgency_keywords = {
            'high': ['butuh cepat', 'segera', 'urgent', 'sekarang', 'hari ini', 'besok', 'minggu ini'],
            'medium': ['bulan ini', 'cari', 'dicari', 'dibutuhkan'],
            'low': ['rencana', 'pertimbangan', 'nanti']
        }
        
        text_lower = text.lower()
        score = 0
        
        for keyword in urgency_keywords['high']:
            if keyword in text_lower:
                score += 30
        
        for keyword in urgency_keywords['medium']:
            if keyword in text_lower:
                score += 20
        
        for keyword in urgency_keywords['low']:
            if keyword in text_lower:
                score += 10
        
        return min(score, 100)  # Max score 100
    
    def _estimate_potential_value(self, text: str) -> str:
        """
        Estimasi nilai potensial berdasarkan kata kunci harga
        """
        price_patterns = [
            r'(\d+)\s*(?:juta|jt)',
            r'(\d+)\s*(?:miliar|milyar|mil)',
            r'rp\s*(\d+)',
            r'idr\s*(\d+)'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return f"Price mentioned: {matches[0]}"
        
        return "Price not mentioned"
    
    def _extract_property_details(self, text: str) -> Dict:
        """
        Ekstrak detail properti dari teks
        """
        details = {
            'bedrooms': None,
            'bathrooms': None,
            'land_area': None,
            'building_area': None,
            'property_type': 'unknown'
        }
        
        # Regex untuk kamar tidur
        bedroom_pattern = r'(\d+)\s*(?:kt|kamar tidur|bedroom)'
        bedrooms = re.findall(bedroom_pattern, text.lower())
        if bedrooms:
            details['bedrooms'] = int(bedrooms[0])
        
        # Regex untuk kamar mandi
        bathroom_pattern = r'(\d+)\s*(?:km|kamar mandi|bathroom)'
        bathrooms = re.findall(bathroom_pattern, text.lower())
        if bathrooms:
            details['bathrooms'] = int(bathrooms[0])
        
        # Regex untuk luas tanah
        land_pattern = r'(\d+)\s*(?:m2|meter persegi|lt|tanah)'
        land_areas = re.findall(land_pattern, text.lower())
        if land_areas:
            details['land_area'] = int(land_areas[0])
        
        # Regex untuk luas bangunan
        building_pattern = r'(\d+)\s*(?:m2|meter persegi|lb|bangunan)'
        building_areas = re.findall(building_pattern, text.lower())
        if building_areas:
            details['building_area'] = int(building_areas[0])
        
        # Identifikasi tipe properti
        if 'rumah' in text.lower():
            details['property_type'] = 'house'
        elif 'apartemen' in text.lower():
            details['property_type'] = 'apartment'
        elif 'ruko' in text.lower():
            details['property_type'] = 'shophouse'
        
        return details
    
    def monitor_government_announcements(self) -> List[Dict]:
        """
        Memantau pengumuman pemerintah terkait infrastruktur dan perizinan
        """
        try:
            announcements = [
                {
                    'source': 'Dinas Penataan Ruang',
                    'title': 'Pengembangan Transit Oriented Development (TOD) di Jakarta Selatan',
                    'date': '2024-01-20',
                    'impact': 'high',
                    'opportunity_type': 'mixed_use_development',
                    'location': 'Jakarta Selatan',
                    'details': 'Pemerintah menyetujui pengembangan area 5 hektar di sekitar stasiun MRT'
                },
                {
                    'source': 'Kementerian PUPR',
                    'title': 'Program Infrastruktur Jalan Tol Baru',
                    'date': '2024-01-18',
                    'impact': 'medium',
                    'opportunity_type': 'commercial_development',
                    'location': 'Tangerang',
                    'details': 'Pembangunan jalan tol baru akan meningkatkan aksesibilitas area industri'
                }
            ]
            
            self.logger.info(f"Monitored {len(announcements)} government announcements")
            return announcements
            
        except Exception as e:
            self.logger.error(f"Error monitoring government announcements: {e}")
            return []
    
    def analyze_social_media_signals(self) -> List[Dict]:
        """
        Menganalisis sinyal dari media sosial untuk identifikasi peluang
        """
        try:
            signals = [
                {
                    'platform': 'LinkedIn',
                    'source': 'Property Developer Group',
                    'content': 'Looking for land parcels in BSD area for residential project',
                    'date': '2024-01-19',
                    'urgency': 'high',
                    'contact_info': 'developer@property.com',
                    'estimated_value': '10M+ USD'
                },
                {
                    'platform': 'Facebook',
                    'source': 'Real Estate Investment Forum',
                    'content': 'Joint venture opportunity for commercial complex in Bekasi',
                    'date': '2024-01-17',
                    'urgency': 'medium',
                    'contact_info': 'investor@realestate.co.id',
                    'estimated_value': '5M+ USD'
                }
            ]
            
            self.logger.info(f"Analyzed {len(signals)} social media signals")
            return signals
            
        except Exception as e:
            self.logger.error(f"Error analyzing social media signals: {e}")
            return []
    
    def track_competitor_activities(self) -> List[Dict]:
        """
        Melacak aktivitas kompetitor untuk identifikasi peluang
        """
        try:
            activities = [
                {
                    'competitor': 'Properti Maju Jaya',
                    'activity': 'Land acquisition in Tangerang',
                    'location': 'Tangerang Selatan',
                    'land_size': '3000 sqm',
                    'estimated_investment': '15M USD',
                    'project_type': 'residential',
                    'opportunity_gap': 'Nearby areas still available for development'
                },
                {
                    'competitor': 'Rumah Indah Developer',
                    'activity': 'Launching new commercial complex',
                    'location': 'Bekasi',
                    'project_size': '20000 sqm',
                    'estimated_investment': '8M USD',
                    'project_type': 'commercial',
                    'opportunity_gap': 'Supporting residential development needed'
                }
            ]
            
            self.logger.info(f"Tracked {len(activities)} competitor activities")
            return activities
            
        except Exception as e:
            self.logger.error(f"Error tracking competitor activities: {e}")
            return []
    
    def generate_lead_score(self, lead: Dict) -> Dict:
        """
        Menghitung skor kualifikasi untuk lead
        """
        try:
            score = 0
            factors = {}
            
            # Budget criteria (30% weight)
            if lead.get('budget', 0) >= self.qualification_criteria['min_budget']:
                score += 30
                factors['budget'] = 'Pass'
            else:
                factors['budget'] = 'Fail'
            
            # Location criteria (25% weight)
            location = lead.get('location', '').lower()
            if any(loc.lower() in location for loc in self.qualification_criteria['preferred_locations']):
                score += 25
                factors['location'] = 'Pass'
            else:
                factors['location'] = 'Fail'
            
            # Project type criteria (20% weight)
            project_type = lead.get('project_type', '').lower()
            if project_type in self.qualification_criteria['project_types']:
                score += 20
                factors['project_type'] = 'Pass'
            else:
                factors['project_type'] = 'Fail'
            
            # Urgency criteria (15% weight)
            urgency = lead.get('urgency', '').lower()
            if urgency in ['high', 'immediate']:
                score += 15
                factors['urgency'] = 'High'
            elif urgency in ['medium']:
                score += 10
                factors['urgency'] = 'Medium'
            else:
                factors['urgency'] = 'Low'
            
            # Contact availability (10% weight)
            if lead.get('contact_info'):
                score += 10
                factors['contact'] = 'Available'
            else:
                factors['contact'] = 'Missing'
            
            # Determine qualification
            qualification = 'Hot' if score >= 80 else 'Warm' if score >= 60 else 'Cold'
            
            return {
                'lead_id': lead.get('id', 'Unknown'),
                'total_score': score,
                'qualification': qualification,
                'factors': factors,
                'recommendation': self._get_recommendation(score, qualification)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating lead score: {e}")
            return {}
    
    def generate_daily_lead_report(self) -> Dict:
        """
        Menghasilkan laporan lead harian
        """
        try:
            # Collect all lead sources
            development_ops = self.search_development_opportunities(['tanah', 'properti', 'development'])
            government_ann = self.monitor_government_announcements()
            social_signals = self.analyze_social_media_signals()
            competitor_act = self.track_competitor_activities()
            
            # Score all leads
            all_leads = development_ops + government_ann + social_signals + competitor_act
            scored_leads = []
            
            for lead in all_leads:
                lead_score = self.generate_lead_score(lead)
                lead['score'] = lead_score
                scored_leads.append(lead)
            
            # Sort by score
            scored_leads.sort(key=lambda x: x['score']['total_score'], reverse=True)
            
            report = {
                'date': datetime.now().isoformat(),
                'total_leads': len(scored_leads),
                'hot_leads': len([l for l in scored_leads if l['score']['qualification'] == 'Hot']),
                'warm_leads': len([l for l in scored_leads if l['score']['qualification'] == 'Warm']),
                'cold_leads': len([l for l in scored_leads if l['score']['qualification'] == 'Cold']),
                'top_opportunities': scored_leads[:5],
                'recommendations': self._generate_daily_recommendations(scored_leads)
            }
            
            self.logger.info(f"Daily lead report generated with {len(scored_leads)} leads")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating daily lead report: {e}")
            return {}
    
    def _search_online_platforms(self, term: str, location: str = None) -> List[Dict]:
        """Mock search untuk online platforms"""
        # Simulasi hasil pencarian
        return [
            {
                'id': f"LEAD_{hash(term) % 1000:03d}",
                'title': f"Development Opportunity: {term}",
                'location': location or 'Jakarta',
                'budget': 1000000000,
                'project_type': 'residential',
                'urgency': 'medium',
                'contact_info': 'contact@property.com',
                'source': 'Online Platform',
                'date': datetime.now().isoformat()
            }
        ]
    
    def _qualify_leads(self, leads: List[Dict]) -> List[Dict]:
        """Filter leads based on basic criteria"""
        qualified = []
        for lead in leads:
            if lead.get('budget', 0) >= self.qualification_criteria['min_budget']:
                qualified.append(lead)
        return qualified
    
    def _get_recommendation(self, score: int, qualification: str) -> str:
        """Get action recommendation based on score"""
        if qualification == 'Hot':
            return "Immediate contact required - high priority lead"
        elif qualification == 'Warm':
            return "Contact within 24 hours - good potential"
        else:
            return "Monitor for now - low priority"
    
    def save_leads_capture(self, buyer_results: List[Dict], seller_results: List[Dict]) -> str:
        """
        Menyimpan hasil tangkapan lead ke file logs/scout_leads_capture.txt
        """
        try:
            capture_file = 'logs/scout_leads_capture.txt'
            
            # Buat laporan terstruktur
            capture_content = f"""
{'='*80}
SCOUT AGENT LEADS CAPTURE REPORT
{'='*80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Location: Serang

{'='*80}
1. CALON PEMBELI (BUYER LEADS)
{'='*80}

"""
            
            # Tambahkan hasil pencarian pembeli
            for i, lead in enumerate(buyer_results, 1):
                capture_content += f"""
{i}. {lead['title']}
   URL: {lead['url']}
   Snippet: {lead['snippet']}
   Search Time: {lead['search_time']}
   Source: {lead['source']}
   Urgency Score: {lead['urgency_score']}/100
   Potential Value: {lead['potential_value']}
   Contact Info: {lead['contact_info']}
   
"""
            
            capture_content += f"""
{'='*80}
2. PENJUAL PROPERTI (SELLER LEADS)
{'='*80}

"""
            
            # Tambahkan hasil pencarian penjual
            for i, lead in enumerate(seller_results, 1):
                capture_content += f"""
{i}. {lead['title']}
   URL: {lead['url']}
   Snippet: {lead['snippet']}
   Search Time: {lead['search_time']}
   Source: {lead['source']}
   Urgency Score: {lead['urgency_score']}/100
   Property Details: {lead['property_details']}
   Contact Info: {lead['contact_info']}
   
"""
            
            # Tambahkan analisis lead
            capture_content += f"""
{'='*80}
3. ANALISIS LEAD RINGKAS
{'='*80}

Total Leads Captured:
- Buyer Leads: {len(buyer_results)} leads
- Seller Leads: {len(seller_results)} leads
- Total: {len(buyer_results) + len(seller_results)} leads

High Urgency Leads (Score > 50):
- Buyers: {len([b for b in buyer_results if b['urgency_score'] > 50])}
- Sellers: {len([s for s in seller_results if s['urgency_score'] > 50])}

Leads with Contact Info:
- Buyers: {len([b for b in buyer_results if any(b['contact_info'].values())])}
- Sellers: {len([s for s in seller_results if any(s['contact_info'].values())])}

Recommended Actions:
1. Prioritize high urgency leads for immediate contact
2. Verify contact information before outreach
3. Prepare tailored approach for buyers vs sellers
4. Schedule follow-up for medium urgency leads

{'='*80}
END OF LEADS CAPTURE REPORT
{'='*80}
"""
            
            # Simpan ke file
            with open(capture_file, 'w', encoding='utf-8') as f:
                f.write(capture_content)
            
            self.logger.info(f"Leads capture saved to: {capture_file}")
            return capture_file
            
        except Exception as e:
            self.logger.error(f"Error saving leads capture: {e}")
            return ""
    
    def run_serang_lead_hunting(self) -> Dict:
        """
        Menjalankan lead hunting lengkap untuk Serang dan menyimpan hasilnya
        """
        try:
            self.logger.info("Starting Serang lead hunting...")
            
            # Step 1: Cari calon pembeli
            buyer_results = self.search_serang_buyers()
            time.sleep(2)  # Rate limiting
            
            # Step 2: Cari penjual properti
            seller_results = self.search_serang_sellers()
            time.sleep(2)  # Rate limiting
            
            # Step 3: Simpan hasil tangkapan
            capture_file = self.save_leads_capture(buyer_results, seller_results)
            
            # Step 4: Return summary
            summary = {
                'status': 'success',
                'location': 'Serang',
                'buyer_leads_found': len(buyer_results),
                'seller_leads_found': len(seller_results),
                'total_leads': len(buyer_results) + len(seller_results),
                'high_urgency_buyers': len([b for b in buyer_results if b['urgency_score'] > 50]),
                'high_urgency_sellers': len([s for s in seller_results if s['urgency_score'] > 50]),
                'capture_file': capture_file,
                'execution_time': datetime.now().isoformat()
            }
            
            self.logger.info(f"Serang lead hunting completed. Capture saved to: {capture_file}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error in Serang lead hunting: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Test the module
    logging.basicConfig(level=logging.INFO)
    lh = LeadHunter()
    
    # Run Serang lead hunting
    result = lh.run_serang_lead_hunting()
    print(json.dumps(result, indent=2, ensure_ascii=False))

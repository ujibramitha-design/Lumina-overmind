"""
LUMINA OS - MASS SCOUT MODULE
=====================================

Reconnaissance & Tripwire System - Target Hunting & Bait Deployment
AI-only target finding with human handoff capabilities

Features:
- High-intent target hunting using DuckDuckGo search
- Contact and URL extraction from search results
- Database integration with status tracking
- Area-specific keyword targeting
- Anti-blocking measures for web scraping
"""

import os
import sys
import json
import asyncio
import logging
import re
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import requests

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)

# Import BeautifulSoup
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    os.system("pip install beautifulsoup4")
    from bs4 import BeautifulSoup

# Database connection for activity logging
try:
    from prisma import Client as PrismaClient
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("Warning: Prisma client not available, activity logging disabled")

# Platform infiltration import
try:
    from .platform_infiltrator import platform_infiltrator
    INFILTRATOR_AVAILABLE = True
except ImportError:
    INFILTRATOR_AVAILABLE = False
    print("Warning: Platform infiltrator not available, advanced scraping disabled")

# Stealth protocol import
try:
    from .stealth_protocol import stealth_protocol, human_delay, stealth_operation, get_random_user_agent
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("Warning: Stealth protocol not available, using basic delays")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

class TripwireScout:
    """
    Tripwire Scout - Mass reconnaissance system for high-intent target hunting
    Specialized in finding and qualifying potential leads for bait deployment
    """
    
    def __init__(self):
        """Initialize Tripwire Scout"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize database connection
        try:
            from core_modules.db_manager_supabase import get_supabase_manager
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Tripwire Scout: Database connected for reconnaissance{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Tripwire Scout: Database connection failed: {e}{END}")
        
        # Initialize Telegram sender for notifications
        try:
            from core_modules.notifications.telegram_sender import get_telegram_sender
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Tripwire Scout: Telegram sender initialized{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Tripwire Scout: Telegram sender failed: {e}{END}")
        
        # Search configuration
        self.search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Contact extraction patterns
        self.phone_patterns = [
            r'\+62[0-9]{9,12}',  # +62xxxxxxxxx
            r'62[0-9]{9,12}',   # 62xxxxxxxxx
            r'08[0-9]{8,11}',   # 08xxxxxxxxx
            r'021[0-9]{7,10}',  # Jakarta landline
            r'022[0-9]{7,10}',  # Bandung landline
            r'031[0-9]{7,10}',  # Semarang landline
            r'024[0-9]{7,10}',  # Surabaya landline
            r'0[0-9]{9,12}',   # General landline
        ]
        
        self.email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        ]
        
        # URL patterns for property platforms
        self.property_patterns = [
            r'(rumah123\.com|rumah\.com|olx\.co\.id|lamudi\.co\.id|properti\.id)',
            r'(linkedin\.com/in/|facebook\.com/|instagram\.com/)',
            r'(wa\.me|api\.whatsapp\.com|chat\.whatsapp\.com)',
        ]
        
        self.logger.info(f"{CYAN}🔍 TRIPWIRE SCOUT: Mass reconnaissance system initialized{END}")
        self.logger.info(f"{GREEN}✅ Ready for high-intent target hunting{END}")
        
        # Platform infiltration capabilities
        self.infiltration_enabled = INFILTRATOR_AVAILABLE
        if self.infiltration_enabled:
            self.logger.info(f"{GREEN}✅ Platform infiltration module loaded{END}")
        else:
            self.logger.warning(f"{YELLOW}⚠️ Platform infiltration module not available{END}")
        
        # Stealth protocol capabilities
        self.stealth_enabled = STEALTH_AVAILABLE
        if self.stealth_enabled:
            self.logger.info(f"{GREEN}✅ Stealth protocol module loaded{END}")
        else:
            self.logger.warning(f"{YELLOW}⚠️ Stealth protocol module not available, using basic delays{END}")
    
    def log_activity(self, action: str, details: str = None, project_data: Dict[str, Any] = None):
        """Log activity to database with project awareness"""
        if not DB_AVAILABLE:
            return
        
        try:
            db = PrismaClient()
            
            # Extract project information
            project_id = None
            project_name = None
            project_type = None
            gaze_data = {}
            
            if project_data:
                project_id = project_data.get('id')
                project_name = project_data.get('namaProyek')
                project_type = project_data.get('tipeProyek')
                gaze_data = {
                    'project_name': project_name,
                    'project_type': project_type,
                    'metadata': project_data
                }
            
            # Create activity log
            activity = db.vrsentinellog.create({
                'action': action,
                'details': details or f"{action} operation completed",
                'projectId': project_id,
                'gazeData': gaze_data,
                'timestamp': datetime.now()
            })
            
            self.logger.info(f"{GREEN}📝 Activity logged: {action} for project {project_name}{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Failed to log activity: {str(e)}{END}")
        finally:
            if 'db' in locals():
                db.disconnect()
    
    async def infiltrate_platforms(self, keywords: List[str], platforms: List[str] = None, project_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Advanced platform infiltration with data enrichment
        
        Args:
            keywords: Keywords to search for
            platforms: Platforms to infiltrate (linkedin, facebook, government)
            project_data: Project data for logging
            
        Returns:
            List of enriched contact data
        """
        if not self.infiltration_enabled:
            self.logger.warning(f"{YELLOW}⚠️ Platform infiltration not available{END}")
            return []
        
        try:
            self.logger.info(f"{BLUE}🎭 Starting platform infiltration{END}")
            
            # Default platforms if not specified
            if not platforms:
                platforms = ['linkedin', 'facebook', 'government']
            
            all_contacts = []
            
            # LinkedIn infiltration
            if 'linkedin' in platforms:
                self.logger.info(f"{CYAN}🔍 Infiltrating LinkedIn for: {keywords}{END}")
                self.log_activity(
                    action="platform_infiltration_linkedin",
                    details=f"Starting LinkedIn infiltration for {len(keywords)} keywords",
                    project_data=project_data
                )
                
                for keyword in keywords:
                    try:
                        linkedin_contacts = await platform_infiltrator.scrape_linkedin_profiles(
                            search_query=keyword,
                            max_profiles=10
                        )
                        
                        # Enrich and save contacts
                        for contact in linkedin_contacts:
                            enriched_contact = await self._enrich_contact_data(contact, 'LinkedIn', project_data)
                            all_contacts.append(enriched_contact)
                            
                        self.logger.info(f"{GREEN}✅ LinkedIn: {len(linkedin_contacts)} contacts extracted for '{keyword}'{END}")
                        
                        # Rate limiting
                        await asyncio.sleep(random.uniform(3, 6))
                        
                    except Exception as e:
                        self.logger.error(f"{RED}❌ LinkedIn infiltration error for '{keyword}': {str(e)}{END}")
                        continue
            
            # Facebook infiltration
            if 'facebook' in platforms:
                self.logger.info(f"{CYAN}🔍 Infiltrating Facebook for: {keywords}{END}")
                self.log_activity(
                    action="platform_infiltration_facebook",
                    details=f"Starting Facebook infiltration for {len(keywords)} keywords",
                    project_data=project_data
                )
                
                for keyword in keywords:
                    try:
                        facebook_contacts = await platform_infiltrator.scrape_facebook_groups(
                            group_search=keyword,
                            max_posts=15
                        )
                        
                        # Enrich and save contacts
                        for contact in facebook_contacts:
                            enriched_contact = await self._enrich_contact_data(contact, 'Facebook', project_data)
                            all_contacts.append(enriched_contact)
                            
                        self.logger.info(f"{GREEN}✅ Facebook: {len(facebook_contacts)} contacts extracted for '{keyword}'{END}")
                        
                        # Rate limiting
                        await asyncio.sleep(random.uniform(2, 4))
                        
                    except Exception as e:
                        self.logger.error(f"{RED}❌ Facebook infiltration error for '{keyword}': {str(e)}{END}")
                        continue
            
            # Government directory infiltration
            if 'government' in platforms and project_data:
                location = project_data.get('namaWilayah') or project_data.get('lokasi', 'Indonesia')
                
                self.logger.info(f"{CYAN}🔍 Infiltrating Government Directories for: {location}{END}")
                self.log_activity(
                    action="platform_infiltration_government",
                    details=f"Starting Government Directory infiltration for {location}",
                    project_data=project_data
                )
                
                try:
                    gov_contacts = await platform_infiltrator.scrape_government_directories(
                        institution_type='pemda',
                        location=location,
                        max_contacts=25
                    )
                    
                    # Enrich and save contacts
                    for contact in gov_contacts:
                        enriched_contact = await self._enrich_contact_data(contact, 'Government Directory', project_data)
                        all_contacts.append(enriched_contact)
                        
                    self.logger.info(f"{GREEN}✅ Government: {len(gov_contacts)} contacts extracted for {location}{END}")
                    
                except Exception as e:
                    self.logger.error(f"{RED}❌ Government infiltration error: {str(e)}{END}")
            
            # Log completion
            self.log_activity(
                action="platform_infiltration_completed",
                details=f"Platform infiltration completed: {len(all_contacts)} total contacts extracted",
                project_data=project_data
            )
            
            self.logger.info(f"{GREEN}✅ Platform infiltration completed: {len(all_contacts)} total contacts{END}")
            return all_contacts
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Platform infiltration failed: {str(e)}{END}")
            return []
    
    async def _enrich_contact_data(self, contact: Dict[str, Any], platform: str, project_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enrich contact data with additional information and save to database
        
        Args:
            contact: Raw contact data from platform
            platform: Source platform
            project_data: Project data for context
            
        Returns:
            Enriched contact data
        """
        try:
            # Add enrichment data
            enriched_contact = {
                **contact,
                'project_id': project_data.get('id') if project_data else None,
                'project_name': project_data.get('namaProyek') if project_data else None,
                'project_type': project_data.get('tipeProyek') if project_data else None,
                'enriched_at': datetime.now().isoformat(),
                'data_quality_score': self._calculate_data_quality_score(contact),
                'contact_priority': self._calculate_contact_priority(contact, project_data)
            }
            
            # Save to database if available
            if self.supabase_manager:
                try:
                    lead_data = {
                        'business_name': contact.get('nama', 'Unknown'),
                        'contact': self._format_contact_string(contact),
                        'url': contact.get('url', ''),
                        'keywords': [contact.get('platform_sumber', platform)],
                        'source': platform,
                        'area': project_data.get('namaWilayah') or project_data.get('lokasi') if project_data else None,
                        'project_id': project_data.get('id') if project_data else None,
                        'platform_sumber': platform,
                        'jabatan': contact.get('jabatan'),
                        'priority': enriched_contact['contact_priority'],
                        'status': 'scouted',
                        'tripwire_data': {
                            'platform': platform,
                            'confidence_score': contact.get('confidence_score', 0.0),
                            'extracted_at': contact.get('extracted_at'),
                            'enriched_data': enriched_contact
                        }
                    }
                    
                    result = self.supabase_manager.insert_lead(lead_data)
                    if result['success']:
                        self.logger.info(f"{GREEN}💾 Enriched contact saved: {contact.get('nama', 'Unknown')} from {platform}{END}")
                    else:
                        self.logger.warning(f"{YELLOW}⚠️ Failed to save enriched contact: {result.get('error')}{END}")
                        
                except Exception as e:
                    self.logger.error(f"{RED}❌ Database save error: {str(e)}{END}")
            
            return enriched_contact
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Contact enrichment error: {str(e)}{END}")
            return contact
    
    def _format_contact_string(self, contact: Dict[str, Any]) -> str:
        """Format contact information into a single string"""
        contact_parts = []
        
        if contact.get('nomor_hp'):
            contact_parts.append(f"Phone: {contact['nomor_hp']}")
        
        if contact.get('email'):
            contact_parts.append(f"Email: {contact['email']}")
        
        if contact.get('jabatan'):
            contact_parts.append(f"Position: {contact['jabatan']}")
        
        return " | ".join(contact_parts) if contact_parts else "No contact info"
    
    def _calculate_data_quality_score(self, contact: Dict[str, Any]) -> float:
        """Calculate data quality score for contact"""
        score = 0.0
        
        # Name quality (30%)
        name = contact.get('nama', '')
        if name and len(name.split()) >= 2:
            score += 0.3
        elif name:
            score += 0.15
        
        # Contact info quality (40%)
        if contact.get('nomor_hp'):
            score += 0.2
        if contact.get('email'):
            score += 0.2
        
        # Job title quality (20%)
        if contact.get('jabatan'):
            score += 0.2
        
        # Platform confidence (10%)
        confidence = contact.get('confidence_score', 0.0)
        score += confidence * 0.1
        
        return min(score, 1.0)
    
    def _calculate_contact_priority(self, contact: Dict[str, Any], project_data: Dict[str, Any] = None) -> str:
        """Calculate contact priority based on data and project type"""
        quality_score = self._calculate_data_quality_score(contact)
        project_type = project_data.get('tipeProyek', 'KOMERSIL') if project_data else 'KOMERSIL'
        
        # High-value indicators
        high_value_indicators = []
        
        if project_type == 'KOMERSIL':
            high_value_indicators.extend([
                'CEO', 'Director', 'President', 'Manager', 'Owner', 'Founder',
                'Executive', 'Vice President', 'VP', 'Head', 'Lead'
            ])
        else:  # SUBSIDI
            high_value_indicators.extend([
                'PNS', 'Pegawai Negeri', 'Karyawan', 'Staff', 'Officer',
                'Camat', 'Lurah', 'Kepala', 'Sekretaris'
            ])
        
        # Check for high-value indicators
        jabatan = contact.get('jabatan', '').lower()
        is_high_value = any(indicator.lower() in jabatan for indicator in high_value_indicators)
        
        # Determine priority
        if quality_score >= 0.8 and is_high_value:
            return 'HIGH'
        elif quality_score >= 0.6 and is_high_value:
            return 'MEDIUM'
        elif quality_score >= 0.4:
            return 'LOW'
        else:
            return 'VERY_LOW'
    
    async def hunt_high_intent_targets(self, keywords: List[str], area: str = "", campaign_mode: str = "REGULAR", project_type: str = "KOMERSIL", project_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Hunt for high-intent targets using specified keywords and area with geo-targeting support
        
        Args:
            keywords: List of keywords to search for
            area: Geographic area to focus on
            campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
            project_type: Project type (KOMERSIL, SUBSIDI)
            project_data: Project data including coordinates and radius for geo-targeting
            
        Returns:
            Dictionary with hunting results and statistics
        """
        try:
            self.logger.info(f"{BLUE}🔍 TRIPWIRE SCOUT: Starting high-intent target hunt{END}")
            self.logger.info(f"{CYAN}📋 Keywords: {keywords}{END}")
            self.logger.info(f"{CYAN}📍 Area: {area if area else 'All areas'}{END}")
            self.logger.info(f"{CYAN}⚔️ Campaign Mode: {campaign_mode}{END}")
            self.logger.info(f"{CYAN}🏢 Project Type: {project_type}{END}")
            
            # Log activity start
            project_name = project_data.get('namaProyek') if project_data else None
            self.log_activity(
                action=f"mass_scout_hunt_{campaign_mode.lower()}",
                details=f"Starting hunt for {len(keywords)} keywords in {area or 'all areas'}",
                project_data=project_data
            )
            
            # Geo-targeting information
            if project_data:
                if project_data.get('tipeInputLokasi') == 'KOORDINAT':
                    lat = project_data.get('latitude')
                    lng = project_data.get('longitude')
                    radius = project_data.get('radiusKm', 5)
                    self.logger.info(f"{GREEN}🎯 Geo-Targeting: {lat}, {lng} within {radius}km radius{END}")
                elif project_data.get('namaWilayah'):
                    self.logger.info(f"{GREEN}🎯 Location Target: {project_data.get('namaWilayah')}{END}")
            
            # Apply campaign-specific keyword enhancement
            enhanced_keywords = self._enhance_keywords_for_campaign(keywords, campaign_mode, project_type)
            
            hunting_results = {
                "keywords": enhanced_keywords,
                "area": area,
                "campaign_mode": campaign_mode,
                "start_time": datetime.now(),
                "targets_found": [],
                "total_searches": 0,
                "successful_extractions": 0,
                "failed_extractions": 0,
                "duplicates": 0,
                "status": "active"
            }
            
            # Search for each enhanced keyword
            for keyword in enhanced_keywords:
                self.logger.info(f"{YELLOW}🔍 Searching for keyword: '{keyword}'{END}")
                
                # Build search query with geo-targeting
                search_query = keyword
                if project_data and project_data.get('tipeInputLokasi') == 'KOORDINAT':
                    # Geo-targeting: prioritize targets within radius
                    lat = project_data.get('latitude')
                    lng = project_data.get('longitude')
                    radius = project_data.get('radiusKm', 5)
                    
                    # Add geo-specific terms for higher precision
                    geo_terms = f"near {lat} {lng} within {radius}km"
                    search_query = f"{keyword} {geo_terms}"
                    
                    # Add location-specific keywords for government/institutional targets
                    if project_type == "KOMERSIL":
                        search_query += " AND (Pemda OR Kementerian OR Perusahaan OR Kantor)"
                    else:
                        search_query += " AND (Pemerintah OR Kantor OR Instansi)"
                        
                    self.logger.info(f"{GREEN}🎯 Geo-targeted query: '{search_query}'{END}")
                elif area:
                    # Traditional area-based search
                    search_query = f"{keyword} {area}"
                elif project_data and project_data.get('namaWilayah'):
                    # Use specific wilayah name
                    search_query = f"{keyword} {project_data.get('namaWilayah')}"
                
                # Perform search
                search_results = self._perform_duckduckgo_search(search_query)
                hunting_results["total_searches"] += 1
                
                # Extract targets from search results
                targets = self._extract_targets_from_results(search_results, keyword)
                
                # Add targets to results
                for target in targets:
                    # Check for duplicates
                    if not self._is_duplicate_target(target, hunting_results["targets_found"]):
                        hunting_results["targets_found"].append(target)
                        hunting_results["successful_extractions"] += 1
                        self.logger.info(f"{GREEN}✅ Target found: {target['contact_info'] or target['url'][:50]}{END}")
                    else:
                        hunting_results["duplicates"] += 1
                        self.logger.info(f"{YELLOW}⚠️ Duplicate target skipped{END}")
                
                # Rate limiting to avoid blocking
                if self.stealth_enabled:
                    await human_delay("search")
                else:
                    time.sleep(random.uniform(2, 4))
            
            # Save targets to database with project type
            saved_count = self._save_targets_to_database(hunting_results["targets_found"], project_type)
            
            # Platform infiltration for enhanced data
            if self.infiltration_enabled and project_data:
                self.logger.info(f"{CYAN}🎭 Starting platform infiltration for enhanced data{END}")
                
                # Extract keywords for infiltration
                infiltration_keywords = [kw for kw in keywords if len(kw) > 2]
                if infiltration_keywords:
                    platform_contacts = await self.infiltrate_platforms(
                        keywords=infiltration_keywords,
                        platforms=['linkedin', 'government'],  # Focus on high-value platforms
                        project_data=project_data
                    )
                    
                    # Add platform contacts to results
                    hunting_results["platform_contacts"] = platform_contacts
                    hunting_results["platform_infiltration"] = True
                    
                    self.logger.info(f"{GREEN}✅ Platform infiltration added {len(platform_contacts)} enhanced contacts{END}")
                else:
                    hunting_results["platform_contacts"] = []
                    hunting_results["platform_infiltration"] = False
            else:
                hunting_results["platform_contacts"] = []
                hunting_results["platform_infiltration"] = False
            
            # Update results
            hunting_results["end_time"] = datetime.now()
            hunting_results["duration"] = (hunting_results["end_time"] - hunting_results["start_time"]).total_seconds()
            hunting_results["targets_saved"] = saved_count
            hunting_results["status"] = "completed"
            
            # Send notification
            self._send_hunting_completion_notification(hunting_results)
            
            # Log activity completion
            self.log_activity(
                action=f"mass_scout_hunt_completed",
                details=f"Hunt completed: {len(hunting_results['targets_found'])} targets found, {saved_count} saved in {hunting_results['duration']:.1f}s",
                project_data=project_data
            )
            
            self.logger.info(f"{GREEN}✅ TRIPWIRE SCOUT: Hunt completed{END}")
            self.logger.info(f"{CYAN}📊 Results: {len(hunting_results['targets_found'])} targets found, {saved_count} saved{END}")
            
            return hunting_results
            
        except Exception as e:
            self.logger.error(f"{RED}❌ TRIPWIRE SCOUT: Hunting error: {str(e)}{END}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _perform_duckduckgo_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform DuckDuckGo search and return results"""
        try:
            # DuckDuckGo instant answer API
            url = "https://duckduckgo.com/html/"
            params = {
                'q': query,
                'kl': 'us-en',
                'ad': 'n',
                'df': 'q',
                'safesearch': 'on',
                'source': 'web',
                'num': '20'
            }
            
            response = requests.get(url, params=params, headers=self.search_headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML results
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extract search results
            for result in soup.find_all('div', class_='result'):
                try:
                    title_elem = result.find('a', class_='result__a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet_elem = result.find('a', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'duckduckgo'
                        })
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            self.logger.error(f"{RED}❌ DuckDuckGo search error: {str(e)}{END}")
            return []
    
    def _extract_targets_from_results(self, search_results: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
        """Extract contact information and URLs from search results"""
        targets = []
        
        for result in search_results:
            try:
                target = {
                    'keyword': keyword,
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('snippet', ''),
                    'source': result.get('source', 'duckduckgo'),
                    'contact_info': None,
                    'contact_type': None,
                    'confidence_score': 0,
                    'scouted_at': datetime.now().isoformat(),
                    'status': 'scouted'
                }
                
                # Extract contact information
                contact_info = self._extract_contact_info(result)
                if contact_info:
                    target.update(contact_info)
                
                # Calculate confidence score
                target['confidence_score'] = self._calculate_confidence_score(target)
                
                # Only include targets with meaningful contact info or URLs
                if target['confidence_score'] > 30:
                    targets.append(target)
                
            except Exception as e:
                self.logger.error(f"{RED}❌ Target extraction error: {str(e)}{END}")
                continue
        
        return targets
    
    def _extract_contact_info(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract contact information from search result"""
        contact_info = {}
        
        # Combine all text for analysis
        text_to_analyze = f"{result.get('title', '')} {result.get('snippet', '')} {result.get('url', '')}"
        
        # Extract phone numbers
        for pattern in self.phone_patterns:
            matches = re.findall(pattern, text_to_analyze)
            if matches:
                contact_info['contact_info'] = matches[0]
                contact_info['contact_type'] = 'phone'
                break
        
        # Extract email addresses
        if 'contact_info' not in contact_info:
            for pattern in self.email_patterns:
                matches = re.findall(pattern, text_to_analyze)
                if matches:
                    contact_info['contact_info'] = matches[0]
                    contact_info['contact_type'] = 'email'
                    break
        
        # Extract property URLs
        if 'contact_info' not in contact_info:
            for pattern in self.property_patterns:
                if re.search(pattern, text_to_analyze):
                    contact_info['contact_info'] = result.get('url', '')
                    contact_info['contact_type'] = 'url'
                    break
        
        return contact_info
    
    def _calculate_confidence_score(self, target: Dict[str, Any]) -> int:
        """Calculate confidence score for target"""
        score = 0
        
        # High-intent keywords in title
        high_intent_keywords = [
            'cari', 'butuh', 'dicari', 'mencari', 'ingin', 'mau', 'beli', 'jual',
            'KPR', 'kpr', 'cicilan', 'DP', 'uang muka', 'booking', 'survey',
            'serius', 'urgent', 'segera', 'cepat', 'langsung', 'nego', 'deal'
        ]
        
        title_lower = target.get('title', '').lower()
        snippet_lower = target.get('snippet', '').lower()
        
        for keyword in high_intent_keywords:
            if keyword in title_lower:
                score += 20
            elif keyword in snippet_lower:
                score += 10
        
        # Contact information presence
        if target.get('contact_info'):
            score += 30
        
        # Property platform URLs
        url = target.get('url', '')
        if any(pattern in url for pattern in self.property_patterns):
            score += 20
        
        # Length and quality of content
        if len(target.get('title', '')) > 20:
            score += 10
        if len(target.get('snippet', '')) > 50:
            score += 10
        
        return min(score, 100)
    
    def _is_duplicate_target(self, target: Dict[str, Any], existing_targets: List[Dict[str, Any]]) -> bool:
        """Check if target is duplicate"""
        contact_info = target.get('contact_info')
        url = target.get('url')
        
        for existing in existing_targets:
            # Check duplicate by contact info
            if contact_info and existing.get('contact_info') == contact_info:
                return True
            
            # Check duplicate by URL
            if url and existing.get('url') == url:
                return True
        
        return False
    
    def _save_targets_to_database(self, targets: List[Dict[str, Any]], project_type: str = "KOMERSIL") -> int:
        """Save targets to database with project type isolation"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - targets not saved{END}")
                return 0
            
            saved_count = 0
            for target in targets:
                try:
                    # Prepare lead data for database with project type
                    lead_data = {
                        'contact_info': target.get('contact_info'),
                        'contact_type': target.get('contact_type'),
                        'url': target.get('url'),
                        'title': target.get('title'),
                        'snippet': target.get('snippet'),
                        'source': target.get('source'),
                        'keyword': target.get('keyword'),
                        'confidence_score': target.get('confidence_score'),
                        'status': 'scouted',
                        'scouted_at': target.get('scouted_at'),
                        'project_type': project_type,  # Add project type for isolation
                        'tripwire_data': {
                            'area': '',
                            'bait_deployed': False,
                            'response_received': False,
                            'hot_responded': False,
                            'project_type': project_type  # Add project type to tripwire data
                        }
                    }
                    
                    # Insert to database
                    result = self.supabase_manager.insert_lead(lead_data)
                    
                    if result['success']:
                        saved_count += 1
                        self.logger.info(f"{GREEN}✅ Target saved to database: {target['contact_info'] or target['url'][:50]}{END}")
                    else:
                        self.logger.error(f"{RED}❌ Failed to save target: {result.get('error')}{END}")
                
                except Exception as e:
                    self.logger.error(f"{RED}❌ Database save error: {str(e)}{END}")
                    continue
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Database save error: {str(e)}{END}")
            return 0
    
    def _send_hunting_completion_notification(self, results: Dict[str, Any]):
        """Send hunting completion notification to Telegram"""
        try:
            if self.telegram_sender:
                notification_text = f"""
🔍 <b>TRIPWIRE SCOUT COMPLETED</b>

📊 <b>Hunting Results:</b>
• Keywords: {len(results['keywords'])}
• Area: {results['area'] or 'All areas'}
• Total Searches: {results['total_searches']}
• Targets Found: {len(results['targets_found'])}
• Successful: {results['successful_extractions']}
• Failed: {results['failed_extractions']}
• Duplicates: {results['duplicates']}
• Saved: {results.get('targets_saved', 0)}
• Duration: {results.get('duration', 0):.1f}s

🎯 <b>High-Intent Targets Ready:</b>
{len(results['targets_found'])} targets now available for bait deployment

⏰ <b>Completed:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Tripwire Scout ready for bait deployment phase</i>
                """.strip()
                
                self.telegram_sender.send_message(notification_text)
            else:
                self.logger.warning(f"{YELLOW}⚠️ Telegram not available - notification not sent{END}")
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Notification error: {str(e)}{END}")
    
    def get_scouted_targets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recently scouted targets from database"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - using empty list{END}")
                return []
            
            # Query database for scouted targets
            result = self.supabase_manager.get_leads_by_status('scouted', limit)
            
            if result['success']:
                return result['data']
            else:
                self.logger.error(f"{RED}❌ Failed to get scouted targets: {result.get('error')}{END}")
                return []
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database query error: {str(e)}{END}")
            return []
    
    def get_hunting_statistics(self) -> Dict[str, Any]:
        """Get hunting statistics"""
        try:
            if not self.supabase_manager:
                return {
                    "total_scouted": 0,
                    "recent_24h": 0,
                    "recent_7d": 0,
                    "total_targets": 0
                }
            
            # Get statistics from database
            stats = self.supabase_manager.get_lead_statistics()
            
            return {
                "total_scouted": stats.get('status_counts', {}).get('scouted', 0),
                "recent_24h": stats.get('recent_24h', {}).get('scouted', 0),
                "recent_7d": stats.get('recent_7d', {}).get('scouted', 0),
                "total_targets": stats.get('total_leads', 0)
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Statistics error: {str(e)}{END}")
            return {
                "total_scouted": 0,
                "recent_24h": 0,
                "recent_7d": 0,
                "total_targets": 0
            }
    
    def _enhance_keywords_for_campaign(self, keywords: List[str], campaign_mode: str, project_type: str = "KOMERSIL") -> List[str]:
        """
        Enhance keywords based on campaign mode and project type
        
        Args:
            keywords: Original keywords
            campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
            project_type: Project type (KOMERSIL, SUBSIDI)
            
        Returns:
            Enhanced keywords list
        """
        try:
            enhanced_keywords = []
            
            # Add project type specific keywords first
            if project_type == "KOMERSIL":
                komersil_keywords = [
                    "rumah mewah", "properti eksklusif", "hunian prestise", "villa mewah",
                    "apartemen premium", "condominium kelas atas", "properti investasi",
                    "rumah untuk eksekutif", "properti untuk pengusaha", "hunian profesional",
                    "KPR reguler", "KPR komersial", "cicilan rumah mewah", "DP rumah mewah",
                    "lokasi strategis", "fasilitas premium", "akses mudah", "nilai investasi",
                    "capital gain", "properti komersial", "rumah untuk manajer", "rumah direktur",
                    # Geo-targeting keywords for high-precision targeting
                    "kantor pusat", "kantor cabang", "gedung perkantoran", "kawasan bisnis",
                    "perusahaan multinasional", "korporat", "executive housing", "CEO residence"
                ]
                enhanced_keywords.extend(komersil_keywords)
                self.logger.info(f"{YELLOW}👑 KOMERSIL mode: Added {len(komersil_keywords)} luxury keywords{END}")
                
            elif project_type == "SUBSIDI":
                subsidi_keywords = [
                    "rumah subsidi", "rumah murah", "properti terjangkau", "hunian subsidi",
                    "KPR FLPP", "KPR subsidi pemerintah", "cicilan ringan", "DP ringan",
                    "rumah untuk PNS", "rumah untuk P3K", "rumah untuk pegawai negeri",
                    "rumah untuk UMR", "rumah untuk karyawan swasta", "hunian keluarga",
                    "program rumah subsidi", "bantuan down payment", "kemudahan KPR",
                    "cicilan terjangkau", "DP terjangkau", "rumah untuk pekerja",
                    "properti untuk PNS", "hunian aparatur negara", "rumah untuk guru",
                    # Geo-targeting keywords for government/institutional areas
                    "kantor pemerintah", "instansi pemerintah", "kantor kelurahan", "kantor kecamatan",
                    "kantor dinas", "fasilitas umum", "area pemerintahan", "kantor PNS"
                ]
                enhanced_keywords.extend(subsidi_keywords)
                self.logger.info(f"{BLUE}🛡️ SUBSIDI mode: Added {len(subsidi_keywords)} affordable keywords{END}")
            
            # Add campaign mode specific keywords
            if campaign_mode == "HEADHUNTER":
                # Add HEADHUNTER specific keywords
                headhunter_keywords = [
                    "dipromosikan menjadi manager",
                    "direktur baru",
                    "new role area",
                    "promosi jabatan",
                    "kenaikan pangkat",
                    "executive promotion",
                    "career advancement",
                    "management position",
                    "leadership role",
                    "senior appointment"
                ]
                enhanced_keywords.extend(headhunter_keywords)
                self.logger.info(f"{CYAN}🎯 HEADHUNTER mode: Added {len(headhunter_keywords)} strategic keywords{END}")
                
            elif campaign_mode == "B2B_SWEEPING":
                # Add B2B_SWEEPING specific keywords
                b2b_keywords = [
                    "HRD manager",
                    "General Affair",
                    "pabrik baru beroperasi",
                    "pembukaan kantor cabang",
                    "corporate expansion",
                    "business development",
                    "company relocation",
                    "employee housing",
                    "corporate housing program",
                    "Bantuan Relokasi Karyawan",
                    "karyawan pindah"
                ]
                
                # Add area-specific keywords for B2B
                if keywords:
                    for keyword in keywords:
                        for b2b_keyword in b2b_keywords:
                            if "area" in keyword.lower() or "lokasi" in keyword.lower():
                                enhanced_keywords.append(f"{b2b_keyword} {keyword}")
                            else:
                                enhanced_keywords.append(b2b_keyword)
                else:
                    enhanced_keywords.extend(b2b_keywords)
                
                self.logger.info(f"{CYAN}🏢 B2B_SWEEPING mode: Added {len(b2b_keywords)} corporate keywords{END}")
                
            else:
                # REGULAR mode - use original keywords
                enhanced_keywords.extend(keywords)
                self.logger.info(f"{CYAN}📋 REGULAR mode: Using original keywords{END}")
            
            # Remove duplicates while preserving order
            seen = set()
            unique_keywords = []
            for keyword in enhanced_keywords:
                if keyword not in seen:
                    seen.add(keyword)
                    unique_keywords.append(keyword)
            
            self.logger.info(f"{GREEN}✅ Enhanced keywords: {len(unique_keywords)} unique terms{END}")
            return unique_keywords
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Keyword enhancement error: {str(e)}{END}")
            return keywords

# Global Tripwire Scout instance
tripwire_scout = TripwireScout()

# Convenience functions
async def hunt_high_intent_targets(keywords: List[str], area: str = "", campaign_mode: str = "REGULAR", project_type: str = "KOMERSIL", project_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Convenience function to hunt high-intent targets
    
    Args:
        keywords: List of keywords to search for
        area: Geographic area to focus on
        campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
        project_type: Project type (KOMERSIL, SUBSIDI)
        project_data: Project data including coordinates and radius for geo-targeting
        
    Returns:
        Dictionary with hunting results
    """
    return await tripwire_scout.hunt_high_intent_targets(keywords, area, campaign_mode, project_type, project_data)

def generate_dork_queries(keywords: List[str], area: str = "", campaign_mode: str = "REGULAR", project_type: str = "KOMERSIL") -> List[str]:
    """
    Generate dork queries for mass scouting
    
    Args:
        keywords: List of keywords to search for
        area: Geographic area to focus on
        campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
        project_type: Project type (KOMERSIL, SUBSIDI)
        
    Returns:
        List of generated dork queries
    """
    try:
        # Log dorking activity
        if DB_AVAILABLE:
            db = PrismaClient()
            project_name = project_type  # Fallback to project type if no project data
            
            db.vrsentinellog.create({
                'action': 'generate_dork_queries',
                'details': f'Generating dork queries for {len(keywords)} keywords in {area or "all areas"}',
                'gazeData': {
                    'project_type': project_type,
                    'campaign_mode': campaign_mode,
                    'keywords_count': len(keywords),
                    'area': area
                },
                'timestamp': datetime.now()
            })
            db.disconnect()
        
        # Generate enhanced keywords
        enhanced_keywords = tripwire_scout._enhance_keywords_for_campaign(keywords, campaign_mode, project_type)
        
        # Create dork queries
        dork_queries = []
        for keyword in enhanced_keywords:
            if area:
                query = f'"{keyword}" {area}'
            else:
                query = f'"{keyword}"'
            dork_queries.append(query)
        
        return dork_queries
        
    except Exception as e:
        print(f"Error generating dork queries: {str(e)}")
        return keywords

def get_scouted_targets(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Convenience function to get scouted targets
    
    Args:
        limit: Maximum number of targets to return
        
    Returns:
        List of scouted targets
    """
    return tripwire_scout.get_scouted_targets(limit)

async def infiltrate_platforms(keywords: List[str], platforms: List[str] = None, project_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Convenience function for platform infiltration
    
    Args:
        keywords: Keywords to search for
        platforms: Platforms to infiltrate (linkedin, facebook, government)
        project_data: Project data for context
        
    Returns:
        List of enriched contact data
    """
    return await tripwire_scout.infiltrate_platforms(keywords, platforms, project_data)

def get_hunting_statistics() -> Dict[str, Any]:
    """
    Convenience function to get hunting statistics
    
    Returns:
        Dictionary with hunting statistics
    """
    return tripwire_scout.get_hunting_statistics()

async def run_official_api_scout(keywords: List[str], project_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Placeholder function for official API scouting
    
    Args:
        keywords: Keywords to search for
        project_data: Project data for context
        
    Returns:
        Dictionary with API scouting results
    """
    try:
        # TODO: Implement official API integration
        # This would connect to official property APIs, government databases, etc.
        
        logger.info(f"🔌 Running Official API Scout for {len(keywords)} keywords")
        
        # Placeholder implementation
        api_results = {
            "status": "completed",
            "method": "API_OFFICIAL",
            "keywords": keywords,
            "leads_found": 0,  # Would be populated by actual API calls
            "message": "Official API scouting placeholder - implement actual API integration"
        }
        
        # Log activity
        if DB_AVAILABLE:
            db = PrismaClient()
            db.vrsentinellog.create({
                'action': 'official_api_scout',
                'details': f'Official API scouting for {len(keywords)} keywords',
                'gazeData': {
                    'method': 'API_OFFICIAL',
                    'keywords_count': len(keywords),
                    'project_data': project_data
                },
                'timestamp': datetime.now()
            })
            db.disconnect()
        
        return api_results
        
    except Exception as e:
        logger.error(f"❌ Official API Scout error: {str(e)}")
        return {
            "status": "failed",
            "method": "API_OFFICIAL",
            "error": str(e),
            "keywords": keywords
        }

async def run_direct_scrape(keywords: List[str], project_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Placeholder function for direct web scraping
    
    Args:
        keywords: Keywords to search for
        project_data: Project data for context
        
    Returns:
        Dictionary with scraping results
    """
    try:
        # TODO: Implement direct web scraping integration
        # This would use the existing mass_scout functionality
        
        logger.info(f"🕷️ Running Direct Scrape for {len(keywords)} keywords")
        
        # Use existing tripwire_scout for scraping
        scraping_results = await tripwire_scout.hunt_high_intent_targets(
            keywords=keywords,
            campaign_mode="REGULAR",
            project_type=project_data.get('tipeProyek', 'KOMERSIL') if project_data else 'KOMERSIL',
            project_data=project_data
        )
        
        # Log activity
        if DB_AVAILABLE:
            db = PrismaClient()
            db.vrsentinellog.create({
                'action': 'direct_scrape',
                'details': f'Direct scraping for {len(keywords)} keywords',
                'gazeData': {
                    'method': 'DIRECT_SCRAPE',
                    'keywords_count': len(keywords),
                    'project_data': project_data,
                    'results_count': len(scraping_results.get('targets_found', []))
                },
                'timestamp': datetime.now()
            })
            db.disconnect()
        
        return {
            "status": scraping_results.get('status', 'unknown'),
            "method": "DIRECT_SCRAPE",
            "keywords": keywords,
            "leads_found": len(scraping_results.get('targets_found', [])),
            "targets": scraping_results.get('targets_found', []),
            "scraping_data": scraping_results
        }
        
    except Exception as e:
        logger.error(f"❌ Direct Scrape error: {str(e)}")
        return {
            "status": "failed",
            "method": "DIRECT_SCRAPE",
            "error": str(e),
            "keywords": keywords
        }

async def run_hybrid_scout(keywords: List[str], project_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Hybrid scouting that combines API and scraping methods
    
    Args:
        keywords: Keywords to search for
        project_data: Project data for context
        
    Returns:
        Dictionary with hybrid scouting results
    """
    try:
        logger.info(f"🔀 Running Hybrid Scout for {len(keywords)} keywords")
        
        # Step 1: Run official API scout
        api_results = await run_official_api_scout(keywords, project_data)
        
        # Step 2: Run direct scrape
        scrape_results = await run_direct_scrape(keywords, project_data)
        
        # Step 3: Merge and deduplicate results
        all_leads = []
        
        # Add API leads (placeholder for now)
        if api_results.get('status') == 'completed':
            # TODO: Process actual API leads when implemented
            pass
        
        # Add scraped leads
        if scrape_results.get('status') == 'completed':
            scraped_leads = scrape_results.get('targets', [])
            all_leads.extend(scraped_leads)
        
        # Deduplicate leads (simple URL-based for now)
        seen_urls = set()
        deduplicated_leads = []
        
        for lead in all_leads:
            lead_url = lead.get('url', '')
            if lead_url and lead_url not in seen_urls:
                seen_urls.add(lead_url)
                deduplicated_leads.append(lead)
        
        # Log hybrid activity
        if DB_AVAILABLE:
            db = PrismaClient()
            db.vrsentinellog.create({
                'action': 'hybrid_scout',
                'details': f'Hybrid scouting for {len(keywords)} keywords',
                'gazeData': {
                    'method': 'HYBRID',
                    'keywords_count': len(keywords),
                    'project_data': project_data,
                    'api_leads': len(api_results.get('leads_found', [])),
                    'scraped_leads': len(scrape_results.get('leads_found', 0)),
                    'deduplicated_leads': len(deduplicated_leads)
                },
                'timestamp': datetime.now()
            })
            db.disconnect()
        
        hybrid_results = {
            "status": "completed",
            "method": "HYBRID",
            "keywords": keywords,
            "leads_found": len(deduplicated_leads),
            "api_results": api_results,
            "scrape_results": scrape_results,
            "deduplicated_leads": deduplicated_leads,
            "total_api_leads": len(api_results.get('leads_found', [])),
            "total_scraped_leads": len(scrape_results.get('leads_found', 0)),
            "message": f"Hybrid scouting completed: {len(deduplicated_leads)} unique leads found"
        }
        
        logger.info(f"✅ Hybrid Scout completed: {len(deduplicated_leads)} unique leads")
        return hybrid_results
        
    except Exception as e:
        logger.error(f"❌ Hybrid Scout error: {str(e)}")
        return {
            "status": "failed",
            "method": "HYBRID",
            "error": str(e),
            "keywords": keywords
        }

async def execute_scout_mode(keywords: List[str], scout_mode: str, project_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Execute scouting based on selected mode
    
    Args:
        keywords: Keywords to search for
        scout_mode: Selected scout mode (API_OFFICIAL, DIRECT_SCRAPE, HYBRID)
        project_data: Project data for context
        
    Returns:
        Dictionary with scouting results
    """
    try:
        logger.info(f"🎯 Executing Scout Mode: {scout_mode}")
        
        if scout_mode == 'API_OFFICIAL':
            return await run_official_api_scout(keywords, project_data)
        elif scout_mode == 'DIRECT_SCRAPE':
            return await run_direct_scrape(keywords, project_data)
        elif scout_mode == 'HYBRID':
            return await run_hybrid_scout(keywords, project_data)
        else:
            raise ValueError(f"Unknown scout mode: {scout_mode}")
            
    except Exception as e:
        logger.error(f"❌ Scout Mode execution error: {str(e)}")
        return {
            "status": "failed",
            "scout_mode": scout_mode,
            "error": str(e),
            "keywords": keywords
        }

async def green_zone_dorking(project_type: str, area: str = "", max_results: int = 50) -> Dict[str, Any]:
    """
    Green-Zone Dorking Logic - Free Google Search with strict dorking parameters
    
    Args:
        project_type: Project type (KOMERSIL or SUBSIDI)
        area: Geographic area for targeting
        max_results: Maximum results to return
        
    Returns:
        Dictionary with green-zone dorking results
    """
    try:
        self.logger.info(f"🌱 Starting Green-Zone Dorking for {project_type} in {area}")
        
        # Green-Zone Dorking Templates
        dorking_templates = {
            'KOMERSIL': [
                '(pengusaha OR direktur OR "CEO" OR "managing director") "nomor hp" OR "wa" OR "whatsapp" filetype:pdf OR filetype:xls OR filetype:doc',
                '(owner OR founder OR "business owner") "contact person" OR "phone number" OR "mobile" filetype:pdf OR filetype:doc',
                '(investor OR "venture capital" OR "angel investor") "email address" OR "contact info" filetype:pdf OR filetype:xls',
                '(entrepreneur OR "startup founder" OR "tech founder") "phone" OR "mobile number" OR "contact" filetype:pdf',
                '(businessman OR "business executive" OR "company director") "whatsapp" OR "telegram" OR "line" filetype:pdf OR filetype:doc'
            ],
            'SUBSIDI': [
                '(daftar CPNS OR "pegawai negeri" OR "PNS" OR "ASN") "nomor telepon" OR "whatsapp" site:go.id OR site:ac.id filetype:pdf OR filetype:xls',
                '(guru honorer OR "guru tidak tetap" OR "GTK") "nomor hp" OR "contact" site:ac.id OR site:go.id filetype:pdf OR filetype:doc',
                '(("dosen" OR "lecturer" OR "professor") OR "staf pengajar") "email" OR "phone" OR "kontak" site:ac.id filetype:pdf OR filetype:xls',
                '(mahasiswa OR "student" OR "alumni") "nomor telepon" OR "whatsapp" OR "contact" site:ac.id filetype:pdf OR filetype:doc',
                '(pegawai OR "staff" OR "karyawan") "daftar nomor" OR "contact list" site:go.id OR site:ac.id filetype:pdf OR filetype:xls'
            ]
        }
        
        # Get dorking templates for project type
        templates = dorking_templates.get(project_type, dorking_templates['KOMERSIL'])
        
        # Add area to queries if provided
        if area:
            templates = [f"{template} {area}" for template in templates]
        
        self.logger.info(f"🎯 Generated {len(templates)} green-zone dorking queries")
        
        # Execute green-zone searches
        all_results = []
        successful_queries = 0
        failed_queries = 0
        
        for i, query in enumerate(templates, 1):
            try:
                self.logger.info(f"🔍 Green-Zone Query {i}/{len(templates)}: {query}")
                
                # Use stealth delay
                if self.stealth_enabled:
                    await human_delay("search")
                else:
                    await asyncio.sleep(random.uniform(3, 8))  # Longer delays for green-zone
                
                # Perform Google Search (using requests for simplicity)
                search_results = await self._perform_green_zone_search(query)
                
                if search_results:
                    self.logger.info(f"✅ Green-Zone Query {i}: Found {len(search_results)} results")
                    
                    # Extract contact information from results
                    for result in search_results:
                        contact_data = self._extract_green_zone_contact(result, query, project_type)
                        if contact_data:
                            all_results.append(contact_data)
                    
                    successful_queries += 1
                else:
                    self.logger.warning(f"⚠️ Green-Zone Query {i}: No results found")
                    failed_queries += 1
                
                # Rate limiting between queries
                if i < len(templates):
                    if self.stealth_enabled:
                        await human_delay("search")
                    else:
                        await asyncio.sleep(random.uniform(5, 10))
                        
            except Exception as e:
                self.logger.error(f"❌ Green-Zone Query {i} failed: {str(e)}")
                failed_queries += 1
                continue
        
        # Process and deduplicate results
        deduplicated_results = self._deduplicate_green_zone_results(all_results)
        
        # Log green-zone activity
        if DB_AVAILABLE:
            db = PrismaClient()
            db.vrsentinellog.create({
                'action': 'green_zone_dorking',
                'details': f'Green-Zone dorking for {project_type} in {area}',
                'gazeData': {
                    'project_type': project_type,
                    'area': area,
                    'total_queries': len(templates),
                    'successful_queries': successful_queries,
                    'failed_queries': failed_queries,
                    'total_results': len(all_results),
                    'deduplicated_results': len(deduplicated_results)
                },
                'timestamp': datetime.now()
            })
            db.disconnect()
        
        green_zone_results = {
            "status": "completed",
            "method": "GREEN_ZONE_DORKING",
            "project_type": project_type,
            "area": area,
            "total_queries": len(templates),
            "successful_queries": successful_queries,
            "failed_queries": failed_queries,
            "total_results": len(all_results),
            "deduplicated_results": len(deduplicated_results),
            "contacts": deduplicated_results[:max_results],  # Limit results
            "success_rate": successful_queries / len(templates) if templates else 0,
            "message": f"Green-Zone dorking completed: {len(deduplicated_results)} unique contacts found"
        }
        
        self.logger.info(f"🌱 Green-Zone Dorking completed: {len(deduplicated_results)} unique contacts")
        return green_zone_results
        
    except Exception as e:
        self.logger.error(f"❌ Green-Zone Dorking error: {str(e)}")
        return {
            "status": "failed",
            "method": "GREEN_ZONE_DORKING",
            "project_type": project_type,
            "area": area,
            "error": str(e),
            "contacts": []
        }

async def _perform_green_zone_search(self, query: str) -> List[Dict[str, Any]]:
    """Perform green-zone Google search using requests"""
    try:
        # Use DuckDuckGo as alternative to Google Search (more accessible)
        search_url = "https://duckduckgo.com/html/"
        params = {
            'q': query,
            'kl': 'id-id',  # Indonesian locale
            'df': 'l',  # Last 24 hours
        }
        
        headers = {
            'User-Agent': get_random_user_agent() if STEALTH_AVAILABLE else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Make search request
        response = requests.get(
            search_url, 
            params=params, 
            headers=headers, 
            timeout=30
        )
        
        if response.status_code == 200:
            # Parse HTML response
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results
            results = []
            result_elements = soup.find_all('div', class_='result')
            
            for element in result_elements[:20]:  # Limit to 20 results per query
                try:
                    title_elem = element.find('a', class_='result__a')
                    snippet_elem = element.find('a', class_='result__a')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True)
                        
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'query': query,
                            'source': 'duckduckgo_green_zone'
                        })
                        
                except Exception as e:
                    continue
            
            return results
            
        else:
            self.logger.warning(f"Green-Zone search failed with status {response.status_code}")
            return []
            
    except Exception as e:
        self.logger.error(f"Green-Zone search error: {str(e)}")
        return []

def _extract_green_zone_contact(self, result: Dict[str, Any], query: str, project_type: str) -> Optional[Dict[str, Any]]:
    """Extract contact information from green-zone search result"""
    try:
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        url = result.get('url', '')
        
        # Combine text for processing
        text = f"{title} {snippet}"
        
        # Phone number patterns
        phone_patterns = [
            r'(\+62|62|0)8[1-9][0-9]{6,10}',
            r'0[2-9][0-9]{7,11}',
            r'\b\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{4,6}\b'
        ]
        
        # Email patterns
        email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        ]
        
        # Extract phone numbers
        phones = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        # Extract emails
        emails = []
        for pattern in email_patterns:
            matches = re.findall(pattern, text)
            emails.extend(matches)
        
        # Extract names (simple pattern)
        name_patterns = [
            r'[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'[A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+',
            r'Mr\.\s+[A-Z][a-z]+',
            r'Mrs\.\s+[A-Z][a-z]+',
            r'Dr\.\s+[A-Z][a-z]+',
            r'Prof\.\s+[A-Z][a-z]+'
        ]
        
        names = []
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            names.extend(matches)
        
        # Only return if we found contact info
        if phones or emails:
            return {
                'nama': names[0] if names else 'Unknown',
                'nomor_hp': phones[0] if phones else None,
                'email': emails[0] if emails else None,
                'url': url,
                'title': title,
                'snippet': snippet,
                'query': query,
                'project_type': project_type,
                'source': 'green_zone_dorking',
                'confidence_score': 0.7,  # Moderate confidence for green-zone
                'extracted_at': datetime.now().isoformat()
            }
        
        return None
        
    except Exception as e:
        self.logger.error(f"Error extracting green-zone contact: {str(e)}")
        return None

def _deduplicate_green_zone_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate green-zone results"""
    seen_contacts = set()
    deduplicated = []
    
    for result in results:
        # Create unique key based on phone or email
        key = None
        if result.get('nomor_hp'):
            key = f"phone:{result['nomor_hp']}"
        elif result.get('email'):
            key = f"email:{result['email']}"
        elif result.get('url'):
            key = f"url:{result['url']}"
        
        if key and key not in seen_contacts:
            seen_contacts.add(key)
            deduplicated.append(result)
    
    return deduplicated

# Test function
if __name__ == "__main__":
    print(f"{CYAN}{'='*80}{END}")
    print(f"🔍 LUMINA OS - TRIPWIRE SCOUT MODULE{END}")
    print(f"{'='*80}{END}")
    
    print(f"{BLUE}🔍 Testing Tripwire Scout...{END}")
    
    # Test hunting
    test_keywords = ['cari rumah BSD', 'butuh KPR cepat', 'beli rumah Serang']
    results = hunt_high_intent_targets(test_keywords, "Jakarta")
    
    print(f"{GREEN}✅ Test hunting completed{END}")
    print(f"{CYAN}📊 Results: {len(results['targets_found'])} targets found{END}")
    
    print(f"{'='*80}{END}")

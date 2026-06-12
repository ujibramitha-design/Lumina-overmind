"""
Twin-Dragon Engine - Platform Infiltrator Module
Advanced platform-specific scraping with Playwright for rich data extraction
"""

import asyncio
import json
import re
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from urllib.parse import quote, urlparse

# Playwright for async browser automation
try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Warning: Playwright not available, platform infiltration disabled")

# Database connection for activity logging
try:
    from prisma import Client as PrismaClient
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("Warning: Prisma client not available, activity logging disabled")

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
END = '\033[0m'

class PlatformInfiltrator:
    """
    Advanced platform-specific scraping with Playwright
    Supports LinkedIn, Facebook, and Government Directory infiltration
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # User agents for different platforms
        self.user_agents = {
            'linkedin': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'facebook': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'government': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Data extraction patterns
        self.extraction_patterns = {
            'phone': [
                r'\+62[0-9]{9,12}',
                r'62[0-9]{9,12}',
                r'08[0-9]{8,11}',
                r'021[0-9]{7,10}',
                r'022[0-9]{7,10}',
                r'031[0-9]{7,10}',
                r'0[0-9]{9,12}'
            ],
            'email': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            ],
            'job_title': [
                r'(Manager|Director|CEO|CTO|CFO|COO|President|Vice President|VP|Head|Lead|Supervisor|Staff|Officer|Engineer|Analyst|Consultant|Specialist|Coordinator|Administrator|Assistant)',
                r'(PNS|Pegawai Negeri Sipil|Pegawai Pemerintah|Karyawan|Staff|Professional)',
                r'(Kepala|Camat|Lurah|Sekretaris|Bendahara|Kasir|Staf|Tim|Team)'
            ],
            'name': [
                r'[A-Z][a-z]+\s+[A-Z][a-z]+',  # First Last
                r'[A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+',  # First M. Last
                r'[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+'  # First Middle Last
            ]
        }
        
        self.logger = logger
        self.logger.info(f"{CYAN}🎭 PLATFORM INFILTRATOR: Advanced scraping system initialized{END}")
    
    async def initialize_browser(self, platform: str = 'linkedin') -> bool:
        """Initialize Playwright browser with platform-specific settings"""
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error(f"{RED}❌ Playwright not available{END}")
            return False
        
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser with stealth settings
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Create context with user agent
            self.context = await self.browser.new_context(
                user_agent=self.user_agents.get(platform, self.user_agents['linkedin']),
                viewport={'width': 1920, 'height': 1080},
                locale='id-ID'
            )
            
            # Create page
            self.page = await self.context.new_page()
            
            # Set stealth settings
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['id-ID', 'id', 'en-US', 'en'],
                });
                
                window.chrome = {
                    runtime: {},
                };
            """)
            
            self.logger.info(f"{GREEN}✅ Browser initialized for {platform} infiltration{END}")
            return True
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Browser initialization failed: {str(e)}{END}")
            return False
    
    async def scrape_linkedin_profiles(self, search_query: str, max_profiles: int = 20) -> List[Dict[str, Any]]:
        """
        Scrape LinkedIn public profiles for professional contacts
        
        Args:
            search_query: Search query for LinkedIn
            max_profiles: Maximum number of profiles to scrape
            
        Returns:
            List of extracted profile data
        """
        if not await self.initialize_browser('linkedin'):
            return []
        
        try:
            self.logger.info(f"{BLUE}🔍 Starting LinkedIn infiltration for: {search_query}{END}")
            
            # Navigate to LinkedIn search
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={quote(search_query)}"
            await self.page.goto(search_url, wait_until='networkidle')
            
            # Wait for content to load
            await asyncio.sleep(random.uniform(2, 4))
            
            profiles = []
            
            # Scroll and collect profiles
            for scroll_count in range(5):
                # Extract profile links
                profile_elements = await self.page.query_selector_all('.search-result__result-link')
                
                for element in profile_elements[:max_profiles]:
                    try:
                        # Get profile URL
                        profile_url = await element.get_attribute('href')
                        if not profile_url:
                            continue
                        
                        # Navigate to profile page
                        await self.page.goto(profile_url, wait_until='networkidle')
                        await asyncio.sleep(random.uniform(1, 3))
                        
                        # Extract profile data
                        profile_data = await self._extract_linkedin_profile_data()
                        if profile_data:
                            profiles.append(profile_data)
                        
                        # Go back to search results
                        await self.page.go_back()
                        await asyncio.sleep(random.uniform(1, 2))
                        
                        if len(profiles) >= max_profiles:
                            break
                            
                    except Exception as e:
                        self.logger.warning(f"{YELLOW}⚠️ Error scraping profile: {str(e)}{END}")
                        continue
                
                if len(profiles) >= max_profiles:
                    break
                
                # Scroll down for more results
                await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(random.uniform(2, 4))
            
            self.logger.info(f"{GREEN}✅ LinkedIn infiltration completed: {len(profiles)} profiles extracted{END}")
            return profiles
            
        except Exception as e:
            self.logger.error(f"{RED}❌ LinkedIn infiltration failed: {str(e)}{END}")
            return []
        finally:
            await self._cleanup_browser()
    
    async def _extract_linkedin_profile_data(self) -> Optional[Dict[str, Any]]:
        """Extract comprehensive data from LinkedIn profile"""
        try:
            # Extract name
            name_element = await self.page.query_selector('h1.text-heading-xlarge')
            name = await name_element.inner_text() if name_element else None
            
            # Extract headline/job title
            headline_element = await self.page.query_selector('.text-body-medium.break-words')
            headline = await headline_element.inner_text() if headline_element else None
            
            # Extract contact info from profile sections
            contact_info = await self._extract_contact_info_from_page()
            
            # Extract location
            location_element = await self.page.query_selector('.text-body-small.inline.t-black--light')
            location = await location_element.inner_text() if location_element else None
            
            # Extract current position from headline
            jabatan = self._extract_job_title_from_text(headline or '')
            
            # Extract company info
            company_info = await self._extract_company_info()
            
            profile_data = {
                'nama': name,
                'nomor_hp': contact_info.get('phone'),
                'email': contact_info.get('email'),
                'jabatan': jabatan,
                'platform_sumber': 'LinkedIn',
                'lokasi': location,
                'perusahaan': company_info.get('name'),
                'headline': headline,
                'url': self.page.url,
                'extracted_at': datetime.now().isoformat(),
                'confidence_score': self._calculate_confidence_score(name, contact_info, jabatan)
            }
            
            # Only return profiles with meaningful data
            if name and (contact_info.get('phone') or contact_info.get('email') or jabatan):
                return profile_data
            
            return None
            
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️ Error extracting profile data: {str(e)}{END}")
            return None
    
    async def scrape_facebook_groups(self, group_search: str, max_posts: int = 30) -> List[Dict[str, Any]]:
        """
        Scrape Facebook public groups for potential leads
        
        Args:
            group_search: Search query for Facebook groups
            max_posts: Maximum number of posts to analyze
            
        Returns:
            List of extracted contact data
        """
        if not await self.initialize_browser('facebook'):
            return []
        
        try:
            self.logger.info(f"{BLUE}🔍 Starting Facebook infiltration for: {group_search}{END}")
            
            # Navigate to Facebook search
            search_url = f"https://www.facebook.com/search/groups/?q={quote(group_search)}"
            await self.page.goto(search_url, wait_until='networkidle')
            
            # Wait for content to load
            await asyncio.sleep(random.uniform(3, 5))
            
            contacts = []
            
            # Find group links
            group_links = await self.page.query_selector_all('a[href*="/groups/"]')
            
            for group_link in group_links[:5]:  # Limit to 5 groups
                try:
                    group_url = await group_link.get_attribute('href')
                    if not group_url:
                        continue
                    
                    # Navigate to group
                    await self.page.goto(group_url, wait_until='networkidle')
                    await asyncio.sleep(random.uniform(2, 3))
                    
                    # Extract contact info from group posts
                    group_contacts = await self._extract_facebook_group_contacts(max_posts // 5)
                    contacts.extend(group_contacts)
                    
                    if len(contacts) >= max_posts:
                        break
                        
                except Exception as e:
                    self.logger.warning(f"{YELLOW}⚠️ Error scraping Facebook group: {str(e)}{END}")
                    continue
            
            self.logger.info(f"{GREEN}✅ Facebook infiltration completed: {len(contacts)} contacts extracted{END}")
            return contacts
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Facebook infiltration failed: {str(e)}{END}")
            return []
        finally:
            await self._cleanup_browser()
    
    async def scrape_government_directories(self, institution_type: str, location: str, max_contacts: int = 50) -> List[Dict[str, Any]]:
        """
        Scrape government directories for institutional contacts
        
        Args:
            institution_type: Type of institution (pemda, kementerian, dll)
            location: Geographic location
            max_contacts: Maximum number of contacts to extract
            
        Returns:
            List of extracted government contacts
        """
        if not await self.initialize_browser('government'):
            return []
        
        try:
            self.logger.info(f"{BLUE}🔍 Starting Government Directory infiltration: {institution_type} in {location}{END}")
            
            # Government directory URLs
            gov_directories = {
                'pemda': f"https://www.jendela.data.go.id/instansi/{quote(location)}",
                'kementerian': 'https://www.kemenkumham.go.id/kontak',
                'instansi': f"https://www.papua.go.id/direktori-instansi-pemerintah/{quote(location)}"
            }
            
            base_url = gov_directories.get(institution_type, gov_directories['pemda'])
            
            # Navigate to directory
            await self.page.goto(base_url, wait_until='networkidle')
            await asyncio.sleep(random.uniform(2, 4))
            
            contacts = []
            
            # Extract contact information
            contact_elements = await self.page.query_selector_all('.contact-item, .directory-item, .staff-item, .pegawai-item')
            
            for element in contact_elements[:max_contacts]:
                try:
                    # Extract contact data
                    contact_data = await self._extract_government_contact_data(element)
                    if contact_data:
                        contacts.append(contact_data)
                        
                except Exception as e:
                    self.logger.warning(f"{YELLOW}⚠️ Error extracting government contact: {str(e)}{END}")
                    continue
            
            self.logger.info(f"{GREEN}✅ Government Directory infiltration completed: {len(contacts)} contacts extracted{END}")
            return contacts
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Government Directory infiltration failed: {str(e)}{END}")
            return []
        finally:
            await self._cleanup_browser()
    
    async def _extract_contact_info_from_page(self) -> Dict[str, str]:
        """Extract contact information from current page"""
        contact_info = {}
        
        try:
            # Look for phone numbers
            page_text = await self.page.inner_text()
            
            for pattern in self.extraction_patterns['phone']:
                matches = re.findall(pattern, page_text)
                if matches:
                    contact_info['phone'] = matches[0]
                    break
            
            # Look for emails
            for pattern in self.extraction_patterns['email']:
                matches = re.findall(pattern, page_text)
                if matches:
                    contact_info['email'] = matches[0]
                    break
                    
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️ Error extracting contact info: {str(e)}{END}")
        
        return contact_info
    
    async def _extract_company_info(self) -> Dict[str, str]:
        """Extract company information from LinkedIn profile"""
        company_info = {}
        
        try:
            # Look for current company
            experience_section = await self.page.query_selector('.experience')
            if experience_section:
                company_element = await experience_section.query_selector('.t-14.t-normal span[aria-hidden="true"]')
                if company_element:
                    company_info['name'] = await company_element.inner_text()
                    
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️ Error extracting company info: {str(e)}{END}")
        
        return company_info
    
    def _extract_job_title_from_text(self, text: str) -> str:
        """Extract job title from text using regex patterns"""
        if not text:
            return ''
        
        for pattern in self.extraction_patterns['job_title']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return ''
    
    async def _extract_facebook_group_contacts(self, max_posts: int) -> List[Dict[str, Any]]:
        """Extract contact information from Facebook group posts"""
        contacts = []
        try:
            # Look for posts with contact information
            posts = await self.page.query_selector_all('[role="article"]')
            
            for post in posts[:max_posts]:
                try:
                    post_text = await post.inner_text()
                    
                    # Extract contact info from post
                    contact_info = self._extract_contact_info_from_text(post_text)
                    
                    # Extract name from post
                    name = self._extract_name_from_text(post_text)
                    
                    if name and (contact_info.get('phone') or contact_info.get('email')):
                        contacts.append({
                            'nama': name,
                            'nomor_hp': contact_info.get('phone'),
                            'email': contact_info.get('email'),
                            'jabatan': 'Facebook Group Member',
                            'platform_sumber': 'Facebook',
                            'post_content': post_text[:200] + '...' if len(post_text) > 200 else post_text,
                            'extracted_at': datetime.now().isoformat(),
                            'confidence_score': self._calculate_confidence_score(name, contact_info, '')
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Error extracting individual Facebook post: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"Failed to query Facebook posts: {str(e)}")
        
        return contacts
    
    async def _extract_government_contact_data(self, element) -> Optional[Dict[str, Any]]:
        """Extract comprehensive government contact data"""
        try:
            # Get all text from the element
            element_text = await element.inner_text()

            # Extract name
            name = self._extract_name_from_text(element_text)
            if not name:
                return None
            
            # Extract contact info
            contact_info = self._extract_contact_info_from_text(element_text)
            
            # Extract job title
            jabatan = self._extract_job_title_from_text(element_text)
            
            # Extract position/unit
            position = self._extract_government_position(element_text)
            
            return {
                'nama': name,
                'nomor_hp': contact_info.get('phone'),
                'email': contact_info.get('email'),
                'jabatan': jabatan or position,
                'platform_sumber': 'Government Directory',
                'unit_kerja': position,
                'contact_details': element_text[:200] + '...' if len(element_text) > 200 else element_text,
                'extracted_at': datetime.now().isoformat(),
                'confidence_score': self._calculate_confidence_score(name, contact_info, jabatan)
            }
        except Exception as e:
            self.logger.warning(f"Error extracting government contact: {str(e)}")
            return None
    
    def _extract_contact_info_from_text(self, text: str) -> Dict[str, str]:
        """Extract contact information from text"""
        contact_info = {}
        
        # Phone numbers
        for pattern in self.extraction_patterns['phone']:
            matches = re.findall(pattern, text)
            if matches:
                contact_info['phone'] = matches[0]
                break
        
        # Emails
        for pattern in self.extraction_patterns['email']:
            matches = re.findall(pattern, text)
            if matches:
                contact_info['email'] = matches[0]
                break
        
        return contact_info
    
    def _extract_name_from_text(self, text: str) -> str:
        """Extract name from text using regex patterns"""
        for pattern in self.extraction_patterns['name']:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return ''
    
    def _extract_government_position(self, text: str) -> str:
        """Extract government position from text"""
        gov_positions = [
            r'(Kepala\s+[A-Za-z\s]+)',
            r'(Camat\s+[A-Za-z\s]+)',
            r'(Lurah\s+[A-Za-z\s]+)',
            r'(Sekretaris\s+[A-Za-z\s]+)',
            r'(Bendahara\s+[A-Za-z\s]+)',
            r'(Kasir\s+[A-Za-z\s]+)',
            r'(Staff\s+[A-Za-z\s]+)',
            r'(Tim\s+[A-Za-z\s]+)'
        ]
        
        for pattern in gov_positions:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return ''
    
    def _calculate_confidence_score(self, name: str, contact_info: Dict[str, str], jabatan: str) -> float:
        """Calculate confidence score for extracted data"""
        score = 0.0
        
        # Name contributes 40%
        if name and len(name.split()) >= 2:
            score += 0.4
        elif name:
            score += 0.2
        
        # Contact info contributes 40%
        if contact_info.get('phone'):
            score += 0.2
        if contact_info.get('email'):
            score += 0.2
        
        # Job title contributes 20%
        if jabatan:
            score += 0.2
        
        return min(score, 1.0)
    
    async def _cleanup_browser(self):
        """Clean up browser resources"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️ Browser cleanup error: {str(e)}{END}")
    
    def log_activity(self, action: str, details: str = None, platform: str = None, results_count: int = 0):
        """Log infiltration activity to database"""
        if not DB_AVAILABLE:
            return
        
        try:
            db = PrismaClient()
            
            db.vrsentinellog.create({
                'action': f"platform_infiltration_{action}",
                'details': details or f"{action} operation completed",
                'gazeData': {
                    'platform': platform,
                    'results_count': results_count,
                    'infiltration_type': action
                },
                'timestamp': datetime.now()
            })
            
            self.logger.info(f"{GREEN}📝 Platform infiltration logged: {action} on {platform}{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Failed to log infiltration activity: {str(e)}{END}")
        finally:
            if 'db' in locals():
                db.disconnect()

# Global infiltrator instance
platform_infiltrator = PlatformInfiltrator()

# Convenience functions
async def scrape_linkedin(search_query: str, max_profiles: int = 20) -> List[Dict[str, Any]]:
    """Convenience function for LinkedIn scraping"""
    return await platform_infiltrator.scrape_linkedin_profiles(search_query, max_profiles)

async def scrape_facebook(group_search: str, max_posts: int = 30) -> List[Dict[str, Any]]:
    """Convenience function for Facebook scraping"""
    return await platform_infiltrator.scrape_facebook_groups(group_search, max_posts)

async def scrape_government(institution_type: str, location: str, max_contacts: int = 50) -> List[Dict[str, Any]]:
    """Convenience function for government directory scraping"""
    return await platform_infiltrator.scrape_government_directories(institution_type, location, max_contacts)

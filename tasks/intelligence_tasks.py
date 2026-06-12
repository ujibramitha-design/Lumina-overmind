"""
LUMINA OS - INTELLIGENCE TASKS
================================

Async intelligence processing tasks for lead scouting,
market analysis, trend detection, and data processing.

Features:
- 48-Radar Scout Engine with extreme intelligence protocols
- Market trend analysis and entity extraction
- Lead scoring with intent classification
- Proxy rotation and anti-detection measures
- Telecom HLR database integration
- Urban foresight and government affinity analysis
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Import Celery app
from tasks.celery_app import celery_app, intelligence_task
from core_modules.proxy_rotator import proxy_rotator
from core_modules.intelligence.mass_scout import TripwireScout
from core_modules.intelligence.telecom_hlr_db import INDONESIA_HLR_MAPPING
from agents.scout_agent.gov_affinity_scout import GovAffinityScout
from agents.scout_agent.urban_foresight_scout import generate_future_map
from core_modules.trend_analyzer import analyze_market_trends

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@intelligence_task
def scout_leads(
    self,
    campaign_mode: str,
    area: str,
    keywords: List[str],
    max_results: int = 100,
    use_proxy: bool = True,
    target_region: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scout leads using 48-Radar Scout Engine with extreme intelligence protocols
    
    Args:
        campaign_mode: Campaign mode (BASIC, HLR_SNIPER, EXTREME_INTELLIGENCE, etc.)
        area: Target geographic area
        keywords: Search keywords
        max_results: Maximum number of results
        use_proxy: Whether to use proxy rotation
        target_region: Target region for HLR scanning
    
    Returns:
        Dictionary containing scouting results
    """
    
    try:
        logger.info(f"Starting lead scouting: {campaign_mode} in {area}")
        
        # Initialize mass scout
        scout = TripwireScout()
        
        # Generate dork queries based on campaign mode
        queries = scout.generate_dork_queries(campaign_mode, area, keywords)
        
        # Add HLR-specific queries if HLR_SNIPER mode
        if campaign_mode == 'HLR_SNIPER' and target_region:
            hlr_queries = generate_hlr_queries(target_region, keywords)
            queries.extend(hlr_queries)
        
        # Execute search queries
        all_results = []
        
        for query in queries:
            try:
                # Use stealth request if proxy enabled
                if use_proxy:
                    response, error = proxy_rotator.make_stealth_request(
                        url=query['url'],
                        method='GET',
                        timeout=30
                    )
                else:
                    response = requests.get(query['url'], timeout=30)
                    error = None
                
                if error:
                    logger.warning(f"Query failed: {query['url']} - {error}")
                    continue
                
                # Extract leads from search results
                leads = extract_leads_from_search_results(
                    response.text,
                    query['keywords'],
                    campaign_mode
                )
                
                all_results.extend(leads)
                
                # Check if we have enough results
                if len(all_results) >= max_results:
                    break
                    
            except Exception as e:
                logger.error(f"Error processing query {query['url']}: {e}")
                continue
        
        # Process and validate leads
        processed_leads = []
        for lead in all_results[:max_results]:
            processed_lead = process_lead_data(lead, campaign_mode, area)
            if processed_lead:
                processed_leads.append(processed_lead)
        
        logger.info(f"Lead scouting completed: {len(processed_leads)} leads found")
        
        return {
            'success': True,
            'campaign_mode': campaign_mode,
            'area': area,
            'keywords': keywords,
            'leads_found': len(processed_leads),
            'leads': processed_leads,
            'queries_used': len(queries),
            'scouted_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Lead scouting failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@intelligence_task
def analyze_market_trends(
    self,
    days: int = 30,
    area: Optional[str] = None,
    include_entity_analysis: bool = True
) -> Dict[str, Any]:
    """
    Analyze market trends and generate intelligence reports
    
    Args:
        days: Number of days to analyze
        area: Specific area to focus on
        include_entity_analysis: Whether to include entity extraction
    
    Returns:
        Dictionary containing trend analysis results
    """
    
    try:
        logger.info(f"Starting market trend analysis: {days} days")
        
        # Generate trend report
        trend_report = analyze_market_trends(days)
        
        # Add area-specific analysis if provided
        if area:
            area_analysis = analyze_area_trends(area, days)
            trend_report['area_analysis'] = area_analysis
        
        # Add entity analysis if requested
        if include_entity_analysis:
            entity_analysis = extract_entity_trends(days)
            trend_report['entity_analysis'] = entity_analysis
        
        logger.info(f"Market trend analysis completed")
        
        return {
            'success': True,
            'analysis_period': days,
            'trend_report': trend_report,
            'analyzed_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Market trend analysis failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@intelligence_task
def generate_area_intelligence_report(
    self,
    coordinates: Tuple[float, float],
    area_name: str,
    include_gov_analysis: bool = True,
    include_urban_analysis: bool = True
) -> Dict[str, Any]:
    """
    Generate comprehensive area intelligence report
    
    Args:
        coordinates: Latitude and longitude
        area_name: Name of the area
        include_gov_analysis: Whether to include government affinity analysis
        include_urban_analysis: Whether to include urban foresight analysis
    
    Returns:
        Dictionary containing area intelligence report
    """
    
    try:
        logger.info(f"Generating area intelligence report: {area_name}")
        
        report = {
            'area_name': area_name,
            'coordinates': coordinates,
            'generated_at': datetime.now().isoformat()
        }
        
        # Government affinity analysis
        if include_gov_analysis:
            try:
                scout = GovAffinityScout()
                gov_report = scout.generate_market_intelligence_report(coordinates)
                report['government_analysis'] = gov_report
            except Exception as e:
                logger.error(f"Government analysis failed: {e}")
                report['government_analysis'] = {'error': str(e)}
        
        # Urban foresight analysis
        if include_urban_analysis:
            try:
                urban_report = generate_future_map(coordinates, area_name)
                report['urban_analysis'] = urban_report
            except Exception as e:
                logger.error(f"Urban analysis failed: {e}")
                report['urban_analysis'] = {'error': str(e)}
        
        logger.info(f"Area intelligence report completed: {area_name}")
        
        return {
            'success': True,
            'report': report
        }
        
    except Exception as e:
        logger.error(f"Area intelligence report failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@intelligence_task
def health_check_proxies(self) -> Dict[str, Any]:
    """
    Health check all proxies in the rotation pool
    
    Returns:
        Dictionary containing proxy health status
    """
    
    try:
        logger.info("Starting proxy health check")
        
        proxy_rotator.health_check_proxies()
        
        stats = proxy_rotator.get_statistics()
        
        logger.info(f"Proxy health check completed: {stats['active_proxies']}/{stats['total_proxies']} active")
        
        return {
            'success': True,
            'proxy_stats': stats,
            'checked_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Proxy health check failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@intelligence_task
def process_lead_batch(
    self,
    leads: List[Dict[str, Any]],
    campaign_id: Optional[str] = None,
    enable_entity_extraction: bool = True,
    enable_intent_classification: bool = True
) -> Dict[str, Any]:
    """
    Process batch of leads with entity extraction and intent classification
    
    Args:
        leads: List of lead data
        campaign_id: Campaign ID
        enable_entity_extraction: Whether to extract entities
        enable_intent_classification: Whether to classify intent
    
    Returns:
        Dictionary containing processing results
    """
    
    try:
        logger.info(f"Processing lead batch: {len(leads)} leads")
        
        processed_leads = []
        
        for lead in leads:
            try:
                processed_lead = lead.copy()
                
                # Entity extraction
                if enable_entity_extraction:
                    entities = extract_entities_from_text(lead.get('content', ''))
                    processed_lead['entities'] = entities
                
                # Intent classification
                if enable_intent_classification:
                    intent = classify_lead_intent(lead.get('content', ''))
                    processed_lead['intent'] = intent
                
                # Lead scoring
                score = calculate_lead_score(processed_lead)
                processed_lead['score'] = score
                
                processed_leads.append(processed_lead)
                
            except Exception as e:
                logger.error(f"Error processing lead: {e}")
                continue
        
        logger.info(f"Lead batch processing completed: {len(processed_leads)} leads processed")
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'total_leads': len(leads),
            'processed_leads': len(processed_leads),
            'leads': processed_leads,
            'processed_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Lead batch processing failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@intelligence_task
def generate_daily_reports(self) -> Dict[str, Any]:
    """
    Generate daily intelligence reports
    
    Returns:
        Dictionary containing daily reports
    """
    
    try:
        logger.info("Generating daily intelligence reports")
        
        reports = {}
        
        # Market trends report
        try:
            market_report = analyze_market_trends(1)
            reports['market_trends'] = market_report
        except Exception as e:
            logger.error(f"Market trends report failed: {e}")
            reports['market_trends'] = {'error': str(e)}
        
        # Proxy health report
        try:
            proxy_stats = proxy_rotator.get_statistics()
            reports['proxy_health'] = proxy_stats
        except Exception as e:
            logger.error(f"Proxy health report failed: {e}")
            reports['proxy_health'] = {'error': str(e)}
        
        # System performance report
        try:
            from tasks.celery_app import TaskMonitor
            task_stats = TaskMonitor.get_task_stats()
            reports['system_performance'] = task_stats
        except Exception as e:
            logger.error(f"System performance report failed: {e}")
            reports['system_performance'] = {'error': str(e)}
        
        logger.info("Daily reports generation completed")
        
        return {
            'success': True,
            'reports': reports,
            'generated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Daily reports generation failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

# Helper functions

def generate_hlr_queries(target_region: str, keywords: List[str]) -> List[Dict[str, Any]]:
    """Generate HLR-specific queries for target region"""
    
    queries = []
    
    if target_region in INDONESIA_HLR_MAPPING:
        prefixes = INDONESIA_HLR_MAPPING[target_region]
        
        for prefix in prefixes:
            for keyword in keywords:
                # Generate search queries with HLR prefixes
                query = f"{keyword} {prefix}"
                search_url = f"https://duckduckgo.com/html/?q={query}"
                
                queries.append({
                    'url': search_url,
                    'keywords': [keyword],
                    'type': 'hlr_search',
                    'prefix': prefix
                })
    
    return queries

def extract_leads_from_search_results(html_content: str, keywords: List[str], campaign_mode: str) -> List[Dict[str, Any]]:
    """Extract leads from search results HTML"""
    
    leads = []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find search result elements
        results = soup.find_all('div', class_='result') or soup.find_all('div', class_='web-result')
        
        for result in results:
            try:
                lead = extract_lead_from_result(result, keywords, campaign_mode)
                if lead:
                    leads.append(lead)
            except Exception as e:
                logger.debug(f"Error extracting lead from result: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error parsing search results: {e}")
    
    return leads

def extract_lead_from_result(result_element, keywords: List[str], campaign_mode: str) -> Optional[Dict[str, Any]]:
    """Extract lead information from a single search result"""
    
    try:
        # Extract title and URL
        title_elem = result_element.find('a', class_='result__a') or result_element.find('a')
        if not title_elem:
            return None
        
        title = title_elem.get_text(strip=True)
        url = title_elem.get('href')
        
        if not url:
            return None
        
        # Extract description
        desc_elem = result_element.find('div', class_='result__snippet') or result_element.find('div', class_='snippet')
        description = desc_elem.get_text(strip=True) if desc_elem else ''
        
        # Extract contact information
        text_content = f"{title} {description}"
        contacts = extract_contact_info(text_content)
        
        # Create lead object
        lead = {
            'title': title,
            'url': url,
            'description': description,
            'content': text_content,
            'keywords': keywords,
            'campaign_mode': campaign_mode,
            'contacts': contacts,
            'extracted_at': datetime.now().isoformat()
        }
        
        return lead
        
    except Exception as e:
        logger.debug(f"Error extracting lead from result: {e}")
        return None

def extract_contact_info(text: str) -> Dict[str, List[str]]:
    """Extract contact information from text"""
    
    contacts = {
        'phone_numbers': [],
        'emails': [],
        'websites': []
    }
    
    # Phone number regex for Indonesian numbers
    phone_pattern = r'(\+62|62|0)8[1-9][0-9]{6,10}'
    phone_matches = re.findall(phone_pattern, text)
    contacts['phone_numbers'] = list(set(phone_matches))
    
    # Email regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, text)
    contacts['emails'] = list(set(email_matches))
    
    # Website regex
    website_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    website_matches = re.findall(website_pattern, text)
    contacts['websites'] = list(set(website_matches))
    
    return contacts

def process_lead_data(lead: Dict[str, Any], campaign_mode: str, area: str) -> Optional[Dict[str, Any]]:
    """Process and validate lead data"""
    
    try:
        # Validate required fields
        if not lead.get('title') or not lead.get('url'):
            return None
        
        # Add processing metadata
        lead['campaign_mode'] = campaign_mode
        lead['area'] = area
        lead['processed_at'] = datetime.now().isoformat()
        
        # Calculate initial score
        lead['initial_score'] = calculate_initial_score(lead)
        
        return lead
        
    except Exception as e:
        logger.error(f"Error processing lead data: {e}")
        return None

def calculate_initial_score(lead: Dict[str, Any]) -> float:
    """Calculate initial lead score based on available data"""
    
    score = 0.0
    
    # Phone number presence
    if lead.get('contacts', {}).get('phone_numbers'):
        score += 0.3
    
    # Email presence
    if lead.get('contacts', {}).get('emails'):
        score += 0.2
    
    # Website presence
    if lead.get('contacts', {}).get('websites'):
        score += 0.1
    
    # Keywords in title
    title = lead.get('title', '').lower()
    for keyword in lead.get('keywords', []):
        if keyword.lower() in title:
            score += 0.1
    
    # Campaign mode bonus
    campaign_mode = lead.get('campaign_mode', '')
    if campaign_mode in ['EXTREME_INTELLIGENCE', 'HLR_SNIPER']:
        score += 0.2
    elif campaign_mode in ['PANOPTICON', 'LEVIATHAN']:
        score += 0.15
    
    return min(score, 1.0)

def extract_entities_from_text(text: str) -> Dict[str, Any]:
    """Extract entities from text using regex patterns"""
    
    entities = {
        'price': [],
        'location': [],
        'bank': [],
        'pain_point': []
    }
    
    # Price extraction
    price_patterns = [
        r'(\d+\s*(?:juta|miliar|ribu|jt|milyar|rb))\s*(?:rupiah|rp)',
        r'(?:rp|rupiah)\s*(\d+(?:\.\d+)?)',
        r'harga\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in price_patterns:
        matches = re.findall(pattern, text.lower())
        entities['price'].extend(matches)
    
    # Location extraction
    location_patterns = [
        r'(?:di|daerah|wilayah|kawasan)\s*([a-zA-Z\s]+?)(?:[,\.]|$)',
        r'cluster\s*([a-zA-Z0-9\s]+)',
        r'perumahan\s*([a-zA-Z0-9\s]+)'
    ]
    
    for pattern in location_patterns:
        matches = re.findall(pattern, text.lower())
        entities['location'].extend(matches)
    
    # Bank extraction
    bank_pattern = r'(btn|bni|bri|bca|mandiri|cimb|danamon|permata|panin)'
    bank_matches = re.findall(bank_pattern, text.lower())
    entities['bank'].extend(bank_matches)
    
    # Pain point extraction
    pain_point_patterns = [
        r'(?:(?:khawatir|sulit|bingung)\s*(?:dengan|tentang|soal))\s*([a-zA-Z\s]+)',
        r'(?:masalah|kendala)\s*([a-zA-Z\s]+)'
    ]
    
    for pattern in pain_point_patterns:
        matches = re.findall(pattern, text.lower())
        entities['pain_point'].extend(matches)
    
    # Remove duplicates and empty strings
    for key in entities:
        entities[key] = list(set(filter(None, entities[key])))
    
    return entities

def classify_lead_intent(text: str) -> str:
    """Classify lead intent based on text content"""
    
    text_lower = text.lower()
    
    # Informational indicators
    informational_keywords = ['tanya', 'info', 'informasi', 'detail', 'spek', 'fasilitas', 'lokasi']
    
    # Comparison indicators
    comparison_keywords = ['bandingkan', 'perbandingan', 'pilih', 'mana', 'lebih', 'bagus', 'cocok']
    
    # Pain-Point indicators
    pain_point_keywords = ['khawatir', 'sulit', 'bingung', 'masalah', 'belum', 'tidak']
    
    # Transactional indicators
    transactional_keywords = ['beli', 'beli rumah', 'cari rumah', 'butuh rumah', 'survey', 'nego', 'deal', 'booking']
    
    # Count keyword matches
    informational_count = sum(1 for keyword in informational_keywords if keyword in text_lower)
    comparison_count = sum(1 for keyword in comparison_keywords if keyword in text_lower)
    pain_point_count = sum(1 for keyword in pain_point_keywords if keyword in text_lower)
    transactional_count = sum(1 for keyword in transactional_keywords if keyword in text_lower)
    
    # Determine intent based on highest count
    counts = {
        'Informational': informational_count,
        'Comparison': comparison_count,
        'Pain-Point': pain_point_count,
        'Transactional': transactional_count
    }
    
    return max(counts, key=counts.get)

def calculate_lead_score(lead: Dict[str, Any]) -> float:
    """Calculate comprehensive lead score"""
    
    score = lead.get('initial_score', 0.0)
    
    # Entity-based scoring
    entities = lead.get('entities', {})
    
    # Price mentions
    if entities.get('price'):
        score += 0.1
    
    # Location mentions
    if entities.get('location'):
        score += 0.1
    
    # Bank mentions
    if entities.get('bank'):
        score += 0.05
    
    # Pain point mentions
    if entities.get('pain_point'):
        score += 0.15
    
    # Intent-based scoring
    intent = lead.get('intent', 'Informational')
    intent_scores = {
        'Transactional': 0.3,
        'Pain-Point': 0.25,
        'Comparison': 0.2,
        'Informational': 0.1
    }
    
    score += intent_scores.get(intent, 0.1)
    
    return min(score, 1.0)

def analyze_area_trends(area: str, days: int) -> Dict[str, Any]:
    """Analyze trends for specific area"""
    
    # This would implement area-specific trend analysis
    # For now, return placeholder data
    return {
        'area': area,
        'trend_score': 0.7,
        'trending_topics': ['property', 'investment', 'development'],
        'recommendations': ['Focus on luxury properties', 'Highlight investment potential']
    }

def extract_entity_trends(days: int) -> Dict[str, Any]:
    """Extract entity-based trends"""
    
    # This would implement entity trend analysis
    # For now, return placeholder data
    return {
        'price_trends': ['300-500 juta', '500-800 juta'],
        'location_trends': ['Jakarta', 'Surabaya', 'Bandung'],
        'bank_trends': ['BCA', 'BNI', 'BRI'],
        'pain_point_trends': ['DP', 'KPR', 'lokasi']
    }

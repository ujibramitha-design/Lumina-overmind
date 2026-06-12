"""
LinkedIn Executive Scout - High-Net-Worth Individual Hunter
Scans LinkedIn for executive career trigger events and identifies high-value prospects

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import json
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import core modules
from core_modules.db_manager import DatabaseManager

# Configure logging
logger = logging.getLogger(__name__)

class TriggerEventType(Enum):
    """Career trigger event types"""
    PROMOTION = "promotion"
    RELOCATION = "relocation"
    COMPANY_IPO = "company_ipo"
    COMPANY_FUNDING = "company_funding"

@dataclass
class ExecutiveProfile:
    """Executive profile data structure"""
    name: str
    current_position: str
    company: str
    industry: str
    experience_years: int
    education: str
    location: str
    linkedin_url: str
    trigger_events: List[Dict[str, Any]]
    net_worth_estimate: str
    purchase_probability: int

class LinkedInExecScout:
    """LinkedIn Executive Scout for High-Net-Worth Individual Hunting"""
    
    def __init__(self):
        self.name = "LinkedIn Executive Scout"
        self.version = "1.0.0"
        self.db_manager = DatabaseManager()
        
        # API Credentials (Blueprint for future implementation)
        self.api_credentials = {
            'linkedin_access_token': os.getenv('LINKEDIN_ACCESS_TOKEN', ''),
            'linkedin_client_id': os.getenv('LINKEDIN_CLIENT_ID', ''),
            'linkedin_client_secret': os.getenv('LINKEDIN_CLIENT_SECRET', ''),
            'apify_linkedin_token': os.getenv('APIFY_LINKEDIN_TOKEN', '')
        }
        
        # Target companies for executive hunting
        self.target_companies = [
            'Gojek', 'Tokopedia', 'Traveloka', 'Bukalapak', 'OVO',
            'DANA', 'Shopee', 'Lazada', 'Sea Group', 'Grab',
            'Telkom Indonesia', 'Bank Central Asia', 'Bank Mandiri',
            'Bank Rakyat', 'Astra International', 'Unilever Indonesia',
            'Coca-Cola Amatil', 'Nestle Indonesia', 'Procter & Gamble',
            'Microsoft Indonesia', 'Google Indonesia', 'Amazon Indonesia'
        ]
        
        # Target cities for relocation monitoring
        self.target_cities = [
            'Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang',
            'Makassar', 'Palembang', 'Tangerang', 'Depok', 'Bekasi',
            'Bogor', 'Batam', 'Pekanbaru', 'Bandar Lampung', 'Malang'
        ]
        
        # Executive positions to target
        self.executive_positions = [
            'CEO', 'CTO', 'CFO', 'COO', 'President Director',
            'Vice President', 'Director', 'Senior Manager',
            'Head of', 'Chief', 'Managing Director',
            'Executive Director', 'Regional Director'
        ]
        
        # Realistic Indonesian executive names
        self.executive_names = [
            'Budi Santoso', 'Andi Wijaya', 'Rudi Hartono', 'Eko Prasetyo',
            'Hendro Wibowo', 'Fajar Kusuma', 'Dewi Lestari', 'Siti Nurhaliza',
            'Ahmad Fauzi', 'Muhammad Rizki', 'Putri Permata', 'Rina Amelia',
            'Bambang Sutrisno', 'Cahyo Nugroho', 'Indah Permata', 'Reza Pahlevi',
            'Taufik Hidayat', 'Yuni Kartika', 'Doni Prasetyo', 'Maya Sari'
        ]
        
        # Industry classifications
        self.industries = [
            'Technology', 'Finance', 'Banking', 'E-commerce', 'Telecommunications',
            'Manufacturing', 'Consumer Goods', 'Consulting', 'Healthcare', 'Real Estate',
            'Energy', 'Transportation', 'Media', 'Entertainment', 'Education'
        ]
        
        # Educational backgrounds
        self.education_backgrounds = [
            'University of Indonesia', 'Gadjah Mada University', 'Bandung Institute of Technology',
            'Airlangga University', 'University of Indonesia', 'Binus University',
            'Trisakti University', 'Padjadjaran University', 'University of Indonesia',
            'Harvard University', 'Stanford University', 'MIT', 'Carnegie Mellon',
            'Oxford University', 'Cambridge University', 'NUS', 'NTU'
        ]
        
        logger.info(f"🎯 {self.name} v{self.version} initialized")
        logger.info(f"👔 Targeting {len(self.target_companies)} companies")
        logger.info(f"🌍 Monitoring {len(self.target_cities)} cities")
        logger.info(f"💼 Focusing on {len(self.executive_positions)} executive positions")
    
    def scan_career_trigger_events(self, target_companies: List[str], target_cities: List[str]) -> Dict[str, Any]:
        """
        Scan LinkedIn for career trigger events among executives
        
        Args:
            target_companies: List of target companies to monitor
            target_cities: List of target cities for relocation monitoring
            
        Returns:
            Dict containing scan results and executive profiles
        """
        
        logger.info(f"🔍 Starting LinkedIn executive career trigger event scan...")
        logger.info(f"🏢 Target Companies: {target_companies}")
        logger.info(f"🌍 Target Cities: {target_cities}")
        
        scan_results = {
            'scan_id': f"linkedin_exec_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'target_companies': target_companies,
            'target_cities': target_cities,
            'start_time': datetime.now().isoformat(),
            'executive_profiles': [],
            'trigger_events_found': {
                'promotion': 0,
                'relocation': 0,
                'company_ipo': 0,
                'company_funding': 0
            },
            'high_value_executives': [],
            'statistics': {
                'total_profiles_scanned': 0,
                'high_net_worth_count': 0,
                'trigger_events_total': 0,
                'average_purchase_probability': 0
            },
            'end_time': None,
            'duration_seconds': 0
        }
        
        # Simulate LinkedIn API calls (in real implementation, this would use LinkedIn API)
        logger.info("📡 Simulating LinkedIn API calls for executive profiles...")
        
        # Generate executive profiles with trigger events
        executive_profiles = self._generate_executive_profiles(target_companies, target_cities)
        scan_results['executive_profiles'] = executive_profiles
        scan_results['statistics']['total_profiles_scanned'] = len(executive_profiles)
        
        # Analyze and categorize trigger events
        high_value_executives = []
        total_purchase_probability = 0
        
        for profile in executive_profiles:
            # Count trigger events
            for event in profile.trigger_events:
                event_type = event['type']
                scan_results['trigger_events_found'][event_type] += 1
                scan_results['statistics']['trigger_events_total'] += 1
            
            # Calculate purchase probability
            total_purchase_probability += profile.purchase_probability
            
            # Identify high-net-worth individuals
            if profile.purchase_probability >= 80:
                high_value_executives.append(profile)
                scan_results['statistics']['high_net_worth_count'] += 1
        
        scan_results['high_value_executives'] = high_value_executives
        scan_results['statistics']['average_purchase_probability'] = (
            total_purchase_probability / len(executive_profiles) if executive_profiles else 0
        )
        
        # Calculate duration
        scan_results['end_time'] = datetime.now().isoformat()
        start_dt = datetime.fromisoformat(scan_results['start_time'])
        end_dt = datetime.fromisoformat(scan_results['end_time'])
        scan_results['duration_seconds'] = (end_dt - start_dt).total_seconds()
        
        logger.info(f"✅ LinkedIn executive scan completed in {scan_results['duration_seconds']:.2f}s")
        logger.info(f"👔 Total profiles scanned: {scan_results['statistics']['total_profiles_scanned']}")
        logger.info(f"💎 High-net-worth executives: {scan_results['statistics']['high_net_worth_count']}")
        logger.info(f"🎯 Trigger events found: {scan_results['statistics']['trigger_events_total']}")
        logger.info(f"📈 Average purchase probability: {scan_results['statistics']['average_purchase_probability']:.1f}%")
        
        return scan_results
    
    def _generate_executive_profiles(self, target_companies: List[str], target_cities: List[str]) -> List[ExecutiveProfile]:
        """Generate realistic executive profiles with trigger events"""
        
        profiles = []
        
        # Generate 15-25 executive profiles
        profile_count = random.randint(15, 25)
        
        for i in range(profile_count):
            # Generate base executive profile
            name = random.choice(self.executive_names)
            position = random.choice(self.executive_positions)
            company = random.choice(target_companies)
            industry = random.choice(self.industries)
            experience_years = random.randint(8, 25)
            education = random.choice(self.education_backgrounds)
            location = random.choice(target_cities)
            
            # Generate trigger events
            trigger_events = self._generate_trigger_events(company, location)
            
            # Calculate net worth estimate
            net_worth = self._estimate_net_worth(position, company, experience_years, trigger_events)
            
            # Calculate purchase probability based on trigger events
            purchase_probability = self._calculate_purchase_probability(trigger_events, net_worth)
            
            # Create LinkedIn URL
            linkedin_url = f"https://linkedin.com/in/{name.lower().replace(' ', '-').replace('.', '')}"
            
            profile = ExecutiveProfile(
                name=name,
                current_position=position,
                company=company,
                industry=industry,
                experience_years=experience_years,
                education=education,
                location=location,
                linkedin_url=linkedin_url,
                trigger_events=trigger_events,
                net_worth_estimate=net_worth,
                purchase_probability=purchase_probability
            )
            
            profiles.append(profile)
        
        # Sort by purchase probability (highest first)
        profiles.sort(key=lambda x: x.purchase_probability, reverse=True)
        
        return profiles
    
    def _generate_trigger_events(self, company: str, location: str) -> List[Dict[str, Any]]:
        """Generate realistic trigger events for executive"""
        
        trigger_events = []
        event_count = random.randint(0, 3)  # Each executive can have 0-3 trigger events
        
        for i in range(event_count):
            event_type = random.choice(list(TriggerEventType))
            
            if event_type == TriggerEventType.PROMOTION:
                # Promotion event
                old_position = random.choice(['Senior Manager', 'Manager', 'Senior Specialist'])
                new_position = random.choice(['Director', 'Vice President', 'Senior Director'])
                
                event = {
                    'type': 'promotion',
                    'description': f'Promoted from {old_position} to {new_position}',
                    'date': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                    'impact': 'High',
                    'salary_increase': f"{random.randint(20, 50)}%"
                }
                
            elif event_type == TriggerEventType.RELOCATION:
                # Relocation event
                old_city = random.choice(['Surabaya', 'Bandung', 'Medan', 'Semarang'])
                new_city = location
                
                event = {
                    'type': 'relocation',
                    'description': f'Relocated from {old_city} to {new_city}',
                    'date': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                    'impact': 'High',
                    'relocation_package': f"Rp {random.randint(50, 200)} juta"
                }
                
            elif event_type == TriggerEventType.COMPANY_IPO:
                # Company IPO event
                event = {
                    'type': 'company_ipo',
                    'description': f'Company {company} announced IPO',
                    'date': (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                    'impact': 'Very High',
                    'estimated_value': f"Rp {random.randint(1, 10)} triliun",
                    'stock_options': f"{random.randint(1000, 10000)} shares"
                }
                
            elif event_type == TriggerEventType.COMPANY_FUNDING:
                # Company funding event
                funding_round = random.choice(['Series A', 'Series B', 'Series C', 'Series D'])
                funding_amount = f"Rp {random.randint(100, 1000)} miliar"
                
                event = {
                    'type': 'company_funding',
                    'description': f'Company {company} secured {funding_round} funding of {funding_amount}',
                    'date': (datetime.now() - timedelta(days=random.randint(1, 45))).isoformat(),
                    'impact': 'High',
                    'funding_round': funding_round,
                    'valuation': f"Rp {random.randint(2, 20)} triliun"
                }
            
            trigger_events.append(event)
        
        return trigger_events
    
    def _estimate_net_worth(self, position: str, company: str, experience_years: int, trigger_events: List[Dict[str, Any]]) -> str:
        """Estimate net worth based on position, company, experience, and trigger events"""
        
        base_worth = {
            'CEO': '10-50 Miliar',
            'CTO': '8-40 Miliar',
            'CFO': '5-30 Miliar',
            'COO': '5-25 Miliar',
            'President Director': '3-20 Miliar',
            'Vice President': '2-15 Miliar',
            'Director': '2-10 Miliar',
            'Senior Manager': '1-8 Miliar',
            'Head of': '1-6 Miliar',
            'Chief': '3-25 Miliar',
            'Managing Director': '5-30 Miliar',
            'Executive Director': '3-20 Miliar',
            'Regional Director': '2-15 Miliar'
        }
        
        base_range = base_worth.get(position, '1-5 Miliar')
        
        # Adjust for company prestige
        top_companies = ['Gojek', 'Tokopedia', 'Traveloka', 'Sea Group', 'Grab', 'Microsoft Indonesia', 'Google Indonesia']
        if company in top_companies:
            base_range = self._upgrade_net_worth_range(base_range)
        
        # Adjust for experience
        if experience_years > 15:
            base_range = self._upgrade_net_worth_range(base_range)
        elif experience_years < 10:
            base_range = self._downgrade_net_worth_range(base_range)
        
        # Adjust for trigger events
        for event in trigger_events:
            if event['type'] in ['company_ipo', 'company_funding']:
                base_range = self._upgrade_net_worth_range(base_range)
            elif event['type'] == 'promotion':
                base_range = self._upgrade_net_worth_range(base_range)
        
        return base_range
    
    def _upgrade_net_worth_range(self, current_range: str) -> str:
        """Upgrade net worth range"""
        range_map = {
            '1-5 Miliar': '2-8 Miliar',
            '2-8 Miliar': '3-12 Miliar',
            '3-12 Miliar': '5-20 Miliar',
            '5-20 Miliar': '8-30 Miliar',
            '8-30 Miliar': '10-50 Miliar',
            '10-50 Miliar': '15-75 Miliar'
        }
        return range_map.get(current_range, current_range)
    
    def _downgrade_net_worth_range(self, current_range: str) -> str:
        """Downgrade net worth range"""
        range_map = {
            '15-75 Miliar': '10-50 Miliar',
            '10-50 Miliar': '8-30 Miliar',
            '8-30 Miliar': '5-20 Miliar',
            '5-20 Miliar': '3-12 Miliar',
            '3-12 Miliar': '2-8 Miliar',
            '2-8 Miliar': '1-5 Miliar'
        }
        return range_map.get(current_range, current_range)
    
    def _calculate_purchase_probability(self, trigger_events: List[Dict[str, Any]], net_worth: str) -> int:
        """
        Calculate purchase probability based on trigger events
        RELOCATION + PROMOTION = 90+ score (special case)
        """
        
        base_probability = 30  # Base probability for executives
        
        # Check for special case: RELOCATION + PROMOTION
        has_relocation = any(event['type'] == 'relocation' for event in trigger_events)
        has_promotion = any(event['type'] == 'promotion' for event in trigger_events)
        
        if has_relocation and has_promotion:
            # Special case: RELOCATION + PROMOTION = 90+ score
            base_probability = 90
            # Add bonus for additional events
            if len(trigger_events) > 2:
                base_probability += 5
        else:
            # Regular scoring for other combinations
            for event in trigger_events:
                if event['type'] == 'relocation':
                    base_probability += 25
                elif event['type'] == 'promotion':
                    base_probability += 20
                elif event['type'] == 'company_ipo':
                    base_probability += 30
                elif event['type'] == 'company_funding':
                    base_probability += 25
        
        # Adjust based on net worth
        if '50 Miliar' in net_worth or '75 Miliar' in net_worth:
            base_probability += 10
        elif '30 Miliar' in net_worth or '20 Miliar' in net_worth:
            base_probability += 5
        
        # Multiple events bonus
        if len(trigger_events) >= 2:
            base_probability += 10
        elif len(trigger_events) >= 3:
            base_probability += 15
        
        return min(100, max(0, base_probability))
    
    def integrate_executive_prospects(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate high-net-worth executive prospects into database
        
        Args:
            scan_results: Results from scan_career_trigger_events
            
        Returns:
            Dict containing integration results
        """
        
        high_value_executives = scan_results.get('high_value_executives', [])
        
        if not high_value_executives:
            logger.info("ℹ️ No high-value executives to integrate")
            return {
                'integrated_count': 0,
                'success': True,
                'message': 'No high-value executives found'
            }
        
        logger.info(f"🔄 Integrating {len(high_value_executives)} high-value executives into database...")
        
        integration_results = {
            'integrated_count': 0,
            'failed_count': 0,
            'success': True,
            'integration_details': [],
            'errors': []
        }
        
        for executive in high_value_executives:
            try:
                # Prepare lead data for executive
                lead_data = {
                    'url': executive.linkedin_url,
                    'title': f"LinkedIn Executive: {executive.name} - {executive.current_position}",
                    'content_snippet': f"{executive.current_position} at {executive.company}. Trigger events: {len(executive.trigger_events)}",
                    'score': executive.purchase_probability,
                    'source': 'LinkedIn_Scout',
                    'status': 'hot',  # Executives are always hot leads
                    'lead_type': 'LinkedIn Executive',
                    'location': executive.location,
                    'query_used': f"executive_{executive.company}_{executive.location}",
                    'contact_info': json.dumps({
                        'name': executive.name,
                        'position': executive.current_position,
                        'company': executive.company,
                        'linkedin_url': executive.linkedin_url
                    }),
                    'urgency_score': executive.purchase_probability,
                    'potential_value': executive.net_worth_estimate,
                    'data_quality_score': 95,  # Very high quality from LinkedIn
                    'metadata': json.dumps({
                        'executive_profile': {
                            'name': executive.name,
                            'current_position': executive.current_position,
                            'company': executive.company,
                            'industry': executive.industry,
                            'experience_years': executive.experience_years,
                            'education': executive.education,
                            'location': executive.location,
                            'net_worth_estimate': executive.net_worth_estimate,
                            'purchase_probability': executive.purchase_probability
                        },
                        'trigger_events': executive.trigger_events,
                        'scan_id': scan_results.get('scan_id', ''),
                        'extraction_method': 'linkedin_executive_scout'
                    }),
                    'behavioral_signals': json.dumps({
                        'executive_signals': {
                            'career_advancement': len([e for e in executive.trigger_events if e['type'] == 'promotion']),
                            'relocation_status': len([e for e in executive.trigger_events if e['type'] == 'relocation']),
                            'company_growth': len([e for e in executive.trigger_events if e['type'] in ['company_ipo', 'company_funding']]),
                            'decision_making_power': 'High' if 'Director' in executive.current_position or 'VP' in executive.current_position else 'Medium'
                        },
                        'purchase_indicators': {
                            'trigger_event_count': len(executive.trigger_events),
                            'net_worth_tier': self._classify_net_worth(executive.net_worth_estimate),
                            'career_stability': executive.experience_years,
                            'industry_prestige': self._classify_industry_prestige(executive.industry)
                        }
                    }),
                    'system_info': json.dumps({
                        'agent': self.name,
                        'version': self.version,
                        'processing_time': scan_results.get('duration_seconds', 0),
                        'confidence_score': executive.purchase_probability,
                        'profile_type': 'LinkedIn Executive'
                    })
                }
                
                # Insert into database
                lead_id = self.db_manager.insert_lead(lead_data)
                
                integration_results['integrated_count'] += 1
                integration_results['integration_details'].append({
                    'lead_id': lead_id,
                    'name': executive.name,
                    'position': executive.current_position,
                    'company': executive.company,
                    'net_worth': executive.net_worth_estimate,
                    'purchase_probability': executive.purchase_probability,
                    'trigger_events': len(executive.trigger_events),
                    'status': 'success'
                })
                
                logger.info(f"✅ Integrated executive: {executive.name} ({executive.current_position})")
                logger.info(f"   💼 {executive.company} - 💰 {executive.net_worth_estimate}")
                logger.info(f"   🎯 Purchase Probability: {executive.purchase_probability}%")
                
            except Exception as e:
                integration_results['failed_count'] += 1
                error_msg = f"Failed to integrate executive {executive.name}: {str(e)}"
                integration_results['errors'].append(error_msg)
                logger.error(error_msg)
        
        logger.info(f"🎯 Executive integration completed: {integration_results['integrated_count']} successful, {integration_results['failed_count']} failed")
        
        return integration_results
    
    def _classify_net_worth(self, net_worth: str) -> str:
        """Classify net worth into tiers"""
        if '75 Miliar' in net_worth or '50 Miliar' in net_worth:
            return 'Ultra High Net Worth'
        elif '30 Miliar' in net_worth or '20 Miliar' in net_worth:
            return 'High Net Worth'
        elif '15 Miliar' in net_worth or '10 Miliar' in net_worth:
            return 'Medium-High Net Worth'
        else:
            return 'Medium Net Worth'
    
    def _classify_industry_prestige(self, industry: str) -> str:
        """Classify industry prestige"""
        high_prestige = ['Technology', 'Finance', 'Banking', 'E-commerce', 'Telecommunications']
        medium_prestige = ['Manufacturing', 'Consumer Goods', 'Consulting', 'Healthcare']
        
        if industry in high_prestige:
            return 'High Prestige'
        elif industry in medium_prestige:
            return 'Medium Prestige'
        else:
            return 'Standard'
    
    def run_executive_hunting(self, target_companies: List[str] = None, target_cities: List[str] = None) -> Dict[str, Any]:
        """
        Run complete executive hunting workflow
        
        Args:
            target_companies: List of target companies (optional)
            target_cities: List of target cities (optional)
            
        Returns:
            Dict containing complete analysis results
        """
        
        logger.info("🚀 Starting LinkedIn Executive Hunting workflow...")
        
        # Use defaults if not provided
        if target_companies is None:
            target_companies = self.target_companies[:10]  # Top 10 companies
        if target_cities is None:
            target_cities = self.target_cities[:8]  # Top 8 cities
        
        # Step 1: Scan career trigger events
        scan_results = self.scan_career_trigger_events(target_companies, target_cities)
        
        # Step 2: Integrate executive prospects
        integration_results = self.integrate_executive_prospects(scan_results)
        
        # Step 3: Generate summary report
        summary_report = {
            'workflow_id': f"linkedin_exec_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'target_companies': target_companies,
            'target_cities': target_cities,
            'scan_summary': {
                'total_profiles_scanned': scan_results['statistics']['total_profiles_scanned'],
                'high_net_worth_executives': scan_results['statistics']['high_net_worth_count'],
                'trigger_events_found': scan_results['statistics']['trigger_events_total'],
                'scan_duration': scan_results['duration_seconds']
            },
            'integration_summary': {
                'executives_integrated': integration_results['integrated_count'],
                'integration_success_rate': (integration_results['integrated_count'] / len(scan_results['high_value_executives']) * 100) if scan_results['high_value_executives'] else 0,
                'integration_errors': integration_results['failed_count']
            },
            'top_executives': scan_results['high_value_executives'][:5],  # Top 5 executives
            'trigger_analysis': self._analyze_trigger_distribution(scan_results['trigger_events_found']),
            'company_analysis': self._analyze_company_performance(scan_results['executive_profiles']),
            'recommendations': self._generate_executive_recommendations(scan_results, integration_results),
            'execution_time': scan_results['duration_seconds'],
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("🎉 LinkedIn Executive Hunting workflow completed successfully!")
        logger.info(f"📊 Summary: {summary_report['scan_summary']['total_profiles_scanned']} profiles scanned, {summary_report['integration_summary']['executives_integrated']} executives integrated")
        logger.info(f"💎 High-net-worth executives: {summary_report['scan_summary']['high_net_worth_executives']}")
        
        return summary_report
    
    def _analyze_trigger_distribution(self, trigger_events: Dict[str, int]) -> Dict[str, Any]:
        """Analyze distribution of trigger events"""
        
        total_events = sum(trigger_events.values())
        
        return {
            'distribution': trigger_events,
            'most_common': max(trigger_events.items(), key=lambda x: x[1]) if trigger_events else None,
            'total_events': total_events,
            'event_diversity': len([v for v in trigger_events.values() if v > 0])
        }
    
    def _analyze_company_performance(self, profiles: List[ExecutiveProfile]) -> Dict[str, Any]:
        """Analyze which companies have the most high-value executives"""
        
        company_stats = {}
        
        for profile in profiles:
            company = profile.company
            if company not in company_stats:
                company_stats[company] = {
                    'total_executives': 0,
                    'high_value_count': 0,
                    'avg_purchase_probability': 0,
                    'avg_net_worth': []
                }
            
            company_stats[company]['total_executives'] += 1
            if profile.purchase_probability >= 80:
                company_stats[company]['high_value_count'] += 1
            company_stats[company]['avg_purchase_probability'] += profile.purchase_probability
            company_stats[company]['avg_net_worth'].append(profile.net_worth_estimate)
        
        # Calculate averages
        for company, stats in company_stats.items():
            stats['avg_purchase_probability'] = stats['avg_purchase_probability'] / stats['total_executives']
            # Determine most common net worth range
            net_worth_counts = {}
            for net_worth in stats['avg_net_worth']:
                net_worth_counts[net_worth] = net_worth_counts.get(net_worth, 0) + 1
            stats['most_common_net_worth'] = max(net_worth_counts.items(), key=lambda x: x[1])[0] if net_worth_counts else 'Unknown'
        
        return company_stats
    
    def _generate_executive_recommendations(self, scan_results: Dict, integration_results: Dict) -> List[str]:
        """Generate recommendations based on executive hunting results"""
        
        recommendations = []
        
        # High-value executives recommendation
        if integration_results['integrated_count'] > 10:
            recommendations.append("High volume of executives found - Prepare luxury property portfolio and executive briefing materials")
        elif integration_results['integrated_count'] > 5:
            recommendations.append("Moderate executive volume - Focus on premium property options and personalized outreach")
        
        # Trigger events recommendations
        trigger_events = scan_results['trigger_events_found']
        if trigger_events['relocation'] > 5:
            recommendations.append("Multiple executive relocations detected - Prepare relocation package and area orientation materials")
        
        if trigger_events['promotion'] > 5:
            recommendations.append("Executive promotions surge - Focus on upgrade properties and investment opportunities")
        
        if trigger_events['company_ipo'] > 0 or trigger_events['company_funding'] > 0:
            recommendations.append("Company growth events detected - Target executives with investment property options")
        
        # Company-specific recommendations
        company_analysis = self._analyze_company_performance(scan_results['executive_profiles'])
        if company_analysis:
            top_company = max(company_analysis.items(), key=lambda x: x[1]['high_value_count'])
            recommendations.append(f"Focus on {top_company[0]} - highest concentration of high-value executives ({top_company[1]['high_value_count']})")
        
        # Net worth recommendations
        high_net_worth_count = scan_results['statistics']['high_net_worth_count']
        if high_net_worth_count > 10:
            recommendations.append("Ultra-high net worth executives found - Prepare exclusive luxury property portfolio")
        elif high_net_worth_count > 5:
            recommendations.append("High net worth executives identified - Focus on premium and luxury property segments")
        
        return recommendations


# Convenience functions for external usage
def run_linkedin_executive_hunting(target_companies: List[str] = None, target_cities: List[str] = None) -> Dict[str, Any]:
    """
    Convenience function to run LinkedIn executive hunting
    
    Args:
        target_companies: List of target companies to monitor
        target_cities: List of target cities for relocation monitoring
        
    Returns:
        Dict containing complete executive hunting results
    """
    scout = LinkedInExecScout()
    return scout.run_executive_hunting(target_companies, target_cities)


if __name__ == "__main__":
    # Example usage
    print("🎯 LinkedIn Executive Scout - Example Usage")
    print("=" * 60)
    
    # Define targets
    companies = ['Gojek', 'Tokopedia', 'Traveloka', 'Sea Group']
    cities = ['Jakarta', 'Surabaya', 'Bandung']
    
    print(f"🏢 Target Companies: {companies}")
    print(f"🌍 Target Cities: {cities}")
    print("=" * 60)
    
    # Run executive hunting
    results = run_linkedin_executive_hunting(companies, cities)
    
    print(f"\n📊 Executive Hunting Results:")
    print(f"Total Profiles Scanned: {results['scan_summary']['total_profiles_scanned']}")
    print(f"High-Net-Worth Executives: {results['scan_summary']['high_net_worth_executives']}")
    print(f"Executives Integrated: {results['integration_summary']['executives_integrated']}")
    print(f"Execution Time: {results['execution_time']:.2f} seconds")
    
    print(f"\n👔 Top 3 Executives:")
    for i, executive in enumerate(results['top_executives'][:3], 1):
        print(f"{i}. {executive.name} - {executive.current_position}")
        print(f"   🏢 {executive.company} | 💰 {executive.net_worth_estimate}")
        print(f"   🎯 Purchase Probability: {executive.purchase_probability}%")
        print(f"   ⚡ Trigger Events: {len(executive.trigger_events)}")
    
    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"• {rec}")
    
    print("=" * 60)
    print(f"🏁 LinkedIn Executive Hunting completed successfully!")
    print("=" * 60)

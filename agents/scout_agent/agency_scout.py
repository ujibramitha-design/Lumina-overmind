"""
Agency Scout Module - HUNTER_AGENT_AI_MARKETING_DIGITAL
Comprehensive agency intelligence system untuk market analysis dan competitor tracking
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgencyScout:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agency_database = self._load_agency_database()
        
    def _load_agency_database(self) -> Dict:
        """Load agency database dari config file"""
        try:
            with open('config/agency_marketing_database_fixed.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error("Agency database file not found")
            return {"agency_marketing_database": {}}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing agency database: {e}")
            return {"agency_marketing_database": {}}
    
    def get_agency_by_id(self, agency_id: str) -> Optional[Dict]:
        """Get agency information by ID"""
        try:
            db = self.agency_database["agency_marketing_database"]
            
            for region_name, region_data in db["regions"].items():
                for agency_data in region_data["agencies"]:
                    if agency_data["id"] == agency_id:
                        return agency_data
            
            return None
        except Exception as e:
            self.logger.error(f"Error getting agency {agency_id}: {e}")
            return None
    
    def get_agencies_by_region(self, region: str) -> List[Dict]:
        """Get all agencies in a specific region"""
        try:
            db = self.agency_database["agency_marketing_database"]
            
            if region in db["regions"]:
                return db["regions"][region]["agencies"]
            else:
                return []
        except Exception as e:
            self.logger.error(f"Error getting agencies for region {region}: {e}")
            return []
    
    def get_agencies_by_type(self, agency_type: str) -> List[Dict]:
        """Get agencies by type"""
        try:
            db = self.agency_database["agency_marketing_database"]
            matching_agencies = []
            
            for region_name, region_data in db["regions"].items():
                for agency_data in region_data["agencies"]:
                    if agency_data["type"].lower() == agency_type.lower():
                        agency_data["region"] = region_name
                        matching_agencies.append(agency_data)
            
            return matching_agencies
        except Exception as e:
            self.logger.error(f"Error getting agencies by type {agency_type}: {e}")
            return []
    
    def get_agencies_by_specialization(self, specialization: str) -> List[Dict]:
        """Get agencies by specialization"""
        try:
            db = self.agency_database["agency_marketing_database"]
            matching_agencies = []
            
            for region_name, region_data in db["regions"].items():
                for agency_data in region_data["agencies"]:
                    if "specializations" in agency_data:
                        if specialization.lower() in [s.lower() for s in agency_data["specializations"]]:
                            agency_data["region"] = region_name
                            matching_agencies.append(agency_data)
            
            return matching_agencies
        except Exception as e:
            self.logger.error(f"Error getting agencies by specialization {specialization}: {e}")
            return []
    
    def get_agency_agents_by_region(self, region: str) -> Dict:
        """Get all agents in a specific region"""
        try:
            agencies = self.get_agencies_by_region(region)
            all_agents = []
            
            for agency in agencies:
                if "agents" in agency:
                    for agent in agency["agents"]:
                        agent["agency_name"] = agency["name"]
                        agent["agency_id"] = agency["id"]
                        agent["agency_type"] = agency["type"]
                        agent["agency_reputation"] = agency.get("reputation", "Unknown")
                        all_agents.append(agent)
            
            return {
                "region": region,
                "total_agencies": len(agencies),
                "total_agents": len(all_agents),
                "agents": all_agents
            }
        except Exception as e:
            self.logger.error(f"Error getting agents for region {region}: {e}")
            return {}
    
    def get_premium_agencies(self) -> List[Dict]:
        """Get premium agencies (Excellent and Very Good reputation)"""
        try:
            db = self.agency_database["agency_marketing_database"]
            premium_agencies = []
            
            for region_name, region_data in db["regions"].items():
                for agency_data in region_data["agencies"]:
                    reputation = agency_data.get("reputation", "").lower()
                    if reputation in ["excellent", "very good"]:
                        agency_data["region"] = region_name
                        premium_agencies.append(agency_data)
            
            return premium_agencies
        except Exception as e:
            self.logger.error(f"Error getting premium agencies: {e}")
            return []
    
    def get_digital_marketing_agencies(self) -> List[Dict]:
        """Get digital marketing agencies"""
        return self.get_agencies_by_type("Digital Marketing Agency")
    
    def get_national_franchises(self) -> List[Dict]:
        """Get national franchise agencies"""
        return self.get_agencies_by_type("National Franchise")
    
    def get_independent_agencies(self) -> List[Dict]:
        """Get independent agencies"""
        return self.get_agencies_by_type("Independent")
    
    def search_agencies(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search agencies with filters"""
        try:
            results = []
            db = self.agency_database["agency_marketing_database"]
            
            # Default filters
            if filters is None:
                filters = {}
            
            region_filter = filters.get("region")
            type_filter = filters.get("type")
            specialization_filter = filters.get("specialization")
            reputation_filter = filters.get("reputation")
            
            for region_name, region_data in db["regions"].items():
                if region_filter and region_name != region_filter:
                    continue
                
                for agency_data in region_data["agencies"]:
                    # Search in agency name and type
                    if query.lower() in agency_data["name"].lower() or \
                       query.lower() in agency_data["type"].lower():
                        
                        # Apply filters
                        if type_filter and agency_data["type"].lower() != type_filter.lower():
                            continue
                        
                        if specialization_filter and "specializations" in agency_data:
                            if specialization_filter.lower() not in [s.lower() for s in agency_data["specializations"]]:
                                continue
                        
                        if reputation_filter and agency_data.get("reputation", "").lower() != reputation_filter.lower():
                            continue
                        
                        agency_data["region"] = region_name
                        results.append(agency_data)
            
            return results
        except Exception as e:
            self.logger.error(f"Error searching agencies: {e}")
            return []
    
    def get_agency_market_analysis(self) -> Dict:
        """Generate comprehensive agency market analysis"""
        try:
            db = self.agency_database["agency_marketing_database"]
            market_stats = db["market_statistics"]
            
            analysis = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "report_type": "Agency Market Intelligence Report",
                    "data_source": "Agency Marketing Database",
                    "total_agencies_analyzed": db["total_agencies"]
                },
                "executive_summary": {
                    "total_agencies": db["total_agencies"],
                    "total_agents": market_stats["total_agents"],
                    "market_coverage": market_stats["market_coverage"],
                    "agency_types": market_stats["agency_types"],
                    "reputation_distribution": market_stats["reputation_distribution"]
                },
                "regional_analysis": self._analyze_regional_agency_performance(db),
                "agency_type_analysis": self._analyze_agency_types(db),
                "specialization_analysis": self._analyze_specializations(market_stats),
                "reputation_analysis": self._analyze_reputation_distribution(market_stats),
                "contact_analysis": self._analyze_contact_methods(market_stats),
                "services_analysis": self._analyze_services_offered(market_stats),
                "strategic_insights": self._generate_agency_strategic_insights(db, market_stats)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error generating agency market analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_regional_agency_performance(self, db: Dict) -> Dict:
        """Analyze agency performance by region"""
        regional_analysis = {}
        
        for region_name, region_data in db["regions"].items():
            agencies = region_data["agencies"]
            
            # Calculate regional metrics
            total_agents = sum(len(agency.get("agents", [])) for agency in agencies)
            premium_agencies = len([a for a in agencies if a.get("reputation", "").lower() in ["excellent", "very good"]])
            digital_agencies = len([a for a in agencies if "digital" in a["type"].lower()])
            
            # Agency type distribution
            type_distribution = {}
            for agency in agencies:
                agency_type = agency["type"]
                type_distribution[agency_type] = type_distribution.get(agency_type, 0) + 1
            
            # Specialization distribution
            specialization_distribution = {}
            for agency in agencies:
                if "specializations" in agency:
                    for spec in agency["specializations"]:
                        specialization_distribution[spec] = specialization_distribution.get(spec, 0) + 1
            
            regional_analysis[region_name] = {
                "total_agencies": len(agencies),
                "total_agents": total_agents,
                "market_value_idr": region_data["market_value_idr"],
                "premium_agencies": premium_agencies,
                "digital_agencies": digital_agencies,
                "type_distribution": type_distribution,
                "specialization_distribution": specialization_distribution,
                "top_agencies": self._get_top_agencies_by_region(agencies)
            }
        
        return regional_analysis
    
    def _get_top_agencies_by_region(self, agencies: List[Dict]) -> List[Dict]:
        """Get top agencies by reputation for a region"""
        # Sort by reputation and establishment year
        reputation_order = {"excellent": 4, "very good": 3, "good": 2, "fair": 1}
        
        def agency_score(agency):
            reputation_score = reputation_order.get(agency.get("reputation", "fair").lower(), 1)
            experience_score = min(agency.get("established_year", 2020), 2020) - 2000  # Years since 2000
            return reputation_score * 10 + experience_score
        
        sorted_agencies = sorted(agencies, key=agency_score, reverse=True)
        
        return sorted_agencies[:5]  # Top 5 per region
    
    def _analyze_agency_types(self, db: Dict) -> Dict:
        """Analyze agency types distribution"""
        type_analysis = {}
        
        for region_name, region_data in db["regions"].items():
            agencies = region_data["agencies"]
            
            for agency in agencies:
                agency_type = agency["type"]
                
                if agency_type not in type_analysis:
                    type_analysis[agency_type] = {
                        "total_agencies": 0,
                        "regions": [],
                        "total_agents": 0,
                        "average_reputation": 0,
                        "notable_agencies": []
                    }
                
                type_analysis[agency_type]["total_agencies"] += 1
                if region_name not in type_analysis[agency_type]["regions"]:
                    type_analysis[agency_type]["regions"].append(region_name)
                
                type_analysis[agency_type]["total_agents"] += len(agency.get("agents", []))
                
                # Add notable agencies (Excellent reputation)
                if agency.get("reputation", "").lower() == "excellent":
                    type_analysis[agency_type]["notable_agencies"].append({
                        "name": agency["name"],
                        "region": region_name,
                        "established": agency.get("established_year", "Unknown")
                    })
        
        return type_analysis
    
    def _analyze_specializations(self, market_stats: Dict) -> Dict:
        """Analyze specializations distribution"""
        specializations = market_stats["specializations"]
        
        # Group specializations by category
        categories = {
            "residential": ["rumah_komersil", "rumah_menengah", "rumah_premium", "apartemen"],
            "commercial": ["ruko", "tanah"],
            "financing": ["kpr", "subsidy"],
            "marketing": ["digital_marketing", "professional_networking"]
        }
        
        categorized = {}
        for category, specs in categories.items():
            categorized[category] = {
                "total_agencies": sum(specializations.get(spec, 0) for spec in specs),
                "specializations": {}
            }
            
            for spec in specs:
                if spec in specializations:
                    categorized[category]["specializations"][spec] = specializations[spec]
        
        return categorized
    
    def _analyze_reputation_distribution(self, market_stats: Dict) -> Dict:
        """Analyze reputation distribution"""
        reputation_dist = market_stats["reputation_distribution"]
        
        total = sum(reputation_dist.values())
        
        return {
            "total_agencies": total,
            "distribution": reputation_dist,
            "percentages": {
                rep: round((count / total) * 100, 1) 
                for rep, count in reputation_dist.items()
            },
            "quality_score": self._calculate_quality_score(reputation_dist)
        }
    
    def _calculate_quality_score(self, reputation_dist: Dict) -> float:
        """Calculate overall quality score based on reputation"""
        weights = {"excellent": 4, "very good": 3, "good": 2, "fair": 1}
        total_weighted = sum(weights.get(rep, 1) * count for rep, count in reputation_dist.items())
        total_count = sum(reputation_dist.values())
        
        return round(total_weighted / total_count, 2) if total_count > 0 else 0
    
    def _analyze_contact_methods(self, market_stats: Dict) -> Dict:
        """Analyze contact methods distribution"""
        contact_methods = market_stats["contact_methods"]
        
        return {
            "availability": contact_methods,
            "coverage_percentage": {
                method: round((count / 50) * 100, 1) 
                for method, count in contact_methods.items()
            },
            "digital_presence": {
                "website": contact_methods.get("website", 0),
                "social_media": contact_methods.get("social_media", 0),
                "total_digital": contact_methods.get("website", 0) + contact_methods.get("social_media", 0)
            }
        }
    
    def _analyze_services_offered(self, market_stats: Dict) -> Dict:
        """Analyze services offered by agencies"""
        services = market_stats["services_offered"]
        
        # Group services by category
        categories = {
            "core_services": ["Penjualan Properti", "Konsultasi Properti", "Pemasaran Digital", "KPR dan Financing"],
            "advanced_services": ["Franchise Opportunities", "Professional Networking", "Digital Marketing"],
            "support_services": ["Legal Documentation", "Appraisal Service", "Property Management"]
        }
        
        categorized = {}
        for category, service_list in categories.items():
            categorized[category] = {
                "services": [],
                "coverage": 0
            }
            
            for service in services:
                if service in service_list:
                    categorized[category]["services"].append(service)
                    # Estimate coverage based on service importance
                    if service in ["Penjualan Properti", "Konsultasi Properti"]:
                        categorized[category]["coverage"] = 50  # All agencies
                    elif service in ["Pemasaran Digital", "KPR dan Financing"]:
                        categorized[category]["coverage"] = 25  # Half of agencies
                    else:
                        categorized[category]["coverage"] = 10  # Some agencies
        
        return categorized
    
    def _generate_agency_strategic_insights(self, db: Dict, market_stats: Dict) -> List[str]:
        """Generate strategic insights for agency market"""
        insights = []
        
        # Market concentration insights
        total_agencies = db["total_agencies"]
        if total_agencies > 40:
            insights.append("High market concentration with 50+ agencies indicates competitive landscape")
        
        # Digital transformation insights
        digital_agencies = market_stats["agency_types"].get("digital_marketing", 0)
        if digital_agencies > 5:
            insights.append(f"Growing digital marketing presence with {digital_agencies} specialized agencies")
        
        # Quality insights
        quality_score = self._calculate_quality_score(market_stats["reputation_distribution"])
        if quality_score > 2.5:
            insights.append("High market quality with strong reputation distribution")
        elif quality_score < 2.0:
            insights.append("Market quality improvement opportunities exist")
        
        # Regional insights
        regions = db["regions"]
        if len(regions) >= 3:
            insights.append("Complete regional coverage across Kota Serang, Kabupaten Serang, and Kota Cilegon")
        
        # Specialization insights
        specializations = market_stats["specializations"]
        if specializations.get("rumah_komersil", 0) > 40:
            insights.append("Strong focus on commercial residential properties")
        
        if specializations.get("digital_marketing", 0) > 5:
            insights.append("Digital marketing specialization indicates modern market approach")
        
        # Contact method insights
        contact_methods = market_stats["contact_methods"]
        digital_presence = contact_methods.get("website", 0) + contact_methods.get("social_media", 0)
        if digital_presence > 30:
            insights.append("Strong digital presence with 60%+ agencies having online profiles")
        
        return insights
    
    def get_agency_intelligence_report(self, agency_id: str) -> Dict:
        """Generate comprehensive intelligence report for a specific agency"""
        try:
            agency_data = self.get_agency_by_id(agency_id)
            if not agency_data:
                return {"error": "Agency not found"}
            
            # Calculate metrics
            total_agents = len(agency_data.get("agents", []))
            agent_experience_avg = sum(agent.get("experience_years", 0) for agent in agency_data.get("agents", [])) / total_agents if total_agents > 0 else 0
            
            # Contact methods analysis
            contact_methods = []
            if agency_data.get("contact", {}).get("phone"):
                contact_methods.append("phone")
            if agency_data.get("contact", {}).get("email"):
                contact_methods.append("email")
            if agency_data.get("contact", {}).get("website"):
                contact_methods.append("website")
            if agency_data.get("contact", {}).get("social_media"):
                contact_methods.append("social_media")
            
            report = {
                "agency_id": agency_id,
                "basic_info": {
                    "name": agency_data["name"],
                    "type": agency_data["type"],
                    "contact": agency_data["contact"],
                    "established_year": agency_data.get("established_year", "Unknown"),
                    "reputation": agency_data.get("reputation", "Unknown"),
                    "market_position": agency_data.get("market_position", "Unknown")
                },
                "agent_analysis": {
                    "total_agents": total_agents,
                    "average_experience_years": round(agent_experience_avg, 1),
                    "featured_agents": [agent for agent in agency_data.get("agents", []) if agent.get("featured")],
                    "specializations": list(set(agent.get("specialization", "") for agent in agency_data.get("agents", [])))
                },
                "services_analysis": {
                    "total_services": len(agency_data.get("services", [])),
                    "services_offered": agency_data.get("services", []),
                    "contact_methods": contact_methods,
                    "digital_presence": len([m for m in contact_methods if m in ["website", "social_media"]])
                },
                "market_intelligence": {
                    "specializations": agency_data.get("specializations", []),
                    "coverage_areas": agency_data.get("coverage_areas", []),
                    "achievements": agency_data.get("achievements", []),
                    "market_strength": self._calculate_agency_market_strength(agency_data)
                }
            }
            
            return report
        except Exception as e:
            self.logger.error(f"Error generating intelligence report for {agency_id}: {e}")
            return {"error": str(e)}
    
    def _calculate_agency_market_strength(self, agency_data: Dict) -> str:
        """Calculate market strength based on agency data"""
        reputation = agency_data.get("reputation", "").lower()
        established_year = agency_data.get("established_year", 2020)
        total_agents = len(agency_data.get("agents", []))
        
        # Calculate strength score
        score = 0
        
        # Reputation score
        reputation_scores = {"excellent": 4, "very good": 3, "good": 2, "fair": 1}
        score += reputation_scores.get(reputation, 1)
        
        # Experience score
        experience_years = 2020 - established_year
        if experience_years > 10:
            score += 3
        elif experience_years > 5:
            score += 2
        elif experience_years > 2:
            score += 1
        
        # Team size score
        if total_agents > 10:
            score += 3
        elif total_agents > 5:
            score += 2
        elif total_agents > 2:
            score += 1
        
        # Determine strength
        if score >= 8:
            return "Very Strong"
        elif score >= 6:
            return "Strong"
        elif score >= 4:
            return "Moderate"
        else:
            return "Weak"
    
    def export_agency_database_to_csv(self) -> str:
        """Export agency database to CSV format"""
        try:
            db = self.agency_database["agency_marketing_database"]
            csv_lines = []
            
            # CSV Header
            csv_lines.append("Region,Agency_ID,Agency_Name,Type,Phone,Email,Website,Established_Year,Reputation,Market_Position,Total_Agents,Services")
            
            # Data rows
            for region_name, region_data in db["regions"].items():
                for agency_data in region_data["agencies"]:
                    contact = agency_data.get("contact", {})
                    total_agents = len(agency_data.get("agents", []))
                    services = "; ".join(agency_data.get("services", []))
                    
                    csv_lines.append(f"{region_name},{agency_data['id']},{agency_data['name']},{agency_data['type']},{contact.get('phone', '')},{contact.get('email', '')},{contact.get('website', '')},{agency_data.get('established_year', '')},{agency_data.get('reputation', '')},{agency_data.get('market_position', '')},{total_agents},{services}")
            
            return "\n".join(csv_lines)
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            return ""
    
    def save_agency_intelligence_report(self, report: Dict) -> str:
        """Save agency intelligence report to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/agency_intelligence_report_{timestamp}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Write markdown report
                f.write("# AGENCY INTELLIGENCE REPORT\n\n")
                f.write(f"Generated: {report['report_metadata']['generated_at']}\n\n")
                
                f.write("## EXECUTIVE SUMMARY\n\n")
                summary = report['executive_summary']
                f.write(f"- Total Agencies: {summary['total_agencies']}\n")
                f.write(f"- Total Agents: {summary['total_agents']}\n")
                f.write(f"- Market Coverage: {summary['market_coverage']}\n")
                f.write(f"- Agency Types: {len(summary['agency_types'])}\n\n")
                
                f.write("## REGIONAL ANALYSIS\n\n")
                for region, data in report['regional_analysis'].items():
                    f.write(f"### {region.title()}\n")
                    f.write(f"- Total Agencies: {data['total_agencies']}\n")
                    f.write(f"- Total Agents: {data['total_agents']}\n")
                    f.write(f"- Market Value: IDR {data['market_value_idr']:,}\n")
                    f.write(f"- Premium Agencies: {data['premium_agencies']}\n")
                    f.write(f"- Digital Agencies: {data['digital_agencies']}\n\n")
                
                f.write("## STRATEGIC INSIGHTS\n\n")
                for i, insight in enumerate(report['strategic_insights'], 1):
                    f.write(f"{i}. {insight}\n")
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving agency intelligence report: {e}")
            return ""

# Global instance for easy access
agency_scout = AgencyScout()

"""
Property Intelligence Scout Module - HUNTER_AGENT_AI_MARKETING_DIGITAL
Advanced property intelligence system dengan market analysis dan competitor tracking
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PropertyIntelligenceScout:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.property_database = self._load_property_database()
        
    def _load_property_database(self) -> Dict:
        """Load property database dari config file"""
        try:
            with open('config/banten_property_database.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error("Property database file not found")
            return {"property_database": {}}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing property database: {e}")
            return {"property_database": {}}
    
    def generate_property_market_report(self) -> Dict:
        """Generate comprehensive property market report"""
        try:
            db = self.property_database["property_database"]
            market_stats = db["market_statistics"]
            
            report = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "report_type": "Property Market Intelligence Report",
                    "data_source": "Banten Property Database",
                    "total_properties_analyzed": db["total_properties"]
                },
                "executive_summary": {
                    "total_market_value_idr": db["market_value_idr"],
                    "total_units": market_stats["total_units_all_regions"],
                    "available_units": market_stats["available_units"],
                    "sold_units": market_stats["sold_units"],
                    "overall_sales_rate": round(market_stats["sold_units"] / market_stats["total_units_all_regions"] * 100, 2),
                    "average_price_idr": market_stats["average_price_idr"]
                },
                "regional_analysis": self._analyze_regional_performance(db),
                "market_segment_analysis": self._analyze_market_segments(market_stats),
                "price_analysis": self._analyze_price_distribution(market_stats),
                "competitor_analysis": self._analyze_competitor_performance(db),
                "availability_analysis": self._analyze_unit_availability(db),
                "market_trends": self._identify_market_trends(market_stats),
                "strategic_recommendations": self._generate_strategic_recommendations(db, market_stats)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating property market report: {e}")
            return {"error": str(e)}
    
    def _analyze_regional_performance(self, db: Dict) -> Dict:
        """Analyze performance by region"""
        regional_analysis = {}
        
        for region_name, region_data in db["regions"].items():
            # Calculate regional metrics
            total_units = 0
            sold_units = 0
            available_units = 0
            total_value = 0
            
            for property_data in region_data["properties"]:
                for unit_type in property_data["type_units"]:
                    total_units += unit_type["total_units"]
                    sold_units += unit_type["sold_units"]
                    available_units += unit_type["available_units"]
                    total_value += unit_type["price_idr"] * unit_type["total_units"]
            
            sales_rate = (sold_units / total_units * 100) if total_units > 0 else 0
            availability_rate = (available_units / total_units * 100) if total_units > 0 else 0
            
            regional_analysis[region_name] = {
                "total_properties": region_data["total_properties"],
                "market_value_idr": region_data["market_value_idr"],
                "total_units": total_units,
                "sold_units": sold_units,
                "available_units": available_units,
                "sales_rate": round(sales_rate, 2),
                "availability_rate": round(availability_rate, 2),
                "total_revenue_idr": total_value,
                "average_price_per_unit": round(total_value / total_units) if total_units > 0 else 0,
                "performance_rating": self._calculate_performance_rating(sales_rate, availability_rate)
            }
        
        return regional_analysis
    
    def _analyze_market_segments(self, market_stats: Dict) -> Dict:
        """Analyze performance by market segment"""
        segment_analysis = {}
        
        for segment, data in market_stats["market_segments"].items():
            sales_rate = (data["sold_units"] / data["total_units"] * 100) if data["total_units"] > 0 else 0
            availability_rate = (data["available_units"] / data["total_units"] * 100) if data["total_units"] > 0 else 0
            
            segment_analysis[segment] = {
                "total_units": data["total_units"],
                "sold_units": data["sold_units"],
                "available_units": data["available_units"],
                "sales_rate": round(sales_rate, 2),
                "availability_rate": round(availability_rate, 2),
                "average_price_idr": data["average_price_idr"],
                "market_share": round(data["total_units"] / market_stats["total_units_all_regions"] * 100, 2),
                "revenue_idr": data["average_price_idr"] * data["sold_units"],
                "segment_health": self._calculate_segment_health(sales_rate, availability_rate)
            }
        
        return segment_analysis
    
    def _analyze_price_distribution(self, market_stats: Dict) -> Dict:
        """Analyze price distribution"""
        price_range = market_stats["price_range_idr"]
        avg_price = market_stats["average_price_idr"]
        
        return {
            "minimum_price_idr": price_range["min"],
            "maximum_price_idr": price_range["max"],
            "average_price_idr": avg_price,
            "price_range_idr": price_range["max"] - price_range["min"],
            "price_categories": {
                "budget": {"max": 300000000, "description": "Under 300M IDR"},
                "menengah": {"min": 300000000, "max": 800000000, "description": "300M - 800M IDR"},
                "menengah_atas": {"min": 800000000, "max": 1500000000, "description": "800M - 1.5B IDR"},
                "premium": {"min": 1500000000, "max": 3000000000, "description": "1.5B - 3B IDR"},
                "luxury": {"min": 3000000000, "description": "Above 3B IDR"}
            },
            "market_positioning": self._analyze_market_positioning(avg_price)
        }
    
    def _analyze_competitor_performance(self, db: Dict) -> Dict:
        """Analyze competitor performance"""
        top_properties = db["market_statistics"]["top_properties_by_sales"]
        competitor_analysis = {}
        
        for i, prop in enumerate(top_properties, 1):
            competitor_analysis[f"rank_{i}"] = {
                "property_name": prop["name"],
                "total_sold": prop["total_sold"],
                "revenue_idr": prop["revenue_idr"],
                "market_share": round(prop["total_sold"] / db["market_statistics"]["total_units_all_regions"] * 100, 2),
                "performance_grade": self._calculate_performance_grade(i, len(top_properties))
            }
        
        return competitor_analysis
    
    def _analyze_unit_availability(self, db: Dict) -> Dict:
        """Analyze unit availability across all properties"""
        availability_summary = {
            "total_available_units": 0,
            "total_units": 0,
            "availability_by_region": {},
            "high_demand_properties": [],
            "low_demand_properties": [],
            "availability_trends": {}
        }
        
        for region_name, region_data in db["regions"].items():
            region_available = 0
            region_total = 0
            
            for property_data in region_data["properties"]:
                prop_available = sum(unit["available_units"] for unit in property_data["type_units"])
                prop_total = sum(unit["total_units"] for unit in property_data["type_units"])
                prop_sold = sum(unit["sold_units"] for unit in property_data["type_units"])
                
                availability_rate = (prop_available / prop_total * 100) if prop_total > 0 else 0
                
                region_available += prop_available
                region_total += prop_total
                availability_summary["total_available_units"] += prop_available
                availability_summary["total_units"] += prop_total
                
                # Categorize by demand
                if availability_rate < 20:
                    availability_summary["high_demand_properties"].append({
                        "name": property_data["name"],
                        "region": region_name,
                        "availability_rate": round(availability_rate, 2),
                        "sold_units": prop_sold,
                        "available_units": prop_available
                    })
                elif availability_rate > 80:
                    availability_summary["low_demand_properties"].append({
                        "name": property_data["name"],
                        "region": region_name,
                        "availability_rate": round(availability_rate, 2),
                        "sold_units": prop_sold,
                        "available_units": prop_available
                    })
            
            region_availability_rate = (region_available / region_total * 100) if region_total > 0 else 0
            availability_summary["availability_by_region"][region_name] = {
                "available_units": region_available,
                "total_units": region_total,
                "availability_rate": round(region_availability_rate, 2)
            }
        
        # Overall availability rate
        overall_availability_rate = (availability_summary["total_available_units"] / availability_summary["total_units"] * 100) if availability_summary["total_units"] > 0 else 0
        availability_summary["overall_availability_rate"] = round(overall_availability_rate, 2)
        
        return availability_summary
    
    def _identify_market_trends(self, market_stats: Dict) -> Dict:
        """Identify current market trends"""
        overall_sales_rate = market_stats["sold_units"] / market_stats["total_units_all_regions"] * 100
        
        trends = {
            "market_health": self._assess_market_health(overall_sales_rate),
            "demand_trend": self._assess_demand_trend(market_stats),
            "price_trend": self._assess_price_trend(market_stats),
            "segment_trends": self._assess_segment_trends(market_stats["market_segments"]),
            "regional_trends": self._assess_regional_trends(market_stats),
            "forecast": self._generate_market_forecast(market_stats)
        }
        
        return trends
    
    def _generate_strategic_recommendations(self, db: Dict, market_stats: Dict) -> List[str]:
        """Generate strategic recommendations based on market analysis"""
        recommendations = []
        
        overall_sales_rate = market_stats["sold_units"] / market_stats["total_units_all_regions"] * 100
        
        # Market health recommendations
        if overall_sales_rate > 85:
            recommendations.append("Market is very strong - consider accelerating development pace")
        elif overall_sales_rate < 60:
            recommendations.append("Market needs stimulation - consider pricing adjustments or marketing campaigns")
        
        # Segment recommendations
        for segment, data in market_stats["market_segments"].items():
            segment_sales_rate = data["sold_units"] / data["total_units"] * 100
            
            if segment_sales_rate > 90:
                recommendations.append(f"{segment.title()} segment is performing excellently - increase supply in this segment")
            elif segment_sales_rate < 50:
                recommendations.append(f"{segment.title()} segment needs attention - review pricing or marketing strategy")
        
        # Availability recommendations
        if market_stats["available_units"] < market_stats["total_units_all_regions"] * 0.2:
            recommendations.append("Low availability indicates high demand - consider new launches or price adjustments")
        elif market_stats["available_units"] > market_stats["total_units_all_units"] * 0.6:
            recommendations.append("High availability may indicate oversupply - adjust pricing or marketing efforts")
        
        # Regional recommendations
        for region_name, region_data in db["regions"].items():
            region_units = sum(sum(unit["total_units"] for unit in prop["type_units"]) for prop in region_data["properties"])
            region_sold = sum(sum(unit["sold_units"] for unit in prop["type_units"]) for prop in region_data["properties"])
            region_sales_rate = (region_sold / region_units * 100) if region_units > 0 else 0
            
            if region_sales_rate > 90:
                recommendations.append(f"{region_name.title()} shows exceptional performance - expand presence in this region")
            elif region_sales_rate < 50:
                recommendations.append(f"{region_name.title()} needs strategic intervention - review local market conditions")
        
        return recommendations
    
    def _calculate_performance_rating(self, sales_rate: float, availability_rate: float) -> str:
        """Calculate performance rating based on sales and availability"""
        if sales_rate > 80 and availability_rate < 30:
            return "Excellent"
        elif sales_rate > 60 and availability_rate < 50:
            return "Good"
        elif sales_rate > 40 and availability_rate < 70:
            return "Average"
        else:
            return "Needs Improvement"
    
    def _calculate_segment_health(self, sales_rate: float, availability_rate: float) -> str:
        """Calculate segment health"""
        if sales_rate > 85 and availability_rate < 25:
            return "Very Healthy"
        elif sales_rate > 70 and availability_rate < 45:
            return "Healthy"
        elif sales_rate > 50 and availability_rate < 65:
            return "Moderate"
        else:
            return "Needs Attention"
    
    def _calculate_performance_grade(self, rank: int, total_properties: int) -> str:
        """Calculate performance grade based on ranking"""
        if rank <= total_properties * 0.25:
            return "A+"
        elif rank <= total_properties * 0.5:
            return "A"
        elif rank <= total_properties * 0.75:
            return "B"
        else:
            return "C"
    
    def _analyze_market_positioning(self, avg_price: int) -> str:
        """Analyze market positioning based on average price"""
        if avg_price < 300000000:
            return "Budget-Focused"
        elif avg_price < 800000000:
            return "Mass Market"
        elif avg_price < 1500000000:
            return "Mid-Market"
        elif avg_price < 3000000000:
            return "Premium"
        else:
            return "Luxury"
    
    def _assess_market_health(self, sales_rate: float) -> str:
        """Assess overall market health"""
        if sales_rate > 85:
            return "Very Strong"
        elif sales_rate > 70:
            return "Strong"
        elif sales_rate > 55:
            return "Moderate"
        else:
            return "Weak"
    
    def _assess_demand_trend(self, market_stats: Dict) -> str:
        """Assess demand trend"""
        availability_rate = market_stats["available_units"] / market_stats["total_units_all_regions"]
        
        if availability_rate < 0.2:
            return "Very High Demand"
        elif availability_rate < 0.4:
            return "High Demand"
        elif availability_rate < 0.6:
            return "Moderate Demand"
        else:
            return "Low Demand"
    
    def _assess_price_trend(self, market_stats: Dict) -> str:
        """Assess price trend"""
        avg_price = market_stats["average_price_idr"]
        
        # This would ideally use historical data, but for now we'll use segment distribution
        premium_units = market_stats["market_segments"]["premium"]["total_units"]
        total_units = market_stats["total_units_all_regions"]
        premium_ratio = premium_units / total_units
        
        if premium_ratio > 0.3:
            return "Upward Trend"
        elif premium_ratio > 0.2:
            return "Stable"
        else:
            return "Downward Pressure"
    
    def _assess_segment_trends(self, segments: Dict) -> Dict:
        """Assess trends by segment"""
        trends = {}
        
        for segment, data in segments.items():
            sales_rate = data["sold_units"] / data["total_units"] * 100
            
            if sales_rate > 80:
                trends[segment] = "Strong Growth"
            elif sales_rate > 60:
                trends[segment] = "Steady Growth"
            elif sales_rate > 40:
                trends[segment] = "Slow Growth"
            else:
                trends[segment] = "Declining"
        
        return trends
    
    def _assess_regional_trends(self, market_stats: Dict) -> Dict:
        """Assess trends by region"""
        # This would ideally use regional data
        return {
            "kota_serang": "Steady Growth",
            "kabupaten_serang": "High Growth",
            "kota_cilegon": "Moderate Growth"
        }
    
    def _generate_market_forecast(self, market_stats: Dict) -> Dict:
        """Generate market forecast"""
        current_sales_rate = market_stats["sold_units"] / market_stats["total_units_all_units"] * 100
        
        forecast = {
            "next_quarter": {
                "expected_sales_rate": min(95, current_sales_rate + 5),
                "confidence": "Medium"
            },
            "next_semester": {
                "expected_sales_rate": min(90, current_sales_rate + 10),
                "confidence": "Low"
            },
            "next_year": {
                "expected_sales_rate": min(85, current_sales_rate + 15),
                "confidence": "Low"
            }
        }
        
        return forecast
    
    def export_property_database_to_csv(self) -> str:
        """Export property database to CSV format"""
        try:
            db = self.property_database["property_database"]
            csv_lines = []
            
            # CSV Header
            csv_lines.append("Region,Property_ID,Property_Name,Developer,Location,Type,Price_IDR,Land_Area,Building_Area,Bedrooms,Bathrooms,Available_Units,Sold_Units,Total_Units,Status,Market_Position")
            
            # Data rows
            for region_name, region_data in db["regions"].items():
                for property_data in region_data["properties"]:
                    for unit_type in property_data["type_units"]:
                        csv_lines.append(f"{region_name},{property_data['id']},{property_data['name']},{property_data['developer']},{property_data['location']},{unit_type['type']},{unit_type['price_idr']},{unit_type['land_area']},{unit_type['building_area']},{unit_type['bedrooms']},{unit_type['bathrooms']},{unit_type['available_units']},{unit_type['sold_units']},{unit_type['total_units']},{unit_type['status']},{property_data['market_position']}")
            
            return "\n".join(csv_lines)
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            return ""
    
    def save_property_intelligence_report(self, report: Dict) -> str:
        """Save property intelligence report to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/property_intelligence_report_{timestamp}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Write markdown report
                f.write("# PROPERTY INTELLIGENCE REPORT\n\n")
                f.write(f"Generated: {report['report_metadata']['generated_at']}\n\n")
                
                f.write("## EXECUTIVE SUMMARY\n\n")
                summary = report['executive_summary']
                f.write(f"- Total Market Value: IDR {summary['total_market_value_idr']:,}\n")
                f.write(f"- Total Units: {summary['total_units']}\n")
                f.write(f"- Sold Units: {summary['sold_units']}\n")
                f.write(f"- Available Units: {summary['available_units']}\n")
                f.write(f"- Overall Sales Rate: {summary['overall_sales_rate']}%\n")
                f.write(f"- Average Price: IDR {summary['average_price_idr']:,}\n\n")
                
                f.write("## REGIONAL ANALYSIS\n\n")
                for region, data in report['regional_analysis'].items():
                    f.write(f"### {region.title()}\n")
                    f.write(f"- Total Properties: {data['total_properties']}\n")
                    f.write(f"- Market Value: IDR {data['market_value_idr']:,}\n")
                    f.write(f"- Sales Rate: {data['sales_rate']}%\n")
                    f.write(f"- Availability Rate: {data['availability_rate']}%\n")
                    f.write(f"- Performance Rating: {data['performance_rating']}\n\n")
                
                f.write("## STRATEGIC RECOMMENDATIONS\n\n")
                for i, rec in enumerate(report['strategic_recommendations'], 1):
                    f.write(f"{i}. {rec}\n")
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving property intelligence report: {e}")
            return ""

# Global instance for easy access
property_intelligence_scout = PropertyIntelligenceScout()

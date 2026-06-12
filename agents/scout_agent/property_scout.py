"""
Property Scout Module - HUNTER_AGENT_AI_MARKETING_DIGITAL
Comprehensive property intelligence untuk market analysis dan competitor tracking
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PropertyScout:
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
    
    def get_property_by_id(self, property_id: str) -> Optional[Dict]:
        """Get property information by ID"""
        try:
            db = self.property_database["property_database"]
            
            for region_name, region_data in db["regions"].items():
                for property_data in region_data["properties"]:
                    if property_data["id"] == property_id:
                        return property_data
            
            return None
        except Exception as e:
            self.logger.error(f"Error getting property {property_id}: {e}")
            return None
    
    def get_properties_by_region(self, region: str) -> List[Dict]:
        """Get all properties in a specific region"""
        try:
            db = self.property_database["property_database"]
            
            if region in db["regions"]:
                return db["regions"][region]["properties"]
            else:
                return []
        except Exception as e:
            self.logger.error(f"Error getting properties for region {region}: {e}")
            return []
    
    def get_properties_by_price_range(self, min_price: int, max_price: int) -> List[Dict]:
        """Get properties within specific price range"""
        try:
            matching_properties = []
            db = self.property_database["property_database"]
            
            for region_name, region_data in db["regions"].items():
                for property_data in region_data["properties"]:
                    for unit_type in property_data["type_units"]:
                        if min_price <= unit_type["price_idr"] <= max_price:
                            matching_properties.append({
                                "property_id": property_data["id"],
                                "property_name": property_data["name"],
                                "developer": property_data["developer"],
                                "region": region_name,
                                "location": property_data["location"],
                                "type": unit_type["type"],
                                "price_idr": unit_type["price_idr"],
                                "available_units": unit_type["available_units"],
                                "sold_units": unit_type["sold_units"],
                                "total_units": unit_type["total_units"],
                                "status": unit_type["status"],
                                "facilities": property_data["facilities"]
                            })
            
            return matching_properties
        except Exception as e:
            self.logger.error(f"Error getting properties by price range: {e}")
            return []
    
    def get_available_units_by_region(self, region: str) -> Dict:
        """Get available units summary by region"""
        try:
            properties = self.get_properties_by_region(region)
            available_summary = {}
            
            for property_data in properties:
                property_name = property_data["name"]
                available_units = 0
                total_units = 0
                
                for unit_type in property_data["type_units"]:
                    available_units += unit_type["available_units"]
                    total_units += unit_type["total_units"]
                
                available_summary[property_name] = {
                    "available_units": available_units,
                    "total_units": total_units,
                    "sold_units": total_units - available_units,
                    "availability_rate": (available_units / total_units * 100) if total_units > 0 else 0
                }
            
            return available_summary
        except Exception as e:
            self.logger.error(f"Error getting available units for region {region}: {e}")
            return {}
    
    def get_sold_units_by_region(self, region: str) -> Dict:
        """Get sold units summary by region"""
        try:
            properties = self.get_properties_by_region(region)
            sold_summary = {}
            
            for property_data in properties:
                property_name = property_data["name"]
                sold_units = 0
                total_units = 0
                
                for unit_type in property_data["type_units"]:
                    sold_units += unit_type["sold_units"]
                    total_units += unit_type["total_units"]
                
                sold_summary[property_name] = {
                    "sold_units": sold_units,
                    "total_units": total_units,
                    "sales_rate": (sold_units / total_units * 100) if total_units > 0 else 0
                }
            
            return sold_summary
        except Exception as e:
            self.logger.error(f"Error getting sold units for region {region}: {e}")
            return {}
    
    def get_price_comparison(self, property_ids: List[str]) -> List[Dict]:
        """Compare prices across multiple properties"""
        try:
            comparison_data = []
            
            for property_id in property_ids:
                property_data = self.get_property_by_id(property_id)
                if property_data:
                    for unit_type in property_data["type_units"]:
                        comparison_data.append({
                            "property_id": property_id,
                            "property_name": property_data["name"],
                            "developer": property_data["developer"],
                            "type": unit_type["type"],
                            "price_idr": unit_type["price_idr"],
                            "price_per_m2": unit_type["price_idr"] / unit_type["building_area"],
                            "land_area": unit_type["land_area"],
                            "building_area": unit_type["building_area"],
                            "bedrooms": unit_type["bedrooms"],
                            "bathrooms": unit_type["bathrooms"],
                            "available_units": unit_type["available_units"],
                            "status": unit_type["status"]
                        })
            
            return comparison_data
        except Exception as e:
            self.logger.error(f"Error comparing prices: {e}")
            return []
    
    def get_market_overview(self) -> Dict:
        """Get comprehensive market overview"""
        try:
            db = self.property_database["property_database"]
            market_stats = db["market_statistics"]
            
            overview = {
                "total_properties": db["total_properties"],
                "market_value_idr": db["market_value_idr"],
                "total_units": market_stats["total_units_all_regions"],
                "available_units": market_stats["available_units"],
                "sold_units": market_stats["sold_units"],
                "average_price_idr": market_stats["average_price_idr"],
                "price_range_idr": market_stats["price_range_idr"],
                "market_segments": market_stats["market_segments"],
                "top_properties": market_stats["top_properties_by_sales"],
                "regional_breakdown": {}
            }
            
            # Add regional breakdown
            for region_name, region_data in db["regions"].items():
                overview["regional_breakdown"][region_name] = {
                    "total_properties": region_data["total_properties"],
                    "market_value_idr": region_data["market_value_idr"],
                    "properties_count": len(region_data["properties"])
                }
            
            return overview
        except Exception as e:
            self.logger.error(f"Error getting market overview: {e}")
            return {}
    
    def search_properties(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search properties with filters"""
        try:
            results = []
            db = self.property_database["property_database"]
            
            # Default filters
            if filters is None:
                filters = {}
            
            min_price = filters.get("min_price", 0)
            max_price = filters.get("max_price", float('inf'))
            min_bedrooms = filters.get("min_bedrooms", 0)
            region_filter = filters.get("region")
            
            for region_name, region_data in db["regions"].items():
                if region_filter and region_name != region_filter:
                    continue
                
                for property_data in region_data["properties"]:
                    # Search in property name and developer
                    if query.lower() in property_data["name"].lower() or \
                       query.lower() in property_data["developer"].lower():
                        
                        for unit_type in property_data["type_units"]:
                            # Apply filters
                            if (min_price <= unit_type["price_idr"] <= max_price and
                                unit_type["bedrooms"] >= min_bedrooms):
                                
                                results.append({
                                    "property_id": property_data["id"],
                                    "property_name": property_data["name"],
                                    "developer": property_data["developer"],
                                    "region": region_name,
                                    "location": property_data["location"],
                                    "type": unit_type["type"],
                                    "price_idr": unit_type["price_idr"],
                                    "land_area": unit_type["land_area"],
                                    "building_area": unit_type["building_area"],
                                    "bedrooms": unit_type["bedrooms"],
                                    "bathrooms": unit_type["bathrooms"],
                                    "carport": unit_type["carport"],
                                    "available_units": unit_type["available_units"],
                                    "sold_units": unit_type["sold_units"],
                                    "total_units": unit_type["total_units"],
                                    "status": unit_type["status"],
                                    "facilities": property_data["facilities"],
                                    "market_position": property_data["market_position"]
                                })
            
            return results
        except Exception as e:
            self.logger.error(f"Error searching properties: {e}")
            return []
    
    def get_property_intelligence_report(self, property_id: str) -> Dict:
        """Generate comprehensive intelligence report for a specific property"""
        try:
            property_data = self.get_property_by_id(property_id)
            if not property_data:
                return {"error": "Property not found"}
            
            # Calculate metrics
            total_units = sum(unit["total_units"] for unit in property_data["type_units"])
            available_units = sum(unit["available_units"] for unit in property_data["type_units"])
            sold_units = sum(unit["sold_units"] for unit in property_data["type_units"])
            
            # Price analysis
            prices = [unit["price_idr"] for unit in property_data["type_units"]]
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            # Sales performance
            sales_rate = (sold_units / total_units * 100) if total_units > 0 else 0
            availability_rate = (available_units / total_units * 100) if total_units > 0 else 0
            
            report = {
                "property_id": property_id,
                "basic_info": {
                    "name": property_data["name"],
                    "developer": property_data["developer"],
                    "location": property_data["location"],
                    "coordinates": property_data["coordinates"],
                    "market_position": property_data["market_position"],
                    "facilities": property_data["facilities"],
                    "launch_date": property_data["launch_date"],
                    "completion_date": property_data["completion_date"]
                },
                "unit_analysis": {
                    "total_units": total_units,
                    "available_units": available_units,
                    "sold_units": sold_units,
                    "sales_rate": round(sales_rate, 2),
                    "availability_rate": round(availability_rate, 2)
                },
                "price_analysis": {
                    "min_price_idr": min_price,
                    "max_price_idr": max_price,
                    "average_price_idr": round(avg_price),
                    "price_per_m2": property_data["price_per_m2"]
                },
                "unit_types": property_data["type_units"],
                "market_intelligence": {
                    "sales_velocity": "high" if sales_rate > 80 else "medium" if sales_rate > 50 else "low",
                    "price_competitiveness": "competitive" if avg_price < 500000000 else "premium" if avg_price < 1000000000 else "luxury",
                    "market_demand": "high" if availability_rate < 20 else "medium" if availability_rate < 50 else "low"
                }
            }
            
            return report
        except Exception as e:
            self.logger.error(f"Error generating intelligence report for {property_id}: {e}")
            return {"error": str(e)}
    
    def update_property_status(self, property_id: str, unit_type: str, sold_units: int) -> bool:
        """Update sold units count for a specific property unit type"""
        try:
            # This would typically update the database
            # For now, we'll just log the update
            self.logger.info(f"Updating {property_id} - {unit_type}: sold_units = {sold_units}")
            
            # In a real implementation, this would:
            # 1. Load the database
            # 2. Update the specific unit type
            # 3. Save the database
            # 4. Update market statistics
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating property status: {e}")
            return False
    
    def generate_market_trends_report(self) -> Dict:
        """Generate market trends analysis"""
        try:
            db = self.property_database["property_database"]
            market_stats = db["market_statistics"]
            
            trends = {
                "overall_market": {
                    "total_properties": db["total_properties"],
                    "total_units": market_stats["total_units_all_regions"],
                    "sold_units": market_stats["sold_units"],
                    "available_units": market_stats["available_units"],
                    "overall_sales_rate": round(market_stats["sold_units"] / market_stats["total_units_all_regions"] * 100, 2)
                },
                "segment_analysis": {},
                "price_trends": {
                    "average_price": market_stats["average_price_idr"],
                    "price_range": market_stats["price_range_idr"],
                    "price_distribution": {}
                },
                "regional_performance": {},
                "recommendations": []
            }
            
            # Segment analysis
            for segment, data in market_stats["market_segments"].items():
                segment_sales_rate = (data["sold_units"] / data["total_units"] * 100) if data["total_units"] > 0 else 0
                trends["segment_analysis"][segment] = {
                    "total_units": data["total_units"],
                    "sold_units": data["sold_units"],
                    "available_units": data["available_units"],
                    "sales_rate": round(segment_sales_rate, 2),
                    "average_price": data["average_price_idr"]
                }
            
            # Regional performance
            for region_name, region_data in db["regions"].items():
                total_region_units = sum(
                    sum(unit["total_units"] for unit in prop["type_units"])
                    for prop in region_data["properties"]
                )
                sold_region_units = sum(
                    sum(unit["sold_units"] for unit in prop["type_units"])
                    for prop in region_data["properties"]
                )
                
                region_sales_rate = (sold_region_units / total_region_units * 100) if total_region_units > 0 else 0
                
                trends["regional_performance"][region_name] = {
                    "total_properties": region_data["total_properties"],
                    "market_value": region_data["market_value_idr"],
                    "total_units": total_region_units,
                    "sold_units": sold_region_units,
                    "sales_rate": round(region_sales_rate, 2)
                }
            
            # Generate recommendations
            recommendations = []
            
            # High demand segments
            for segment, data in trends["segment_analysis"].items():
                if data["sales_rate"] > 80:
                    recommendations.append(f"{segment.title()} segment shows high demand ({data['sales_rate']:.1f}% sales rate)")
            
            # Low availability regions
            for region, data in trends["regional_performance"].items():
                if data["sales_rate"] > 85:
                    recommendations.append(f"{region.title()} shows strong sales performance ({data['sales_rate']:.1f}% sales rate)")
            
            trends["recommendations"] = recommendations
            
            return trends
        except Exception as e:
            self.logger.error(f"Error generating market trends report: {e}")
            return {"error": str(e)}

# Global instance for easy access
property_scout = PropertyScout()

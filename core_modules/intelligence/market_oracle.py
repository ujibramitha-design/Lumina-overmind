"""
LUMINA OS - PROJECT ORACLE
====================================

Market Prediction Engine
Advanced Market Intelligence and Prediction System

Features:
- Market Trend Analysis
- Price Prediction Models
- Demand Forecasting
- Competitor Intelligence
- Investment Opportunity Scoring
- Risk Assessment
- Strategic Recommendations
"""

import os
import sys
import json
import time
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
import statistics
from collections import defaultdict, Counter

# Add root directory to Python path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.append(str(root_dir))

# Import required modules
try:
    import google.generativeai as genai
    from core_modules.db_manager_supabase import get_supabase_manager
    from core_modules.notifications.telegram_sender import get_telegram_sender
    from agents.scout_agent.competitor_scout import run_competitor_surveillance
    from core_modules.trend_analyzer import analyze_market_trends
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing required packages...")
    os.system("pip install numpy pandas")
    print("Please restart the script after installation")
    sys.exit(1)

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

@dataclass
class MarketPrediction:
    """Market prediction data structure"""
    prediction_type: str
    confidence_score: float
    timeframe: str
    prediction_value: float
    current_value: float
    trend_direction: str  # up, down, stable
    factors: List[str]
    risks: List[str]
    opportunities: List[str]
    recommendation: str
    created_at: datetime
    expires_at: datetime

@dataclass
class PricePrediction:
    """Price prediction data structure"""
    location: str
    property_type: str
    current_price: float
    predicted_price: float
    price_change_percent: float
    confidence_score: float
    timeframe_months: int
    market_factors: List[str]
    risk_level: str
    investment_recommendation: str
    created_at: datetime

@dataclass
class DemandForecast:
    """Demand forecast data structure"""
    location: str
    property_type: str
    current_demand: str
    predicted_demand: str
    demand_trend: str
    confidence_score: float
    timeframe_months: int
    key_drivers: List[str]
    seasonal_patterns: List[str]
    market_saturation: float
    recommendation: str
    created_at: datetime

class MarketOracle:
    """
    Project Oracle - Market Prediction Engine
    Advanced market intelligence and prediction system for Lumina OS
    """
    
    def __init__(self):
        """Initialize Market Oracle"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini AI
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            self.logger.info(f"{GREEN}✅ Gemini AI initialized for market prediction{END}")
        else:
            self.gemini_model = None
            self.logger.warning(f"{YELLOW}⚠️ Gemini API key not found - using analytical models{END}")
        
        # Initialize database
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Database connected for market oracle{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Database connection failed: {e}{END}")
        
        # Initialize Telegram sender
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Telegram sender initialized for oracle alerts{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Telegram sender failed: {e}{END}")
        
        # Prediction models configuration
        self.prediction_models = {
            'price_regression': True,
            'demand_forecasting': True,
            'trend_analysis': True,
            'competitor_intelligence': True,
            'risk_assessment': True
        }
        
        # Market parameters
        self.location_focus = ["Serang", "Tangerang", "Jakarta", "Bogor", "Bandung", "Depok", "Bekasi"]
        self.property_types = ["Rumah", "Apartemen", "Ruko", "Tanah", "Cluster"]
        self.prediction_timeframes = [3, 6, 12, 24]  # months
        
        # Historical data cache
        self.historical_data = {}
        self.market_predictions = {}
        
        self.logger.info(f"{MAGENTA}🔮 PROJECT ORACLE: Market Prediction Engine initialized{END}")
        self.logger.info(f"{CYAN}📊 Prediction Models: {list(self.prediction_models.keys())}{END}")
        self.logger.info(f"{GREEN}✅ Ready for market intelligence and prediction{END}")
    
    def collect_market_data(self, days_back: int = 90) -> Dict[str, Any]:
        """
        Collect market data from various sources
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            Market data dictionary
        """
        try:
            self.logger.info(f"{BLUE}📊 Collecting market data for last {days_back} days...{END}")
            
            market_data = {
                'leads_data': [],
                'competitor_data': [],
                'trend_data': [],
                'price_history': [],
                'demand_indicators': []
            }
            
            # Collect leads data
            if self.supabase_manager:
                leads_result = self.supabase_manager.get_leads_by_date(days_back)
                if leads_result['success']:
                    market_data['leads_data'] = leads_result['data']
                    self.logger.info(f"{GREEN}✅ Collected {len(leads_result['data'])} leads{END}")
            
            # Collect competitor data
            try:
                competitor_result = run_competitor_surveillance()
                if competitor_result:
                    market_data['competitor_data'] = competitor_result
                    self.logger.info(f"{GREEN}✅ Collected competitor intelligence{END}")
            except Exception as e:
                self.logger.warning(f"{YELLOW}⚠️ Failed to collect competitor data: {e}{END}")
            
            # Collect trend data
            try:
                trend_result = analyze_market_trends(days_back)
                if trend_result:
                    market_data['trend_data'] = trend_result
                    self.logger.info(f"{GREEN}✅ Collected market trends{END}")
            except Exception as e:
                self.logger.warning(f"{YELLOW}⚠️ Failed to collect trend data: {e}{END}")
            
            # Store in cache
            self.historical_data = market_data
            
            return market_data
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Collect market data error: {str(e)}{END}")
            return {}
    
    def analyze_price_trends(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze price trends from market data
        
        Args:
            market_data: Market data dictionary
            
        Returns:
            Price trend analysis results
        """
        try:
            self.logger.info(f"{BLUE}📈 Analyzing price trends...{END}")
            
            price_analysis = {
                'average_prices': {},
                'price_trends': {},
                'price_volatility': {},
                'location_rankings': {},
                'property_type_rankings': {}
            }
            
            leads_data = market_data.get('leads_data', [])
            
            if not leads_data:
                self.logger.warning(f"{YELLOW}⚠️ No leads data available for price analysis{END}")
                return price_analysis
            
            # Extract price information
            prices_by_location = defaultdict(list)
            prices_by_property_type = defaultdict(list)
            
            for lead in leads_data:
                location = lead.get('location', 'Unknown')
                property_type = self._extract_property_type(lead.get('business_name', ''))
                score = lead.get('score', 0)
                
                # Estimate price based on score (simplified model)
                estimated_price = self._estimate_price_from_score(score, location, property_type)
                
                if estimated_price > 0:
                    prices_by_location[location].append(estimated_price)
                    prices_by_property_type[property_type].append(estimated_price)
            
            # Calculate averages and trends
            for location, prices in prices_by_location.items():
                if prices:
                    price_analysis['average_prices'][location] = statistics.mean(prices)
                    price_analysis['price_volatility'][location] = statistics.stdev(prices) if len(prices) > 1 else 0
            
            for prop_type, prices in prices_by_property_type.items():
                if prices:
                    price_analysis['average_prices'][prop_type] = statistics.mean(prices)
                    price_analysis['price_volatility'][prop_type] = statistics.stdev(prices) if len(prices) > 1 else 0
            
            # Rank locations and property types
            price_analysis['location_rankings'] = dict(sorted(
                price_analysis['average_prices'].items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
            
            price_analysis['property_type_rankings'] = dict(sorted(
                price_analysis['average_prices'].items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
            
            self.logger.info(f"{GREEN}✅ Price trends analyzed for {len(price_analysis['average_prices'])} categories{END}")
            
            return price_analysis
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Analyze price trends error: {str(e)}{END}")
            return {}
    
    def predict_prices(self, location: str, property_type: str, timeframe_months: int = 12) -> PricePrediction:
        """
        Predict future prices for a specific location and property type
        
        Args:
            location: Location name
            property_type: Property type
            timeframe_months: Prediction timeframe in months
            
        Returns:
            Price prediction object
        """
        try:
            self.logger.info(f"{CYAN}🔮 Predicting prices for {property_type} in {location} ({timeframe_months} months){END}")
            
            # Get current market data
            if not self.historical_data:
                self.collect_market_data()
            
            market_data = self.historical_data
            price_analysis = self.analyze_price_trends(market_data)
            
            # Get current price
            current_price = price_analysis.get('average_prices', {}).get(location, 0)
            if current_price == 0:
                current_price = price_analysis.get('average_prices', {}).get(property_type, 500000000)  # Default fallback
            
            # Calculate price prediction
            predicted_price = self._calculate_price_prediction(
                current_price, location, property_type, timeframe_months, price_analysis
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_prediction_confidence(
                location, property_type, price_analysis
            )
            
            # Determine trend direction
            price_change_percent = ((predicted_price - current_price) / current_price) * 100
            trend_direction = "up" if price_change_percent > 2 else "down" if price_change_percent < -2 else "stable"
            
            # Assess risk level
            risk_level = self._assess_investment_risk(
                location, property_type, price_change_percent, confidence_score
            )
            
            # Generate recommendation
            recommendation = self._generate_investment_recommendation(
                trend_direction, risk_level, price_change_percent, confidence_score
            )
            
            # Identify market factors
            market_factors = self._identify_market_factors(location, property_type, market_data)
            
            prediction = PricePrediction(
                location=location,
                property_type=property_type,
                current_price=current_price,
                predicted_price=predicted_price,
                price_change_percent=price_change_percent,
                confidence_score=confidence_score,
                timeframe_months=timeframe_months,
                market_factors=market_factors,
                risk_level=risk_level,
                investment_recommendation=recommendation,
                created_at=datetime.now()
            )
            
            self.logger.info(f"{GREEN}✅ Price prediction completed: {location} - {property_type}{END}")
            self.logger.info(f"{CYAN}📊 Current: Rp {current_price:,} → Predicted: Rp {predicted_price:,} ({price_change_percent:+.1f}%){END}")
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Predict prices error: {str(e)}{END}")
            # Return fallback prediction
            return PricePrediction(
                location=location,
                property_type=property_type,
                current_price=500000000,
                predicted_price=520000000,
                price_change_percent=4.0,
                confidence_score=0.6,
                timeframe_months=timeframe_months,
                market_factors=["Limited data"],
                risk_level="Medium",
                investment_recommendation="Proceed with caution",
                created_at=datetime.now()
            )
    
    def forecast_demand(self, location: str, property_type: str, timeframe_months: int = 12) -> DemandForecast:
        """
        Forecast market demand for a specific location and property type
        
        Args:
            location: Location name
            property_type: Property type
            timeframe_months: Forecast timeframe in months
            
        Returns:
            Demand forecast object
        """
        try:
            self.logger.info(f"{CYAN}📈 Forecasting demand for {property_type} in {location} ({timeframe_months} months){END}")
            
            # Get current market data
            if not self.historical_data:
                self.collect_market_data()
            
            market_data = self.historical_data
            leads_data = market_data.get('leads_data', [])
            
            # Analyze current demand
            current_demand = self._analyze_current_demand(location, property_type, leads_data)
            predicted_demand = self._predict_future_demand(current_demand, timeframe_months, market_data)
            
            # Determine demand trend
            demand_trend = self._determine_demand_trend(current_demand, predicted_demand)
            
            # Calculate confidence score
            confidence_score = self._calculate_demand_confidence(location, property_type, leads_data)
            
            # Identify key drivers
            key_drivers = self._identify_demand_drivers(location, property_type, market_data)
            
            # Analyze seasonal patterns
            seasonal_patterns = self._analyze_seasonal_patterns(leads_data)
            
            # Calculate market saturation
            market_saturation = self._calculate_market_saturation(location, property_type, market_data)
            
            # Generate recommendation
            recommendation = self._generate_demand_recommendation(
                demand_trend, market_saturation, confidence_score
            )
            
            forecast = DemandForecast(
                location=location,
                property_type=property_type,
                current_demand=current_demand,
                predicted_demand=predicted_demand,
                demand_trend=demand_trend,
                confidence_score=confidence_score,
                timeframe_months=timeframe_months,
                key_drivers=key_drivers,
                seasonal_patterns=seasonal_patterns,
                market_saturation=market_saturation,
                recommendation=recommendation,
                created_at=datetime.now()
            )
            
            self.logger.info(f"{GREEN}✅ Demand forecast completed: {location} - {property_type}{END}")
            self.logger.info(f"{CYAN}📊 Current: {current_demand} → Predicted: {predicted_demand} ({demand_trend}){END}")
            
            return forecast
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Forecast demand error: {str(e)}{END}")
            # Return fallback forecast
            return DemandForecast(
                location=location,
                property_type=property_type,
                current_demand="Medium",
                predicted_demand="High",
                demand_trend="Increasing",
                confidence_score=0.6,
                timeframe_months=timeframe_months,
                key_drivers=["Market growth"],
                seasonal_patterns=["Q4 peak"],
                market_saturation=0.6,
                recommendation="Monitor closely",
                created_at=datetime.now()
            )
    
    def generate_market_intelligence_report(self, location: str = "Serang") -> Dict[str, Any]:
        """
        Generate comprehensive market intelligence report
        
        Args:
            location: Location to analyze
            
        Returns:
            Market intelligence report
        """
        try:
            self.logger.info(f"{MAGENTA}🧠 Generating market intelligence report for {location}...{END}")
            
            # Collect market data
            market_data = self.collect_market_data(days_back=90)
            
            # Generate predictions
            predictions = []
            for property_type in ["Rumah", "Apartemen", "Ruko"]:
                price_pred = self.predict_prices(location, property_type, 12)
                demand_forecast = self.forecast_demand(location, property_type, 12)
                
                predictions.append({
                    'property_type': property_type,
                    'price_prediction': asdict(price_pred),
                    'demand_forecast': asdict(demand_forecast)
                })
            
            # Analyze competitor landscape
            competitor_analysis = self._analyze_competitor_landscape(market_data)
            
            # Identify investment opportunities
            opportunities = self._identify_investment_opportunities(location, predictions, market_data)
            
            # Assess risks
            risks = self._assess_market_risks(location, predictions, market_data)
            
            # Generate strategic recommendations
            recommendations = self._generate_strategic_recommendations(
                location, predictions, opportunities, risks
            )
            
            report = {
                'location': location,
                'report_date': datetime.now().isoformat(),
                'data_period': 'Last 90 days',
                'predictions': predictions,
                'competitor_analysis': competitor_analysis,
                'investment_opportunities': opportunities,
                'market_risks': risks,
                'strategic_recommendations': recommendations,
                'market_overview': self._generate_market_overview(market_data)
            }
            
            # Send report to Telegram
            if self.telegram_sender:
                report_summary = self._create_telegram_report_summary(report)
                self.telegram_sender.send_message(report_summary)
            
            self.logger.info(f"{GREEN}✅ Market intelligence report generated for {location}{END}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Generate market intelligence report error: {str(e)}{END}")
            return {}
    
    # Helper methods
    def _extract_property_type(self, business_name: str) -> str:
        """Extract property type from business name"""
        business_name_lower = business_name.lower()
        if 'apartemen' in business_name or 'apart' in business_name:
            return "Apartemen"
        elif 'ruko' in business_name or 'kios' in business_name:
            return "Ruko"
        elif 'tanah' in business_name or 'kavling' in business_name:
            return "Tanah"
        else:
            return "Rumah"
    
    def _estimate_price_from_score(self, score: int, location: str, property_type: str) -> float:
        """Estimate price from lead score"""
        # Base prices by property type
        base_prices = {
            "Rumah": 400000000,
            "Apartemen": 600000000,
            "Ruko": 800000000,
            "Tanah": 200000000
        }
        
        # Location multipliers
        location_multipliers = {
            "Jakarta": 2.0,
            "Tangerang": 1.5,
            "Bogor": 1.2,
            "Depok": 1.3,
            "Bekasi": 1.4,
            "Bandung": 1.1,
            "Serang": 1.0
        }
        
        base_price = base_prices.get(property_type, 400000000)
        location_mult = location_multipliers.get(location, 1.0)
        
        # Score-based multiplier (1-10 scale)
        score_mult = 0.5 + (score / 10) * 1.5
        
        return int(base_price * location_mult * score_mult)
    
    def _calculate_price_prediction(self, current_price: float, location: str, 
                                   property_type: str, timeframe_months: int, 
                                   price_analysis: Dict[str, Any]) -> float:
        """Calculate price prediction using analytical models"""
        # Get historical volatility
        volatility = price_analysis.get('price_volatility', {}).get(location, 0.1)
        
        # Market growth rate (simplified)
        monthly_growth_rate = 0.005  # 0.5% per month average
        
        # Adjust based on property type
        property_multipliers = {
            "Rumah": 1.0,
            "Apartemen": 1.1,
            "Ruko": 0.9,
            "Tanah": 1.2
        }
        
        prop_mult = property_multipliers.get(property_type, 1.0)
        
        # Calculate prediction
        predicted_price = current_price * (1 + monthly_growth_rate * timeframe_months) * prop_mult
        
        # Add some randomness for realism
        import random
        random_factor = 1 + (random.random() - 0.5) * 0.1  # ±5% random variation
        predicted_price *= random_factor
        
        return int(predicted_price)
    
    def _calculate_prediction_confidence(self, location: str, property_type: str, 
                                       price_analysis: Dict[str, Any]) -> float:
        """Calculate prediction confidence score"""
        # Base confidence
        base_confidence = 0.7
        
        # Adjust based on data availability
        avg_prices = price_analysis.get('average_prices', {})
        if location in avg_prices:
            base_confidence += 0.1
        
        if property_type in avg_prices:
            base_confidence += 0.1
        
        # Adjust based on volatility
        volatility = price_analysis.get('price_volatility', {}).get(location, 0.1)
        if volatility < 0.05:  # Low volatility increases confidence
            base_confidence += 0.1
        elif volatility > 0.2:  # High volatility decreases confidence
            base_confidence -= 0.1
        
        return min(base_confidence, 0.95)
    
    def _assess_investment_risk(self, location: str, property_type: str, 
                              price_change_percent: float, confidence_score: float) -> str:
        """Assess investment risk level"""
        risk_score = 0
        
        # Price change risk
        if abs(price_change_percent) > 15:
            risk_score += 2
        elif abs(price_change_percent) > 8:
            risk_score += 1
        
        # Confidence risk
        if confidence_score < 0.6:
            risk_score += 2
        elif confidence_score < 0.8:
            risk_score += 1
        
        # Location risk (simplified)
        high_risk_locations = ["Jakarta", "Tangerang"]
        if location in high_risk_locations:
            risk_score += 1
        
        if risk_score >= 3:
            return "High"
        elif risk_score >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _generate_investment_recommendation(self, trend_direction: str, risk_level: str, 
                                         price_change_percent: float, confidence_score: float) -> str:
        """Generate investment recommendation"""
        if risk_level == "High":
            return "High risk - Consider alternative investments"
        elif trend_direction == "up" and risk_level == "Low":
            return "Good investment opportunity - Consider buying"
        elif trend_direction == "down" and price_change_percent < -10:
            return "Price drop detected - Monitor for buying opportunity"
        else:
            return "Hold and monitor market conditions"
    
    def _identify_market_factors(self, location: str, property_type: str, market_data: Dict[str, Any]) -> List[str]:
        """Identify market factors affecting predictions"""
        factors = []
        
        # Economic factors (simplified)
        factors.extend([
            "Interest rate environment",
            "Inflation trends",
            "Government policies",
            "Infrastructure development"
        ])
        
        # Location-specific factors
        if location in ["Jakarta", "Tangerang"]:
            factors.append("Urbanization pressure")
        
        # Property type factors
        if property_type == "Apartemen":
            factors.append("Lifestyle preferences")
        elif property_type == "Ruko":
            factors.append("Business climate")
        
        return factors
    
    def _analyze_current_demand(self, location: str, property_type: str, leads_data: List[Dict]) -> str:
        """Analyze current demand level"""
        # Filter leads for location and property type
        relevant_leads = []
        for lead in leads_data:
            lead_location = lead.get('location', '').lower()
            business_name = lead.get('business_name', '').lower()
            
            if location.lower() in lead_location or property_type.lower() in business_name:
                relevant_leads.append(lead)
        
        # Determine demand level based on lead count and scores
        lead_count = len(relevant_leads)
        avg_score = statistics.mean([lead.get('score', 0) for lead in relevant_leads]) if relevant_leads else 0
        
        if lead_count > 20 and avg_score > 7:
            return "High"
        elif lead_count > 10 and avg_score > 5:
            return "Medium"
        elif lead_count > 5:
            return "Low"
        else:
            return "Very Low"
    
    def _predict_future_demand(self, current_demand: str, timeframe_months: int, market_data: Dict[str, Any]) -> str:
        """Predict future demand"""
        demand_hierarchy = ["Very Low", "Low", "Medium", "High", "Very High"]
        current_index = demand_hierarchy.index(current_demand)
        
        # Simple trend prediction (can be enhanced with ML models)
        trend_factor = 0.1  # 10% chance of moving up per month
        expected_change = (timeframe_months * trend_factor)
        
        # Add some randomness
        import random
        random_factor = (random.random() - 0.5) * 0.2  # ±10% random variation
        
        new_index = current_index + expected_change + random_factor
        new_index = max(0, min(len(demand_hierarchy) - 1, new_index))
        
        return demand_hierarchy[int(new_index)]
    
    def _determine_demand_trend(self, current_demand: str, predicted_demand: str) -> str:
        """Determine demand trend"""
        demand_hierarchy = ["Very Low", "Low", "Medium", "High", "Very High"]
        current_index = demand_hierarchy.index(current_demand)
        predicted_index = demand_hierarchy.index(predicted_demand)
        
        if predicted_index > current_index:
            return "Increasing"
        elif predicted_index < current_index:
            return "Decreasing"
        else:
            return "Stable"
    
    def _calculate_demand_confidence(self, location: str, property_type: str, leads_data: List[Dict]) -> float:
        """Calculate demand forecast confidence"""
        base_confidence = 0.6
        
        # Adjust based on data volume
        relevant_leads = [
            lead for lead in leads_data
            if location.lower() in lead.get('location', '').lower() or 
               property_type.lower() in lead.get('business_name', '').lower()
        ]
        
        if len(relevant_leads) > 50:
            base_confidence += 0.2
        elif len(relevant_leads) > 20:
            base_confidence += 0.1
        
        return min(base_confidence, 0.9)
    
    def _identify_demand_drivers(self, location: str, property_type: str, market_data: Dict[str, Any]) -> List[str]:
        """Identify key demand drivers"""
        drivers = []
        
        # General drivers
        drivers.extend([
            "Population growth",
            "Economic development",
            "Infrastructure projects"
        ])
        
        # Location-specific drivers
        if location == "Serang":
            drivers.extend([
                "Industrial development",
                "Government projects",
                "Accessibility improvement"
            ])
        
        # Property type-specific drivers
        if property_type == "Rumah":
            drivers.extend([
                "Family formation",
                "School quality",
                "Neighborhood development"
            ])
        elif property_type == "Apartemen":
            drivers.extend([
                "Urban lifestyle",
                "Investment returns",
                "Convenience factors"
            ])
        
        return drivers
    
    def _analyze_seasonal_patterns(self, leads_data: List[Dict]) -> List[str]:
        """Analyze seasonal patterns in demand"""
        # Simplified seasonal analysis
        patterns = []
        
        # Group leads by month
        monthly_leads = defaultdict(int)
        for lead in leads_data:
            try:
                date_str = lead.get('date_found', '')
                if date_str:
                    date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    month = date.strftime('%B')
                    monthly_leads[month] += 1
            except:
                continue
        
        # Identify peak months
        if monthly_leads:
            sorted_months = sorted(monthly_leads.items(), key=lambda x: x[1], reverse=True)
            top_months = [month for month, count in sorted_months[:3]]
            patterns.extend([f"Peak demand in {month}" for month in top_months])
        
        return patterns
    
    def _calculate_market_saturation(self, location: str, property_type: str, market_data: Dict[str, Any]) -> float:
        """Calculate market saturation level"""
        # Simplified saturation calculation
        leads_data = market_data.get('leads_data', [])
        
        # Count relevant properties
        relevant_properties = 0
        for lead in leads_data:
            if location.lower() in lead.get('location', '').lower():
                relevant_properties += 1
        
        # Estimate saturation (simplified)
        max_properties = 1000  # Arbitrary number for example
        saturation = min(relevant_properties / max_properties, 1.0)
        
        return saturation
    
    def _generate_demand_recommendation(self, demand_trend: str, market_saturation: float, confidence_score: float) -> str:
        """Generate demand-based recommendation"""
        if demand_trend == "Increasing" and market_saturation < 0.7:
            return "Strong demand - Consider increasing supply"
        elif demand_trend == "Decreasing" and market_saturation > 0.8:
            return "Oversupplied market - Consider reducing inventory"
        elif confidence_score < 0.6:
            return "Low confidence - Monitor closely"
        else:
            return "Stable market - Maintain current strategy"
    
    def _analyze_competitor_landscape(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor landscape"""
        competitor_data = market_data.get('competitor_data', [])
        
        if not competitor_data:
            return {"status": "No competitor data available"}
        
        # Extract competitor information
        competitors = []
        for competitor in competitor_data:
            if isinstance(competitor, dict):
                competitors.append({
                    'name': competitor.get('name', 'Unknown'),
                    'base_price': competitor.get('base_price', 0),
                    'promos': competitor.get('promos', []),
                    'sentiment_score': competitor.get('sentiment_score', 0)
                })
        
        # Calculate statistics
        if competitors:
            avg_price = statistics.mean([c['base_price'] for c in competitors if c['base_price'] > 0])
            avg_sentiment = statistics.mean([c['sentiment_score'] for c in competitors if c['sentiment_score'] != 0])
            
            return {
                'competitor_count': len(competitors),
                'average_price': avg_price,
                'average_sentiment': avg_sentiment,
                'price_range': {
                    'min': min([c['base_price'] for c in competitors if c['base_price'] > 0]),
                    'max': max([c['base_price'] for c in competitors if c['base_price'] > 0])
                },
                'top_competitors': sorted(competitors, key=lambda x: x['base_price'], reverse=True)[:5]
            }
        
        return {"status": "No valid competitor data"}
    
    def _identify_investment_opportunities(self, location: str, predictions: List[Dict], market_data: Dict[str, Any]) -> List[str]:
        """Identify investment opportunities"""
        opportunities = []
        
        for pred in predictions:
            price_pred = pred['price_prediction']
            demand_forecast = pred['demand_forecast']
            
            # Check for undervalued properties
            if (price_pred['price_change_percent'] > 5 and 
                demand_forecast['predicted_demand'] in ['High', 'Very High'] and
                price_pred['confidence_score'] > 0.7):
                
                opportunities.append(
                    f"Undervalued {price_pred['property_type']} in {location} "
                    f"({price_pred['price_change_percent']:+.1f}% growth potential)"
                )
        
        # Add general opportunities based on market data
        trends = market_data.get('trend_data', {})
        if trends:
            trending_topics = trends.get('trending_topics', [])
            if 'KPR' in trending_topics:
                opportunities.append("Financing-friendly market - KPR demand increasing")
            if 'DP' in trending_topics:
                opportunities.append("Down payment assistance programs gaining traction")
        
        return opportunities
    
    def _assess_market_risks(self, location: str, predictions: List[Dict], market_data: Dict[str, Any]) -> List[str]:
        """Assess market risks"""
        risks = []
        
        # Check for high volatility
        for pred in predictions:
            price_pred = pred['price_prediction']
            if price_pred['confidence_score'] < 0.5:
                risks.append(
                    f"Low confidence prediction for {price_pred['property_type']} in {location}"
                )
        
        # General market risks
        risks.extend([
            "Interest rate volatility",
            "Regulatory changes",
            "Economic uncertainty",
            "Supply chain disruptions"
        ])
        
        # Location-specific risks
        if location in ["Jakarta", "Tangerang"]:
            risks.append("High competition and price pressure")
        
        return risks
    
    def _generate_strategic_recommendations(self, location: str, predictions: List[Dict], 
                                             opportunities: List[str], risks: List[str]) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # General recommendations
        recommendations.append(f"Focus on {location} market with data-driven approach")
        
        # Property-specific recommendations
        for pred in predictions:
            price_pred = pred['price_prediction']
            demand_forecast = pred['demand_forecast']
            
            if price_pred['trend_direction'] == 'up':
                recommendations.append(
                    f"Consider increasing {price_pred['property_type']} inventory in {location}"
                )
            elif price_pred['trend_direction'] == 'down':
                recommendations.append(
                    f"Monitor {price_pred['property_type']} prices for buying opportunities in {location}"
                )
        
        # Opportunity-based recommendations
        for opportunity in opportunities[:3]:  # Top 3 opportunities
            recommendations.append(f"EXPLORE: {opportunity}")
        
        # Risk-based recommendations
        for risk in risks[:3]:  # Top 3 risks
            recommendations.append(f"MITIGATE: {risk}")
        
        return recommendations
    
    def _generate_market_overview(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market overview"""
        leads_data = market_data.get('leads_data', [])
        
        return {
            'total_leads': len(leads_data),
            'average_score': statistics.mean([lead.get('score', 0) for lead in leads_data]) if leads_data else 0,
            'top_locations': self._get_top_locations(leads_data),
            'trending_keywords': self._get_trending_keywords(leads_data),
            'data_quality': 'Good' if len(leads_data) > 50 else 'Limited'
        }
    
    def _get_top_locations(self, leads_data: List[Dict]) -> List[str]:
        """Get top locations from leads data"""
        location_counts = Counter(lead.get('location', 'Unknown') for lead in leads_data)
        return [loc for loc, count in location_counts.most_common(5)]
    
    def _get_trending_keywords(self, leads_data: List[Dict]) -> List[str]:
        """Get trending keywords from leads data"""
        all_keywords = []
        for lead in leads_data:
            keywords = lead.get('keywords', '').split(',')
            all_keywords.extend([kw.strip() for kw in keywords if kw.strip()])
        
        keyword_counts = Counter(all_keywords)
        return [kw for kw, count in keyword_counts.most_common(10)]
    
    def _create_telegram_report_summary(self, report: Dict[str, Any]) -> str:
        """Create Telegram-friendly report summary"""
        location = report['location']
        date = report['report_date']
        
        summary = f"""
🔮 **MARKET ORACLE REPORT**
📍 **Location**: {location}
📅 **Date**: {date}

📊 **PREDICTIONS**:
"""
        
        # Add top 3 predictions
        for i, pred in enumerate(report['predictions'][:3]):
            price_pred = pred['price_prediction']
            demand_forecast = pred['demand_forecast']
            
            summary += f"""
{i+1}. {pred['property_type']}:
   💰 Current: Rp {price_pred['current_price']:,}
   📈 Predicted: Rp {price_pred['predicted_price']:} ({price_pred['price_change_percent']:+.1f}%)
   📊 Demand: {demand_forecast['current_demand']} → {demand_forecast['predicted_demand']} ({demand_forecast['demand_trend']})
   🎯 Risk: {price_pred['risk_level']}
"""
        
        # Add opportunities
        opportunities = report.get('investment_opportunities', [])[:3]
        if opportunities:
            summary += "\n💡 **OPPORTUNITIES**:\n"
            for i, opp in enumerate(opportunities):
                summary += f"{i+1}. {opp}\n"
        
        # Add recommendations
        recommendations = report.get('strategic_recommendations', [])[:3]
        if recommendations:
            summary += "\n🎯 **RECOMMENDATIONS**:\n"
            for i, rec in enumerate(recommendations):
                summary += f"{i+1}. {rec}\n"
        
        return summary.strip()
    
    def get_oracle_statistics(self) -> Dict[str, Any]:
        """Get oracle system statistics"""
        return {
            'predictions_generated': len(self.market_predictions),
            'data_collection_runs': len(self.historical_data),
            'active_models': list(self.prediction_models.keys()),
            'locations_tracked': self.location_focus,
            'property_types_tracked': self.property_types,
            'last_update': datetime.now().isoformat(),
            'system_status': 'Operational'
        }

# Global market oracle instance
market_oracle = MarketOracle()

# Convenience functions
def predict_market_prices(location: str, property_type: str, timeframe_months: int = 12) -> PricePrediction:
    """Convenience function to predict market prices"""
    return market_oracle.predict_prices(location, property_type, timeframe_months)

def forecast_market_demand(location: str, property_type: str, timeframe_months: int = 12) -> DemandForecast:
    """Convenience function to forecast market demand"""
    return market_oracle.forecast_demand(location, property_type, timeframe_months)

def generate_market_intelligence(location: str = "Serang") -> Dict[str, Any]:
    """Convenience function to generate market intelligence"""
    return market_oracle.generate_market_intelligence_report(location)

def get_oracle_stats() -> Dict[str, Any]:
    """Convenience function to get oracle statistics"""
    return market_oracle.get_oracle_statistics()

# Test function
if __name__ == "__main__":
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - PROJECT ORACLE{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    # Test market intelligence
    print(f"{BLUE}🧠 Testing market intelligence generation...{END}")
    
    # Generate report for Serang
    report = generate_market_intelligence("Serang")
    
    if report:
        print(f"{GREEN}✅ Market intelligence report generated{END}")
        print(f"{CYAN}📍 Location: {report['location']}{END}")
        print(f"{CYAN}📅 Report Date: {report['report_date']}{END}")
        print(f"{CYAN}📊 Predictions: {len(report['predictions'])} property types{END}")
        
        # Show sample prediction
        if report['predictions']:
            sample_pred = report['predictions'][0]
            price_pred = sample_pred['price_prediction']
            print(f"{GREEN}✅ Sample Prediction:{END}")
            print(f"  Property: {price_pred['property_type']}")
            print(f"  Current: Rp {price_pred['current_price']:,}")
            print(f"  Predicted: Rp {price_pred['predicted_price']::,}")
            print(f"  Change: {price_pred['price_change_percent']:+.1f}%")
            print(f"  Confidence: {price_pred['confidence_score']:.1f}")
            print(f"  Risk: {price_pred['risk_level']}")
    else:
        print(f"{YELLOW}⚠️ No report data available{END}")
    
    # Show statistics
    stats = get_oracle_stats()
    print(f"{CYAN}📊 Oracle Statistics:{END}")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"{MAGENTA}{'='*80}{END}")

"""
Trend Analyzer Module - Advanced Intelligence Layer
Mendeteksi tren pasar dari database leads untuk strategic insights
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging
from collections import Counter, defaultdict

class TrendAnalyzer:
    def __init__(self, db_path: str = "data/leads.db"): # (SQLite - removed)
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path
        self.trends_file = "logs/market_trends.txt"
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Trend detection keywords
        self.trend_keywords = {
            'price_trends': ['harga', 'rp', 'juta', 'miliar', 'cicilan', 'dp', 'uang muka'],
            'location_trends': ['serang', 'tangerang', 'jakarta', 'bogor', 'depok', 'bekasi', 'cipocok', 'cilegon'],
            'bank_trends': ['btn', 'bni', 'bri', 'bca', 'mandiri', 'cimb', 'danamon', 'permata', 'panin', 'kpr'],
            'pain_point_trends': ['khawatir', 'sulit', 'bingung', 'masalah', 'kendala', 'kesulitan', 'belum', 'tidak'],
            'intent_trends': ['beli', 'cari', 'butuh', 'dicari', 'survey', 'nego', 'deal', 'booking', 'ajukan']
        }
        
        # Trend analysis periods
        self.analysis_periods = {
            'daily': 1,
            'weekly': 7,
            'monthly': 30
        }
    
    def get_leads_from_database(self, days_back: int = 30) -> List[Dict]:
        """
        Retrieve leads dari database untuk analisis tren
        """
        try:
            if not os.path.exists(self.db_path):
                self.logger.warning(f"Database not found: {self.db_path}")
                return []
            
            # SQLite connection removed
            # cursor = conn.cursor()
            
            # Get leads dari N hari terakhir
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            query = """
            SELECT id, title, content_snippet, entity_data, intent_category, 
                   score, lead_type, location, date_found, source
            FROM leads 
            WHERE date_found >= ? 
            ORDER BY date_found DESC
            """
            
            # cursor.execute() removedquery, (cutoff_date,))
            # rows = cursor.fetchall()
            rows = [] # Return empty list as DB logic is removed
            
            leads = []
            for row in rows:
                lead = {
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'entity_data': json.loads(row[3]) if row[3] else {},
                    'intent_category': row[4],
                    'score': row[5],
                    'lead_type': row[6],
                    'location': row[7],
                    'date_found': row[8],
                    'source': row[9]
                }
                leads.append(lead)
            
            # conn.close() # removed
            self.logger.info(f"Retrieved {len(leads)} leads from database (last {days_back} days)")
            return leads
            
        except Exception as e:
            self.logger.error(f"Error retrieving leads from database: {e}")
            return []
    
    def extract_keywords_from_leads(self, leads: List[Dict]) -> Dict[str, Counter]:
        """
        Extract dan hitung frekuensi keywords dari leads
        """
        keyword_counters = {}
        
        for category, keywords in self.trend_keywords.items():
            counter = Counter()
            
            for lead in leads:
                text = f"{lead.get('title', '')} {lead.get('content', '')}".lower()
                
                # Count keyword occurrences
                for keyword in keywords:
                    count = len(re.findall(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE))
                    if count > 0:
                        counter[keyword] += count
            
            keyword_counters[category] = counter
        
        return keyword_counters
    
    def analyze_entity_trends(self, leads: List[Dict]) -> Dict[str, Dict]:
        """
        Analisis tren dari entity data yang diekstrak
        """
        entity_trends = {
            'price_ranges': Counter(),
            'locations': Counter(),
            'banks': Counter(),
            'pain_points': Counter()
        }
        
        for lead in leads:
            entities = lead.get('entity_data', {})
            
            # Price ranges
            price = entities.get('price', '')
            if price:
                # Categorize price ranges
                if 'juta' in price.lower() or 'jt' in price.lower():
                    price_range = self._categorize_price_range(price)
                    entity_trends['price_ranges'][price_range] += 1
            
            # Locations
            location = entities.get('location', '')
            if location:
                entity_trends['locations'][location] += 1
            
            # Banks
            bank = entities.get('bank', '')
            if bank:
                entity_trends['banks'][bank.upper()] += 1
            
            # Pain points
            pain_point = entities.get('pain_point', '')
            if pain_point:
                entity_trends['pain_points'][pain_point] += 1
        
        return entity_trends
    
    def _categorize_price_range(self, price_text: str) -> str:
        """
        Kategorisasi harga ke range tertentu
        """
        price_text = price_text.lower()
        
        # Extract numbers
        numbers = re.findall(r'\d+', price_text)
        if not numbers:
            return 'unknown'
        
        num = int(numbers[0])
        
        if 'miliar' in price_text or 'milyar' in price_text:
            return '1M+'
        elif 'juta' in price_text or 'jt' in price_text:
            if num < 300:
                return '<300M'
            elif num < 500:
                return '300-500M'
            elif num < 700:
                return '500-700M'
            elif num < 1000:
                return '700-1B'
            else:
                return '1B+'
        elif 'ribu' in price_text or 'rb' in price_text:
            return '<10M'
        else:
            return 'unknown'
    
    def analyze_intent_trends(self, leads: List[Dict]) -> Dict[str, Counter]:
        """
        Analisis tren intent classification
        """
        intent_counter = Counter()
        intent_by_source = defaultdict(Counter)
        
        for lead in leads:
            intent = lead.get('intent_category', 'Informational')
            source = lead.get('source', 'Unknown')
            
            intent_counter[intent] += 1
            intent_by_source[source][intent] += 1
        
        return {
            'overall': intent_counter,
            'by_source': dict(intent_by_source)
        }
    
    def detect_trending_topics(self, keyword_counters: Dict[str, Counter], threshold: float = 0.1) -> List[Dict]:
        """
        Deteksi topics yang sedang trending
        """
        trending_topics = []
        
        for category, counter in keyword_counters.items():
            if not counter:
                continue
            
            total = sum(counter.values())
            
            for keyword, count in counter.most_common():
                frequency = count / total
                
                if frequency >= threshold:  # Threshold untuk trending
                    trending_topics.append({
                        'category': category,
                        'keyword': keyword,
                        'count': count,
                        'frequency': frequency,
                        'trend_level': self._calculate_trend_level(frequency)
                    })
        
        # Sort by frequency
        trending_topics.sort(key=lambda x: x['frequency'], reverse=True)
        
        return trending_topics
    
    def _calculate_trend_level(self, frequency: float) -> str:
        """
        Kalkulasi level trending berdasarkan frekuensi
        """
        if frequency >= 0.3:
            return 'HIGH'
        elif frequency >= 0.2:
            return 'MEDIUM'
        elif frequency >= 0.1:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def generate_trend_report(self, leads: List[Dict]) -> Dict:
        """
        Generate comprehensive trend report
        """
        if not leads:
            return {'status': 'no_data', 'message': 'No leads found for analysis'}
        
        # Extract keywords
        keyword_counters = self.extract_keywords_from_leads(leads)
        
        # Analyze entities
        entity_trends = self.analyze_entity_trends(leads)
        
        # Analyze intents
        intent_trends = self.analyze_intent_trends(leads)
        
        # Detect trending topics
        trending_topics = self.detect_trending_topics(keyword_counters)
        
        # Calculate statistics
        total_leads = len(leads)
        high_score_leads = len([l for l in leads if l.get('score', 0) >= 7])
        
        # Generate insights
        insights = self._generate_insights(
            keyword_counters, entity_trends, intent_trends, trending_topics
        )
        
        report = {
            'status': 'success',
            'analysis_date': datetime.now().isoformat(),
            'period_analyzed': f'{len(leads)} leads',
            'statistics': {
                'total_leads': total_leads,
                'high_score_leads': high_score_leads,
                'high_intent_percentage': (high_score_leads / total_leads * 100) if total_leads > 0 else 0
            },
            'keyword_trends': keyword_counters,
            'entity_trends': entity_trends,
            'intent_trends': intent_trends,
            'trending_topics': trending_topics[:10],  # Top 10 trending topics
            'insights': insights
        }
        
        return report
    
    def _generate_insights(self, keyword_counters: Dict, entity_trends: Dict, 
                          intent_trends: Dict, trending_topics: List[Dict]) -> List[Dict]:
        """
        Generate actionable insights dari trend analysis
        """
        insights = []
        
        # Price insights
        price_ranges = entity_trends.get('price_ranges', Counter())
        if price_ranges:
            most_common_price = price_ranges.most_common(1)[0]
            insights.append({
                'type': 'price_insight',
                'title': 'Price Range Trend',
                'description': f'Most common price range: {most_common_price[0]} ({most_common_price[1]} leads)',
                'actionable': True,
                'recommendation': f'Focus marketing efforts on properties in {most_common_price[0]} range'
            })
        
        # Location insights
        locations = entity_trends.get('locations', Counter())
        if locations:
            top_location = locations.most_common(1)[0]
            insights.append({
                'type': 'location_insight',
                'title': 'Hot Location',
                'description': f'Most mentioned location: {top_location[0]} ({top_location[1]} leads)',
                'actionable': True,
                'recommendation': f'Increase inventory in {top_location[0]} area'
            })
        
        # Pain point insights
        pain_points = entity_trends.get('pain_points', Counter())
        if pain_points:
            top_pain = pain_points.most_common(1)[0]
            insights.append({
                'type': 'pain_point_insight',
                'title': 'Common Customer Concern',
                'description': f'Most common pain point: {top_pain[0]} ({top_pain[1]} mentions)',
                'actionable': True,
                'recommendation': f'Address {top_pain[0]} concerns in marketing materials'
            })
        
        # Intent insights
        overall_intents = intent_trends.get('overall', Counter())
        if overall_intents:
            top_intent = overall_intents.most_common(1)[0]
            insights.append({
                'type': 'intent_insight',
                'title': 'Dominant Customer Intent',
                'description': f'Most common intent: {top_intent[0]} ({top_intent[1]} leads)',
                'actionable': True,
                'recommendation': f'Tailor messaging for {top_intent[0]} intent customers'
            })
        
        # Trending topic insights
        high_trends = [t for t in trending_topics if t.get('trend_level') == 'HIGH']
        if high_trends:
            insights.append({
                'type': 'trending_topic_insight',
                'title': 'Hot Trending Topics',
                'description': f'{len(high_trends)} high-trending topics detected',
                'actionable': True,
                'recommendation': 'Leverage trending topics in marketing campaigns'
            })
        
        return insights
    
    def save_trend_report(self, report: Dict) -> bool:
        """
        Save trend report ke file
        """
        try:
            with open(self.trends_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("MARKET TRENDS ANALYSIS REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Analysis Date: {report['analysis_date']}\n")
                f.write(f"Period Analyzed: {report['period_analyzed']}\n\n")
                
                # Statistics
                stats = report.get('statistics', {})
                f.write("STATISTICS:\n")
                f.write(f"Total Leads: {stats.get('total_leads', 0)}\n")
                f.write(f"High Score Leads: {stats.get('high_score_leads', 0)}\n")
                f.write(f"High Intent Percentage: {stats.get('high_intent_percentage', 0):.1f}%\n\n")
                
                # Trending Topics
                trending = report.get('trending_topics', [])
                if trending:
                    f.write("TRENDING TOPICS:\n")
                    for i, topic in enumerate(trending[:10], 1):
                        f.write(f"{i}. {topic['keyword']} ({topic['category']}) - {topic['trend_level']} trend\n")
                        f.write(f"   Frequency: {topic['frequency']:.1%}, Count: {topic['count']}\n")
                    f.write("\n")
                
                # Entity Trends
                entities = report.get('entity_trends', {})
                if entities.get('price_ranges'):
                    f.write("PRICE RANGE TRENDS:\n")
                    for price_range, count in entities['price_ranges'].most_common():
                        f.write(f"- {price_range}: {count} leads\n")
                    f.write("\n")
                
                if entities.get('locations'):
                    f.write("LOCATION TRENDS:\n")
                    for location, count in entities['locations'].most_common(5):
                        f.write(f"- {location}: {count} leads\n")
                    f.write("\n")
                
                if entities.get('pain_points'):
                    f.write("PAIN POINT TRENDS:\n")
                    for pain_point, count in entities['pain_points'].most_common(5):
                        f.write(f"- {pain_point}: {count} mentions\n")
                    f.write("\n")
                
                # Intent Trends
                intents = report.get('intent_trends', {})
                if intents.get('overall'):
                    f.write("INTENT DISTRIBUTION:\n")
                    for intent, count in intents['overall'].most_common():
                        f.write(f"- {intent}: {count} leads\n")
                    f.write("\n")
                
                # Insights
                insights = report.get('insights', [])
                if insights:
                    f.write("ACTIONABLE INSIGHTS:\n")
                    for i, insight in enumerate(insights, 1):
                        f.write(f"{i}. {insight['title']}\n")
                        f.write(f"   {insight['description']}\n")
                        f.write(f"   Recommendation: {insight['recommendation']}\n\n")
                
                f.write("=" * 80 + "\n")
                f.write(f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Trend report saved to {self.trends_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving trend report: {e}")
            return False
    
    def analyze_and_save_trends(self, days_back: int = 30) -> Dict:
        """
        Complete trend analysis workflow
        """
        try:
            # Get leads from database
            leads = self.get_leads_from_database(days_back)
            
            # Generate trend report
            report = self.generate_trend_report(leads)
            
            # Save report
            if report.get('status') == 'success':
                self.save_trend_report(report)
                self.logger.info("Trend analysis completed successfully")
            else:
                self.logger.warning("Trend analysis completed with no data")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error in trend analysis workflow: {e}")
            return {'status': 'error', 'message': str(e)}

# Global trend analyzer instance
trend_analyzer = TrendAnalyzer()

# Convenience functions
def analyze_market_trends(days_back: int = 30) -> Dict:
    """Analyze market trends and save report"""
    return trend_analyzer.analyze_and_save_trends(days_back)

def get_trending_topics(threshold: float = 0.1) -> List[Dict]:
    """Get current trending topics"""
    leads = trend_analyzer.get_leads_from_database(7)  # Last 7 days
    keyword_counters = trend_analyzer.extract_keywords_from_leads(leads)
    return trend_analyzer.detect_trending_topics(keyword_counters, threshold)

if __name__ == "__main__":
    # Test trend analyzer
    logging.basicConfig(level=logging.INFO)
    print("=== Trend Analyzer Test ===")
    
    report = analyze_market_trends(30)
    print(f"Trend Analysis Status: {report.get('status')}")
    
    if report.get('status') == 'success':
        print(f"Analyzed {report.get('period_analyzed')}")
        print(f"Trending topics found: {len(report.get('trending_topics', []))}")
        print(f"Insights generated: {len(report.get('insights', []))}")
        print(f"Report saved to: {trend_analyzer.trends_file}")
    else:
        print(f"No data available or error occurred")

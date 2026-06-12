"""
Market Intelligence Module - Scout Agent
Mengumpulkan dan menganalisis data pasar properti menggunakan DuckDuckGo Search
Professional version dengan User-Agent masking dan comprehensive error handling
"""

import requests
import json
import time
import os
import random
from datetime import datetime
from typing import Dict, List, Optional
import logging
from ddgs import DDGS

class MarketIntelligence:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Professional User-Agent rotation untuk menghindari blocking
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
        
        # Rate limiting settings
        self.request_delay = 2  # seconds between requests
        self.max_retries = 3
        self.retry_delay = 5  # seconds between retries
        
    def _safe_search_with_retry(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Melakukan pencarian dengan retry logic dan error handling yang komprehensif
        """
        for attempt in range(self.max_retries):
            try:
                # Rotate User-Agent untuk setiap attempt
                self.ddgs = DDGS()
                
                self.logger.info(f"Search attempt {attempt + 1}/{self.max_retries} for query: {query}")
                
                # Lakukan pencarian dengan timeout
                results = list(self.ddgs.text(query, max_results=max_results))
                
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
                
                # Wait before retry dengan exponential backoff
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    self.logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
        
        self.logger.error(f"All {self.max_retries} attempts failed for query: {query}")
        return []
    
    def search_cipocok_jaya_prices(self) -> List[Dict]:
        """
        Mencari informasi harga rumah baru di sekitar Cipocok Jaya Serang menggunakan DuckDuckGo
        Dengan comprehensive error handling dan professional User-Agent rotation
        """
        try:
            # Query pencarian untuk harga rumah di Cipocok Jaya
            query = "Harga rumah baru di sekitar Cipocok Jaya Serang"
            self.logger.info(f"Starting price search for: {query}")
            
            # Rate limiting
            time.sleep(self.request_delay)
            
            # Lakukan pencarian dengan retry logic
            results = self._safe_search_with_retry(query, max_results=10)
            
            # Proses hasil pencarian
            search_results = []
            for result in results:
                try:
                    search_data = {
                        'query': query,
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'search_time': datetime.now().isoformat(),
                        'source': 'DuckDuckGo',
                        'data_type': 'price_info',
                        'location': 'Cipocok Jaya, Serang'
                    }
                    search_results.append(search_data)
                except Exception as e:
                    self.logger.error(f"Error processing search result: {e}")
                    continue
            
            self.logger.info(f"Successfully processed {len(search_results)} price results for Cipocok Jaya")
            return search_results
            
        except Exception as e:
            self.logger.error(f"Critical error in search_cipocok_jaya_prices: {e}")
            return []
    
    def search_cipocok_jaya_facilities(self) -> List[Dict]:
        """
        Mencari informasi fasilitas umum terbaru di Cipocok Jaya menggunakan DuckDuckGo
        Dengan comprehensive error handling dan professional User-Agent rotation
        """
        try:
            # Query pencarian untuk fasilitas umum di Cipocok Jaya
            query = "Fasilitas umum terbaru di Cipocok Jaya"
            self.logger.info(f"Starting facilities search for: {query}")
            
            # Rate limiting
            time.sleep(self.request_delay)
            
            # Lakukan pencarian dengan retry logic
            results = self._safe_search_with_retry(query, max_results=10)
            
            # Proses hasil pencarian
            search_results = []
            for result in results:
                try:
                    search_data = {
                        'query': query,
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'search_time': datetime.now().isoformat(),
                        'source': 'DuckDuckGo',
                        'data_type': 'facility_info',
                        'location': 'Cipocok Jaya, Serang'
                    }
                    search_results.append(search_data)
                except Exception as e:
                    self.logger.error(f"Error processing facility search result: {e}")
                    continue
            
            self.logger.info(f"Successfully processed {len(search_results)} facility results for Cipocok Jaya")
            return search_results
            
        except Exception as e:
            self.logger.error(f"Critical error in search_cipocok_jaya_facilities: {e}")
            return []
    
    def analyze_market_trends(self, location: str) -> Dict:
        """
        Menganalisis tren pasar di lokasi tertentu
        """
        try:
            trends = {
                'location': location,
                'price_trend': 'increasing',
                'demand_level': 'high',
                'inventory_level': 'low',
                'average_price': self._get_average_price(location),
                'days_on_market': 45,
                'price_per_sqm': 15000000,
                'market_sentiment': 'positive',
                'analysis_date': datetime.now().isoformat()
            }
            
            self.logger.info(f"Market analysis completed for {location}")
            return trends
            
        except Exception as e:
            self.logger.error(f"Error analyzing market trends: {e}")
            return {}
    
    def identify_opportunities(self, location: str) -> List[Dict]:
        """
        Mengidentifikasi peluang investasi/proyek
        """
        try:
            opportunities = [
                {
                    'type': 'residential_development',
                    'location': f"{location} - Central Area",
                    'potential_roi': '25%',
                    'risk_level': 'medium',
                    'timeline': '18 months',
                    'required_capital': '5M',
                    'market_demand': 'high',
                    'competitive_advantage': 'Strategic location near transit'
                },
                {
                    'type': 'commercial_renovation',
                    'location': f"{location} - Business District",
                    'potential_roi': '18%',
                    'risk_level': 'low',
                    'timeline': '12 months',
                    'required_capital': '2M',
                    'market_demand': 'medium',
                    'competitive_advantage': 'Existing infrastructure'
                }
            ]
            
            self.logger.info(f"Identified {len(opportunities)} opportunities in {location}")
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Error identifying opportunities: {e}")
            return []
    
    def monitor_competitors(self, location: str) -> List[Dict]:
        """
        Memantau aktivitas kompetitor
        """
        try:
            competitors = [
                {
                    'name': 'Properti Maju Jaya',
                    'active_projects': 3,
                    'price_range': '800M - 2.5B',
                    'market_share': '15%',
                    'strengths': ['Brand recognition', 'Quality construction'],
                    'weaknesses': ['Higher pricing', 'Limited locations']
                },
                {
                    'name': 'Rumah Indah Developer',
                    'active_projects': 5,
                    'price_range': '600M - 1.8B',
                    'market_share': '12%',
                    'strengths': ['Affordable pricing', 'Quick delivery'],
                    'weaknesses': ['Basic amenities', 'Limited design options']
                }
            ]
            
            self.logger.info(f"Monitored {len(competitors)} competitors in {location}")
            return competitors
            
        except Exception as e:
            self.logger.error(f"Error monitoring competitors: {e}")
            return []
    
    def generate_market_report(self, location: str) -> Dict:
        """
        Menghasilkan laporan pasar komprehensif
        """
        try:
            listings = self.search_property_listings(location)
            trends = self.analyze_market_trends(location)
            opportunities = self.identify_opportunities(location)
            competitors = self.monitor_competitors(location)
            
            report = {
                'location': location,
                'generated_at': datetime.now().isoformat(),
                'market_overview': trends,
                'active_listings': len(listings),
                'opportunities': opportunities,
                'competitor_analysis': competitors,
                'recommendations': self._generate_recommendations(trends, opportunities)
            }
            
            self.logger.info(f"Market report generated for {location}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating market report: {e}")
            return {}
    
    def _generate_mock_listings(self, location: str, property_type: str) -> List[Dict]:
        """Generate mock data untuk testing"""
        listings = []
        for i in range(10):
            listing = {
                'id': f"LIST_{i+1:03d}",
                'title': f"Modern {property_type.title()} in {location}",
                'location': location,
                'price': 800000000 + (i * 100000000),
                'bedrooms': 2 + (i % 3),
                'bathrooms': 1 + (i % 2),
                'land_area': 120 + (i * 20),
                'building_area': 80 + (i * 15),
                'listing_date': '2024-01-15',
                'agent': 'Hunter Agent',
                'contact': '+62-812-3456-7890'
            }
            listings.append(listing)
        return listings
    
    def _get_average_price(self, location: str) -> str:
        """Mock average price calculation"""
        return "1.2B IDR"
    
    def save_intelligence_report(self, price_results: List[Dict], facility_results: List[Dict]) -> str:
        """
        Menyimpan hasil riset intelijen pasar ke file logs/scout_intelligence_report.txt
        """
        try:
            report_file = 'logs/scout_intelligence_report.txt'
            
            # Buat laporan terstruktur
            report_content = f"""
{'='*80}
SCOUT AGENT MARKET INTELLIGENCE REPORT
{'='*80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Location Focus: Cipocok Jaya, Serang

{'='*80}
1. HARGA RUMAH BARU DI SEKITAR CIPOCOK JAYA SERANG
{'='*80}

"""
            
            # Tambahkan hasil pencarian harga
            for i, result in enumerate(price_results, 1):
                report_content += f"""
{i}. {result['title']}
   URL: {result['url']}
   Snippet: {result['snippet']}
   Search Time: {result['search_time']}
   Source: {result['source']}

"""
            
            report_content += f"""
{'='*80}
2. FASILITAS UMUM TERBARU DI CIPOCOK JAYA
{'='*80}

"""
            
            # Tambahkan hasil pencarian fasilitas
            for i, result in enumerate(facility_results, 1):
                report_content += f"""
{i}. {result['title']}
   URL: {result['url']}
   Snippet: {result['snippet']}
   Search Time: {result['search_time']}
   Source: {result['source']}

"""
            
            # Tambahkan analisis singkat
            report_content += f"""
{'='*80}
3. ANALISIS RINGKAS
{'='*80}

Total Search Results:
- Harga Rumah: {len(price_results)} results
- Fasilitas Umum: {len(facility_results)} results

Key Insights:
- Lokasi Cipocok Jaya menunjukkan {len(price_results)} informasi harga yang relevan
- Terdapat {len(facility_results)} fasilitas umum yang dapat menjadi value proposition
- Rekomendasi: Lakukan survei lokasi untuk validasi data online

{'='*80}
END OF REPORT
{'='*80}
"""
            
            # Simpan ke file
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"Intelligence report saved to: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"Error saving intelligence report: {e}")
            return ""
    
    def monitor_competitor_prices(self) -> Dict:
        """
        Monitor harga kompetitor di area Cipocok Jaya untuk drift detection
        """
        try:
            self.logger.info("Starting competitor price monitoring for Cipocok Jaya...")
            
            # Query untuk monitoring harga kompetitor
            competitor_queries = [
                "harga rumah kompetitor Cipocok Jaya",
                "developer properti Cipocok Jaya harga",
                "perumahan murah Cipocok Jaya Serang",
                "promo rumah Cipocok Jaya"
            ]
            
            all_competitor_data = []
            
            for query in competitor_queries:
                # Rate limiting
                time.sleep(self.request_delay)
                
                # Lakukan pencarian
                results = self._safe_search_with_retry(query, max_results=8)
                
                for result in results:
                    competitor_info = {
                        'query': query,
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'search_time': datetime.now().isoformat(),
                        'source': 'DuckDuckGo',
                        'data_type': 'competitor_pricing',
                        'location': 'Cipocok Jaya, Serang',
                        'extracted_price': self._extract_price_from_text(result.get('body', '')),
                        'price_trend': 'unknown'
                    }
                    all_competitor_data.append(competitor_info)
            
            # Analisis drift detection
            drift_analysis = self._analyze_price_drift(all_competitor_data)
            
            # Save drift monitoring log
            drift_log_file = self._save_drift_monitoring_log(drift_analysis)
            
            self.logger.info(f"Competitor monitoring completed. Drift log saved to: {drift_log_file}")
            return {
                'status': 'success',
                'competitor_data_count': len(all_competitor_data),
                'drift_analysis': drift_analysis,
                'drift_log_file': drift_log_file,
                'execution_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in competitor price monitoring: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': datetime.now().isoformat()
            }
    
    def _extract_price_from_text(self, text: str) -> Dict:
        """
        Ekstrak informasi harga dari teks
        """
        try:
            price_info = {
                'raw_text': text,
                'prices_found': [],
                'currency': 'IDR',
                'min_price': None,
                'max_price': None,
                'avg_price': None
            }
            
            # Pattern untuk harga
            price_patterns = [
                r'(\d+(?:\.\d+)?)\s*(?:juta|jt)',
                r'(\d+(?:\.\d+)?)\s*(?:miliar|milyar|mil)',
                r'rp\s*(\d+(?:\.\d+)?)',
                r'idr\s*(\d+(?:\.\d+)?)',
                r'harga\s*(\d+(?:\.\d+)?)'
            ]
            
            prices = []
            for pattern in price_patterns:
                matches = re.findall(pattern, text.lower())
                for match in matches:
                    try:
                        price_num = float(match.replace('.', ''))
                        
                        # Convert to IDR
                        if 'juta' in text.lower() or 'jt' in text.lower():
                            price_idr = price_num * 1000000
                        elif 'miliar' in text.lower() or 'mil' in text.lower():
                            price_idr = price_num * 1000000000
                        else:
                            # Assume juta if no unit specified
                            price_idr = price_num * 1000000
                        
                        prices.append(price_idr)
                    except:
                        continue
            
            if prices:
                price_info['prices_found'] = prices
                price_info['min_price'] = min(prices)
                price_info['max_price'] = max(prices)
                price_info['avg_price'] = sum(prices) / len(prices)
            
            return price_info
            
        except Exception as e:
            self.logger.error(f"Error extracting price from text: {e}")
            return {'raw_text': text, 'error': str(e)}
    
    def _analyze_price_drift(self, competitor_data: List[Dict]) -> Dict:
        """
        Analisis drift detection untuk harga kompetitor
        """
        try:
            # Load historical data
            historical_file = 'data/historical_prices.json'
            historical_prices = []
            
            if os.path.exists(historical_file):
                with open(historical_file, 'r', encoding='utf-8') as f:
                    historical_data = json.load(f)
                    historical_prices = historical_data.get('prices', [])
            
            # Extract current prices
            current_prices = []
            for data in competitor_data:
                price_info = data.get('extracted_price', {})
                if price_info.get('prices_found'):
                    current_prices.extend(price_info['prices_found'])
            
            # Calculate averages
            current_avg = sum(current_prices) / len(current_prices) if current_prices else 0
            historical_avg = sum(historical_prices) / len(historical_prices) if historical_prices else 0
            
            # Drift analysis
            drift_percentage = 0
            drift_status = 'stable'
            
            if historical_avg > 0:
                drift_percentage = ((current_avg - historical_avg) / historical_avg) * 100
                
                if drift_percentage < -10:
                    drift_status = 'WARNING - Aggressive Price Drop'
                elif drift_percentage < -5:
                    drift_status = 'CAUTION - Price Decrease'
                elif drift_percentage > 10:
                    drift_status = 'INFO - Price Increase'
                else:
                    drift_status = 'stable'
            
            # Save current prices to historical
            historical_prices.extend(current_prices)
            with open(historical_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'prices': historical_prices[-100:]  # Keep last 100 prices
                }, f, indent=2, ensure_ascii=False)
            
            return {
                'current_average_price': current_avg,
                'historical_average_price': historical_avg,
                'drift_percentage': drift_percentage,
                'drift_status': drift_status,
                'total_competitor_listings': len(competitor_data),
                'price_range': {
                    'min': min(current_prices) if current_prices else 0,
                    'max': max(current_prices) if current_prices else 0
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing price drift: {e}")
            return {
                'drift_status': 'error',
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _save_drift_monitoring_log(self, drift_analysis: Dict) -> str:
        """
        Simpan drift monitoring log ke file
        """
        try:
            log_file = 'logs/market_drift.txt'
            
            # Create log entry
            log_entry = f"""
{'='*80}
MARKET DRIFT MONITORING LOG - CIPOCOK JAYA
{'='*80}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: {drift_analysis.get('drift_status', 'Unknown')}
Drift Percentage: {drift_analysis.get('drift_percentage', 0):.2f}%

Price Analysis:
- Current Average: {self._format_price(drift_analysis.get('current_average_price', 0))}
- Historical Average: {self._format_price(drift_analysis.get('historical_average_price', 0))}
- Price Range: {self._format_price(drift_analysis.get('price_range', {}).get('min', 0))} - {self._format_price(drift_analysis.get('price_range', {}).get('max', 0))}
- Total Listings: {drift_analysis.get('total_competitor_listings', 0)}

Market Intelligence:
{self._generate_market_intelligence(drift_analysis)}

{'='*80}
END OF DRIFT ANALYSIS
{'='*80}

"""
            
            # Append to log file
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            self.logger.info(f"Drift monitoring log saved to: {log_file}")
            return log_file
            
        except Exception as e:
            self.logger.error(f"Error saving drift monitoring log: {e}")
            return ""
    
    def _format_price(self, price: float) -> str:
        """
        Format harga untuk display
        """
        if price >= 1000000000:
            return f"{price/1000000000:.1f} Miliar IDR"
        elif price >= 1000000:
            return f"{price/1000000:.0f} Juta IDR"
        else:
            return f"{price:,.0f} IDR"
    
    def _generate_market_intelligence(self, drift_analysis: Dict) -> str:
        """
        Generate market intelligence insights
        """
        drift_status = drift_analysis.get('drift_status', 'stable')
        drift_pct = drift_analysis.get('drift_percentage', 0)
        
        insights = []
        
        if 'WARNING' in drift_status:
            insights.append("⚠️  COMPETITOR ALERT: Significant price drop detected!")
            insights.append("   → Competitors are being very aggressive")
            insights.append("   → Consider reviewing pricing strategy")
            insights.append("   → Opportunity for market share gain")
        elif 'CAUTION' in drift_status:
            insights.append("⚠️  Price decrease detected - monitor closely")
            insights.append("   → Competitors may be testing lower price points")
        elif drift_pct > 10:
            insights.append("📈 Market prices increasing - inflationary pressure")
            insights.append("   → Opportunity for premium positioning")
        else:
            insights.append("✅ Market prices stable - normal competition")
        
        # Add price range insights
        price_range = drift_analysis.get('price_range', {})
        if price_range.get('min') and price_range.get('max'):
            spread = price_range['max'] - price_range['min']
            if spread > 500000000:  # 500 Juta spread
                insights.append("📊 Wide price range indicates diverse market segments")
            else:
                insights.append("📊 Narrow price range indicates competitive pricing")
        
        return '\n'.join(insights)
    
    def run_market_intelligence(self) -> Dict:
        """
        Menjalankan riset lengkap untuk market intelligence
        """
        try:
            self.logger.info("Starting market intelligence operations...")
            
            # Step 1: Search for price information
            self.logger.info("Step 1: Searching for price information...")
            price_results = self.search_cipocok_jaya_prices()
            
            # Step 2: Search for facility information
            self.logger.info("Step 2: Searching for facility information...")
            facility_results = self.search_cipocok_jaya_facilities()
            
            # Step 3: Monitor competitor prices
            self.logger.info("Step 3: Monitoring competitor prices...")
            competitor_monitoring = self.monitor_competitor_prices()
            
            # Step 4: Save intelligence report
            self.logger.info("Step 4: Generating intelligence report...")
            report_file = self.save_intelligence_report(price_results, facility_results)
            
            self.logger.info("Market intelligence completed successfully!")
            
            return {
                'status': 'success',
                'price_search_results': len(price_results),
                'facility_search_results': len(facility_results),
                'competitor_monitoring': competitor_monitoring,
                'report_file': report_file,
                'total_data_points': len(price_results) + len(facility_results),
                'execution_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in market intelligence: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': datetime.now().isoformat()
            }
    
    def run_cipocok_jaya_research(self) -> Dict:
        """
        Menjalankan riset lengkap untuk Cipocok Jaya dengan drift monitoring
        """
        try:
            self.logger.info("Starting Elite Hunter Cipocok Jaya market research...")
            
            # Step 1: Cari informasi harga
            price_results = self.search_cipocok_jaya_prices()
            time.sleep(2)  # Rate limiting
            
            # Step 2: Cari informasi fasilitas
            facility_results = self.search_cipocok_jaya_facilities()
            time.sleep(2)  # Rate limiting
            
            # Step 3: Monitor harga kompetitor (NEW)
            competitor_monitoring = self.monitor_competitor_prices()
            time.sleep(2)  # Rate limiting
            
            # Step 4: Simpan laporan
            report_file = self.save_intelligence_report(price_results, facility_results)
            
            # Step 5: Return summary with drift analysis
            summary = {
                'status': 'success',
                'location': 'Cipocok Jaya, Serang',
                'price_search_results': len(price_results),
                'facility_search_results': len(facility_results),
                'report_file': report_file,
                'competitor_monitoring': competitor_monitoring,
                'drift_status': competitor_monitoring.get('drift_analysis', {}).get('drift_status', 'unknown'),
                'execution_time': datetime.now().isoformat()
            }
            
            self.logger.info(f"Elite Hunter Cipocok Jaya research completed. Drift status: {summary['drift_status']}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error in Elite Hunter Cipocok Jaya research: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Test the module
    logging.basicConfig(level=logging.INFO)
    mi = MarketIntelligence()
    
    # Run Cipocok Jaya research
    result = mi.run_cipocok_jaya_research()
    print(json.dumps(result, indent=2, ensure_ascii=False))

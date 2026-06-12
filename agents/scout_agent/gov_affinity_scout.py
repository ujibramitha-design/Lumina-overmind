"""
Gov Affinity Scout Module
Advanced government office mapping dan PNS/P3K market analysis untuk property intelligence
"""

import json
import os
import requests
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI for PNS/P3K inference
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

class GovAffinityScout:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Google Places API configuration
        self.google_api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        self.base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        
        # Government office keywords untuk scanning
        self.gov_keywords = [
            'Dinas', 'Kementerian', 'Kantor Pemerintah', 'BAPPEDA', 
            'DPRD', 'Pengadilan', 'Kejaksaan', 'Kecamatan', 'Kantor Lurah',
            'Kantor Camat', 'Kantor Walikota', 'Pemerintah Kabupaten',
            'Kantor Bupati', 'Kantor Gubernur', 'Kanwil', 'Instansi'
        ]
        
        # Government office types untuk Places API
        self.gov_place_types = [
            'local_government_office',
            'city_hall',
            'courthouse',
            'police',
            'post_office',
            'fire_station',
            'embassy',
            'consulate'
        ]
        
        # Radius configuration
        self.scan_radius = 10000  # 10km radius
        self.density_radius = 2000  # 2km radius untuk density scoring
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
        
        # OpenAI configuration for PNS/P3K inference
        self.openai_client = None
        self.use_llm = False
        
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                self.use_llm = True
                self.logger.info("OpenAI client initialized for PNS/P3K inference")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
                self.use_llm = False
        else:
            self.logger.warning("OpenAI not available. Using traditional PNS/P3K analysis")
            self.use_llm = False
    
    def map_government_offices(self, location_coordinate: Tuple[float, float]) -> Dict:
        """
        Map government offices dalam radius 10km dari lokasi proyek
        Returns: Dict dengan government office data
        """
        try:
            lat, lng = location_coordinate
            self.logger.info(f"Mapping government offices around coordinates: {lat}, {lng}")
            
            if not self.google_api_key:
                self.logger.warning("Google Places API key not configured")
                return self._mock_government_offices(location_coordinate)
            
            all_gov_offices = []
            
            # Search untuk setiap keyword
            for keyword in self.gov_keywords:
                try:
                    # Search dengan keyword
                    params = {
                        'location': f'{lat},{lng}',
                        'radius': self.scan_radius,
                        'keyword': keyword,
                        'type': 'local_government_office',
                        'key': self.google_api_key,
                        'language': 'id'
                    }
                    
                    response = requests.get(self.base_url, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get('status') == 'OK':
                            for place in data.get('results', []):
                                # Calculate distance
                                place_lat = place.get('geometry', {}).get('location', {}).get('lat', 0)
                                place_lng = place.get('geometry', {}).get('location', {}).get('lng', 0)
                                distance = self._calculate_distance(lat, lng, place_lat, place_lng)
                                
                                gov_office = {
                                    'name': place.get('name', ''),
                                    'address': place.get('vicinity', ''),
                                    'location': {
                                        'lat': place_lat,
                                        'lng': place_lng
                                    },
                                    'distance_meters': distance,
                                    'distance_km': round(distance / 1000, 2),
                                    'types': place.get('types', []),
                                    'rating': place.get('rating', 0),
                                    'user_ratings_total': place.get('user_ratings_total', 0),
                                    'gov_category': self._classify_government_office(place),
                                    'keyword_found': keyword,
                                    'scan_timestamp': datetime.now().isoformat()
                                }
                                
                                all_gov_offices.append(gov_office)
                        else:
                            self.logger.warning(f"Google Places API error for keyword '{keyword}': {data.get('status')}")
                    else:
                        self.logger.error(f"HTTP error for keyword '{keyword}': {response.status_code}")
                
                except Exception as e:
                    self.logger.error(f"Error searching for keyword '{keyword}': {e}")
                    continue
            
            # Remove duplicates berdasarkan nama dan lokasi
            unique_offices = self._remove_duplicate_offices(all_gov_offices)
            
            # Sort by distance
            unique_offices.sort(key=lambda x: x['distance_meters'])
            
            # Save to data file
            self._save_government_offices(unique_offices, location_coordinate)
            
            result = {
                'status': 'success',
                'location_coordinate': location_coordinate,
                'scan_radius_km': self.scan_radius / 1000,
                'total_offices_found': len(unique_offices),
                'government_offices': unique_offices,
                'scan_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Government office mapping completed: {len(unique_offices)} offices found")
            return result
            
        except Exception as e:
            self.logger.error(f"Error mapping government offices: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_coordinate': location_coordinate
            }
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate distance between two coordinates in meters
        """
        try:
            # Haversine formula
            R = 6371000  # Earth's radius in meters
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lng = math.radians(lng2 - lng1)
            
            a = (math.sin(delta_lat / 2) ** 2 +
                 math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            distance = R * c
            return distance
            
        except Exception as e:
            self.logger.error(f"Error calculating distance: {e}")
            return 0
    
    def _classify_government_office(self, place: Dict) -> str:
        """
        Classify government office type
        """
        try:
            name = place.get('name', '').lower()
            types = place.get('types', [])
            
            # Classification logic
            if any(keyword in name for keyword in ['dinas', 'kementerian', 'instansi']):
                return 'Ministry/Department'
            elif any(keyword in name for keyword in ['bappeda', 'bpbd']):
                return 'Regional Planning'
            elif any(keyword in name for keyword in ['dprd', 'dewan perwakilan']):
                return 'Legislative'
            elif any(keyword in name for keyword in ['pengadilan', 'kejaksaan', 'kejaksaan negeri']):
                return 'Judicial'
            elif any(keyword in name for keyword in ['kecamatan', 'camat', 'lurah']):
                return 'Local Administration'
            elif any(keyword in name for keyword in ['walikota', 'bupati', 'gubernur']):
                return 'Executive'
            elif 'city_hall' in types:
                return 'City Hall'
            elif 'courthouse' in types:
                return 'Courthouse'
            elif 'police' in types:
                return 'Police'
            else:
                return 'Government Office'
                
        except Exception as e:
            self.logger.error(f"Error classifying government office: {e}")
            return 'Unknown'
    
    def _remove_duplicate_offices(self, offices: List[Dict]) -> List[Dict]:
        """
        Remove duplicate offices berdasarkan nama dan lokasi
        """
        try:
            unique_offices = []
            seen_offices = set()
            
            for office in offices:
                # Create unique identifier
                name = office.get('name', '').lower().strip()
                lat = office.get('location', {}).get('lat', 0)
                lng = office.get('location', {}).get('lng', 0)
                
                identifier = f"{name}_{lat}_{lng}"
                
                if identifier not in seen_offices:
                    seen_offices.add(identifier)
                    unique_offices.append(office)
            
            return unique_offices
            
        except Exception as e:
            self.logger.error(f"Error removing duplicate offices: {e}")
            return offices
    
    def _save_government_offices(self, offices: List[Dict], location_coordinate: Tuple[float, float]):
        """
        Save government offices data ke JSON file
        """
        try:
            data = {
                'location_coordinate': location_coordinate,
                'scan_radius_km': self.scan_radius / 1000,
                'scan_timestamp': datetime.now().isoformat(),
                'total_offices': len(offices),
                'government_offices': offices
            }
            
            filename = 'data/gov_hubs.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Government offices data saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving government offices data: {e}")
    
    def _mock_government_offices(self, location_coordinate: Tuple[float, float]) -> Dict:
        """
        Mock government offices data untuk testing
        """
        try:
            mock_offices = [
                {
                    'name': 'Dinas Perumahan Rakyak dan Kawasan Permukiman Kabupaten Serang',
                    'address': 'Jl. Ahmad Yani No. 1, Serang',
                    'location': {'lat': -6.1256, 'lng': 106.1445},
                    'distance_meters': 500,
                    'distance_km': 0.5,
                    'types': ['local_government_office'],
                    'rating': 4.2,
                    'user_ratings_total': 156,
                    'gov_category': 'Ministry/Department',
                    'keyword_found': 'Dinas',
                    'scan_timestamp': datetime.now().isoformat()
                },
                {
                    'name': 'Kantor Bupati Serang',
                    'address': 'Jl. Ahmad Yani No. 2, Serang',
                    'location': {'lat': -6.1260, 'lng': 106.1450},
                    'distance_meters': 800,
                    'distance_km': 0.8,
                    'types': ['local_government_office'],
                    'rating': 4.5,
                    'user_ratings_total': 89,
                    'gov_category': 'Executive',
                    'keyword_found': 'Kantor Pemerintah',
                    'scan_timestamp': datetime.now().isoformat()
                },
                {
                    'name': 'BAPPEDA Kabupaten Serang',
                    'address': 'Jl. KH. Abdul Hadi No. 45, Serang',
                    'location': {'lat': -6.1240, 'lng': 106.1430},
                    'distance_meters': 1200,
                    'distance_km': 1.2,
                    'types': ['local_government_office'],
                    'rating': 4.0,
                    'user_ratings_total': 67,
                    'gov_category': 'Regional Planning',
                    'keyword_found': 'BAPPEDA',
                    'scan_timestamp': datetime.now().isoformat()
                },
                {
                    'name': 'DPRD Kabupaten Serang',
                    'address': 'Jl. Raya Serang Km. 3, Serang',
                    'location': {'lat': -6.1270, 'lng': 106.1460},
                    'distance_meters': 1500,
                    'distance_km': 1.5,
                    'types': ['local_government_office'],
                    'rating': 3.8,
                    'user_ratings_total': 45,
                    'gov_category': 'Legislative',
                    'keyword_found': 'DPRD',
                    'scan_timestamp': datetime.now().isoformat()
                },
                {
                    'name': 'Kejaksaan Negeri Serang',
                    'address': 'Jl. Diponegoro No. 15, Serang',
                    'location': {'lat': -6.1230, 'lng': 106.1420},
                    'distance_meters': 1800,
                    'distance_km': 1.8,
                    'types': ['courthouse'],
                    'rating': 4.1,
                    'user_ratings_total': 78,
                    'gov_category': 'Judicial',
                    'keyword_found': 'Kejaksaan',
                    'scan_timestamp': datetime.now().isoformat()
                },
                {
                    'name': 'Kantor Camat Cipocok Jaya',
                    'address': 'Jl. Cipocok Jaya Raya No. 10, Serang',
                    'location': {'lat': -6.1280, 'lng': 106.1470},
                    'distance_meters': 2200,
                    'distance_km': 2.2,
                    'types': ['local_government_office'],
                    'rating': 3.5,
                    'user_ratings_total': 23,
                    'gov_category': 'Local Administration',
                    'keyword_found': 'Kecamatan',
                    'scan_timestamp': datetime.now().isoformat()
                }
            ]
            
            # Save mock data
            self._save_government_offices(mock_offices, location_coordinate)
            
            return {
                'status': 'success',
                'location_coordinate': location_coordinate,
                'scan_radius_km': self.scan_radius / 1000,
                'total_offices_found': len(mock_offices),
                'government_offices': mock_offices,
                'scan_timestamp': datetime.now().isoformat(),
                'note': 'Mock data used for demonstration'
            }
            
        except Exception as e:
            self.logger.error(f"Error creating mock government offices: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_coordinate': location_coordinate
            }
    
    def calculate_density_score(self, location_coordinate: Tuple[float, float]) -> Dict:
        """
        Calculate Professional Density Score untuk area sekitar lokasi proyek
        """
        try:
            lat, lng = location_coordinate
            
            # Load government offices data
            gov_data = self._load_government_offices()
            
            if not gov_data:
                self.logger.warning("No government offices data found")
                return {
                    'status': 'error',
                    'error': 'No government offices data available',
                    'density_score': 0,
                    'tier': 'Unknown'
                }
            
            offices = gov_data.get('government_offices', [])
            
            # Count offices within 2km radius
            offices_within_2km = [
                office for office in offices 
                if office.get('distance_meters', 0) <= self.density_radius
            ]
            
            # Calculate density score
            office_count_2km = len(offices_within_2km)
            
            # Scoring logic
            if office_count_2km >= 5:
                density_score = 10
                tier = 'Tier 1 Govt Hotspot'
            elif office_count_2km >= 3:
                density_score = 7
                tier = 'Tier 2 Govt Area'
            elif office_count_2km >= 1:
                density_score = 4
                tier = 'Tier 3 Govt Area'
            else:
                density_score = 1
                tier = 'Low Govt Presence'
            
            # Calculate category distribution
            category_distribution = {}
            for office in offices_within_2km:
                category = office.get('gov_category', 'Unknown')
                category_distribution[category] = category_distribution.get(category, 0) + 1
            
            result = {
                'status': 'success',
                'location_coordinate': location_coordinate,
                'density_radius_km': self.density_radius / 1000,
                'density_score': density_score,
                'tier': tier,
                'offices_within_2km': office_count_2km,
                'total_offices_within_10km': len(offices),
                'category_distribution': category_distribution,
                'assessment_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Density score calculated: {density_score}/10 ({tier})")
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating density score: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'density_score': 0,
                'tier': 'Unknown'
            }
    
    def _load_government_offices(self) -> Optional[Dict]:
        """
        Load government offices data dari JSON file
        """
        try:
            filename = 'data/gov_hubs.json'
            
            if not os.path.exists(filename):
                self.logger.warning(f"Government offices data file not found: {filename}")
                return None
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading government offices data: {e}")
            return None
    
    def estimate_market_potential(self, location_coordinate: Tuple[float, float]) -> Dict:
        """
        Estimate market potential untuk PNS/P3K target audience
        """
        try:
            # Get density score
            density_result = self.calculate_density_score(location_coordinate)
            
            if density_result.get('status') != 'success':
                return density_result
            
            density_score = density_result.get('density_score', 0)
            tier = density_result.get('tier', 'Unknown')
            
            # Determine market potential
            if tier == 'Tier 1 Govt Hotspot':
                market_potential = 'Very High'
                target_priority = 'PNS/P3K Priority'
                market_segment = 'Government Employees'
                confidence = 'High'
            elif tier == 'Tier 2 Govt Area':
                market_potential = 'High'
                target_priority = 'Secondary Target'
                market_segment = 'Mixed (Govt + Private)'
                confidence = 'Medium'
            elif tier == 'Tier 3 Govt Area':
                market_potential = 'Medium'
                target_priority = 'Tertiary Target'
                market_segment = 'General Market'
                confidence = 'Low'
            else:
                market_potential = 'Low'
                target_priority = 'Not Recommended'
                market_segment = 'General Market'
                confidence = 'Very Low'
            
            # Generate marketing profile dengan AI
            marketing_profile = self._generate_pns_marketing_profile(
                density_result, market_potential, tier
            )
            
            result = {
                'status': 'success',
                'location_coordinate': location_coordinate,
                'density_score': density_score,
                'tier': tier,
                'market_potential': market_potential,
                'target_priority': target_priority,
                'market_segment': market_segment,
                'confidence_level': confidence,
                'marketing_profile': marketing_profile,
                'assessment_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Market potential estimated: {market_potential} ({tier})")
            return result
            
        except Exception as e:
            self.logger.error(f"Error estimating market potential: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'market_potential': 'Unknown'
            }
    
    def _generate_pns_marketing_profile(self, density_result: Dict, market_potential: str, tier: str) -> Dict:
        """
        Generate marketing profile untuk PNS/P3K target audience
        """
        try:
            if not self.use_llm:
                return self._fallback_pns_marketing_profile(density_result, market_potential, tier)
            
            # Prepare context for LLM
            offices_within_2km = density_result.get('offices_within_2km', 0)
            category_distribution = density_result.get('category_distribution', {})
            
            prompt = f"""
            Buat profil marketing untuk proyek perumahan yang menarget PNS/P3K dengan informasi berikut:
            
            Lokasi: Density Score {density_result.get('density_score', 0)}/10 ({tier})
            Jumlah kantor pemerintahan dalam radius 2km: {offices_within_2km}
            Distribusi kategori: {category_distribution}
            Potensi pasar: {market_potential}
            
            Instruksi:
            1. Sesuaikan profil marketing untuk target PNS/P3K
            2. Fokus pada narasi cicilan stabil, dekat lokasi kerja, dan fasilitas investasi jangka panjang
            3. Berikan rekomendasi strategi marketing yang spesifik
            4. Sertakan key selling points yang relevan untuk PNS/P3K
            5. Tentukan channel marketing yang efektif
            
            Return dalam format JSON:
            {{
                "target_audience": "PNS/P3K Priority",
                "key_selling_points": ["point 1", "point 2", "point 3"],
                "marketing_narrative": "narrative marketing yang sesuai",
                "recommended_channels": ["channel 1", "channel 2"],
                "pricing_strategy": "strategi harga",
                "investment_benefits": ["benefit 1", "benefit 2"],
                "risk_factors": ["risk 1", "risk 2"],
                "success_metrics": ["metric 1", "metric 2"]
            }}
            """
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a marketing expert specializing in Indonesian property development for government employees (PNS/P3K). Create detailed marketing profiles with actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse LLM response
            llm_response = response.choices[0].message.content.strip()
            
            try:
                if llm_response.startswith('```json'):
                    llm_response = llm_response.replace('```json', '').replace('```', '').strip()
                
                marketing_profile = json.loads(llm_response)
                
                self.logger.info("LLM-generated PNS marketing profile created")
                return marketing_profile
                
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse LLM marketing profile response")
                return self._fallback_pns_marketing_profile(density_result, market_potential, tier)
                
        except Exception as e:
            self.logger.error(f"Error generating LLM marketing profile: {e}")
            return self._fallback_pns_marketing_profile(density_result, market_potential, tier)
    
    def _fallback_pns_marketing_profile(self, density_result: Dict, market_potential: str, tier: str) -> Dict:
        """
        Fallback marketing profile tanpa LLM
        """
        try:
            offices_count = density_result.get('offices_within_2km', 0)
            
            # Base profile
            profile = {
                'target_audience': 'PNS/P3K Priority' if tier == 'Tier 1 Govt Hotspot' else 'Secondary Target',
                'key_selling_points': [
                    'Lokasi strategis dekat kantor pemerintahan',
                    'Akses mudah ke fasilitas publik',
                    'Investasi jangka panjang yang stabil'
                ],
                'marketing_narrative': 'Hunian ideal untuk aparatur negara dengan cicilan yang terjangkau dan lokasi yang mendukung karir',
                'recommended_channels': ['Kerjasama dengan instansi', 'Word of mouth', 'Local marketing'],
                'pricing_strategy': 'Cicilan KPR yang disesuaikan dengan gaji PNS',
                'investment_benefits': ['Nilai properti yang stabil', 'Potensi capital gain', 'Kenyamanan jangka panjang'],
                'risk_factors': ['Regulasi perubahan zona', 'Fluktuasi pasar properti'],
                'success_metrics': ['Tingkat hunian', 'Kepuasan pembeli', 'Waktu penjualan']
            }
            
            # Adjust based on tier
            if tier == 'Tier 1 Govt Hotspot':
                profile['key_selling_points'].extend([
                    'Dikelilingi oleh 5+ kantor pemerintahan dalam radius 2km',
                    'Ekosistem bisnis yang matang'
                ])
                profile['recommended_channels'].extend([
                    'Direct marketing ke kantor pemerintahan',
                    'Program KPR khusus PNS'
                ])
            elif tier == 'Low Govt Presence':
                profile['key_selling_points'] = [
                    'Lokasi yang berkembang',
                    'Potensi pertumbuhan area',
                    'Harga yang lebih terjangkau'
                ]
                profile['marketing_narrative'] = 'Hunian dengan potensi investasi jangka panjang di area yang sedang berkembang'
            
            return profile
            
        except Exception as e:
            self.logger.error(f"Error creating fallback marketing profile: {e}")
            return {
                'target_audience': 'General Market',
                'key_selling_points': ['Lokasi strategis'],
                'marketing_narrative': 'Hunian ideal untuk keluarga Indonesia',
                'recommended_channels': ['Online marketing'],
                'pricing_strategy': 'Cicilan KPR standar',
                'investment_benefits': ['Nilai properti'],
                'risk_factors': ['Risiko pasar'],
                'success_metrics': ['Penjualan']
            }
    
    def generate_market_intelligence_report(self, location_coordinate: Tuple[float, float]) -> Dict:
        """
        Generate comprehensive market intelligence report
        """
        try:
            self.logger.info("Generating comprehensive market intelligence report...")
            
            # Step 1: Map government offices
            gov_mapping = self.map_government_offices(location_coordinate)
            
            # Step 2: Calculate density score
            density_score = self.calculate_density_score(location_coordinate)
            
            # Step 3: Estimate market potential
            market_potential = self.estimate_market_potential(location_coordinate)
            
            # Step 4: Generate visual report
            visual_report = self._generate_visual_report(gov_mapping, density_score, market_potential)
            
            # Step 5: Save comprehensive report
            comprehensive_report = {
                'location_coordinate': location_coordinate,
                'government_mapping': gov_mapping,
                'density_analysis': density_score,
                'market_potential': market_potential,
                'visual_report': visual_report,
                'report_timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
            # Save to file
            self._save_comprehensive_report(comprehensive_report)
            
            return comprehensive_report
            
        except Exception as e:
            self.logger.error(f"Error generating market intelligence report: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_coordinate': location_coordinate
            }
    
    def _generate_visual_report(self, gov_mapping: Dict, density_score: Dict, market_potential: Dict) -> str:
        """
        Generate visual report dalam format markdown
        """
        try:
            report = []
            
            # Header
            report.append("# GOVERNMENT AFFINITY MARKET INTELLIGENCE REPORT")
            report.append("=" * 60)
            report.append("")
            
            # Location info
            coord = gov_mapping.get('location_coordinate', (0, 0))
            report.append(f"**Location Coordinates:** {coord[0]}, {coord[1]}")
            report.append(f"**Scan Radius:** {gov_mapping.get('scan_radius_km', 0)} km")
            report.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")
            
            # Summary
            report.append("## EXECUTIVE SUMMARY")
            report.append("")
            tier = market_potential.get('tier', 'Unknown')
            potential = market_potential.get('market_potential', 'Unknown')
            report.append(f"- **Area Classification:** {tier}")
            report.append(f"- **Market Potential:** {potential}")
            report.append(f"- **Density Score:** {density_score.get('density_score', 0)}/10")
            report.append(f"- **Target Priority:** {market_potential.get('target_priority', 'Unknown')}")
            report.append("")
            
            # Government offices table
            report.append("## GOVERNMENT OFFICES ANALYSIS")
            report.append("")
            report.append("| Nama Kantor Pemerintahan | Jarak dari Proyek | Potensi Impact | Kategori | Rating |")
            report.append("|---|---|---|---|---|")
            
            offices = gov_mapping.get('government_offices', [])
            for office in offices[:10]:  # Show top 10
                name = office.get('name', 'Unknown')
                distance = office.get('distance_km', 0)
                impact = self._calculate_impact_score(office)
                category = office.get('gov_category', 'Unknown')
                rating = office.get('rating', 0)
                
                report.append(f"| {name} | {distance} km | {impact} | {category} | {rating} |")
            
            if len(offices) > 10:
                report.append(f"| ... dan {len(offices) - 10} lainnya | | | | | |")
            
            report.append("")
            
            # Density analysis
            report.append("## DENSITY ANALYSIS")
            report.append("")
            report.append(f"- **Offices within 2km:** {density_score.get('offices_within_2km', 0)}")
            report.append(f"- **Total offices within 10km:** {density_score.get('total_offices_within_10km', 0)}")
            report.append(f"- **Density Score:** {density_score.get('density_score', 0)}/10")
            report.append(f"- **Tier Classification:** {density_score.get('tier', 'Unknown')}")
            report.append("")
            
            # Category distribution
            category_dist = density_score.get('category_distribution', {})
            if category_dist:
                report.append("### Category Distribution")
                report.append("")
                for category, count in category_dist.items():
                    report.append(f"- **{category}:** {count} offices")
                report.append("")
            
            # Market potential
            report.append("## MARKET POTENTIAL ASSESSMENT")
            report.append("")
            report.append(f"- **Market Segment:** {market_potential.get('market_segment', 'Unknown')}")
            report.append(f"- **Confidence Level:** {market_potential.get('confidence_level', 'Unknown')}")
            report.append(f"- **Target Audience:** {market_potential.get('target_priority', 'Unknown')}")
            report.append("")
            
            # Marketing profile
            marketing_profile = market_potential.get('marketing_profile', {})
            if marketing_profile:
                report.append("## MARKETING STRATEGY")
                report.append("")
                
                key_points = marketing_profile.get('key_selling_points', [])
                if key_points:
                    report.append("### Key Selling Points")
                    for point in key_points:
                        report.append(f"- {point}")
                    report.append("")
                
                narrative = marketing_profile.get('marketing_narrative', '')
                if narrative:
                    report.append("### Marketing Narrative")
                    report.append(f"{narrative}")
                    report.append("")
                
                channels = marketing_profile.get('recommended_channels', [])
                if channels:
                    report.append("### Recommended Channels")
                    for channel in channels:
                        report.append(f"- {channel}")
                    report.append("")
            
            # Recommendations
            report.append("## STRATEGIC RECOMMENDATIONS")
            report.append("")
            
            recommendations = self._generate_strategic_recommendations(gov_mapping, density_score, market_potential)
            for i, rec in enumerate(recommendations, 1):
                report.append(f"{i}. {rec}")
            
            report.append("")
            report.append("=" * 60)
            report.append("*Report generated by Gov Affinity Scout System*")
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"Error generating visual report: {e}")
            return f"Error generating report: {str(e)}"
    
    def _calculate_impact_score(self, office: Dict) -> str:
        """
        Calculate impact score untuk government office
        """
        try:
            distance = office.get('distance_meters', 0)
            category = office.get('gov_category', '')
            rating = office.get('rating', 0)
            
            # Impact logic
            if distance <= 1000:  # Within 1km
                if 'Executive' in category or 'Ministry/Department' in category:
                    return 'Very High'
                elif 'Legislative' in category or 'Judicial' in category:
                    return 'High'
                else:
                    return 'Medium'
            elif distance <= 2000:  # Within 2km
                if 'Executive' in category or 'Ministry/Department' in category:
                    return 'High'
                else:
                    return 'Medium'
            else:
                return 'Low'
                
        except Exception as e:
            self.logger.error(f"Error calculating impact score: {e}")
            return 'Unknown'
    
    def _generate_strategic_recommendations(self, gov_mapping: Dict, density_score: Dict, market_potential: Dict) -> List[str]:
        """
        Generate strategic recommendations
        """
        try:
            recommendations = []
            
            tier = density_score.get('tier', '')
            offices_count = density_score.get('offices_within_2km', 0)
            
            # Tier-based recommendations
            if tier == 'Tier 1 Govt Hotspot':
                recommendations.append("Fokus pada pengembangan hunian menengah ke atas (type 36-72) untuk PNS/P3K")
                recommendations.append("Jalin kerjasama dengan kantor pemerintahan untuk program KPR khusus")
                recommendations.append("Highlight aksesibilitas ke fasilitas publik dan lokasi kerja")
                recommendations.append("Tawarkan fasilitas investasi jangka panjang dan nilai properti stabil")
            elif tier == 'Tier 2 Govt Area':
                recommendations.append("Kembangkan hunian dengan harga yang kompetitif untuk berbagai segmen")
                recommendations.append("Manfaatkan keberadaan kantor pemerintahan sebagai value proposition")
                recommendations.append("Target baik PNS/P3K maupun masyarakat umum")
            elif tier == 'Tier 3 Govt Area':
                recommendations.append("Fokus pada hunian terjangkau untuk pasar luas")
                recommendations.append("Manfaatkan potensi pertumbuhan area yang didukung oleh infrastruktur pemerintah")
            else:
                recommendations.append("Evaluasi kembali lokasi atau fokus pada value proposition lain")
            
            # Category-based recommendations
            category_dist = density_score.get('category_distribution', {})
            if 'Executive' in category_dist:
                recommendations.append("Tawarkan hunian premium dengan fasilitas mewah untuk pejabat tinggi")
            if 'Local Administration' in category_dist:
                recommendations.append("Kembangkan hunian yang ramah keluarga dengan fasilitas pendidikan")
            if 'Judicial' in category_dist:
                recommendations.append("Emphasize keamanan dan ketenangan area")
            
            return recommendations[:5]  # Top 5 recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating strategic recommendations: {e}")
            return ["Error generating recommendations"]
    
    def _save_comprehensive_report(self, report: Dict):
        """
        Save comprehensive report ke file
        """
        try:
            filename = f"reports/market_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Also save markdown report
            md_filename = 'reports/market_intelligence.md'
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(report.get('visual_report', 'No visual report available'))
            
            self.logger.info(f"Comprehensive report saved to {filename} and {md_filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving comprehensive report: {e}")

# Global Gov Affinity Scout instance
gov_affinity_scout = GovAffinityScout()

# Convenience functions
def map_government_offices(location_coordinate: Tuple[float, float]) -> Dict:
    """Map government offices around location"""
    return gov_affinity_scout.map_government_offices(location_coordinate)

def calculate_density_score(location_coordinate: Tuple[float, float]) -> Dict:
    """Calculate density score for area"""
    return gov_affinity_scout.calculate_density_score(location_coordinate)

def estimate_market_potential(location_coordinate: Tuple[float, float]) -> Dict:
    """Estimate market potential for PNS/P3K"""
    return gov_affinity_scout.estimate_market_potential(location_coordinate)

def generate_market_intelligence(location_coordinate: Tuple[float, float]) -> Dict:
    """Generate comprehensive market intelligence report"""
    return gov_affinity_scout.generate_market_intelligence_report(location_coordinate)

if __name__ == "__main__":
    # Test Gov Affinity Scout
    logging.basicConfig(level=logging.INFO)
    
    print("=== Gov Affinity Scout Test ===")
    
    # Test with Serang coordinates
    test_coordinates = (-6.1256, 106.1445)  # Cipocok Jaya, Serang
    
    print(f"Testing with coordinates: {test_coordinates}")
    
    # Test government office mapping
    gov_result = map_government_offices(test_coordinates)
    print(f"Government offices mapped: {gov_result.get('total_offices_found', 0)}")
    
    # Test density scoring
    density_result = calculate_density_score(test_coordinates)
    print(f"Density score: {density_result.get('density_score', 0)}/10")
    print(f"Tier: {density_result.get('tier', 'Unknown')}")
    
    # Test market potential
    market_result = estimate_market_potential(test_coordinates)
    print(f"Market potential: {market_result.get('market_potential', 'Unknown')}")
    print(f"Target priority: {market_result.get('target_priority', 'Unknown')}")
    
    # Test comprehensive report
    comprehensive_result = generate_market_intelligence(test_coordinates)
    print(f"Comprehensive report status: {comprehensive_result.get('status', 'Unknown')}")
    
    print("\nGov Affinity Scout test completed!")

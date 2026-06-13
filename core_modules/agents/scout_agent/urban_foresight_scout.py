"""
Urban Foresight Scout Module
Advanced infrastructure dan urban development analysis untuk 3-10 tahun ke depan
"""

import json
import os
import requests
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dotenv import load_dotenv

# Try to import OpenAI for LLM-powered analysis
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

class UrbanForesightScout:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs('data', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
        
        # Infrastructure crawler configuration
        self.infrastructure_sources = [
            {
                'name': 'Pemerintah Provinsi Banten',
                'url': 'https://pu.go.id',
                'query_patterns': ['rencana tol', 'rencana infrastruktur', 'pembangunan jalan', 'proyek infrastruktur']
            },
            {
                'name': 'PUPR Kota Serang',
                'url': 'https://pu.go.id',
                'query_patterns': ['rencana infrastruktur', 'pembangunan jalan', 'proyek infrastruktur', 'pengembangan']
            },
            {
                'name': 'Jasa Marga',
                'url': 'https://jurnalmassa.co.id',
                'query_patterns': ['kawasan industri', 'rencana industri', 'kawasan komersial', 'rencana bisnis']
            }
        ]
        
        # Zoning configuration
        self.zoning_types = {
            'residential': ['perumahan', 'cluster', 'griya', 'residence'],
            'commercial': ['mall', 'pusat belanja', 'supermarket', 'pasar', 'pertokoan'],
            'industrial': ['industri', 'pabrik', 'manufaktur', 'pabrik'],
            'infrastructure': ['jalan tol', 'jalan', 'jembatan', 'terminal', 'bandara']
        }
        
        # Targeting matrix configuration
        self.targeting_categories = {
            'pedagang': ['sekolah', 'tk', 'paud', 'pendidikan', 'universitas'],
            'wirausaha': ['ukm', 'usaha kecil', 'usaha menengah', 'startup', 'bisnis'],
            'retail': ['retail', 'minimarket', 'warung', 'kedai']
        }
        
        # Timeline configuration
        self.analysis_years = list(range(2024, 2035))  # 2024-2034 (11 years)
        
        # OpenAI configuration for LLM-powered analysis
        self.openai_client = None
        self.use_llm = False
        
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                self.use_llm = True
                self.logger.info("OpenAI client initialized for urban foresight analysis")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
                self.use_llm = False
        else:
            self.logger.warning("OpenAI not available. Using traditional analysis methods")
            self.use_llm = False
    
    def crawl_infrastructure_projects(self, location_name: str) -> Dict:
        """
        Crawl infrastructure projects dari portal berita pemerintah dan situs terkait
        """
        try:
            self.logger.info(f"Crawling infrastructure projects for {location_name}...")
            
            infrastructure_data = []
            
            for source in self.infrastructure_sources:
                try:
                    projects = self._crawl_source(source, location_name)
                    infrastructure_data.extend(projects)
                    
                    # Rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    self.logger.error(f"Error crawling {source['name']}: {e}")
                    continue
            
            # Save infrastructure data
            self._save_infrastructure_data(infrastructure_data, location_name)
            
            result = {
                'status': 'success',
                'location_name': location_name,
                'total_projects_found': len(infrastructure_data),
                'infrastructure_projects': infrastructure_data,
                'crawl_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Infrastructure crawling completed: {len(infrastructure_data)} projects found")
            return result
            
        except Exception as e:
            self.logger.error(f"Error crawling infrastructure projects: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_name': location_name
            }
    
    def _crawl_source(self, source: Dict, location_name: str) -> List[Dict]:
        """
        Crawl single source untuk infrastructure projects
        """
        try:
            projects = []
            
            for query_pattern in source['query_patterns']:
                try:
                    # Search query
                    search_url = f"{source['url']}/search?q={query_pattern} {location_name}"
                    
                    response = requests.get(search_url, timeout=30)
                    
                    if response.status_code == 200:
                        content = response.text
                        
                        # Extract project information using regex
                        project_matches = self._extract_project_info(content, query_pattern, location_name)
                        projects.extend(project_matches)
                    
                except Exception as e:
                    self.logger.error(f"Error searching {source['name']} with query '{query_pattern}': {e}")
                    continue
            
            return projects
            
        except Exception as e:
            self.logger.error(f"Error crawling source {source['name']}: {e}")
            return []
    
    def _extract_project_info(self, content: str, query_pattern: str, location_name: str) -> List[Dict]:
        """
        Extract project information dari web content
        """
        try:
            projects = []
            
            # Regex patterns untuk project extraction
            project_patterns = [
                rf'{query_pattern}.*?({location_name}.*?(\d+)[\s-]*(?:miliar|juta|triliun)\s+(?:juta|triliun))',
                rf'{query_pattern}.*?({location_name}.*?(?:dengan|untuk|untuk)\s+(\d+)[\s-]*(?:miliar|juta|triliun))',
                rf'proyek.*?({location_name})\s+estimasi\s+(\d+)\s+tahun',
                rf'proyek.*?({location_name})\s+selesai\s+(\d{4}\s+)',
                rf'proyek.*?({location_name})\s+dampak\s+(?:lokasi|area)\s+(?:strategis|dampak)',
                rf'proyek.*?({location_name})\s+tahun\s+target'
            ]
            
            for pattern in project_patterns:
                try:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    
                    for match in matches:
                        # Extract project details
                        project = self._parse_project_info(match, query_pattern, location_name)
                        if project:
                            projects.append(project)
                            
                except Exception as e:
                    self.logger.error(f"Error parsing project info: {e}")
                    continue
            
            return self._remove_duplicate_projects(projects)
            
        except Exception as e:
            self.logger.error(f"Error extracting project info: {e}")
            return []
    
    def _parse_project_info(self, match: tuple, query_pattern: str, location_name: str) -> Optional[Dict]:
        """
        Parse individual project information dari regex match
        """
        try:
            # Extract project name
            project_name = f"{query_pattern} {location_name}"
            
            # Extract details
            if len(match) >= 3:
                # Format: (query_pattern, location_name, cost, timeline, impact, location)
                cost = match[2] if len(match) > 2 else 'Unknown'
                timeline = match[3] if len(match) > 3 else 'Unknown'
                impact = match[4] if len(match) > 4 else 'Unknown'
                location = match[5] if len(match) > 5 else f"{location_name}"
                
                return {
                    'name': project_name,
                    'cost': cost,
                    'timeline': timeline,
                    'impact': impact,
                    'location': location,
                    'query_pattern': query_pattern,
                    'source': 'web_crawl',
                    'extracted_date': datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error parsing project info: {e}")
            return None
    
    def _remove_duplicate_projects(self, projects: List[Dict]) -> List[Dict]:
        """
        Remove duplicate projects berdasarkan nama dan lokasi
        """
        try:
            unique_projects = []
            seen_projects = set()
            
            for project in projects:
                # Create unique identifier
                name = project.get('name', '').lower().strip()
                location = project.get('location', '').lower().strip()
                cost = project.get('cost', '')
                
                identifier = f"{name}_{location}_{cost}"
                
                if identifier not in seen_projects:
                    seen_projects.add(identifier)
                    unique_projects.append(project)
            
            return unique_projects
            
        except Exception as e:
            self.logger.error(f"Error removing duplicate projects: {e}")
            return projects
    
    def scan_zoning_krk_documents(self, location_name: str) -> Dict:
        """
        Scan dokumen RTRW/RDTR untuk zoning dan KRK informasi
        """
        try:
            self.logger.info(f"Scanning Zoning & KRK documents for {location_name}...")
            
            zoning_data = []
            
            # Search untuk RTRW documents
            rtrw_results = self._search_documents('RTRW', location_name, '2024-2034')
            zoning_data.extend(rtrw_results)
            
            # Search untuk RDTR documents
            rdtr_results = self._search_documents('RDTR', location_name, '2024-2034')
            zoning_data.extend(rdtr_results)
            
            # Analyze documents dengan LLM
            analyzed_documents = self._analyze_zoning_documents(zoning_data)
            
            # Save zoning data
            self._save_zoning_data(zoning_data, location_name, analyzed_documents)
            
            result = {
                'status': 'success',
                'location_name': location_name,
                'total_documents_found': len(zoning_data),
                'rtrw_documents': len(rtrw_results),
                'rdtr_documents': len(rdtr_results),
                'analyzed_documents': analyzed_documents,
                'zoning_data': zoning_data,
                'scan_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Zoning & KRK scanning completed: {len(zoning_data)} documents found")
            return result
            
        except Exception as e:
            self.logger.error(f"Error scanning zoning documents: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_name': location_name
            }
    
    def _search_documents(self, doc_type: str, location_name: str, year_range: str) -> List[Dict]:
        """
        Search untuk dokumen tipe tertentu
        """
        try:
            # Mock implementation - dalam implementasi nyata, ini akan menggunakan web scraping
            mock_documents = []
            
            if doc_type == 'RTRW':
                mock_documents = [
                    {
                        'name': f'RTRW {location_name} 2024-2034',
                        'document_type': 'RTRW',
                        'url': f'https://example.com/rtrw-{location_name.lower().replace(' ', '-')}-2024.pdf',
                        'year_range': '2024-2034',
                        'location': location_name,
                        'extracted_date': datetime.now().isoformat()
                    },
                    {
                        'name': f'RTRW {location_name} 2025-2035',
                        'document_type': 'RTRW',
                        'url': f'https://example.com/rtrw-{location_name.lower().replace(' ', '-')}-2025.pdf',
                        'year_range': '2025-2035',
                        'location': location_name,
                        'extracted_date': datetime.now().isoformat()
                    }
                ]
            elif doc_type == 'RDTR':
                mock_documents = [
                    {
                        'name': f'RDTR {location_name} 2024-2034',
                        'document_type': 'RDTR',
                        'url': f'https://example.com/rdtr-{location_name.lower().replace(' ', '-')}-2024.pdf',
                        'year_range': '2024-2034',
                        'location': location_name,
                        'extracted_date': datetime.now().isoformat()
                    },
                    {
                        'name': f'RDTR {location_name} 2025-2035',
                        'document_type': 'RDTR',
                        'url': f'https://example.com/rdtr-{location_name.lower().replace(' ', '-')}-2025.pdf',
                        'year_range': '2025-2035',
                        'location': location_name,
                        'extracted_date': datetime.now().isoformat()
                    }
                ]
            
            return mock_documents
            
        except Exception as e:
            self.logger.error(f"Error searching {doc_type} documents: {e}")
            return []
    
    def _analyze_zoning_documents(self, documents: List[Dict]) -> Dict:
        """
        Analyze zoning documents dengan LLM
        """
        try:
            if not self.use_llm:
                return self._fallback_zoning_analysis(documents)
            
            analyzed_docs = []
            
            for doc in documents:
                try:
                    # Prepare content for LLM analysis
                    content = f"Document: {doc.get('name', '')}\n"
                    content += f"Type: {doc.get('document_type', '')}\n"
                    content += f"Location: {doc.get('location', '')}\n"
                    content += f"Year Range: {doc.get('year_range', '')}\n"
                    
                    # LLM analysis
                    prompt = f"""
                    Analisis dokumen perencanaan kawasan:
                    
                    {content}
                    
                    Instruksi:
                    1. Ekstrak informasi tentang 'rencana peruntukan kawasan komersial/perdagangan'
                    2. Identifikasi informasi tentang 'rencana perluasan kawasan industri'
                    3. Catat tahun target dan estimasi selesai
                    4. Identifikasi dampak lokasi terhadap area sekitarnya
                    
                    Return dalam format JSON:
                    {{
                        "zoning_type": "jenis zona",
                        "target_year": "tahun target",
                        "estimated_completion": "estimasi selesai",
                        "location_impact": "dampak lokasi",
                        "key_projects": ["proyek 1", "proyek 2"],
                        "strategic_importance": "significance"
                    }}
                    """
                    
                    # Call OpenAI API
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an urban planning expert. Analyze zoning documents and extract structured information about development plans and zoning strategies."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=300
                    )
                    
                    # Parse LLM response
                    llm_response = response.choices[0].message.content.strip()
                    
                    try:
                        if llm_response.startswith('```json'):
                            llm_response = llm_response.replace('```json', '').replace('```', '').strip()
                        
                        analysis_data = json.loads(llm_response)
                        
                        analyzed_doc = {
                            'document_name': doc.get('name', ''),
                            'zoning_type': analysis_data.get('zoning_type', 'Unknown'),
                            'target_year': analysis_data.get('target_year', 'Unknown'),
                            'estimated_completion': analysis_data.get('estimated_completion', 'Unknown'),
                            'location_impact': analysis_data.get('location_impact', 'Unknown'),
                            'key_projects': analysis_data.get('key_projects', []),
                            'strategic_importance': analysis_data.get('strategic_importance', 'Unknown'),
                            'llm_analysis': llm_response
                        }
                        
                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to parse LLM response for document {doc.get('name', 'Unknown')}")
                        analyzed_doc = self._fallback_zoning_analysis([doc])
                    
                    analyzed_docs.append(analyzed_doc)
                    
                except Exception as e:
                    self.logger.error(f"Error analyzing document {doc.get('name', 'Unknown')}: {e}")
                    analyzed_doc = self._fallback_zoning_analysis([doc])
                    analyzed_docs.append(analyzed_doc)
            
            return {
                'status': 'success',
                'total_documents': len(analyzed_docs),
                'zoning_analysis': analyzed_docs,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing zoning documents: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _fallback_zoning_analysis(self, documents: List[Dict]) -> Dict:
        """
        Fallback zoning analysis tanpa LLM
        """
        try:
            analyzed_docs = []
            
            for doc in documents:
                # Simple keyword-based analysis
                content = f"{doc.get('name', '')} {doc.get('document_type', '')} {doc.get('location', '')}"
                
                zoning_type = 'Unknown'
                target_year = 'Unknown'
                estimated_completion = 'Unknown'
                location_impact = 'Unknown'
                
                # Keyword-based classification
                content_lower = content.lower()
                if 'komersial' in content_lower or 'industri' in content_lower:
                    zoning_type = 'Commercial/Industrial'
                elif 'perumahan' in content_lower or 'cluster' in content_lower:
                    zoning_type = 'Residential'
                elif 'jalan' in content_lower or 'infrastruktur' in content_lower:
                    zoning_type = 'Infrastructure'
                
                # Extract year information
                year_match = re.search(r'(\d{4})', content)
                if year_match:
                    target_year = f"20{year_match.group(0)}s"
                
                # Extract timeline information
                if 'selesai' in content_lower:
                    estimated_completion = 'Completed'
                elif 'target' in content_lower:
                    estimated_completion = 'In Progress'
                
                analyzed_doc = {
                    'document_name': doc.get('name', ''),
                    'zoning_type': zoning_type,
                    'target_year': target_year,
                    'estimated_completion': estimated_completion,
                    'location_impact': location_impact,
                    'key_projects': [],
                    'strategic_importance': 'Medium',
                    'analysis_method': 'keyword_based'
                }
                
                analyzed_docs.append(analyzed_doc)
            
            return {
                'status': 'success',
                'total_documents': len(analyzed_docs),
                'zoning_analysis': analyzed_docs,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in fallback zoning analysis: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def analyze_targeting_matrix(self, location_name: str) -> Dict:
        """
        Analyze targeting matrix untuk pedagang dan wirausaha
        """
        try:
            self.logger.info(f"Analyzing targeting matrix for {location_name}...")
            
            # Load zoning data
            zoning_data = self._load_zoning_data(location_name)
            
            if not zoning_data:
                self.logger.warning(f"No zoning data found for {location_name}")
                return {
                    'status': 'error',
                    'error': 'No zoning data available',
                    'location_name': location_name
                }
            
            zoning_analysis = zoning_data.get('zoning_analysis', {})
            
            # Analyze targeting opportunities
            targeting_opportunities = self._analyze_targeting_opportunities(zoning_analysis, location_name)
            
            # Load infrastructure data
            infrastructure_data = self._load_infrastructure_data(location_name)
            
            result = {
                'status': 'success',
                'location_name': location_name,
                'zoning_analysis': zoning_analysis,
                'targeting_opportunities': targeting_opportunities,
                'infrastructure_projects': infrastructure_data,
                'targeting_matrix': {
                    'pedagang': self._analyze_pedagang_opportunities(zoning_analysis, infrastructure_data),
                    'wirausaha': self._analyze_wirausaha_opportunities(zoning_analysis, infrastructure_data),
                    'retail': self._analyze_retail_opportunities(zoning_analysis, infrastructure_data)
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Targeting matrix analysis completed for {location_name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing targeting matrix: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_name': location_name
            }
    
    def _load_zoning_data(self, location_name: str) -> Optional[Dict]:
        """
        Load zoning data dari file
        """
        try:
            filename = f'data/zoning_data_{location_name.lower().replace(' ', '_')}.json'
            
            if not os.path.exists(filename):
                self.logger.warning(f"Zoning data file not found: {filename}")
                return None
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading zoning data: {e}")
            return None
    
    def _load_infrastructure_data(self, location_name: str) -> Optional[Dict]:
        """
        Load infrastructure data dari file
        """
        try:
            filename = f'data/infrastructure_{location_name.lower().replace(' ', '_')}.json'
            
            if not os.path.exists(filename):
                self.logger.warning(f"Infrastructure data file not found: {filename}")
                return None
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading infrastructure data: {e}")
            return None
    
    def _analyze_targeting_opportunities(self, zoning_analysis: Dict, infrastructure_data: Dict) -> Dict:
        """
        Analyze targeting opportunities berdasarkan zoning dan infrastructure data
        """
        try:
            opportunities = {
                'pedagang': {
                    'opportunity_score': 0,
                    'key_locations': [],
                    'infrastructure_support': 0,
                    'market_size': 'Unknown'
                },
                'wirausaha': {
                    'opportunity_score': 0,
                    'industrial_clusters': [],
                    'retail_hubs': [],
                    'commercial_potential': 0
                },
                'retail': {
                    'opportunity_score': 0,
                    'retail_centers': [],
                    'commercial_density': 0,
                    'market_access': 0
                }
            }
            
            # Analyze zoning untuk targeting opportunities
            zoning_docs = zoning_analysis.get('zoning_analysis', [])
            
            for doc in zoning_docs:
                zoning_type = doc.get('zoning_type', 'Unknown')
                target_year = doc.get('target_year', 'Unknown')
                
                if zoning_type in ['Residential', 'Mixed']:
                    opportunities['pedagang']['opportunity_score'] += 2
                    opportunities['pedagang']['key_locations'].append(doc.get('document_name', ''))
                elif zoning_type in ['Commercial/Industrial']:
                    opportunities['wirausaha']['opportunity_score'] += 3
                    opportunities['wirausaha']['industrial_clusters'].append(doc.get('document_name', ''))
                elif 'Infrastructure' in zoning_type:
                    opportunities['pedagang']['infrastructure_support'] += 1
                    opportunities['wirausaha']['infrastructure_support'] += 1
            
            # Analyze infrastructure untuk retail opportunities
            for project in infrastructure_data.get('infrastructure_projects', []):
                project_type = project.get('name', '').lower()
                
                if 'mall' in project_type or 'supermarket' in project_type:
                    opportunities['retail']['opportunity_score'] += 2
                    opportunities['retail']['retail_centers'].append(project.get('name', ''))
                elif 'pasar' in project_type or 'pertokoan' in project_type:
                    opportunities['retail']['opportunity_score'] += 1
                    opportunities['retail']['commercial_density'] += 1
            
            # Calculate market size estimates
            total_opportunity = sum(opportunities[key]['opportunity_score'] for key in opportunities)
            
            if total_opportunity > 0:
                if total_opportunity >= 8:
                    market_size = 'Large'
                elif total_opportunity >= 5:
                    market_size = 'Medium'
                else:
                    market_size = 'Small'
            else:
                market_size = 'Very Small'
            
            # Update market size in all categories
            for key in opportunities:
                if opportunities[key]['opportunity_score'] > 0:
                    opportunities[key]['market_size'] = market_size
            
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Error analyzing targeting opportunities: {e}")
            return {
                'pedagang': {'opportunity_score': 0, 'key_locations': [], 'infrastructure_support': 0, 'market_size': 'Unknown'},
                'wirausaha': {'opportunity_score': 0, 'industrial_clusters': [], 'retail_hubs': [], 'commercial_potential': 0},
                'retail': {'opportunity_score': 0, 'retail_centers': [], 'commercial_density': 0, 'market_access': 0}
            }
    
    def _analyze_pedagang_opportunities(self, zoning_analysis: Dict, infrastructure_data: Dict) -> Dict:
        """
        Analyze pedagang opportunities
        """
        try:
            pedagang_ops = {
                'opportunity_score': 0,
                'key_locations': [],
                'infrastructure_support': 0,
                'market_size': 'Unknown'
            }
            
            # Analyze zoning untuk pedagang opportunities
            zoning_docs = zoning_analysis.get('zoning_analysis', [])
            
            for doc in zoning_docs:
                zoning_type = doc.get('zoning_type', 'Unknown')
                target_year = doc.get('target_year', 'Unknown')
                
                if zoning_type in ['Residential', 'Mixed']:
                    pedagang_ops['opportunity_score'] += 3
                    pedagang_ops['key_locations'].append(doc.get('document_name', ''))
                elif zoning_type in ['Commercial/Industrial']:
                    pedagang_ops['opportunity_score'] += 2
                    pedagang_ops['infrastructure_support'] += 1
            
            # Analyze infrastructure support
            for project in infrastructure_data.get('infrastructure_projects', []):
                project_type = project.get('name', '').lower()
                
                if 'jalan' in project_type or 'infrastruktur' in project_type:
                    pedagang_ops['infrastructure_support'] += 1
            
            # Calculate market size
            if pedagang_ops['opportunity_score'] >= 8:
                pedagang_ops['market_size'] = 'Large'
            elif pedagang_ops['opportunity_score'] >= 5:
                pedagang_ops['market_size'] = 'Medium'
            elif pedagang_ops['opportunity_score'] >= 3:
                pedagang_ops['market_size'] = 'Small'
            else:
                pedagang_ops['market_size'] = 'Very Small'
            
            return pedagang_ops
            
        except Exception as e:
            self.logger.error(f"Error analyzing pedagang opportunities: {e}")
            return {
                'opportunity_score': 0,
                'key_locations': [],
                'infrastructure_support': 0,
                'market_size': 'Unknown'
            }
    
    def _analyze_wirausaha_opportunities(self, zoning_analysis: Dict, infrastructure_data: Dict) -> Dict:
        """
        Analyze wirausaha opportunities
        """
        try:
            wirausaha_ops = {
                'opportunity_score': 0,
                'industrial_clusters': [],
                'retail_hubs': [],
                'commercial_potential': 0
            }
            
            # Analyze zoning untuk wirausaha opportunities
            zoning_docs = zoning_analysis.get('zoning_analysis', [])
            
            for doc in zoning_docs:
                zoning_type = doc.get('zoning_type', 'Unknown')
                target_year = doc.get('target_year', 'Unknown')
                
                if zoning_type in ['Commercial/Industrial']:
                    wirausaha_ops['opportunity_score'] += 4
                    wirausaha_ops['industrial_clusters'].append(doc.get('document_name', ''))
                elif 'Infrastructure' in zoning_type:
                    wirausaha_ops['infrastructure_support'] += 1
            
            # Analyze infrastructure untuk retail opportunities
            for project in infrastructure_data.get('infrastructure_projects', []):
                project_type = project.get('name', '').lower()
                
                if 'mall' in project_type or 'supermarket' in project_type:
                    wirausaha_ops['commercial_potential'] += 2
                    wirausaha_ops['retail_hubs'].append(project.get('name', ''))
            
            # Calculate market potential
            if wirausaha_ops['opportunity_score'] >= 8:
                wirausaha_ops['market_potential'] = 'High'
            elif wirausaha_ops['opportunity_score'] >= 5:
                wirausaha_ops['market_potential'] = 'Medium'
            elif wirausaha_ops['opportunity_score'] >= 3:
                wirausaha_ops['market_potential'] = 'Low'
            else:
                wirausaha_ops['market_potential'] = 'Very Low'
            
            return wirausaha_ops
            
        except Exception as e:
            self.logger.error(f"Error analyzing wirausaha opportunities: {e}")
            return {
                'opportunity_score': 0,
                'industrial_clusters': [],
                'retail_hubs': [],
                'commercial_potential': 0
            }
    
    def _analyze_retail_opportunities(self, zoning_analysis: Dict, infrastructure_data: Dict) -> Dict:
        """
        Analyze retail opportunities
        """
        try:
            retail_ops = {
                'opportunity_score': 0,
                'retail_centers': [],
                'commercial_density': 0,
                'market_access': 0
            }
            
            # Analyze zoning untuk retail opportunities
            zoning_docs = zoning_analysis.get('zoning_analysis', [])
            
            for doc in zoning_docs:
                zoning_type = doc.get('zoning_type', 'Unknown')
                
                if zoning_type in ['Commercial']:
                    retail_ops['opportunity_score'] += 2
                    retail_ops['retail_centers'].append(doc.get('document_name', 'name'))
                elif 'Residential' in zoning_type:
                    retail_ops['market_access'] += 1
            
            # Analyze infrastructure for retail support
            for project in infrastructure_data.get('infrastructure_projects', []):
                project_type = project.get('name', '').lower()
                
                if 'jalan' in project_type or 'infrastruktur' in project_type:
                    retail_ops['commercial_density'] += 1
            
            # Calculate market access
            if retail_ops['opportunity_score'] >= 8:
                retail_ops['market_access'] = 'High'
            elif retail_ops['opportunity_score'] >= 5:
                retail_ops['market_access'] = 'Medium'
            elif retail_ops['opportunity_score'] >= 3:
                retail_ops['market_access'] = 'Low'
            else:
                retail_ops['market_access'] = 'Very Low'
            
            return retail_ops
            
        except Exception as e:
            self.logger.error(f"Error analyzing retail opportunities: {e}")
            return {
                'opportunity_score': 0,
                'retail_centers': [],
                'commercial_density': 0,
                'market_access': 'Very Low'
            }
    
    def generate_future_map(self, location_coordinate: Tuple[float, float], location_name: str) -> Dict:
        """
        Generate comprehensive 10-year future map dengan semua data terkumpul
        """
        try:
            self.logger.info(f"Generating future map for {location_name} ({location_coordinate})...")
            
            # Step 1: Map infrastructure projects
            infrastructure_result = self.crawl_infrastructure_projects(location_name)
            
            # Step 2: Scan zoning documents
            zoning_result = self.scan_zoning_krk_documents(location_name)
            
            # Step 3: Analyze targeting matrix
            targeting_result = self.analyze_targeting_matrix(location_name)
            
            # Step 4: Generate timeline data
            timeline_data = self._generate_timeline_data(
                infrastructure_result, 
                zoning_result, 
                targeting_result, 
                location_name
            )
            
            # Step 5: Generate visual report
            visual_report = self._generate_visual_timeline_report(timeline_data, location_name)
            
            # Step 6: Save comprehensive report
            comprehensive_report = {
                'status': 'success',
                'location_coordinate': location_coordinate,
                'location_name': location_name,
                'analysis_years': self.analysis_years,
                'infrastructure_mapping': infrastructure_result,
                'zoning_analysis': zoning_result,
                'targeting_matrix': targeting_result,
                'timeline_data': timeline_data,
                'visual_report': visual_report,
                'report_timestamp': datetime.now().isoformat()
            }
            
            # Save to file
            self._save_comprehensive_report(comprehensive_report, location_name)
            
            return comprehensive_report
            
        except Exception as e:
            self.logger.error(f"Error generating future map: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'location_coordinate': location_coordinate,
                'location_name': location_name
            }
    
    def _generate_timeline_data(self, infrastructure_result: Dict, zoning_result: Dict, targeting_result: Dict, location_name: str) -> List[Dict]:
        """
        Generate timeline data untuk 10 tahun ke depan
        """
        try:
            timeline_data = []
            
            for year in self.analysis_years:
                # Infrastructure projects for this year
                year_infra = [
                    proj for proj in infrastructure_result.get('infrastructure_projects', [])
                    if any(f"{year}" in proj.get('timeline', '').lower())
                ]
                
                # Zoning analysis for this year
                year_zoning = [
                    doc for doc in zoning_result.get('zoning_analysis', [])
                    if any(f"{year}" in doc.get('target_year', '').lower())
                ]
                
                # Targeting opportunities for this year
                targeting = targeting_result.get('targeting_matrix', {})
                
                # Create timeline entry
                timeline_entry = {
                    'year': year,
                    'infrastructure_projects': year_infra,
                    'zoning_documents': year_zoning,
                    'targeting_opportunities': targeting,
                    'market_potential': self._calculate_market_potential(targeting)
                }
                
                timeline_data.append(timeline_entry)
            
            return timeline_data
            
        except Exception as e:
            self.logger.error(f"Error generating timeline data: {e}")
            return []
    
    def _calculate_market_potential(self, targeting_result: Dict) -> str:
        """
        Calculate overall market potential dari targeting matrix
        """
        try:
            pedagang_score = targeting_result.get('pedagang', {}).get('opportunity_score', 0)
            wirausaha_score = targeting_result.get('wirausaha', {}).get('opportunity_score', 0)
            retail_score = targeting_result.get('retail', {}).get('opportunity_score', 0)
            
            total_score = pedagang_score + wirausaha_score + retail_score
            
            if total_score >= 15:
                return 'Very High'
            elif total_score >= 10:
                return 'High'
            elif total_score >= 5:
                return 'Medium'
            else:
                return 'Low'
                
        except Exception as e:
            self.logger.error(f"Error calculating market potential: {e}")
            return 'Unknown'
    
    def _generate_visual_timeline_report(self, timeline_data: List[Dict], location_name: str) -> str:
        """
        Generate visual timeline report dalam format markdown
        """
        try:
            report = []
            
            # Header
            report.append(f"# URBAN FORESIGHT REPORT")
            report.append("=" * 60)
            report.append("")
            report.append(f"**Location:** {location_name}")
            report.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")
            
            # Timeline table
            report.append("## 10-YEAR DEVELOPMENT TIMELINE")
            report.append("")
            report.append("| Tahun | Proyek Infrastruktur | Zoning | Targeting Opportunities | Market Potential |")
            report.append("|---|---|---|---|---|---|")
            
            for entry in timeline_data:
                year = entry.get('year', 'Unknown')
                infra_count = len(entry.get('infrastructure_projects', []))
                zoning_count = len(entry.get('zoning_documents', []))
                targeting = entry.get('targeting_opportunities', {})
                
                pedagang_ops = targeting.get('pedagang', {})
                wirausaha_ops = targeting.get('wirausaha', {})
                retail_ops = targeting.get('retail', {})
                
                market_potential = self._calculate_market_potential(entry['targeting_opportunities'])
                
                report.append(f"| {year} | {infra_count} | {zoning_count} | {pedagang_ops['market_size']} | {market_potential} |")
            
            report.append("")
            
            # Strategic summary
            report.append("## STRATEGIC INSIGHTS")
            report.append("")
            
            # Future projections
            high_potential_years = [entry for entry in timeline_data if self._calculate_market_potential(entry['targeting_opportunities']) in ['Very High', 'High']]
            medium_potential_years = [entry for entry in timeline_data if self._calculate_market_potential(entry['targeting_opportunities']) in ['Medium']]
            
            report.append(f"**High Potential Years:** {len(high_potential_years)} ({', '.join(map(str, high_potential_years))})")
            report.append(f"**Medium Potential Years:** {len(medium_potential_years)} ({', '.join(map(str, medium_potential_years))}")
            
            report.append("")
            report.append("## KEY INFRASTRUCTURE PRIORITIES")
            report.append("")
            
            # Infrastructure priorities
            infra_priorities = {}
            for entry in timeline_data:
                for proj in entry.get('infrastructure_projects', []):
                    proj_name = proj.get('name', '')
                    project_type = proj.get('name', '').lower()
                    infra_priorities[project_type] = infra_priorities.get(project_type, 0) + 1
            
            if infra_priorities:
                report.append("### Infrastructure Priorities:")
                for project_type, count in sorted(infra_priorities.items(), key=lambda x: x[1], reverse=True):
                    report.append(f"- {project_type}: {count} projects")
            
            report.append("")
            report.append("## TARGETING MATRIX SUMMARY")
            report.append("")
            
            # Targeting matrix summary
            pedagang_size = targeting_result.get('pedagang', {}).get('market_size', 'Unknown')
            wirausaha_size = targeting_result.get('wirausaha', {}).get('market_size', 'Unknown')
            retail_size = targeting_result.get('retail', {}).get('market_size', 'Unknown')
            
            report.append(f"**Pedagang Market:** {pedagang_size}")
            report.append(f"**Wirausaha Market:** {wirausaha_size}")
            report.append(f"**Retail Market:** {retail_size}")
            
            report.append("")
            report.append("=" * 60)
            report.append("*Report generated by Urban Foresight Scout System*")
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"Error generating visual timeline report: {e}")
            return f"Error generating visual timeline report: {e}"
    
    def _save_comprehensive_report(self, report: Dict, location_name: str):
        """
        Save comprehensive future map report ke file
        """
        try:
            # Save JSON report
            json_filename = f"reports/urban_foresight_{location_name.lower().replace(' ', '_')}_comprehensive.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Save markdown report
            md_filename = f"reports/urban_foresight.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(report.get('visual_report', 'No visual report available'))
            
            self.logger.info(f"Comprehensive report saved to {json_filename} and {md_filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving comprehensive report: {e}")
    
    def _save_infrastructure_data(self, infrastructure_data: List[Dict], location_name: str):
        """
        Save infrastructure data ke file
        """
        try:
            data = {
                'location_name': location_name,
                'scan_timestamp': datetime.now().isoformat(),
                'total_projects': len(infrastructure_data),
                'infrastructure_projects': infrastructure_data
            }
            
            filename = f'data/infrastructure_{location_name.lower().replace(' ', '_')}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Infrastructure data saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving infrastructure data: {e}")
    
    def _save_zoning_data(self, zoning_data: Dict, location_name: str, analyzed_documents: Dict):
        """
        Save zoning data ke file
        """
        try:
            data = {
                'location_name': location_name,
                'scan_timestamp': datetime.now().isoformat(),
                'total_documents': len(zoning_data),
                'zoning_documents': zoning_data,
                'analyzed_documents': analyzed_documents
            }
            
            filename = f'data/zoning_{location_name.lower().replace(' ', '_')}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Zoning data saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving zoning data: {e}")
    
    def _save_comprehensive_report(self, report: Dict, location_name: str):
        """
        Save comprehensive report ke file
        """
        try:
            # Save JSON report
            json_filename = f"reports/urban_foresight_{location_name.lower().replace(' ', '_')}_comprehensive.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Comprehensive report saved to {json_filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving comprehensive report: {e}")

# Global Urban Foresight Scout instance
urban_foresight_scout = UrbanForesightScout()

# Convenience functions
def map_government_offices(location_coordinate: Tuple[float, float]) -> Dict:
    """Map government offices around location"""
    return urban_foresight_scout.map_government_offices(location_coordinate)

def scan_zoning_krk_documents(location_name: str) -> Dict:
    """Scan zoning and KRK documents"""
    return urban_foresight_scout.scan_zoning_krk_documents(location_name)

def analyze_targeting_matrix(location_name: str) -> Dict:
    """Analyze targeting matrix for pedagang and wirausaha"""
    return urban_foresight_scout.analyze_targeting_matrix(location_name)

def generate_future_map(location_coordinate: Tuple[float, float], location_name: str) -> Dict:
    """Generate 10-year future map"""
    return urban_foresight_scout.generate_future_map(location_coordinate, location_name)

if __name__ == "__main__":
    # Test Urban Foresight Scout
    logging.basicConfig(level=logging.INFO)
    
    print("=== Urban Foresight Scout Test ===")
    
    # Test with Serang coordinates
    test_coordinates = (-6.1256, 106.1445)
    
    print(f"Testing with coordinates: {test_coordinates}")
    
    # Test infrastructure crawling
    infra_result = map_government_offices(test_coordinates)
    print(f"Infrastructure projects found: {infra_result.get('total_projects_found', 0)}")
    
    # Test zoning scanning
    zoning_result = scan_zoning_krk_documents('Serang')
    print(f"Zoning documents found: {zoning_result.get('total_documents_found', 0)}")
    
    # Test targeting matrix
    targeting_result = analyze_targeting_matrix('Serang')
    print(f"Pedagang opportunities: {targeting_result.get('targeting_matrix', {}).get('pedagang', {}).get('market_size', 'Unknown')}")
    print(f"Wirausaha opportunities: {targeting_result.get('targeting_matrix', {}).get('wirausaha', {}).get('market_size', 'Unknown')}")
    
    # Test future map generation
    future_map = generate_future_map(test_coordinates, 'Serang')
    print(f"Future map status: {future_map.get('status', 'Unknown')}")
    
    print("\nUrban Foresight Scout test completed!")

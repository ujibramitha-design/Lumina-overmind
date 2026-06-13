"""
Banten Ministry Intelligence Scout untuk HUNTER_AGENT_AI_MARKETING_DIGITAL
Comprehensive data collection untuk semua kementrian di Banten
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re
import csv
import os

class BantenMinistryScout:
    """
    Advanced Banten Ministry Intelligence Scout
    Mengumpulkan data lengkap untuk semua kementrian di Banten
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Data storage paths
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        self.reports_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Banten regions focus
        self.banten_regions = {
            'kota_serang': {
                'name': 'Kota Serang',
                'capital': 'Serang',
                'type': 'Kota',
                'population': 655000,
                'area_km2': 266.74,
                'districts': ['Cipocok Jaya', 'Curug', 'Kasemen', 'Serang', 'Taktakan', 'Walantaka'],
                'ministry_offices': [
                    'Kementerian Dalam Negeri',
                    'Kementerian Hukum dan HAM',
                    'Kementerian Keuangan',
                    'Kementerian Pendidikan dan Kebudayaan',
                    'Kementerian Kesehatan',
                    'Kementerian Sosial',
                    'Kementerian Perhubungan',
                    'Kementerian Pekerjaan Umum dan Perumahan Rakyat',
                    'Kementerian Pertanian',
                    'Kementerian Perindustrian',
                    'Kementerian Perdagangan',
                    'Kementerian Lingkungan Hidup dan Kehutanan',
                    'Kementerian Kelautan dan Perikanan',
                    'Kementerian Tenaga Kerja dan Transmigrasi',
                    'Kementerian Pariwisata dan Ekonomi Kreatif',
                    'Kementerian Komunikasi dan Informatika',
                    'Kementerian Koperasi dan UKM',
                    'Kementerian Pemberdayaan Perempuan dan Perlindungan Anak',
                    'Kementerian Pemuda dan Olahraga',
                    'Kementerian Agama',
                    'Kementerian Luar Negeri',
                    'Kementerian Pertahanan',
                    'Kementerian BUMN',
                    'Kementerian Investasi',
                    'Kementerian Kesehatan',
                    'Kementerian Pendidikan',
                    'Kementerian Perhubungan',
                    'Kementerian Pekerjaan Umum',
                    'Kementerian Sosial',
                    'Kementerian Pertanian',
                    'Kementerian Perindustrian',
                    'Kementerian Perdagangan',
                    'Kementerian Lingkungan Hidup',
                    'Kementerian Kelautan dan Perikanan',
                    'Kementerian Tenaga Kerja',
                    'Kementerian Pariwisata',
                    'Kementerian Komunikasi dan Informatika',
                    'Kementerian Koperasi',
                    'Kementerian Pemberdayaan Perempuan',
                    'Kementerian Pemuda dan Olahraga',
                    'Kementerian Agama',
                    'Kementerian Luar Negeri',
                    'Kementerian Pertahanan',
                    'Kementerian BUMN',
                    'Kementerian Investasi',
                    'Kementerian Badan Usaha Milik Negara',
                    'Kementerian Pemberdayaan Aparatur Sipil Negara',
                    'Kementerian Pendapatan Negara',
                    'Kementerian Perencanaan Pembangunan Nasional',
                    'Kementerian Badan Intelijen Negara',
                    'Kementerian Badan Pengawas Keuangan',
                    'Kementerian Badan Pemeriksa Keuangan',
                    'Kementerian Badan Meteorologi Klimatologi dan Geofisika',
                    'Kementerian Badan Narkotika Nasional',
                    'Kementerian Badan Pengawas Obat dan Makanan',
                    'Kementerian Badan Kependudukan dan Keluarga Berencana',
                    'Kementerian Badan Penanggulangan Bencana',
                    'Kementerian Badan Penelitian dan Pengembangan',
                    'Kementerian Badan Informasi Geospasial',
                    'Kementerian Badan Standardisasi Nasional',
                    'Kementerian Badan Pengawas Tenaga Nuklir',
                    'Kementerian Badan Pengawas Obat dan Makanan',
                    'Kementerian Badan Kependudukan dan Keluarga Berencana',
                    'Kementerian Badan Penanggulangan Bencana',
                    'Kementerian Badan Penelitian dan Pengembangan',
                    'Kementerian Badan Informasi Geospasial',
                    'Kementerian Badan Standardisasi Nasional',
                    'Kementerian Badan Pengawas Tenaga Nuklir'
                ]
            },
            'kabupaten_serang': {
                'name': 'Kabupaten Serang',
                'capital': 'Ciruas',
                'type': 'Kabupaten',
                'population': 1580000,
                'area_km2': 1855.78,
                'districts': [
                    'Ciruas', 'Cikeusal', 'Cinangka', 'Ciomas', 'Gunungsari', 'Kramatwatu',
                    'Kopo', 'Mancak', 'Padarincang', 'Pabuaran', 'Pamarayan', 'Pontang',
                    'Tanara', 'Tirtayasa', 'Waringinkurung', 'Baros', 'Binuang',
                    'Bojonglopo', 'Carenang', 'Jawilan', 'Kibin', 'Lebakwana',
                    'Muncang', 'Petir', 'Puloampel', 'Sindang Sari', 'Sukaresmi',
                    'Tunjungharjo', 'Warunggunung'
                ],
                'ministry_offices': [
                    'Kementerian Dalam Negeri',
                    'Kementerian Hukum dan HAM',
                    'Kementerian Keuangan',
                    'Kementerian Pendidikan dan Kebudayaan',
                    'Kementerian Kesehatan',
                    'Kementerian Sosial',
                    'Kementerian Perhubungan',
                    'Kementerian Pekerjaan Umum dan Perumahan Rakyat',
                    'Kementerian Pertanian',
                    'Kementerian Perindustrian',
                    'Kementerian Perdagangan',
                    'Kementerian Lingkungan Hidup dan Kehutanan',
                    'Kementerian Kelautan dan Perikanan',
                    'Kementerian Tenaga Kerja dan Transmigrasi',
                    'Kementerian Pariwisata dan Ekonomi Kreatif',
                    'Kementerian Komunikasi dan Informatika',
                    'Kementerian Koperasi dan UKM',
                    'Kementerian Pemberdayaan Perempuan dan Perlindungan Anak',
                    'Kementerian Pemuda dan Olahraga',
                    'Kementerian Agama',
                    'Kementerian Luar Negeri',
                    'Kementerian Pertahanan',
                    'Kementerian BUMN',
                    'Kementerian Investasi',
                    'Kementerian Kesehatan',
                    'Kementerian Pendidikan',
                    'Kementerian Perhubungan',
                    'Kementerian Pekerjaan Umum',
                    'Kementerian Sosial',
                    'Kementerian Pertanian',
                    'Kementerian Perindustrian',
                    'Kementerian Perdagangan',
                    'Kementerian Lingkungan Hidup',
                    'Kementerian Kelautan dan Perikanan',
                    'Kementerian Tenaga Kerja',
                    'Kementerian Pariwisata',
                    'Kementerian Komunikasi dan Informatika',
                    'Kementerian Koperasi',
                    'Kementerian Pemberdayaan Perempuan',
                    'Kementerian Pemuda dan Olahraga',
                    'Kementerian Agama',
                    'Kementerian Luar Negeri',
                    'Kementerian Pertahanan',
                    'Kementerian BUMN',
                    'Kementerian Investasi',
                    'Kementerian Badan Usaha Milik Negara',
                    'Kementerian Pemberdayaan Aparatur Sipil Negara',
                    'Kementerian Pendapatan Negara',
                    'Kementerian Perencanaan Pembangunan Nasional',
                    'Kementerian Badan Intelijen Negara',
                    'Kementerian Badan Pengawas Keuangan',
                    'Kementerian Badan Pemeriksa Keuangan',
                    'Kementerian Badan Meteorologi Klimatologi dan Geofisika',
                    'Kementerian Badan Narkotika Nasional',
                    'Kementerian Badan Pengawas Obat dan Makanan',
                    'Kementerian Badan Kependudukan dan Keluarga Berencana',
                    'Kementerian Badan Penanggulangan Bencana',
                    'Kementerian Badan Penelitian dan Pengembangan',
                    'Kementerian Badan Informasi Geospasial',
                    'Kementerian Badan Standardisasi Nasional',
                    'Kementerian Badan Pengawas Tenaga Nuklir',
                    'Kementerian Badan Pengawas Obat dan Makanan',
                    'Kementerian Badan Kependudukan dan Keluarga Berencana',
                    'Kementerian Badan Penanggulangan Bencana',
                    'Kementerian Badan Penelitian dan Pengembangan',
                    'Kementerian Badan Informasi Geospasial',
                    'Kementerian Badan Standardisasi Nasional',
                    'Kementerian Badan Pengawas Tenaga Nuklir'
                ]
            },
            'kota_cilegon': {
                'name': 'Kota Cilegon',
                'capital': 'Cilegon',
                'type': 'Kota',
                'population': 435000,
                'area_km2': 175.51,
                'districts': ['Cibeber', 'Cilegon', 'Ciwandan', 'Grogol', 'Jombang', 'Pulomerak'],
                'ministry_offices': [
                    'Kementerian Dalam Negeri',
                    'Kementerian Hukum dan HAM',
                    'Kementerian Keuangan',
                    'Kementerian Pendidikan dan Kebudayaan',
                    'Kementerian Kesehatan',
                    'Kementerian Sosial',
                    'Kementerian Perhubungan',
                    'Kementerian Pekerjaan Umum dan Perumahan Rakyat',
                    'Kementerian Pertanian',
                    'Kementerian Perindustrian',
                    'Kementerian Perdagangan',
                    'Kementerian Lingkungan Hidup dan Kehutanan',
                    'Kementerian Kelautan dan Perikanan',
                    'Kementerian Tenaga Kerja dan Transmigrasi',
                    'Kementerian Pariwisata dan Ekonomi Kreatif',
                    'Kementerian Komunikasi dan Informatika',
                    'Kementerian Koperasi dan UKM',
                    'Kementerian Pemberdayaan Perempuan dan Perlindungan Anak',
                    'Kementerian Pemuda dan Olahraga',
                    'Kementerian Agama',
                    'Kementerian Luar Negeri',
                    'Kementerian Pertahanan',
                    'Kementerian BUMN',
                    'Kementerian Investasi',
                    'Kementerian Kesehatan',
                    'Kementerian Pendidikan',
                    'Kementerian Perhubungan',
                    'Kementerian Pekerjaan Umum',
                    'Kementerian Sosial',
                    'Kementerian Pertanian',
                    'Kementerian Perindustrian',
                    'Kementerian Perdagangan',
                    'Kementerian Lingkungan Hidup',
                    'Kementerian Kelautan dan Perikanan',
                    'Kementerian Tenaga Kerja',
                    'Kementerian Pariwisata',
                    'Kementerian Komunikasi dan Informatika',
                    'Kementerian Koperasi',
                    'Kementerian Pemberdayaan Perempuan',
                    'Kementerian Pemuda dan Olahraga',
                    'Kementerian Agama',
                    'Kementerian Luar Negeri',
                    'Kementerian Pertahanan',
                    'Kementerian BUMN',
                    'Kementerian Investasi',
                    'Kementerian Badan Usaha Milik Negara',
                    'Kementerian Pemberdayaan Aparatur Sipil Negara',
                    'Kementerian Pendapatan Negara',
                    'Kementerian Perencanaan Pembangunan Nasional',
                    'Kementerian Badan Intelijen Negara',
                    'Kementerian Badan Pengawas Keuangan',
                    'Kementerian Badan Pemeriksa Keuangan',
                    'Kementerian Badan Meteorologi Klimatologi dan Geofisika',
                    'Kementerian Badan Narkotika Nasional',
                    'Kementerian Badan Pengawas Obat dan Makanan',
                    'Kementerian Badan Kependudukan dan Keluarga Berencana',
                    'Kementerian Badan Penanggulangan Bencana',
                    'Kementerian Badan Penelitian dan Pengembangan',
                    'Kementerian Badan Informasi Geospasial',
                    'Kementerian Badan Standardisasi Nasional',
                    'Kementerian Badan Pengawas Tenaga Nuklir',
                    'Kementerian Badan Pengawas Obat dan Makanan',
                    'Kementerian Badan Kependudukan dan Keluarga Berencana',
                    'Kementerian Badan Penanggulangan Bencana',
                    'Kementerian Badan Penelitian dan Pengembangan',
                    'Kementerian Badan Informasi Geospasial',
                    'Kementerian Badan Standardisasi Nasional',
                    'Kementerian Badan Pengawas Tenaga Nuklir'
                ]
            }
        }
    
    def collect_all_banten_ministry_data(self, target_regions: List[str] = None) -> Dict:
        """
        Kumpulkan data dari semua kementrian di Banten
        """
        if target_regions is None:
            target_regions = ['kota_serang', 'kabupaten_serang', 'kota_cilegon']
        
        self.logger.info(f"Starting comprehensive Banten ministry data collection for regions: {target_regions}")
        
        all_data = {
            'collection_timestamp': datetime.now().isoformat(),
            'target_regions': target_regions,
            'regions': {},
            'summary': {
                'total_regions': len(target_regions),
                'total_ministries': 0,
                'total_offices': 0,
                'total_employees': 0,
                'total_data_points': 0,
                'provincial_info': {
                    'province': 'Banten',
                    'capital': 'Serang',
                    'population': 12100000,
                    'area_km2': 9662.93,
                    'governor': 'Al Muktabar',
                    'established_year': 2000
                }
            }
        }
        
        for region_key, region_config in self.banten_regions.items():
            if region_key in target_regions:
                self.logger.info(f"Collecting data from {region_config['name']}...")
                
                region_data = self._collect_region_ministry_data(region_key, region_config)
                all_data['regions'][region_key] = region_data
                all_data['summary']['total_ministries'] += region_data.get('total_ministries', 0)
                all_data['summary']['total_offices'] += region_data.get('total_offices', 0)
                all_data['summary']['total_employees'] += region_data.get('total_employees', 0)
                all_data['summary']['total_data_points'] += region_data.get('total_data_points', 0)
                
                # Rate limiting antar region
                time.sleep(2)
        
        # Save comprehensive data
        self._save_comprehensive_data(all_data)
        
        # Generate intelligence report
        self._generate_intelligence_report(all_data)
        
        self.logger.info(f"Comprehensive Banten ministry data collection completed: {all_data['summary']['total_data_points']} data points")
        
        return all_data
    
    def _collect_region_ministry_data(self, region_key: str, region_config: Dict) -> Dict:
        """
        Kumpulkan data untuk region spesifik
        """
        region_data = {
            'region_name': region_config['name'],
            'region_key': region_key,
            'collection_timestamp': datetime.now().isoformat(),
            'ministries': {},
            'total_ministries': 0,
            'total_offices': 0,
            'total_employees': 0,
            'total_data_points': 0,
            'region_info': {
                'capital': region_config['capital'],
                'type': region_config['type'],
                'population': region_config['population'],
                'area_km2': region_config['area_km2'],
                'districts': region_config['districts']
            }
        }
        
        for ministry_name in region_config['ministry_offices']:
            self.logger.info(f"Collecting data for {ministry_name} in {region_config['name']}...")
            
            ministry_data = self._collect_ministry_data(ministry_name, region_key, region_config)
            region_data['ministries'][ministry_name] = ministry_data
            region_data['total_ministries'] += 1
            region_data['total_offices'] += ministry_data.get('office_count', 0)
            region_data['total_employees'] += ministry_data.get('employee_count', 0)
            region_data['total_data_points'] += ministry_data.get('data_points', 0)
            
            # Rate limiting antar ministry
            time.sleep(1)
        
        return region_data
    
    def _collect_ministry_data(self, ministry_name: str, region_key: str, region_config: Dict) -> Dict:
        """
        Kumpulkan data untuk kementrian spesifik
        """
        ministry_data = {
            'ministry_name': ministry_name,
            'region': region_key,
            'collection_timestamp': datetime.now().isoformat(),
            'office_count': 0,
            'employee_count': 0,
            'data_points': 0,
            'ministry_profile': {},
            'leadership': {},
            'contact_info': {},
            'services': {},
            'programs': {},
            'budget': {},
            'facilities': {},
            'performance': {}
        }
        
        # Generate ministry profile
        ministry_profile = self._generate_ministry_profile(ministry_name, region_config)
        ministry_data['ministry_profile'] = ministry_profile
        ministry_data['data_points'] += 5  # Profile data points
        
        # Generate leadership data
        leadership_data = self._generate_leadership_data(ministry_name, region_config)
        ministry_data['leadership'] = leadership_data
        ministry_data['data_points'] += len(leadership_data)
        
        # Generate contact info
        contact_info = self._generate_contact_info(ministry_name, region_config)
        ministry_data['contact_info'] = contact_info
        ministry_data['data_points'] += len(contact_info)
        
        # Generate services
        services_data = self._generate_services_data(ministry_name, region_config)
        ministry_data['services'] = services_data
        ministry_data['data_points'] += len(services_data)
        
        # Generate programs
        programs_data = self._generate_programs_data(ministry_name, region_config)
        ministry_data['programs'] = programs_data
        ministry_data['data_points'] += len(programs_data)
        
        # Generate budget info
        budget_data = self._generate_budget_data(ministry_name, region_config)
        ministry_data['budget'] = budget_data
        ministry_data['data_points'] += 4  # Budget data points
        
        # Generate facilities
        facilities_data = self._generate_facilities_data(ministry_name, region_config)
        ministry_data['facilities'] = facilities_data
        ministry_data['data_points'] += len(facilities_data)
        
        # Generate performance metrics
        performance_data = self._generate_performance_data(ministry_name, region_config)
        ministry_data['performance'] = performance_data
        ministry_data['data_points'] += 5  # Performance data points
        
        # Calculate office count and employee count
        ministry_data['office_count'] = self._calculate_office_count(ministry_name, region_config)
        ministry_data['employee_count'] = self._calculate_employee_count(ministry_name, region_config)
        
        return ministry_data
    
    def _generate_ministry_profile(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate ministry profile (simulated data)
        """
        profile = {
            'official_name': f"Kantor {ministry_name} Wilayah {region_config['name']}",
            'abbreviation': self._get_ministry_abbreviation(ministry_name),
            'established_year': 2000 + (hash(ministry_name) % 20),
            'ministry_type': self._get_ministry_type(ministry_name),
            'main_functions': self._get_ministry_functions(ministry_name),
            'legal_basis': f"Undang-Undang Nomor {hash(ministry_name) % 1000} Tahun {2000 + (hash(ministry_name) % 20)}",
            'vision': f"Terwujudnya {self._get_ministry_focus(ministry_name)} yang profesional dan berkualitas di {region_config['name']}",
            'mission': [
                f"Menyelenggarakan {self._get_ministry_focus(ministry_name)} yang terbaik",
                f"Meningkatkan kualitas pelayanan {self._get_ministry_focus(ministry_name)}",
                f"Mewujudkan tata kelola {self._get_ministry_focus(ministry_name)} yang baik",
                f"Memfasilitasi akses masyarakat terhadap {self._get_ministry_focus(ministry_name)}"
            ],
            'strategic_goals': [
                f"Peningkatan kualitas {self._get_ministry_focus(ministry_name)}",
                f"Optimalisasi pelayanan {self._get_ministry_focus(ministry_name)}",
                f"Digitalisasi {self._get_ministry_focus(ministry_name)}",
                f"Pemberdayaan masyarakat dalam {self._get_ministry_focus(ministry_name)}"
            ],
            'core_values': [
                'Integritas',
                'Profesionalisme',
                'Akuntabilitas',
                'Transparansi',
                'Pelayanan Publik'
            ]
        }
        
        return profile
    
    def _generate_leadership_data(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate leadership data (simulated data)
        """
        leadership = {
            'kepala_kantor': {
                'name': f"Drs. {self._get_indonesian_name()}",
                'title': f"Kepala Kantor {ministry_name} Wilayah {region_config['name']}",
                'period': f"{2020 + (hash(ministry_name) % 4)} - {2024 + (hash(ministry_name) % 4)}",
                'education': "S2 Administrasi Publik",
                'experience': f"{15 + (hash(ministry_name) % 10)} tahun di bidang {self._get_ministry_focus(ministry_name)}",
                'phone': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name + 'kepala') % 10000:04d}",
                'email': f"kepala.{ministry_name.lower().replace(' ', '_').replace('kementerian_', '')}@{region_config['name'].lower().replace(' ', '')}.go.id"
            },
            'sekretaris': {
                'name': f"Dra. {self._get_indonesian_name()}",
                'title': f"Sekretaris {ministry_name} Wilayah {region_config['name']}",
                'period': f"{2021 + (hash(ministry_name) % 3)} - {2025 + (hash(ministry_name) % 3)}",
                'education': "S1 Hukum",
                'experience': f"{10 + (hash(ministry_name + 'sekretaris') % 8)} tahun di bidang administrasi",
                'phone': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name + 'sekretaris') % 10000:04d}",
                'email': f"sekretaris.{ministry_name.lower().replace(' ', '_').replace('kementerian_', '')}@{region_config['name'].lower().replace(' ', '')}.go.id"
            },
            'kepala_seksi': [
                {
                    'section': f"Seksi {self._get_ministry_focus(ministry_name)} I",
                    'name': f"{self._get_indonesian_name()}, S.Sos",
                    'title': f"Kepala Seksi {self._get_ministry_focus(ministry_name)} I",
                    'phone': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name + 'seksi1') % 10000:04d}"
                },
                {
                    'section': f"Seksi {self._get_ministry_focus(ministry_name)} II",
                    'name': f"{self._get_indonesian_name()}, S.T.",
                    'title': f"Kepala Seksi {self._get_ministry_focus(ministry_name)} II",
                    'phone': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name + 'seksi2') % 10000:04d}"
                }
            ]
        }
        
        return leadership
    
    def _generate_contact_info(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate contact information (simulated data)
        """
        contact_info = {
            'office_address': f"Jl. {self._get_street_name()} No. {hash(ministry_name) % 100}, {region_config['capital']}, {region_config['name']}, Banten",
            'postal_code': f"{42100 + (hash(ministry_name) % 100)}",
            'phone_office': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name) % 10000:04d}",
            'fax': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name + 'fax') % 10000:04d}",
            'email_general': f"info.{ministry_name.lower().replace(' ', '_').replace('kementerian_', '')}@{region_config['name'].lower().replace(' ', '')}.go.id",
            'email_service': f"layanan.{ministry_name.lower().replace(' ', '_').replace('kementerian_', '')}@{region_config['name'].lower().replace(' ', '')}.go.id",
            'website': f"https://{ministry_name.lower().replace(' ', '_').replace('kementerian_', '')}.{region_config['name'].lower().replace(' ', '')}.go.id",
            'social_media': {
                'facebook': f"https://facebook.com/{ministry_name.lower().replace(' ', '')}.{region_config['name'].lower().replace(' ', '')}",
                'twitter': f"https://twitter.com/@{ministry_name.lower().replace(' ', '')}_{region_config['name'].lower().replace(' ', '')}",
                'instagram': f"https://instagram.com/{ministry_name.lower().replace(' ', '')}.{region_config['name'].lower().replace(' ', '')}"
            },
            'office_hours': {
                'senin_jumat': '08:00 - 16:00',
                'sabtu': '08:00 - 12:00',
                'minggu': 'Tutup'
            },
            'service_hours': {
                'senin_jumat': '08:00 - 15:00',
                'sabtu': '08:00 - 12:00',
                'minggu': 'Tutup'
            },
            'emergency_contact': f"+62-{self._get_phone_code(region_config['name'])}-{hash(ministry_name + 'emergency') % 10000:04d}"
        }
        
        return contact_info
    
    def _generate_services_data(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate services data (simulated data)
        """
        services = {}
        
        # Generate services based on ministry type
        if 'Dalam Negeri' in ministry_name:
            services = {
                'administrasi_pemerintahan': {
                    'description': 'Pelayanan administrasi pemerintahan',
                    'requirements': ['KTP', 'KK', 'Surat permohonan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Persetujuan → Penerbitan'
                },
                'kependudukan': {
                    'description': 'Pelayanan kependudukan',
                    'requirements': ['KTP', 'KK', 'Akta kelahiran'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Verifikasi → Penerbitan'
                },
                'pemerintahan': {
                    'description': 'Pelayanan pemerintahan',
                    'requirements': ['Surat permohonan', 'Dokumen pendukung'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                }
            }
        elif 'Hukum dan HAM' in ministry_name:
            services = {
                'legal_aid': {
                    'description': 'Bantuan hukum',
                    'requirements': ['KTP', 'KK', 'Surat keterangan miskin'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'ham': {
                    'description': 'Pelayanan hak asasi manusia',
                    'requirements': ['KTP', 'Laporan pelanggaran', 'Bukti'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Laporan → Investigasi → Tindak lanjut'
                },
                'notaris': {
                    'description': 'Pelayanan notaris',
                    'requirements': ['KTP', 'Dokumen yang akan disahkan'],
                    'processing_time': '1-3 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Verifikasi → Penandatanganan'
                }
            }
        elif 'Keuangan' in ministry_name:
            services = {
                'pajak': {
                    'description': 'Pelayanan perpajakan',
                    'requirements': ['NPWP', 'Laporan pajak', 'Dokumen pendukung'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Penyelesaian'
                },
                'anggaran': {
                    'description': 'Pelayanan anggaran',
                    'requirements': ['RAB', 'Dokumen pendukung', 'Surat permohonan'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                },
                'keuangan': {
                    'description': 'Pelayanan keuangan',
                    'requirements': ['Surat permohonan', 'Dokumen pendukung'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Pencairan'
                }
            }
        elif 'Pendidikan dan Kebudayaan' in ministry_name:
            services = {
                'pendidikan': {
                    'description': 'Pelayanan pendidikan',
                    'requirements': ['KTP', 'Ijazah', 'Surat permohonan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Persetujuan'
                },
                'kebudayaan': {
                    'description': 'Pelayanan kebudayaan',
                    'requirements': ['KTP', 'Proposal', 'Dokumen pendukung'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                },
                'beasiswa': {
                    'description': 'Program beasiswa',
                    'requirements': ['KTP', 'KK', 'Raport', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Pencairan'
                }
            }
        elif 'Kesehatan' in ministry_name:
            services = {
                'kesehatan': {
                    'description': 'Pelayanan kesehatan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan sakit'],
                    'processing_time': '1-3 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Pemeriksaan → Pengobatan'
                },
                'bpjs': {
                    'description': 'Pelayanan BPJS',
                    'requirements': ['KTP', 'KK', 'Kartu BPJS'],
                    'processing_time': '1-2 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Verifikasi → Aktivasi'
                },
                'vaksin': {
                    'description': 'Program vaksinasi',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '1 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Vaksinasi → Kartu vaksin'
                }
            }
        elif 'Sosial' in ministry_name:
            services = {
                'bantuan_sosial': {
                    'description': 'Program bantuan sosial',
                    'requirements': ['KTP', 'KK', 'Surat keterangan miskin'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Pencairan'
                },
                'pemberdayaan': {
                    'description': 'Program pemberdayaan sosial',
                    'requirements': ['KTP', 'KK', 'Proposal'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Program'
                },
                'perlindungan': {
                    'description': 'Program perlindungan sosial',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Perlindungan'
                }
            }
        elif 'Perhubungan' in ministry_name:
            services = {
                'perizinan_kendaraan': {
                    'description': 'Perizinan kendaraan',
                    'requirements': ['KTP', 'STNK', 'BPKB'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 50.000 - Rp 200.000',
                    'procedure': 'Pengajuan → Verifikasi → Persetujuan'
                },
                'uji_kir': {
                    'description': 'Uji kelayakan kendaraan',
                    'requirements': ['STNK', 'Kendaraan'],
                    'processing_time': '1-2 hari kerja',
                    'fee': 'Rp 30.000 - Rp 150.000',
                    'procedure': 'Pendaftaran → Uji → Sertifikat'
                },
                'angkutan': {
                    'description': 'Perizinan angkutan',
                    'requirements': ['KTP', 'STNK', 'Surat izin'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 500.000 - Rp 2.000.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                }
            }
        elif 'Pekerjaan Umum dan Perumahan Rakyat' in ministry_name:
            services = {
                'perizinan_bangunan': {
                    'description': 'Perizinan bangunan',
                    'requirements': ['KTP', 'IMB', 'Rencana bangunan'],
                    'processing_time': '14-30 hari kerja',
                    'fee': 'Rp 1.000.000 - Rp 5.000.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                },
                'perumahan': {
                    'description': 'Program perumahan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Program'
                },
                'infrastruktur': {
                    'description': 'Pelayanan infrastruktur',
                    'requirements': ['Surat permohonan', 'Dokumen pendukung'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                }
            }
        elif 'Pertanian' in ministry_name:
            services = {
                'pertanian': {
                    'description': 'Pelayanan pertanian',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'perkebunan': {
                    'description': 'Pelayanan perkebunan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'peternakan': {
                    'description': 'Pelayanan peternakan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                }
            }
        elif 'Perindustrian' in ministry_name:
            services = {
                'perizinan_industri': {
                    'description': 'Perizinan industri',
                    'requirements': ['KTP', 'SIUP', 'Surat izin'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 500.000 - Rp 2.000.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                },
                'pemberdayaan_industri': {
                    'description': 'Pemberdayaan industri',
                    'requirements': ['KTP', 'KK', 'Proposal'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Program'
                },
                'standar_industri': {
                    'description': 'Standar industri',
                    'requirements': ['Surat permohonan', 'Dokumen pendukung'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Evaluasi → Sertifikat'
                }
            }
        elif 'Perdagangan' in ministry_name:
            services = {
                'perizinan_dagang': {
                    'description': 'Perizinan perdagangan',
                    'requirements': ['KTP', 'SIUP', 'NPWP'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Verifikasi → Persetujuan'
                },
                'pasar': {
                    'description': 'Pelayanan pasar',
                    'requirements': ['KTP', 'Surat permohonan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Lokasi'
                },
                'harga': {
                    'description': 'Pengawasan harga',
                    'requirements': ['Laporan', 'Bukti'],
                    'processing_time': '3-7 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Laporan → Investigasi → Tindakan'
                }
            }
        elif 'Lingkungan Hidup dan Kehutanan' in ministry_name:
            services = {
                'lingkungan': {
                    'description': 'Pelayanan lingkungan',
                    'requirements': ['KTP', 'Surat permohonan', 'Dokumen'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                },
                'kehutanan': {
                    'description': 'Pelayanan kehutanan',
                    'requirements': ['KTP', 'Surat keterangan', 'Dokumen'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Izin'
                },
                'penghijauan': {
                    'description': 'Program penghijauan',
                    'requirements': ['KTP', 'KK', 'Surat permohonan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Program'
                }
            }
        elif 'Kelautan dan Perikanan' in ministry_name:
            services = {
                'kelautan': {
                    'description': 'Pelayanan kelautan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Izin'
                },
                'perikanan': {
                    'description': 'Pelayanan perikanan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'aquaculture': {
                    'description': 'Program aquaculture',
                    'requirements': ['KTP', 'KK', 'Proposal'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Program'
                }
            }
        elif 'Tenaga Kerja dan Transmigrasi' in ministry_name:
            services = {
                'tenaga_kerja': {
                    'description': 'Pelayanan tenaga kerja',
                    'requirements': ['KTP', 'KK', 'Ijazah'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Verifikasi → Penempatan'
                },
                'pelatihan': {
                    'description': 'Program pelatihan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Seleksi → Pelatihan'
                },
                'transmigrasi': {
                    'description': 'Program transmigrasi',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Program'
                }
            }
        elif 'Pariwisata dan Ekonomi Kreatif' in ministry_name:
            services = {
                'pariwisata': {
                    'description': 'Pelayanan pariwisata',
                    'requirements': ['KTP', 'Proposal', 'Dokumen'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                },
                'ekonomi_kreatif': {
                    'description': 'Pelayanan ekonomi kreatif',
                    'requirements': ['KTP', 'Proposal', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Program'
                },
                'event': {
                    'description': 'Pelayanan event',
                    'requirements': ['Proposal', 'Dokumen pendukung'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 500.000 - Rp 2.000.000',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                }
            }
        elif 'Komunikasi dan Informatika' in ministry_name:
            services = {
                'komunikasi': {
                    'description': 'Pelayanan komunikasi',
                    'requirements': ['KTP', 'Surat permohonan', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                },
                'informatika': {
                    'description': 'Pelayanan informatika',
                    'requirements': ['KTP', 'Surat permohonan', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                },
                'statistik': {
                    'description': 'Pelayanan statistik',
                    'requirements': ['Surat permohonan', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Data'
                }
            }
        elif 'Koperasi dan UKM' in ministry_name:
            services = {
                'koperasi': {
                    'description': 'Pelayanan koperasi',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Pendirian'
                },
                'ukm': {
                    'description': 'Pelayanan UKM',
                    'requirements': ['KTP', 'KK', 'Proposal'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Bantuan'
                },
                'modal': {
                    'description': 'Program modal',
                    'requirements': ['KTP', 'KK', 'Proposal'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Pencairan'
                }
            }
        elif 'Pemberdayaan Perempuan dan Perlindungan Anak' in ministry_name:
            services = {
                'perempuan': {
                    'description': 'Pelayanan pemberdayaan perempuan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Program'
                },
                'anak': {
                    'description': 'Perlindungan anak',
                    'requirements': ['KTP', 'KK', 'Laporan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Laporan → Investigasi → Perlindungan'
                },
                'kdrt': {
                    'description': 'Kekerasan dalam rumah tangga',
                    'requirements': ['Laporan', 'Bukti', 'KTP'],
                    'processing_time': '1-3 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Laporan → Investigasi → Perlindungan'
                }
            }
        elif 'Pemuda dan Olahraga' in ministry_name:
            services = {
                'pemuda': {
                    'description': 'Pelayanan pemuda',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Program'
                },
                'olahraga': {
                    'description': 'Pelayanan olahraga',
                    'requirements': ['Proposal', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Program'
                },
                'fasilitas': {
                    'description': 'Fasilitas olahraga',
                    'requirements': ['Surat permohonan', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Penggunaan'
                }
            }
        elif 'Agama' in ministry_name:
            services = {
                'agama': {
                    'description': 'Pelayanan agama',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'tempat_ibadah': {
                    'description': 'Pelayanan tempat ibadah',
                    'requirements': ['Proposal', 'Dokumen'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 100.000 - Rp 500.000',
                    'procedure': 'Pengajuan → Survey → Persetujuan'
                },
                'bantuan': {
                    'description': 'Bantuan agama',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                }
            }
        elif 'Luar Negeri' in ministry_name:
            services = {
                'paspor': {
                    'description': 'Pelayanan paspor',
                    'requirements': ['KTP', 'KK', 'Foto', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 300.000 - Rp 600.000',
                    'procedure': 'Pengajuan → Verifikasi → Penerbitan'
                },
                'visa': {
                    'description': 'Pelayanan visa',
                    'requirements': ['Paspor', 'Surat undangan', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Rp 500.000 - Rp 1.000.000',
                    'procedure': 'Pengajuan → Verifikasi → Persetujuan'
                },
                'konsuler': {
                    'description': 'Pelayanan konsuler',
                    'requirements': ['KTP', 'Paspor', 'Surat keterangan'],
                    'processing_time': '1-3 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                }
            }
        elif 'Pertahanan' in ministry_name:
            services = {
                'pertahanan': {
                    'description': 'Pelayanan pertahanan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'wajib_militer': {
                    'description': 'Pelayanan wajib militer',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Verifikasi → Pelaksanaan'
                },
                'cadangan': {
                    'description': 'Pelayanan cadangan',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Verifikasi → Pelaksanaan'
                }
            }
        elif 'BUMN' in ministry_name:
            services = {
                'bumn': {
                    'description': 'Pelayanan BUMN',
                    'requirements': ['KTP', 'KK', 'Surat keterangan'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Bantuan'
                },
                'investasi': {
                    'description': 'Pelayanan investasi BUMN',
                    'requirements': ['KTP', 'NPWP', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Investasi'
                },
                'bantuan': {
                    'description': 'Bantuan BUMN',
                    'requirements': ['KTP', 'KK', 'Proposal'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Evaluasi → Bantuan'
                }
            }
        elif 'Investasi' in ministry_name:
            services = {
                'investasi': {
                    'description': 'Pelayanan investasi',
                    'requirements': ['KTP', 'NPWP', 'Dokumen'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Persetujuan'
                },
                'izin_investasi': {
                    'description': 'Perizinan investasi',
                    'requirements': ['Proposal', 'Dokumen pendukung'],
                    'processing_time': '14-21 hari kerja',
                    'fee': 'Rp 1.000.000 - Rp 5.000.000',
                    'procedure': 'Pengajuan → Evaluasi → Persetujuan'
                },
                'fasilitasi': {
                    'description': 'Fasilitasi investasi',
                    'requirements': ['KTP', 'NPWP', 'Proposal'],
                    'processing_time': '7-14 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Fasilitasi'
                }
            }
        else:
            # Generic services for other ministries
            services = {
                'konsultasi_umum': {
                    'description': 'Konsultasi umum',
                    'requirements': ['KTP', 'Identitas diri'],
                    'processing_time': '1-2 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pendaftaran → Konsultasi → Follow-up'
                },
                'pengaduan': {
                    'description': 'Layanan pengaduan',
                    'requirements': ['Identitas diri', 'Surat pengaduan'],
                    'processing_time': '3-7 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pengajuan → Verifikasi → Tindak lanjut'
                },
                'informasi': {
                    'description': 'Layanan informasi',
                    'requirements': ['Identitas diri'],
                    'processing_time': '1 hari kerja',
                    'fee': 'Gratis',
                    'procedure': 'Pertanyaan → Jawaban → Dokumentasi'
                }
            }
        
        return services
    
    def _generate_programs_data(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate programs data (simulated data)
        """
        programs = {}
        
        # Generate programs based on ministry type
        if 'Dalam Negeri' in ministry_name:
            programs = {
                'program_pemerintahan': {
                    'description': 'Program pemerintahan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Administrasi', 'Pelayanan', 'Koordinasi']
                },
                'program_kependudukan': {
                    'description': 'Program kependudukan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 300.000.000',
                    'activities': ['Registrasi', 'Verifikasi', 'Dokumentasi']
                }
            }
        elif 'Hukum dan HAM' in ministry_name:
            programs = {
                'program_hukum': {
                    'description': 'Program bantuan hukum',
                    'target': 'Masyarakat miskin',
                    'duration': 'Tahunan',
                    'budget': 'Rp 400.000.000',
                    'activities': ['Konsultasi', 'Bantuan', 'Pendidikan']
                },
                'program_ham': {
                    'description': 'Program HAM',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 300.000.000',
                    'activities': ['Edukasi', 'Advokasi', 'Monitoring']
                }
            }
        elif 'Keuangan' in ministry_name:
            programs = {
                'program_pajak': {
                    'description': 'Program pajak',
                    'target': 'Wajib pajak',
                    'duration': 'Tahunan',
                    'budget': 'Rp 200.000.000',
                    'activities': ['Sosialisasi', 'Pelayanan', 'Penegakan']
                },
                'program_anggaran': {
                    'description': 'Program anggaran',
                    'target': 'Pemerintah daerah',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Perencanaan', 'Evaluasi', 'Monitoring']
                }
            }
        elif 'Pendidikan dan Kebudayaan' in ministry_name:
            programs = {
                'program_pendidikan': {
                    'description': 'Program pendidikan',
                    'target': 'Siswa',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Beasiswa', 'Sarana', 'Pelatihan']
                },
                'program_kebudayaan': {
                    'description': 'Program kebudayaan',
                    'target': 'Seniman',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Festival', 'Pameran', 'Workshop']
                }
            }
        elif 'Kesehatan' in ministry_name:
            programs = {
                'program_kesehatan': {
                    'description': 'Program kesehatan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Pemeriksaan', 'Vaksinasi', 'Edukasi']
                },
                'program_bpjs': {
                    'description': 'Program BPJS',
                    'target': 'Pekerja',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Registrasi', 'Pelayanan', 'Monitoring']
                }
            }
        elif 'Sosial' in ministry_name:
            programs = {
                'program_bantuan': {
                    'description': 'Program bantuan sosial',
                    'target': 'Masyarakat miskin',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['PKH', 'BLT', 'Jamkesmas']
                },
                'program_pemberdayaan': {
                    'description': 'Program pemberdayaan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Pelatihan', 'Modal', 'Koperasi']
                }
            }
        elif 'Perhubungan' in ministry_name:
            programs = {
                'program_transportasi': {
                    'description': 'Program transportasi',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Bus kota', 'Angkutan umum', 'Terminal']
                },
                'program_keselamatan': {
                    'description': 'Program keselamatan',
                    'target': 'Pengguna jalan',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Patroli', 'Edukasi', 'Rambu']
                }
            }
        elif 'Pekerjaan Umum dan Perumahan Rakyat' in ministry_name:
            programs = {
                'program_infrastruktur': {
                    'description': 'Program infrastruktur',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 2.000.000.000',
                    'activities': ['Jalan', 'Jembatan', 'Drainase']
                },
                'program_perumahan': {
                    'description': 'Program perumahan',
                    'target': 'Masyarakat berpenghasilan rendah',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.500.000.000',
                    'activities': ['Rumah subsidi', 'Rumah susun', 'Perbaikan']
                }
            }
        elif 'Pertanian' in ministry_name:
            programs = {
                'program_pertanian': {
                    'description': 'Program pertanian',
                    'target': 'Petani',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Bibit', 'Pupuk', 'Pelatihan']
                },
                'program_perkebunan': {
                    'description': 'Program perkebunan',
                    'target': 'Petani perkebunan',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Benih', 'Teknologi', 'Pemasaran']
                }
            }
        elif 'Perindustrian' in ministry_name:
            programs = {
                'program_industri': {
                    'description': 'Program industri',
                    'target': 'Pengusaha industri',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Teknologi', 'Standar', 'Pemasaran']
                },
                'program_umkm': {
                    'description': 'Program UMKM',
                    'target': 'Pengusaha kecil',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Pelatihan', 'Modal', 'Pemasaran']
                }
            }
        elif 'Perdagangan' in ministry_name:
            programs = {
                'program_perdagangan': {
                    'description': 'Program perdagangan',
                    'target': 'Pedagang',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Pasar', 'Promosi', 'Pelatihan']
                },
                'program_harga': {
                    'description': 'Program pengawasan harga',
                    'target': 'Konsumen',
                    'duration': 'Tahunan',
                    'budget': 'Rp 400.000.000',
                    'activities': ['Monitoring', 'Enforcement', 'Edukasi']
                }
            }
        elif 'Lingkungan Hidup dan Kehutanan' in ministry_name:
            programs = {
                'program_lingkungan': {
                    'description': 'Program lingkungan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Penghijauan', 'Sampah', 'Pendidikan']
                },
                'program_kehutanan': {
                    'description': 'Program kehutanan',
                    'target': 'Petani kehutanan',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Reboisasi', 'Konservasi', 'Pelatihan']
                }
            }
        elif 'Kelautan dan Perikanan' in ministry_name:
            programs = {
                'program_kelautan': {
                    'description': 'Program kelautan',
                    'target': 'Nelayan',
                    'duration': 'Tahunan',
                    'budget': 'Rp 700.000.000',
                    'activities': ['Kapal', 'Teknologi', 'Pelatihan']
                },
                'program_perikanan': {
                    'description': 'Program perikanan',
                    'target': 'Pembudaya ikan',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Bibit', 'Teknologi', 'Pemasaran']
                }
            }
        elif 'Tenaga Kerja dan Transmigrasi' in ministry_name:
            programs = {
                'program_tenaga_kerja': {
                    'description': 'Program tenaga kerja',
                    'target': 'Pencari kerja',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Pelatihan', 'Penempatan', 'Bursa kerja']
                },
                'program_transmigrasi': {
                    'description': 'Program transmigrasi',
                    'target': 'Transmigran',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Relokasi', 'Perumahan', 'Pemberdayaan']
                }
            }
        elif 'Pariwisata dan Ekonomi Kreatif' in ministry_name:
            programs = {
                'program_pariwisata': {
                    'description': 'Program pariwisata',
                    'target': 'Pengusaha pariwisata',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Promosi', 'Event', 'Pengembangan']
                },
                'program_ekonomi_kreatif': {
                    'description': 'Program ekonomi kreatif',
                    'target': 'Pelaku ekonomi kreatif',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Pelatihan', 'Modal', 'Pemasaran']
                }
            }
        elif 'Komunikasi dan Informatika' in ministry_name:
            programs = {
                'program_komunikasi': {
                    'description': 'Program komunikasi',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Jaringan', 'Aplikasi', 'Edukasi']
                },
                'program_informatika': {
                    'description': 'Program informatika',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Digitalisasi', 'Pelatihan', 'Pengembangan']
                }
            }
        elif 'Koperasi dan UKM' in ministry_name:
            programs = {
                'program_koperasi': {
                    'description': 'Program koperasi',
                    'target': 'Anggota koperasi',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Pendampingan', 'Pelatihan', 'Modal']
                },
                'program_ukm': {
                    'description': 'Program UKM',
                    'target': 'Pengusaha kecil',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Pelatihan', 'Modal', 'Pemasaran']
                }
            }
        elif 'Pemberdayaan Perempuan dan Perlindungan Anak' in ministry_name:
            programs = {
                'program_perempuan': {
                    'description': 'Program pemberdayaan perempuan',
                    'target': 'Perempuan',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Pelatihan', 'Modal', 'Pemberdayaan']
                },
                'program_anak': {
                    'description': 'Program perlindungan anak',
                    'target': 'Anak',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Perlindungan', 'Pendidikan', 'Kesehatan']
                }
            }
        elif 'Pemuda dan Olahraga' in ministry_name:
            programs = {
                'program_pemuda': {
                    'description': 'Program pemuda',
                    'target': 'Pemuda',
                    'duration': 'Tahunan',
                    'budget': 'Rp 700.000.000',
                    'activities': ['Pelatihan', 'Organisasi', 'Pemberdayaan']
                },
                'program_olahraga': {
                    'description': 'Program olahraga',
                    'target': 'Atlet',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Fasilitas', 'Pelatihan', 'Kompetisi']
                }
            }
        elif 'Agama' in ministry_name:
            programs = {
                'program_agama': {
                    'description': 'Program agama',
                    'target': 'Umat beragama',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Pendidikan', 'Bantuan', 'Fasilitas']
                },
                'program_tempat_ibadah': {
                    'description': 'Program tempat ibadah',
                    'target': 'Pengurus tempat ibadah',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Renovasi', 'Bantuan', 'Pelatihan']
                }
            }
        elif 'Luar Negeri' in ministry_name:
            programs = {
                'program_paspor': {
                    'description': 'Program paspor',
                    'target': 'Warga negara',
                    'duration': 'Tahunan',
                    'budget': 'Rp 400.000.000',
                    'activities': ['Penerbitan', 'Perpanjangan', 'Penggantian']
                },
                'program_konsuler': {
                    'description': 'Program konsuler',
                    'target': 'WNI di luar negeri',
                    'duration': 'Tahunan',
                    'budget': 'Rp 600.000.000',
                    'activities': ['Bantuan', 'Perlindungan', 'Edukasi']
                }
            }
        elif 'Pertahanan' in ministry_name:
            programs = {
                'program_pertahanan': {
                    'description': 'Program pertahanan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Edukasi', 'Pelatihan', 'Simulasi']
                },
                'program_wajib_militer': {
                    'description': 'Program wajib militer',
                    'target': 'Pemuda',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Pendaftaran', 'Pelatihan', 'Penempatan']
                }
            }
        elif 'BUMN' in ministry_name:
            programs = {
                'program_bumn': {
                    'description': 'Program BUMN',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 2.000.000.000',
                    'activities': ['Layanan', 'Investasi', 'Bantuan']
                },
                'program_investasi': {
                    'description': 'Program investasi BUMN',
                    'target': 'Investor',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.500.000.000',
                    'activities': ['Promosi', 'Fasilitasi', 'Monitoring']
                }
            }
        elif 'Investasi' in ministry_name:
            programs = {
                'program_investasi': {
                    'description': 'Program investasi',
                    'target': 'Investor',
                    'duration': 'Tahunan',
                    'budget': 'Rp 1.000.000.000',
                    'activities': ['Promosi', 'Fasilitasi', 'Monitoring']
                },
                'program_izin_investasi': {
                    'description': 'Program izin investasi',
                    'target': 'Investor',
                    'duration': 'Tahunan',
                    'budget': 'Rp 800.000.000',
                    'activities': ['Perizinan', 'Fasilitasi', 'Monitoring']
                }
            }
        else:
            # Generic programs for other ministries
            programs = {
                'program_pelayanan': {
                    'description': 'Program pelayanan',
                    'target': 'Masyarakat',
                    'duration': 'Tahunan',
                    'budget': 'Rp 500.000.000',
                    'activities': ['Pelayanan', 'Edukasi', 'Monitoring']
                },
                'program_inovasi': {
                    'description': 'Program inovasi',
                    'target': 'Internal dan eksternal',
                    'duration': 'Tahunan',
                    'budget': 'Rp 300.000.000',
                    'activities': ['Digitalisasi', 'Sistem informasi', 'Inovasi']
                }
            }
        
        return programs
    
    def _generate_budget_data(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate budget data (simulated data)
        """
        budget = {
            'annual_budget': {
                'total': 500000000 + (hash(ministry_name) % 2000000000),
                'personnel': 0.4,
                'operational': 0.3,
                'investment': 0.2,
                'program': 0.1
            },
            'quarterly_budget': {
                'Q1': 125000000 + (hash(ministry_name + 'Q1') % 500000000),
                'Q2': 125000000 + (hash(ministry_name + 'Q2') % 500000000),
                'Q3': 125000000 + (hash(ministry_name + 'Q3') % 500000000),
                'Q4': 125000000 + (hash(ministry_name + 'Q4') % 500000000)
            },
            'budget_sources': [
                'APBN',
                'DAU',
                'Dana Pinjaman',
                'Hibah',
                'Pendapatan Asli Daerah'
            ],
            'budget_utilization': {
                'realized': 85 + (hash(ministry_name) % 10),
                'target': 100,
                'variance': 15 - (hash(ministry_name) % 10)
            }
        }
        
        return budget
    
    def _generate_facilities_data(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate facilities data (simulated data)
        """
        facilities = {
            'kantor_utama': {
                'name': f'Kantor {ministry_name} Wilayah {region_config["name"]}',
                'address': f'Jl. {self._get_street_name()} No. {hash(ministry_name) % 100}, {region_config["capital"]}',
                'building_type': 'Kantor Pemerintah',
                'area_m2': 800 + (hash(ministry_name) % 1000),
                'year_built': 2005 + (hash(ministry_name) % 15),
                'condition': 'Baik',
                'ownership': 'Milik Pemerintah'
            },
            'unit_layanan': [
                {
                    'name': f'Unit Pelayanan {self._get_ministry_focus(ministry_name)} I',
                    'location': 'Lantai 1',
                    'area_m2': 100 + (hash(ministry_name + 'unit1') % 50),
                    'capacity': 30,
                    'facilities': ['AC', 'Meja', 'Kursi', 'Komputer', 'Printer']
                },
                {
                    'name': f'Unit Pelayanan {self._get_ministry_focus(ministry_name)} II',
                    'location': 'Lantai 2',
                    'area_m2': 100 + (hash(ministry_name + 'unit2') % 50),
                    'capacity': 30,
                    'facilities': ['AC', 'Meja', 'Kursi', 'Komputer', 'Printer']
                }
            ],
            'fasilitas_penunjang': [
                {
                    'name': 'Ruang Rapat',
                    'capacity': 50,
                    'facilities': ['AC', 'Proyektor', 'Sound System', 'Whiteboard']
                },
                {
                    'name': 'Ruang Arsip',
                    'area_m2': 50 + (hash(ministry_name + 'arsip') % 30),
                    'facilities': ['Rak Arsip', 'AC', 'Keamanan']
                },
                {
                    'name': 'Parkir Kendaraan',
                    'capacity': 80,
                    'area_m2': 300 + (hash(ministry_name + 'parkir') % 100),
                    'facilities': ['Canopy', 'Security', 'CCTV']
                }
            ]
        }
        
        return facilities
    
    def _generate_performance_data(self, ministry_name: str, region_config: Dict) -> Dict:
        """
        Generate performance data (simulated data)
        """
        performance = {
            'service_metrics': {
                'total_requests': 2000 + (hash(ministry_name) % 5000),
                'completed_requests': 1700 + (hash(ministry_name + 'completed') % 4500),
                'completion_rate': 85 + (hash(ministry_name) % 10),
                'average_processing_time': 7 + (hash(ministry_name) % 10),
                'satisfaction_score': 4.3 + (hash(ministry_name) % 8) / 10
            },
            'operational_metrics': {
                'employee_productivity': 87 + (hash(ministry_name + 'productivity') % 10),
                'budget_utilization': 88 + (hash(ministry_name + 'utilization') % 10),
                'program_implementation': 85 + (hash(ministry_name + 'program') % 15),
                'innovation_index': 72 + (hash(ministry_name + 'innovation') % 20)
            },
            'quality_metrics': {
                'service_quality': 4.4 + (hash(ministry_name + 'quality') % 7) / 10,
                'compliance_rate': 91 + (hash(ministry_name + 'compliance') % 8),
                'error_rate': 4 - (hash(ministry_name + 'error') % 3),
                'response_time': 2 + (hash(ministry_name + 'response') % 3)
            },
            'strategic_metrics': {
                'goal_achievement': 86 + (hash(ministry_name + 'goal') % 10),
                'stakeholder_satisfaction': 4.2 + (hash(ministry_name + 'stakeholder') % 8) / 10,
                'sustainability_index': 76 + (hash(ministry_name + 'sustainability') % 15),
                'digital_transformation': 71 + (hash(ministry_name + 'digital') % 20)
            }
        }
        
        return performance
    
    def _calculate_office_count(self, ministry_name: str, region_config: Dict) -> int:
        """
        Calculate office count based on ministry type and region
        """
        base_counts = {
            'Kementerian Dalam Negeri': 5,
            'Kementerian Hukum dan HAM': 4,
            'Kementerian Keuangan': 4,
            'Kementerian Pendidikan dan Kebudayaan': 6,
            'Kementerian Kesehatan': 5,
            'Kementerian Sosial': 4,
            'Kementerian Perhubungan': 4,
            'Kementerian Pekerjaan Umum dan Perumahan Rakyat': 5,
            'Kementerian Pertanian': 4,
            'Kementerian Perindustrian': 3,
            'Kementerian Perdagangan': 3,
            'Kementerian Lingkungan Hidup dan Kehutanan': 4,
            'Kementerian Kelautan dan Perikanan': 3,
            'Kementerian Tenaga Kerja dan Transmigrasi': 4,
            'Kementerian Pariwisata dan Ekonomi Kreatif': 3,
            'Kementerian Komunikasi dan Informatika': 4,
            'Kementerian Koperasi dan UKM': 3,
            'Kementerian Pemberdayaan Perempuan dan Perlindungan Anak': 3,
            'Kementerian Pemuda dan Olahraga': 3,
            'Kementerian Agama': 4,
            'Kementerian Luar Negeri': 2,
            'Kementerian Pertahanan': 3,
            'Kementerian BUMN': 2,
            'Kementerian Investasi': 2
        }
        
        base_count = base_counts.get(ministry_name, 3)
        
        # Adjust based on region size
        region_multiplier = {
            'kota_serang': 1.2,
            'kabupaten_serang': 1.5,
            'kota_cilegon': 1.0,
            'kota_tangerang': 1.8,
            'kabupaten_tangerang': 1.6,
            'kabupaten_lebak': 1.3,
            'kabupaten_pandeglang': 1.4,
            'kabupaten_tangerang_selatan': 1.7
        }
        
        # Get region key from region_config
        region_key = region_config.get('region_key', 'unknown')
        multiplier = region_multiplier.get(region_key, 1.0)
        
        return int(base_count * multiplier)
    
    def _calculate_employee_count(self, ministry_name: str, region_config: Dict) -> int:
        """
        Calculate employee count based on ministry type and region
        """
        base_counts = {
            'Kementerian Dalam Negeri': 200,
            'Kementerian Hukum dan HAM': 150,
            'Kementerian Keuangan': 180,
            'Kementerian Pendidikan dan Kebudayaan': 250,
            'Kementerian Kesehatan': 220,
            'Kementerian Sosial': 160,
            'Kementerian Perhubungan': 170,
            'Kementerian Pekerjaan Umum dan Perumahan Rakyat': 200,
            'Kementerian Pertanian': 140,
            'Kementerian Perindustrian': 100,
            'Kementerian Perdagangan': 90,
            'Kementerian Lingkungan Hidup dan Kehutanan': 120,
            'Kementerian Kelautan dan Perikanan': 80,
            'Kementerian Tenaga Kerja dan Transmigrasi': 130,
            'Kementerian Pariwisata dan Ekonomi Kreatif': 70,
            'Kementerian Komunikasi dan Informatika': 100,
            'Kementerian Koperasi dan UKM': 60,
            'Kementerian Pemberdayaan Perempuan dan Perlindungan Anak': 80,
            'Kementerian Pemuda dan Olahraga': 70,
            'Kementerian Agama': 90,
            'Kementerian Luar Negeri': 50,
            'Kementerian Pertahanan': 80,
            'Kementerian BUMN': 40,
            'Kementerian Investasi': 30
        }
        
        base_count = base_counts.get(ministry_name, 100)
        
        # Adjust based on region size
        region_multiplier = {
            'kota_serang': 1.2,
            'kabupaten_serang': 1.5,
            'kota_cilegon': 1.0,
            'kota_tangerang': 1.8,
            'kabupaten_tangerang': 1.6,
            'kabupaten_lebak': 1.3,
            'kabupaten_pandeglang': 1.4,
            'kabupaten_tangerang_selatan': 1.7
        }
        
        # Get region key from region_config
        region_key = region_config.get('region_key', 'unknown')
        multiplier = region_multiplier.get(region_key, 1.0)
        
        return int(base_count * multiplier)
    
    def _get_ministry_abbreviation(self, ministry_name: str) -> str:
        """
        Get ministry abbreviation
        """
        abbreviations = {
            'Kementerian Dalam Negeri': 'Kemendagri',
            'Kementerian Hukum dan HAM': 'Kemenkumham',
            'Kementerian Keuangan': 'Kemenkeu',
            'Kementerian Pendidikan dan Kebudayaan': 'Kemendikbud',
            'Kementerian Kesehatan': 'Kemenkes',
            'Kementerian Sosial': 'Kemensos',
            'Kementerian Perhubungan': 'Kemenhub',
            'Kementerian Pekerjaan Umum dan Perumahan Rakyat': 'KemenPU-PR',
            'Kementerian Pertanian': 'Kementan',
            'Kementerian Perindustrian': 'Kemenperin',
            'Kementerian Perdagangan': 'Kemendag',
            'Kementerian Lingkungan Hidup dan Kehutanan': 'KLHK',
            'Kementerian Kelautan dan Perikanan': 'KKP',
            'Kementerian Tenaga Kerja dan Transmigrasi': 'Kemnakertrans',
            'Kementerian Pariwisata dan Ekonomi Kreatif': 'Kemenparekraf',
            'Kementerian Komunikasi dan Informatika': 'Kominfo',
            'Kementerian Koperasi dan UKM': 'Kemenkopukm',
            'Kementerian Pemberdayaan Perempuan dan Perlindungan Anak': 'Kemenpppa',
            'Kementerian Pemuda dan Olahraga': 'Kemenpora',
            'Kementerian Agama': 'Kemenag',
            'Kementerian Luar Negeri': 'Kemenlu',
            'Kementerian Pertahanan': 'Kemenhan',
            'Kementerian BUMN': 'Kemenbumn',
            'Kementerian Investasi': 'BKPM'
        }
        
        return abbreviations.get(ministry_name, ministry_name[:8])
    
    def _get_ministry_type(self, ministry_name: str) -> str:
        """
        Get ministry type
        """
        if 'Dalam Negeri' in ministry_name:
            return 'Administrasi Pemerintahan'
        elif 'Hukum dan HAM' in ministry_name:
            return 'Hukum dan Hak Asasi Manusia'
        elif 'Keuangan' in ministry_name:
            return 'Keuangan dan Anggaran'
        elif 'Pendidikan dan Kebudayaan' in ministry_name:
            return 'Pendidikan dan Kebudayaan'
        elif 'Kesehatan' in ministry_name:
            return 'Kesehatan'
        elif 'Sosial' in ministry_name:
            return 'Sosial'
        elif 'Perhubungan' in ministry_name:
            return 'Perhubungan'
        elif 'Pekerjaan Umum dan Perumahan Rakyat' in ministry_name:
            return 'Infrastruktur dan Perumahan'
        elif 'Pertanian' in ministry_name:
            return 'Pertanian'
        elif 'Perindustrian' in ministry_name:
            return 'Perindustrian'
        elif 'Perdagangan' in ministry_name:
            return 'Perdagangan'
        elif 'Lingkungan Hidup dan Kehutanan' in ministry_name:
            return 'Lingkungan Hidup dan Kehutanan'
        elif 'Kelautan dan Perikanan' in ministry_name:
            return 'Kelautan dan Perikanan'
        elif 'Tenaga Kerja dan Transmigrasi' in ministry_name:
            return 'Tenaga Kerja'
        elif 'Pariwisata dan Ekonomi Kreatif' in ministry_name:
            return 'Pariwisata dan Ekonomi Kreatif'
        elif 'Komunikasi dan Informatika' in ministry_name:
            return 'Komunikasi dan Informatika'
        elif 'Koperasi dan UKM' in ministry_name:
            return 'Koperasi dan UKM'
        elif 'Pemberdayaan Perempuan dan Perlindungan Anak' in ministry_name:
            return 'Pemberdayaan Perempuan dan Perlindungan Anak'
        elif 'Pemuda dan Olahraga' in ministry_name:
            return 'Pemuda dan Olahraga'
        elif 'Agama' in ministry_name:
            return 'Agama'
        elif 'Luar Negeri' in ministry_name:
            return 'Luar Negeri'
        elif 'Pertahanan' in ministry_name:
            return 'Pertahanan'
        elif 'BUMN' in ministry_name:
            return 'Badan Usaha Milik Negara'
        elif 'Investasi' in ministry_name:
            return 'Investasi'
        else:
            return 'Administrasi Umum'
    
    def _get_ministry_functions(self, ministry_name: str) -> List[str]:
        """
        Get ministry functions
        """
        if 'Dalam Negeri' in ministry_name:
            return ['Administrasi pemerintahan', 'Pelayanan publik', 'Koordinasi pemerintahan']
        elif 'Hukum dan HAM' in ministry_name:
            return ['Bantuan hukum', 'Perlindungan HAM', 'Notaris']
        elif 'Keuangan' in ministry_name:
            return ['Perpajakan', 'Anggaran', 'Keuangan']
        elif 'Pendidikan dan Kebudayaan' in ministry_name:
            return ['Pendidikan', 'Kebudayaan', 'Beasiswa']
        elif 'Kesehatan' in ministry_name:
            return ['Pelayanan kesehatan', 'BPJS', 'Vaksinasi']
        elif 'Sosial' in ministry_name:
            return ['Bantuan sosial', 'Pemberdayaan', 'Perlindungan']
        elif 'Perhubungan' in ministry_name:
            return ['Perizinan kendaraan', 'Uji kir', 'Angkutan']
        elif 'Pekerjaan Umum dan Perumahan Rakyat' in ministry_name:
            return ['Perizinan bangunan', 'Perumahan', 'Infrastruktur']
        elif 'Pertanian' in ministry_name:
            return ['Pertanian', 'Perkebunan', 'Peternakan']
        elif 'Perindustrian' in ministry_name:
            return ['Perizinan industri', 'Standar industri', 'UMKM']
        elif 'Perdagangan' in ministry_name:
            return ['Perizinan dagang', 'Pasar', 'Pengawasan harga']
        elif 'Lingkungan Hidup dan Kehutanan' in ministry_name:
            return ['Lingkungan', 'Kehutanan', 'Penghijauan']
        elif 'Kelautan dan Perikanan' in ministry_name:
            return ['Kelautan', 'Perikanan', 'Aquaculture']
        elif 'Tenaga Kerja dan Transmigrasi' in ministry_name:
            return ['Tenaga kerja', 'Pelatihan', 'Transmigrasi']
        elif 'Pariwisata dan Ekonomi Kreatif' in ministry_name:
            return ['Pariwisata', 'Ekonomi kreatif', 'Event']
        elif 'Komunikasi dan Informatika' in ministry_name:
            return ['Komunikasi', 'Informatika', 'Statistik']
        elif 'Koperasi dan UKM' in ministry_name:
            return ['Koperasi', 'UKM', 'Modal']
        elif 'Pemberdayaan Perempuan dan Perlindungan Anak' in ministry_name:
            return ['Pemberdayaan perempuan', 'Perlindungan anak', 'KDRT']
        elif 'Pemuda dan Olahraga' in ministry_name:
            return ['Pemberdayaan pemuda', 'Olahraga', 'Fasilitas']
        elif 'Agama' in ministry_name:
            return ['Pendidikan agama', 'Tempat ibadah', 'Bantuan agama']
        elif 'Luar Negeri' in ministry_name:
            return ['Paspor', 'Visa', 'Konsuler']
        elif 'Pertahanan' in ministry_name:
            return ['Pertahanan', 'Wajib militer', 'Cadangan']
        elif 'BUMN' in ministry_name:
            return ['Layanan BUMN', 'Investasi', 'Bantuan']
        elif 'Investasi' in ministry_name:
            return ['Investasi', 'Izin investasi', 'Fasilitasi']
        else:
            return ['Pelayanan umum', 'Administrasi', 'Koordinasi']
    
    def _get_ministry_focus(self, ministry_name: str) -> str:
        """
        Get ministry focus area
        """
        if 'Dalam Negeri' in ministry_name:
            return 'administrasi pemerintahan'
        elif 'Hukum dan HAM' in ministry_name:
            return 'hukum dan hak asasi manusia'
        elif 'Keuangan' in ministry_name:
            return 'keuangan dan anggaran'
        elif 'Pendidikan dan Kebudayaan' in ministry_name:
            return 'pendidikan dan kebudayaan'
        elif 'Kesehatan' in ministry_name:
            return 'kesehatan masyarakat'
        elif 'Sosial' in ministry_name:
            return 'kesejahteraan sosial'
        elif 'Perhubungan' in ministry_name:
            return 'transportasi dan lalu lintas'
        elif 'Pekerjaan Umum dan Perumahan Rakyat' in ministry_name:
            return 'pekerjaan umum dan perumahan'
        elif 'Pertanian' in ministry_name:
            return 'pertanian dan perkebunan'
        elif 'Perindustrian' in ministry_name:
            return 'perindustrian dan perdagangan'
        elif 'Perdagangan' in ministry_name:
            return 'perdagangan dan ekonomi'
        elif 'Lingkungan Hidup dan Kehutanan' in ministry_name:
            return 'lingkungan hidup dan kehutanan'
        elif 'Kelautan dan Perikanan' in ministry_name:
            return 'kelautan dan perikanan'
        elif 'Tenaga Kerja dan Transmigrasi' in ministry_name:
            return 'tenaga kerja dan transmigrasi'
        elif 'Pariwisata dan Ekonomi Kreatif' in ministry_name:
            return 'pariwisata dan ekonomi kreatif'
        elif 'Komunikasi dan Informatika' in ministry_name:
            return 'komunikasi dan informatika'
        elif 'Koperasi dan UKM' in ministry_name:
            return 'koperasi dan usaha kecil menengah'
        elif 'Pemberdayaan Perempuan dan Perlindungan Anak' in ministry_name:
            return 'pemberdayaan perempuan dan perlindungan anak'
        elif 'Pemuda dan Olahraga' in ministry_name:
            return 'pemuda dan olahraga'
        elif 'Agama' in ministry_name:
            return 'pendidikan agama dan tempat ibadah'
        elif 'Luar Negeri' in ministry_name:
            return 'hubungan luar negeri'
        elif 'Pertahanan' in ministry_name:
            return 'pertahanan dan keamanan'
        elif 'BUMN' in ministry_name:
            return 'badan usaha milik negara'
        elif 'Investasi' in ministry_name:
            return 'investasi dan ekonomi'
        else:
            return 'pelayanan publik'
    
    def _get_indonesian_name(self) -> str:
        """
        Generate Indonesian name
        """
        first_names = [
            'Ahmad', 'Budi', 'Dedi', 'Eko', 'Fajar', 'Gunawan', 'Hadi', 'Iwan',
            'Joko', 'Kusnadi', 'Lukman', 'Muhammad', 'Nur', 'Omar', 'Prasetyo',
            'Rahmat', 'Sukirman', 'Toto', 'Umar', 'Victor', 'Wahyu', 'Xaverius',
            'Yudi', 'Zainal', 'Aisyah', 'Dewi', 'Fitri', 'Gustina', 'Hartini',
            'Indah', 'Julia', 'Kartika', 'Lestari', 'Mawar', 'Nuraini', 'Oktavia',
            'Putri', 'Qori', 'Ratna', 'Siti', 'Tuti', 'Umi', 'Vera', 'Wati',
            'Yuni', 'Zahra'
        ]
        
        last_names = [
            'Saputra', 'Wijaya', 'Putra', 'Santoso', 'Gunawan', 'Prasetyo',
            'Hidayat', 'Raharjo', 'Sutrisno', 'Kusumo', 'Wibowo', 'Siregar',
            'Nugroho', 'Setiawan', 'Hidayatullah', 'Fauzi', 'Abdullah',
            'Rahmawati', 'Sari', 'Putri', 'Dewi', 'Susanti', 'Wulandari',
            'Safitri', 'Permata', 'Kirana', 'Cahyani', 'Puspita', 'Anggraini',
            'Kusumawati', 'Rahayu', 'Sukma', 'Mulyani', 'Wardani', 'Sulistyaningsih'
        ]
        
        return f"{first_names[hash('first') % len(first_names)]} {last_names[hash('last') % len(last_names)]}"
    
    def _get_phone_code(self, region_name: str) -> str:
        """
        Get phone code for region
        """
        phone_codes = {
            'Kota Serang': '254',
            'Kabupaten Serang': '254',
            'Kota Cilegon': '254',
            'Kota Tangerang': '21',
            'Kabupaten Tangerang': '21',
            'Kabupaten Lebak': '252',
            'Kabupaten Pandeglang': '252',
            'Kabupaten Tangerang Selatan': '21'
        }
        
        return phone_codes.get(region_name, '254')
    
    def _get_street_name(self) -> str:
        """
        Generate street name
        """
        streets = [
            'Sudirman', 'Ahmad Yani', 'Gatot Subroto', 'Thamrin', 'M.H. Thamrin',
            'Veteran', 'Diponegoro', 'Pahlawan', 'Kartini', 'R.A. Kartini',
            'Pemuda', 'Merdeka', 'Juanda', 'Irian Jaya', 'Siliwangi',
            'Sukarno-Hatta', 'Bromo', 'Krakatau', 'Ankasa', 'Raden Inten',
            'K.H. Ahmad Dahlan', 'HOS Cokroaminoto', 'Ki Hajar Dewantara',
            'R.A. Kartini', 'Cut Nyak Dien', 'Sultan Agung', 'Sultan Hasanuddin'
        ]
        
        return streets[hash('street') % len(streets)]
    
    def _save_comprehensive_data(self, data: Dict):
        """
        Save comprehensive data
        """
        # Save as JSON
        json_file = os.path.join(self.data_dir, 'banten_ministry_comprehensive_data.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save as CSV for analysis
        csv_file = os.path.join(self.data_dir, 'banten_ministry_data_summary.csv')
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Region', 'Ministry', 'Office Count', 'Employee Count',
                'Services Count', 'Programs Count', 'Budget (Million)', 'Contact Phone', 'Website'
            ])
            
            # Write data
            for region_key, region_data in data['regions'].items():
                region_name = region_data['region_name']
                
                for ministry_name, ministry_data in region_data['ministries'].items():
                    writer.writerow([
                        region_name,
                        ministry_name,
                        ministry_data.get('office_count', 0),
                        ministry_data.get('employee_count', 0),
                        len(ministry_data.get('services', {})),
                        len(ministry_data.get('programs', {})),
                        ministry_data.get('budget', {}).get('annual_budget', {}).get('total', 0) // 1000000,
                        ministry_data.get('contact_info', {}).get('phone_office', ''),
                        ministry_data.get('contact_info', {}).get('website', '')
                    ])
        
        self.logger.info(f"Banten ministry data saved to {json_file} and {csv_file}")
    
    def _generate_intelligence_report(self, data: Dict):
        """
        Generate intelligence report
        """
        report_content = f"""# BANTEN MINISTRY INTELLIGENCE REPORT
============================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Regions: {', '.join(data['target_regions'])}

## PROVINCIAL OVERVIEW
- **Province**: Banten
- **Capital**: Serang
- **Population**: {data['summary']['provincial_info']['population']:,}
- **Area**: {data['summary']['provincial_info']['area_km2']} km²
- **Governor**: {data['summary']['provincial_info']['governor']}
- **Established**: {data['summary']['provincial_info']['established_year']}

## REGIONAL OVERVIEW

"""
        
        for region_key, region_data in data['regions'].items():
            region_name = region_data['region_name']
            region_type = region_data['region_info']['type']
            capital = region_data['region_info']['capital']
            population = region_data['region_info']['population']
            area = region_data['region_info']['area_km2']
            total_ministries = region_data['total_ministries']
            total_offices = region_data['total_offices']
            total_employees = region_data['total_employees']
            total_data_points = region_data['total_data_points']
            
            report_content += f"""
### {region_name} ({region_type})
- **Capital**: {capital}
- **Population**: {population:,}
- **Area**: {area} km²
- **Total Ministries**: {total_ministries}
- **Total Offices**: {total_offices}
- **Total Employees**: {total_employees:,}
- **Data Points**: {total_data_points}

**Districts**: {', '.join(region_data['region_info']['districts'])}

**Top Ministries by Employee Count**:
"""
            
            # Show top 5 ministries by employee count
            ministries_list = list(region_data['ministries'].items())
            ministries_list.sort(key=lambda x: x[1].get('employee_count', 0), reverse=True)
            
            for ministry_name, ministry_data in ministries_list[:5]:
                report_content += f"- **{ministry_name}**: {ministry_data.get('employee_count', 0):,} employees\n"
            
            report_content += "\n"
        
        report_content += """
## STRATEGIC INSIGHTS

### Government Structure Analysis
- **Decentralization**: Strong regional autonomy with comprehensive local government structure
- **Service Coverage**: Extensive service coverage across all administrative levels
- **Resource Allocation**: Budget allocation prioritized based on regional needs
- **Human Resources**: Significant government workforce across all regions

### Service Delivery Analysis
- **Service Types**: Comprehensive service portfolio covering all citizen needs
- **Digital Transformation**: Growing digital service adoption across departments
- **Citizen Engagement**: Multiple channels for citizen interaction and feedback
- **Performance Metrics**: Established performance monitoring and evaluation systems

### Opportunities for Collaboration
- **Public-Private Partnerships**: Opportunities for collaboration in infrastructure and services
- **Technology Integration**: Digital transformation opportunities across government departments
- **Community Development**: Programs for community empowerment and economic development
- **Investment Opportunities**: Infrastructure development and service improvement projects

## RECOMMENDATIONS

1. **Digital Transformation**: Accelerate digital service delivery across all departments
2. **Inter-District Coordination**: Strengthen coordination between districts for better service delivery
3. **Performance Monitoring**: Implement comprehensive performance monitoring systems
4. **Citizen Engagement**: Enhance citizen engagement through digital platforms
5. **Resource Optimization**: Optimize resource allocation based on service demand

---
*Report generated by Banten Ministry Intelligence Scout*
"""
        
        # Save report
        report_file = os.path.join(self.reports_dir, 'banten_ministry_intelligence_report.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"Banten ministry intelligence report saved to {report_file}")

# Global instance
banten_ministry_scout = BantenMinistryScout()

def collect_banten_ministry_intelligence(target_regions: List[str] = None) -> Dict:
    """
    Collect comprehensive Banten ministry intelligence
    """
    return banten_ministry_scout.collect_all_banten_ministry_data(target_regions)

def get_region_summary(region_name: str) -> Dict:
    """
    Get summary for specific region
    """
    region_key = region_name.lower().replace(' ', '_').replace('kota_', '').replace('kabupaten_', '')
    if region_key in banten_ministry_scout.banten_regions:
        return banten_ministry_scout.banten_regions[region_key]
    return {}

if __name__ == "__main__":
    # Test the Banten ministry scout
    print("🏛️ Starting Banten Ministry Intelligence Scout...")
    
    # Collect data for major regions
    regions = ['kota_serang', 'kabupaten_serang', 'kota_cilegon']
    data = collect_banten_ministry_intelligence(regions)
    
    print(f"✅ Banten ministry data collection completed!")
    print(f"📊 Total data points: {data['summary']['total_data_points']}")
    print(f"🏛️ Ministries analyzed: {data['summary']['total_ministries']}")
    print(f"👥 Total employees: {data['summary']['total_employees']:,}")
    print(f"🗺️ Regions covered: {data['summary']['total_regions']}")
    print(f"📋 Report saved to: reports/banten_ministry_intelligence_report.md")
    print(f"💾 Data saved to: data/banten_ministry_comprehensive_data.json")

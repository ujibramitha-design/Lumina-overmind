"""
LUMINA OS - ADVANCED MASS SCOUT MODULE
=========================================

Advanced Intelligence & Google Dorking System
Military-grade reconnaissance with advanced search operators

Features:
- Google Dork Generator with 4 lethal search modes
- Advanced Search Operators for precise targeting
- Social media extraction (LinkedIn, Twitter, Forum)
- Competitor intelligence gathering
- Life events targeting
- Campaign source tracking
- SQLite/Supabase integration
- Command Line ready execution
"""

import os
import sys

import json
import asyncio
import logging
import re
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import requests

# Import Telecom HLR Database
try:
    from .telecom_hlr_db import INDONESIA_HLR_MAPPING, get_region_prefixes, get_provider_from_prefix, get_region_from_prefix
except ImportError:
    # Fallback if telecom_hlr_db not available
    INDONESIA_HLR_MAPPING = {}
    def get_region_prefixes(region, provider=None):
        return []
    def get_provider_from_prefix(prefix):
        return 'unknown'
    def get_region_from_prefix(prefix):
        return 'unknown'

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)

# Import BeautifulSoup
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    os.system("pip install beautifulsoup4")
    from bs4 import BeautifulSoup

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

class AdvancedTripwireScout:
    """
    Advanced Tripwire Scout - Military-grade reconnaissance system
    Specialized in Google Dorking and advanced intelligence gathering
    """
    
    def __init__(self):
        """Initialize Advanced Tripwire Scout"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize database connection
        try:
            from core_modules.db_manager_supabase import get_supabase_manager
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Advanced Scout: Database connected for intelligence gathering{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Advanced Scout: Database connection failed: {e}{END}")
        
        # Initialize Telegram sender for notifications
        try:
            from core_modules.notifications.telegram_sender import get_telegram_sender
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Advanced Scout: Telegram sender initialized{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Advanced Scout: Telegram sender failed: {e}{END}")
        
        # Search configuration for advanced dorking
        self.search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # Advanced contact extraction patterns
        self.phone_patterns = [
            r'\+62[0-9]{9,12}',  # +62xxxxxxxxx
            r'62[0-9]{9,12}',   # 62xxxxxxxxx
            r'08[0-9]{8,11}',   # 08xxxxxxxxx
            r'021[0-9]{7,10}',  # Jakarta landline
            r'022[0-9]{7,10}',  # Bandung landline
            r'031[0-9]{7,10}',  # Semarang landline
            r'024[0-9]{7,10}',  # Surabaya landline
            r'0[0-9]{9,12}',   # General landline
        ]
        
        self.email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        ]
        
        # Social media patterns for extraction
        self.social_patterns = {
            'linkedin': [
                r'linkedin\.com/in/([a-zA-Z0-9-]+)',
                r'linkedin\.com/company/([a-zA-Z0-9-]+)',
            ],
            'twitter': [
                r'twitter\.com/([a-zA-Z0-9_]+)',
                r'x\.com/([a-zA-Z0-9_]+)',
            ],
            'facebook': [
                r'facebook\.com/([a-zA-Z0-9.]+)',
                r'fb\.com/([a-zA-Z0-9.]+)',
            ],
            'instagram': [
                r'instagram\.com/([a-zA-Z0-9_.]+)',
            ],
            'forum': [
                r'kaskus\.co\.id/threads/([a-zA-Z0-9-]+)',
                r'forum\.([a-zA-Z0-9.-]+)',
            ]
        }
        
        self.logger.info(f"{CYAN}🔍 ADVANCED TRIPWIRE SCOUT: Military-grade reconnaissance system initialized{END}")
        self.logger.info(f"{GREEN}✅ Ready for Google Dorking and advanced intelligence gathering{END}")
    
    def generate_dork_queries(self, campaign_mode: str, area: str = "", competitors: List[str] = None) -> List[str]:
        """
        Generate Advanced Search Operator queries based on campaign mode
        
        Args:
            campaign_mode: Campaign mode (ORGANIC_SOSMED, HEADHUNTER, COMPETITOR_INTERCEPT, LIFE_EVENTS)
            area: Geographic area to focus on
            competitors: List of competitor names for COMPETITOR_INTERCEPT mode
            
        Returns:
            List of advanced search operator queries
        """
        try:
            self.logger.info(f"{BLUE}🔍 GENERATING DORK QUERIES{END}")
            self.logger.info(f"{CYAN}⚔️ Campaign Mode: {campaign_mode}{END}")
            self.logger.info(f"{CYAN}📍 Area: {area if area else 'All areas'}{END}")
            
            dork_queries = []
            base_queries = []
            
            if campaign_mode == "ORGANIC_SOSMED":
                # Organic social media dorks
                base_queries = [
                    f'site:twitter.com OR site:facebook.com "rekomendasi rumah" {area} -loker -lowongan',
                    f'site:instagram.com "cari rumah" {area} -jual -beli',
                    f'site:kaskus.co.id "pengalaman beli rumah" {area} -iklan',
                    f'site:facebook.com/groups "rumah dijual" {area} -agent -broker',
                    f'site:twitter.com "review properti" {area} -spam',
                    f'site:reddit.com/r/properti "cari kos" {area} -apartment',
                    f'site:facebook.com "testimoni developer" {area} -scam',
                    f'site:twitter.com OR site:facebook.com "rumah subsidi" {area} -bpjs',
                    f'site:forum "tips beli rumah" {area} -kpr -bank',
                    f'site:linkedin.com "property investment" {area} -job -hiring',
                ]
                
            elif campaign_mode == "HEADHUNTER":
                # Headhunter dorks for executive prospects
                base_queries = [
                    f'site:linkedin.com/in "promoted to manager" OR "new role" {area}',
                    f'site:linkedin.com/in "career advancement" {area} -job -hiring',
                    f'site:linkedin.com/in "executive position" {area} -recruiter',
                    f'site:linkedin.com/in "senior manager" {area} -entry -junior',
                    f'site:linkedin.com/in "director level" {area} -intern -trainee',
                    f'site:linkedin.com/in "C-level" OR "CXO" {area} -startup',
                    f'site:linkedin.com/in "new appointment" {area} -contract -freelance',
                    f'site:linkedin.com/in "leadership role" {area} -student -graduate',
                    f'site:linkedin.com/in "board member" {area} -volunteer',
                    f'site:linkedin.com/in "business owner" {area} -small -micro',
                ]
                
            elif campaign_mode == "COMPETITOR_INTERCEPT":
                # Competitor intelligence dorks
                if not competitors:
                    competitors = ["perumahan a", "cluster b", "griya c", "residence d", "housing e"]
                
                for competitor in competitors:
                    competitor_dorks = [
                        f'"kecewa" OR "bermasalah" "perumahan {competitor}"',
                        f'"komplain" OR "keluhan" "{competitor}" developer',
                        f'"penipuan" OR "scam" "{competitor}" properti',
                        f'"buruk" OR "jelek" kualitas "{competitor}"',
                        f'"terlambat" OR "deadline" "{competitor}" serah',
                        f'"batal" OR "gagal" "{competitor}" project',
                        f'"mahal" OR "overpriced" "{competitor}" harga',
                        f'"tipu" OR "hoax" "{competitor}" investasi',
                        f'"sengketa" OR "konflik" "{competitor}" lahan',
                        f'"proses" OR "biaya" "{competitor}" KPR',
                    ]
                    base_queries.extend(competitor_dorks)
                    
            elif campaign_mode == "UPGRADER_INTERCEPT":
                # Upgrade intercept dorks for small house owners
                base_queries = [
                    f'site:olx.co.id OR site:facebook.com "dijual rumah tipe 36" OR "overkredit rumah" {area}',
                    f'site:olx.co.id OR site:facebook.com "jual rumah murah" OR "rumah kecil" {area}',
                    f'site:olx.co.id OR site:facebook.com "cicilan rumah" OR "KPR rumah" {area}',
                    f'site:olx.co.id OR site:facebook.com "rumah subsidi" OR "rumah murah" {area}',
                    f'site:olx.co.id OR site:facebook.com "tipe 21" OR "tipe 22" "dijual" {area}',
                    f'site:olx.co.id OR site:facebook.com "rumah minimalis" OR "rumah sederhana" {area}',
                    f'site:olx.co.id OR site:facebook.com "upgrade rumah" OR "pindah rumah" {area}',
                    f'site:olx.co.id OR site:facebook.com "butuh rumah lebih besar" {area}',
                    f'site:olx.co.id OR site:facebook.com "keluarga bertambah" "cari rumah" {area}',
                    f'site:olx.co.id OR site:facebook.com "anak mulai sekolah" "rumah" {area}',
                ]
                
            elif campaign_mode == "NESTING_INSTINCT":
                # Nesting instinct dorks for young couples
                base_queries = [
                    f'"rekomendasi dokter kandungan" {area} OR "rekomendasi vendor WO" {area}',
                    f'"rekomendasi gedung pernikahan" {area} OR "gedung pernikahan" {area}',
                    f'"rekomendasi vendor pernikahan" {area} OR "dokter kandungan" {area}',
                    f'"rekomendasi wedding organizer" {area} OR "WO vendor" {area}',
                    f'"rekomendasi dekor pernikahan" {area} OR "dekorasi pernikahan" {area}',
                    f'"rekomendasi catering pernikahan" {area} OR "catering pernikahan" {area}',
                    f'"rekomendasi souvenir pernikahan" {area} OR "souvenir pernikahan" {area}',
                    f'"rekomendasi MC pernikahan" {area} OR "MC pernikahan" {area}',
                    f'"rekomendasi fotografer pernikahan" {area} OR "fotografer pernikahan" {area}',
                    f'"rekomendasi wedding venue" {area} OR "gedung pernikahan" {area}',
                ]
                
            elif campaign_mode == "MIGRATION_RADAR":
                # Migration radar dorks for professionals/expatriates
                base_queries = [
                    f'site:quora.com OR site:reddit.com "tanya biaya hidup di {area}" OR "moving to {area}"',
                    f'site:quora.com OR site:reddit.com "rekomendasi pindah ke {area}" OR "cost of living {area}"',
                    f'site:quora.com OR site:reddit.com "expat life in {area}" OR "living in {area}"',
                    f'site:quora.com OR site:reddit.com "job opportunities in {area}" OR "working in {area}"',
                    f'site:quora.com OR site:reddit.com "salary in {area}" OR "income in {area}"',
                    f'site:quora.com OR site:reddit.com "housing in {area}" OR "accommodation in {area}"',
                    f'site:quora.com OR site:reddit.com "schools in {area}" OR "education in {area}"',
                    f'site:quora.com OR site:reddit.com "healthcare in {area}" OR "medical in {area}"',
                    f'site:quora.com OR site:reddit.com "transportation in {area}" OR "commute in {area}"',
                ]
                
            elif campaign_mode == "WINDFALL_ANOMALY":
                # Windfall anomaly dorks for cash holders
                base_queries = [
                    f'"alhamdulillah cair JHT" OR "bingung uang pesangon" OR "investasi dana nganggur"',
                    f'"cair JHT" OR "uang JHT" OR "dana pensiun" "investasi properti"',
                    f'"uang cash" OR "uang tunai" "investasi properti" OR "beli properti cash"',
                    f'"uang kontan" OR "uang fisik" "beli rumah" OR "properti cash"',
                    f'"dana pensiun" OR "dana pensiunan" "investasi aman" OR "properti"',
                    f'"uang tabungan" OR "deposito besar" "investasi properti" OR "beli rumah"',
                    f'"uang receh" OR "uang tunai besar" "beli properti" OR "investasi"',
                    f'"uang simpanan" OR "tabungan" "investasi properti" OR "beli rumah"',
                    f'"uang muka" OR "DP cash" OR "uang tunai" "beli rumah" OR "DP"',
                    f'"uang ghoib" OR "uang haram" "investasi" OR "bersihkan uang"',
                ]
                
            elif campaign_mode == "PANOPTICON":
                # Geospatial & Review Sniffing dorks
                base_queries = [
                    f'site:google.com/maps/contrib/ "review" {area} OR site:tripadvisor.com "kecewa" {area}',
                    f'site:google.com/maps/contrib/ "review" "hotel" {area} OR site:tripadvisor.com "buruk" {area}',
                    f'site:google.com/maps/contrib/ "review" "apartment" {area} OR site:tripadvisor.com "jelek" {area}',
                    f'site:google.com/maps/contrib/ "review" "mall" {area} OR site:tripadvisor.com "tidak" {area}',
                    f'site:google.com/maps/contrib/ "review" "restoran" {area} OR site:tripadvisor.com "masalah" {area}',
                    f'site:google.com/maps/contrib/ "review" "rumah sakit" {area} OR site:tripadvisor.com "keluhan" {area}',
                    f'site:google.com/maps/contrib/ "review" "sekolah" {area} OR site:tripadvisor.com "saran" {area}',
                    f'site:google.com/maps/contrib/ "review" "universitas" {area} OR site:tripadvisor.com "pengalaman" {area}',
                    f'site:google.com/maps/contrib/ "review" "kantor" {area} OR site:tripadvisor.com "kerja" {area}',
                    f'site:google.com/maps/contrib/ "review" "properti" {area} OR site:tripadvisor.com "investasi" {area}',
                ]
                
            elif campaign_mode == "LEVIATHAN":
                # B2B Tender Winners dorks
                base_queries = [
                    f'site:lpse.*.go.id "pemenang tender" {area} OR site:techinasia.com/id "mendapatkan pendanaan"',
                    f'site:lpse.*.go.id "pemenang tender" {area} OR site:dailysocial.id "meraih pendanaan"',
                    f'site:lpse.*.go.id "pemenang tender" "konstruksi" {area} OR site:techinasia.com/id "funding"',
                    f'site:lpse.*.go.id "pemenang tender" "teknologi" {area} OR site:dailysocial.id "investasi"',
                    f'site:lpse.*.go.id "pemenang tender" "furniture" {area} OR site:techinasia.com/id "startup"',
                    f'site:lpse.*.go.id "pemenang tender" "kantor" {area} OR site:dailysocial.id "bisnis"',
                    f'site:lpse.*.go.id "pemenang tender" "peralatan" {area} OR site:techinasia.com/id "venture"',
                    f'site:lpse.*.go.id "pemenang tender" "jasa" {area} OR site:dailysocial.id "modal"',
                    f'site:lpse.*.go.id "pemenang tender" "logistik" {area} OR site:techinasia.com/id "series"',
                    f'site:lpse.*.go.id "pemenang tender" "konsultasi" {area} OR site:dailysocial.id "seed"',
                ]
                
            elif campaign_mode == "PROXY_WEALTH":
                # Luxury Correlation dorks
                base_queries = [
                    f'site:olx.co.id OR site:modifikasi.com "wts rolex" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual rubicon" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "stik golf titleist" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual patek philippe" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual omega speedmaster" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual audemars piguet" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual breitling" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual tag heuer" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual cartier" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual jam mewah" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual tas branded" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual sepatu branded" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual mobil mewah" {area}',
                    f'site:olx.co.id OR site:modifikasi.com "jual perhiasan emas" {area}',
                ]
                
            elif campaign_mode == "TRANSITION":
                # Life-Transition Exploitation dorks
                base_queries = [
                    f'"rekomendasi pengacara keluarga" {area} OR "jual rumah gono gini" {area}',
                    f'"jual cepat rumah warisan" {area} OR "jual rumah hibah" {area}',
                    f'"rekomendasi notaris warisan" {area} OR "jual rumah pensiunan" {area}',
                    f'"rekomendasi pengacara perceraian" {area} OR "jual rumah cerai" {area}',
                    f'"rekomendasi konsultan hibah" {area} OR "jual asset warisan" {area}',
                    f'"rekomendasi ahli waris" {area} OR "jual properti warisan" {area}',
                    f'"rekomendasi notaris perceraian" {area} OR "jual rumah pisah" {area}',
                    f'"rekomendasi mediator keluarga" {area} OR "jual rumah konflik" {area}',
                    f'"rekomendasi pengacara bisnis keluarga" {area} OR "jual usaha keluarga" {area}',
                    f'"rekomendasi konsultan keuangan keluarga" {area} OR "jual properti keluarga" {area}',
                ]
                
            elif campaign_mode == "CHOKEPOINT":
                # Commuter Distress dorks
                base_queries = [
                    f'site:twitter.com "tua di jalan" OR "capek KRL" OR "pengen ngekos aja" {area}',
                    f'site:twitter.com "macet parah" OR "jalan kantor" OR "stres perjalanan" {area}',
                    f'site:twitter.com "capek commuter" OR "naik kendaraan umum" OR "jauh dari kantor" {area}',
                    f'site:twitter.com "waktu tempuh" OR "lama di jalan" OR "macet pagi" {area}',
                    f'site:twitter.com "macet sore" OR "pulang kerja" OR "transportasi umum" {area}',
                    f'site:twitter.com "stres kerja" OR "lelah commuting" OR "jalan kantor" {area}',
                    f'site:twitter.com "transit" OR " commuter" OR "public transport" {area}',
                    f'site:twitter.com "krl" OR "mrt" OR "busway" {area}',
                    f'site:twitter.com "ojek online" OR "gojek" OR "grab" {area}',
                    f'site:twitter.com "dekat kantor" OR "kos dekat kantor" OR "tempat tinggal" {area}',
                ]
                
            elif campaign_mode == "VULTURE":
                # Cash-Rich Auction Investors dorks
                base_queries = [
                    f'"prosedur lelang bank" OR "cari properti BU" OR "menang lelang KPKNL" {area}',
                    f'"lelang bank bca" OR "lelang bank mandiri" OR "lelang bank bri" {area}',
                    f'"lelang properti" OR "asset lelang" OR "bank auction" {area}',
                    f'"properti sitaan" OR "rumah sitaan" OR "lelang kpknl" {area}',
                    f'"cari rumah murah" OR "properti murah" OR "rumah lelang" {area}',
                    f'"investasi lelang" OR "beli properti lelang" OR "uang tunai" {area}',
                    f'"cash buyer" OR "pembeli tunai" OR "tanpa kpr" {area}',
                    f'"properti undervalued" OR "harga murah" OR "diskon besar" {area}',
                    f'"quick sale" OR "jual cepat" OR "butuh uang cepat" {area}',
                    f'"bank foreclosure" OR "sitasi" OR "asset recovery" {area}',
                ]
                
            elif campaign_mode == "NEUROMANCER":
                # New Money / Crypto Whales dorks
                base_queries = [
                    f'site:twitter.com "cuan kripto" OR "take profit saham" OR "porto hijau" OR "baru IPO"',
                    f'site:twitter.com "profit crypto" OR "saham untung" OR "green portfolio" OR "new IPO"',
                    f'site:twitter.com "bitcoin profit" OR "ethereum gain" OR "crypto trading" OR "stock profit"',
                    f'site:twitter.com "crypto millionaire" OR "saham untung besar" OR "trading profit" OR "investasi digital"',
                    f'site:twitter.com "exit crypto" OR "real estate investing" OR "tangible asset" OR "property investment"',
                    f'site:twitter.com "hedging" OR "asset protection" OR "diversification" OR "real asset"',
                    f'site:twitter.com "IPO profit" OR "startup exit" OR "venture capital" OR "angel investor"',
                    f'site:twitter.com "tech money" OR "digital wealth" OR "crypto wealth" OR "new money"',
                    f'site:twitter.com "ROI" OR "return on investment" OR "capital gain" OR "investment return"',
                    f'site:twitter.com "portfolio rebalancing" OR "asset allocation" OR "wealth management" OR "financial planning"',
                ]
                
            elif campaign_mode == "BLOODLINE":
                # Generational Wealth dorks
                base_queries = [
                    f'site:linkedin.com "proud parent" OR "wisuda putri" OR "lulus dari" {area}',
                    f'site:linkedin.com "graduation gift" OR "anak lulus" OR "proud father" OR "proud mother"',
                    f'site:linkedin.com "university graduation" OR "college graduation" OR "graduation ceremony"',
                    f'site:linkedin.com "gift for child" OR "property for child" OR "investment for child"',
                    f'site:linkedin.com "parent investment" OR "family wealth" OR "generational wealth transfer"',
                    f'site:linkedin.com "successful parent" OR "wealthy parent" OR "family planning"',
                    f'site:linkedin.com "first home" OR "starter home" OR "property gift" OR "real estate investment"',
                    f'site:linkedin.com "child education" OR "school investment" OR "future planning" OR "family legacy"',
                    f'site:linkedin.com "wealth management" OR "family office" OR "private banking" OR "estate planning"',
                    f'site:linkedin.com "luxury property" OR "premium property" OR "exclusive property" OR "high-end real estate"',
                ]
                
            elif campaign_mode == "PROPHET":
                # Miliarder Ganti Untung dorks
                base_queries = [
                    f'"pembayaran uang ganti rugi tol" OR "warga desa terima miliaran" OR "cair ganti rugi lahan" {area}',
                    f'"uang kompensasi jalan tol" OR "ganti rugi lahan warga" OR "pembayaran kompensasi pembebasan lahan" {area}',
                    f'"cair uang kompensasi" OR "penerima uang kompensasi" OR "warga dapat miliaran" {area}',
                    f'"pembebasan lahan" OR "kompensasi tanah" OR "uang ganti rugi" {area}',
                    f'"warga terima uang" OR "kompensasi tanah" OR "pembayaran kompensasi" {area}',
                    f'"proyek pemerintah" OR "pembayaran kompensasi" OR "uang kompensasi" {area}',
                    f'"pembayaran uang" OR "ganti rugi" OR "kompensasi" {area}',
                    f'"warga lokal" OR "penerima kompensasi" OR "uang kompensasi" {area}',
                    f'"pembayaran kompensasi" OR "cair uang" OR "penerima uang" {area}',
                    f'"kompensasi jalan" OR "pembayaran kompensasi" OR "uang kompensasi" {area}',
                ]
                
            elif campaign_mode == "PARASITE":
                # Dark Social Infiltration dorks
                base_queries = [
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "warga" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "investor" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "properti" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "rumah" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "investasi" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "bisnis" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "developer" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "pengusaha" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "komunitas" {area}',
                    f'site:facebook.com OR site:twitter.com "chat.whatsapp.com" OR "t.me/joinchat" "diskusi" {area}',
                ]
                
            elif campaign_mode == "RENEGADE":
                # Rejected Buyers - InHouse Target dorks
                base_queries = [
                    f'"KPR ditolak bank" OR "gagal BI checking" OR "susah KPR karena freelance" {area}',
                    f'"KPR tidak disetujui" OR "BI checking gagal" OR "freelance tidak dapat KPR" {area}',
                    f'"penolakan KPR" OR "checking gagal" OR "susah approval KPR" {area}',
                    f'"KPR ditolak" OR "BI checking tidak lulus" OR "freelance KPR ditolak" {area}',
                    f'"gagal KPR" OR "checking gagal" OR "penghasilan tidak tetap" {area}',
                    f'"KPR freelance" OR "checking gagal freelance" OR "approval KPR gagal" {area}',
                    f'"BI checking" OR "penolakan bank" OR "KPR tidak disetujui" {area}',
                    f'"susah KPR" OR "gagal checking" OR "freelance tidak dapat KPR" {area}',
                    f'"KPR ditolak bank" OR "checking gagal" OR "penghasilan freelance" {area}',
                ]
                
            elif campaign_mode == "BLACKHOLE":
                # Quora/Forum Honeypotting dorks
                base_queries = [
                    f'site:quora.com "cara beli rumah" OR "tips beli rumah" OR "panduan beli rumah"',
                    f'site:reddit.com "cara beli rumah" OR "tips beli rumah" OR "panduan beli rumah"',
                    f'site:quora.com "how to buy house" OR "house buying guide" OR "home purchase tips"',
                    f'site:reddit.com "how to buy house" OR "house buying guide" OR "home purchase tips"',
                    f'site:quora.com "beli rumah pertama" OR "tips rumah pertama" OR "panduan rumah pertama"',
                    f'site:reddit.com "beli rumah pertama" OR "tips rumah pertama" OR "panduan rumah pertama"',
                    f'site:quora.com "cara KPR rumah" OR "tips KPR rumah" OR "panduan KPR rumah"',
                    f'site:reddit.com "cara KPR rumah" OR "tips KPR rumah" OR "panduan KPR rumah"',
                    f'site:quora.com "investasi properti" OR "tips investasi properti" OR "panduan investasi properti"',
                    f'site:reddit.com "investasi properti" OR "tips investasi properti" OR "panduan investasi properti"',
                ]
                
            elif campaign_mode == "OXYGEN":
                # Health & Environmental Refugees dorks
                base_queries = [
                    f'"anak sering ISPA" OR "udara jakarta memburuk" OR "cari daerah asri" OR "rekomendasi air purifier" {area}',
                    f'"polusi udara" OR "kualitas udara buruk" OR "rumah sehat" OR "lingkungan hijau" {area}',
                    f'"air bersih" OR "filter air" OR "air minum sehat" OR "tanpa polusi" {area}',
                    f'"kesehatan keluarga" OR "lingkungan bersih" OR "rumah sehat" OR "daerah bebas polusi" {area}',
                    f'"rekomendasi area sehat" OR "tempat tinggal sehat" OR "lokasi bersih" {area}',
                    f'"masker udara" OR "air purifier" OR "filter polusi" OR "kualitas udara" {area}',
                    f'"hindari polusi" OR "lokasi asri" OR "lingkungan hijau" OR "rumah di luar kota" {area}',
                    f'"rekomendasi tempat tinggal" OR "area bersih" OR "kualitas hidup" {area}',
                    f'"penyakit pernapasan" OR "asma anak" OR "alergi polusi" OR "udara bersih" {area}',
                ]
                
            elif campaign_mode == "DIASPORA":
                # Cross-Border Wealth dorks
                base_queries = [
                    f'site:facebook.com "pekerja migran" OR "cara KPR dari luar negeri" OR "investasi dari luar negeri" {area}',
                    f'site:facebook.com "TKI" OR "TKW" OR "pekerja indonesia di luar negeri" OR "investasi properti dari luar negeri" {area}',
                    f'site:facebook.com "pekerja migran malaysia" OR "pekerja migran singapura" OR "investasi dari malaysia" {area}',
                    f'site:facebook.com "pekerja migran hongkong" OR "pekerja migran taiwan" OR "investasi dari hongkong" {area}',
                    f'site:facebook.com "TKI di luar negeri" OR "TKW di luar negeri" OR "properti untuk TKI" {area}',
                    f'site:facebook.com "investasi properti" OR "beli properti dari luar negeri" OR "KPR untuk WNI" {area}',
                    f'site:facebook.com "rekomendasi investasi" OR "tips investasi" OR "cara investasi properti" {area}',
                    f'site:facebook.com "pekerja indonesia" OR "pengiriman TKI" OR "remitansi ke indonesia" {area}',
                    f'site:facebook.com "bisnis luar negeri" OR "usaha TKI" OR "peluang bisnis" {area}',
                    f'site:facebook.com "properti untuk TKI" OR "rumah untuk TKI" OR "investasi aman" {area}',
                ]
                
            elif campaign_mode == "HABITAT":
                # Space-Demanding Hobbies dorks
                base_queries = [
                    f'"komunitas anjing besar" OR "butuh garasi luas" OR "bikin taman luas" OR "jual anjing karena pindah" {area}',
                    f'"hobi memelihara hewan" OR "butuh lahan luas" OR "bikin kandang" OR "tempat tinggal untuk hewan peliharaan" {area}',
                    f'"komunitas kucing" OR "butuh rumah untuk kucing" OR "pelihara hewan" OR "pet friendly" {area}',
                    f'"komunitas burung" OR "avicultur" OR "bikin sangkar burung" OR "tempat untuk burung" {area}',
                    f'"komunitas reptil" OR "pelihara reptil" OR "terarium" OR "bikin kandang reptil" {area}',
                    f'"komunitas ikan" OR "aquarium" OR "ikan hias" OR "bikin kolam ikan" {area}',
                    f'"hobi pertanian" OR "berkebun" OR "lahan pertanian" OR "rumah dengan kebun" {area}',
                    f'"komunitas tanaman hias" OR "florist" OR "bikin taman" OR "rumah dengan taman" {area}',
                    f'"komunitas fitness" OR "olahraga" OR "gym di rumah" OR "tempat olahraga" {area}',
                ]
                
            elif campaign_mode == "SYMBIOSIS":
                # Supply Chain Intercept dorks
                base_queries = [
                    f'site:instagram.com OR site:facebook.com "jasa angkut pindahan" {area} OR "jasa interior" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa angkut barang" OR "jasa pindahan" OR "jasa packing" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa desain interior" OR "interior design" OR "dekor rumah" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa renovasi" OR "kontraktor renovasi" OR "tukang bangun" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa angkut mobil" OR "jasa ekspedisi" OR "jasa logistik" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa pembersihan" OR "cleaning service" OR "jasa bersih" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa catering" OR "katering" OR "jasa makanan" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa event organizer" OR "EO" OR "event planner" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa photography" OR "fotografer" OR "dokumentasi" {area}',
                    f'site:instagram.com OR site:facebook.com "jasa pernikahan" OR "wedding organizer" OR "wedding planner" {area}',
                ]
                
            elif campaign_mode == "DISTRESS":
                # Debt-Driven Relocation dorks
                base_queries = [
                    f'"restrukturisasi utang KPR" OR "sita jaminan bank" OR "jual BU bayar utang" {area}',
                    f'"konsolidasi utang" OR "gabung pinjaman" OR "bayar utang dengan jual properti" {area}',
                    f'"jual rumah untuk bayar utang" OR "jual cepat bayar utang" OR "jual aset bayar utang" {area}',
                    f'"kredit macet" OR "refinancing KPR" OR "take over KPR" OR "bantuan bayar utang" {area}',
                    f'"pinjaman lunas" OR "pinjaman tanpa agunan" OR "dana talangan" OR "uang darurat" {area}',
                    f'"bantuan restrukturisasi utang" OR "konsultan utang" OR "penyelesaian masalah utang" {area}',
                    f'"jual aset untuk bayar utang" OR "likuidasi aset" OR "dana tunai cepat" {area}',
                    f'"cara bayar utang" OR "solusi masalah keuangan" OR "keluar dari masalah utang" {area}',
                    f'"bantuan finansial" OR "konsultasi keuangan" OR "restrukturisasi finansial" {area}',
                    f'"uang darurat" OR "dana cepat" OR "pinjaman darurat" OR "butuh uang sekarang" {area}',
                ]
                
            elif campaign_mode == "REBELLION":
                # Angry Renters dorks
                base_queries = [
                    f'"ibu kost galak" OR "capek ngontrak" OR "harga sewa naik" OR "kontrakan bocor" {area}',
                    f'"pemilik kost galak" OR "sakit ngontrak" OR "sewa naik terus" OR "kontrak tidak diperpanjang" {area}',
                    f'"capek bayar sewa" OR "harga sewa tidak wajar" OR "pemilik sewa nakal" OR "kontrak sewa tidak adil" {area}',
                    f'"pindah karena sewa" OR "cari rumah sendiri" OR "berhenti ngontrak" OR "sakit sewa" {area}',
                    f'"uang sewa hangus" OR "cicilan sewa sia-sia" OR "sewa lebih mahal dari KPR" OR "ingin punya rumah" {area}',
                    f'"pemilik sewa tidak bertanggung jawab" OR "kontrak sewa tidak jelas" OR "biaya sewa tidak masuk akal" {area}',
                    f'"capek dari kontrak" OR "ingin keluar dari kos" OR "pindah dari kost" OR "sewa tidak nyaman" {area}',
                    f'"pemilik sewa serakah" OR "sewa tidak sesuai" OR "kontrak sewa bermasalah" OR "uang sewa mubazir" {area}',
                    f'"ingin akuisisi properti" OR "stop sewa beli rumah" OR "dari ngontrak ke KPR" OR "sewa vs cicilan" {area}',
                ]
                
            elif campaign_mode == "SANDWICH":
                # Multi-Generational Housing dorks
                base_queries = [
                    f'"rumah untuk mertua" OR "kamar bawah orang tua sakit" OR "gabung rumah mertua" {area}',
                    f'"rumah 2 lantai untuk keluarga" OR "rumah dengan kamar bawah" OR "rumah untuk orang tua" {area}',
                    f'"tinggal bersama orang tua" OR "rumah keluarga besar" OR "rumah multi generasi" {area}',
                    f'"kamar untuk lansia" OR "rumah dengan fasilitas lansia" OR "rumah untuk orang tua lanjut usia" {area}',
                    f'"rumah dengan kamar terpisah" OR "rumah untuk mertua dan anak" OR "desain rumah keluarga" {area}',
                    f'"rumah untuk orang tua sakit" OR "kamar perawat lansia" OR "rumah dengan akses mudah untuk lansia" {area}',
                    f'"rumah 3 kamar untuk keluarga" OR "rumah dengan kamar tambahan" OR "rumah untuk keluarga besar" {area}',
                    f'"rumah dengan fasilitas lansia" OR "rumah aksesibel untuk lansia" OR "rumah untuk orang tua" {area}',
                    f'"rumah multi generasi" OR "rumah untuk 3 generasi" OR "rumah dengan kamar bawah" {area}',
                ]
                
            elif campaign_mode == "EXODUS":
                # WFH & Digital Nomads dorks
                base_queries = [
                    f'"pindah ke pinggir kota" OR "wfh selamanya" OR "bikin studio kedap suara" OR "biznet masuk daerah" {area}',
                    f'"kerja remote dari pinggir kota" OR "rumah WFH" OR "studio untuk WFH" OR "internet cepat pinggir kota" {area}',
                    f'"digital nomad" OR "kerja dari mana saja" OR "rumah dengan internet cepat" OR "tempat tinggal remote" {area}',
                    f'"bikin studio di rumah" OR "ruang kerja di rumah" OR "home office" OR "WFH permanent" {area}',
                    f'"pindah ke luar kota" OR "rumah pinggir kota" OR "lokasi WFH" OR "internet stabil" {area}',
                    f'"bikin studio kedap suara" OR "ruang studio kedap" OR "home studio" OR "musik studio" {area}',
                    f'"biznet masuk daerah" OR "internet fiber" OR "koneksi internet cepat" OR "lokasi remote work" {area}',
                    f'"pindah karena WFH" OR "kerja dari rumah permanen" OR "rumah dengan fasilitas WFH" OR "tempat kerja remote" {area}',
                    f'"digital lifestyle" OR "remote work lifestyle" OR "work from anywhere" OR "nomad life" {area}',
                    f'"rumah dengan koneksi baik" OR "internet stabil untuk WFH" OR "lokasi remote work friendly" {area}',
                ]
                
            elif campaign_mode == "GENTRIFICATION":
                # Infrastructure Speculators dorks
                base_queries = [
                    f'"pembangunan kampus baru" OR "cari tanah dekat kampus" OR "bikin kost kostan di" {area}',
                    f'"pembangunan rumah sakit" OR "tanah dekat fasilitas umum" OR "investasi infrastruktur" {area}',
                    f'"pembangunan tol" OR "tanah dekat jalan tol" OR "lokasi strategis infrastruktur" {area}',
                    f'"pembangunan mall" OR "tanah dekat pusat perbelanjaan" OR "investasi komersial" {area}',
                    f'"pembangunan stasiun" OR "tanah dekat transportasi umum" OR "lokasi dekat MRT" {area}',
                    f'"pembangunan sekolah" OR "tanah dekat sekolah" OR "investasi pendidikan" {area}',
                    f'"pembangunan kawasan industri" OR "tanah dekat pabrik" OR "investasi industri" {area}',
                    f'"pembangunan bandara" OR "tanah dekat bandara" OR "lokasi strategis transportasi udara" {area}',
                    f'"pembangunan pelabuhan" OR "tanah dekat pelabuhan" OR "investasi logistik" {area}',
                    f'"pembangunan fasilitas" OR "tanah dekat fasilitas publik" OR "lokasi dekat infrastruktur" {area}',
                ]
                
            elif campaign_mode == "LOTTERY":
                # Policy & Subsidy Hunters dorks
                base_queries = [
                    f'"kapan bebas PPN" OR "rumah DP 0 rupiah" OR "kuota FLPP" OR "subsidi KPR" {area}',
                    f'"PPN ditanggung" OR "rumah tanpa DP" OR "subsidi rumah" OR "bantuan KPR" {area}',
                    f'"FLPP 2024" OR "kuota FLPP" OR "subsidi perumahan" OR "rumah murah" {area}',
                    f'"KPR subsidi" OR "bunga KPR" OR "KPR rendah" OR "rumah subsidi" {area}',
                    f'"rumah DP 0" OR "tanpa DP" OR "cicilan ringan" OR "rumah murah" {area}',
                    f'"program rumah murah" OR "bantuan perumahan" OR "kuota rumah murah" OR "subsidi Pemerintah" {area}',
                    f'"PPN 0%" OR "bebas PPN" OR "diskon PPN" OR "rumah tanpa PPN" {area}',
                    f'"bantuan DP" OR "subsidi DP" OR "bantuan uang muka" OR "cicilan dibantu" {area}',
                    f'"promo KPR" OR "diskon KPR" OR "bunga KPR" OR "KPR murah" OR "KPR ringan" {area}',
                    f'"program perumahan" OR "kuota perumahan" OR "rumah bersubsidi" OR "bantuan perumahan" {area}',
                ]
                
            elif campaign_mode == "LOGISTICS":
                # E-commerce Boom dorks
                base_queries = [
                    f'"ruang tamu penuh paket" OR "butuh ruko untuk shopee" OR "ditegur RT karena kurir" OR "admin packing rumah" {area}',
                    f'"gudang untuk online shop" OR "butuh tempat packing" OR "sewa gudang kecil" OR "usaha dari rumah" {area}',
                    f'"dropship dari rumah" OR "stok barang di rumah" OR "bikin toko online" OR "jualan online dari rumah" {area}',
                    f'"butuh ruang usaha" OR "cari ruko murah" OR "sewa ruko bulanan" OR "tempat usaha kecil" {area}',
                    f'"online shop butuh gudang" OR "packing dan pengiriman" OR "kurir sering lewat" OR "tetangga komplain pengiriman" {area}',
                    f'"bisnis dari rumah" OR "usaha e-commerce" OR "butuh tempat usaha" OR "ruang kerja di rumah" {area}',
                    f'"stock barang di rumah" OR "butuh gudang kecil" OR "sewa tempat usaha" OR "cari ruko untuk bisnis" {area}',
                    f'"admin packing di rumah" OR "butuh ruang gudang" OR "usaha online shop" OR "tempat untuk bisnis online" {area}',
                    f'"kurir sering lewat rumah" OR "tetangga komplain bisnis" OR "butuh tempat usaha terpisah" OR "cari ruko untuk toko online" {area}',
                ]
                
            elif campaign_mode == "EV_TRAP":
                # Electric Vehicle Charging Crisis dorks
                base_queries = [
                    f'"tambah daya PLN ngecas mobil" OR "gak ada garasi" OR "sewa garasi bulanan" OR "pasang wallbox wuling" {area}',
                    f'"butuh garasi untuk mobil listrik" OR "pasang charger mobil listrik" OR "daya listrik tidak cukup" OR "ngecas mobil di rumah" {area}',
                    f'"sewa garasi untuk mobil listrik" OR "cari rumah dengan garasi luas" OR "butuh daya besar untuk EV" OR "charging station di rumah" {area}',
                    f'"pasang wallbox di rumah" OR "tambah daya listrik untuk mobil listrik" OR "butuh garasi untuk mobil" OR "daya listrik tidak kuat" {area}',
                    f'"ngecas mobil listrik di rumah" OR "butuh tempat charging mobil" OR "daya listrik untuk EV" OR "garasi untuk mobil listrik" {area}',
                    f'"sewa tempat untuk mobil listrik" OR "cari rumah dengan listrik besar" OR "butuh charging station" OR "daya listrik untuk charging" {area}',
                    f'"butuh garasi bulanan" OR "cari rumah dengan garasi" OR "pasang charger mobil" OR "listrik tidak cukup untuk EV" {area}',
                    f'"wallbox untuk mobil listrik" OR "daya listrik untuk wallbox" OR "butuh tempat charging" OR "garasi untuk mobil elektrik" {area}',
                    f'"charging mobil listrik" OR "butuh daya listrik besar" OR "cari rumah dengan garasi luas" OR "sewa tempat charging" {area}',
                ]
                
            elif campaign_mode == "TABULA_RASA":
                # Life Escape/Healing dorks
                base_queries = [
                    f'"over dp gedung pernikahan" OR "batal nikah jual cincin" OR "butuh tempat baru healing" {area}',
                    f'"butuh tempat tinggal baru" OR "mulai hidup baru" OR "cari ketenangan" OR "butuh privasi" {area}',
                    f'"butuh tempat healing" OR "cari lingkungan tenang" OR "butuh kedamaian" OR "pindah untuk ketenangan" {area}',
                    f'"jual cincin pernikahan" OR "batal pernikahan" OR "butuh tempat baru" OR "mulai hidup sendiri" {area}',
                    f'"butuh rumah untuk healing" OR "cari lingkungan yang tenang" OR "butuh privasi" OR "pindah dari kota" {area}',
                    f'"butuh kedamaian" OR "cari ketenangan" OR "butuh lingkungan yang tenang" OR "butuh tempat untuk healing" {area}',
                    f'"butuh rumah sendiri" OR "cari ketenangan" OR "butuh privasi" OR "mulai hidup baru" {area}',
                    f'"butuh tempat tinggal yang tenang" OR "cari lingkungan yang damai" OR "butuh kedamaian" OR "butuh rumah untuk healing" {area}',
                    f'"butuh rumah sendiri" OR "cari rumah untuk healing" OR "butuh privasi" OR "butuh ketenangan" {area}',
                ]
                
            elif campaign_mode == "HEIRLOOM":
                # Inheritance & Insurance Liquidators dorks
                base_queries = [
                    f'"cara urus turun waris" OR "asuransi jiwa cair" OR "jual tanah warisan" {area}',
                    f'"dapat warisan dari orang tua" OR "asuransi cair" OR "jual tanah warisan" OR "investasi warisan" {area}',
                    f'"cara mengurus warisan" OR "asuransi jiwa cair" OR "jual properti warisan" OR "investasi dari warisan" {area}',
                    f'"dapat uang dari asuransi" OR "jual tanah warisan" OR "investasi warisan" OR "cara mengurus warisan" {area}',
                    f'"warisan dari orang tua" OR "asuransi jiwa cair" OR "jual properti warisan" OR "investasi dari warisan" {area}',
                    f'"dapat uang warisan" OR "jual tanah warisan" OR "investasi warisan" OR "cara mengurus warisan" {area}',
                    f'"asuransi cair" OR "jual tanah warisan" OR "investasi warisan" OR "cara mengurus warisan" {area}',
                    f'"warisan keluarga" OR "asuransi jiwa cair" OR "jual properti warisan" OR "investasi dari warisan" {area}',
                    f'"dapat uang asuransi" OR "jual tanah warisan" OR "investasi warisan" OR "cara mengurus warisan" {area}',
                ]
                
            elif campaign_mode == "ZOOKEEPER":
                # Extreme Pet Owners dorks
                base_queries = [
                    f'"ditegur RT karena pelihara" OR "bikin kandang aviary" OR "peredam suara burung" {area}',
                    f'"butuh rumah untuk pelihara hewan" OR "bikin kandang burung" OR "peredam suara untuk hewan" OR "pelihara hewan di rumah" {area}',
                    f'"komplain RT karena pelihara" OR "butuh kandang untuk burung" OR "peredam suara untuk peliharaan" OR "hewan peliharaan" {area}',
                    f'"butuh rumah dengan halaman" OR "bikin kandang untuk hewan" OR "peredam suara untuk burung" OR "pelihara hewan besar" {area}',
                    f'"butuh ruang untuk hewan" OR "bikin kandang aviary" OR "peredam suara untuk peliharaan" OR "hewan peliharaan" {area}',
                    f'"butuh rumah dengan taman" OR "bikin kandang untuk burung" OR "peredam suara untuk hewan" OR "pelihara hewan di rumah" {area}',
                    f'"butuh halaman untuk hewan" OR "bikin kandang untuk peliharaan" OR "peredam suara untuk burung" OR "hewan peliharaan" {area}',
                    f'"butuh rumah untuk hewan" OR "bikin kandang untuk burung" OR "peredam suara untuk peliharaan" OR "pelihara hewan" {area}',
                    f'"butuh ruang untuk peliharaan" OR "bikin kandang untuk hewan" OR "peredam suara untuk burung" OR "hewan peliharaan" {area}',
                ]
                
            elif campaign_mode == "HLR_SNIPER":
                # Regional Prefix Targeting dorks with HLR database integration
                base_queries = []
                
                # Check if area is a region name or specific prefix
                if area and area.upper() in INDONESIA_HLR_MAPPING:
                    # Area is a region name, get all prefixes for that region
                    target_region = area.upper()
                    region_prefixes = get_region_prefixes(target_region)
                    
                    # Generate dorks for each prefix in the region
                    for prefix in region_prefixes:
                        base_queries.extend([
                            f'"{prefix}*" "jual cepat" OR "dijual rugi" OR "jual BU" OR "overkredit"',
                            f'"{prefix}*" "butuh uang cepat" OR "jual murah" OR "take over" OR "nego"',
                            f'"{prefix}*" "dijual cepat" OR "over kredit" OR "cicilan ringan" OR "bisa nego"',
                            f'"{prefix}*" "jual asset" OR "butuh dana" OR "jual properti" OR "take over KPR"',
                        ])
                    
                    # Add region-specific queries
                    base_queries.extend([
                        f'region "{target_region}" "jual cepat" OR "dijual rugi" OR "jual BU"',
                        f'region "{target_region}" "over kredit" OR "take over" OR "nego"',
                        f'"{target_region}" "jual properti" OR "butuh dana" OR "take over KPR"',
                    ])
                    
                elif area and area.startswith('08'):
                    # Area is a specific prefix, use it directly
                    hlr_prefix = area.strip()
                    base_queries = [
                        f'"{hlr_prefix}*" "jual cepat" OR "dijual rugi" OR "jual BU" OR "overkredit"',
                        f'"{hlr_prefix}*" "butuh uang cepat" OR "jual murah" OR "take over" OR "nego"',
                        f'"{hlr_prefix}*" "dijual cepat" OR "over kredit" OR "cicilan ringan" OR "bisa nego"',
                        f'"{hlr_prefix}*" "jual asset" OR "butuh dana" OR "jual properti" OR "take over KPR"',
                        f'"{hlr_prefix}*" "dijual rugi" OR "over kredit" OR "cicilan bisa nego" OR "butuh dana"',
                        f'"{hlr_prefix}*" "jual cepat rumah" OR "over kredit" OR "take over" OR "nego keras"',
                        f'"{hlr_prefix}*" "dijual BU" OR "over kredit" OR "cicilan ringan" OR "bisa nego"',
                        f'"{hlr_prefix}*" "jual properti" OR "butuh dana" OR "over kredit" OR "nego"',
                        f'"{hlr_prefix}*" "jual cepat" OR "over kredit" OR "take over" OR "cicilan ringan"',
                    ]
                else:
                    # Default to common prefixes if no specific prefix/region provided
                    default_prefixes = ['0812', '0813', '0852', '0856', '0878', '0895']  # Mix of providers
                    
                    for prefix in default_prefixes:
                        base_queries.extend([
                            f'"{prefix}*" "jual cepat" OR "dijual rugi" OR "jual BU" OR "overkredit"',
                            f'"{prefix}*" "butuh uang cepat" OR "jual murah" OR "take over" OR "nego"',
                        ])
                
                # Limit queries to prevent too many results
                if len(base_queries) > 50:
                    base_queries = base_queries[:50]
                
            elif campaign_mode == "WA_ME_INTERCEPT":
                # Direct WA Link Harvesting dorks
                base_queries = [
                    f'"wa.me/62" OR "api.whatsapp.com/send" "cari rumah" OR "tanya KPR" OR "butuh kontrakan" {area}',
                    f'"wa.me/62" OR "628" "jual rumah" OR "cari rumah" OR "butuh properti" {area}',
                    f'"wa.me/62" OR "08" "tanya KPR" OR "butuh KPR" OR "cicilan" {area}',
                    f'"api.whatsapp.com/send" OR "wa.me/62" "jual cepat" OR "dijual" OR "nego" {area}',
                    f'"wa.me/62" OR "628" "butuh kontrakan" OR "cari kontrakan" OR "sewa rumah" {area}',
                    f'"wa.me/62" OR "08" "cari rumah murah" OR "rumah murah" OR "properti murah" {area}',
                    f'"api.whatsapp.com/send" OR "wa.me/62" "tanya harga" OR "berapa harga" OR "info" {area}',
                    f'"wa.me/62" OR "628" "survey" OR "cek lokasi" OR "lihat rumah" {area}',
                    f'"wa.me/62" OR "08" "butuh info" OR "tanya" OR "detail properti" {area}',
                ]
                
            elif campaign_mode == "ISP_GEO":
                # Localized WiFi Complaints dorks
                base_queries = [
                    f'"biznet gangguan" OR "indihome los merah" OR "pasang wifi murah" {area}',
                    f'"wifi tidak stabil" OR "internet lemot" OR "koneksi internet jelek" {area}',
                    f'"pasang wifi baru" OR "butuh internet cepat" OR "provider internet" {area}',
                    f'"wifi murah" OR "internet rumah" OR "pasang indihome" OR "biznet" {area}',
                    f'"gangguan internet" OR "wifi putus" OR "koneksi tidak stabil" {area}',
                    f'"indihome gangguan" OR "biznet tidak stabil" OR "wifi lemot" {area}',
                    f'"butuh provider wifi" OR "internet untuk rumah" OR "pasang internet" {area}',
                    f'"wifi untuk WFH" OR "internet kerja dari rumah" OR "koneksi stabil" {area}',
                    f'"keluhan wifi" OR "komplain internet" OR "provider tidak bagus" {area}',
                ]
                
            elif campaign_mode == "COMMUTE_NODE":
                # Micro-Transit Tracing dorks
                base_queries = [
                    f'"angkot rute" OR "titik jemput stasiun" OR "ojek pangkalan" {area}',
                    f'"halte bus" OR "stasiun terdekat" OR "rute angkot" OR "ojek online" {area}',
                    f'"transportasi umum" OR "akses stasiun" OR "titik jemput" OR "pangkalan ojek" {area}',
                    f'"rute transportasi" OR "halte terdekat" OR "stasiun commuter" OR "ojek pangkalan" {area}',
                    f'"akses commuter" OR "halte bus" OR "rute angkot" OR "ojek online" {area}',
                    f'"transportasi ke stasiun" OR "halte commuter" OR "rute angkot" OR "pangkalan" {area}',
                    f'"akses commuter line" OR "halte bus" OR "stasiun terdekat" OR "ojek pangkalan" {area}',
                    f'"rute angkot ke stasiun" OR "titik jemput commuter" OR "ojek pangkalan" {area}',
                    f'"halte commuter" OR "stasiun commuter" OR "rute angkot" OR "ojek online" {area}',
                ]
                
            elif campaign_mode == "GAVEL":
                # Court/SIPP Public Records dorks
                base_queries = [
                    f'site:sipp.pn-*.go.id "harta gono gini" {area} OR site:hukumonline.com/klinik "pembagian rumah cerai" {area}',
                    f'site:sipp.pn-*.go.id "putusan cerai" OR "pembagian harta" {area}',
                    f'site:hukumonline.com/klinik "gugatan cerai" OR "harta bersama" {area}',
                    f'site:sipp.pn-*.go.id "eksekusi putusan" OR "eksekusi harta" {area}',
                    f'site:hukumonline.com/klinik "mediasi perceraian" OR "damai" {area}',
                    f'site:sipp.pn-*.go.id "proses cerai" OR "harta gono gini" {area}',
                    f'site:hukumonline.com/klinik "hak asuh anak" OR "nafkah" {area}',
                    f'site:sipp.pn-*.go.id "pembagian harta" OR "harta bersama" {area}',
                    f'site:hukumonline.com/klinik "perceraian cepat" OR "biaya cerai" {area}',
                    f'site:sipp.pn-*.go.id "putusan hak milik" OR "sengketa harta" {area}',
                ]
                
            elif campaign_mode == "PROGRESSIVE":
                # Vehicle Tax/Space Exhaustion dorks
                base_queries = [
                    f'"pajak progresif mobil ke 3" OR "bikin garasi di luar" OR "ditegur RT parkir mobil" {area}',
                    f'"pajak mobil naik" OR "butuh garasi tambahan" OR "parkir mobil di luar" {area}',
                    f'"pajak kendaraan" OR "garasi penuh" OR "parkir mobil di depan rumah" {area}',
                    f'"pajak progresif" OR "butuh tempat parkir" OR "garasi tidak cukup" {area}',
                    f'"pajak mobil ke 2" OR "bikin garasi sampingan" OR "parkir di halaman" {area}',
                    f'"pajak kendaraan tinggi" OR "butuh lahan parkir" OR "garasi ekstensi" {area}',
                    f'"pajak progresif naik" OR "garasi tidak muat" OR "parkir di trotoar" {area}',
                    f'"pajak mobil mahal" OR "butuh tempat parkir mobil" OR "garasi modular" {area}',
                    f'"pajak kendaraan" OR "bikin carport" OR "parkir mobil di bawah" {area}',
                    f'"pajak progresif kendaraan" OR "butuh solusi parkir" OR "garasi tambahan" {area}',
                ]
                
            elif campaign_mode == "PINTEREST":
                # Future Blueprinting dorks
                base_queries = [
                    f'site:pinterest.com "rumah impian" OR "inspirasi dapur" {area}',
                    f'site:pinterest.com "desain rumah minimalis" OR "interior rumah" {area}',
                    f'site:pinterest.com "taman rumah" OR "dekorasi kamar" {area}',
                    f'site:pinterest.com "rumah modern" OR "dapur minimalis" {area}',
                    f'site:pinterest.com "inspirasi rumah" OR "desain eksterior" {area}',
                    f'site:pinterest.com "renovasi rumah" OR "dekorasi rumah" {area}',
                    f'site:pinterest.com "rumah idaman" OR "dapur impian" {area}',
                    f'site:pinterest.com "desain interior" OR "taman minimalis" {area}',
                    f'site:pinterest.com "rumah kecil" OR "dapur cantik" {area}',
                    f'site:pinterest.com "arsitektur rumah" OR "inspirasi desain" {area}',
                ]
                
            elif campaign_mode == "PLASTIC":
                # High-Tier Credit/Perfect BI Checking dorks
                base_queries = [
                    f'"limit BCA naik" OR "kartu kredit limit ratusan" OR "gesek tunai modal bisnis" {area}',
                    f'"limit kartu kredit tinggi" OR "BI checking sempurna" OR "skor kredit bagus" {area}',
                    f'"limit kartu kredit naik" OR "cicilan KPR mudah" OR "approval instant" {area}',
                    f'"skor kredit 850" OR "BI checking bersih" OR "limit kartu jutaan" {area}',
                    f'"kartu kredit premium" OR "cicilan tanpa riba" OR "KPR langsung cair" {area}',
                    f'"limit BCA ratusan juta" OR "skor kredit excellent" OR "cicilan ringan" {area}',
                    f'"kartu kredit platinum" OR "BI checking perfect" OR "approval KPR cepat" {area}',
                    f'"limit mandiri tinggi" OR "cicilan mudah disetujui" OR "KPR instant approval" {area}',
                    f'"skor kredit 900" OR "limit kartu premium" OR "cicilan tanpa survey" {area}',
                ]
                
            elif campaign_mode == "INCUBATOR":
                # New Business Birth dorks
                base_queries = [
                    f'site:glints.com/id OR site:jobstreet.co.id "penempatan cabang baru" OR "karyawan pertama" {area}',
                    f'site:glints.com/id "lowongan pekerjaan baru" OR "bisnis startup" {area}',
                    f'site:jobstreet.co.id "perusahaan baru" OR "lokasi bisnis" OR "kantor cabang" {area}',
                    f'site:glints.com/id "startup hiring" OR "ekspansi bisnis" OR "buka cabang" {area}',
                    f'site:jobstreet.co.id "lowongan kerja" OR "perusahaan berkembang" OR "rekrutmen massal" {area}',
                    f'site:glints.com/id "perusahaan teknologi" OR "digital startup" OR "bisnis online" {area}',
                    f'site:jobstreet.co.id "perusahaan baru" OR "lokasi usaha" OR "tempat usaha" {area}',
                    f'site:glints.com/id "startup funding" OR "investasi startup" OR "bisnis baru" {area}',
                    f'site:jobstreet.co.id "peluang bisnis" OR "usaha baru" OR "lokasi strategis" {area}',
                    f'site:glints.com/id "ekspansi perusahaan" OR "buka cabang baru" OR "lokasi premium" {area}',
                ]
                
            elif campaign_mode == "ATLANTIS":
                # Climate Refugees dorks
                base_queries = [
                    f'"capek nguras banjir" OR "kena rob" OR "jual rumah daerah banjir" {area}',
                    f'"banjir naik" OR "rumah kebanjiran" OR "pindah dari daerah banjir" {area}',
                    f'"rumah aman dari banjir" OR "lokasi tinggi bebas banjir" {area}',
                    f'"daerah kering" OR "bukit hijau" OR "lokasi strategis banjir" {area}',
                    f'"rumah di atas" OR "lokasi aman banjir" OR "perumahan bebas banjir" {area}',
                    f'"jual cepat karena banjir" OR "rumah terkena dampak" OR "lokasi banjir aman" {area}',
                    f'"pindah hindari banjir" OR "cari rumah tinggi" OR "lokasi strategis" {area}',
                    f'"banjir tahun ini" OR "prediksi banjir" OR "zona merah banjir" {area}',
                    f'"rumah dekat sungai" OR "lokasi aman" OR "infrastructure banjir" {area}',
                ]
                
            elif campaign_mode == "ZONING":
                # School District Hackers dorks
                base_queries = [
                    f'"kalah zonasi sekolah" OR "pindah KK demi PPDB" OR "cari rumah dekat SMA" {area}',
                    f'"zonasi sekolah terbaik" OR "pindah untuk anak" OR "rumah dekat sekolah unggulan" {area}',
                    f'"akses sekolah mudah" OR "lokasi sekolah strategis" OR "rumah di radius sekolah" {area}',
                    f'"pindah demi sekolah" OR "cari rumah dekat SD" OR "lokasi PPDB" {area}',
                    f'"rumah dekat sekolah negeri" OR "zonasi sekolah" OR "akses fasilitas pendidikan" {area}',
                    f'"pindah KK ke sekolah" OR "rumah untuk anak sekolah" OR "lokasi sekolah favorit" {area}',
                    f'"sekolah terdekat" OR "radius sekolah" OR "lokasi pendidikan" {area}',
                    f'"pindah untuk PPDB" OR "rumah dekat sekolah dasar" OR "akses sekolah" {area}',
                    f'"rumah di area sekolah" OR "lokasi strategis sekolah" OR "fasilitas PPDB" {area}',
                    f'"pindah anak sekolah" OR "cari rumah dekat SMP" OR "akses sekolah menengah" {area}',
                ]
                
            elif campaign_mode == "PILGRIM":
                # Spiritual/Community Migration dorks
                base_queries = [
                    f'"cari rumah dekat masjid" OR "perumahan islami" OR "tetangga sefrekuensi" {area}',
                    f'"komunitas muslim" OR "lingkungan islami" OR "perumahan syariah" {area}',
                    f'"masjid terdekat" OR "rumah dekat surau" OR "lokasi ibadah" {area}',
                    f'"tetangga baik" OR "komunitas harmonis" OR "lingkungan islami" {area}',
                    f'"perumahan muslim" OR "rumah dekat masjid agung" OR "lokasi islami" {area}',
                    f'"cari rumah islami" OR "komunitas taqwa" OR "lingkungan religius" {area}',
                    f'"masjid jami" OR "rumah dekat musholla" OR "akses fasilitas ibadah" {area}',
                    f'"tetangga islami" OR "komunitas muslimah" OR "perumahan hijau" {area}',
                    f'"rumah dekat pesantren" OR "lokasi pendidikan islam" OR "fasilitas keagamaan" {area}',
                    f'"cari rumah dekat masjid agung" OR "perumahan muslim" OR "lokasi strategis" {area}',
                    f'"komunitas islami" OR "tetangga sefrekuensi" OR "lingkungan harmonis" {area}',
                ]
                
            elif campaign_mode == "HOLLYWOOD":
                # Content Creator Estates dorks
                base_queries = [
                    f'"komplain tetangga pas live" OR "kamar kedap suara" OR "rumah buat studio konten" {area}',
                    f'"rumah buat studio" OR "kamar rekaman" OR "kedap suara studio" {area}',
                    f'"rumah untuk konten" OR "studio di rumah" OR "kamar kedap" {area}',
                    f'"rumah dengan studio" OR "rumah konten creator" OR "lokasi streaming" {area}',
                    f'"rumah untuk youtuber" OR "studio rekaman" OR "rumah creator" {area}',
                    f'"komplain suara" OR "tetangga komplain" OR "kedap suara" {area}',
                    f'"rumah kedap suara" OR "studio kedap" OR "akustik studio" {area}',
                    f'"rumah untuk live streaming" OR "lokasi konten" OR "ruang kerja konten" {area}',
                    f'"rumah creator" OR "studio rekaman" OR "ruang produksi" {area}',
                    f'"rumah dengan fasilitas konten" OR "lokasi streaming" OR "akustik ruang" {area}',
                ]
                
            elif campaign_mode == "SYNDICATE":
                # Legal/Notary Intercept dorks
                base_queries = [
                    f'"biaya notaris AJB" OR "rekomendasi KJPP" OR "biaya balik nama SHM" {area}',
                    f'"biaya balik nama" OR "notaris murah" OR "rekomendasi notaris" {area}',
                    f'"biaya pembuatan SHM" OR "notaris terdekat" OR "KJPP murah" {area}',
                    f'"biaya balik nama murah" OR "rekomendasi notaris" OR "biaya AJB" {area}',
                    f'"biaya pembuatan AJB" OR "notaris terpercaya" OR "biaya balik nama" {area}',
                    f'"rekomendasi notaris" OR "biaya murah" OR "notaris cepat" {area}',
                    f'"biaya notaris SHM" OR "rekomendasi KJPP" OR "biaya pembuatan" {area}',
                    f'"biaya balik nama SHM" OR "notaris terdekat" OR "biaya AJB" {area}',
                    f'"biaya pembuatan AJB" OR "notaris terpercaya" OR "rekomendasi" {area}',
                    f'"biaya murah" OR "notaris cepat" OR "KJPP terdekat" OR "AJB murah" {area}',
                    f'"rekomendasi KJPP" OR "biaya pembuatan" OR "notaris strategis" {area}',
                ]
                
            elif campaign_mode == "LIFE_EVENTS":
                # Life events dorks for motivated sellers
                base_queries = [
                    f'"jual cepat" OR "jual BU" "untuk DP rumah" {area}',
                    f'"butuh uang" "jual rumah" {area} -pinjam -kredit',
                    f'"pindah" OR "relokasi" "jual rumah" {area} -sewa',
                    f'"cerai" OR "pisah" "jual asset" {area} -hak',
                    f'"waris" OR "wasiat" "jual properti" {area} -notaris',
                    f'"dagang" OR "usaha" "modal usaha" "jual rumah" {area}',
                    f'"kuliah" OR "biaya sekolah" "jual rumah" {area}',
                    f'"medis" OR "obat" "jual rumah" {area} -bpjs',
                    f'"utang" OR "cicilan" "jual rumah" {area} -bank',
                    f'"darurat" OR "keperluan" "jual cepat rumah" {area}',
                ]
                
            else:
                # Default regular mode
                base_queries = [
                    f'"cari rumah" {area} -kpr -subsidi',
                    f'"beli rumah" {area} -overpriced',
                    f'"properti" {area} -apartment',
                    f'"rumah dijual" {area} -agent',
                    f'"developer" {area} -scam',
                ]
            
            # Add area-specific variations
            if area:
                area_variations = [
                    area.lower(),
                    area.replace(" ", "").lower(),
                    area.replace(" ", "-").lower(),
                ]
                
                for query in base_queries:
                    for variation in area_variations:
                        if variation not in query.lower():
                            dork_queries.append(query.replace(area, variation, 1))
            
            # Add original queries
            dork_queries.extend(base_queries)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_queries = []
            for query in dork_queries:
                if query not in seen:
                    seen.add(query)
                    unique_queries.append(query)
            
            self.logger.info(f"{GREEN}✅ Generated {len(unique_queries)} unique dork queries{END}")
            self.logger.info(f"{CYAN}📋 Query modes: {campaign_mode}{END}")
            
            return unique_queries
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Dork generation error: {str(e)}{END}")
            return []
    
    def hunt_high_intent_targets(self, campaign_mode: str, area: str = "", competitors: List[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Hunt for high-intent targets using advanced Google Dorking
        
        Args:
            campaign_mode: Campaign mode (ORGANIC_SOSMED, HEADHUNTER, COMPETITOR_INTERCEPT, LIFE_EVENTS)
            area: Geographic area to focus on
            competitors: List of competitor names for COMPETITOR_INTERCEPT mode
            limit: Maximum number of targets to find
            
        Returns:
            Dictionary with hunting results and statistics
        """
        try:
            self.logger.info(f"{BLUE}🔍 ADVANCED TRIPWIRE SCOUT: Starting advanced intelligence hunt{END}")
            self.logger.info(f"{CYAN}⚔️ Campaign Mode: {campaign_mode}{END}")
            self.logger.info(f"{CYAN}📍 Area: {area if area else 'All areas'}{END}")
            self.logger.info(f"{CYAN}🎯 Target Limit: {limit}{END}")
            
            hunting_results = {
                "campaign_mode": campaign_mode,
                "area": area,
                "competitors": competitors or [],
                "start_time": datetime.now(),
                "targets_found": [],
                "total_queries": 0,
                "successful_extractions": 0,
                "failed_extractions": 0,
                "duplicates": 0,
                "campaign_sources": {},
                "status": "active"
            }
            
            # Generate dork queries
            dork_queries = self.generate_dork_queries(campaign_mode, area, competitors)
            hunting_results["total_queries"] = len(dork_queries)
            
            if not dork_queries:
                self.logger.warning(f"{YELLOW}⚠️ No dork queries generated{END}")
                hunting_results["status"] = "no_queries"
                hunting_results["end_time"] = datetime.now()
                return hunting_results
            
            self.logger.info(f"{CYAN}📋 Executing {len(dork_queries)} advanced dork queries{END}")
            
            # Execute each dork query
            for i, dork_query in enumerate(dork_queries, 1):
                self.logger.info(f"{YELLOW}🔍 Query {i}/{len(dork_queries)}: '{dork_query}'{END}")
                
                # Perform advanced search
                search_results = self._perform_advanced_search(dork_query)
                
                # Extract targets with advanced logic
                targets = self._extract_targets_from_advanced_results(search_results, dork_query, campaign_mode)
                
                # Add targets to results
                for target in targets:
                    # Check for duplicates
                    if not self._is_duplicate_target(target, hunting_results["targets_found"]):
                        hunting_results["targets_found"].append(target)
                        hunting_results["successful_extractions"] += 1
                        
                        # Track campaign source
                        campaign_source = target.get('campaign_source', 'unknown')
                        if campaign_source not in hunting_results["campaign_sources"]:
                            hunting_results["campaign_sources"][campaign_source] = 0
                        hunting_results["campaign_sources"][campaign_source] += 1
                        
                        self.logger.info(f"{GREEN}✅ Target found: {target['contact_info'] or target['social_profile'] or target['url'][:50]}{END}")
                    else:
                        hunting_results["duplicates"] += 1
                
                # Rate limiting to avoid blocking
                time.sleep(2)
                
                # Stop if limit reached
                if len(hunting_results["targets_found"]) >= limit:
                    self.logger.info(f"{CYAN}📋 Target limit reached: {limit}{END}")
                    break
            
            # Save targets to database
            saved_count = self._save_advanced_targets_to_database(hunting_results["targets_found"])
            
            # Update results
            hunting_results["end_time"] = datetime.now()
            hunting_results["duration"] = (hunting_results["end_time"] - hunting_results["start_time"]).total_seconds()
            hunting_results["targets_saved"] = saved_count
            hunting_results["status"] = "completed"
            
            # Send completion notification
            self._send_advanced_hunting_notification(hunting_results)
            
            self.logger.info(f"{GREEN}✅ ADVANCED TRIPWIRE SCOUT: Hunt completed{END}")
            self.logger.info(f"{CYAN}📊 Results: {len(hunting_results['targets_found'])} targets found, {saved_count} saved{END}")
            self.logger.info(f"{CYAN}📋 Campaign Sources: {hunting_results['campaign_sources']}{END}")
            
            return hunting_results
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Advanced hunting error: {str(e)}{END}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _perform_advanced_search(self, dork_query: str) -> List[Dict[str, Any]]:
        """Perform advanced search using Google Dork"""
        try:
            # Use DuckDuckGo for dork execution (more permissive than Google)
            url = "https://duckduckgo.com/html/"
            params = {
                'q': dork_query,
                'kl': 'us-en',
                'ad': 'n',
                'df': 'q',
                'safesearch': 'on',
                'source': 'web',
                'num': '20'
            }
            
            response = requests.get(url, params=params, headers=self.search_headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML results
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extract search results
            for result in soup.find_all('div', class_='result'):
                try:
                    title_elem = result.find('a', class_='result__a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet_elem = result.find('a', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'duckduckgo_advanced',
                            'dork_query': dork_query
                        })
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Advanced search error: {str(e)}{END}")
            return []
    
    def _extract_targets_from_advanced_results(self, search_results: List[Dict[str, Any]], dork_query: str, campaign_mode: str) -> List[Dict[str, Any]]:
        """Extract targets with advanced social media and contact extraction"""
        targets = []
        
        for result in search_results:
            try:
                target = {
                    'dork_query': dork_query,
                    'campaign_mode': campaign_mode,
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('snippet', ''),
                    'source': result.get('source', 'duckduckgo_advanced'),
                    'contact_info': None,
                    'contact_type': None,
                    'social_profile': None,
                    'social_platform': None,
                    'social_username': None,
                    'confidence_score': 0,
                    'scouted_at': datetime.now().isoformat(),
                    'status': 'scouted',
                    'campaign_source': dork_query[:100]  # Track which dork found this
                }
                
                # Advanced extraction logic
                extracted_info = self._extract_advanced_contact_info(result, campaign_mode)
                target.update(extracted_info)
                
                # Calculate confidence score
                target['confidence_score'] = self._calculate_advanced_confidence_score(target, campaign_mode)
                
                # Only include targets with meaningful data
                if target['confidence_score'] > 30:
                    targets.append(target)
                
            except Exception as e:
                self.logger.error(f"{RED}❌ Advanced target extraction error: {str(e)}{END}")
                continue
        
        return targets
    
    def _extract_advanced_contact_info(self, result: Dict[str, Any], campaign_mode: str) -> Dict[str, Any]:
        """Extract advanced contact and social media information"""
        extracted_info = {}
        
        # Combine all text for analysis
        text_to_analyze = f"{result.get('title', '')} {result.get('snippet', '')} {result.get('url', '')}"
        url = result.get('url', '')
        
        # Extract social media profiles
        social_info = self._extract_social_profiles(url, text_to_analyze)
        if social_info:
            extracted_info.update(social_info)
        
        # Extract contact information
        contact_info = self._extract_contact_info(text_to_analyze)
        if contact_info:
            extracted_info.update(contact_info)
        
        # Campaign-specific extraction
        if campaign_mode == "HEADHUNTER":
            # Look for executive indicators
            executive_keywords = ['manager', 'director', 'executive', 'cxo', 'vp', 'president', 'leader']
            if any(keyword in text_to_analyze.lower() for keyword in executive_keywords):
                extracted_info['executive_indicators'] = True
                extracted_info['confidence_boost'] = 20
        
        elif campaign_mode == "COMPETITOR_INTERCEPT":
            # Look for complaint indicators
            complaint_keywords = ['kecewa', 'bermasalah', 'komplain', 'keluhan', 'buruk', 'jelek']
            if any(keyword in text_to_analyze.lower() for keyword in complaint_keywords):
                extracted_info['complaint_indicators'] = True
                extracted_info['confidence_boost'] = 25
        
        elif campaign_mode == "UPGRADER_INTERCEPT":
            # Look for upgrade indicators
            upgrade_keywords = ['upgrade', 'pindah', 'tipe 36', 'overkredit', 'rumah murah', 'rumah kecil']
            if any(keyword in text_to_analyze.lower() for keyword in upgrade_keywords):
                extracted_info['upgrade_indicators'] = True
                extracted_info['confidence_boost'] = 25
        
        elif campaign_mode == "NESTING_INSTINCT":
            # Look for nesting indicators
            nesting_keywords = ['dokter kandungan', 'vendor WO', 'gedung pernikahan', 'pernikahan', 'wedding', 'MC', 'fotografer']
            if any(keyword in text_to_analyze.lower() for keyword in nesting_keywords):
                extracted_info['nesting_indicators'] = True
                extracted_info['confidence_boost'] = 30
        
        elif campaign_mode == "MIGRATION_RADAR":
            # Look for migration indicators
            migration_keywords = ['biaya hidup', 'moving to', 'relokasi', 'cost of living', 'expat', 'salary', 'housing']
            if any(keyword in text_to_analyze.lower() for keyword in migration_keywords):
                extracted_info['migration_indicators'] = True
                extracted_info['confidence_boost'] = 20
        
        elif campaign_mode == "WINDFALL_ANOMALY":
            # Look for windfall indicators
            windfall_keywords = ['alhamdulillah cair', 'uang pesangon', 'dana nganggur', 'cair JHT', 'uang cash', 'uang tunai']
            if any(keyword in text_to_analyze.lower() for keyword in windfall_keywords):
                extracted_info['windfall_indicators'] = True
                extracted_info['confidence_boost'] = 35
        
        elif campaign_mode == "PANOPTICON":
            # Look for review indicators
            review_keywords = ['review', 'kecewa', 'buruk', 'jelek', 'tidak', 'masalah', 'keluhan', 'saran', 'pengalaman', 'kerja', 'investasi']
            if any(keyword in text_to_analyze.lower() for keyword in review_keywords):
                extracted_info['review_indicators'] = True
                extracted_info['confidence_boost'] = 20
        
        elif campaign_mode == "LEVIATHAN":
            # Look for tender/funding indicators
            tender_keywords = ['pemenang tender', 'mendapatkan pendanaan', 'meraih pendanaan', 'funding', 'investasi', 'startup', 'bisnis', 'modal', 'venture', 'series', 'seed']
            if any(keyword in text_to_analyze.lower() for keyword in tender_keywords):
                extracted_info['tender_indicators'] = True
                extracted_info['confidence_boost'] = 25
        
        elif campaign_mode == "PROXY_WEALTH":
            # Look for luxury indicators
            luxury_keywords = ['rolex', 'rubicon', 'stik golf', 'titleist', 'patek philippe', 'omega', 'audemars piguet', 'breitling', 'tag heuer', 'cartier', 'jam mewah', 'branded', 'mobil mewah', 'perhiasan emas']
            if any(keyword in text_to_analyze.lower() for keyword in luxury_keywords):
                extracted_info['luxury_indicators'] = True
                extracted_info['confidence_boost'] = 40
        
        elif campaign_mode == "TRANSITION":
            # Look for life transition indicators
            transition_keywords = ['pengacara keluarga', 'rumah gono gini', 'rumah warisan', 'jual rumah hibah', 'rumah pensiunan', 'pengacara perceraian', 'jual rumah cerai', 'konsultan hibah', 'ahli waris', 'notaris perceraian', 'mediator keluarga']
            if any(keyword in text_to_analyze.lower() for keyword in transition_keywords):
                extracted_info['transition_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "CHOKEPOINT":
            # Look for commuter distress indicators
            commuter_keywords = ['tua di jalan', 'capek krl', 'pengen ngekos', 'macet parah', 'jalan kantor', 'stres perjalanan', 'capek commuter', 'waktu tempuh', 'macet pagi', 'macet sore', 'lelah commuting']
            if any(keyword in text_to_analyze.lower() for keyword in commuter_keywords):
                extracted_info['commuter_distress_indicators'] = True
                extracted_info['confidence_boost'] = 35
        
        elif campaign_mode == "VULTURE":
            # Look for auction investor indicators
            auction_keywords = ['prosedur lelang bank', 'cari properti BU', 'menang lelang KPKNL', 'lelang bank', 'asset lelang', 'properti sitaan', 'rumah sitaan', 'cash buyer', 'pembeli tunai', 'properti undervalued', 'bank foreclosure', 'sitasi']
            if any(keyword in text_to_analyze.lower() for keyword in auction_keywords):
                extracted_info['auction_investor_indicators'] = True
                extracted_info['confidence_boost'] = 40
        
        elif campaign_mode == "NEUROMANCER":
            # Look for new money/crypto whale indicators
            crypto_keywords = ['cuan kripto', 'take profit saham', 'porto hijau', 'baru IPO', 'profit crypto', 'saham untung', 'bitcoin profit', 'crypto millionaire', 'exit crypto', 'hedging', 'diversification', 'tech money', 'crypto wealth', 'portfolio rebalancing']
            if any(keyword in text_to_analyze.lower() for keyword in crypto_keywords):
                extracted_info['crypto_whale_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "BLOODLINE":
            # Look for generational wealth indicators
            generational_keywords = ['proud parent', 'wisuda putri', 'lulus dari', 'graduation gift', 'anak lulus', 'property for child', 'parent investment', 'family wealth', 'successful parent', 'first home', 'child education', 'wealth management', 'luxury property']
            if any(keyword in text_to_analyze.lower() for keyword in generational_keywords):
                extracted_info['generational_wealth_indicators'] = True
                extracted_info['confidence_boost'] = 50
        
        elif campaign_mode == "PROPHET":
            # Look for compensation indicators
            compensation_keywords = ['pembayaran uang ganti rugi', 'warga desa terima miliaran', 'cair ganti rugi lahan', 'uang kompensasi', 'ganti rugi lahan', 'pembayaran kompensasi', 'cair uang kompensasi', 'penerima uang kompensasi', 'warga dapat miliaran', 'pembebasan lahan', 'kompensasi tanah']
            if any(keyword in text_to_analyze.lower() for keyword in compensation_keywords):
                extracted_info['compensation_indicators'] = True
                extracted_info['confidence_boost'] = 55
        
        elif campaign_mode == "PARASITE":
            # Look for dark social indicators
            dark_social_keywords = ['chat.whatsapp.com', 't.me/joinchat', 'warga', 'investor', 'properti', 'rumah', 'investasi', 'bisnis', 'developer', 'pengusaha', 'komunitas', 'diskusi']
            if any(keyword in text_to_analyze.lower() for keyword in dark_social_keywords):
                extracted_info['dark_social_indicators'] = True
                extracted_info['confidence_boost'] = 30
        
        elif campaign_mode == "RENEGADE":
            # Look for KPR rejection indicators
            rejection_keywords = ['KPR ditolak bank', 'gagal BI checking', 'susah KPR karena freelance', 'KPR tidak disetujui', 'BI checking gagal', 'freelance tidak dapat KPR', 'penolakan KPR', 'checking gagal', 'susah approval KPR', 'BI checking tidak lulus', 'gagal KPR', 'checking gagal', 'penghasilan tidak tetap', 'KPR freelance', 'approval KPR gagal', 'penolakan bank', 'KPR tidak disetujui']
            if any(keyword in text_to_analyze.lower() for keyword in rejection_keywords):
                extracted_info['kpr_rejection_indicators'] = True
                extracted_info['confidence_boost'] = 35
        
        elif campaign_mode == "BLACKHOLE":
            # Look for forum/question indicators
            forum_keywords = ['cara beli rumah', 'tips beli rumah', 'panduan beli rumah', 'how to buy house', 'house buying guide', 'home purchase tips', 'beli rumah pertama', 'tips rumah pertama', 'panduan rumah pertama', 'cara KPR rumah', 'tips KPR rumah', 'panduan KPR rumah', 'investasi properti', 'tips investasi properti', 'panduan investasi properti']
            if any(keyword in text_to_analyze.lower() for keyword in forum_keywords):
                extracted_info['forum_question_indicators'] = True
                extracted_info['confidence_boost'] = 25
        
        elif campaign_mode == "OXYGEN":
            # Look for health/environmental indicators
            health_keywords = ['anak sering ISPA', 'udara jakarta memburuk', 'cari daerah asri', 'rekomendasi air purifier', 'polusi udara', 'kualitas udara buruk', 'rumah sehat', 'lingkungan hijau', 'air bersih', 'filter air', 'air minum sehat', 'tanpa polusi', 'kesehatan keluarga', 'lingkungan bersih', 'rumah sehat', 'daerah bebas polusi', 'rekomendasi area sehat', 'tempat tinggal sehat', 'lokasi bersih', 'masker udara', 'air purifier', 'filter polusi', 'kualitas udara', 'hindari polusi', 'lokasi asri', 'lingkungan hijau', 'rumah di luar kota', 'rekomendasi tempat tinggal', 'area bersih', 'kualitas hidup', 'penyakit pernapasan', 'asma anak', 'alergi polusi', 'udara bersih']
            if any(keyword in text_to_analyze.lower() for keyword in health_keywords):
                extracted_info['health_environmental_indicators'] = True
                extracted_info['confidence_boost'] = 35
        
        elif campaign_mode == "DIASPORA":
            # Look for cross-border wealth indicators
            diaspora_keywords = ['pekerja migran', 'cara KPR dari luar negeri', 'investasi dari luar negeri', 'TKI', 'TKW', 'pekerja indonesia di luar negeri', 'investasi properti dari luar negeri', 'pekerja migran malaysia', 'pekerja migran singapura', 'investasi dari malaysia', 'pekerja migran hongkong', 'pekerja migran taiwan', 'investasi dari hongkong', 'TKI di luar negeri', 'TKW di luar negeri', 'properti untuk TKI', 'investasi properti', 'beli properti dari luar negeri', 'KPR untuk WNI', 'rekomendasi investasi', 'tips investasi', 'cara investasi properti', 'pekerja indonesia', 'pengiriman TKI', 'remitansi ke indonesia', 'bisnis luar negeri', 'usaha TKI', 'peluang bisnis', 'properti untuk TKI', 'rumah untuk TKI', 'investasi aman']
            if any(keyword in text_to_analyze.lower() for keyword in diaspora_keywords):
                extracted_info['cross_border_wealth_indicators'] = True
                extracted_info['confidence_boost'] = 40
        
        elif campaign_mode == "HABITAT":
            # Look for space-demanding hobbies indicators
            habitat_keywords = ['komunitas anjing besar', 'butuh garasi luas', 'bikin taman luas', 'jual anjing karena pindah', 'hobi memelihara hewan', 'butuh lahan luas', 'bikin kandang', 'tempat tinggal untuk hewan peliharaan', 'komunitas kucing', 'butuh rumah untuk kucing', 'pelihara hewan', 'pet friendly', 'komunitas burung', 'avicultur', 'bikin sangkar burung', 'tempat untuk burung', 'komunitas reptil', 'pelihara reptil', 'terarium', 'bikin kandang reptil', 'komunitas ikan', 'aquarium', 'ikan hias', 'bikin kolam ikan', 'hobi pertanian', 'berkebun', 'lahan pertanian', 'rumah dengan kebun', 'komunitas tanaman hias', 'florist', 'bikin taman', 'rumah dengan taman', 'komunitas fitness', 'olahraga', 'gym di rumah', 'tempat olahraga']
            if any(keyword in text_to_analyze.lower() for keyword in habitat_keywords):
                extracted_info['space_demanding_hobbies_indicators'] = True
                extracted_info['confidence_boost'] = 30
        
        elif campaign_mode == "SYMBIOSIS":
            # Look for supply chain indicators
            symbiosis_keywords = ['jasa angkut pindahan', 'jasa interior', 'jasa angkut barang', 'jasa pindahan', 'jasa packing', 'jasa desain interior', 'interior design', 'dekor rumah', 'jasa renovasi', 'kontraktor renovasi', 'tukang bangun', 'jasa angkut mobil', 'jasa ekspedisi', 'jasa logistik', 'jasa pembersihan', 'cleaning service', 'jasa bersih', 'jasa catering', 'katering', 'jasa makanan', 'jasa event organizer', 'EO', 'event planner', 'jasa photography', 'fotografer', 'dokumentasi', 'jasa pernikahan', 'wedding organizer', 'wedding planner']
            if any(keyword in text_to_analyze.lower() for keyword in symbiosis_keywords):
                extracted_info['supply_chain_indicators'] = True
                extracted_info['confidence_boost'] = 25
        
        elif campaign_mode == "DISTRESS":
            # Look for debt-driven relocation indicators
            distress_keywords = ['restrukturisasi utang KPR', 'sita jaminan bank', 'jual BU bayar utang', 'konsolidasi utang', 'gabung pinjaman', 'bayar utang dengan jual properti', 'jual rumah untuk bayar utang', 'jual cepat bayar utang', 'jual aset bayar utang', 'kredit macet', 'refinancing KPR', 'take over KPR', 'bantuan bayar utang', 'pinjaman lunas', 'pinjaman tanpa agunan', 'dana talangan', 'uang darurat', 'bantuan restrukturisasi utang', 'konsultan utang', 'penyelesaian masalah utang', 'jual aset untuk bayar utang', 'likuidasi aset', 'dana tunai cepat', 'cara bayar utang', 'solusi masalah keuangan', 'keluar dari masalah utang', 'bantuan finansial', 'konsultasi keuangan', 'restrukturisasi finansial', 'uang darurat', 'dana cepat', 'pinjaman darurat', 'butuh uang sekarang']
            if any(keyword in text_to_analyze.lower() for keyword in distress_keywords):
                extracted_info['debt_driven_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "REBELLION":
            # Look for angry renters indicators
            rebellion_keywords = ['ibu kost galak', 'capek ngontrak', 'harga sewa naik', 'kontrakan bocor', 'pemilik kost galak', 'sakit ngontrak', 'sewa naik terus', 'kontrak tidak diperpanjang', 'capek bayar sewa', 'harga sewa tidak wajar', 'pemilik sewa nakal', 'kontrak sewa tidak adil', 'pindah karena sewa', 'cari rumah sendiri', 'berhenti ngontrak', 'sakit sewa', 'uang sewa hangus', 'cicilan sewa sia-sia', 'sewa lebih mahal dari KPR', 'ingin punya rumah', 'pemilik sewa tidak bertanggung jawab', 'kontrak sewa tidak jelas', 'biaya sewa tidak masuk akal', 'capek dari kontrak', 'ingin keluar dari kos', 'pindah dari kost', 'sewa tidak nyaman', 'pemilik sewa serakah', 'sewa tidak sesuai', 'kontrak sewa bermasalah', 'uang sewa mubazir', 'ingin akuisisi properti', 'stop sewa beli rumah', 'dari ngontrak ke KPR', 'sewa vs cicilan']
            if any(keyword in text_to_analyze.lower() for keyword in rebellion_keywords):
                extracted_info['angry_renters_indicators'] = True
                extracted_info['confidence_boost'] = 50
        
        elif campaign_mode == "SANDWICH":
            # Look for multi-generational housing indicators
            sandwich_keywords = ['rumah untuk mertua', 'kamar bawah orang tua sakit', 'gabung rumah mertua', 'rumah 2 lantai untuk keluarga', 'rumah dengan kamar bawah', 'rumah untuk orang tua', 'tinggal bersama orang tua', 'rumah keluarga besar', 'rumah multi generasi', 'kamar untuk lansia', 'rumah dengan fasilitas lansia', 'rumah untuk orang tua lanjut usia', 'rumah dengan kamar terpisah', 'rumah untuk mertua dan anak', 'desain rumah keluarga', 'rumah untuk orang tua sakit', 'kamar perawat lansia', 'rumah dengan akses mudah untuk lansia', 'rumah 3 kamar untuk keluarga', 'rumah dengan kamar tambahan', 'rumah untuk keluarga besar', 'rumah dengan fasilitas lansia', 'rumah aksesibel untuk lansia', 'rumah untuk orang tua', 'rumah multi generasi', 'rumah untuk 3 generasi', 'rumah dengan kamar bawah']
            if any(keyword in text_to_analyze.lower() for keyword in sandwich_keywords):
                extracted_info['multi_generational_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "EXODUS":
            # Look for WFH & digital nomads indicators
            exodus_keywords = ['pindah ke pinggir kota', 'wfh selamanya', 'bikin studio kedap suara', 'biznet masuk daerah', 'kerja remote dari pinggir kota', 'rumah WFH', 'studio untuk WFH', 'internet cepat pinggir kota', 'digital nomad', 'kerja dari mana saja', 'rumah dengan internet cepat', 'tempat tinggal remote', 'bikin studio di rumah', 'ruang kerja di rumah', 'home office', 'WFH permanent', 'pindah ke luar kota', 'rumah pinggir kota', 'lokasi WFH', 'internet stabil', 'bikin studio kedap suara', 'ruang studio kedap', 'home studio', 'musik studio', 'biznet masuk daerah', 'internet fiber', 'koneksi internet cepat', 'lokasi remote work', 'pindah karena WFH', 'kerja dari rumah permanen', 'rumah dengan fasilitas WFH', 'tempat kerja remote', 'digital lifestyle', 'remote work lifestyle', 'work from anywhere', 'nomad life', 'rumah dengan koneksi baik', 'internet stabil untuk WFH', 'lokasi remote work friendly']
            if any(keyword in text_to_analyze.lower() for keyword in exodus_keywords):
                extracted_info['wfh_digital_nomads_indicators'] = True
                extracted_info['confidence_boost'] = 40
        
        elif campaign_mode == "GENTRIFICATION":
            # Look for infrastructure speculators indicators
            gentrification_keywords = ['pembangunan kampus baru', 'cari tanah dekat kampus', 'bikin kost kostan di', 'pembangunan rumah sakit', 'tanah dekat fasilitas umum', 'investasi infrastruktur', 'pembangunan tol', 'tanah dekat jalan tol', 'lokasi strategis infrastruktur', 'pembangunan mall', 'tanah dekat pusat perbelanjaan', 'investasi komersial', 'pembangunan stasiun', 'tanah dekat transportasi umum', 'lokasi dekat MRT', 'pembangunan sekolah', 'tanah dekat sekolah', 'investasi pendidikan', 'pembangunan kawasan industri', 'tanah dekat pabrik', 'investasi industri', 'pembangunan bandara', 'tanah dekat bandara', 'lokasi strategis transportasi udara', 'pembangunan pelabuhan', 'tanah dekat pelabuhan', 'investasi logistik', 'pembangunan fasilitas', 'tanah dekat fasilitas publik', 'lokasi dekat infrastruktur']
            if any(keyword in text_to_analyze.lower() for keyword in gentrification_keywords):
                extracted_info['infrastructure_speculators_indicators'] = True
                extracted_info['confidence_boost'] = 55
        
        elif campaign_mode == "LOTTERY":
            # Look for policy & subsidy hunters indicators
            lottery_keywords = ['kapan bebas PPN', 'rumah DP 0 rupiah', 'kuota FLPP', 'subsidi KPR', 'PPN ditanggung', 'rumah tanpa DP', 'subsidi rumah', 'bantuan KPR', 'FLPP 2024', 'kuota FLPP', 'subsidi perumahan', 'rumah murah', 'KPR subsidi', 'bunga KPR', 'KPR rendah', 'rumah subsidi', 'rumah DP 0', 'tanpa DP', 'cicilan ringan', 'rumah murah', 'program rumah murah', 'bantuan perumahan', 'kuota rumah murah', 'subsidi Pemerintah', 'PPN 0%', 'bebas PPN', 'diskon PPN', 'rumah tanpa PPN', 'bantuan DP', 'subsidi DP', 'bantuan uang muka', 'cicilan dibantu', 'promo KPR', 'diskon KPR', 'bunga KPR', 'KPR murah', 'KPR ringan', 'program perumahan', 'kuota perumahan', 'rumah bersubsidi', 'bantuan perumahan']
            if any(keyword in text_to_analyze.lower() for keyword in lottery_keywords):
                extracted_info['policy_subsidy_hunters_indicators'] = True
                extracted_info['confidence_boost'] = 60
        
        elif campaign_mode == "LOGISTICS":
            # Look for e-commerce boom indicators
            logistics_keywords = ['ruang tamu penuh paket', 'butuh ruko untuk shopee', 'ditegur RT karena kurir', 'admin packing rumah', 'gudang untuk online shop', 'butuh tempat packing', 'sewa gudang kecil', 'usaha dari rumah', 'dropship dari rumah', 'stok barang di rumah', 'bikin toko online', 'jualan online dari rumah', 'butuh ruang usaha', 'cari ruko murah', 'sewa ruko bulanan', 'tempat usaha kecil', 'online shop butuh gudang', 'packing dan pengiriman', 'kurir sering lewat', 'tetangga komplain pengiriman', 'bisnis dari rumah', 'usaha e-commerce', 'butuh tempat usaha', 'ruang kerja di rumah', 'stock barang di rumah', 'butuh gudang kecil', 'sewa tempat usaha', 'cari ruko untuk bisnis', 'admin packing di rumah', 'butuh ruang gudang', 'usaha online shop', 'tempat untuk bisnis online', 'kurir sering lewat rumah', 'tetangga komplain bisnis', 'butuh tempat usaha terpisah', 'cari ruko untuk toko online']
            if any(keyword in text_to_analyze.lower() for keyword in logistics_keywords):
                extracted_info['ecommerce_boom_indicators'] = True
                extracted_info['confidence_boost'] = 55
        
        elif campaign_mode == "EV_TRAP":
            # Look for electric vehicle charging crisis indicators
            ev_trap_keywords = ['tambah daya PLN ngecas mobil', 'gak ada garasi', 'sewa garasi bulanan', 'pasang wallbox wuling', 'butuh garasi untuk mobil listrik', 'pasang charger mobil listrik', 'daya listrik tidak cukup', 'ngecas mobil di rumah', 'sewa garasi untuk mobil listrik', 'cari rumah dengan garasi luas', 'butuh daya besar untuk EV', 'charging station di rumah', 'pasang wallbox di rumah', 'tambah daya listrik untuk mobil listrik', 'butuh garasi untuk mobil', 'daya listrik tidak kuat', 'ngecas mobil listrik di rumah', 'butuh tempat charging mobil', 'daya listrik untuk EV', 'garasi untuk mobil listrik', 'sewa tempat untuk mobil listrik', 'cari rumah dengan listrik besar', 'butuh charging station', 'daya listrik untuk charging', 'butuh garasi bulanan', 'cari rumah dengan garasi', 'pasang charger mobil', 'listrik tidak cukup untuk EV', 'wallbox untuk mobil listrik', 'daya listrik untuk wallbox', 'butuh tempat charging', 'garasi untuk mobil elektrik', 'charging mobil listrik', 'butuh daya listrik besar', 'cari rumah dengan garasi luas', 'sewa tempat charging']
            if any(keyword in text_to_analyze.lower() for keyword in ev_trap_keywords):
                extracted_info['ev_charging_crisis_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "TABULA_RASA":
            # Look for life escape/healing indicators
            tabula_rasa_keywords = ['over dp gedung pernikahan', 'batal nikah jual cincin', 'butuh tempat baru healing', 'butuh tempat tinggal baru', 'mulai hidup baru', 'cari ketenangan', 'butuh privasi', 'butuh tempat healing', 'cari lingkungan tenang', 'butuh kedamaian', 'pindah untuk ketenangan', 'jual cincin pernikahan', 'batal pernikahan', 'butuh tempat baru', 'mulai hidup sendiri', 'butuh rumah untuk healing', 'cari lingkungan yang tenang', 'butuh privasi', 'pindah dari kota', 'butuh kedamaian', 'cari ketenangan', 'butuh lingkungan yang tenang', 'butuh tempat untuk healing', 'butuh rumah sendiri', 'cari ketenangan', 'butuh privasi', 'mulai hidup baru', 'butuh tempat tinggal yang tenang', 'cari lingkungan yang damai', 'butuh kedamaian', 'butuh rumah untuk healing', 'butuh rumah sendiri', 'cari rumah untuk healing', 'butuh privasi', 'butuh ketenangan']
            if any(keyword in text_to_analyze.lower() for keyword in tabula_rasa_keywords):
                extracted_info['life_escape_healing_indicators'] = True
                extracted_info['confidence_boost'] = 40
        
        elif campaign_mode == "HEIRLOOM":
            # Look for inheritance & insurance liquidators indicators
            heirloom_keywords = ['cara urus turun waris', 'asuransi jiwa cair', 'jual tanah warisan', 'dapat warisan dari orang tua', 'asuransi cair', 'jual tanah warisan', 'investasi warisan', 'cara mengurus warisan', 'asuransi jiwa cair', 'jual properti warisan', 'investasi dari warisan', 'dapat uang dari asuransi', 'jual tanah warisan', 'investasi warisan', 'cara mengurus warisan', 'warisan dari orang tua', 'asuransi jiwa cair', 'jual properti warisan', 'investasi dari warisan', 'dapat uang warisan', 'jual tanah warisan', 'investasi warisan', 'cara mengurus warisan', 'asuransi cair', 'jual tanah warisan', 'investasi warisan', 'cara mengurus warisan', 'warisan keluarga', 'asuransi jiwa cair', 'jual properti warisan', 'investasi dari warisan', 'dapat uang asuransi', 'jual tanah warisan', 'investasi warisan', 'cara mengurus warisan']
            if any(keyword in text_to_analyze.lower() for keyword in heirloom_keywords):
                extracted_info['inheritance_insurance_indicators'] = True
                extracted_info['confidence_boost'] = 65
        
        elif campaign_mode == "ZOOKEEPER":
            # Look for extreme pet owners indicators
            zookeeper_keywords = ['ditegur RT karena pelihara', 'bikin kandang aviary', 'peredam suara burung', 'butuh rumah untuk pelihara hewan', 'bikin kandang burung', 'peredam suara untuk hewan', 'pelihara hewan di rumah', 'komplain RT karena pelihara', 'butuh kandang untuk burung', 'peredam suara untuk peliharaan', 'hewan peliharaan', 'butuh rumah dengan halaman', 'bikin kandang untuk hewan', 'peredam suara untuk burung', 'pelihara hewan besar', 'butuh ruang untuk hewan', 'bikin kandang aviary', 'peredam suara untuk peliharaan', 'hewan peliharaan', 'butuh rumah dengan taman', 'bikin kandang untuk burung', 'peredam suara untuk hewan', 'pelihara hewan di rumah', 'butuh halaman untuk hewan', 'bikin kandang untuk peliharaan', 'peredam suara untuk burung', 'hewan peliharaan', 'butuh rumah untuk hewan', 'bikin kandang untuk burung', 'peredam suara untuk peliharaan', 'hewan peliharaan', 'butuh ruang untuk peliharaan', 'bikin kandang untuk hewan', 'peredam suara untuk burung', 'hewan peliharaan']
            if any(keyword in text_to_analyze.lower() for keyword in zookeeper_keywords):
                extracted_info['extreme_pet_owners_indicators'] = True
                extracted_info['confidence_boost'] = 35
        
        elif campaign_mode == "HLR_SNIPER":
            # Look for regional prefix targeting indicators
            hlr_sniper_keywords = ['jual cepat', 'dijual rugi', 'jual BU', 'overkredit', 'butuh uang cepat', 'jual murah', 'take over', 'nego', 'dijual cepat', 'over kredit', 'cicilan ringan', 'bisa nego', 'jual asset', 'butuh dana', 'jual properti', 'take over KPR', 'dijual rugi', 'over kredit', 'cicilan bisa nego', 'butuh dana', 'jual cepat rumah', 'over kredit', 'take over', 'nego keras', 'dijual BU', 'over kredit', 'cicilan ringan', 'bisa nego', 'jual properti', 'butuh dana', 'over kredit', 'nego', 'jual cepat', 'over kredit', 'take over', 'cicilan ringan']
            if any(keyword in text_to_analyze.lower() for keyword in hlr_sniper_keywords):
                extracted_info['regional_prefix_indicators'] = True
                extracted_info['confidence_boost'] = 70
        
        elif campaign_mode == "WA_ME_INTERCEPT":
            # Look for direct WA link harvesting indicators
            wa_me_intercept_keywords = ['wa.me/62', 'api.whatsapp.com/send', '628', '08', 'cari rumah', 'tanya KPR', 'butuh kontrakan', 'jual rumah', 'cari rumah', 'butuh properti', 'tanya KPR', 'butuh KPR', 'cicilan', 'jual cepat', 'dijual', 'nego', 'butuh kontrakan', 'cari kontrakan', 'sewa rumah', 'cari rumah murah', 'rumah murah', 'properti murah', 'tanya harga', 'berapa harga', 'info', 'survey', 'cek lokasi', 'lihat rumah', 'butuh info', 'tanya', 'detail properti']
            if any(keyword in text_to_analyze.lower() for keyword in wa_me_intercept_keywords):
                extracted_info['wa_link_harvesting_indicators'] = True
                extracted_info['confidence_boost'] = 50
        
        elif campaign_mode == "ISP_GEO":
            # Look for localized WiFi complaints indicators
            isp_geo_keywords = ['biznet gangguan', 'indihome los merah', 'pasang wifi murah', 'wifi tidak stabil', 'internet lemot', 'koneksi internet jelek', 'pasang wifi baru', 'butuh internet cepat', 'provider internet', 'wifi murah', 'internet rumah', 'pasang indihome', 'biznet', 'gangguan internet', 'wifi putus', 'koneksi tidak stabil', 'indihome gangguan', 'biznet tidak stabil', 'wifi lemot', 'butuh provider wifi', 'internet untuk rumah', 'pasang internet', 'wifi untuk WFH', 'internet kerja dari rumah', 'koneksi stabil', 'keluhan wifi', 'komplain internet', 'provider tidak bagus']
            if any(keyword in text_to_analyze.lower() for keyword in isp_geo_keywords):
                extracted_info['wifi_complaints_indicators'] = True
                extracted_info['confidence_boost'] = 30
        
        elif campaign_mode == "COMMUTE_NODE":
            # Look for micro-transit tracing indicators
            commute_node_keywords = ['angkot rute', 'titik jemput stasiun', 'ojek pangkalan', 'halte bus', 'stasiun terdekat', 'rute angkot', 'ojek online', 'transportasi umum', 'akses stasiun', 'titik jemput', 'pangkalan ojek', 'rute transportasi', 'halte terdekat', 'stasiun commuter', 'ojek pangkalan', 'akses commuter', 'halte bus', 'rute angkot', 'ojek online', 'transportasi ke stasiun', 'halte commuter', 'rute angkot', 'pangkalan', 'akses commuter line', 'halte bus', 'stasiun terdekat', 'ojek pangkalan', 'rute angkot ke stasiun', 'titik jemput commuter', 'ojek pangkalan', 'halte commuter', 'stasiun commuter', 'rute angkot', 'ojek online']
            if any(keyword in text_to_analyze.lower() for keyword in commute_node_keywords):
                extracted_info['micro_transit_indicators'] = True
                extracted_info['confidence_boost'] = 25
        
        elif campaign_mode == "GAVEL":
            # Look for court/SIPP public records indicators
            gavel_keywords = ['harta gono gini', 'pembagian rumah cerai', 'putusan cerai', 'pembagian harta', 'gugatan cerai', 'harta bersama', 'eksekusi putusan', 'eksekusi harta', 'mediasi perceraian', 'damai', 'proses cerai', 'hak asuh anak', 'nafkah', 'pembagian harta', 'harta bersama', 'perceraian cepat', 'biaya cerai', 'putusan hak milik', 'sengketa harta']
            if any(keyword in text_to_analyze.lower() for keyword in gavel_keywords):
                extracted_info['court_sipp_indicators'] = True
                extracted_info['confidence_boost'] = 75
        
        elif campaign_mode == "PROGRESSIVE":
            # Look for vehicle tax/space exhaustion indicators
            progressive_keywords = ['pajak progresif mobil ke 3', 'bikin garasi di luar', 'ditegur RT parkir mobil', 'pajak mobil naik', 'butuh garasi tambahan', 'parkir mobil di luar', 'pajak kendaraan', 'garasi penuh', 'parkir mobil di depan rumah', 'pajak progresif', 'butuh tempat parkir', 'garasi tidak cukup', 'pajak mobil ke 2', 'bikin garasi sampingan', 'parkir di halaman', 'pajak kendaraan tinggi', 'butuh lahan parkir', 'garasi ekstensi', 'pajak progresif naik', 'garasi tidak muat', 'parkir di trotoar', 'pajak mobil mahal', 'butuh tempat parkir mobil', 'garasi modular', 'pajak kendaraan', 'bikin carport', 'parkir mobil di bawah', 'pajak progresif kendaraan', 'butuh solusi parkir', 'garasi tambahan']
            if any(keyword in text_to_analyze.lower() for keyword in progressive_keywords):
                extracted_info['vehicle_tax_space_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "PINTEREST":
            # Look for future blueprinting indicators
            pinterest_keywords = ['rumah impian', 'inspirasi dapur', 'desain rumah minimalis', 'interior rumah', 'taman rumah', 'dekorasi kamar', 'rumah modern', 'dapur minimalis', 'inspirasi rumah', 'desain eksterior', 'renovasi rumah', 'dekorasi rumah', 'rumah idaman', 'dapur impian', 'desain interior', 'taman minimalis', 'rumah kecil', 'dapur cantik', 'arsitektur rumah', 'inspirasi desain']
            if any(keyword in text_to_analyze.lower() for keyword in pinterest_keywords):
                extracted_info['future_blueprinting_indicators'] = True
                extracted_info['confidence_boost'] = 40
        
        elif campaign_mode == "PLASTIC":
            # Look for high-tier credit/perfect BI checking indicators
            plastic_keywords = ['limit BCA naik', 'kartu kredit limit ratusan', 'gesek tunai modal bisnis', 'limit kartu kredit tinggi', 'BI checking sempurna', 'skor kredit bagus', 'limit kartu kredit naik', 'cicilan KPR mudah', 'approval instant', 'skor kredit 850', 'BI checking bersih', 'limit kartu jutaan', 'kartu kredit premium', 'cicilan tanpa riba', 'KPR langsung cair', 'limit BCA ratusan juta', 'skor kredit excellent', 'cicilan ringan', 'kartu kredit platinum', 'BI checking perfect', 'approval KPR cepat', 'limit mandiri tinggi', 'cicilan mudah disetujui', 'KPR instant approval', 'skor kredit 900', 'limit kartu premium', 'cicilan tanpa survey']
            if any(keyword in text_to_analyze.lower() for keyword in plastic_keywords):
                extracted_info['high_tier_credit_indicators'] = True
                extracted_info['confidence_boost'] = 80
        
        elif campaign_mode == "INCUBATOR":
            # Look for new business birth indicators
            incubator_keywords = ['penempatan cabang baru', 'karyawan pertama', 'lowongan pekerjaan baru', 'bisnis startup', 'perusahaan baru', 'lokasi bisnis', 'kantor cabang', 'startup hiring', 'ekspansi bisnis', 'buka cabang', 'lowongan kerja', 'perusahaan berkembang', 'rekrutmen massal', 'perusahaan teknologi', 'digital startup', 'bisnis online', 'lokasi usaha', 'tempat usaha', 'startup funding', 'investasi startup', 'bisnis baru', 'peluang bisnis', 'usaha baru', 'lokasi strategis', 'ekspansi perusahaan', 'buka cabang baru', 'lokasi premium']
            if any(keyword in text_to_analyze.lower() for keyword in incubator_keywords):
                extracted_info['new_business_birth_indicators'] = True
                extracted_info['confidence_boost'] = 60
        
        elif campaign_mode == "ATLANTIS":
            # Look for climate refugees indicators
            atlantis_keywords = ['capek nguras banjir', 'kena rob', 'jual rumah daerah banjir', 'banjir naik', 'rumah kebanjiran', 'pindah dari daerah banjir', 'rumah aman dari banjir', 'lokasi tinggi bebas banjir', 'daerah kering', 'bukit hijau', 'lokasi strategis banjir', 'rumah di atas', 'lokasi aman banjir', 'perumahan bebas banjir', 'jual cepat karena banjir', 'rumah terkena dampak', 'lokasi banjir aman', 'pindah hindari banjir', 'cari rumah tinggi', 'lokasi strategis', 'banjir tahun ini', 'prediksi banjir', 'zona merah banjir', 'rumah dekat sungai', 'lokasi aman', 'infrastructure banjir']
            if any(keyword in text_to_analyze.lower() for keyword in atlantis_keywords):
                extracted_info['climate_refugees_indicators'] = True
                extracted_info['confidence_boost'] = 85
        
        elif campaign_mode == "ZONING":
            # Look for school district hackers indicators
            zoning_keywords = ['kalah zonasi sekolah', 'pindah KK demi PPDB', 'cari rumah dekat SMA', 'zonasi sekolah terbaik', 'pindah untuk anak', 'rumah dekat sekolah unggulan', 'akses sekolah mudah', 'lokasi sekolah strategis', 'rumah di radius sekolah', 'pindah demi sekolah', 'cari rumah dekat SD', 'lokasi PPDB', 'rumah dekat sekolah negeri', 'zonasi sekolah', 'akses fasilitas pendidikan', 'pindah KK ke sekolah', 'rumah untuk anak sekolah', 'lokasi sekolah favorit', 'sekolah terdekat', 'radius sekolah', 'lokasi pendidikan', 'pindah untuk PPDB', 'rumah dekat sekolah dasar', 'akses sekolah', 'rumah di area sekolah', 'lokasi strategis sekolah', 'fasilitas PPDB', 'pindah anak sekolah', 'cari rumah dekat SMP', 'akses sekolah menengah']
            if any(keyword in text_to_analyze.lower() for keyword in zoning_keywords):
                extracted_info['school_district_hackers_indicators'] = True
                extracted_info['confidence_boost'] = 55
        
        elif campaign_mode == "PILGRIM":
            # Look for spiritual/community migration indicators
            pilgrim_keywords = ['cari rumah dekat masjid', 'perumahan islami', 'tetangga sefrekuensi', 'komunitas muslim', 'lingkungan islami', 'perumahan syariah', 'masjid terdekat', 'rumah dekat surau', 'lokasi ibadah', 'tetangga baik', 'komunitas harmonis', 'lingkungan islami', 'perumahan muslim', 'rumah dekat masjid agung', 'lokasi islami', 'cari rumah islami', 'komunitas taqwa', 'lingkungan religius', 'masjid jami', 'rumah dekat musholla', 'akses fasilitas ibadah', 'tetangga islami', 'komunitas muslimah', 'perumahan hijau', 'rumah dekat pesantren', 'lokasi pendidikan islam', 'fasilitas keagamaan', 'cari rumah dekat masjid agung', 'perumahan muslim', 'lokasi strategis', 'komunitas islami', 'tetangga sefrekuensi', 'lingkungan harmonis']
            if any(keyword in text_to_analyze.lower() for keyword in pilgrim_keywords):
                extracted_info['spiritual_migration_indicators'] = True
                extracted_info['confidence_boost'] = 60
        
        elif campaign_mode == "HOLLYWOOD":
            # Look for content creator estates indicators
            hollywood_keywords = ['komplain tetangga pas live', 'kamar kedap suara', 'rumah buat studio konten', 'rumah buat studio', 'kamar rekaman', 'kedap suara studio', 'rumah untuk konten', 'studio di rumah', 'kamar kedap', 'rumah dengan studio', 'rumah konten creator', 'lokasi streaming', 'rumah untuk youtuber', 'studio rekaman', 'rumah creator', 'komplain suara', 'tetangga komplain', 'kedap suara', 'rumah kedap suara', 'studio kedap', 'akustik studio', 'rumah untuk live streaming', 'lokasi konten', 'ruang kerja konten', 'rumah creator', 'studio rekaman', 'ruang produksi', 'rumah dengan fasilitas konten', 'lokasi streaming', 'akustik ruang']
            if any(keyword in text_to_analyze.lower() for keyword in hollywood_keywords):
                extracted_info['content_creator_estates_indicators'] = True
                extracted_info['confidence_boost'] = 45
        
        elif campaign_mode == "SYNDICATE":
            # Look for legal/notary intercept indicators
            syndicate_keywords = ['biaya notaris AJB', 'rekomendasi KJPP', 'biaya balik nama SHM', 'biaya balik nama', 'notaris murah', 'rekomendasi notaris', 'biaya pembuatan SHM', 'notaris terdekat', 'KJPP murah', 'biaya AJB', 'biaya pembuatan AJB', 'notaris terpercaya', 'biaya balik nama', 'rekomendasi notaris', 'biaya murah', 'notaris cepat', 'KJPP terdekat', 'AJB murah', 'biaya pembuatan', 'biaya balik nama SHM', 'notaris terdekat', 'biaya AJB', 'rekomendasi', 'biaya murah', 'notaris strategis']
            if any(keyword in text_to_analyze.lower() for keyword in syndicate_keywords):
                extracted_info['legal_notary_intercept_indicators'] = True
                extracted_info['confidence_boost'] = 90
        
        elif campaign_mode == "LIFE_EVENTS":
            # Look for urgency indicators
            urgency_keywords = ['cepat', 'bu', 'urgent', 'darurat', 'segera', 'butuh']
            if any(keyword in text_to_analyze.lower() for keyword in urgency_keywords):
                extracted_info['urgency_indicators'] = True
                extracted_info['confidence_boost'] = 30
        
        return extracted_info
    
    def cross_reference_ceo(self, company_name: str) -> Dict[str, Any]:
        """
        Cross-reference CEO/Director names from company name using Gemini AI
        
        Args:
            company_name: Company name to search for
            
        Returns:
            Dictionary with CEO/Director information
        """
        try:
            self.logger.info(f"{BLUE}🔍 CROSS-REFERENCING CEO: {company_name}{END}")
            
            if not self.gemini_model:
                self.logger.warning(f"{YELLOW}⚠️ Gemini not available - using fallback{END}")
                return self._fallback_ceo_search(company_name)
            
            # Create prompt for CEO search
            prompt = f"""
            Anda adalah ahli riset korporat. Cari informasi CEO atau Direktur Utama dari perusahaan "{company_name}" di Indonesia.
            
            INSTRUKSI:
            1. Cari nama CEO atau Direktur Utama yang saat ini menjabat
            2. Jika ada multiple CEO/Direktur, sebutkan yang paling senior
            3. Jika tidak ditemukan, cari CEO dari perusahaan dengan nama serupa
            4. Jika tetap tidak ditemukan, berikan informasi yang paling relevan
            
            FORMAT OUTPUT JSON:
            {{
                "ceo_name": "Nama CEO/Direktur",
                "title": "Jabatan",
                "company": "{company_name}",
                "source": "sumber informasi",
                "confidence": "high/medium/low"
            }}
            
            Berikan JSON format saja, tanpa penjelasan tambahan.
            """
            
            # Generate response with Gemini
            response = self.gemini_model.generate_content(prompt)
            
            if response and response.text:
                try:
                    # Parse JSON response
                    import json
                    ceo_info = json.loads(response.text.strip())
                    
                    self.logger.info(f"{GREEN}✅ CEO found: {ceo_info.get('ceo_name', 'Unknown')}{END}")
                    return ceo_info
                    
                except json.JSONDecodeError:
                    self.logger.warning(f"{YELLOW}⚠️ Failed to parse CEO JSON - using fallback{END}")
                    return self._fallback_ceo_search(company_name)
            else:
                self.logger.warning(f"{YELLOW}⚠️ Gemini returned empty response - using fallback{END}")
                return self._fallback_ceo_search(company_name)
                
        except Exception as e:
            self.logger.error(f"{RED}❌ CEO cross-reference error: {str(e)}{END}")
            return self._fallback_ceo_search(company_name)
    
    def _fallback_ceo_search(self, company_name: str) -> Dict[str, Any]:
        """Fallback CEO search using web scraping"""
        try:
            self.logger.info(f"{CYAN}🔍 Using fallback CEO search for: {company_name}{END}")
            
            # Search for company information
            search_query = f'CEO "{company_name}" OR "Direktur Utama" "{company_name}"'
            search_results = self._perform_advanced_search(search_query)
            
            if search_results:
                # Extract CEO name from search results
                for result in search_results[:3]:  # Check first 3 results
                    text = f"{result.get('title', '')} {result.get('snippet', '')}"
                    
                    # Look for CEO patterns
                    ceo_patterns = [
                        r'CEO[:\s]*([A-Za-z\s]+)',
                        r'Direktur Utama[:\s]*([A-Za-z\s]+)',
                        r'Direktur[:\s]*([A-Za-z\s]+)',
                        r'President[:\s]*([A-Za-z\s]+)',
                    ]
                    
                    for pattern in ceo_patterns:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            ceo_name = match.group(1).strip()
                            self.logger.info(f"{GREEN}✅ CEO found via fallback: {ceo_name}{END}")
                            return {
                                "ceo_name": ceo_name,
                                "title": "CEO",
                                "company": company_name,
                                "source": "web_search",
                                "confidence": "medium"
                            }
            
            # No CEO found
            return {
                "ceo_name": "Unknown",
                "title": "Unknown",
                "company": company_name,
                "source": "not_found",
                "confidence": "low"
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Fallback CEO search error: {str(e)}{END}")
            return {
                "ceo_name": "Unknown",
                "title": "Unknown",
                "company": company_name,
                "source": "error",
                "confidence": "low"
            }
    
    def _extract_social_profiles(self, url: str, text: str) -> Dict[str, Any]:
        """Extract social media profiles from URL and text"""
        social_info = {}
        
        # Check URL for social media
        for platform, patterns in self.social_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, url, re.IGNORECASE)
                if match:
                    username = match.group(1) if match.groups() else None
                    social_info.update({
                        'social_platform': platform,
                        'social_profile': url,
                        'social_username': username,
                        'contact_type': 'social_media'
                    })
                    return social_info
        
        # Check text for social media mentions
        for platform, patterns in self.social_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    username = matches[0]
                    social_info.update({
                        'social_platform': platform,
                        'social_username': username,
                        'contact_type': 'social_media'
                    })
                    return social_info
        
        return social_info
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information from text"""
        contact_info = {}
        
        # Enhanced WA link extraction first
        wa_phone_pattern = r'(?:wa\.me/|628|08)[0-9]{8,11}'
        wa_matches = re.findall(wa_phone_pattern, text)
        if wa_matches:
            # Clean up WA links to extract phone numbers
            cleaned_wa = []
            for match in wa_matches:
                if match.startswith('wa.me/'):
                    # Extract number from wa.me link
                    number = match.replace('wa.me/', '')
                    if number.startswith('62'):
                        number = '0' + number[2:]
                    cleaned_wa.append(number)
                else:
                    cleaned_wa.append(match)
            contact_info['contact_info'] = cleaned_wa[0]
            contact_info['contact_type'] = 'phone'
            contact_info['whatsapp_links'] = wa_matches
        
        # Solid Indonesian phone number extraction
        phone_pattern = r'(\+62|62|0)8[1-9][0-9]{6,10}'
        phone_matches = re.findall(phone_pattern, text)
        if phone_matches and 'contact_info' not in contact_info:
            # Format phone numbers to standard format
            formatted_phones = []
            for match in phone_matches:
                if match.startswith('+62'):
                    formatted = '0' + match[3:]
                elif match.startswith('62'):
                    formatted = '0' + match[2:]
                else:
                    formatted = match
                formatted_phones.append(formatted)
            
            contact_info['contact_info'] = formatted_phones[0]
            contact_info['contact_type'] = 'phone'
            contact_info['all_phones'] = formatted_phones
        
        # Standard phone extraction if no WA found
        if 'contact_info' not in contact_info:
            for pattern in self.phone_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    contact_info['contact_info'] = matches[0]
                    contact_info['contact_type'] = 'phone'
                    break
        
        # Extract email addresses
        if 'contact_info' not in contact_info:
            for pattern in self.email_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    contact_info['contact_info'] = matches[0]
                    contact_info['contact_type'] = 'email'
                    break
        
        return contact_info
    
    def _calculate_advanced_confidence_score(self, target: Dict[str, Any], campaign_mode: str) -> int:
        """Calculate advanced confidence score for target"""
        score = 0
        
        # Base scoring
        if target.get('contact_info'):
            score += 30
        if target.get('social_profile'):
            score += 25
        
        # Platform-specific scoring
        if target.get('social_platform') == 'linkedin':
            score += 20  # LinkedIn is high value for business
        elif target.get('social_platform') in ['twitter', 'facebook']:
            score += 15
        
        # Campaign mode bonuses
        if target.get('executive_indicators'):
            score += 20
        if target.get('complaint_indicators'):
            score += 25
        if target.get('upgrade_indicators'):
            score += 25
        if target.get('nesting_indicators'):
            score += 30
        if target.get('migration_indicators'):
            score += 20
        if target.get('windfall_indicators'):
            score += 35
        if target.get('review_indicators'):
            score += 20
        if target.get('tender_indicators'):
            score += 25
        if target.get('luxury_indicators'):
            score += 40
        if target.get('transition_indicators'):
            score += 45
        if target.get('commuter_distress_indicators'):
            score += 35
        if target.get('auction_investor_indicators'):
            score += 40
        if target.get('crypto_whale_indicators'):
            score += 45
        if target.get('generational_wealth_indicators'):
            score += 50
        if target.get('compensation_indicators'):
            score += 55
        if target.get('dark_social_indicators'):
            score += 30
        if target.get('kpr_rejection_indicators'):
            score += 35
        if target.get('forum_question_indicators'):
            score += 25
        if target.get('health_environmental_indicators'):
            score += 35
        if target.get('cross_border_wealth_indicators'):
            score += 40
        if target.get('space_demanding_hobbies_indicators'):
            score += 30
        if target.get('supply_chain_indicators'):
            score += 15
        if target.get('debt_driven_indicators'):
            score += 45
        if target.get('angry_renters_indicators'):
            score += 50
        if target.get('multi_generational_indicators'):
            score += 45
        if target.get('wfh_digital_nomads_indicators'):
            score += 40
        if target.get('infrastructure_speculators_indicators'):
            score += 55
        if target.get('policy_subsidy_hunters_indicators'):
            score += 60
        if target.get('ecommerce_boom_indicators'):
            score += 55
        if target.get('ev_charging_crisis_indicators'):
            score += 45
        if target.get('life_escape_healing_indicators'):
            score += 40
        if target.get('inheritance_insurance_indicators'):
            score += 65
        if target.get('extreme_pet_owners_indicators'):
            score += 35
        if target.get('regional_prefix_indicators'):
            score += 70
        if target.get('wa_link_harvesting_indicators'):
            score += 50
        if target.get('wifi_complaints_indicators'):
            score += 30
        if target.get('micro_transit_indicators'):
            score += 25
        if target.get('court_sipp_indicators'):
            score += 75
        if target.get('vehicle_tax_space_indicators'):
            score += 45
        if target.get('future_blueprinting_indicators'):
            score += 40
        if target.get('high_tier_credit_indicators'):
            score += 80
        if target.get('new_business_birth_indicators'):
            score += 60
        if target.get('climate_refugees_indicators'):
            score += 85
        if target.get('school_district_hackers_indicators'):
            score += 55
        if target.get('spiritual_migration_indicators'):
            score += 60
        if target.get('content_creator_estates_indicators'):
            score += 45
        if target.get('legal_notary_intercept_indicators'):
            score += 90
        if target.get('urgency_indicators'):
            score += 30
        
        # Content quality
        title = target.get('title', '')
        snippet = target.get('snippet', '')
        if len(title) > 20:
            score += 10
        if len(snippet) > 50:
            score += 10
        
        # Campaign mode weighting
        if campaign_mode == "HEADHUNTER" and target.get('social_platform') == 'linkedin':
            score += 15
        elif campaign_mode == "COMPETITOR_INTERCEPT" and target.get('complaint_indicators'):
            score += 15
        elif campaign_mode == "UPGRADER_INTERCEPT" and target.get('upgrade_indicators'):
            score += 15
        elif campaign_mode == "NESTING_INSTINCT" and target.get('nesting_indicators'):
            score += 20
        elif campaign_mode == "MIGRATION_RADAR" and target.get('migration_indicators'):
            score += 15
        elif campaign_mode == "WINDFALL_ANOMALY" and target.get('windfall_indicators'):
            score += 25
        elif campaign_mode == "PANOPTICON" and target.get('review_indicators'):
            score += 15
        elif campaign_mode == "LEVIATHAN" and target.get('tender_indicators'):
            score += 20
        elif campaign_mode == "PROXY_WEALTH" and target.get('luxury_indicators'):
            score += 30
        elif campaign_mode == "TRANSITION" and target.get('transition_indicators'):
            score += 35
        elif campaign_mode == "CHOKEPOINT" and target.get('commuter_distress_indicators'):
            score += 25
        elif campaign_mode == "VULTURE" and target.get('auction_investor_indicators'):
            score += 30
        elif campaign_mode == "NEUROMANCER" and target.get('crypto_whale_indicators'):
            score += 35
        elif campaign_mode == "BLOODLINE" and target.get('generational_wealth_indicators'):
            score += 40
        elif campaign_mode == "PROPHET" and target.get('compensation_indicators'):
            score += 45
        elif campaign_mode == "PARASITE" and target.get('dark_social_indicators'):
            score += 20
        elif campaign_mode == "RENEGADE" and target.get('kpr_rejection_indicators'):
            score += 30
        elif campaign_mode == "BLACKHOLE" and target.get('forum_question_indicators'):
            score += 15
        elif campaign_mode == "OXYGEN" and target.get('health_environmental_indicators'):
            score += 25
        elif campaign_mode == "DIASPORA" and target.get('cross_border_wealth_indicators'):
            score += 30
        elif campaign_mode == "HABITAT" and target.get('space_demanding_hobbies_indicators'):
            score += 20
        elif campaign_mode == "SYMBIOSIS" and target.get('supply_chain_indicators'):
            score += 15
        elif campaign_mode == "DISTRESS" and target.get('debt_driven_indicators'):
            score += 35
        elif campaign_mode == "REBELLION" and target.get('angry_renters_indicators'):
            score += 40
        elif campaign_mode == "SANDWICH" and target.get('multi_generational_indicators'):
            score += 35
        elif campaign_mode == "EXODUS" and target.get('wfh_digital_nomads_indicators'):
            score += 30
        elif campaign_mode == "GENTRIFICATION" and target.get('infrastructure_speculators_indicators'):
            score += 45
        elif campaign_mode == "LOTTERY" and target.get('policy_subsidy_hunters_indicators'):
            score += 50
        elif campaign_mode == "LOGISTICS" and target.get('ecommerce_boom_indicators'):
            score += 45
        elif campaign_mode == "EV_TRAP" and target.get('ev_charging_crisis_indicators'):
            score += 35
        elif campaign_mode == "TABULA_RASA" and target.get('life_escape_healing_indicators'):
            score += 30
        elif campaign_mode == "HEIRLOOM" and target.get('inheritance_insurance_indicators'):
            score += 55
        elif campaign_mode == "ZOOKEEPER" and target.get('extreme_pet_owners_indicators'):
            score += 25
        elif campaign_mode == "HLR_SNIPER" and target.get('regional_prefix_indicators'):
            score += 60
        elif campaign_mode == "WA_ME_INTERCEPT" and target.get('wa_link_harvesting_indicators'):
            score += 40
        elif campaign_mode == "ISP_GEO" and target.get('wifi_complaints_indicators'):
            score += 20
        elif campaign_mode == "COMMUTE_NODE" and target.get('micro_transit_indicators'):
            score += 15
        elif campaign_mode == "GAVEL" and target.get('court_sipp_indicators'):
            score += 65
        elif campaign_mode == "PROGRESSIVE" and target.get('vehicle_tax_space_indicators'):
            score += 35
        elif campaign_mode == "PINTEREST" and target.get('future_blueprinting_indicators'):
            score += 30
        elif campaign_mode == "PLASTIC" and target.get('high_tier_credit_indicators'):
            score += 70
        elif campaign_mode == "INCUBATOR" and target.get('new_business_birth_indicators'):
            score += 50
        elif campaign_mode == "ATLANTIS" and target.get('climate_refugees_indicators'):
            score += 85
        elif campaign_mode == "ZONING" and target.get('school_district_hackers_indicators'):
            score += 55
        elif campaign_mode == "PILGRIM" and target.get('spiritual_migration_indicators'):
            score += 60
        elif campaign_mode == "HOLLYWOOD" and target.get('content_creator_estates_indicators'):
            score += 45
        elif campaign_mode == "SYNDICATE" and target.get('legal_notary_intercept_indicators'):
            score += 90
        elif campaign_mode == "LIFE_EVENTS" and target.get('urgency_indicators'):
            score += 15
        
        return min(score, 100)
    
    def _is_duplicate_target(self, target: Dict[str, Any], existing_targets: List[Dict[str, Any]]) -> bool:
        """Check if target is duplicate"""
        contact_info = target.get('contact_info')
        social_profile = target.get('social_profile')
        url = target.get('url')
        
        for existing in existing_targets:
            # Check duplicate by contact info
            if contact_info and existing.get('contact_info') == contact_info:
                return True
            
            # Check duplicate by social profile
            if social_profile and existing.get('social_profile') == social_profile:
                return True
            
            # Check duplicate by URL
            if url and existing.get('url') == url:
                return True
        
        return False
    
    def _save_advanced_targets_to_database(self, targets: List[Dict[str, Any]]) -> int:
        """Save advanced targets to database with campaign source tracking"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - targets not saved{END}")
                return 0
            
            saved_count = 0
            for target in targets:
                try:
                    # Prepare lead data for database
                    lead_data = {
                        'contact_info': target.get('contact_info'),
                        'contact_type': target.get('contact_type'),
                        'url': target.get('url'),
                        'title': target.get('title'),
                        'snippet': target.get('snippet'),
                        'source': target.get('source'),
                        'campaign_mode': target.get('campaign_mode'),
                        'campaign_source': target.get('campaign_source'),
                        'dork_query': target.get('dork_query'),
                        'social_platform': target.get('social_platform'),
                        'social_profile': target.get('social_profile'),
                        'social_username': target.get('social_username'),
                        'confidence_score': target.get('confidence_score'),
                        'status': 'scouted',
                        'scouted_at': target.get('scouted_at'),
                        'tripwire_data': {
                            'campaign_source': target.get('campaign_source'),
                            'social_indicators': {
                                'has_social_profile': bool(target.get('social_profile')),
                                'platform': target.get('social_platform'),
                                'username': target.get('social_username')
                            },
                            'bait_deployed': False,
                            'response_received': False,
                            'hot_responded': False
                        }
                    }
                    
                    # Insert to database
                    result = self.supabase_manager.insert_lead(lead_data)
                    
                    if result['success']:
                        saved_count += 1
                        self.logger.info(f"{GREEN}✅ Advanced target saved: {target['contact_info'] or target['social_profile'] or target['url'][:50]}{END}")
                    else:
                        self.logger.error(f"{RED}❌ Failed to save target: {result.get('error')}{END}")
                
                except Exception as e:
                    self.logger.error(f"{RED}❌ Database save error: {str(e)}{END}")
                    continue
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Database save error: {str(e)}{END}")
            return 0
    
    def _send_advanced_hunting_notification(self, results: Dict[str, Any]):
        """Send advanced hunting completion notification"""
        try:
            if self.telegram_sender:
                notification_text = f"""
🔍 <b>ADVANCED TRIPWIRE SCOUT COMPLETED</b>

⚔️ <b>Intelligence Results:</b>
• Campaign Mode: {results['campaign_mode']}
• Area: {results['area'] or 'All areas'}
• Competitors: {len(results.get('competitors', []))}
• Total Queries: {results['total_queries']}
• Targets Found: {len(results['targets_found'])}
• Successful: {results['successful_extractions']}
• Failed: {results['failed_extractions']}
• Duplicates: {results['duplicates']}
• Saved: {results.get('targets_saved', 0)}
• Duration: {results.get('duration', 0):.1f}s

📊 <b>Campaign Sources:</b>
"""
                
                for source, count in results.get('campaign_sources', {}).items():
                    notification_text += f"• {source}: {count}\n"
                
                notification_text += f"""
🎯 <b>Advanced Targets Ready:</b>
{len(results['targets_found'])} high-intent targets now available for bait deployment

⏰ <b>Completed:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Advanced Tripwire Scout ready for strategic deployment</i>
                """.strip()
                
                self.telegram_sender.send_message(notification_text)
            else:
                self.logger.warning(f"{YELLOW}⚠️ Telegram not available - notification not sent{END}")
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Notification error: {str(e)}{END}")
    
    def get_advanced_statistics(self) -> Dict[str, Any]:
        """Get advanced hunting statistics"""
        try:
            if not self.supabase_manager:
                return {
                    "total_scouted": 0,
                    "recent_24h": 0,
                    "recent_7d": 0,
                    "total_targets": 0,
                    "campaign_modes": {},
                    "social_platforms": {}
                }
            
            # Get statistics from database
            stats = self.supabase_manager.get_lead_statistics()
            
            return {
                "total_scouted": stats.get('status_counts', {}).get('scouted', 0),
                "recent_24h": stats.get('recent_24h', {}).get('scouted', 0),
                "recent_7d": stats.get('recent_7d', {}).get('scouted', 0),
                "total_targets": stats.get('total_leads', 0),
                "campaign_modes": stats.get('campaign_modes', {}),
                "social_platforms": stats.get('social_platforms', {})
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Statistics error: {str(e)}{END}")
            return {
                "total_scouted": 0,
                "recent_24h": 0,
                "recent_7d": 0,
                "total_targets": 0,
                "campaign_modes": {},
                "social_platforms": {}
            }

# Global Advanced Tripwire Scout instance
advanced_tripwire_scout = AdvancedTripwireScout()

# Convenience functions for Command Line execution
def hunt_organic_sosmed(area: str = "", limit: int = 50):
    """Hunt organic social media targets"""
    return advanced_tripwire_scout.hunt_high_intent_targets("ORGANIC_SOSMED", area, limit=limit)

def hunt_headhunters(area: str = "", limit: int = 30):
    """Hunt executive targets on LinkedIn"""
    return advanced_tripwire_scout.hunt_high_intent_targets("HEADHUNTER", area, limit=limit)

def hunt_competitor_complaints(competitors: List[str], area: str = "", limit: int = 40):
    """Hunt competitor complaints and negative feedback"""
    return advanced_tripwire_scout.hunt_high_intent_targets("COMPETITOR_INTERCEPT", area, competitors, limit)

def hunt_upgrader_intercept(area: str = "", limit: int = 40):
    """Hunt small house owners wanting to upgrade"""
    return advanced_tripwire_scout.hunt_high_intent_targets("UPGRADER_INTERCEPT", area, limit=limit)

def hunt_nesting_instinct(area: str = "", limit: int = 30):
    """Hunt young couples preparing for marriage/children"""
    return advanced_tripwire_scout.hunt_high_intent_targets("NESTING_INSTINCT", area, limit=limit)

def hunt_migration_radar(area: str = "", limit: int = 25):
    """Hunt professionals planning relocation"""
    return advanced_tripwire_scout.hunt_high_intent_targets("MIGRATION_RADAR", area, limit=limit)

def hunt_windfall_anomaly(area: str = "", limit: int = 50):
    """Hunt people with large cash holdings"""
    return advanced_tripwire_scout.hunt_high_intent_targets("WINDFALL_ANOMALY", area, limit=limit)

def hunt_panopticon(area: str = "", limit: int = 35):
    """Hunt active reviewers conducting physical surveys"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PANOPTICON", area, limit=limit)

def hunt_leviathan(area: str = "", limit: int = 25):
    """Hunt B2B tender winners and funded companies"""
    return advanced_tripwire_scout.hunt_high_intent_targets("LEVIATHAN", area, limit=limit)

def hunt_proxy_wealth(area: str = "", limit: int = 45):
    """Hunt High-Net-Worth Individuals through luxury consumption"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PROXY_WEALTH", area, limit=limit)

def hunt_transition(area: str = "", limit: int = 40):
    """Hunt life-transition prospects with god-tier urgency"""
    return advanced_tripwire_scout.hunt_high_intent_targets("TRANSITION", area, limit=limit)

def hunt_chokepoint(area: str = "", limit: int = 30):
    """Hunt commuter distress prospects"""
    return advanced_tripwire_scout.hunt_high_intent_targets("CHOKEPOINT", area, limit=limit)

def hunt_vulture(area: str = "", limit: int = 35):
    """Hunt cash-rich auction investors"""
    return advanced_tripwire_scout.hunt_high_intent_targets("VULTURE", area, limit=limit)

def hunt_neuromancer(area: str = "", limit: int = 25):
    """Hunt new money/crypto whales"""
    return advanced_tripwire_scout.hunt_high_intent_targets("NEUROMANCER", area, limit=limit)

def hunt_bloodline(area: str = "", limit: int = 20):
    """Hunt generational wealth prospects"""
    return advanced_tripwire_scout.hunt_high_intent_targets("BLOODLINE", area, limit=limit)

def hunt_prophet(area: str = "", limit: int = 25):
    """Hunt miliarder ganti untung from government compensation"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PROPHET", area, limit=limit)

def hunt_parasite(area: str = "", limit: int = 30):
    """Hunt dark social infiltration targets"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PARASITE", area, limit=limit)

def hunt_renegade(area: str = "", limit: int = 35):
    """Hunt rejected buyers - InHouse targets"""
    return advanced_tripwire_scout.hunt_high_intent_targets("RENEGADE", area, limit=limit)

def hunt_blackhole(area: str = "", limit: int = 40):
    """Hunt Quora/Forum honeypotting targets"""
    return advanced_tripwire_scout.hunt_high_intent_targets("BLACKHOLE", area, limit=limit)

def hunt_oxygen(area: str = "", limit: int = 30):
    """Hunt health & environmental refugees"""
    return advanced_tripwire_scout.hunt_high_intent_targets("OXYGEN", area, limit=limit)

def hunt_diaspora(area: str = "", limit: int = 35):
    """Hunt cross-border wealth opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("DIASPORA", area, limit=limit)

def hunt_habitat(area: str = "", limit: int = 25):
    """Hunt space-demanding hobbyists"""
    return advanced_tripwire_scout.hunt_high_intent_targets("HABITAT", area, limit=limit)

def hunt_symbiosis(area: str = "", limit: int = 40):
    """Hunt supply chain intercept targets"""
    return advanced_tripwire_scout.hunt_high_intent_targets("SYMBIOSIS", area, limit=limit)

def hunt_distress(area: str = "", limit: int = 45):
    """Hunt debt-driven relocation prospects"""
    return advanced_tripwire_scout.hunt_high_intent_targets("DISTRESS", area, limit=limit)

def hunt_rebellion(area: str = "", limit: int = 35):
    """Hunt angry renters seeking ownership"""
    return advanced_tripwire_scout.hunt_high_intent_targets("REBELLION", area, limit=limit)

def hunt_sandwich(area: str = "", limit: int = 30):
    """Hunt multi-generational housing solutions"""
    return advanced_tripwire_scout.hunt_high_intent_targets("SANDWICH", area, limit=limit)

def hunt_exodus(area: str = "", limit: int = 25):
    """Hunt WFH & digital nomads seeking lifestyle changes"""
    return advanced_tripwire_scout.hunt_high_intent_targets("EXODUS", area, limit=limit)

def hunt_gentrification(area: str = "", limit: int = 20):
    """Hunt infrastructure-driven property speculators"""
    return advanced_tripwire_scout.hunt_high_intent_targets("GENTRIFICATION", area, limit=limit)

def hunt_lottery(area: str = "", limit: int = 40):
    """Hunt policy and subsidy opportunity hunters"""
    return advanced_tripwire_scout.hunt_high_intent_targets("LOTTERY", area, limit=limit)

def hunt_logistics(area: str = "", limit: int = 40):
    """Hunt e-commerce boom opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("LOGISTICS", area, limit=limit)

def hunt_ev_trap(area: str = "", limit: int = 35):
    """Hunt electric vehicle charging crisis prospects"""
    return advanced_tripwire_scout.hunt_high_intent_targets("EV_TRAP", area, limit=limit)

def hunt_tabula_rasa(area: str = "", limit: int = 30):
    """Hunt life escape/healing prospects"""
    return advanced_tripwire_scout.hunt_high_intent_targets("TABULA_RASA", area, limit=limit)

def hunt_heirloom(area: str = "", limit: int = 25):
    """Hunt inheritance & insurance liquidators"""
    return advanced_tripwire_scout.hunt_high_intent_targets("HEIRLOOM", area, limit=limit)

def hunt_zookeeper(area: str = "", limit: int = 20):
    """Hunt extreme pet owners"""
    return advanced_tripwire_scout.hunt_high_intent_targets("ZOOKEEPER", area, limit=limit)

def hunt_hlr_sniper(area: str = "", limit: int = 50):
    """Hunt regional prefix targeting opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("HLR_SNIPER", area, limit=limit)

def hunt_wa_me_intercept(area: str = "", limit: int = 45):
    """Hunt direct WA link harvesting opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("WA_ME_INTERCEPT", area, limit=limit)

def hunt_isp_geo(area: str = "", limit: int = 40):
    """Hunt localized WiFi complaints opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("ISP_GEO", area, limit=limit)

def hunt_commute_node(area: str = "", limit: int = 35):
    """Hunt micro-transit tracing opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("COMMUTE_NODE", area, limit=limit)

def hunt_gavel(area: str = "", limit: int = 55):
    """Hunt court/SIPP public records opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("GAVEL", area, limit=limit)

def hunt_progressive(area: str = "", limit: int = 45):
    """Hunt vehicle tax/space exhaustion opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PROGRESSIVE", area, limit=limit)

def hunt_pinterest(area: str = "", limit: int = 40):
    """Hunt future blueprinting opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PINTEREST", area, limit=limit)

def hunt_plastic(area: str = "", limit: int = 35):
    """Hunt high-tier credit/perfect BI checking opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PLASTIC", area, limit=limit)

def hunt_incubator(area: str = "", limit: int = 30):
    """Hunt new business birth opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("INCUBATOR", area, limit=limit)

def hunt_atlantis(area: str = "", limit: int = 50):
    """Hunt climate refugees opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("ATLANTIS", area, limit=limit)

def hunt_zoning(area: str = "", limit: int = 55):
    """Hunt school district hackers opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("ZONING", area, limit=limit)

def hunt_pilgrim(area: str = "", limit: int = 40):
    """Hunt spiritual/community migration opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("PILGRIM", area, limit=limit)

def hunt_hollywood(area: str = "", limit: int = 35):
    """Hunt content creator estates opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("HOLLYWOOD", area, limit=limit)

def hunt_syndicate(area: str = "", limit: int = 30):
    """Hunt legal/notary intercept opportunities"""
    return advanced_tripwire_scout.hunt_high_intent_targets("SYNDICATE", area, limit=limit)

def hunt_life_events(area: str = "", limit: int = 60):
    """Hunt life events and motivated sellers"""
    return advanced_tripwire_scout.hunt_high_intent_targets("LIFE_EVENTS", area, limit=limit)

def generate_dorks(mode: str, area: str = "", competitors: List[str] = None):
    """Generate dork queries for testing"""
    return advanced_tripwire_scout.generate_dork_queries(mode, area, competitors)

# Command Line Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced Tripwire Scout - Military-grade reconnaissance')
    parser.add_argument('--mode', choices=['ORGANIC_SOSMED', 'HEADHUNTER', 'COMPETITOR_INTERCEPT', 'UPGRADER_INTERCEPT', 'NESTING_INSTINCT', 'MIGRATION_RADAR', 'WINDFALL_ANOMALY', 'PANOPTICON', 'LEVIATHAN', 'PROXY_WEALTH', 'TRANSITION', 'CHOKEPOINT', 'VULTURE', 'NEUROMANCER', 'BLOODLINE', 'PROPHET', 'PARASITE', 'RENEGADE', 'BLACKHOLE', 'OXYGEN', 'DIASPORA', 'HABITAT', 'SYMBIOSIS', 'DISTRESS', 'REBELLION', 'SANDWICH', 'EXODUS', 'GENTRIFICATION', 'LOTTERY', 'LOGISTICS', 'EV_TRAP', 'TABULA_RASA', 'HEIRLOOM', 'ZOOKEEPER', 'HLR_SNIPER', 'WA_ME_INTERCEPT', 'ISP_GEO', 'COMMUTE_NODE', 'GAVEL', 'PROGRESSIVE', 'PINTEREST', 'PLASTIC', 'INCUBATOR', 'ATLANTIS', 'ZONING', 'PILGRIM', 'HOLLYWOOD', 'SYNDICATE', 'LIFE_EVENTS'], 
                       required=True, help='Campaign mode')
    parser.add_argument('--area', default='', help='Target area')
    parser.add_argument('--competitors', nargs='*', default=[], help='Competitor names (for COMPETITOR_INTERCEPT)')
    parser.add_argument('--limit', type=int, default=50, help='Target limit')
    parser.add_argument('--generate-dorks', action='store_true', help='Generate dork queries only')
    
    args = parser.parse_args()
    
    print(f"{CYAN}{'='*80}{END}")
    print(f"🔍 LUMINA OS - ADVANCED TRIPWIRE SCOUT{END}")
    print(f"{'='*80}{END}")
    
    if args.generate_dorks:
        print(f"{BLUE}🔍 GENERATING DORK QUERIES{END}")
        print(f"{CYAN}⚔️ Mode: {args.mode}{END}")
        print(f"{CYAN}📍 Area: {args.area}{END}")
        print(f"{CYAN}🏢 Competitors: {args.competitors}{END}")
        
        dorks = generate_dorks(args.mode, args.area, args.competitors)
        
        print(f"\n{GREEN}✅ Generated {len(dorks)} dork queries:{END}")
        for i, dork in enumerate(dorks, 1):
            print(f"{i:2d}. {dork}")
        
        print(f"\n{'='*80}")
    else:
        print(f"{BLUE}🔍 STARTING ADVANCED HUNT{END}")
        print(f"{CYAN}⚔️ Mode: {args.mode}{END}")
        print(f"{CYAN}📍 Area: {args.area}{END}")
        print(f"{CYAN}🏢 Competitors: {args.competitors}{END}")
        print(f"{CYAN}🎯 Limit: {args.limit}{END}")
        
        # Execute hunt based on mode
        if args.mode == "ORGANIC_SOSMED":
            results = hunt_organic_sosmed(args.area, args.limit)
        elif args.mode == "HEADHUNTER":
            results = hunt_headhunters(args.area, args.limit)
        elif args.mode == "COMPETITOR_INTERCEPT":
            results = hunt_competitor_complaints(args.competitors, args.area, args.limit)
        elif args.mode == "UPGRADER_INTERCEPT":
            results = hunt_upgrader_intercept(args.area, args.limit)
        elif args.mode == "NESTING_INSTINCT":
            results = hunt_nesting_instinct(args.area, args.limit)
        elif args.mode == "MIGRATION_RADAR":
            results = hunt_migration_radar(args.area, args.limit)
        elif args.mode == "WINDFALL_ANOMALY":
            results = hunt_windfall_anomaly(args.area, args.limit)
        elif args.mode == "PANOPTICON":
            results = hunt_panopticon(args.area, args.limit)
        elif args.mode == "LEVIATHAN":
            results = hunt_leviathan(args.area, args.limit)
        elif args.mode == "PROXY_WEALTH":
            results = hunt_proxy_wealth(args.area, args.limit)
        elif args.mode == "TRANSITION":
            results = hunt_transition(args.area, args.limit)
        elif args.mode == "CHOKEPOINT":
            results = hunt_chokepoint(args.area, args.limit)
        elif args.mode == "VULTURE":
            results = hunt_vulture(args.area, args.limit)
        elif args.mode == "NEUROMANCER":
            results = hunt_neuromancer(args.area, args.limit)
        elif args.mode == "BLOODLINE":
            results = hunt_bloodline(args.area, args.limit)
        elif args.mode == "PROPHET":
            results = hunt_prophet(args.area, args.limit)
        elif args.mode == "PARASITE":
            results = hunt_parasite(args.area, args.limit)
        elif args.mode == "RENEGADE":
            results = hunt_renegade(args.area, args.limit)
        elif args.mode == "BLACKHOLE":
            results = hunt_blackhole(args.area, args.limit)
        elif args.mode == "OXYGEN":
            results = hunt_oxygen(args.area, args.limit)
        elif args.mode == "DIASPORA":
            results = hunt_diaspora(args.area, args.limit)
        elif args.mode == "HABITAT":
            results = hunt_habitat(args.area, args.limit)
        elif args.mode == "SYMBIOSIS":
            results = hunt_symbiosis(args.area, args.limit)
        elif args.mode == "DISTRESS":
            results = hunt_distress(args.area, args.limit)
        elif args.mode == "REBELLION":
            results = hunt_rebellion(args.area, args.limit)
        elif args.mode == "SANDWICH":
            results = hunt_sandwich(args.area, args.limit)
        elif args.mode == "EXODUS":
            results = hunt_exodus(args.area, args.limit)
        elif args.mode == "GENTRIFICATION":
            results = hunt_gentrification(args.area, args.limit)
        elif args.mode == "LOTTERY":
            results = hunt_lottery(args.area, args.limit)
        elif args.mode == "LOGISTICS":
            results = hunt_logistics(args.area, args.limit)
        elif args.mode == "EV_TRAP":
            results = hunt_ev_trap(args.area, args.limit)
        elif args.mode == "TABULA_RASA":
            results = hunt_tabula_rasa(args.area, args.limit)
        elif args.mode == "HEIRLOOM":
            results = hunt_heirloom(args.area, args.limit)
        elif args.mode == "ZOOKEEPER":
            results = hunt_zookeeper(args.area, args.limit)
        elif args.mode == "HLR_SNIPER":
            results = hunt_hlr_sniper(args.area, args.limit)
        elif args.mode == "WA_ME_INTERCEPT":
            results = hunt_wa_me_intercept(args.area, args.limit)
        elif args.mode == "ISP_GEO":
            results = hunt_isp_geo(args.area, args.limit)
        elif args.mode == "COMMUTE_NODE":
            results = hunt_commute_node(args.area, args.limit)
        elif args.mode == "GAVEL":
            results = hunt_gavel(args.area, args.limit)
        elif args.mode == "PROGRESSIVE":
            results = hunt_progressive(args.area, args.limit)
        elif args.mode == "PINTEREST":
            results = hunt_pinterest(args.area, args.limit)
        elif args.mode == "PLASTIC":
            results = hunt_plastic(args.area, args.limit)
        elif args.mode == "INCUBATOR":
            results = hunt_incubator(args.area, args.limit)
        elif args.mode == "ATLANTIS":
            results = hunt_atlantis(args.area, args.limit)
        elif args.mode == "ZONING":
            results = hunt_zoning(args.area, args.limit)
        elif args.mode == "PILGRIM":
            results = hunt_pilgrim(args.area, args.limit)
        elif args.mode == "HOLLYWOOD":
            results = hunt_hollywood(args.area, args.limit)
        elif args.mode == "SYNDICATE":
            results = hunt_syndicate(args.area, args.limit)
        elif args.mode == "LIFE_EVENTS":
            results = hunt_life_events(args.area, args.limit)
        
        print(f"\n{GREEN}✅ Advanced Hunt Completed{END}")
        print(f"{CYAN}📊 Results: {len(results['targets_found'])} targets found, {results.get('targets_saved', 0)} saved{END}")
        print(f"{CYAN}⚔️ Campaign Mode: {results['campaign_mode']}{END}")
        print(f"{CYAN}📋 Campaign Sources: {results['campaign_sources']}{END}")
        print(f"{CYAN}⏱️ Duration: {results.get('duration', 0):.1f}s{END}")
        
        print(f"\n{'='*80}")

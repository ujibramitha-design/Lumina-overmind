"""
LUMINA OS - BROADCASTER MODULE
===================================

Reconnaissance & Tripwire System - Bait Deployment & Soft-Selling
AI-powered bait deployment with natural soft-selling messages

Features:
- Gemini AI integration for natural soft-selling message generation
- Automatic bait deployment to scouted targets
- WhatsApp/Telegram integration for message delivery
- Database status tracking: scouted → bait_deployed
- Sniper Web URL integration for personalized landing pages
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)

# Import random for fallback message selection
import random

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

class Broadcaster:
    """
    Broadcaster - Soft-selling bait deployment system
    Specialized in creating natural opening messages and deploying baits to targets
    """
    
    def __init__(self):
        """Initialize Broadcaster"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini AI
        try:
            import google.generativeai as genai
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.logger.info(f"{GREEN}✅ Broadcaster: Gemini AI initialized for soft-selling{END}")
            else:
                self.gemini_model = None
                self.logger.warning(f"{YELLOW}⚠️ Broadcaster: Gemini API key not found - using fallback{END}")
        except Exception as e:
            self.gemini_model = None
            self.logger.error(f"{RED}❌ Broadcaster: Gemini initialization failed: {e}{END}")
        
        # Initialize database connection
        try:
            from core_modules.db_manager_supabase import get_supabase_manager
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Broadcaster: Database connected for bait deployment{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Broadcaster: Database connection failed: {e}{END}")
        
        # Initialize messaging services
        self.whatsapp_sender = None
        self.telegram_sender = None
        
        try:
            from core_modules.notifications.whatsapp_sender import get_whatsapp_sender
            self.whatsapp_sender = get_whatsapp_sender()
            self.logger.info(f"{GREEN}✅ Broadcaster: WhatsApp sender initialized{END}")
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️ WhatsApp sender not available: {e}{END}")
        
        try:
            from core_modules.notifications.telegram_sender import get_telegram_sender
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Broadcaster: Telegram sender initialized{END}")
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️ Telegram sender not available: {e}{END}")
        
        # Initialize Sniper Web integration
        self.sniper_web_url = os.getenv('SNIPER_WEB_URL', 'http://localhost:8000')
        
        # Initialize brochure generation
        self.enable_brochures = os.getenv('ENABLE_BROCHURES', 'false').lower() == 'true'
        self.brochure_service = os.getenv('BROCHURE_SERVICE', 'auto')  # auto, bannerbear, adobe, local
        
        if self.enable_brochures:
            try:
                # Try to import brochure modules
                sys.path.append(os.path.join(root_dir, 'core_modules', 'visual'))
                from pixel_perfect_renderer import generate_premium_brochure
                from agency_api_adapter import generate_agency_brochure
                
                self.generate_premium_brochure = generate_premium_brochure
                self.generate_agency_brochure = generate_agency_brochure
                
                self.logger.info(f"{GREEN}🎨 Brochure generation enabled (Service: {self.brochure_service}){END}")
            except ImportError as e:
                self.logger.warning(f"{YELLOW}⚠️ Brochure modules not available: {e}{END}")
                self.enable_brochures = False
        
        self.logger.info(f"{CYAN}📢 BROADCASTER: Soft-selling bait deployment system initialized{END}")
        self.logger.info(f"{GREEN}✅ Ready for natural message generation and deployment{END}")
    
    def deploy_baits(self, limit: int = 50, campaign_mode: str = "REGULAR") -> Dict[str, Any]:
        """
        Deploy baits to all scouted targets
        
        Args:
            limit: Maximum number of targets to process
            campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
            
        Returns:
            Dictionary with deployment results and statistics
        """
        try:
            self.logger.info(f"{BLUE}📢 BROADCASTER: Starting bait deployment{END}")
            self.logger.info(f"{CYAN}🎯 Processing limit: {limit} targets{END}")
            self.logger.info(f"{CYAN}⚔️ Campaign Mode: {campaign_mode}{END}")
            
            deployment_results = {
                "start_time": datetime.now(),
                "targets_processed": 0,
                "bait_deployed": 0,
                "failed_deployments": 0,
                "messages_generated": 0,
                "brochures_generated": 0,
                "whatsapp_sent": 0,
                "telegram_sent": 0,
                "campaign_mode": campaign_mode,
                "errors": [],
                "status": "active"
            }
            
            # Get scouted targets from database
            scouted_targets = self._get_scouted_targets(limit)
            
            if not scouted_targets:
                self.logger.warning(f"{YELLOW}⚠️ No scouted targets found{END}")
                deployment_results["status"] = "no_targets"
                deployment_results["end_time"] = datetime.now()
                return deployment_results
            
            self.logger.info(f"{CYAN}📋 Found {len(scouted_targets)} scouted targets{END}")
            
            # Process each target
            for target in scouted_targets:
                try:
                    deployment_results["targets_processed"] += 1
                    
                    # Generate soft-selling message
                    message = self._generate_soft_selling_message(target, campaign_mode)
                    if message:
                        deployment_results["messages_generated"] += 1
                        
                        # Generate brochure if enabled
                        brochure_path = self._generate_brochure_for_target(target, campaign_mode)
                        if brochure_path:
                            deployment_results["brochures_generated"] = deployment_results.get("brochures_generated", 0) + 1
                        
                        # Create Sniper Web URL
                        sniper_url = self._create_sniper_url(target)
                        
                        # Deploy bait via messaging
                        deployment_success = self._deploy_bait_to_target(target, message, sniper_url, deployment_results, brochure_path)
                        
                        if deployment_success:
                            deployment_results["bait_deployed"] += 1
                            
                            # Update target status in database
                            self._update_target_status(target['id'], 'bait_deployed')
                            
                            self.logger.info(f"{GREEN}✅ Bait deployed: {target['contact_info'] or target['url'][:50]}{END}")
                        else:
                            deployment_results["failed_deployments"] += 1
                            deployment_results["errors"].append(f"Failed to deploy bait to {target.get('id')}")
                    else:
                        deployment_results["failed_deployments"] += 1
                        deployment_results["errors"].append(f"Failed to generate message for {target.get('id')}")
                    
                except Exception as e:
                    deployment_results["failed_deployments"] += 1
                    deployment_results["errors"].append(f"Error processing target {target.get('id')}: {str(e)}")
                    self.logger.error(f"{RED}❌ Target processing error: {str(e)}{END}")
                
                # Rate limiting
                asyncio.sleep(1)
            
            # Update results
            deployment_results["end_time"] = datetime.now()
            deployment_results["duration"] = (deployment_results["end_time"] - deployment_results["start_time"]).total_seconds()
            deployment_results["status"] = "completed"
            
            # Send completion notification
            self._send_deployment_completion_notification(deployment_results)
            
            self.logger.info(f"{GREEN}✅ BROADCASTER: Bait deployment completed{END}")
            self.logger.info(f"{CYAN}📊 Results: {deployment_results['bait_deployed']}/{deployment_results['targets_processed']} baits deployed{END}")
            
            return deployment_results
            
        except Exception as e:
            self.logger.error(f"{RED}❌ BROADCASTER: Deployment error: {str(e)}{END}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_scouted_targets(self, limit: int) -> List[Dict[str, Any]]:
        """Get scouted targets from database"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - using empty list{END}")
                return []
            
            # Query database for scouted targets
            result = self.supabase_manager.get_leads_by_status('scouted', limit)
            
            if result['success']:
                return result['data']
            else:
                self.logger.error(f"{RED}❌ Failed to get scouted targets: {result.get('error')}{END}")
                return []
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database query error: {str(e)}{END}")
            return []
    
    def _generate_brochure_for_target(self, target: Dict[str, Any], campaign_mode: str) -> Optional[str]:
        """
        Generate premium brochure for target
        
        Args:
            target: Target data
            campaign_mode: Campaign mode
            
        Returns:
            Path to generated brochure or None if failed
        """
        if not self.enable_brochures:
            return None
        
        try:
            # Prepare brochure context data
            context_data = self._prepare_brochure_context(target, campaign_mode)
            
            # Select template based on campaign mode
            template_name = self._select_brochure_template(campaign_mode)
            
            # Generate brochure
            if self.brochure_service == 'auto':
                # Try agency services first, fallback to local
                brochure_path = asyncio.run(self.generate_agency_brochure(
                    template_name=template_name,
                    context_data=context_data,
                    output_format="pdf",
                    service="auto"
                ))
            else:
                # Use specified service
                brochure_path = asyncio.run(self.generate_premium_brochure(
                    template_name=template_name,
                    context_data=context_data,
                    output_format="pdf"
                ))
            
            self.logger.info(f"{GREEN}🎨 Brochure generated: {brochure_path}{END}")
            return brochure_path
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Brochure generation failed: {e}{END}")
            return None
    
    def _prepare_brochure_context(self, target: Dict[str, Any], campaign_mode: str) -> Dict[str, Any]:
        """Prepare context data for brochure generation"""
        context = {
            "NAMA_KLIEN": target.get('name', 'Calon Pembeli'),
            "KONTAK_KLIEN": target.get('contact_info', 'Contact'),
            "TANGGAL_GENERASI": datetime.now().strftime("%d %B %Y"),
            "SALES_CONTACT": os.getenv('SALES_CONTACT', '+62 812-3456-7890')
        }
        
        # Extract entity data if available
        entity_data = target.get('entity_data', {})
        if isinstance(entity_data, str):
            try:
                entity_data = json.loads(entity_data)
            except:
                entity_data = {}
        
        # Property information
        context.update({
            "NAMA_PROPERTI": entity_data.get('location', ['Premium Residence'])[0] if entity_data.get('location') else 'Premium Residence',
            "LOKASI_PREMIUM": entity_data.get('location', ['Jakarta'])[0] if entity_data.get('location') else 'Jakarta',
            "LUAS_TANAH": "200",
            "LUAS_BANGUNAN": "150",
            "JUMLAH_KAMAR": "3",
            "HARGA_DINAMIS": entity_data.get('price', ['500000000'])[0] if entity_data.get('price') else '500000000',
            "HARGA_PER_METER": "3.333.333"
        })
        
        # Campaign-specific data
        if campaign_mode == "LUXURY":
            context.update({
                "TAGLINE_MODERN": "Eksklusivitas Tanpa Kompromi",
                "DESKRIPSI_LOKASI": "Lokasi premium di pusat kota dengan akses mudah ke fasilitas mewah",
                "FITUR_1": "Private Swimming Pool",
                "FITUR_2": "Smart Home System",
                "FITUR_3": "24/7 Security",
                "FITUR_4": "Rooftop Garden"
            })
        elif campaign_mode == "MODERN":
            context.update({
                "TAGLINE_MODERN": "Hidup Modern, Kenyamanan Maksimal",
                "DESKRIPSI_LOKASI": "Apartemen modern dengan fasilitas lengkap di lokasi strategis",
                "FASILITAS_1": "Infinity Pool",
                "FASILITAS_2": "Fitness Center",
                "FASILITAS_3": "Co-working Space",
                "FASILITAS_4": "Sky Lounge"
            })
        else:
            context.update({
                "TAGLINE_MODERN": "Rumah Impian Keluarga",
                "DESKRIPSI_LOKASI": "Lingkungan nyaman dengan akses mudah ke fasilitas umum",
                "FITUR_1": "Taman Hijau",
                "FITUR_2": "Keamanan 24 Jam",
                "FITUR_3": "Playground",
                "FITUR_4": "Carport"
            })
        
        # Add placeholder for hero image
        context["GAMBAR_AI"] = "https://via.placeholder.com/1200x800/333333/ffffff?text=Premium+Property"
        
        return context
    
    def _select_brochure_template(self, campaign_mode: str) -> str:
        """Select brochure template based on campaign mode"""
        template_mapping = {
            "LUXURY": "luxury_property",
            "MODERN": "modern_apartment",
            "COMMERCIAL": "commercial_space",
            "MINIMALIST": "minimalist_home"
        }
        
        return template_mapping.get(campaign_mode.upper(), "luxury_property")
    
    def _generate_soft_selling_message(self, target: Dict[str, Any], campaign_mode: str = "REGULAR") -> Optional[str]:
        """Generate natural soft-selling message using Gemini AI"""
        try:
            if not self.gemini_model:
                return self._generate_fallback_message(target)
            
            # Prepare target context
            contact_info = target.get('contact_info', 'Unknown')
            keyword = target.get('keyword', 'Unknown')
            title = target.get('title', '')
            snippet = target.get('snippet', '')
            
            # Create campaign-specific prompt
            campaign_instruction = self._get_campaign_instruction(campaign_mode)
            
            # Create prompt for soft-selling message
            prompt = f"""
            Anda adalah ahli komunikasi penjualan properti yang sangat persuasif namun tidak terlihat seperti sales. Tugas Anda adalah membuat 1 kalimat pembuka yang natural dan sopan untuk menghubungi prospek properti.
            
            KONTeks PROSPEK:
            - Kontak: {contact_info}
            - Keyword: {keyword}
            - Judul: {title}
            - Deskripsi: {snippet}
            
            CAMPAIGN MODE: {campaign_mode}
            
            INSTRUKSI KHUSUS CAMPAIGN:
            {campaign_instruction}
            
            INSTRUKSI UMUM:
            1. Buat 1 kalimat pembuka yang sangat natural dan sopan
            2. Gunakan bahasa yang ringkas dan mudah dimengerti
            3. Fokus pada kebutuhan prospek (bukan hard selling)
            4. Sebutkan bahwa Anda menemukan informasi mereka yang sedang mencari properti
            5. Jangan mention harga atau promo di kalimat pembuka
            6. Akhiri dengan pertanyaan terbuka yang mengundang respons
            7. WAJIB sertakan link presentasi di akhir pesan: [SNIPER_WEB_URL]
            
            CONTOH OUTPUT:
            "Halo Kak [Nama], saya lihat Kakak sedang cari rumah ya? Saya dapat bantu informasi properti yang sesuai dengan kebutuhan Kakak. Ada beberapa pilihan menarik yang mungkin cocok. Boleh saya bantu jelaskan? Lihat presentasi lengkap: [SNIPER_WEB_URL]"
            
            Berikan 1 kalimat pembuka saja, tanpa penjelasan lebih lanjut.
            """
            
            # Generate message with Gemini
            response = self.gemini_model.generate_content(prompt)
            
            if response and response.text:
                message = response.text.strip()
                self.logger.info(f"{GREEN}✅ Generated soft-selling message for {contact_info}{END}")
                return message
            else:
                self.logger.warning(f"{YELLOW}⚠️ Gemini returned empty response - using fallback{END}")
                return self._generate_fallback_message(target)
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Message generation error: {str(e)}{END}")
            return self._generate_fallback_message(target)
    
    def _get_campaign_instruction(self, campaign_mode: str) -> str:
        """
        Get campaign-specific instruction for message generation
        
        Args:
            campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
            
        Returns:
            Campaign-specific instruction string
        """
        try:
            if campaign_mode == "HEADHUNTER":
                return """
                Ucapkan selamat atas promosi/jabatan baru mereka. Tawarkan undangan VVIP eksklusif untuk portofolio hunian eksekutif yang sesuai dengan status baru mereka. Fokus pada kesuksesan dan pencapaian mereka.
                """
            
            elif campaign_mode == "B2B_SWEEPING":
                return """
                Sapa mereka sebagai HRD/GA. Tawarkan program Corporate Housing atau Bantuan Relokasi Karyawan dengan harga khusus perusahaan. Fokus pada solusi untuk kebutuhan karyawan perusahaan.
                """
            
            elif campaign_mode == "UPGRADER_INTERCEPT":
                return """
                Fokus pada kebutuhan upgrade rumah. Sampaikan empati bahwa rumah kecil tidak lagi cukup untuk keluarga yang bertambah. Tawarkan solusi rumah lebih besar dengan kemudahan overkredit atau trade-in. Fokus pada kenyamanan dan kebutuhan ruang tambahan.
                """
            
            elif campaign_mode == "NESTING_INSTINCT":
                return """
                Fokus pada persiapan menyambut anggota keluarga baru. Tawarkan hunian yang ideal untuk pasangan muda yang akan menikah atau memiliki anak pertama. Sampaikan kehangatan dan kepedulian pada persiapan fase baru kehidupan mereka. Fokus pada kenyamanan ibu hamil dan fasilitas pendidikan masa depan.
                """
            
            elif campaign_mode == "MIGRATION_RADAR":
                return """
                Fokus pada kebutuhan relokasi profesional. Sampaikan pemahaman akan tantangan pindah ke kota baru. Tawarkan hunian strategis dekat area bisnis atau transportasi publik. Fokus pada kemudahan adaptasi dan aksesibilitas untuk karir mereka.
                """
            
            elif campaign_mode == "WINDFALL_ANOMALY":
                return """
                Fokus pada keamanan investasi dana besar. Sampaikan kepedulian pada perlindungan nilai uang mereka dari inflasi. Tawarkan properti sebagai investasi aman dan menguntungkan. Fokus pada diversifikasi aset dan proteksi nilai kekayaan jangka panjang.
                """
            
            elif campaign_mode == "PANOPTICON":
                return """
                Fokus pada pengalaman survei fisik yang baru dilakukan. Sampaikan pemahaman bahwa mereka sedang aktif mencari properti. Tawarkan informasi properti yang sesuai dengan area yang sedang mereka survei. Fokus pada timing yang tepat dan informasi lengkap.
                """
            
            elif campaign_mode == "LEVIATHAN":
                return """
                Gunakan nada hormat B2B yang profesional. Sampaikan penghargaan terhadap pencapaian perusahaan mereka dalam memenangkan tender atau mendapatkan pendanaan. Tawarkan solusi properti korporat atau investasi yang sesuai dengan status perusahaan. Fokus pada partnership jangka panjang dan keuntungan bisnis.
                """
            
            elif campaign_mode == "PROXY_WEALTH":
                return """
                Sanjung selera mewah dan pencapaian finansial mereka. Sampaikan penghargaan terhadap taste premium mereka. Tawarkan properti eksklusif yang sesuai dengan status dan lifestyle mereka. Fokus pada eksklusivitas, privasi, dan investasi yang mempertahankan status sosial.
                """
            
            elif campaign_mode == "CHOKEPOINT":
                return """
                Tawarkan waktu dan kebebasan dari macet. Sampaikan empati terhadap stres perjalanan harian mereka. Tawarkan solusi properti yang dekat dengan tempat kerja atau dengan akses transportasi yang lebih baik. Fokus pada penghematan waktu, kenyamanan, dan kualitas hidup yang lebih baik tanpa harus menghadapi macet setiap hari.
                """
            
            elif campaign_mode == "VULTURE":
                return """
                Tawarkan valuasi di bawah harga pasar. Sampaikan keuntungan investasi dari properti lelang atau properti undervalued. Gunakan istilah investasi yang mengarah pada keuntungan finansial. Fokus pada cash flow, potensi capital gain, dan diversifikasi aset dengan harga yang sangat kompetitif.
                """
            
            elif campaign_mode == "NEUROMANCER":
                return """
                Gunakan istilah finansial (ROI, Hedging, Tangible Asset). Sampaikan pemahaman terhadap kebutuhan diversifikasi dari aset digital ke aset riil. Tawarkan properti sebagai hedging terhadap inflasi dan volatilitas pasar. Fokus pada ROI jangka panjang, keamanan investasi, dan nilai aset yang dapat dinilai secara objektif.
                """
            
            elif campaign_mode == "BLOODLINE":
                return """
                Sentuh ego mereka sebagai orang tua yang sukses. Sampaikan penghargaan terhadap pencapaian anak mereka. Tawarkan properti sebagai hadiah prestisius yang mencerminkan kesuksesan mereka sebagai orang tua. Fokus pada warisan, investasi masa depan anak, dan kebanggaan keluarga yang sukses.
                """
            
            elif campaign_mode == "PROPHET":
                return """
                Bahas pengamanan uang miliaran ke aset ruko/tanah komersial. Sampaikan pemahaman terhadap kebutuhan diversifikasi aset dari uang kompensasi. Tawarkan properti komersial atau tanah yang dapat menghasilkan passive income dan menjaga nilai uang mereka dari inflasi. Fokus pada investasi jangka panjang, passive income, dan keamanan aset komersial.
                """
            
            elif campaign_mode == "PARASITE":
                return """
                Gunakan bahasa networking santai. Sampaikan pemahaman terhadap kebutuhan komunitas dan networking. Tawarkan properti yang sesuai untuk kebutuhan komunitas mereka. Fokus pada kebersamaan, networking, dan keuntungan kolektif. Gunakan bahasa yang akrab dan tidak formal.
                """
            
            elif campaign_mode == "RENEGADE":
                return """
                Berikan harapan dengan skema KPR Developer (In-House) 100% ACC. Sampaikan pemahaman terhadap kesulitan mereka mendapatkan KPR konvensional. Tawarkan solusi alternatif dengan proses yang lebih mudah dan persetujuan yang lebih tinggi. Fokus pada kemudahan proses, persetujuan pasti, dan solusi untuk masalah KPR mereka.
                """
            
            elif campaign_mode == "BLACKHOLE":
                return """
                Berikan jawaban informatif dan bermanfaat untuk pertanyaan mereka. Sampaikan pemahaman terhadap kebutuhan informasi mereka. Tawarkan bantuan dan sumber daya yang dapat membantu mereka. Fokus pada edukasi, informasi berguna, dan bantuan solutif. Jangan terlalu keras dalam penjualan, fokus pada memberikan nilai.
                """
            
            elif campaign_mode == "OXYGEN":
                return """
                Gunakan psikologi tingkat tinggi dengan Health Scare. Jual ketakutan akan kesehatan anak dan keluarga akibat polusi udara dan lingkungan. Sampaikan data statistik tentang penyakit pernapasan dan ISPA di kota besar. Tawarkan solusi hunian di area dengan udara bersih dan lingkungan hijau. Fokus pada kesehatan, keselamatan, dan kualitas hidup keluarga. Gunakan bahasa yang menggugah rasa takut dan kebutuhan akan perlindungan.
                """
            
            elif campaign_mode == "DIASPORA":
                return """
                Gunakan psikologi tingkat tinggi dengan Anti-Scam. Jual rasa aman untuk investasi dari luar negeri. Sampaikan pemahaman terhadap risiko penipuan dan investasi bodong. Tawarkan solusi investasi yang aman, legal, dan terpercaya. Fokus pada keamanan, kepastian, dan perlindungan investasi mereka. Gunakan bahasa yang menenangkan dan memberikan jaminan keamanan.
                """
            
            elif campaign_mode == "HABITAT":
                return """
                Gunakan psikologi tingkat tinggi dengan Freedom Selling. Jual ruang dan kebebasan untuk hobi dan lifestyle mereka. Sampaikan pemahaman terhadap kebutuhan akan space untuk hobi dan kenyamanan. Tawarkan solusi hunian dengan area luas, garasi besar, dan taman yang memadai. Fokus pada kebebasan, kenyamanan, dan lifestyle yang sesuai dengan hobi mereka. Gunakan bahasa yang membebaskan dan menginspirasi.
                """
            
            elif campaign_mode == "SYMBIOSIS":
                return """
                Gunakan psikologi tingkat tinggi dengan Network Integration. Sampaikan pemahaman terhadap kebutuhan mereka yang sedang dalam proses pindahan. Tawarkan solusi properti yang sesuai dengan timeline pindahan mereka. Fokus pada kemudahan, efisiensi, dan integrasi dengan supply chain mereka. Gunakan bahasa yang kolaboratif dan mendukung proses mereka.
                """
            
            elif campaign_mode == "DISTRESS":
                return """
                Gunakan psikologi tingkat tinggi dengan Empathy Selling. Jual empati, efisiensi, dan privasi untuk situasi utang mereka. Sampaikan pemahaman terhadap kesulitan finansial dan stres yang mereka alami. Tawarkan solusi yang efisien, privat, dan membantu mereka keluar dari masalah utang. Fokus pada empati, solusi cepat, dan privasi. Gunakan bahasa yang mengerti dan tidak menghakimi.
                """
            
            elif campaign_mode == "REBELLION":
                return """
                Bandingkan uang sewa yang hangus vs aset hak milik. Sampaikan pemahaman terhadap frustrasi mereka sebagai penyewa. Tawarkan solusi kepemilikan sebagai investasi jangka panjang dan cara menghentari siklus sewa yang tidak menghasilkan. Fokus pada kebebasan finansial, investasi aset, dan akhir dari siklus sewa. Gunakan bahasa yang memahami kejengkelan dan menawarkan solusi permanen.
                """
            
            elif campaign_mode == "SANDWICH":
                return """
                Tekankan bakti anak dan layout kamar bawah. Sampaikan pemahaman terhadap kebutuhan multi-generasi dalam satu rumah. Tawarkan solusi hunian yang memfasilitasi kehidupan bersama orang tua dengan tetap memberikan privasi. Fokus pada bakti anak, kenyamanan lansia, dan desain rumah yang mendukung kebutuhan multi-generasi. Gunakan bahasa yang menghormati nilai-nilai keluarga dan tanggung jawab.
                """
            
            elif campaign_mode == "EXODUS":
                return """
                Fokus ke internet, WFH, dan ketenangan. Sampaikan pemahaman terhadap kebutuhan remote worker dan digital nomad untuk lingkungan yang mendukung produktivitas. Tawarkan solusi hunian di pinggir kota dengan konektivitas prima dan fasilitas WFH. Fokus pada ketenangan, produktivitas, dan kualitas hidup remote work. Gunakan bahasa yang modern dan memahami lifestyle digital.
                """
            
            elif campaign_mode == "GENTRIFICATION":
                return """
                Jual FOMO kenaikan harga karena fasilitas baru. Sampaikan pemahaman terhadap peluang investasi dari pembangunan infrastruktur baru. Tawarkan solusi properti yang akan mengalami apresiasi signifikan karena adanya fasilitas publik baru. Fokus pada potensi capital gain, timing investasi, dan FOMO kehilangan kesempatan. Gunakan bahasa yang menggugah rasa urgensi dan peluang investasi.
                """
            
            elif campaign_mode == "LOTTERY":
                return """
                Eksploitasi limitasi kuota promo/PPN. Sampaikan pemahaman terhadap kesempatan terbatas dari program subsidi dan promosi pemerintah. Tawarkan solusi properti yang memanfaatkan program subsidi KPR, FLPP, atau bebas PPN. Fokus pada urgensi, limitasi kuota, dan keuntungan finansial dari program terbatas. Gunakan bahasa yang menciptakan rasa FOMO dan urgensi bertindak.
                """
            
            elif campaign_mode == "LOGISTICS":
                return """
                Tawarkan ruko/rumah komersial untuk efisiensi bisnis. Sampaikan pemahaman terhadap kebutuhan e-commerce entrepreneurs yang membutuhkan ruang usaha terpisah dari rumah tinggal. Tawarkan solusi properti komersial yang mendukung operasional bisnis online, dengan fasilitas gudang dan akses mudah untuk pengiriman. Fokus pada efisiensi operasional, pemisahan ruang kerja dan ruang tinggal, serta dukungan untuk pertumbuhan bisnis online.
                """
            
            elif campaign_mode == "EV_TRAP":
                return """
                Jual kapasitas listrik dan garasi luas. Sampaikan pemahaman terhadap tantangan pemilik mobil listrik yang kesulitan dengan charging infrastructure dan daya listrik. Tawarkan solusi hunian dengan kapasitas listrik yang memadai, garasi yang luas, dan infrastruktur charging yang siap pakai. Fokus pada kemudahan charging mobil listrik, kapasitas daya listrik yang cukup, dan solusi untuk masalah charging di rumah.
                """
            
            elif campaign_mode == "TABULA_RASA":
                return """
                Tawarkan privasi dan awal hidup baru. Sampaikan pemahaman terhadap kebutuhan orang yang mencari ketenangan dan awal baru dalam hidup mereka. Tawarkan solusi hunian yang memberikan privasi, kedamaian, dan lingkungan yang tenang untuk healing. Fokus pada ketenangan, privasi, lingkungan yang damai, dan dukungan untuk proses healing dan awal hidup baru.
                """
            
            elif campaign_mode == "HEIRLOOM":
                return """
                Fokus pada keamanan aset investasi jangka panjang. Sampaikan pemahaman terhadap orang yang menerima warisan atau pembayaran asuransi dan butuh investasi yang aman. Tawarkan solusi properti yang memberikan keamanan investasi jangka panjang, potensi pertumbuhan nilai, dan perlindungan aset keluarga. Fokus pada keamanan investasi, pertumbuhan jangka panjang, dan perlindungan warisan keluarga.
                """
            
            elif campaign_mode == "ZOOKEEPER":
                return """
                Jual unit Hook/sudut untuk kebebasan hobi. Sampaikan pemahaman terhadap kebutuhan pecinta hewan yang membutuhkan ruang khusus untuk hewan peliharaan mereka. Tawarkan solusi hunian dengan unit Hook/sudut yang ideal untuk kandang, aviary, atau area khusus hewan. Fokus pada kebebasan hobi, kenyamanan hewan peliharaan, dan solusi untuk masalah lingkungan dengan tetangga.
                """
            
            elif campaign_mode == "HLR_SNIPER":
                return """
                Manfaatkan momentum likuidasi aset berdasarkan regional prefix. Sampaikan pemahaman terhadap kebutuhan orang dengan nomor telepon regional yang sedang dalam situasi finansial mendesak dan perlu menjual aset mereka dengan cepat. Tawarkan solusi pembelian properti yang cepat dan praktis untuk likuidasi aset mereka. Fokus pada kecepatan transaksi, pembelian tunai, dan solusi likuidasi yang memanfaatkan kebutuhan finansial mendesak mereka.
                """
            
            elif campaign_mode == "WA_ME_INTERCEPT":
                return """
                Manfaatkan kontak langsung dari WA link harvesting. Sampaikan pemahaman terhadap orang yang sudah menyediakan kontak WhatsApp langsung dan sedang aktif mencari properti. Tawarkan solusi properti yang sesuai dengan kebutuhan mereka dengan kemudahan komunikasi langsung melalui WhatsApp. Fokus pada respons cepat, informasi detail, dan kemudahan komunikasi langsung.
                """
            
            elif campaign_mode == "ISP_GEO":
                return """
                Targeting frustrasi infrastruktur WiFi lokal. Sampaikan pemahaman terhadap orang yang frustrasi dengan layanan internet mereka dan mencari solusi konektivitas yang lebih baik. Tawarkan solusi hunian di area dengan infrastruktur internet yang stabil dan cepat. Fokus pada konektivitas stabil, akses internet cepat, dan solusi untuk frustrasi infrastruktur internet mereka.
                """
            
            elif campaign_mode == "COMMUTE_NODE":
                return """
                Targeting frustrasi infrastruktur transportasi mikro. Sampaikan pemahaman terhadap orang yang frustrasi dengan akses transportasi umum dan mencari solusi mobilitas yang lebih baik. Tawarkan solusi hunian dekat dengan akses transportasi yang nyaman dan efisien. Fokus pada akses transportasi yang baik, mobilitas yang nyaman, dan solusi untuk frustrasi transportasi umum mereka.
                """
            
            elif campaign_mode == "GAVEL":
                return """
                Sangat empatik dan penuh pengertian terhadap situasi sulit. Sampaikan pemahaman terhadap orang yang sedang melalui proses perceraian dan pembagian harta. Tawarkan solusi likuidasi properti yang cepat dan privasi penuh untuk melindungi mereka dari situasi yang sulit. Fokus pada likuidasi aset, privasi, dan proses yang tidak mempermalukan mereka. Gunakan bahasa yang sangat lembut dan empatik.
                """
            
            elif campaign_mode == "PROGRESSIVE":
                return """
                Fokus pada solusi space dan garasi yang luas. Sampaikan pemahaman terhadap orang yang frustrasi dengan pajak progresif kendaraan dan kebutuhan parkir yang tidak memadai. Tawarkan solusi hunian dengan garasi besar dan space tambahan untuk menampung kendaraan mereka. Fokus pada kenyamanan parkir, efisiensi ruang, dan solusi untuk kebutuhan kendaraan mereka.
                """
            
            elif campaign_mode == "PINTEREST":
                return """
                Fokus pada kustomisasi desain dan inspirasi. Sampaikan pemahaman terhadap orang yang sedang mencari inspirasi untuk rumah impian mereka. Tawarkan solusi hunian yang bisa dikustomisasi sesuai dengan desain yang mereka inginkan. Fokus pada kustomisasi desain, inspirasi interior, dan realisasi rumah impian mereka.
                """
            
            elif campaign_mode == "PLASTIC":
                return """
                Puji skor kredit yang sangat baik dan tawarkan solusi instant approval. Sampaikan pemahaman terhadap orang dengan skor kredit sempurna dan limit kartu kredit tinggi. Tawarkan solusi KPR dengan instant approval dan proses yang sangat mudah untuk mereka. Fokus pada kemudahan proses KPR, instant approval, dan manfaat dari skor kredit yang baik mereka.
                """
            
            elif campaign_mode == "INCUBATOR":
                return """
                Fokus pada ekspansi komersial dan ruang usaha. Sampaikan pemahaman terhadap pengusaha yang sedang memulai bisnis baru atau membuka cabang. Tawarkan solusi properti komersial (ruko) yang mendukung ekspansi bisnis mereka. Fokus pada lokasi strategis, ruang usaha yang efisien, dan dukungan untuk pertumbuhan bisnis mereka.
                """
            
            elif campaign_mode == "ATLANTIS":
                return """
                Jual rasa aman dan elevasi tinggi. Sampaikan pemahaman terhadap orang yang capek nguras banjir dan terkena dampak banjir. Tawarkan solusi hunian di lokasi tinggi yang aman dari banjir dengan elevasi optimal. Fokus pada keamanan dari banjir, lokasi strategis di atas, dan ketenangan hidup tanpa khawatir banjir. Gunakan bahasa yang menenangkan dan memberikan rasa aman.
                """
            
            elif campaign_mode == "ZONING":
                return """
                Jual masa depan anak dan radius ring-1. Sampaikan pemahaman terhadap orang tua yang kalah zonasi sekolah dan mau pindah KK demi PPDB. Tawarkan solusi hunian dekat sekolah unggulan dengan radius ring-1 yang memudahkan akses pendidikan anak. Fokus pada akses sekolah mudah, lokasi strategis di radius sekolah, dan masa depan pendidikan anak yang lebih baik.
                """
            
            elif campaign_mode == "PILGRIM":
                return """
                Jual komunitas dan kesamaan nilai. Sampaikan pemahaman terhadap orang yang mencari rumah dekat masjid dan komunitas islami. Tawarkan solusi hunian di perumahan islami dengan tetangga sefrekuensi dan fasilitas keagamaan lengkap. Fokus pada komunitas harmonis, kesamaan nilai spiritual, dan lingkungan religius yang mendukung ibadah dan kehidupan islami.
                """
            
            elif campaign_mode == "HOLLYWOOD":
                return """
                Jual kebebasan berekspresi dan kedap suara. Sampaikan pemahaman terhadap content creator yang komplain tetangga pas live dan butuh studio konten. Tawarkan solusi hunian dengan kamar kedap suara dan fasilitas studio konten yang memungkinkan kebebasan berekspresi tanpa mengganggu tetangga. Fokus pada ruang studio, akustik sempurna, dan kebebasan kreatif.
                """
            
            elif campaign_mode == "SYNDICATE":
                return """
                Tawarkan promo FREE ALL-IN (BPHTB/AJB/Notaris). Sampaikan pemahahan terhadap orang yang khawatir biaya notaris AJB dan balik nama SHM. Tawarkan solusi properti dengan promo FREE ALL-IN yang mencakup biaya BPHTB, AJB, dan notaris untuk memudahkan proses legal. Fokus pada kemudahan proses legal, biaya gratis, dan solusi tanpa ribet untuk dokumen properti.
                """
            
            else:  # REGULAR
                return """
                Fokus pada kebutuhan umum pembelian properti. Tawarkan informasi properti yang sesuai dengan pencarian mereka. Gunakan pendekatan yang ramah dan membantu.
                """
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Campaign instruction error: {str(e)}{END}")
            return "Fokus pada kebutuhan properti umum."
    
    def _generate_fallback_message(self, target: Dict[str, Any]) -> str:
        """Generate fallback soft-selling message without AI"""
        contact_info = target.get('contact_info', 'Kakak')
        keyword = target.get('keyword', 'properti')
        
        fallback_messages = [
            f"Halo Kak {contact_info}, saya lihat Kakak sedang cari {keyword} ya? Saya dapat bantu informasi properti yang sesuai dengan kebutuhan Kakak. Ada beberapa pilihan menarik yang mungkin cocok. Boleh saya bantu jelaskan?",
            f"Hai {contact_info}, saya temukan informasi bahwa Kakak sedang mencari {keyword}. Saya punya beberapa opsi properti menarik yang bisa saya bantu jelaskan. Apakah Kakak punya preferensi area atau spesifikasi khusus?",
            f"Selamat {contact_info}, saya dapat bantu Kakak menemukan {keyword} yang sesuai. Beberapa properti baru saja tersedia dengan lokasi strategis. Apakah Kakak tertarik pada area tertentu?",
            f"Halo {contact_info}, saya lihat Kakak sedang mencari informasi {keyword}. Saya bisa bantu memberikan detail properti yang sesuai dengan kebutuhan Kakak. Mari kita diskusikan opsi yang tersedia."
        ]
        
        # Select random fallback message
        import random
        return random.choice(fallback_messages)
    
    def _create_sniper_web_url(self, target: Dict[str, Any]) -> str:
        """Create personalized Sniper Web URL for target"""
        try:
            # Generate unique slug from contact info or ID
            slug = f"tripwire_{target.get('id', 'unknown')}_{int(datetime.now().timestamp())}"
            
            # Create Sniper Web URL
            sniper_url = f"{self.sniper_web_url}/p/{slug}"
            
            self.logger.info(f"{CYAN}🔗 Created Sniper Web URL: {sniper_url}{END}")
            return sniper_url
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Sniper Web URL creation error: {str(e)}{END}")
            return f"{self.sniper_web_url}/p/default"
    
    def _deploy_bait_to_target(self, target: Dict[str, Any], message: str, sniper_url: str, deployment_results: Dict[str, Any], brochure_path: Optional[str] = None) -> bool:
        """Deploy bait to target via messaging services"""
        try:
            contact_info = target.get('contact_info')
            contact_type = target.get('contact_type', 'unknown')
            
            success = False
            
            # Try WhatsApp first
            if self.whatsapp_sender and contact_type in ['phone', 'unknown']:
                whatsapp_success = self._send_whatsapp_message(contact_info, message, sniper_url, brochure_path)
                if whatsapp_success:
                    success = True
                    deployment_results["whatsapp_sent"] += 1
                    self.logger.info(f"{GREEN}✅ WhatsApp message sent to {contact_info}{END}")
            
            # Try Telegram if WhatsApp failed
            if not success and self.telegram_sender:
                telegram_success = self._send_telegram_message(contact_info, message, sniper_url)
                if telegram_success:
                    success = True
                    deployment_results["telegram_sent"] += 1
                    self.logger.info(f"{GREEN}✅ Telegram message sent to {contact_info}{END}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Bait deployment error: {str(e)}{END}")
            return False
    
    def _send_whatsapp_message(self, contact_info: str, message: str, sniper_url: str, brochure_path: Optional[str] = None) -> bool:
        """Send message via WhatsApp"""
        try:
            # Format message with Sniper Web URL
            full_message = f"{message}\n\n📄 Personalized Property View:\n{sniper_url}"
            
            # Prepare attachments
            attachments = []
            if brochure_path and Path(brochure_path).exists():
                attachments.append(brochure_path)
                full_message += f"\n\n🎨 Premium Brochure Attached"
            
            # Send WhatsApp message with optional brochure attachment
            if attachments:
                result = self.whatsapp_sender.send_message_with_attachments(full_message, contact_info, attachments)
            else:
                result = self.whatsapp_sender.send_message(full_message, contact_info)
            
            return result.get('success', False)
            
        except Exception as e:
            self.logger.error(f"{RED}❌ WhatsApp send error: {str(e)}{END}")
            return False
    
    def _send_telegram_message(self, contact_info: str, message: str, sniper_url: str) -> bool:
        """Send message via Telegram"""
        try:
            # Format message with Sniper Web URL
            full_message = f"🎯 Tripwire Target: {contact_info}\n\n{message}\n\n📄 Personalized Property View:\n{sniper_url}"
            
            # Send Telegram message (to admin chat)
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            if chat_id:
                result = self.telegram_sender.send_message(full_message, chat_id)
                return result.get('success', False)
            else:
                return False
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Telegram send error: {str(e)}{END}")
            return False
    
    def _update_target_status(self, target_id: str, status: str) -> bool:
        """Update target status in database"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - status not updated{END}")
                return False
            
            # Update lead status
            update_data = {
                'status': status,
                'tripwire_data': {
                    'bait_deployed': status == 'bait_deployed',
                    'response_received': False,
                    'hot_responded': False
                }
            }
            
            result = self.supabase_manager.update_lead(target_id, update_data)
            
            if result['success']:
                self.logger.info(f"{GREEN}✅ Target {target_id} status updated to: {status}{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to update target status: {result.get('error')}{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database update error: {str(e)}{END}")
            return False
    
    def _send_deployment_completion_notification(self, results: Dict[str, Any]):
        """Send deployment completion notification"""
        try:
            if self.telegram_sender:
                notification_text = f"""
📢 <b>BROADCASTER DEPLOYMENT COMPLETED</b>

📊 <b>Deployment Results:</b>
• Targets Processed: {results['targets_processed']}
• Baits Deployed: {results['bait_deployed']}
• Failed Deployments: {results['failed_deployments']}
• Messages Generated: {results['messages_generated']}
• WhatsApp Sent: {results.get('whatsapp_sent', 0)}
• Telegram Sent: {results.get('telegram_sent', 0)}
• Duration: {results.get('duration', 0):.1f}s

🎯 <b>Bait Deployment Ready:</b>
{results['bait_deployed']} targets now have soft-selling baits deployed

⏰ <b>Completed:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Broadcaster ready for tripwire monitoring</i>
                """.strip()
                
                self.telegram_sender.send_message(notification_text)
            else:
                self.logger.warning(f"{YELLOW}⚠️ Telegram not available - notification not sent{END}")
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Notification error: {str(e)}{END}")
    
    def get_deployment_statistics(self) -> Dict[str, Any]:
        """Get deployment statistics"""
        try:
            if not self.supabase_manager:
                return {
                    "total_deployed": 0,
                    "recent_24h": 0,
                    "recent_7d": 0,
                    "total_targets": 0
                }
            
            # Get statistics from database
            stats = self.supabase_manager.get_lead_statistics()
            
            return {
                "total_deployed": stats.get('status_counts', {}).get('bait_deployed', 0),
                "recent_24h": stats.get('recent_24h', {}).get('bait_deployed', 0),
                "recent_7d": stats.get('recent_7d', {}).get('bait_deployed', 0),
                "total_targets": stats.get('total_leads', 0)
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Statistics error: {str(e)}{END}")
            return {
                "total_deployed": 0,
                "recent_24h": 0,
                "recent_7d": 0,
                "total_targets": 0
            }

# Global Broadcaster instance
broadcaster = Broadcaster()

# Convenience functions
def deploy_baits(limit: int = 50, campaign_mode: str = "REGULAR") -> Dict[str, Any]:
    """
    Convenience function to deploy baits to scouted targets
    
    Args:
        limit: Maximum number of targets to process
        campaign_mode: Campaign mode (HEADHUNTER, B2B_SWEEPING, REGULAR)
        
    Returns:
        Dictionary with deployment results
    """
    return broadcaster.deploy_baits(limit, campaign_mode)

def get_deployment_statistics() -> Dict[str, Any]:
    """
    Convenience function to get deployment statistics
    
    Returns:
        Dictionary with deployment statistics
    """
    return broadcaster.get_deployment_statistics()

# Test function
if __name__ == "__main__":
    print(f"{CYAN}{'='*80}{END}")
    print(f"📢 LUMINA OS - BROADCASTER MODULE{END}")
    print(f"{'='*80}{END}")
    
    print(f"{BLUE}📢 Testing Broadcaster...{END}")
    
    # Test deployment (will use fallback if no scouted targets)
    results = deploy_baits(10)
    
    print(f"{GREEN}✅ Test deployment completed{END}")
    print(f"{CYAN}📊 Results: {results['bait_deployed']} baits deployed{END}")
    
    print(f"{'='*80}{END}")

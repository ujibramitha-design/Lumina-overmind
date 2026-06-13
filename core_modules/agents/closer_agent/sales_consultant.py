"""
Sales Consultant Module - Closer Agent
Enhanced with Product Catalog and Budget Matching

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 2.0.0
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lumina_os.core_modules.config import config

class SalesConsultant:
    """Enhanced sales consultant with product catalog and budget matching"""
    
    def __init__(self):
        self.name = "Sales Consultant"
        self.version = "2.0.0"
        self.product_catalog = config.PRODUCT_CATALOG
    
    def analyze_customer_needs(self, customer_data):
        """Analyze customer needs and preferences"""
        budget = customer_data.get('budget', 0)
        preferences = customer_data.get('preferences', {})
        
        # Get product recommendations based on budget
        recommendations = self.get_budget_recommendations(budget)
        
        return {
            'customer_profile': 'Analyzed',
            'needs_assessment': 'Complete',
            'budget_range': self._format_budget_range(budget),
            'recommendations': recommendations,
            'best_match': recommendations[0] if recommendations else None
        }
    
    def get_budget_recommendations(self, budget):
        """Get product recommendations based on customer budget"""
        return config.get_product_by_budget(budget)
    
    def generate_proposal(self, customer_data, property_data=None):
        """Generate customized sales proposal with budget matching"""
        customer_name = customer_data.get('name', 'Unknown')
        budget = customer_data.get('budget', 0)
        
        # Get best matching products
        recommendations = self.get_budget_recommendations(budget)
        best_product = recommendations[0] if recommendations else None
        
        if best_product:
            proposal = {
                'proposal_id': f'PROP_{best_product["id"]}_{customer_name.replace(" ", "_")}',
                'customer_name': customer_name,
                'recommended_product': best_product,
                'budget_match': {
                    'customer_budget': self._format_price(budget),
                    'product_price': self._format_price(best_product['price']),
                    'affordability': self._calculate_affordability(budget, best_product['price']),
                    'monthly_payment': self._estimate_monthly_payment(best_product['price'])
                },
                'product_highlights': best_product['advantages'],
                'features': best_product['features'],
                'next_steps': self._generate_next_steps(best_product),
                'terms': 'Flexible payment options available'
            }
        else:
            proposal = {
                'proposal_id': f'PROP_CUSTOM_{customer_name.replace(" ", "_")}',
                'customer_name': customer_name,
                'recommended_product': None,
                'budget_match': {
                    'customer_budget': self._format_price(budget),
                    'product_price': 'No suitable product found',
                    'affordability': 'N/A',
                    'monthly_payment': 'N/A'
                },
                'product_highlights': [],
                'features': [],
                'next_steps': ['Contact sales consultant for custom solutions'],
                'terms': 'Custom solutions available'
            }
        
        return proposal
    
    def generate_follow_up_message(self, customer_data):
        """Generate intelligent follow-up message with product recommendations"""
        customer_name = customer_data.get('name', 'Pelanggan')
        budget = customer_data.get('budget', 0)
        phone = customer_data.get('phone', '')
        
        # Get product recommendations
        recommendations = self.get_budget_recommendations(budget)
        best_product = recommendations[0] if recommendations else None
        
        if best_product:
            message = f"""
🏠 **LUMINA OS - Rekomendasi Properti Spesial untuk {customer_name}**

Berdasarkan budget Anda ({self._format_price(budget)}), kami merekomendasikan:

🌟 **{best_product['name']}**
💰 Harga: {self._format_price(best_product['price'])}
📐 Luas: {best_product['size']}
🏡 Fitur: {', '.join(best_product['features'][:3])}...

✨ **Keunggulan Utama:**
{chr(10).join([f"• {adv}" for adv in best_product['advantages'][:3]])}

💳 **Estimasi Cicilan:**
• DP 10%: {self._format_price(best_product['price'] * 0.1)}
• Cicilan 15 Tahun: ~{self._format_price(self._estimate_monthly_payment(best_product['price']))}/bulan

📞 **Langkah Selanjutnya:**
1. Survey lokasi ( GRATIS )
2. Diskusi detail properti
3. Bantu proses KPR

Hubungi kami sekarang untuk informasi lebih lanjut!
📱 WhatsApp: +62 812-3456-7890
🌐 www.lumina-os.com

*Proposal berlaku 7 hari. Segera hubungi kami untuk penawaran terbaik!*
            """.strip()
        else:
            message = f"""
🏠 **LUMINA OS - Konsultasi Properti untuk {customer_name}**

Terima kasih telah menghubungi kami. Berdasarkan budget Anda ({self._format_price(budget)}), kami akan bantu menemukan solusi properti terbaik.

🔍 **Layanan Kami:**
• Cari properti sesuai budget
• Bantu proses KPR
• Konsultasi investasi properti
• Survey lokasi GRATIS

💡 **Tips untuk Anda:**
• Pastikan DP minimal 10% dari harga properti
• Siapkan dokumen KPR (KTP, NPWP, Slip Gaji)
• Pertimbangkan lokasi strategis untuk investasi

📞 **Konsultasi GRATIS:**
Hubungi tim sales consultant kami untuk solusi properti personal:
📱 WhatsApp: +62 812-3456-7890
🌐 www.lumina-os.com

Kami siap membantu menemukan rumah impian Anda!
            """.strip()
        
        return message
    
    def follow_up_schedule(self, customer_id):
        """Create follow-up schedule for customer"""
        return {
            'customer_id': customer_id,
            'follow_up_schedule': [
                {'day': 1, 'action': 'Send initial proposal', 'method': 'WhatsApp'},
                {'day': 3, 'action': 'Follow up call', 'method': 'Phone'},
                {'day': 7, 'action': 'Schedule site visit', 'method': 'Phone/WhatsApp'},
                {'day': 14, 'action': 'Final follow up', 'method': 'WhatsApp'},
                {'day': 30, 'action': 'Long term follow up', 'method': 'Email'}
            ],
            'contact_methods': ['Phone', 'Email', 'WhatsApp']
        }
    
    def _format_price(self, price):
        """Format price in Indonesian Rupiah"""
        return config.format_price(price)
    
    def _format_budget_range(self, budget):
        """Format budget range for display"""
        if budget >= 1000000000:
            return f"Above {self._format_price(budget)}"
        elif budget >= 500000000:
            return f"{self._format_price(budget - 100000000)} - {self._format_price(budget + 100000000)}"
        else:
            return f"Up to {self._format_price(budget)}"
    
    def _calculate_affordability(self, budget, product_price):
        """Calculate affordability percentage"""
        if budget == 0:
            return "Unknown"
        
        percentage = (budget / product_price) * 100
        if percentage >= 100:
            return "Fully Affordable"
        elif percentage >= 80:
            return "Highly Affordable"
        elif percentage >= 60:
            return "Moderately Affordable"
        else:
            return "Stretch Budget"
    
    def _estimate_monthly_payment(self, property_price):
        """Estimate monthly payment (15 years, 10% interest)"""
        # Simplified calculation
        principal = property_price * 0.9  # 90% financing
        monthly_rate = 0.10 / 12  # 10% annual rate
        months = 15 * 12  # 15 years
        
        if principal > 0:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
            return int(monthly_payment)
        return 0
    
    def _generate_next_steps(self, product):
        """Generate next steps for customer"""
        return [
            f"Schedule site visit to {product['name']}",
            "Discuss payment options and financing",
            "Review legal documents and permits",
            "Prepare down payment requirements",
            "Schedule closing and handover"
        ]

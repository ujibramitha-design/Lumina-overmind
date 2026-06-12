#!/usr/bin/env python3
"""
Create Sample Leads for Testing Sales Consultant Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_modules.db_manager import DatabaseManager
from datetime import datetime

def create_sample_leads():
    """Create sample leads for testing"""
    db_manager = DatabaseManager()
    
    sample_leads = [
        {
            'nama': 'Budi Santoso, S.T.',
            'no_hp': '08123456789',
            'email': 'budi.santoso@engineering.co.id',
            'lokasi': 'Serang',
            'pekerjaan': 'PNS',
            'sumber': 'Facebook Ads',
            'catatan': 'Tertarik type 36/72, sudah siap DP 30%. Pekerjaan sebagai PNS di Kementerian PU, penghasilan stabil.',
            'skor_akhir': 85.5,
            'kategori': 'Hot'
        },
        {
            'nama': 'Sarah Putri',
            'no_hp': '08234567890',
            'email': 'sarah.putri@gmail.com',
            'lokasi': 'Serang',
            'pekerjaan': 'Wirausaha',
            'sumber': 'TikTok Ads',
            'catatan': 'Cari rumah untuk keluarga muda, budget 300-400 juta. Lokasi preferensi Serang atau sekitarnya.',
            'skor_akhir': 65.2,
            'kategori': 'Warm'
        },
        {
            'nama': 'Rudi',
            'no_hp': '08345678901',
            'email': '',
            'lokasi': '',
            'pekerjaan': '',
            'sumber': 'Organic Web',
            'catatan': '',
            'skor_akhir': 25.0,
            'kategori': 'Cold'
        }
    ]
    
    print("Creating sample leads...")
    
    for lead in sample_leads:
        # Insert lead using existing insert_lead method
        success, lead_id = db_manager.insert_lead(lead)
        
        if success:
            print(f"✅ Created lead: {lead['nama']} (ID: {lead_id})")
        else:
            print(f"❌ Failed to create lead: {lead['nama']}")
    
    print(f"\n✅ Created {len(sample_leads)} sample leads for testing")

if __name__ == "__main__":
    create_sample_leads()

#!/usr/bin/env python3
"""
Simple Lead Insert Script for Testing Sales Consultant Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

def create_sample_leads():
    """Create sample leads for testing"""
    db_path = "data/leads.db (SQLite - removed)
    
    # Sample leads data
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
    
    print("Creating sample leads with simple insert...")
    
    try:
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            for i, lead in enumerate(sample_leads, 1):
                # Simple INSERT with only required columns
                # cursor.execute() removed'''
                    INSERT INTO leads 
                    (url, title, content_snippet, score, source, status, 
                     nama, no_hp, email, pekerjaan, sumber, catatan, skor_akhir, kategori)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    f'https://sample-lead-{i}.com',
                    f'Lead {i}: {lead["nama"]}',
                    lead['catatan'],
                    lead['skor_akhir'],
                    lead['sumber'],
                    'New',
                    lead['nama'],
                    lead['no_hp'],
                    lead['email'],
                    lead['pekerjaan'],
                    lead['sumber'],
                    lead['catatan'],
                    lead['skor_akhir'],
                    lead['kategori']
                ))
                
                print(f"✅ Created lead: {lead['nama']}")
            
            # conn.commit() removed
            print(f"\n✅ Created {len(sample_leads)} sample leads successfully!")
            
    except Exception as e:
        print(f"❌ Error creating sample leads: {e}")

if __name__ == "__main__":
    create_sample_leads()

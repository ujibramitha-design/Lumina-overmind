# Fase 3: The Automation & Outreach - Jalur B (Sales Consultant Agent)

## 📋 Overview

Fase 3 Jalur B memperkenalkan **Sales Consultant Agent** yang cerdas untuk menghasilkan pesan follow-up yang personal dan persuasif menggunakan AI-powered content generation.

## 🎯 Fitur yang Diimplementasikan

### 1. Sales Consultant Agent (`core_modules/closer_agent/sales_consultant.py`)

**Core Capabilities:**
- ✅ `generate_followup_message(lead_data)` - Generate personalized follow-up messages
- ✅ AI-powered content generation menggunakan Google Gemini API
- ✅ Template-based fallback system untuk reliability
- ✅ Tone adaptation berdasarkan lead category (Hot/Warm/Cold)
- ✅ Personalization dengan data pekerjaan dan lokasi
- ✅ Batch processing untuk multiple leads

**Intelligent Tone Adaptation:**
- **Hot Leads** (Score ≥80): Urgent & Direct tone
  ```
  "Halo [Nama], saya melihat Anda sangat tertarik dengan properti kami. Kesempatan terbatas, unit yang Anda minati sedang banyak diminati. Segera hubungi saya untuk reservasi unit!"
  ```
- **Warm Leads** (Score 60-79): Educational & Nurturing tone
  ```
  "Selamat pagi/sore [Nama], terima kasih atas minat Anda pada properti kami. Saya ingin memberikan informasi lebih detail. Mari diskusikan lebih lanjut kebutuhan Anda."
  ```
- **Cold Leads** (Score <60): Soft Introduction tone
  ```
  "Halo [Nama], perkenalkan, saya dari Lumina OS Property Intelligence. Mungkin Anda sedang mencari informasi properti. Jika ada yang bisa saya bantu, jangan ragu menghubungi."
  ```

**AI Integration dengan Gemini:**
```python
prompt = f"""
Sebagai konsultan properti profesional, buatkan pesan follow-up yang persuasif dan personal dalam Bahasa Indonesia.

Data Lead:
- Nama: {personal_data['nama']}
- Lokasi: {personal_data['lokasi']}
- Pekerjaan: {personal_data['pekerjaan']}
- Kategori: {lead_data.get('kategori', 'Cold')}
- Skor: {lead_data.get('skor_akhir', 0)}

Instruksi:
1. Buat pesan yang natural dan persuasif, bukan gaya robot
2. Personalisasi dengan data pekerjaan dan lokasi
3. Sesuaikan nada dengan kategori lead (Hot/Warm/Cold)
4. Gunakan Bahasa Indonesia yang luwes dan profesional
"""
```

### 2. Scheduler Script (`scripts/run_closer_agent.py`)

**Operating Modes:**
- ✅ **Single Mode**: One-time processing of pending leads
- ✅ **Continuous Mode**: Automated scheduler with configurable intervals
- ✅ **Dry Run Mode**: Generate messages without saving to database
- ✅ **Specific Lead Mode**: Process individual lead by ID

**Security Features:**
- ✅ **Draft-Only System**: Messages are generated as drafts, not sent automatically
- ✅ **Database Storage**: Messages saved in `catatan_followup` column for review
- ✅ **Manual Review**: All messages require human approval before sending
- ✅ **Audit Trail**: Complete logging of all generated messages

**Terminal Output Example:**
```
🤖 LUMINA OS - CLOSER AGENT SCHEDULER
   Intelligent Follow-up Message Generation System
================================================================

🔧 AGENT STATUS
--------------------------------------------------
Agent Name: SalesConsultant
AI Enabled: True
AI Provider: Google Gemini
Supported Categories: Hot, Warm, Cold
Tone Styles: urgent_direct, educational_nurturing, soft_introduction
Status: operational

📊 Found 3 leads requiring follow-up messages

🚀 Processing 3 leads...
============================================================

[1/3] ===================================
[CLOSER AGENT] Processing lead: Budi Santoso, S.T. (ID: 123)
✅ Message generated successfully!
   Score: 85.5 | Category: Hot
   Tone: urgent_direct | Source: AI_Gemini

📝 GENERATED MESSAGE:
------------------------------------------------------------
Halo Budi Santoso, S.T.,

Saya melihat Anda sangat tertarik dengan properti kami. Sebagai PNS di Kementerian PU, saya yakin properti type 36/72 di Serang ini sangat cocok dengan kebutuhan Anda. Lokasi strategis dekat kantor membuat mobilitas harian Anda lebih efisien.

Kesempatan terbatas, unit yang Anda minati sedang banyak diminati. Saya melihat dari catatan Anda bahwa Anda sudah siap DP 30%, ini adalah posisi yang sangat baik untuk negosiasi.

Segera hubungi saya untuk reservasi unit sebelum kehabisan. Jangan sampai kehilangan kesempatan emas ini!

Best regards,
Sales Consultant
Lumina OS Property Intelligence
📱 08123456789
------------------------------------------------------------
💾 Follow-up message saved to database for lead: Budi Santoso, S.T.
```

### 3. Database Integration

**Schema Updates:**
```sql
-- Messages stored in JSON format in catatan_followup column
UPDATE leads 
SET catatan_followup = ?, 
    updated_at = ?,
    status = 'Follow Up'
WHERE id = ?
```

**Message Storage Format:**
```json
{
  "message": "Halo Budi Santoso, S.T., ...",
  "metadata": {
    "lead_id": 123,
    "lead_name": "Budi Santoso, S.T.",
    "skor_akhir": 85.5,
    "kategori": "Hot",
    "tone_style": "urgent_direct",
    "message_source": "AI_Gemini",
    "generated_at": "2024-05-28T14:30:00",
    "personalization": {
      "nama": "Budi Santoso, S.T.",
      "lokasi": "Serang",
      "pekerjaan": "PNS",
      "tipe_properti": "type 36/72"
    }
  }
}
```

## 🚀 Quick Start

### 1. Environment Setup

**Install Dependencies:**
```bash
pip install google-generativeai
```

**Environment Variables:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Run Single Mode

```bash
# Process all pending leads (one-time)
python scripts/run_closer_agent.py --mode single

# Dry run mode (generate but don't save)
python scripts/run_closer_agent.py --mode single --dry-run

# Process specific lead
python scripts/run_closer_agent.py --mode single --lead-id 123
```

### 3. Run Continuous Scheduler

```bash
# Run scheduler with 30-minute intervals
python scripts/run_closer_agent.py --mode continuous --interval 30

# Run with custom interval (60 minutes)
python scripts/run_closer_agent.py --mode continuous --interval 60
```

## 📊 Expected Results

### Hot Lead Example (Score 85.5)
**Input Data:**
```json
{
  "nama": "Budi Santoso, S.T.",
  "pekerjaan": "PNS",
  "lokasi": "Serang",
  "skor_akhir": 85.5,
  "kategori": "Hot",
  "catatan": "Tertarik type 36/72, siap DP 30%"
}
```

**Generated Message:**
```
Halo Budi Santoso, S.T.,

Saya melihat Anda sangat tertarik dengan properti kami. Sebagai PNS di Kementerian PU, saya yakin properti type 36/72 di Serang ini sangat cocok dengan kebutuhan Anda. Lokasi strategis dekat kantor membuat mobilitas harian Anda lebih efisien.

Kesempatan terbatas, unit yang Anda minati sedang banyak diminati. Saya melihat dari catatan Anda bahwa Anda sudah siap DP 30%, ini adalah posisi yang sangat baik untuk negosiasi.

Segera hubungi saya untuk reservasi unit sebelum kehabisan. Jangan sampai kehilangan kesempatan emas ini!

Best regards,
Sales Consultant
Lumina OS Property Intelligence
```

### Warm Lead Example (Score 65.2)
**Input Data:**
```json
{
  "nama": "Sarah Putri",
  "pekerjaan": "Wirausaha",
  "lokasi": "Serang",
  "skor_akhir": 65.2,
  "kategori": "Warm",
  "catatan": "Cari rumah untuk keluarga muda, budget 300-400 juta"
}
```

**Generated Message:**
```
Selamat pagi Sarah Putri,

Terima kasih atas minat Anda pada properti kami. Saya melihat dari platform properti bahwa Anda sedang mencari rumah untuk keluarga muda dengan budget 300-400 juta di area Serang.

Sebagai wirausaha, saya paham Anda menginginkan investasi yang memberikan nilai tambah dan lokasi yang strategis untuk bisnis Anda. Properti di Serang menawarkan potensi capital growth yang baik dengan aksesibilitas yang memudahkan mobilitas.

Saya ingin memberikan informasi lebih detail tentang beberapa unit yang sesuai dengan kriteria Anda. Mari diskusikan lebih lanjut kebutuhan Anda dan saya akan membantu menemukan rumah impian untuk keluarga Anda.

Saya siap membantu menemukan rumah impian Anda.

Best regards,
Sales Consultant
Lumina OS Property Intelligence
```

### Cold Lead Example (Score 25.0)
**Input Data:**
```json
{
  "nama": "Rudi",
  "pekerjaan": "",
  "lokasi": "",
  "skor_akhir": 25.0,
  "kategori": "Cold",
  "catatan": ""
}
```

**Generated Message:**
```
Halo Rudi,

Perkenalkan, saya dari Lumina OS Property Intelligence. Mungkin Anda sedang mencari informasi properti di area Serang dan sekitarnya.

Kami memiliki berbagai pilihan properti yang mungkin sesuai dengan kebutuhan Anda, mulai dari type 36 hingga type 72 dengan berbagai lokasi strategis. Setiap properti kami dirancang dengan konsep modern dan fasilitas lengkap untuk kenyamanan Anda.

Jika ada yang bisa saya bantu atau jika Anda ingin informasi lebih detail tentang properti kami, jangan ragu menghubungi saya. Saya siap memberikan konsultasi gratis untuk membantu Anda menemukan properti yang tepat.

Semoga hari Anda menyenangkan.

Best regards,
Sales Consultant
Lumina OS Property Intelligence
```

## 🔧 API Reference

### SalesConsultant Class

**Main Methods:**
```python
# Initialize agent
agent = SalesConsultant()

# Generate single message
result = agent.generate_followup_message(lead_data)

# Batch processing
results = agent.batch_generate_messages(leads_data)

# Get agent status
status = agent.get_agent_status()
```

**Response Format:**
```json
{
  "success": true,
  "message": "Halo Budi Santoso, S.T., ...",
  "metadata": {
    "lead_id": 123,
    "lead_name": "Budi Santoso, S.T.",
    "skor_akhir": 85.5,
    "kategori": "Hot",
    "tone_style": "urgent_direct",
    "message_source": "AI_Gemini",
    "generated_at": "2024-05-28T14:30:00",
    "personalization": {
      "nama": "Budi Santoso, S.T.",
      "lokasi": "Serang",
      "pekerjaan": "PNS"
    }
  }
}
```

## 🔒 Security & Compliance

### Safety Measures:
- ✅ **Draft-Only System**: Messages are generated as drafts, not sent automatically
- ✅ **Manual Review**: All messages require human approval before sending
- ✅ **Audit Trail**: Complete logging of all generated messages
- ✅ **Data Privacy**: Personal data handled according to privacy policies
- ✅ **Error Handling**: Graceful fallback to template-based messages

### Logging:
```
[CLOSER AGENT] Processing lead: Budi Santoso, S.T. (ID: 123)
✅ Message generated successfully!
   Score: 85.5 | Category: Hot
   Tone: urgent_direct | Source: AI_Gemini
💾 Follow-up message saved to database for lead: Budi Santoso, S.T.
```

## 📈 Business Impact

### Operational Excellence:
- **Time Savings**: Automated message generation saves hours of manual work
- **Consistency**: Standardized messaging quality across all leads
- **Personalization**: AI-powered personalization increases engagement rates
- **Scalability**: Handle hundreds of leads without manual effort

### Customer Experience:
- **Professional Communication**: High-quality, personalized messages
- **Timely Follow-up**: Automated system ensures no leads are forgotten
- **Relevant Content**: Messages tailored to lead category and profile
- **Trust Building**: Professional tone builds credibility and trust

### Sales Performance:
- **Higher Conversion**: Personalized messages increase conversion rates
- **Better Engagement**: Relevant content improves response rates
- **Efficient Pipeline**: Automated nurturing keeps leads warm
- **Data-Driven**: Scoring-based approach prioritizes high-value leads

## 📁 File Structure

```
core_modules/
├── closer_agent/
│   └── sales_consultant.py      # Main Sales Consultant Agent
scripts/
└── run_closer_agent.py          # Scheduler script
```

## 🎯 Next Steps

### Fase 3 Continuation:
1. **Jalur C**: SMS/WhatsApp Automation System
2. **Jalur D**: Social Media Integration
3. **Jalur E**: Email Campaign Automation

### Enhancement Opportunities:
- Multi-language support
- A/B testing for message templates
- Integration with CRM systems
- Advanced analytics for message performance
- Real-time delivery tracking

## 🚀 System Status

- ✅ **Sales Consultant Agent**: Fully functional with AI integration
- ✅ **AI Gemini Integration**: Working with fallback system
- ✅ **Tone Adaptation**: Hot/Warm/Cold categories implemented
- ✅ **Scheduler Script**: Single and continuous modes available
- ✅ **Security Features**: Draft-only system with manual review
- ✅ **Database Integration**: Messages stored for review and tracking

**Lumina OS Sales Consultant Agent siap untuk intelligent follow-up automation!** 🎉

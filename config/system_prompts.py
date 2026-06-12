# SYSTEM PROMPT UPDATE - Central Intelligence Hub
# Sebelum melakukan riset, muat data dari config/sources.json dan gunakan insight dari reports/executive_summary.md sebagai konteks makro.

INSTRUCTIONS_BEFORE_TASK = """
Sebelum melakukan riset, pastikan untuk:
1. Muat konfigurasi sumber dari config/sources.json
2. Baca executive summary terbaru dari reports/executive_summary.md
3. Gunakan insight makro sebagai konteks untuk pengambilan keputusan
4. Pertimbangkan alerts dan trend dari executive summary dalam analisis
"""

# Update prompts untuk existing agents
SCOUT_AGENT_PROMPT = INSTRUCTIONS_BEFORE_TASK + """
Scout Agent Instructions:
- Gunakan insight dari executive summary untuk target lokasi yang prospektif
- Pertimbangkan government updates dan policy changes dalam strategi pencarian
- Fokus pada area dengan actionable insights dari executive summary
"""

COMPETITOR_AGENT_PROMPT = INSTRUCTIONS_BEFORE_TASK + """
Competitor Agent Instructions:
- Monitor competitor activities dalam konteks market trend dari executive summary
- Perhatikan government updates yang mungkin mempengaruhi strategi kompetitor
- Gunakan alerts dari executive summary untuk identifikasi peluang
"""

GEO_AGENT_PROMPT = INSTRUCTIONS_BEFORE_TASK + """
Geo Agent Instructions:
- Analisis area dengan mempertimbangkan government updates dari executive summary
- Fokus pada lokasi dengan actionable insights dan market trend positif
- Gunakan policy changes untuk identifikasi area dengan potensi masa depan
"""
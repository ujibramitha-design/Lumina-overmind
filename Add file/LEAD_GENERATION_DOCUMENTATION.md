# 🚀 Lead Generation Scraper - Documentation

## Overview
Automated lead generation system using DuckDuckGo search combined with predictive scoring to identify and qualify real estate leads from web search results.

## 🎯 System Architecture

### Data Flow
```
DuckDuckGo Search → LeadScorer → SQLite Database
```

1. **Search**: Use DDGS to search for real estate related queries
2. **Score**: Process results through LeadScorer for quality assessment
3. **Store**: Insert qualified leads into SQLite database
4. **Track**: Monitor scraping statistics and performance

## 🔧 Technical Implementation

### Dependencies
- **Python 3**: Core programming language
- **sqlite3**: Database management
- **duckduckgo-search**: Web search engine (via ddgs)
- **LeadScorer**: Predictive scoring system
- **time**: Rate limiting and delays

### Database Schema
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    contact TEXT,
    url TEXT,
    keywords TEXT,
    source TEXT DEFAULT 'web_scraping',
    score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'new',
    location TEXT,
    date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Key Components

#### LeadScorer Integration
```python
from api.utils.predictive_scoring import LeadScorer

# Initialize scorer
scorer = LeadScorer()

# Score lead content
result = scorer.calculate_score(
    title=business_name,
    description=contact,
    source='duckduckgo_search'
)

# Extract scoring data
score = result.score
status = result.status
keywords = result.keywords_found
```

#### DuckDuckGo Search
```python
from duckduckgo_search import DDGS

# Search with results limit
ddgs = DDGS()
results = ddgs.text(query, max_results=10)

# Process each result
for result in results:
    title = result.get('title', '').strip()
    body = result.get('body', '').strip()
    href = result.get('href', '').strip()
```

## 🚀 Usage Examples

### Basic Single Query
```python
from run_lead_generation import run_scraper

# Single search
stats = run_scraper('jual rumah murah jakarta', max_results=10)
print(f"Inserted: {stats['total_inserted']} leads")
```

### Batch Processing
```python
# Multiple queries
queries = [
    'jual rumah baru tangerang selatan',
    'promo perumahan banten',
    'jual apartemen murah jakarta'
]

stats = run_multiple_queries(queries)
print(f"Total inserted: {stats['total_inserted']}")
```

### Custom Query Function
```python
def custom_search(query, max_results=5):
    """Custom search with custom parameters"""
    return run_scraper(query, max_results=max_results)

# Usage
result = custom_search('jual townhouse bekasi')
print(f"Status: {result['success']}")
print(f"Leads: {result['total_inserted']}")
```

## 📊 Search Queries

### High-Value Real Estate Queries
```python
# Property Sales
'jual rumah murah jakarta'
'jual apartemen murah bekasi'
'jual tanah kavling bogor'
'jual ruko murah depok'

# Promotions
'promo perumahan banten'
'diskon apartemen tangerang'
'cashback properti jakarta'
'promo cluster bekasi'

# Investment
'investasi properti cimahi'
'investasi tanah tangerang'
'beli kavling investasi'
'investasi apartemen bandung'

# Location Specific
'rumah dijual jakarta selatan'
'properti tangerang murah'
'apartemen bekasi baru'
'tanah dijual bogor'
```

## 📈 Output Format

### Console Output
```
[12:34:56] 🔧 🚀 INITIATING SCRAPER: 'jual rumah murah jakarta' | Max Results: 10
[12:34:56] ✅ Database initialized successfully
[12:34:56] ℹ️  🔍 Searching DuckDuckGo for: 'jual rumah murah jakarta'
[12:34:57] 📊 FOUND 10 RESULTS FROM DUCKDUCKGO
[12:34:57] 🔄 PROCESSING RESULTS THROUGH SCORING ENGINE
[12:34:57] 🔍 PROCESSING RESULT 1/10: RumahDijual.com - Jual Rumah Murah...
[12:34:57] ✅ INSERTED: RumahDijual.com... | Score: 85 (Warm)
[12:34:57] 🔍 PROCESSING RESULT 2/10: PropertyKita.com - Jual Rumah...
[12:34:57] ✅ INSERTED: PropertyKita.com... | Score: 90 (Hot)
[12:34:57] 🔍 PROCESSING RESULT 3/10: JualProperti.com - Info Harga...
[12:34:57] ✅ INSERTED: JualProperti.com... | Score: 75 (Warm)
```

### Statistics Summary
```
🎯 🎯 MULTI-QUERY SUMMARY
================================================================================
📊 TOTAL QUERIES PROCESSED: 10
🔍 TOTAL RESULTS SEARCHED: 45
💾 TOTAL LEADS INSERTED: 42
❌ TOTAL FAILURES: 3
📈 QUERY DETAILS:
  ✅ jual rumah baru tangerang selatan: 15 inserted, 0 failed
  ✅ promo perumahan banten: 12 inserted, 0 failed
  ✅ jual apartemen murah jakarta: 10 inserted, 0 failed
  ❌ beli tanah kavling bogor: 0 inserted, 3 failed
```

## 🔧 Configuration

### Search Parameters
- **max_results**: Maximum results to process (default: 10)
- **rate_limiting**: 3 seconds between queries
- **timeout**: Connection timeout handling

### Database Configuration
- **Path**: `data/leads.db`
- **Auto-create**: Database created automatically
- **Indexes**: Score, status, date_found, source

### Scoring Parameters
- **Base Score**: 40 points
- **Hot Keywords**: +30 points each
- **Warm Keywords**: +15 points each
- **Negative Keywords**: -20 points each
- **Score Range**: 0-100 (capped)

## 🚨 Error Handling

### Common Issues
```python
try:
    stats = run_scraper(query, max_results=10)
except KeyboardInterrupt:
    print("⚠️  Process interrupted by user")
except Exception as e:
    print(f"❌ Fatal error: {e}")
```

### Database Errors
```python
# Database connection failure
if not initialize_database(db_path):
    print("❌ Database initialization failed")
    return False

# Insert errors
try:
    cursor.execute(sql, params)
    conn.commit()
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
    continue
```

### Search Limitations
```python
# No results found
if not results:
    print("⚠️ No results found for the query")
    return {'success': True, 'total_searched': 0}

# Rate limiting
time.sleep(3)  # Wait between queries
```

## 📈 Performance Metrics

### Search Performance
- **Query Processing**: ~2-5 seconds per query
- **Scoring Speed**: ~0.1ms per lead
- **Database Insert**: ~0.01ms per lead
- **Total Session**: ~30-60 seconds for 10 queries

### Success Rates
- **Typical Success Rate**: 70-90%
- **Common Failures**: No results, network issues, database errors
- **Retry Strategy**: Manual intervention required

## 🔮 Integration Examples

### With Web Scrapers
```python
# Integrate with existing scraper
class PropertyScraper:
    def __init__(self):
        self.scorer = LeadScorer()
        
    def scrape_and_score(self, data):
        for item in data:
            result = self.scorer.calculate_score(
                title=item['title'],
                description=item['description'],
                source='web_scraping'
            )
            item['score'] = result.score
            item['status'] = result.status
            item['keywords'] = result.keywords_found
        return data
```

### With API Systems
```python
# FastAPI endpoint
@app.post("/api/scrape-leads")
async def scrape_leads(query: str, max_results: int = 10):
    scraper = LeadGenerationScraper()
    stats = scraper.run_scraper(query, max_results)
    return {"success": True, "data": stats}
```

### With CRM Systems
```python
# CRM integration
def sync_leads_to_crm():
    scraper = LeadGenerationScraper()
    stats = scraper.run_multiple_queries([
        'jual rumah murah jakarta',
        'jual apartemen murah bekasi'
    ])
    
    # Sync to CRM system
    for query_data in stats['queries_processed']:
        if query_data['inserted'] > 0:
            crm_sync_lead(query_data['query'])
```

## 🔍 Maintenance

### Database Maintenance
```python
# Clean old leads
def cleanup_old_leads(days=30):
    conn = sqlite3.connect('data/leads.db')
    cursor = conn.cursor()
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    cursor.execute(
        "DELETE FROM leads WHERE date_found < ?",
        (cutoff_date,)
    )
    
    conn.commit()
    conn.close()
    print(f"🧹 Cleaned up leads older than {days} days")
```

### Keyword Updates
```python
# Add new keywords
scorer.add_custom_keyword('hot', 'urgent', 25)
scorer.add_custom_keyword('warm', 'premium', 20)

# Remove outdated keywords
scorer.remove_keyword('hot', 'beli')
```

### Performance Optimization
```python
# Increase search results
stats = run_scraper(query, max_results=20)

# Adjust delay between queries
time.sleep(1)  # Faster processing
```

## 🎯 Best Practices

### Query Optimization
- **Specific Terms**: Use specific property types and locations
- **Include Keywords**: Add pricing and promotional terms
- **Location Targeting**: Include city and area names
- **Property Types**: Mention specific property types

### Rate Limiting
- **Respectful Searching**: Don't overwhelm search engines
- **Appropriate Delays**: 3+ seconds between queries
- **Session Limits**: Limit total queries per session

### Data Quality
- **Lead Validation**: Verify lead quality before storage
- **Duplicate Detection**: Check for existing leads
- **Location Extraction**: Extract location information
- **Keyword Analysis**: Track keyword performance

### Error Recovery
- **Graceful Handling**: Continue processing on individual failures
- **Logging**: Log all errors for debugging
- **Retry Logic**: Implement retry for transient errors
- **User Feedback**: Provide clear error messages

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install ddgs

# Verify imports
python -c "from api.utils.predictive_scoring import LeadScorer"
python -c "from duckduckgo_search import DDGS"
```

### 2. Run Scraper
```bash
# Single query
python run_lead_generation.py

# Multiple queries (built-in)
python run_lead_generation.py
```

### 3. Check Results
```bash
# View database contents
sqlite3 data/leads.db "SELECT business_name, score, status, location FROM leads ORDER BY score DESC LIMIT 10;"

# Count leads by status
sqlite3 data/leads.db "SELECT status, COUNT(*) FROM leads GROUP BY status;"
```

### 4. Integration
```python
# Import in your application
from run_lead_generation import run_scraper

# Use in your code
stats = run_scraper('jual rumah murah jakarta')
leads = get_high_score_leads(stats)
```

## 📁 File Structure
```
dashboard/
├── api/utils/predictive_scoring.py    # Scoring utility
├── data/leads.db                 # SQLite database
├── run_lead_generation.py           # Main scraper script
├── LEAD_GENERATION_DOCUMENTATION.md # This documentation
└── data/                        # Data directory
```

## 🔧 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Fix import path issues
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python run_lead_generation.py
```

#### Database Errors
```bash
# Check database permissions
ls -la data/leads.db

# Rebuild database
rm data/leads.db
python run_lead_generation.py  # Will recreate
```

#### Search Issues
```bash
# Test DuckDuckGo search
python -c "from duckduckgo_search import DDGS; print(DDGS().text('test'))"

# Check internet connection
ping duckduckgo.com
```

#### Package Installation
```bash
# Install missing packages
pip install ddgs
pip install duckduckgo-search
```

---

*Last updated: May 30, 2026*

# 🧠 Predictive Scoring Utility - Documentation

## Overview
Advanced lead scoring system for evaluating lead quality based on content analysis using keyword-based scoring algorithms.

## 🎯 Scoring Algorithm

### Base Score System
- **Base Score**: 40 points (all leads start with this)
- **Hot Keywords**: +30 points each
- **Warm Keywords**: +15 points each
- **Negative Keywords**: -20 points each
- **Score Range**: 0-100 (capped)

### Status Classification
- **Hot**: Score >= 80
- **Warm**: Score 60-79
- **Cold**: Score < 60

## 🔤 Keyword Categories

### Hot Keywords (+30 points each)
```python
HOT_KEYWORDS = {
    'jual': 30, 'harga': 30, 'promo': 30, 'murah': 30,
    'diskon': 30, 'kpr': 30, 'cicilan': 30, 'booking': 30,
    'ready stock': 30, 'ready_stock': 30, 'dijual': 30,
    'beli': 30, 'investasi': 30, 'tunai': 30, 'cash': 30,
    'deal': 30, 'offer': 30, 'penawaran': 30
}
```

**Indicators**:
- High purchase intent
- Pricing discussions
- Promotional content
- Financial terms

### Warm Keywords (+15 points each)
```python
WARM_KEYWORDS = {
    'perumahan': 15, 'cluster': 15, 'apartemen': 15,
    'properti': 15, 'lokasi': 15, 'fasilitas': 15,
    'rumah': 15, 'tanah': 15, 'ruko': 15, 'kavling': 15,
    'type': 15, 'tipe': 15, 'unit': 15, 'bangun': 15,
    'konstruksi': 15, 'developer': 15, 'pengembang': 15,
    'proyek': 15, 'area': 15, 'wilayah': 15,
    'kota': 15, 'alamat': 15
}
```

**Indicators**:
- Property types
- Location information
- General real estate terms
- Developer information

### Negative Keywords (-20 points each)
```python
NEGATIVE_KEYWORDS = {
    'penipuan': -20, 'berita': -20, 'komplain': -20,
    'kasus': -20, 'penipu': -20, 'scam': -20,
    'hoax': -20, 'palsu': -20, 'tipu': -20,
    'masalah': -20, 'keluhan': -20, 'kecewa': -20,
    'buruk': -20, 'jelek': -20, 'gagal': -20,
    'batal': -20, 'tidak': -20, 'bukan': -20,
    'error': -20, 'salah': -20
}
```

**Indicators**:
- Fraud/scam warnings
- Complaints and issues
- Negative experiences
- Problematic situations

## 🏗️ Class Structure

### LeadScorer Class
```python
class LeadScorer:
    def __init__(self):
        """Initialize with compiled regex patterns"""
        
    def calculate_score(self, title: str, description: str, source: str = "") -> ScoringResult:
        """Calculate lead score based on content analysis"""
        
    def batch_score(self, leads: List[Dict[str, str]]) -> List[ScoringResult]:
        """Score multiple leads in batch"""
        
    def add_custom_keyword(self, category: str, keyword: str, score: int) -> bool:
        """Add custom keyword to category"""
        
    def remove_keyword(self, category: str, keyword: str) -> bool:
        """Remove keyword from category"""
        
    def get_keyword_stats(self) -> Dict[str, Dict[str, int]]:
        """Get keyword statistics"""
```

### ScoringResult DataClass
```python
@dataclass
class ScoringResult:
    score: int
    status: str
    keywords_found: List[str]
    breakdown: Dict[str, int]
```

## 🚀 Usage Examples

### Basic Usage
```python
from api.utils.predictive_scoring import LeadScorer

# Initialize scorer
scorer = LeadScorer()

# Calculate single lead score
result = scorer.calculate_score(
    title="JUAL Rumah Murah",
    description="Properti dengan harga promo dan KPR mudah",
    source="website"
)

print(f"Score: {result.score}")
print(f"Status: {result.status}")
print(f"Keywords: {result.keywords_found}")
```

### Batch Processing
```python
leads = [
    {
        'title': 'JUAL CEPAT Rumah',
        'description': 'Properti dengan harga murah',
        'source': 'website'
    },
    {
        'title': 'Perumahan Cluster',
        'description': 'Lokasi strategis',
        'source': 'portal'
    }
]

results = scorer.batch_score(leads)
for result in results:
    print(f"Lead: {result.score} ({result.status})")
```

### Custom Keywords
```python
# Add custom hot keyword
scorer.add_custom_keyword('hot', 'urgent', 25)

# Add custom warm keyword
scorer.add_custom_keyword('warm', 'premium', 20)

# Remove keyword
scorer.remove_keyword('hot', 'urgent')
```

## 📊 Advanced Features

### Text Normalization
- **Case Insensitive**: "JUAL" == "jual"
- **Punctuation Handling**: "jual!" == "jual"
- **Whitespace Normalization**: Multiple spaces → single space
- **Special Characters**: Handles punctuation gracefully

### Performance Optimization
- **Pre-compiled Regex**: Patterns compiled once at initialization
- **Efficient Search**: Word boundary matching
- **Batch Processing**: Process multiple leads efficiently

### Extensibility
- **Custom Keywords**: Add/remove keywords dynamically
- **Category Management**: Hot, warm, negative categories
- **Score Adjustment**: Modify keyword weights

## 🧪 Testing

### Running Tests
```bash
# Run comprehensive test suite
python test_predictive_scoring.py
```

### Test Coverage
- ✅ Basic functionality
- ✅ Hot keyword detection
- ✅ Warm keyword detection
- ✅ Negative keyword detection
- ✅ Status classification
- ✅ Batch processing
- ✅ Edge cases
- ✅ Custom keywords
- ✅ Keyword statistics

### Test Examples
```python
# Test hot keywords
result = scorer.calculate_score(
    "JUAL BELI Promo Diskon",
    "Ready stock dengan harga murah dan KPR",
    "website"
)
# Expected: Score 100 (Hot), Keywords: ['jual', 'beli', 'promo', 'diskon', 'ready stock', 'murah', 'kpr']

# Test warm keywords
result = scorer.calculate_score(
    "Perumahan Cluster Apartemen",
    "Properti dengan lokasi strategis dan fasilitas lengkap",
    "portal"
)
# Expected: Score 100 (capped), Status: Hot

# Test negative keywords
result = scorer.calculate_score(
    "Berita Penipuan",
    "Kasus penipuan investasi properti palsu",
    "social_media"
)
# Expected: Score 0 (capped), Status: Cold
```

## 📈 Integration Examples

### Web Scraper Integration
```python
from api.utils.predictive_scoring import LeadScorer

class PropertyScraper:
    def __init__(self):
        self.scorer = LeadScorer()
    
    def process_lead(self, lead_data):
        """Process scraped lead data and calculate score"""
        score_result = self.scorer.calculate_score(
            title=lead_data.get('title', ''),
            description=lead_data.get('description', ''),
            source=lead_data.get('source', '')
        )
        
        # Add score to lead data
        lead_data['score'] = score_result.score
        lead_data['status'] = score_result.status
        lead_data['keywords'] = score_result.keywords_found
        
        return lead_data
```

### API Integration
```python
# In FastAPI endpoint
from api.utils.predictive_scoring import LeadScorer

@app.post("/api/score-lead")
async def score_lead(lead: LeadRequest):
    scorer = LeadScorer()
    result = scorer.calculate_score(lead.title, lead.description, lead.source)
    
    return {
        "success": True,
        "data": {
            "score": result.score,
            "status": result.status,
            "keywords": result.keywords_found,
            "breakdown": result.breakdown
        }
    }
```

### Database Integration
```python
# In database operations
def update_lead_scores():
    scorer = LeadScorer()
    
    # Get all leads without scores
    leads = db.execute("SELECT id, title, description, source FROM leads WHERE score IS NULL")
    
    for lead in leads:
        result = scorer.calculate_score(lead['title'], lead['description'], lead['source'])
        
        # Update database
        db.execute(
            "UPDATE leads SET score = ?, status = ?, keywords = ? WHERE id = ?",
            (result.score, result.status, ','.join(result.keywords_found), lead['id'])
        )
```

## 🔧 Configuration

### Customizing Keywords
```python
# Add industry-specific keywords
scorer.add_custom_keyword('hot', 'townhouse', 25)
scorer.add_custom_keyword('warm', 'condominium', 15)
scorer.add_custom_keyword('negative', 'litigation', -20)

# Remove unwanted keywords
scorer.remove_keyword('hot', 'beli')  # If 'buy' is too generic
```

### Adjusting Base Score
```python
# Modify base score in the class
class CustomLeadScorer(LeadScorer):
    BASE_SCORE = 50  # Increase base score for your industry
```

### Adding New Categories
```python
class ExtendedLeadScorer(LeadScorer):
    def __init__(self):
        super().__init__()
        # Add new category
        self.MEDIUM_KEYWORDS = {
            'medium': 20,
            'standard': 20,
            'regular': 20
        }
        self._compile_patterns()
```

## 📊 Performance Metrics

### Keyword Statistics
```python
stats = scorer.get_keyword_stats()
print(f"Hot keywords: {stats['hot_keywords']['count']}")
print(f"Warm keywords: {stats['warm_keywords']['count']}")
print(f"Negative keywords: {stats['negative_keywords']['count']}")
```

### Scoring Distribution
```python
# Analyze scoring distribution
import statistics

scores = [result.score for result in batch_results]
print(f"Average score: {statistics.mean(scores):.1f}")
print(f"Median score: {statistics.median(scores)}")
print(f"Score range: {min(scores)} - {max(scores)}")
```

## 🎯 Business Value

### Lead Prioritization
- **Hot Leads**: Immediate follow-up, high conversion potential
- **Warm Leads**: Standard follow-up, moderate potential
- **Cold Leads**: Low priority, nurturing required

### Marketing Insights
- **Keyword Analysis**: Understand customer language patterns
- **Content Optimization**: Adjust marketing copy based on high-performing keywords
- **Lead Quality Trends**: Monitor scoring patterns over time

### Sales Efficiency
- **Automated Triage**: Reduce manual lead qualification
- **Priority Routing**: Route leads to appropriate sales teams
- **Performance Tracking**: Measure conversion rates by lead score

## 🔮 Future Enhancements

### Machine Learning Integration
- **NLP Processing**: Natural language understanding
- **Semantic Analysis**: Context-aware scoring
- **Pattern Recognition**: Identify buying signals

### Advanced Analytics
- **Time-based Scoring**: Consider lead age and activity
- **Source Weighting**: Different scores for different sources
- **Historical Data**: Learn from past conversions

### Real-time Features
- **Live Scoring**: Score leads as they come in
- **Score Updates**: Adjust scores based on interactions
- **Alert System**: Notifications for high-scoring leads

---

## 🚀 Quick Start

1. **Import the utility**:
   ```python
   from api.utils.predictive_scoring import LeadScorer
   ```

2. **Initialize scorer**:
   ```python
   scorer = LeadScorer()
   ```

3. **Score a lead**:
   ```python
   result = scorer.calculate_score(title, description, source)
   ```

4. **Use the results**:
   ```python
   print(f"Score: {result.score}")
   print(f"Status: {result.status}")
   ```

## 📁 File Structure
```
dashboard/
├── api/utils/predictive_scoring.py    # Main scoring utility
├── test_predictive_scoring.py          # Test suite
└── PREDICTIVE_SCORING_DOCUMENTATION.md  # This documentation
```

---

*Last updated: May 30, 2026*

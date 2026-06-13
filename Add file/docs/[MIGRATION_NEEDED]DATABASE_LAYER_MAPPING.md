# 🎯 DATABASE LAYER MAPPING ELITE HUNTER - LENGKAP

## 📊 **DATABASE ARCHITECTURE - SINGLE SOURCE OF TRUTH**

```
🏗️ DATABASE LAYER ARCHITECTURE
├── 📊 leads.db (SQLite)                    # DATABASE UTAMA - SINGLE SOURCE OF TRUTH
│   ├── 👥 leads TABLE                     # LEAD DATA LAYER
│   ├── 🎯 scoring_log TABLE               # SCORING ANALYTICS LAYER  
│   ├── 📈 market_data TABLE               # MARKET INTELLIGENCE LAYER
│   ├── 🏢 competitors TABLE                # COMPETITOR INTELLIGENCE LAYER
│   ├── 📍 geo_data TABLE                   # GEO-INTELLIGENCE LAYER
│   ├── 🔔 alerts TABLE                     # NOTIFICATION LAYER
│   ├── 📝 system_logs TABLE                # SYSTEM MONITORING LAYER
│   └── 🤖 ai_logs TABLE                    # AI PROCESSING LAYER
│
├── 📊 properties.db (SQLite)              # PROPERTY DATA LAYER
│   ├── 🏠 properties TABLE                 # PROPERTY LISTING LAYER
│   ├── 📷 property_media TABLE            # PROPERTY MEDIA LAYER
│   ├── 📋 property_specifications TABLE    # PROPERTY SPECS LAYER
│   └── 📈 property_analytics TABLE          # PROPERTY ANALYTICS LAYER
│
├── 📊 users.db (SQLite)                    # USER MANAGEMENT LAYER
│   ├── 👤 users TABLE                      # USER PROFILE LAYER
│   ├── 🔐 user_sessions TABLE              # USER SESSION LAYER
│   ├── 🎯 user_preferences TABLE           # USER PREFERENCES LAYER
│   └── 📊 user_activity TABLE              # USER ACTIVITY LAYER
│
├── 📊 analytics.db (SQLite)                # ANALYTICS DATA LAYER
│   ├── 📈 performance_metrics TABLE         # PERFORMANCE METRICS LAYER
│   ├── 🎯 conversion_tracking TABLE         # CONVERSION TRACKING LAYER
│   ├── 📊 engagement_metrics TABLE         # ENGAGEMENT METRICS LAYER
│   └── 📈 roi_analytics TABLE              # ROI ANALYTICS LAYER
│
└── 📊 system.db (SQLite)                   # SYSTEM CONFIGURATION LAYER
    ├── ⚙️ system_config TABLE              # SYSTEM CONFIGURATION LAYER
    ├── 🔌 api_keys TABLE                    # API KEYS MANAGEMENT LAYER
    ├── 📋 cron_jobs TABLE                   # SCHEDULED JOBS LAYER
    └── 📝 audit_trail TABLE                 # AUDIT TRAIL LAYER
```

## 🎯 **DATABASE SCHEMA DETAIL - SINGLE SOURCE OF TRUTH**

### 📊 **leads.db - DATABASE UTAMA**

#### **👥 leads TABLE - LEAD DATA LAYER**
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,                           -- Lead title/headline
    url TEXT,                                    -- Source URL
    snippet TEXT,                                -- Content snippet
    content TEXT,                                -- Full content
    score INTEGER DEFAULT 1,                     -- AI scoring (1-10)
    elite_score INTEGER DEFAULT 1,              -- Enhanced scoring
    lead_type TEXT DEFAULT 'unknown',           -- 'buyer', 'seller', 'investor'
    location TEXT,                               -- Geographic location
    status TEXT DEFAULT 'new',                  -- 'new', 'contacted', 'qualified', 'closed'
    intent_category TEXT DEFAULT 'Informational', -- Intent classification
    confidence_level REAL DEFAULT 0.0,          -- Scoring confidence
    
    -- Contact Information Layer
    contact_info TEXT,                           -- JSON: {phone, email, social_media}
    phone_number TEXT,                           -- Extracted phone number
    email_address TEXT,                           -- Extracted email address
    whatsapp_number TEXT,                        -- WhatsApp number
    
    -- Entity Extraction Layer
    entities_extracted TEXT,                    -- JSON: {price, location, bank, pain_point}
    price_range TEXT,                             -- Extracted price range
    budget_range TEXT,                            -- Extracted budget range
    
    -- Behavioral Analysis Layer
    behavioral_signals TEXT,                      -- JSON: {search_intent, engagement_potential, conversion_probability}
    urgency_score INTEGER DEFAULT 0,              -- Urgency assessment (0-100)
    potential_value TEXT,                          -- Estimated potential value
    
    -- Quality Assessment Layer
    data_quality_score INTEGER DEFAULT 0,        -- Content quality score (0-100)
    validation_status TEXT DEFAULT 'pending',    -- 'qualified', 'invalid_format', 'suspected_bot'
    
    -- Source & Tracking Layer
    source_engine TEXT,                           -- Search engine source
    source_zone TEXT,                             -- Hunting zone source
    query_used TEXT,                              -- Search query used
    search_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- Search timestamp
    
    -- Metadata Layer
    metadata TEXT,                                -- JSON: {discovery_timestamp, search_session_id, zone_priority}
    system_info TEXT,                             -- JSON: {processing_version, integrity_check, validation}
    
    -- Timestamps
    date_found DATETIME DEFAULT CURRENT_TIMESTAMP, -- Discovery timestamp
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Creation timestamp
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Last update timestamp
    
    -- Indexes for Performance
    INDEX idx_lead_type (lead_type),
    INDEX idx_location (location),
    INDEX idx_score (score),
    INDEX idx_status (status),
    INDEX idx_date_found (date_found),
    INDEX idx_validation_status (validation_status)
);
```

#### **🎯 scoring_log TABLE - SCORING ANALYTICS LAYER**
```sql
CREATE TABLE scoring_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,                     -- Reference to leads.id
    score INTEGER NOT NULL,                         -- Score assigned
    analysis_type TEXT NOT NULL,                    -- 'llm', 'traditional', 'advanced'
    
    -- LLM Analysis Layer
    llm_response TEXT,                             -- LLM response text
    llm_confidence REAL DEFAULT 0.0,              -- LLM confidence level
    llm_model TEXT,                               -- LLM model used
    
    -- Traditional Scoring Layer
    traditional_score INTEGER DEFAULT 0,           -- Traditional keyword score
    high_intent_count INTEGER DEFAULT 0,          -- High intent keyword matches
    warm_count INTEGER DEFAULT 0,                -- Warm keyword matches
    cold_count INTEGER DEFAULT 0,                -- Cold keyword matches
    negative_count INTEGER DEFAULT 0,             -- Negative keyword matches
    
    -- Entity Analysis Layer
    entities_extracted TEXT,                      -- JSON: {price, location, bank, pain_point}
    entity_confidence REAL DEFAULT 0.0,           -- Entity extraction confidence
    
    -- Intent Classification Layer
    intent_category TEXT,                         -- 'Informational', 'Comparison', 'Pain-Point', 'Transactional'
    intent_confidence REAL DEFAULT 0.0,           -- Intent classification confidence
    
    -- Psychographic Analysis Layer
    psychographic_profile TEXT,                   -- JSON: {primary_value, secondary_values, marketing_insights}
    value_confidence REAL DEFAULT 0.0,            -- Psychographic analysis confidence
    
    -- Quality Indicators Layer
    quality_indicators TEXT,                      -- JSON: {has_contact_info, has_price_info, has_location_info}
    content_length INTEGER DEFAULT 0,              -- Content character length
    title_length INTEGER DEFAULT 0,               -- Title character length
    
    -- Processing Metadata Layer
    processing_time_ms INTEGER DEFAULT 0,          -- Processing time in milliseconds
    processing_version TEXT,                        -- Processing algorithm version
    error_message TEXT,                            -- Error message if any
    
    -- Timestamps
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,   -- Scoring timestamp
    
    -- Indexes for Performance
    INDEX idx_lead_id (lead_id),
    INDEX idx_analysis_type (analysis_type),
    INDEX idx_score (score),
    INDEX idx_timestamp (timestamp),
    INDEX idx_intent_category (intent_category),
    
    -- Foreign Key Constraint
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);
```

#### **📈 market_data TABLE - MARKET INTELLIGENCE LAYER**
```sql
CREATE TABLE market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_type TEXT NOT NULL,                     -- 'price', 'facility', 'competitor', 'trend'
    query TEXT NOT NULL,                           -- Search query used
    search_location TEXT,                          -- Search location
    search_engine TEXT,                           -- Search engine used
    
    -- Results Layer
    results TEXT,                                  -- JSON: {search_results, extracted_data, analysis}
    result_count INTEGER DEFAULT 0,               -- Number of results
    
    -- Market Analysis Layer
    market_insights TEXT,                         -- JSON: {market_trends, price_analysis, competitor_analysis}
    price_analysis TEXT,                          -- JSON: {price_range, average_price, price_trends}
    facility_analysis TEXT,                       -- JSON: {schools, hospitals, commercial_centers}
    competitor_analysis TEXT,                      -- JSON: {competitors, market_share, positioning}
    
    -- Intelligence Layer
    intelligence_summary TEXT,                    -- Executive summary
    recommendations TEXT,                          -- JSON: {strategic_recommendations, action_items}
    confidence_level REAL DEFAULT 0.0,           -- Intelligence confidence
    
    -- Processing Metadata Layer
    processing_time_ms INTEGER DEFAULT 0,          -- Processing time
    data_sources TEXT,                            -- JSON: {sources, reliability, freshness}
    
    -- Timestamps
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,   -- Data collection timestamp
    
    -- Indexes for Performance
    INDEX idx_search_type (search_type),
    INDEX idx_search_location (search_location),
    INDEX idx_timestamp (timestamp),
    INDEX idx_query (query)
);
```

#### **🏢 competitors TABLE - COMPETITOR INTELLIGENCE LAYER**
```sql
CREATE TABLE competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_name TEXT UNIQUE NOT NULL,          -- Competitor name
    competitor_type TEXT DEFAULT 'unknown',        -- 'developer', 'agency', 'individual'
    
    -- Contact Information Layer
    website TEXT,                                  -- Official website
    contact_email TEXT,                           -- Contact email
    contact_phone TEXT,                           -- Contact phone
    social_media TEXT,                            -- JSON: {facebook, instagram, linkedin, twitter}
    
    -- Location Information Layer
    locations TEXT,                                -- JSON: [{name, address, coordinates, projects}]
    primary_location TEXT,                         -- Primary location
    
    -- Business Information Layer
    services TEXT,                                 -- JSON: {services, specialties, target_markets}
    market_position TEXT,                          -- Market positioning
    target_audience TEXT,                          -- Target audience profile
    
    -- Pricing Information Layer
    price_range TEXT,                              -- JSON: {min, max, average, currency}
    pricing_strategy TEXT,                         -- Pricing strategy description
    
    -- Market Intelligence Layer
    market_share REAL DEFAULT 0.0,                -- Estimated market share
    competitive_advantages TEXT,                   -- JSON: {advantages, unique_selling_points}
    competitive_weaknesses TEXT,                   -- JSON: {weaknesses, threats}
    
    -- Reputation Analysis Layer
    reputation_score REAL DEFAULT 0.0,            -- Reputation score (-1 to 1)
    sentiment_analysis TEXT,                        -- JSON: {overall_sentiment, main_complaints, positive_points}
    customer_reviews TEXT,                         -- JSON: {reviews_count, average_rating, recent_reviews}
    
    -- Tracking Layer
    last_scanned DATETIME DEFAULT CURRENT_TIMESTAMP, -- Last data collection
    scan_frequency INTEGER DEFAULT 7,              -- Scan frequency in days
    data_freshness TEXT DEFAULT 'unknown',        -- Data freshness assessment
    
    -- Metadata Layer
    metadata TEXT,                                 -- JSON: {data_sources, reliability, last_update}
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Record creation
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Last update
    
    -- Indexes for Performance
    INDEX idx_competitor_name (competitor_name),
    INDEX idx_competitor_type (competitor_type),
    INDEX idx_primary_location (primary_location),
    INDEX idx_market_share (market_share),
    INDEX idx_last_scanned (last_scanned)
);
```

#### **📍 geo_data TABLE - GEO-INTELLIGENCE LAYER**
```sql
CREATE TABLE geo_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name TEXT NOT NULL,                       -- Area name
    area_type TEXT DEFAULT 'unknown',              -- 'residential', 'commercial', 'industrial', 'mixed'
    
    -- Geographic Information Layer
    latitude REAL NOT NULL,                        -- Area latitude
    longitude REAL NOT NULL,                       -- Area longitude
    radius_meters INTEGER DEFAULT 5000,            -- Analysis radius in meters
    coordinates TEXT,                              -- JSON: {center: {lat, lng}, boundary: [{lat, lng}]}
    
    -- BPS Data Integration Layer
    bps_data TEXT,                                 -- JSON: {population, demographics, economy, infrastructure}
    population_density REAL DEFAULT 0.0,            -- Population density per km²
    dominant_age_group TEXT,                       -- Dominant age group
    average_income TEXT,                           -- Average income range
    growth_rate REAL DEFAULT 0.0,                   -- Population growth rate
    
    -- Facility Mapping Layer
    schools TEXT,                                  -- JSON: [{name, type, distance, rating, capacity}]
    hospitals TEXT,                                -- JSON: [{name, type, distance, beds, services}]
    commercial_centers TEXT,                        -- JSON: [{name, type, distance, size, tenants}]
    transportation TEXT,                            -- JSON: [{type, name, distance, accessibility}]
    
    -- Area Intelligence Layer
    facility_density REAL DEFAULT 0.0,             -- Facility density score
    accessibility_score REAL DEFAULT 0.0,           -- Accessibility score
    market_potential_score REAL DEFAULT 0.0,       -- Market potential score (1-10)
    
    -- Persona Analysis Layer
    area_persona TEXT,                             -- JSON: {type, characteristics, needs, preferences}
    target_audience TEXT,                          -- Target audience profile
    primary_needs TEXT,                            -- Primary needs analysis
    marketing_focus TEXT,                           -- Recommended marketing focus
    
    -- Development Intelligence Layer
    development_projects TEXT,                      -- JSON: [{name, type, status, timeline, impact}]
    infrastructure_plans TEXT,                      -- JSON: [{type, description, timeline, impact}]
    zoning_information TEXT,                         -- JSON: {current_zoning, planned_changes, restrictions}
    
    -- Intelligence Summary Layer
    intelligence_summary TEXT,                      -- Executive summary
    strategic_recommendations TEXT,                 -- JSON: {recommendations, opportunities, threats}
    
    -- Processing Metadata Layer
    data_sources TEXT,                             -- JSON: {sources, reliability, last_update}
    analysis_confidence REAL DEFAULT 0.0,          -- Analysis confidence level
    
    -- Timestamps
    last_analysis DATETIME DEFAULT CURRENT_TIMESTAMP, -- Last analysis timestamp
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Record creation
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Last update
    
    -- Indexes for Performance
    INDEX idx_area_name (area_name),
    INDEX idx_area_type (area_type),
    INDEX idx_market_potential_score (market_potential_score),
    INDEX idx_last_analysis (last_analysis),
    INDEX idx_coordinates (latitude, longitude)
);
```

#### **🔔 alerts TABLE - NOTIFICATION LAYER**
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type TEXT NOT NULL,                      -- 'high_intent_lead', 'price_drift', 'system_error', 'competitor_alert'
    alert_priority TEXT DEFAULT 'medium',          -- 'low', 'medium', 'high', 'critical'
    
    -- Alert Content Layer
    title TEXT NOT NULL,                           -- Alert title
    message TEXT NOT NULL,                         -- Alert message
    details TEXT,                                  -- JSON: {detailed_information, context, data}
    
    -- Related Data Layer
    lead_id INTEGER,                               -- Reference to leads.id (if applicable)
    competitor_id INTEGER,                         -- Reference to competitors.id (if applicable)
    geo_area_id INTEGER,                           -- Reference to geo_data.id (if applicable)
    
    -- Delivery Layer
    delivery_channels TEXT,                        -- JSON: {telegram, email, sms, webhook}
    delivery_status TEXT DEFAULT 'pending',        -- 'pending', 'sent', 'delivered', 'failed'
    delivery_attempts INTEGER DEFAULT 0,          -- Number of delivery attempts
    delivery_timestamp DATETIME,                  -- Successful delivery timestamp
    
    -- Response Layer
    response_required BOOLEAN DEFAULT FALSE,       -- Whether response is required
    response_status TEXT DEFAULT 'pending',       -- 'pending', 'acknowledged', 'resolved', 'ignored'
    response_timestamp DATETIME,                   -- Response timestamp
    
    -- Processing Metadata Layer
    processing_time_ms INTEGER DEFAULT 0,          -- Processing time
    error_message TEXT,                            -- Error message if delivery failed
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Alert creation timestamp
    resolved_at DATETIME,                         -- Resolution timestamp
    
    -- Indexes for Performance
    INDEX idx_alert_type (alert_type),
    INDEX idx_alert_priority (alert_priority),
    INDEX idx_delivery_status (delivery_status),
    INDEX idx_created_at (created_at),
    INDEX idx_lead_id (lead_id),
    INDEX idx_competitor_id (competitor_id),
    
    -- Foreign Key Constraints
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE SET NULL,
    FOREIGN KEY (competitor_id) REFERENCES competitors(id) ON DELETE SET NULL,
    FOREIGN KEY (geo_area_id) REFERENCES geo_data(id) ON DELETE SET NULL
);
```

#### **📝 system_logs TABLE - SYSTEM MONITORING LAYER**
```sql
CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,                           -- Module name (e.g., 'market_intelligence', 'lead_hunter')
    level TEXT NOT NULL,                            -- 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    message TEXT NOT NULL,                         -- Log message
    
    -- Context Information Layer
    context TEXT,                                  -- JSON: {additional_context, parameters, state}
    stack_trace TEXT,                              -- Stack trace for errors
    
    -- Performance Layer
    execution_time_ms INTEGER DEFAULT 0,          -- Execution time in milliseconds
    memory_usage_mb REAL DEFAULT 0.0,              -- Memory usage in MB
    
    -- User/Session Layer
    user_id INTEGER,                               -- User ID (if applicable)
    session_id TEXT,                               -- Session ID (if applicable)
    ip_address TEXT,                               -- IP address (if applicable)
    
    -- Metadata Layer
    metadata TEXT,                                 -- JSON: {additional_metadata, tags, categories}
    
    -- Timestamps
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,   -- Log timestamp
    
    -- Indexes for Performance
    INDEX idx_module (module),
    INDEX idx_level (level),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_level_timestamp (level, timestamp)
);
```

#### **🤖 ai_logs TABLE - AI PROCESSING LAYER**
```sql
CREATE TABLE ai_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ai_model TEXT NOT NULL,                         -- AI model used (e.g., 'gpt-3.5-turbo', 'gpt-4', 'claude-3')
    processing_type TEXT NOT NULL,                  -- 'lead_scoring', 'content_generation', 'sentiment_analysis'
    
    -- Input Data Layer
    input_data TEXT,                               -- JSON: {input_text, parameters, context}
    input_tokens INTEGER DEFAULT 0,               -- Number of input tokens
    
    -- Output Data Layer
    output_data TEXT,                              -- JSON: {output_text, results, analysis}
    output_tokens INTEGER DEFAULT 0,              -- Number of output tokens
    
    -- Performance Layer
    processing_time_ms INTEGER DEFAULT 0,          -- Processing time in milliseconds
    api_cost_usd REAL DEFAULT 0.0,                 -- API cost in USD
    
    -- Quality Assessment Layer
    confidence_score REAL DEFAULT 0.0,             -- AI confidence in output
    quality_rating TEXT DEFAULT 'unknown',        -- 'excellent', 'good', 'fair', 'poor'
    
    -- Error Handling Layer
    error_code TEXT,                               -- Error code if any
    error_message TEXT,                            -- Error message if any
    retry_count INTEGER DEFAULT 0,                -- Number of retries
    
    -- Related Data Layer
    lead_id INTEGER,                               -- Reference to leads.id (if applicable)
    session_id TEXT,                               -- Processing session ID
    
    -- Metadata Layer
    metadata TEXT,                                 -- JSON: {model_version, parameters, settings}
    
    -- Timestamps
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,   -- Processing timestamp
    
    -- Indexes for Performance
    INDEX idx_ai_model (ai_model),
    INDEX idx_processing_type (processing_type),
    INDEX idx_timestamp (timestamp),
    INDEX idx_confidence_score (confidence_score),
    INDEX idx_lead_id (lead_id),
    
    -- Foreign Key Constraint
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE SET NULL
);
```

## 🎯 **DATABASE LAYER MAPPING TO DASHBOARD PAGES**

### 📊 **Overview Dashboard Page**
```
📊 Overview Dashboard ← Database Sources:
├── 👥 leads TABLE
│   ├── Total Leads: COUNT(*) FROM leads
│   ├── Hot Leads: COUNT(*) WHERE score >= 8
│   ├── New Leads Today: COUNT(*) WHERE DATE(date_found) = DATE('now')
│   └── Active Locations: COUNT(DISTINCT location) FROM leads
│
├── 📊 analytics.db
│   ├── Searches Today: SUM(search_count) WHERE DATE(timestamp) = DATE('now')
│   ├── Conversion Rate: AVG(conversion_rate) WHERE DATE(timestamp) = DATE('now')
│   └── Active Users: COUNT(DISTINCT user_id) WHERE DATE(last_active) = DATE('now')
│
└── 🔔 alerts TABLE
    ├── Critical Alerts: COUNT(*) WHERE alert_priority = 'critical' AND delivery_status = 'pending'
    ├── System Status: CASE WHEN COUNT(*) WHERE level = 'ERROR' > 0 THEN 'Error' ELSE 'Active' END
    └── Last Alert: MAX(created_at) FROM alerts
```

### 👥 **Leads Management Dashboard Page**
```
👥 Leads Dashboard ← Database Sources:
├── 👥 leads TABLE
│   ├── Lead List: SELECT * FROM leads ORDER BY date_found DESC
│   ├── Lead Details: SELECT * FROM leads WHERE id = ?
│   ├── Contact Information: contact_info, phone_number, email_address FROM leads
│   ├── Lead Score: score, elite_score, confidence_level FROM leads
│   └── Lead Status: status, validation_status, intent_category FROM leads
│
├── 🎯 scoring_log TABLE
│   ├── Scoring History: SELECT * FROM scoring_log WHERE lead_id = ?
│   ├── Score Breakdown: traditional_score, high_intent_count, warm_count, cold_count
│   ├── Intent Analysis: intent_category, intent_confidence
│   ├── Entity Extraction: entities_extracted, entity_confidence
│   └── Psychographic Profile: psychographic_profile, value_confidence
│
├── 🔔 alerts TABLE
│   ├── Lead Alerts: SELECT * FROM alerts WHERE lead_id = ?
│   ├── Alert History: delivery_status, response_status, created_at
│   └── Response Tracking: response_required, response_timestamp
│
└── 📝 system_logs TABLE
    ├── Processing Logs: SELECT * FROM system_logs WHERE module = 'lead_hunter'
    └── Error Tracking: message, level, timestamp WHERE level = 'ERROR'
```

### 🧠 **AI Scoring Analytics Dashboard Page**
```
🧠 Scoring Dashboard ← Database Sources:
├── 🎯 scoring_log TABLE
│   ├── Scoring Performance: AVG(score), AVG(confidence_level), AVG(processing_time_ms)
│   ├── Method Comparison: COUNT(*) GROUP BY analysis_type (llm, traditional, advanced)
│   ├── Score Distribution: COUNT(*) GROUP BY score
│   ├── Intent Distribution: COUNT(*) GROUP BY intent_category
│   ├── Entity Extraction Stats: AVG(entity_confidence) GROUP BY analysis_type
│   └── Psychographic Analysis: psychographic_profile, value_confidence
│
├── 👥 leads TABLE
│   ├── High Intent Leads: SELECT * WHERE score >= 8 AND intent_category = 'Transactional'
│   ├── Lead Quality: AVG(data_quality_score), AVG(validation_status)
│   ├── Conversion Tracking: status, validation_status, contact_info
│   └── Behavioral Analysis: behavioral_signals, urgency_score, potential_value
│
├── 🤖 ai_logs TABLE
│   ├── AI Performance: AVG(processing_time_ms), AVG(confidence_score), AVG(api_cost_usd)
│   ├── Model Comparison: COUNT(*) GROUP BY ai_model
│   ├── Processing Types: COUNT(*) GROUP BY processing_type
│   ├── Quality Assessment: quality_rating, confidence_score
│   └── Cost Analysis: SUM(api_cost_usd) GROUP BY ai_model
│
└── 📝 system_logs TABLE
    ├── Scoring Module Logs: SELECT * WHERE module = 'scoring_logic'
    ├── Error Analysis: COUNT(*) WHERE level = 'ERROR' AND module = 'scoring_logic'
    └── Performance Metrics: AVG(execution_time_ms) WHERE module = 'scoring_logic'
```

### 📈 **Market Intelligence Dashboard Page**
```
📈 Market Dashboard ← Database Sources:
├── 📈 market_data TABLE
│   ├── Market Trends: search_type, query, results, market_insights
│   ├── Price Analysis: price_analysis, price_range, average_price
│   ├── Facility Analysis: facility_analysis, schools, hospitals, commercial_centers
│   ├── Competitor Analysis: competitor_analysis, market_share, positioning
│   ├── Intelligence Summary: intelligence_summary, recommendations, confidence_level
│   └── Search Performance: result_count, processing_time_ms, data_sources
│
├── 🏢 competitors TABLE
│   ├── Competitor Landscape: competitor_name, market_position, target_audience
│   ├── Market Share Analysis: market_share, competitive_advantages, competitive_weaknesses
│   ├── Pricing Intelligence: price_range, pricing_strategy, market_position
│   ├── Reputation Analysis: reputation_score, sentiment_analysis, customer_reviews
│   ├── Geographic Distribution: locations, primary_location, facility_density
│   └── Tracking Information: last_scanned, scan_frequency, data_freshness
│
├── 👥 leads TABLE
│   ├── Market Response: COUNT(*) GROUP BY location, lead_type
│   ├── Price Sensitivity: entities_extracted, price_range, budget_range
│   ├── Geographic Interest: location, search_location, intent_category
│   └── Competitive Analysis: competitors mentioned, market gaps identified
│
└── 📝 system_logs TABLE
    ├── Market Intelligence Logs: SELECT * WHERE module = 'market_intelligence'
    ├── Competitor Scout Logs: SELECT * WHERE module = 'competitor_scout'
    └── Performance Metrics: AVG(execution_time_ms) WHERE module IN ('market_intelligence', 'competitor_scout')
```

### 📍 **Geo-Intelligence Dashboard Page**
```
📍 Geo Dashboard ← Database Sources:
├── 📍 geo_data TABLE
│   ├── Area Mapping: area_name, latitude, longitude, radius_meters
│   ├── Demographic Analysis: bps_data, population_density, dominant_age_group, average_income
│   ├── Facility Mapping: schools, hospitals, commercial_centers, transportation
│   ├── Intelligence Scores: facility_density, accessibility_score, market_potential_score
│   ├── Persona Analysis: area_persona, target_audience, primary_needs, marketing_focus
│   ├── Development Intelligence: development_projects, infrastructure_plans, zoning_information
│   └── Strategic Insights: intelligence_summary, strategic_recommendations
│
├── 👥 leads TABLE
│   ├── Geographic Distribution: COUNT(*) GROUP BY location, search_location
│   ├── Area Performance: AVG(score) GROUP BY location, intent_category
│   ├── Facility Impact: correlation between facility_density and lead quality
│   ├── Demographic Correlation: lead characteristics vs area demographics
│   └── Market Potential: high potential areas identification
│
├── 📈 market_data TABLE
│   ├── Location Intelligence: market_insights WHERE search_location = ?
│   ├── Facility Demand: facility_analysis WHERE search_location = ?
│   └── Development Impact: development_projects WHERE area_name = ?
│
└── 📝 system_logs TABLE
    ├── Geo-Mapper Logs: SELECT * WHERE module = 'geo_mapper'
    ├── BPS Integration Logs: SELECT * WHERE message LIKE '%BPS%'
    └── Performance Metrics: AVG(execution_time_ms) WHERE module = 'geo_mapper'
```

### ⚙️ **Settings & Configuration Dashboard Page**
```
⚙️ Settings Dashboard ← Database Sources:
├── 📝 system_logs TABLE
│   ├── System Health: COUNT(*) WHERE level = 'ERROR' GROUP BY module
│   ├── Performance Metrics: AVG(execution_time_ms) GROUP BY module
│   ├── Activity Monitoring: COUNT(*) GROUP BY module, DATE(timestamp)
│   ├── Error Tracking: message, stack_trace, timestamp WHERE level = 'ERROR'
│   └── User Activity: user_id, session_id, ip_address, timestamp
│
├── 🔔 alerts TABLE
│   ├── Alert History: SELECT * ORDER BY created_at DESC
│   ├── Delivery Status: COUNT(*) GROUP BY delivery_status, delivery_channels
│   ├── Response Tracking: response_required, response_status, response_timestamp
│   ├── Alert Types: COUNT(*) GROUP BY alert_type, alert_priority
│   └── Performance Metrics: AVG(processing_time_ms), delivery_attempts
│
├── 🤖 ai_logs TABLE
│   ├── AI Model Performance: COUNT(*) GROUP BY ai_model, processing_type
│   ├── Cost Analysis: SUM(api_cost_usd) GROUP BY ai_model, processing_type
│   ├── Quality Assessment: AVG(confidence_score), quality_rating
│   ├── Error Tracking: error_code, error_message, retry_count
│   └── Usage Statistics: input_tokens, output_tokens, processing_time_ms
│
├── 📊 system.db
│   ├── System Configuration: SELECT * FROM system_config
│   ├── API Keys Management: SELECT * FROM api_keys
│   ├── Scheduled Jobs: SELECT * FROM cron_jobs
│   └── Audit Trail: SELECT * FROM audit_trail ORDER BY timestamp DESC
│
└── 📊 users.db
    ├── User Management: SELECT * FROM users
    ├── Session Management: SELECT * FROM user_sessions
    ├── User Preferences: SELECT * FROM user_preferences
    └── Activity Tracking: SELECT * FROM user_activity
```

## 🎯 **DASHBOARD LAYER ARCHITECTURE**

### 🏗️ **Data Layer Architecture**
```
🎯 Dashboard Data Flow Architecture:
├── 📊 Database Layer (Single Source of Truth)
│   ├── SQLite Database Connections (leads.db, properties.db, users.db, analytics.db, system.db)
│   ├── Connection Pool Management
│   ├── Query Optimization with Indexes
│   └── Data Integrity Constraints
│
├── 🔄 API Layer (Data Access)
│   ├── RESTful API Endpoints (/api/leads, /api/analytics, /api/market, /api/geo)
│   ├── GraphQL Query Interface (Complex Data Relationships)
│   ├── WebSocket Real-time Updates
│   └── Response Caching Strategy
│
├── 📊 Business Logic Layer (Data Processing)
│   ├── Data Aggregation Services
│   ├── Metric Calculation Engines
│   ├── Trend Analysis Algorithms
│   └── Intelligence Processing
│
├── 🎨 Presentation Layer (UI Components)
│   ├── React Components (Cards, Tables, Charts)
│   ├── State Management (Redux/Zustand)
│   ├── Real-time Data Updates
│   └── User Interaction Handlers
│
└── 📱 User Interface Layer (Dashboard Pages)
    ├── Overview Dashboard (Multi-source Aggregation)
    ├── Leads Management (CRUD Operations)
    ├── AI Scoring Analytics (Performance Metrics)
    ├── Market Intelligence (Strategic Insights)
    ├── Geo-Intelligence (Location Analysis)
    └── Settings Configuration (System Management)
```

### 🔄 **Real-time Data Flow**
```
🎯 Real-time Data Flow Architecture:
├── 📊 Database Changes (INSERT, UPDATE, DELETE)
│   ├── Lead Creation/Updates → leads TABLE
│   ├── Scoring Results → scoring_log TABLE
│   ├── Market Intelligence → market_data TABLE
│   ├── Geo Intelligence → geo_data TABLE
│   └── System Events → system_logs TABLE
│
├── 🔄 Change Detection (Database Triggers)
│   ├── PostgreSQL LISTEN/NOTIFY (Future Enhancement)
│   ├── SQLite Change Monitoring (Custom Implementation)
│   ├── Polling-based Detection (Current Implementation)
│   └── Event Stream Processing
│
├── 📡 Real-time Updates (WebSocket)
│   ├── Lead Score Updates → Dashboard Components
│   ├── New Lead Notifications → Alert System
│   ├── Market Intelligence Updates → Charts
│   ├── System Status Updates → Status Indicators
│   └── User Activity Tracking → Analytics
│
├── 🎨 UI State Updates (React)
│   ├── Component State Management
│   ├── Chart Data Refresh
│   ├── Table Data Updates
│   ├── Alert Badge Updates
│   └── Real-time Notifications
│
└── 📱 User Experience (Interactive Dashboard)
    ├── Live Data Visualization
    ├── Real-time Status Indicators
    ├── Interactive Filtering & Sorting
    ├── Dynamic Chart Updates
    └── Responsive Data Display
```

## 🎯 **DATABASE OPTIMIZATION STRATEGY**

### 📊 **Performance Optimization**
```sql
-- Index Strategy for High-Performance Queries
CREATE INDEX idx_leads_composite ON leads(score, date_found, status);
CREATE INDEX idx_scoring_log_composite ON scoring_log(lead_id, timestamp, score);
CREATE INDEX idx_market_data_composite ON market_data(search_type, timestamp, result_count);
CREATE INDEX idx_geo_data_composite ON geo_data(market_potential_score, last_analysis);
CREATE INDEX idx_alerts_composite ON alerts(alert_type, created_at, delivery_status);

-- Partitioning Strategy for Large Tables (Future Enhancement)
CREATE TABLE leads_partitioned (
    LIKE leads INCLUDING ALL
) PARTITION BY RANGE (date_found);

-- Materialized Views for Complex Queries
CREATE MATERIALIZED VIEW mv_lead_summary AS
SELECT 
    COUNT(*) as total_leads,
    COUNT(CASE WHEN score >= 8 THEN 1 END) as hot_leads,
    COUNT(CASE WHEN status = 'new' THEN 1 END) as new_leads,
    AVG(score) as avg_score,
    DATE(date_found) as date
FROM leads 
GROUP BY DATE(date_found);

-- Query Optimization for Dashboard Performance
EXPLAIN QUERY PLAN
SELECT l.*, sl.score, sl.intent_category, md.market_insights
FROM leads l
LEFT JOIN scoring_log sl ON l.id = sl.lead_id
LEFT JOIN market_data md ON l.location = md.search_location
WHERE l.status = 'new'
ORDER BY l.date_found DESC
LIMIT 50;
```

### 🔒 **Data Security & Privacy**
```sql
-- Row-Level Security (Future Enhancement)
CREATE POLICY lead_access_policy ON leads
FOR ALL
USING (user_id = current_user_id());

-- Data Encryption (Sensitive Information)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypted Contact Information
ALTER TABLE leads ADD COLUMN encrypted_contact_info BYTEA;
UPDATE leads SET encrypted_contact_info = pgp_sym_encrypt(contact_info, 'encryption_key');

-- Audit Trail Implementation
CREATE TRIGGER leads_audit_trail
AFTER INSERT OR UPDATE OR DELETE ON leads
FOR EACH ROW
EXECUTE FUNCTION audit_lead_function();

-- Data Retention Policy
CREATE OR REPLACE FUNCTION cleanup_old_data()
RETURNS void AS $$
BEGIN
    DELETE FROM system_logs WHERE timestamp < NOW() - INTERVAL '90 days';
    DELETE FROM ai_logs WHERE timestamp < NOW() - INTERVAL '30 days';
    DELETE FROM alerts WHERE created_at < NOW() - INTERVAL '180 days';
END;
$$ LANGUAGE plpgsql;
```

## 🎯 **SCALABILITY & MAINTENANCE**

### 📈 **Scalability Strategy**
```yaml
Database Scaling:
  Read Replicas: 3 read replicas for dashboard queries
  Write Scaling: Connection pooling with 50 connections
  Sharding Strategy: Geographic sharding by region
  Caching Layer: Redis for frequent query results

Performance Monitoring:
  Query Performance: Track slow queries (>100ms)
  Connection Pooling: Monitor connection utilization
  Index Usage: Analyze index effectiveness
  Memory Usage: Monitor database memory consumption

Backup Strategy:
  Daily Backups: Full database backup at 2 AM
  Incremental Backups: Transaction log backup every hour
  Point-in-Time Recovery: 7-day retention
  Cross-Region Backup: Cloud storage replication
```

### 🔧 **Maintenance Procedures**
```sql
-- Database Maintenance Schedule
-- Daily: VACUUM and ANALYZE
VACUUM ANALYZE leads;
VACUUM ANALYZE scoring_log;
VACUUM ANALYZE market_data;

-- Weekly: Index Rebuilding
REINDEX INDEX idx_leads_composite;
REINDEX INDEX idx_scoring_log_composite;

-- Monthly: Statistics Update
ANALYZE leads;
ANALYZE scoring_log;
ANALYZE market_data;

-- Quarterly: Performance Review
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
GROUP BY schemaname, tablename, attname;
```

---

🎯 **Database Layer Mapping Lengkap ini adalah blueprint lengkap untuk dashboard development dengan database sebagai single source of truth. Setiap dashboard page terhubung langsung ke tabel database spesifik dengan query yang dioptimalkan untuk performance dan real-time updates!**

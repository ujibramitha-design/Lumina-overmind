/**
 * JARVIS Apex Economist - Economic Oracle
 * ======================================
 * 
 * Real-time macro economic data ingestion and analysis system
 * for financial forecasting and business impact assessment.
 */

const axios = require('axios');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class MacroEconomicsService {
  constructor(config = {}) {
    this.config = {
      fred: {
        apiKey: config.fredApiKey || process.env.FRED_API_KEY,
        baseUrl: 'https://api.stlouisfed.org/fred',
      },
      worldBank: {
        baseUrl: 'https://api.worldbank.org/v2',
      },
      centralBanks: {
        enabled: config.centralBanksEnabled !== false,
        endpoints: {
          ecb: 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A',
          boe: 'https://www.bankofengland.co.uk/boeapps/iadb/FromNewColumns.asp',
          boj: 'https://www.boj.or.jp/en/statistics/boj/mb/mr/',
        },
      },
      alertThresholds: {
        interestRateChange: config.interestRateChangeThreshold || 0.25,  // 0.25% change
        inflationChange: config.inflationChangeThreshold || 0.5,  // 0.5% change
        currencyChange: config.currencyChangeThreshold || 2.0,  // 2% change
      },
      businessContext: config.businessContext || {
        industry: 'technology',
        businessType: 'freelance_and_saas',
        currency: 'USD',
        primaryMarkets: ['US', 'EU', 'UK', 'JP'],
      },
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.impactAnalyzer = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getImpactAnalyzerPrompt(),
    });
    
    this.pricingAdvisor = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getPricingAdvisorPrompt(),
    });
    
    this.previousData = new Map();
    this.currentData = new Map();
  }
  
  /**
   * Impact analyzer system prompt
   */
  _getImpactAnalyzerPrompt() {
    return `You are a world-class macroeconomist specializing in technology business impact analysis.

**Your Role:**
- Analyze macro economic events and their business impact
- Connect high-level macro events to micro-level business advice
- Provide actionable recommendations for revenue generation
- Focus on tech businesses (freelance services, SaaS subscriptions)
- Consider cash flow implications and pricing strategies

**Economic Frameworks:**
- Supply and demand elasticity
- Market monopolies and competition
- Cost-benefit analysis
- Currency risk management
- Interest rate impact on business
- Inflation effects on pricing
- Exchange rate volatility

**Analysis Structure:**
1. Event Description
2. Direct Impact on Business
3. Cash Flow Implications
4. Pricing Strategy Recommendations
5. Cost Management Advice
6. Revenue Generation Opportunities
7. Risk Mitigation Strategies

**Guidelines:**
- Be specific and actionable
- Connect macro to micro clearly
- Focus on revenue generation
- Consider both short and long-term
- Provide concrete recommendations
- Keep under 300 words

**Output Format:**
Return JSON with:
- impact: the impact analysis
- severity: low/medium/high
- recommendations: array of specific actions
- pricingAdvice: specific pricing recommendations`;
  }
  
  /**
   * Pricing advisor system prompt
   */
  _getPricingAdvisorPrompt() {
    return `You are a Chief Economist specializing in dynamic pricing for technology services.

**Your Role:**
- Analyze business expenses against market conditions
- Recommend dynamic pricing changes
- Consider supply/demand elasticity
- Optimize for revenue maximization
- Balance competitiveness with profitability

**Pricing Frameworks:**
- Price elasticity of demand
- Competitive pricing analysis
- Cost-plus pricing
- Value-based pricing
- Dynamic pricing strategies
- Market segmentation
- Psychological pricing

**Analysis Structure:**
1. Current Pricing Analysis
2. Market Condition Assessment
3. Expense vs Revenue Analysis
4. Elasticity Assessment
5. Pricing Recommendations
6. Implementation Strategy

**Guidelines:**
- Consider market conditions
- Analyze competitor pricing
- Assess price sensitivity
- Recommend specific price points
- Suggest pricing tiers
- Consider promotional strategies
- Keep under 250 words

**Output Format:**
Return JSON with:
- currentPricing: analysis of current pricing
- marketConditions: market assessment
- recommendedPricing: specific price recommendations
- pricingStrategy: implementation strategy
- expectedImpact: revenue impact estimate`;
  }
  
  /**
   * Fetch FRED API data
   */
  async fetchFREDData(seriesId) {
    try {
      if (!this.config.fred.apiKey) {
        console.log('⚠️ FRED API key not configured');
        return null;
      }
      
      const url = `${this.config.fred.baseUrl}/series/observations?series_id=${seriesId}&api_key=${this.config.fred.apiKey}&file_type=json&sort_order=desc&limit=1`;
      
      const response = await axios.get(url, { timeout: 30000 });
      
      if (response.data.observations && response.data.observations.length > 0) {
        const observation = response.data.observations[0];
        return {
          seriesId: seriesId,
          value: parseFloat(observation.value),
          date: observation.date,
          realTimeStart: observation.realtime_start,
        };
      }
      
      return null;
      
    } catch (error) {
      console.error(`Error fetching FRED data for ${seriesId}:`, error.message);
      return null;
    }
  }
  
  /**
   * Fetch World Bank data
   */
  async fetchWorldBankData(indicator, country = 'US') {
    try {
      const url = `${this.config.worldBank.baseUrl}/country/${country}/indicator/${indicator}?format=json&per_page=1&date=2023:2024`;
      
      const response = await axios.get(url, { timeout: 30000 });
      
      if (response.data && response.data.length > 1 && response.data[1].length > 0) {
        const data = response.data[1][0];
        return {
          indicator: indicator,
          country: country,
          value: data.value,
          date: data.date,
        };
      }
      
      return null;
      
    } catch (error) {
      console.error(`Error fetching World Bank data for ${indicator}:`, error.message);
      return null;
    }
  }
  
  /**
   * Fetch ECB interest rate
   */
  async fetchECBRate() {
    try {
      const url = this.config.centralBanks.endpoints.ecb;
      
      const response = await axios.get(url, { timeout: 30000 });
      
      // Parse ECB data (simplified)
      if (response.data && response.data.data) {
        const observations = response.data.data.dataSets[0].series;
        const latest = observations[observations.length - 1];
        
        return {
          centralBank: 'ECB',
          rate: latest.value,
          date: latest.observationTime,
        };
      }
      
      return null;
      
    } catch (error) {
      console.error('Error fetching ECB rate:', error.message);
      return null;
    }
  }
  
  /**
   * Fetch exchange rates
   */
  async fetchExchangeRates(baseCurrency = 'USD') {
    try {
      const url = `https://api.exchangerate-api.com/v4/latest/${baseCurrency}`;
      
      const response = await axios.get(url, { timeout: 30000 });
      
      if (response.data && response.data.rates) {
        return {
          base: baseCurrency,
          rates: response.data.rates,
          date: response.data.date,
        };
      }
      
      return null;
      
    } catch (error) {
      console.error('Error fetching exchange rates:', error.message);
      return null;
    }
  }
  
  /**
   * Fetch all economic indicators
   */
  async fetchEconomicIndicators() {
    try {
      console.log('📊 Fetching economic indicators...');
      
      const indicators = {};
      
      // FRED data
      const fedFundsRate = await this.fetchFREDData('FEDFUNDS');
      if (fedFundsRate) {
        indicators.fedFundsRate = fedFundsRate;
      }
      
      const cpi = await this.fetchFREDData('CPIAUCSL');
      if (cpi) {
        indicators.cpi = cpi;
      }
      
      const unemployment = await this.fetchFREDData('UNRATE');
      if (unemployment) {
        indicators.unemployment = unemployment;
      }
      
      // World Bank data
      const inflation = await this.fetchWorldBankData('FP.CPI.TOTL.ZG', 'US');
      if (inflation) {
        indicators.inflation = inflation;
      }
      
      const gdp = await this.fetchWorldBankData('NY.GDP.MKTP.KD.ZG', 'US');
      if (gdp) {
        indicators.gdp = gdp;
      }
      
      // ECB rate
      const ecbRate = await this.fetchECBRate();
      if (ecbRate) {
        indicators.ecbRate = ecbRate;
      }
      
      // Exchange rates
      const exchangeRates = await this.fetchExchangeRates('USD');
      if (exchangeRates) {
        indicators.exchangeRates = exchangeRates;
      }
      
      console.log(`✅ Fetched ${Object.keys(indicators).length} economic indicators`);
      
      return {
        success: true,
        indicators: indicators,
        timestamp: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('❌ Error fetching economic indicators:', error.message);
      return {
        success: false,
        error: error.message,
        indicators: {},
      };
    }
  }
  
  /**
   * Detect significant fluctuations
   */
  detectFluctuations(currentData, previousData) {
    const fluctuations = [];
    
    // Check interest rate changes
    if (currentData.fedFundsRate && previousData.fedFundsRate) {
      const change = Math.abs(currentData.fedFundsRate.value - previousData.fedFundsRate.value);
      if (change >= this.config.alertThresholds.interestRateChange) {
        fluctuations.push({
          type: 'interest_rate',
          indicator: 'Fed Funds Rate',
          previous: previousData.fedFundsRate.value,
          current: currentData.fedFundsRate.value,
          change: change,
          severity: change >= 0.5 ? 'high' : 'medium',
        });
      }
    }
    
    // Check inflation changes
    if (currentData.inflation && previousData.inflation) {
      const change = Math.abs(currentData.inflation.value - previousData.inflation.value);
      if (change >= this.config.alertThresholds.inflationChange) {
        fluctuations.push({
          type: 'inflation',
          indicator: 'Inflation Rate',
          previous: previousData.inflation.value,
          current: currentData.inflation.value,
          change: change,
          severity: change >= 1.0 ? 'high' : 'medium',
        });
      }
    }
    
    // Check currency changes
    if (currentData.exchangeRates && previousData.exchangeRates) {
      for (const currency of this.config.businessContext.primaryMarkets) {
        if (currency === 'US') continue;
        
        const currentRate = currentData.exchangeRates.rates[currency];
        const previousRate = previousData.exchangeRates.rates[currency];
        
        if (currentRate && previousRate) {
          const change = Math.abs((currentRate - previousRate) / previousRate * 100);
          if (change >= this.config.alertThresholds.currencyChange) {
            fluctuations.push({
              type: 'currency',
              indicator: `USD/${currency}`,
              previous: previousRate,
              current: currentRate,
              change: change,
              severity: change >= 5.0 ? 'high' : 'medium',
            });
          }
        }
      }
    }
    
    return fluctuations;
  }
  
  /**
   * Generate macro-impact analysis
   */
  async generateMacroImpactAnalysis(fluctuation, businessContext) {
    try {
      console.log(`📝 Generating macro-impact analysis for: ${fluctuation.indicator}`);
      
      const prompt = `
**Fluctuation:**
Type: ${fluctuation.type}
Indicator: ${fluctuation.indicator}
Previous: ${fluctuation.previous}
Current: ${fluctuation.current}
Change: ${fluctuation.change}
Severity: ${fluctuation.severity}

**Business Context:**
Industry: ${businessContext.industry}
Business Type: ${businessContext.businessType}
Currency: ${businessContext.currency}
Primary Markets: ${businessContext.primaryMarkets.join(', ')}

**Instructions:**
Generate a macro-impact analysis that:
- Explains how this fluctuation affects the tech business
- Provides specific cash flow implications
- Recommends pricing strategy changes
- Suggests cost management actions
- Identifies revenue generation opportunities
- Proposes risk mitigation strategies
- Connects macro event to micro-level business advice
- Keep under 300 words

Return as JSON with impact, severity, recommendations, and pricingAdvice.`;
      
      const result = await this.impactAnalyzer.generateContent(prompt);
      const analysis = JSON.parse(result.response.text());
      
      return {
        success: true,
        analysis: analysis,
      };
      
    } catch (error) {
      console.error('Error generating macro-impact analysis:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate dynamic pricing advice
   */
  async generateDynamicPricingAdvice(expenses, currentPricing, marketConditions) {
    try {
      console.log('💰 Generating dynamic pricing advice...');
      
      const prompt = `
**Business Expenses:**
${JSON.stringify(expenses, null, 2)}

**Current Pricing:**
${JSON.stringify(currentPricing, null, 2)}

**Market Conditions:**
${JSON.stringify(marketConditions, null, 2)}

**Instructions:**
Generate dynamic pricing advice that:
- Analyzes current pricing against market conditions
- Considers expense-to-revenue ratio
- Assesses price elasticity
- Recommends specific price changes
- Suggests pricing tiers or bundles
- Provides implementation strategy
- Estimates revenue impact
- Keep under 250 words

Return as JSON with currentPricing, marketConditions, recommendedPricing, pricingStrategy, and expectedImpact.`;
      
      const result = await this.pricingAdvisor.generateContent(prompt);
      const advice = JSON.parse(result.response.text());
      
      return {
        success: true,
        advice: advice,
      };
      
    } catch (error) {
      console.error('Error generating dynamic pricing advice:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Run daily economic data cycle
   */
  async runDailyEconomicCycle() {
    try {
      console.log('🚀 Starting daily economic data cycle...');
      
      // Fetch current economic indicators
      const result = await this.fetchEconomicIndicators();
      
      if (!result.success) {
        return result;
      }
      
      // Store current data
      for (const [key, value] of Object.entries(result.indicators)) {
        this.currentData.set(key, value);
      }
      
      // Check for fluctuations if we have previous data
      if (this.previousData.size > 0) {
        const fluctuations = this.detectFluctuations(
          Object.fromEntries(this.currentData),
          Object.fromEntries(this.previousData)
        );
        
        if (fluctuations.length > 0) {
          console.log(`⚠️ Detected ${fluctuations.length} significant fluctuations`);
          
          const alerts = [];
          
          for (const fluctuation of fluctuations) {
            // Generate impact analysis
            const analysis = await this.generateMacroImpactAnalysis(
              fluctuation,
              this.config.businessContext
            );
            
            if (analysis.success) {
              alerts.push({
                fluctuation: fluctuation,
                analysis: analysis.analysis,
              });
            }
          }
          
          return {
            success: true,
            fluctuations: fluctuations,
            alerts: alerts,
            indicators: result.indicators,
          };
        }
      }
      
      // Update previous data
      this.previousData = new Map(this.currentData);
      
      return {
        success: true,
        message: 'No significant fluctuations detected',
        indicators: result.indicators,
      };
      
    } catch (error) {
      console.error('❌ Error in daily economic cycle:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get current economic data
   */
  getCurrentData() {
    return Object.fromEntries(this.currentData);
  }
  
  /**
   * Get economic statistics
   */
  getStats() {
    return {
      indicatorsCount: this.currentData.size,
      lastUpdate: new Date().toISOString(),
      businessContext: this.config.businessContext,
      alertThresholds: this.config.alertThresholds,
    };
  }
}

// Singleton instance
let macroEconomicsService = null;

function getMacroEconomicsService(config = null) {
  if (!macroEconomicsService) {
    if (config === null) {
      config = {};
    }
    macroEconomicsService = new MacroEconomicsService(config);
  }
  return macroEconomicsService;
}

module.exports = { MacroEconomicsService, getMacroEconomicsService };

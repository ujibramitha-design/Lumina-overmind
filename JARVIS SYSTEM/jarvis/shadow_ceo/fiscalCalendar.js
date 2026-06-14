/**
 * JARVIS Fiscal Calendar & Timing Analysis
 * =====================================
 * 
 * Fiscal calendar cross-reference and contract timing analysis
 * for optimal deal timing and negotiation leverage.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class FiscalCalendar {
  constructor(config = {}) {
    this.config = {
      fiscalYears: config.fiscalYears || {
        default: 'january',  // January-December
        tech: 'october',     // October-September (common in tech)
        retail: 'february',  // February-January
        government: 'october',  // October-September
      },
      quarters: {
        Q1: { months: [1, 2, 3], name: 'First Quarter' },
        Q2: { months: [4, 5, 6], name: 'Second Quarter' },
        Q3: { months: [7, 8, 9], name: 'Third Quarter' },
        Q4: { months: [10, 11, 12], name: 'Fourth Quarter' },
      },
      budgetCycles: {
        planning: { quarter: 'Q4', months: [10, 11, 12], description: 'Budget planning season' },
        approval: { quarter: 'Q1', months: [1, 2], description: 'Budget approval season' },
        execution: { quarter: 'Q2', months: [4, 5, 6], description: 'Budget execution season' },
        review: { quarter: 'Q3', months: [7, 8, 9], description: 'Budget review season' },
      },
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.timingAnalyzer = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getTimingAnalyzerPrompt(),
    });
  }
  
  /**
   * Timing analyzer system prompt
   */
  _getTimingAnalyzerPrompt() {
    return `You are a Timing Oracle and Contract Strategy Expert specializing in fiscal calendar analysis.

**Your Role:**
- Analyze contract timing and fiscal calendar alignment
- Cross-reference contract dates with client budget cycles
- Assess market conditions for optimal signing timing
- Identify leverage points based on timing
- Recommend sign-hold-walk decisions
- Consider seasonal business patterns
- Evaluate client financial health implications
- Provide timing-based negotiation leverage

**Fiscal Calendar Frameworks:**
- Budget Planning Season (Q4): Companies plan next year's budget
- Budget Approval Season (Q1): Budgets are approved and finalized
- Budget Execution Season (Q2): Budget execution begins
- Budget Review Season (Q3): Mid-year budget reviews

**Timing Analysis Structure:**
1. Contract Date Analysis
2. Fiscal Calendar Alignment
3. Budget Cycle Position
4. Market Conditions
5. Leverage Assessment
6. Sign-Hold-Walk Recommendation
7. Negotiation Strategy
8. Expected Impact

**Guidelines:**
- Consider industry-specific fiscal years
- Assess budget cycle timing
- Evaluate market conditions
- Identify leverage points
- Provide clear recommendation
- Consider seasonal patterns
- Focus on maximizing deal value
- Keep under 300 words

**Output Format:**
Return JSON with:
- timingAnalysis: timing assessment
- budgetCycle: current budget cycle
- leverage: leverage points
- recommendation: sign/hold/walk
- strategy: negotiation strategy
- expectedImpact: impact on deal value`;
  }
  
  /**
   * Get current fiscal quarter
   */
  getCurrentFiscalQuarter(fiscalYearStart = 'january') {
    const now = new Date();
    const currentMonth = now.getMonth() + 1;  // 1-12
    
    const fiscalMonthMap = {
      january: 1,
      february: 2,
      october: 10,
    };
    
    const startMonth = fiscalMonthMap[fiscalYearStart] || 1;
    
    let fiscalMonth = currentMonth - startMonth + 1;
    if (fiscalMonth <= 0) {
      fiscalMonth += 12;
    }
    
    let quarter;
    if (fiscalMonth <= 3) {
      quarter = 'Q1';
    } else if (fiscalMonth <= 6) {
      quarter = 'Q2';
    } else if (fiscalMonth <= 9) {
      quarter = 'Q3';
    } else {
      quarter = 'Q4';
    }
    
    return {
      quarter: quarter,
      fiscalMonth: fiscalMonth,
      calendarMonth: currentMonth,
      fiscalYearStart: fiscalYearStart,
    };
  }
  
  /**
   * Get budget cycle for company
   */
  getBudgetCycle(companyType = 'default') {
    const fiscalYearStart = this.config.fiscalYears[companyType] || this.config.fiscalYears.default;
    const currentFiscal = this.getCurrentFiscalQuarter(fiscalYearStart);
    
    // Determine budget cycle based on fiscal quarter
    let cycle;
    if (currentFiscal.quarter === 'Q4') {
      cycle = this.config.budgetCycles.planning;
    } else if (currentFiscal.quarter === 'Q1') {
      cycle = this.config.budgetCycles.approval;
    } else if (currentFiscal.quarter === 'Q2') {
      cycle = this.config.budgetCycles.execution;
    } else {
      cycle = this.config.budgetCycles.review;
    }
    
    return {
      currentCycle: cycle,
      fiscalQuarter: currentFiscal,
      companyType: companyType,
    };
  }
  
  /**
   * Analyze contract timing
   */
  async analyzeContractTiming(contractDetails, clientCompany, contractDate = null) {
    try {
      console.log('📅 Analyzing contract timing...');
      
      const dateToAnalyze = contractDate ? new Date(contractDate) : new Date();
      const companyType = this._inferCompanyType(clientCompany);
      const budgetCycle = this.getBudgetCycle(companyType);
      
      const prompt = `
**Contract Details:**
${contractDetails}

**Client Company:**
${clientCompany}
Company Type: ${companyType}

**Contract Date:**
${dateToAnalyze.toISOString()}

**Current Budget Cycle:**
Cycle: ${budgetCycle.currentCycle.description}
Quarter: ${budgetCycle.currentCycle.quarter}
Months: ${budgetCycle.currentCycle.months.join(', ')}

**Instructions:**
Analyze the contract timing and provide:
- Timing analysis (favorable/unfavorable/neutral)
- Budget cycle position
- Leverage points based on timing
- Sign-hold-walk recommendation
- Negotiation strategy
- Expected impact on deal value
- Consider seasonal business patterns
- Assess market conditions

Return as JSON with timingAnalysis, budgetCycle, leverage, recommendation, strategy, and expectedImpact.`;
      
      const result = await this.timingAnalyzer.generateContent(prompt);
      const analysis = JSON.parse(result.response.text());
      
      console.log('✅ Contract timing analysis complete');
      
      return {
        success: true,
        analysis: analysis,
        budgetCycle: budgetCycle,
        contractDate: dateToAnalyze,
      };
      
    } catch (error) {
      console.error('❌ Error analyzing contract timing:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Infer company type from company name or context
   */
  _inferCompanyType(company) {
    const companyLower = company.toLowerCase();
    
    if (companyLower.includes('tech') || companyLower.includes('software') || companyLower.includes('saas')) {
      return 'tech';
    } else if (companyLower.includes('retail') || companyLower.includes('ecommerce') || companyLower.includes('store')) {
      return 'retail';
    } else if (companyLower.includes('government') || companyLower.includes('agency') || companyLower.includes('public')) {
      return 'government';
    }
    
    return 'default';
  }
  
  /**
   * Get optimal signing window
   */
  getOptimalSigningWindow(companyType = 'default') {
    const budgetCycle = this.getBudgetCycle(companyType);
    
    // Optimal windows are typically:
    // - Q1 (Jan-Feb): Budget approval season - high leverage
    // - Q4 (Oct-Dec): Budget planning season - moderate leverage
    // - Q2 (Apr-Jun): Budget execution season - low leverage
    // - Q3 (Jul-Sep): Budget review season - moderate leverage
    
    let optimalWindow;
    let leverage;
    
    if (budgetCycle.currentCycle.quarter === 'Q1') {
      optimalWindow = 'HIGH - Budget approval season';
      leverage = 'high';
    } else if (budgetCycle.currentCycle.quarter === 'Q4') {
      optimalWindow = 'MODERATE - Budget planning season';
      leverage = 'moderate';
    } else if (budgetCycle.currentCycle.quarter === 'Q3') {
      optimalWindow = 'MODERATE - Budget review season';
      leverage = 'moderate';
    } else {
      optimalWindow = 'LOW - Budget execution season';
      leverage = 'low';
    }
    
    return {
      optimalWindow: optimalWindow,
      leverage: leverage,
      currentCycle: budgetCycle.currentCycle.description,
      recommendation: leverage === 'high' ? 'Sign now' : leverage === 'moderate' ? 'Consider signing' : 'Hold for better timing',
    };
  }
  
  /**
   * Get fiscal calendar statistics
   */
  getStats() {
    const currentFiscal = this.getCurrentFiscalQuarter();
    const budgetCycle = this.getBudgetCycle();
    
    return {
      currentQuarter: currentFiscal.quarter,
      currentMonth: currentFiscal.calendarMonth,
      fiscalMonth: currentFiscal.fiscalMonth,
      budgetCycle: budgetCycle.currentCycle.description,
      fiscalYearStart: currentFiscal.fiscalYearStart,
    };
  }
}

// Singleton instance
let fiscalCalendar = null;

function getFiscalCalendar(config = null) {
  if (!fiscalCalendar) {
    if (config === null) {
      config = {};
    }
    fiscalCalendar = new FiscalCalendar(config);
  }
  return fiscalCalendar;
}

module.exports = { FiscalCalendar, getFiscalCalendar };

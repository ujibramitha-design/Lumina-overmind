/**
 * JARVIS Autonomous Scraper Agent
 * ==============================
 * 
 * Web scraping module using Playwright for autonomous data extraction.
 * Handles anti-bot protections, headless browsing, and data export.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class ScraperAgent {
  constructor(config = {}) {
    this.config = {
      headless: config.headless !== false,
      timeout: config.timeout || 30000,
      userAgent: config.userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: config.viewport || { width: 1920, height: 1080 },
      outputDir: config.outputDir || './jarvis/revenue/scraped_data',
      antiBot: {
        enabled: config.antiBotEnabled !== false,
        randomDelay: config.randomDelay || true,
        minDelay: config.minDelay || 1000,
        maxDelay: config.maxDelay || 3000,
        mouseMovements: config.mouseMovements !== false,
        randomScroll: config.randomScroll !== false,
      },
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.scriptGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getScriptGeneratorPrompt(),
    });
    
    this.browser = null;
    this.context = null;
  }
  
  /**
   * Script generator system prompt
   */
  _getScriptGeneratorPrompt() {
    return `You are an expert web scraping script generator. Your role is to write Playwright scraping scripts based on user requirements.

**Your Capabilities:**
- Analyze website structure from description
- Generate Playwright code for data extraction
- Handle dynamic content and JavaScript
- Implement selectors (CSS, XPath, text)
- Add error handling and retries
- Implement anti-bot detection evasion
- Export data to CSV/JSON

**Script Structure:**
1. Browser setup with anti-bot measures
2. Page navigation with delays
3. Data extraction with selectors
4. Error handling and retries
5. Data export to specified format

**Anti-Bot Measures:**
- Random delays between actions
- Mouse movements
- Random scrolling
- User-agent rotation
- Cookie handling
- Headless detection avoidance

**Output Format:**
Return valid JavaScript code that can be executed with Playwright.
Include comments explaining each step.
Handle all common errors.`;
  }
  
  /**
   * Initialize browser
   */
  async initializeBrowser() {
    try {
      this.browser = await chromium.launch({
        headless: this.config.headless,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-blink-features=AutomationControlled',
        ],
      });
      
      this.context = await this.browser.newContext({
        userAgent: this.config.userAgent,
        viewport: this.config.viewport,
        locale: 'en-US',
        timezoneId: 'America/New_York',
        permissions: ['geolocation'],
        geolocation: { latitude: 40.7128, longitude: -74.0060 },  // NYC
      });
      
      // Add stealth measures
      await this.context.addInitScript(() => {
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined,
        });
        
        Object.defineProperty(navigator, 'plugins', {
          get: () => [1, 2, 3, 4, 5],
        });
        
        Object.defineProperty(navigator, 'languages', {
          get: () => ['en-US', 'en'],
        });
      });
      
      console.log('✅ Browser initialized with anti-bot measures');
      
      return true;
    } catch (error) {
      console.error('❌ Error initializing browser:', error.message);
      return false;
    }
  }
  
  /**
   * Generate scraping script
   */
  async generateScrapingScript(target, description) {
    try {
      console.log(`📝 Generating scraping script for: ${target}`);
      
      const prompt = `
**Target:** ${target}
**Description:** ${description}

**Instructions:**
Generate a Playwright scraping script to extract the requested data.
Include:
- Browser setup with anti-bot measures
- Page navigation
- Data extraction with appropriate selectors
- Error handling
- Data export to JSON format

Return only the JavaScript code, no explanations.`;
      
      const result = await this.scriptGenerator.generateContent(prompt);
      const script = result.response.text();
      
      // Extract code from response
      const codeMatch = script.match(/```(?:javascript|js)?\n([\s\S]*?)```/);
      const code = codeMatch ? codeMatch[1] : script;
      
      return {
        success: true,
        script: code,
      };
      
    } catch (error) {
      console.error('❌ Error generating scraping script:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Execute scraping script
   */
  async executeScrapingScript(script, url) {
    try {
      if (!this.browser) {
        await this.initializeBrowser();
      }
      
      const page = await this.context.newPage();
      
      // Add anti-bot measures to page
      await this._addAntiBotMeasures(page);
      
      // Navigate to URL
      console.log(`🌐 Navigating to: ${url}`);
      await page.goto(url, {
        waitUntil: 'networkidle',
        timeout: this.config.timeout,
      });
      
      // Random delay
      if (this.config.antiBot.randomDelay) {
        await this._randomDelay();
      }
      
      // Execute script
      console.log('🔄 Executing scraping script...');
      const data = await page.evaluate(script);
      
      await page.close();
      
      console.log(`✅ Scraping complete. Extracted ${Array.isArray(data) ? data.length : 1} items`);
      
      return {
        success: true,
        data: data,
      };
      
    } catch (error) {
      console.error('❌ Error executing scraping script:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Add anti-bot measures to page
   */
  async _addAntiBotMeasures(page) {
    try {
      // Random mouse movements
      if (this.config.antiBot.mouseMovements) {
        await this._simulateMouseMovements(page);
      }
      
      // Random scrolling
      if (this.config.antiBot.randomScroll) {
        await this._simulateScrolling(page);
      }
      
    } catch (error) {
      console.error('Error adding anti-bot measures:', error.message);
    }
  }
  
  /**
   * Simulate mouse movements
   */
  async _simulateMouseMovements(page) {
    try {
      const viewport = page.viewportSize();
      const movements = Math.floor(Math.random() * 5) + 3;
      
      for (let i = 0; i < movements; i++) {
        const x = Math.random() * viewport.width;
        const y = Math.random() * viewport.height;
        
        await page.mouse.move(x, y);
        await this._randomDelay(100, 500);
      }
    } catch (error) {
      console.error('Error simulating mouse movements:', error.message);
    }
  }
  
  /**
   * Simulate scrolling
   */
  async _simulateScrolling(page) {
    try {
      const scrollCount = Math.floor(Math.random() * 3) + 1;
      
      for (let i = 0; i < scrollCount; i++) {
        const scrollY = Math.random() * 500;
        await page.evaluate((y) => window.scrollBy(0, y), scrollY);
        await this._randomDelay(500, 1500);
      }
      
      // Scroll back to top
      await page.evaluate(() => window.scrollTo(0, 0));
    } catch (error) {
      console.error('Error simulating scrolling:', error.message);
    }
  }
  
  /**
   * Random delay
   */
  async _randomDelay(min = null, max = null) {
    const minDelay = min || this.config.antiBot.minDelay;
    const maxDelay = max || this.config.antiBot.maxDelay;
    const delay = Math.random() * (maxDelay - minDelay) + minDelay;
    
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  /**
   * Export data to file
   */
  async exportData(data, filename, format = 'json') {
    try {
      const dir = this.config.outputDir;
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      const filepath = path.join(dir, filename);
      
      if (format === 'json') {
        fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
      } else if (format === 'csv') {
        const csv = this._convertToCSV(data);
        fs.writeFileSync(filepath, csv);
      }
      
      console.log(`💾 Data exported to: ${filepath}`);
      
      return {
        success: true,
        filepath: filepath,
      };
      
    } catch (error) {
      console.error('❌ Error exporting data:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Convert data to CSV
   */
  _convertToCSV(data) {
    if (!Array.isArray(data) || data.length === 0) {
      return '';
    }
    
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];
    
    for (const row of data) {
      const values = headers.map(header => {
        const value = row[header];
        const escaped = String(value).replace(/"/g, '""');
        return `"${escaped}"`;
      });
      csvRows.push(values.join(','));
    }
    
    return csvRows.join('\n');
  }
  
  /**
   * Autonomous scraping workflow
   */
  async autonomousScrape(target, description, url, outputFormat = 'json') {
    try {
      console.log(`🚀 Starting autonomous scrape: ${target}`);
      
      // Generate scraping script
      const scriptResult = await this.generateScrapingScript(target, description);
      if (!scriptResult.success) {
        return scriptResult;
      }
      
      // Execute scraping script
      const scrapeResult = await this.executeScrapingScript(scriptResult.script, url);
      if (!scrapeResult.success) {
        return scrapeResult;
      }
      
      // Export data
      const filename = `${target.replace(/\s+/g, '_')}_${Date.now()}.${outputFormat}`;
      const exportResult = await this.exportData(scrapeResult.data, filename, outputFormat);
      
      return {
        success: true,
        data: scrapeResult.data,
        filepath: exportResult.filepath,
        itemCount: Array.isArray(scrapeResult.data) ? scrapeResult.data.length : 1,
      };
      
    } catch (error) {
      console.error('❌ Error in autonomous scrape:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Handle common anti-bot mechanisms
   */
  async handleAntiBotMechanisms(page) {
    try {
      // Check for CAPTCHA
      const captcha = await page.$('[class*="captcha"], [id*="captcha"]');
      if (captcha) {
        console.log('⚠️ CAPTCHA detected. Manual intervention required.');
        return { detected: 'captcha', action: 'manual' };
      }
      
      // Check for rate limiting
      const rateLimit = await page.$('[class*="rate-limit"], [class*="blocked"]');
      if (rateLimit) {
        console.log('⚠️ Rate limit detected. Waiting...');
        await this._randomDelay(10000, 30000);  // Wait 10-30 seconds
        return { detected: 'rate_limit', action: 'waited' };
      }
      
      // Check for login requirement
      const login = await page.$('[class*="login"], [class*="signin"]');
      if (login) {
        console.log('⚠️ Login required.');
        return { detected: 'login', action: 'manual' };
      }
      
      return { detected: null };
      
    } catch (error) {
      console.error('Error checking anti-bot mechanisms:', error.message);
      return { detected: null };
    }
  }
  
  /**
   * Run Lighthouse audit on website
   */
  async runLighthouseAudit(url) {
    try {
      console.log(`🔍 Running Lighthouse audit on: ${url}`);
      
      if (!this.browser) {
        await this.initializeBrowser();
      }
      
      const page = await this.context.newPage();
      
      // Navigate to URL
      await page.goto(url, {
        waitUntil: 'networkidle',
        timeout: this.config.timeout,
      });
      
      // Run basic performance checks (simplified Lighthouse-like audit)
      const auditResults = await this._runBasicAudit(page);
      
      await page.close();
      
      console.log('✅ Lighthouse audit complete');
      
      return {
        success: true,
        url: url,
        auditResults: auditResults,
      };
      
    } catch (error) {
      console.error('❌ Error running Lighthouse audit:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Run basic performance audit
   */
  async _runBasicAudit(page) {
    try {
      const metrics = await page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0];
        
        return {
          // Performance metrics
          loadTime: navigation.loadEventEnd - navigation.fetchStart,
          domContentLoaded: navigation.domContentLoadedEventEnd - navigation.fetchStart,
          firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
          firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0,
          
          // Resource counts
          resourceCount: performance.getEntriesByType('resource').length,
          
          // Page info
          title: document.title,
          viewport: {
            width: window.innerWidth,
            height: window.innerHeight,
          },
          
          // Basic SEO checks
          hasMetaDescription: !!document.querySelector('meta[name="description"]'),
          hasH1: !!document.querySelector('h1'),
          hasAltText: Array.from(document.querySelectorAll('img')).filter(img => img.alt).length,
          totalImages: document.querySelectorAll('img').length,
          
          // Security checks
          usesHTTPS: window.location.protocol === 'https:',
          hasMixedContent: document.querySelectorAll('img[src^="http://"]').length > 0,
        };
      });
      
      // Calculate scores
      const scores = {
        performance: this._calculatePerformanceScore(metrics),
        seo: this._calculateSEOScore(metrics),
        security: this._calculateSecurityScore(metrics),
        accessibility: this._calculateAccessibilityScore(metrics),
      };
      
      // Generate recommendations
      const recommendations = this._generateRecommendations(metrics, scores);
      
      return {
        metrics: metrics,
        scores: scores,
        recommendations: recommendations,
        timestamp: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('Error running basic audit:', error.message);
      return {
        metrics: {},
        scores: {},
        recommendations: [],
        error: error.message,
      };
    }
  }
  
  /**
   * Calculate performance score
   */
  _calculatePerformanceScore(metrics) {
    let score = 100;
    
    // Deduct for slow load time
    if (metrics.loadTime > 3000) score -= 20;
    else if (metrics.loadTime > 2000) score -= 10;
    else if (metrics.loadTime > 1000) score -= 5;
    
    // Deduct for slow DOM content loaded
    if (metrics.domContentLoaded > 2000) score -= 15;
    else if (metrics.domContentLoaded > 1000) score -= 5;
    
    // Deduct for slow first contentful paint
    if (metrics.firstContentfulPaint > 2000) score -= 15;
    else if (metrics.firstContentfulPaint > 1000) score -= 5;
    
    return Math.max(0, score);
  }
  
  /**
   * Calculate SEO score
   */
  _calculateSEOScore(metrics) {
    let score = 100;
    
    // Deduct for missing meta description
    if (!metrics.hasMetaDescription) score -= 20;
    
    // Deduct for missing H1
    if (!metrics.hasH1) score -= 15;
    
    // Deduct for missing alt text
    const altTextRatio = metrics.totalImages > 0 ? metrics.hasAltText / metrics.totalImages : 1;
    if (altTextRatio < 0.5) score -= 20;
    else if (altTextRatio < 0.8) score -= 10;
    
    return Math.max(0, score);
  }
  
  /**
   * Calculate security score
   */
  _calculateSecurityScore(metrics) {
    let score = 100;
    
    // Deduct for not using HTTPS
    if (!metrics.usesHTTPS) score -= 50;
    
    // Deduct for mixed content
    if (metrics.hasMixedContent) score -= 20;
    
    return Math.max(0, score);
  }
  
  /**
   * Calculate accessibility score
   */
  _calculateAccessibilityScore(metrics) {
    let score = 100;
    
    // Deduct for missing alt text
    const altTextRatio = metrics.totalImages > 0 ? metrics.hasAltText / metrics.totalImages : 1;
    if (altTextRatio < 0.5) score -= 30;
    else if (altTextRatio < 0.8) score -= 10;
    
    return Math.max(0, score);
  }
  
  /**
   * Generate recommendations
   */
  _generateRecommendations(metrics, scores) {
    const recommendations = [];
    
    // Performance recommendations
    if (scores.performance < 80) {
      recommendations.push({
        category: 'Performance',
        priority: 'high',
        issue: 'Slow page load time',
        recommendation: 'Optimize images, minify CSS/JS, enable compression',
        impact: 'Improves user experience and SEO',
      });
    }
    
    // SEO recommendations
    if (!metrics.hasMetaDescription) {
      recommendations.push({
        category: 'SEO',
        priority: 'high',
        issue: 'Missing meta description',
        recommendation: 'Add a compelling meta description (150-160 characters)',
        impact: 'Improves search engine rankings',
      });
    }
    
    if (!metrics.hasH1) {
      recommendations.push({
        category: 'SEO',
        priority: 'high',
        issue: 'Missing H1 tag',
        recommendation: 'Add a descriptive H1 tag with main keywords',
        impact: 'Improves search engine rankings',
      });
    }
    
    // Security recommendations
    if (!metrics.usesHTTPS) {
      recommendations.push({
        category: 'Security',
        priority: 'critical',
        issue: 'Not using HTTPS',
        recommendation: 'Implement SSL certificate and redirect to HTTPS',
        impact: 'Protects user data and improves trust',
      });
    }
    
    if (metrics.hasMixedContent) {
      recommendations.push({
        category: 'Security',
        priority: 'high',
        issue: 'Mixed content detected',
        recommendation: 'Update all HTTP resources to HTTPS',
        impact: 'Prevents security warnings and improves trust',
      });
    }
    
    // Accessibility recommendations
    if (metrics.totalImages > 0 && (metrics.hasAltText / metrics.totalImages) < 0.8) {
      recommendations.push({
        category: 'Accessibility',
        priority: 'medium',
        issue: 'Missing alt text on images',
        recommendation: 'Add descriptive alt text to all images',
        impact: 'Improves accessibility and SEO',
      });
    }
    
    return recommendations;
  }
  
  /**
   * Generate audit report (Markdown)
   */
  async generateAuditReport(auditResults, format = 'markdown') {
    try {
      const { url, auditResults: results } = auditResults;
      
      if (format === 'markdown') {
        return this._generateMarkdownReport(url, results);
      } else if (format === 'json') {
        return JSON.stringify(auditResults, null, 2);
      }
      
    } catch (error) {
      console.error('Error generating audit report:', error.message);
      return null;
    }
  }
  
  /**
   * Generate Markdown report
   */
  _generateMarkdownReport(url, results) {
    const { metrics, scores, recommendations, timestamp } = results;
    
    let report = `# Website Audit Report\n\n`;
    report += `**URL:** ${url}\n`;
    report += `**Date:** ${timestamp}\n\n`;
    
    report += `## Performance Score: ${scores.performance}/100\n\n`;
    report += `- Load Time: ${Math.round(metrics.loadTime)}ms\n`;
    report += `- DOM Content Loaded: ${Math.round(metrics.domContentLoaded)}ms\n`;
    report += `- First Contentful Paint: ${Math.round(metrics.firstContentfulPaint)}ms\n`;
    report += `- Resources: ${metrics.resourceCount}\n\n`;
    
    report += `## SEO Score: ${scores.seo}/100\n\n`;
    report += `- Meta Description: ${metrics.hasMetaDescription ? '✅' : '❌'}\n`;
    report += `- H1 Tag: ${metrics.hasH1 ? '✅' : '❌'}\n`;
    report += `- Image Alt Text: ${metrics.hasAltText}/${metrics.totalImages}\n\n`;
    
    report += `## Security Score: ${scores.security}/100\n\n`;
    report += `- HTTPS: ${metrics.usesHTTPS ? '✅' : '❌'}\n`;
    report += `- Mixed Content: ${metrics.hasMixedContent ? '❌' : '✅'}\n\n`;
    
    report += `## Accessibility Score: ${scores.accessibility}/100\n\n`;
    report += `- Image Alt Text Ratio: ${metrics.totalImages > 0 ? Math.round((metrics.hasAltText / metrics.totalImages) * 100) : 100}%\n\n`;
    
    report += `## Recommendations\n\n`;
    
    recommendations.forEach((rec, index) => {
      report += `### ${index + 1}. ${rec.issue} (${rec.priority})\n\n`;
      report += `**Category:** ${rec.category}\n`;
      report += `**Recommendation:** ${rec.recommendation}\n`;
      report += `**Impact:** ${rec.impact}\n\n`;
    });
    
    report += `## Code Fixes\n\n`;
    report += `### Performance Optimization\n\n`;
    report += `\`\`\`javascript\n// Example: Lazy load images\nconst images = document.querySelectorAll('img');\nconst imageObserver = new IntersectionObserver((entries, observer) => {\n  entries.forEach(entry => {\n    if (entry.isIntersecting) {\n      const img = entry.target;\n      img.src = img.dataset.src;\n      observer.unobserve(img);\n    }\n  });\n});\n\nimages.forEach(img => imageObserver.observe(img));\n\`\`\`\n\n`;
    
    report += `### SEO Improvement\n\n`;
    report += `\`\`\`html\n<!-- Add meta description -->\n<meta name="description" content="Your compelling description here (150-160 characters)">\n\n<!-- Add H1 tag -->\n<h1>Your main heading with keywords</h1>\n\`\`\`\n\n`;
    
    report += `### Security Fix\n\n`;
    report += `\`\`\`javascript\n// Redirect to HTTPS\nif (location.protocol !== 'https:') {\n  location.replace('https:' + window.location.href.substring(window.location.protocol.length));\n}\n\`\`\`\n\n`;
    
    return report;
  }
  
  /**
   * Save audit report to file
   */
  async saveAuditReport(report, filename) {
    try {
      const dir = './jarvis/revenue/audit_reports';
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      const filepath = path.join(dir, filename);
      fs.writeFileSync(filepath, report);
      
      console.log(`💾 Audit report saved to: ${filepath}`);
      
      return {
        success: true,
        filepath: filepath,
      };
      
    } catch (error) {
      console.error('❌ Error saving audit report:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Close browser
   */
  async closeBrowser() {
    try {
      if (this.context) {
        await this.context.close();
      }
      if (this.browser) {
        await this.browser.close();
      }
      
      this.browser = null;
      this.context = null;
      
      console.log('✅ Browser closed');
      
      return true;
    } catch (error) {
      console.error('❌ Error closing browser:', error.message);
      return false;
    }
  }
}

// Singleton instance
let scraperAgent = null;

function getScraperAgent(config = null) {
  if (!scraperAgent) {
    if (config === null) {
      config = {};
    }
    scraperAgent = new ScraperAgent(config);
  }
  return scraperAgent;
}

module.exports = { ScraperAgent, getScraperAgent };

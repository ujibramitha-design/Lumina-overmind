/**
 * JARVIS Autonomous Micro-SaaS Factory (Empire Builder)
 * =====================================================
 * 
 * Programmatic micro-SaaS application builder with automated
 * frontend, backend, payment integration, and SEO content generation.
 */

const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class EmpireBuilder {
  constructor(config = {}) {
    this.config = {
      outputDir: config.outputDir || './micro-saas-apps',
      framework: config.framework || 'react',  // react or nextjs
      backend: config.backend || 'express',
      paymentProvider: config.paymentProvider || 'stripe',
      seoPostCount: config.seoPostCount || 50,
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.appGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getAppGeneratorPrompt(),
    });
    
    this.seoGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getSEOGeneratorPrompt(),
    });
  }
  
  /**
   * App generator system prompt
   */
  _getAppGeneratorPrompt() {
    return `You are an expert full-stack developer specializing in building micro-SaaS applications.

**Your Role:**
- Generate complete React/Express application code
- Implement frontend components with modern best practices
- Create backend API endpoints with Express
- Integrate payment processing (Stripe mock)
- Follow clean code principles and maintainability

**Tech Stack:**
- Frontend: React with hooks, modern CSS
- Backend: Express.js with REST API
- Database: SQLite (for simplicity)
- Payment: Stripe (mock implementation)
- Styling: CSS modules or Tailwind CSS

**Code Structure:**
1. Frontend components (App, Dashboard, Features, Pricing)
2. Backend server (Express with API routes)
3. Database schema and models
4. Payment integration (Stripe mock)
5. Configuration files (package.json, etc.)

**Guidelines:**
- Use modern React patterns (hooks, functional components)
- Implement error handling
- Add input validation
- Include loading states
- Make it responsive
- Add basic authentication (mock)
- Include API documentation comments

**Output Format:**
Return JSON with:
- frontend: array of file paths and code
- backend: array of file paths and code
- config: configuration files
- database: database schema and models`;
  }
  
  /**
   * SEO generator system prompt
   */
  _getSEOGeneratorPrompt() {
    return `You are an expert SEO content writer specializing in programmatic SEO for micro-SaaS applications.

**Your Role:**
- Generate highly SEO-optimized blog posts
- Target long-tail keywords with low competition
- Write engaging, valuable content
- Include internal linking opportunities
- Optimize for featured snippets

**SEO Best Practices:**
- Target keyword in title (H1)
- Keyword in first 100 words
- Use H2/H3 for structure
- Include related keywords naturally
- Optimize meta description (150-160 chars)
- Add internal links
- Include call-to-action
- Length: 800-1200 words

**Content Structure:**
1. Compelling H1 with target keyword
2. Introduction (hook + keyword)
3. Problem identification
4. Solution presentation
5. Benefits and features
6. How-to guide or tips
7. Conclusion with CTA
8. Meta description

**Output Format:**
Return JSON with:
- title: SEO-optimized title
- slug: URL-friendly slug
- metaDescription: 150-160 chars
- content: full blog post content
- keywords: array of target keywords`;
  }
  
  /**
   * Scaffold new micro-SaaS application
   */
  async scaffoldApp(concept, options = {}) {
    try {
      console.log(`🏗️ Scaffolding micro-SaaS app: ${concept}`);
      
      // Generate app structure
      const appStructure = await this._generateAppStructure(concept, options);
      
      // Create app directory
      const appDir = path.join(this.config.outputDir, this._slugify(concept));
      if (!fs.existsSync(appDir)) {
        fs.mkdirSync(appDir, { recursive: true });
      }
      
      // Create frontend files
      const frontendDir = path.join(appDir, 'frontend');
      if (!fs.existsSync(frontendDir)) {
        fs.mkdirSync(frontendDir, { recursive: true });
      }
      
      for (const file of appStructure.frontend) {
        const filePath = path.join(frontendDir, file.path);
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(filePath, file.code);
        console.log(`✅ Created: ${file.path}`);
      }
      
      // Create backend files
      const backendDir = path.join(appDir, 'backend');
      if (!fs.existsSync(backendDir)) {
        fs.mkdirSync(backendDir, { recursive: true });
      }
      
      for (const file of appStructure.backend) {
        const filePath = path.join(backendDir, file.path);
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(filePath, file.code);
        console.log(`✅ Created: ${file.path}`);
      }
      
      // Create config files
      for (const file of appStructure.config) {
        const filePath = path.join(appDir, file.path);
        fs.writeFileSync(filePath, file.code);
        console.log(`✅ Created: ${file.path}`);
      }
      
      // Generate SEO blog posts
      const seoResult = await this._generateSEOContent(concept, appDir);
      
      console.log(`✅ App scaffolded successfully at: ${appDir}`);
      
      return {
        success: true,
        appDir: appDir,
        concept: concept,
        seoPosts: seoResult.postCount,
      };
      
    } catch (error) {
      console.error('❌ Error scaffolding app:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate app structure
   */
  async _generateAppStructure(concept, options) {
    try {
      console.log('📝 Generating app structure...');
      
      const prompt = `
**Concept:** ${concept}
**Framework:** ${this.config.framework}
**Backend:** ${this.config.backend}
**Payment Provider:** ${this.config.paymentProvider}

**Options:**
${JSON.stringify(options, null, 2)}

**Instructions:**
Generate a complete micro-SaaS application with:
1. Frontend: React components (App, Dashboard, Features, Pricing, Contact)
2. Backend: Express API with routes (auth, payments, features)
3. Database: SQLite schema and models
4. Payment: Stripe mock integration
5. Configuration: package.json, .env.example, README.md

Return as JSON with frontend, backend, config, and database arrays.`;
      
      const result = await this.appGenerator.generateContent(prompt);
      const structure = JSON.parse(result.response.text());
      
      return structure;
      
    } catch (error) {
      console.error('Error generating app structure:', error.message);
      return {
        frontend: [],
        backend: [],
        config: [],
        database: [],
      };
    }
  }
  
  /**
   * Generate SEO content
   */
  async _generateSEOContent(concept, appDir) {
    try {
      console.log('📝 Generating SEO blog posts...');
      
      const postsDir = path.join(appDir, 'posts');
      if (!fs.existsSync(postsDir)) {
        fs.mkdirSync(postsDir, { recursive: true });
      }
      
      const keywords = await this._generateKeywords(concept);
      const posts = [];
      
      for (let i = 0; i < this.config.seoPostCount; i++) {
        const keyword = keywords[i % keywords.length];
        const post = await this._generateBlogPost(concept, keyword, i);
        
        if (post.success) {
          const postPath = path.join(postsDir, `${post.slug}.md`);
          fs.writeFileSync(postPath, this._formatBlogPost(post));
          posts.push(post);
          
          console.log(`✅ Generated post ${i + 1}/${this.config.seoPostCount}: ${post.title}`);
        }
        
        // Small delay between generations
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      // Generate index file
      const indexPath = path.join(postsDir, 'index.json');
      fs.writeFileSync(indexPath, JSON.stringify(posts, null, 2));
      
      return {
        success: true,
        postCount: posts.length,
        posts: posts,
      };
      
    } catch (error) {
      console.error('Error generating SEO content:', error.message);
      return {
        success: false,
        postCount: 0,
        posts: [],
      };
    }
  }
  
  /**
   * Generate SEO keywords
   */
  async _generateKeywords(concept) {
    try {
      const prompt = `
**Concept:** ${concept}

**Instructions:**
Generate 20 long-tail SEO keywords related to this concept.
Focus on:
- Problem-solving keywords
- How-to keywords
- Best practices
- Tool comparisons
- Industry-specific terms

Return as JSON array of keywords.`;
      
      const result = await this.appGenerator.generateContent(prompt);
      const keywords = JSON.parse(result.response.text());
      
      return Array.isArray(keywords) ? keywords : keywords.keywords || [];
      
    } catch (error) {
      console.error('Error generating keywords:', error.message);
      return [];
    }
  }
  
  /**
   * Generate blog post
   */
  async _generateBlogPost(concept, keyword, index) {
    try {
      const prompt = `
**Concept:** ${concept}
**Target Keyword:** ${keyword}
**Post Index:** ${index}

**Instructions:**
Generate an SEO-optimized blog post targeting this keyword.
- Length: 800-1200 words
- Include H1, H2, H3 structure
- Target keyword in title and first 100 words
- Meta description: 150-160 characters
- Include internal linking opportunities
- Add call-to-action at the end

Return as JSON with title, slug, metaDescription, content, and keywords.`;
      
      const result = await this.seoGenerator.generateContent(prompt);
      const post = JSON.parse(result.response.text());
      
      return {
        success: true,
        ...post,
      };
      
    } catch (error) {
      console.error('Error generating blog post:', error.message);
      return {
        success: false,
      };
    }
  }
  
  /**
   * Format blog post as markdown
   */
  _formatBlogPost(post) {
    let content = `---\n`;
    content += `title: "${post.title}"\n`;
    content += `slug: "${post.slug}"\n`;
    content += `metaDescription: "${post.metaDescription}"\n`;
    content += `keywords: [${post.keywords.map(k => `"${k}"`).join(', ')}]\n`;
    content += `date: "${new Date().toISOString()}"\n`;
    content += `---\n\n`;
    content += post.content;
    
    return content;
  }
  
  /**
   * Slugify string
   */
  _slugify(str) {
    return str
      .toLowerCase()
      .replace(/[^\w ]+/g, '')
      .replace(/ +/g, '-');
  }
  
  /**
   * Generate Next.js app scaffold
   */
  async scaffoldNextJSApp(concept, options = {}) {
    const originalFramework = this.config.framework;
    this.config.framework = 'nextjs';
    
    const result = await this.scaffoldApp(concept, options);
    
    this.config.framework = originalFramework;
    
    return result;
  }
  
  /**
   * Get app statistics
   */
  getAppStats(appDir) {
    try {
      const stats = {
        frontendFiles: 0,
        backendFiles: 0,
        seoPosts: 0,
        totalSize: 0,
      };
      
      const frontendDir = path.join(appDir, 'frontend');
      const backendDir = path.join(appDir, 'backend');
      const postsDir = path.join(appDir, 'posts');
      
      if (fs.existsSync(frontendDir)) {
        const countFiles = (dir) => {
          let count = 0;
          const items = fs.readdirSync(dir);
          for (const item of items) {
            const itemPath = path.join(dir, item);
            const stat = fs.statSync(itemPath);
            if (stat.isDirectory()) {
              count += countFiles(itemPath);
            } else {
              count++;
              stats.totalSize += stat.size;
            }
          }
          return count;
        };
        
        stats.frontendFiles = countFiles(frontendDir);
      }
      
      if (fs.existsSync(backendDir)) {
        stats.backendFiles = countFiles(backendDir);
      }
      
      if (fs.existsSync(postsDir)) {
        const posts = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
        stats.seoPosts = posts.length;
      }
      
      return stats;
      
    } catch (error) {
      console.error('Error getting app stats:', error.message);
      return null;
    }
  }
}

// Singleton instance
let empireBuilder = null;

function getEmpireBuilder(config = null) {
  if (!empireBuilder) {
    if (config === null) {
      config = {};
    }
    empireBuilder = new EmpireBuilder(config);
  }
  return empireBuilder;
}

module.exports = { EmpireBuilder, getEmpireBuilder };

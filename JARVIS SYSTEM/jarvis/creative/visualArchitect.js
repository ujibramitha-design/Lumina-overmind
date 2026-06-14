/**
 * JARVIS Visual Architect - Senior Graphic Designer
 * ===============================================
 * 
 * Composite image auto-generation using DALL-E 3 and sharp
 * for high-fidelity marketing graphics and promotional materials.
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class VisualArchitect {
  constructor(config = {}) {
    this.config = {
      outputDir: config.outputDir || './jarvis/creative/outputs',
      assetsDir: config.assetsDir || './jarvis/creative/assets',
      imageGenAPI: config.imageGenAPI || 'dalle',  // dalle or stability
      dalleApiKey: config.dalleApiKey || process.env.OPENAI_API_KEY,
      defaultSize: config.defaultSize || '1024x1024',
      defaultQuality: config.defaultQuality || 'standard',
      ...config,
    };
    
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.promptGenerator = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getPromptGeneratorPrompt(),
    });
    
    // Ensure directories exist
    this._ensureDirectories();
  }
  
  /**
   * Prompt generator system prompt
   */
  _getPromptGeneratorPrompt() {
    return `You are an elite Senior Graphic Designer specializing in AI image generation prompts.

**Your Role:**
- Generate detailed, high-quality prompts for AI image generation
- Create prompts for marketing graphics, social media posts, banners
- Focus on visual composition, color theory, and design principles
- Specify style, mood, lighting, and technical details
- Optimize for high-fidelity, professional output

**Prompt Structure:**
1. Subject description
2. Style and aesthetic
3. Color palette
4. Lighting and atmosphere
5. Composition and framing
6. Technical specifications
7. Mood and emotion
8. Brand alignment

**Guidelines:**
- Be specific and detailed
- Use design terminology
- Consider brand guidelines
- Focus on marketing effectiveness
- Specify resolution and quality
- Keep under 200 words

**Output Format:**
Return the image generation prompt directly as text.`;
  }
  
  /**
   * Ensure directories exist
   */
  _ensureDirectories() {
    if (!fs.existsSync(this.config.outputDir)) {
      fs.mkdirSync(this.config.outputDir, { recursive: true });
    }
    if (!fs.existsSync(this.config.assetsDir)) {
      fs.mkdirSync(this.config.assetsDir, { recursive: true });
    }
  }
  
  /**
   * Generate image prompt
   */
  async generateImagePrompt(concept, style = 'modern', brandGuidelines = null) {
    try {
      console.log('🎨 Generating image prompt...');
      
      const prompt = `
**Concept:** ${concept}
**Style:** ${style}
**Brand Guidelines:** ${brandGuidelines || 'None specified'}

**Instructions:**
Generate a detailed AI image generation prompt for a marketing graphic.
Focus on visual composition, color theory, and design principles.
Specify style, mood, lighting, and technical details.
Keep under 200 words.

Return the prompt directly.`;
      
      const result = await this.promptGenerator.generateContent(prompt);
      const imagePrompt = result.response.text();
      
      console.log('✅ Image prompt generated');
      
      return {
        success: true,
        prompt: imagePrompt,
      };
      
    } catch (error) {
      console.error('❌ Error generating image prompt:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate image using DALL-E 3 (placeholder)
   */
  async generateImage(prompt, options = {}) {
    try {
      console.log('🖼️ Generating image with DALL-E 3...');
      
      // Placeholder for DALL-E 3 API integration
      // In production, use OpenAI's DALL-E 3 API
      
      const size = options.size || this.config.defaultSize;
      const quality = options.quality || this.config.defaultQuality;
      
      // Simulate image generation (replace with actual API call)
      const mockImageBuffer = await this._generateMockImage(prompt, size);
      
      const filename = `generated_${Date.now()}.png`;
      const filepath = path.join(this.config.outputDir, filename);
      
      fs.writeFileSync(filepath, mockImageBuffer);
      
      console.log(`✅ Image generated: ${filepath}`);
      
      return {
        success: true,
        filepath: filepath,
        filename: filename,
      };
      
    } catch (error) {
      console.error('❌ Error generating image:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Generate mock image (placeholder for DALL-E 3)
   */
  async _generateMockImage(prompt, size) {
    // Create a simple colored image as placeholder
    const [width, height] = size.split('x').map(Number);
    
    const svg = `
      <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#4A90E2"/>
        <text x="50%" y="50%" font-family="Arial" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">
          Generated Image
        </text>
      </svg>
    `;
    
    const buffer = Buffer.from(svg);
    return sharp(buffer).png().toBuffer();
  }
  
  /**
   * Composite image with text overlay
   */
  async compositeWithText(imagePath, textOverlay, options = {}) {
    try {
      console.log('🔤 Compositing text overlay...');
      
      const image = sharp(imagePath);
      const metadata = await image.metadata();
      
      // Create text overlay (simplified - in production use canvas or text-to-image)
      const textImage = await this._createTextOverlay(
        textOverlay.text,
        metadata.width,
        metadata.height,
        options
      );
      
      // Composite text onto image
      const outputPath = path.join(
        this.config.outputDir,
        `composite_${Date.now()}.png`
      );
      
      await image
        .composite([
          {
            input: textImage,
            top: options.top || 0,
            left: options.left || 0,
          },
        ])
        .png()
        .toFile(outputPath);
      
      console.log(`✅ Text overlay composited: ${outputPath}`);
      
      return {
        success: true,
        filepath: outputPath,
      };
      
    } catch (error) {
      console.error('❌ Error compositing text:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Create text overlay (simplified)
   */
  async _createTextOverlay(text, width, height, options = {}) {
    const fontSize = options.fontSize || 48;
    const textColor = options.textColor || '#FFFFFF';
    const backgroundColor = options.backgroundColor || 'rgba(0,0,0,0.5)';
    
    const svg = `
      <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="${backgroundColor}"/>
        <text x="50%" y="50%" font-family="Arial" font-size="${fontSize}" fill="${textColor}" text-anchor="middle" dominant-baseline="middle">
          ${text}
        </text>
      </svg>
    `;
    
    const buffer = Buffer.from(svg);
    return sharp(buffer).png().toBuffer();
  }
  
  /**
   * Composite image with logo
   */
  async compositeWithLogo(imagePath, logoPath, options = {}) {
    try {
      console.log('🏷️ Compositing logo...');
      
      const image = sharp(imagePath);
      const logo = sharp(logoPath);
      
      const logoMetadata = await logo.metadata();
      
      // Resize logo if specified
      if (options.logoSize) {
        await logo.resize(options.logoSize);
      }
      
      const outputPath = path.join(
        this.config.outputDir,
        `logo_composite_${Date.now()}.png`
      );
      
      await image
        .composite([
          {
            input: await logo.png().toBuffer(),
            top: options.top || 10,
            left: options.left || 10,
          },
        ])
        .png()
        .toFile(outputPath);
      
      console.log(`✅ Logo composited: ${outputPath}`);
      
      return {
        success: true,
        filepath: outputPath,
      };
      
    } catch (error) {
      console.error('❌ Error compositing logo:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Create marketing banner
   */
  async createMarketingBanner(concept, textOverlay, logoPath = null, options = {}) {
    try {
      console.log('🎨 Creating marketing banner...');
      
      // Generate image prompt
      const promptResult = await this.generateImagePrompt(concept, options.style);
      
      if (!promptResult.success) {
        return promptResult;
      }
      
      // Generate base image
      const imageResult = await this.generateImage(promptResult.prompt, {
        size: options.size || '1024x1024',
        quality: options.quality || 'standard',
      });
      
      if (!imageResult.success) {
        return imageResult;
      }
      
      // Composite text overlay
      const textResult = await this.compositeWithText(
        imageResult.filepath,
        textOverlay,
        {
          fontSize: options.fontSize || 48,
          textColor: options.textColor || '#FFFFFF',
          top: options.textTop || 0,
          left: options.textLeft || 0,
        }
      );
      
      if (!textResult.success) {
        return textResult;
      }
      
      // Composite logo if provided
      let finalPath = textResult.filepath;
      if (logoPath) {
        const logoResult = await this.compositeWithLogo(
          textResult.filepath,
          logoPath,
          {
            logoSize: options.logoSize || 200,
            top: options.logoTop || 10,
            left: options.logoLeft || 10,
          }
        );
        
        if (logoResult.success) {
          finalPath = logoResult.filepath;
        }
      }
      
      console.log(`✅ Marketing banner created: ${finalPath}`);
      
      return {
        success: true,
        filepath: finalPath,
        prompt: promptResult.prompt,
      };
      
    } catch (error) {
      console.error('❌ Error creating marketing banner:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Create social media post
   */
  async createSocialMediaPost(concept, platform = 'instagram', options = {}) {
    try {
      console.log(`📱 Creating ${platform} post...`);
      
      const platformSizes = {
        instagram: '1080x1080',
        twitter: '1200x675',
        linkedin: '1200x627',
        facebook: '1200x630',
      };
      
      const size = platformSizes[platform] || platformSizes.instagram;
      
      const result = await this.createMarketingBanner(
        concept,
        options.textOverlay || { text: options.text || '' },
        options.logoPath,
        {
          ...options,
          size: size,
          style: options.style || 'modern',
        }
      );
      
      return result;
      
    } catch (error) {
      console.error('❌ Error creating social media post:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Resize image
   */
  async resizeImage(imagePath, width, height) {
    try {
      const outputPath = path.join(
        this.config.outputDir,
        `resized_${Date.now()}.png`
      );
      
      await sharp(imagePath)
        .resize(width, height, { fit: 'cover' })
        .png()
        .toFile(outputPath);
      
      console.log(`✅ Image resized: ${outputPath}`);
      
      return {
        success: true,
        filepath: outputPath,
      };
      
    } catch (error) {
      console.error('❌ Error resizing image:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get statistics
   */
  getStats() {
    const outputFiles = fs.readdirSync(this.config.outputDir);
    const assetFiles = fs.readdirSync(this.config.assetsDir);
    
    return {
      outputCount: outputFiles.length,
      assetCount: assetFiles.length,
      outputDir: this.config.outputDir,
      assetsDir: this.config.assetsDir,
    };
  }
}

// Singleton instance
let visualArchitect = null;

function getVisualArchitect(config = null) {
  if (!visualArchitect) {
    if (config === null) {
      config = {};
    }
    visualArchitect = new VisualArchitect(config);
  }
  return visualArchitect;
}

module.exports = { VisualArchitect, getVisualArchitect };

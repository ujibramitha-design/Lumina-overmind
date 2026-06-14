/**
 * JARVIS Entity Extractor
 * =======================
 * 
 * Extracts entities (People, Projects, Technologies, Preferences) from conversations
 * using Gemini AI for NLP-based extraction.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { EntityTypes, Entity, RelationshipTypes, Relationship } = require('./schema');
require('dotenv').config();

class EntityExtractor {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.extractionModel = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-pro',
      systemInstruction: this._getExtractionSystemPrompt(),
    });
  }
  
  /**
   * System prompt for entity extraction
   */
  _getExtractionSystemPrompt() {
    return `You are an Entity Extractor for the JARVIS Knowledge Graph system.

**Your Role:**
- Extract entities from conversation text
- Identify entity types (Person, Project, Technology, Preference, etc.)
- Extract relationships between entities
- Assign confidence scores to extractions
- Provide structured JSON output

**Entity Types to Extract:**
- Person: Names, roles, email addresses
- Project: Project names, descriptions, repositories
- Technology: Programming languages, frameworks, tools
- Preference: User preferences, settings, choices
- Task: Tasks, activities, to-dos
- File: File names, paths, code references
- Bug: Bugs, issues, errors
- Feature: Features, requirements, enhancements
- Concept: Abstract concepts, ideas
- Location: Physical locations, offices
- Time: Temporal references, dates, durations

**Relationship Types to Extract:**
- works_on: Person -> Project
- uses: Project -> Technology
- knows: Person -> Technology
- prefers: Person -> Preference
- has_bug: Project -> Bug
- has_feature: Project -> Feature
- found_in: Bug -> File
- related_to: General semantic relationships

**Extraction Guidelines:**
- Extract all entities mentioned in the text
- Identify relationships between entities
- Assign confidence scores (0-1) based on certainty
- Use context to disambiguate entities
- Preserve original text where possible
- Handle pronouns and references correctly

**Output Format:**
Return JSON with:
- entities: Array of extracted entities
- relationships: Array of extracted relationships
- confidence: Overall confidence score
- context: Conversation context`;
  }
  
  /**
   * Extract entities from conversation text
   */
  async extractEntities(text, context = {}) {
    try {
      console.log('🔍 Extracting entities from conversation...');
      
      const prompt = this._buildExtractionPrompt(text, context);
      const result = await this.extractionModel.generateContent(prompt);
      const response = result.response.text();
      
      // Parse JSON response
      const extraction = this._parseExtractionResponse(response);
      
      // Create Entity and Relationship objects
      const entities = extraction.entities.map(e => new Entity(e));
      const relationships = extraction.relationships.map(r => new Relationship(r));
      
      console.log(`✅ Extracted ${entities.length} entities and ${relationships.length} relationships`);
      
      return {
        success: true,
        entities: entities,
        relationships: relationships,
        confidence: extraction.confidence || 0.8,
        context: context,
      };
    
    } catch (error) {
      console.error('❌ Error extracting entities:', error.message);
      return {
        success: false,
        error: error.message,
        entities: [],
        relationships: [],
      };
    }
  }
  
  /**
   * Build extraction prompt
   */
  _buildExtractionPrompt(text, context) {
    return `
**Conversation Text:**
${text}

**Context:**
- User ID: ${context.userId || 'unknown'}
- Platform: ${context.platform || 'unknown'}
- Timestamp: ${context.timestamp || new Date().toISOString()}
- Previous context: ${context.previousContext || 'none'}

**Instructions:**
Extract all entities and relationships from the conversation text.
Return as JSON with the following structure:
{
  "entities": [
    {
      "type": "entity_type",
      "name": "entity_name",
      "properties": {
        "key": "value"
      },
      "confidence": 0.9
    }
  ],
  "relationships": [
    {
      "sourceId": "source_entity_name",
      "targetId": "target_entity_name",
      "type": "relationship_type",
      "properties": {
        "key": "value"
      },
      "confidence": 0.8
    }
  ],
  "confidence": 0.85
}

**Important:**
- Use entity names as temporary IDs (will be replaced with proper IDs later)
- Include all relevant properties
- Assign confidence scores based on certainty
- Extract both explicit and implicit relationships`;
  }
  
  /**
   * Parse extraction response
   */
  _parseExtractionResponse(response) {
    try {
      // Try to extract JSON from response
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      
      // Fallback: return empty extraction
      return {
        entities: [],
        relationships: [],
        confidence: 0.0,
      };
    
    } catch (error) {
      console.error('Error parsing extraction response:', error.message);
      return {
        entities: [],
        relationships: [],
        confidence: 0.0,
      };
    }
  }
  
  /**
   * Extract entities with conversation history
   */
  async extractFromConversationHistory(history, context = {}) {
    try {
      const allEntities = [];
      const allRelationships = [];
      
      // Extract from each message in history
      for (const message of history) {
        const extraction = await this.extractEntities(message.content, {
          ...context,
          messageId: message.id,
          role: message.role,
        });
        
        if (extraction.success) {
          allEntities.push(...extraction.entities);
          allRelationships.push(...extraction.relationships);
        }
      }
      
      // Deduplicate entities
      const uniqueEntities = this._deduplicateEntities(allEntities);
      const uniqueRelationships = this._deduplicateRelationships(allRelationships);
      
      return {
        success: true,
        entities: uniqueEntities,
        relationships: uniqueRelationships,
        totalMessages: history.length,
      };
    
    } catch (error) {
      console.error('Error extracting from conversation history:', error.message);
      return {
        success: false,
        error: error.message,
        entities: [],
        relationships: [],
      };
    }
  }
  
  /**
   * Deduplicate entities by name and type
   */
  _deduplicateEntities(entities) {
    const entityMap = new Map();
    
    for (const entity of entities) {
      const key = `${entity.type}_${entity.name.toLowerCase()}`;
      
      if (!entityMap.has(key)) {
        entityMap.set(key, entity);
      } else {
        // Merge properties if entity already exists
        const existing = entityMap.get(key);
        existing.properties = { ...existing.properties, ...entity.properties };
        existing.confidence = Math.max(existing.confidence, entity.confidence);
      }
    }
    
    return Array.from(entityMap.values());
  }
  
  /**
   * Deduplicate relationships
   */
  _deduplicateRelationships(relationships) {
    const relationshipMap = new Map();
    
    for (const rel of relationships) {
      const key = `${rel.sourceId}_${rel.targetId}_${rel.type}`;
      
      if (!relationshipMap.has(key)) {
        relationshipMap.set(key, rel);
      } else {
        // Merge properties if relationship already exists
        const existing = relationshipMap.get(key);
        existing.properties = { ...existing.properties, ...rel.properties };
        existing.confidence = Math.max(existing.confidence, rel.confidence);
      }
    }
    
    return Array.from(relationshipMap.values());
  }
  
  /**
   * Extract entities from code context
   */
  async extractFromCode(code, context = {}) {
    try {
      console.log('🔍 Extracting entities from code...');
      
      const prompt = `
**Code:**
\`\`\`
${code}
\`\`\`

**Context:**
${JSON.stringify(context, null, 2)}

**Instructions:**
Extract entities from the code:
- Technologies used (languages, frameworks, libraries)
- Files and modules referenced
- Functions and classes (as concepts)
- Dependencies
- Comments indicating preferences or decisions

Return as JSON with entities and relationships.`;
      
      const result = await this.extractionModel.generateContent(prompt);
      const response = result.response.text();
      const extraction = this._parseExtractionResponse(response);
      
      const entities = extraction.entities.map(e => new Entity(e));
      const relationships = extraction.relationships.map(r => new Relationship(r));
      
      console.log(`✅ Extracted ${entities.length} entities from code`);
      
      return {
        success: true,
        entities: entities,
        relationships: relationships,
        confidence: extraction.confidence || 0.8,
      };
    
    } catch (error) {
      console.error('Error extracting from code:', error.message);
      return {
        success: false,
        error: error.message,
        entities: [],
        relationships: [],
      };
    }
  }
  
  /**
   * Batch extract entities from multiple sources
   */
  async batchExtract(sources) {
    try {
      const results = [];
      
      for (const source of sources) {
        let result;
        
        if (source.type === 'conversation') {
          result = await this.extractEntities(source.text, source.context);
        } else if (source.type === 'code') {
          result = await this.extractFromCode(source.text, source.context);
        } else if (source.type === 'history') {
          result = await this.extractFromConversationHistory(source.history, source.context);
        }
        
        if (result) {
          results.push({
            source: source.id,
            ...result,
          });
        }
      }
      
      // Merge all results
      const allEntities = results.flatMap(r => r.entities);
      const allRelationships = results.flatMap(r => r.relationships);
      
      const uniqueEntities = this._deduplicateEntities(allEntities);
      const uniqueRelationships = this._deduplicateRelationships(allRelationships);
      
      return {
        success: true,
        entities: uniqueEntities,
        relationships: uniqueRelationships,
        sourcesProcessed: results.length,
        results: results,
      };
    
    } catch (error) {
      console.error('Error in batch extraction:', error.message);
      return {
        success: false,
        error: error.message,
        entities: [],
        relationships: [],
      };
    }
  }
}

// Singleton instance
let entityExtractor = null;

function getEntityExtractor() {
  if (!entityExtractor) {
    entityExtractor = new EntityExtractor();
  }
  return entityExtractor;
}

module.exports = { EntityExtractor, getEntityExtractor };

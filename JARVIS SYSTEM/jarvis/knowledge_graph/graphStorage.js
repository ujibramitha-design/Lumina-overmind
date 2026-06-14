/**
 * JARVIS Knowledge Graph Storage
 * ==============================
 * 
 * Stores and queries the knowledge graph using a lightweight JSON-based approach.
 * Provides semantic search and relationship traversal capabilities.
 */

const fs = require('fs');
const path = require('path');
const { Entity, Relationship } = require('./schema');

class GraphStorage {
  constructor(storagePath = './jarvis/data/knowledge_graph.json') {
    this.storagePath = storagePath;
    this.entities = new Map();  // id -> Entity
    this.relationships = new Map();  // id -> Relationship
    this.entityIndex = new Map();  // name -> Set of entity IDs
    this.typeIndex = new Map();  // type -> Set of entity IDs
    this.adjacencyList = new Map();  // entityId -> Set of relationship IDs
    
    this._loadGraph();
  }
  
  /**
   * Load graph from storage
   */
  _loadGraph() {
    try {
      if (fs.existsSync(this.storagePath)) {
        const data = JSON.parse(fs.readFileSync(this.storagePath, 'utf8'));
        
        // Load entities
        for (const entityData of data.entities || []) {
          const entity = new Entity(entityData);
          this.entities.set(entity.id, entity);
          this._indexEntity(entity);
        }
        
        // Load relationships
        for (const relData of data.relationships || []) {
          const relationship = new Relationship(relData);
          this.relationships.set(relationship.id, relationship);
          this._indexRelationship(relationship);
        }
        
        console.log(`✅ Loaded ${this.entities.size} entities and ${this.relationships.size} relationships`);
      } else {
        console.log('📝 Creating new knowledge graph');
        this._saveGraph();
      }
    } catch (error) {
      console.error('❌ Error loading graph:', error.message);
    }
  }
  
  /**
   * Save graph to storage
   */
  _saveGraph() {
    try {
      const data = {
        entities: Array.from(this.entities.values()).map(e => e.toJSON()),
        relationships: Array.from(this.relationships.values()).map(r => r.toJSON()),
        metadata: {
          version: '1.0',
          lastUpdated: new Date().toISOString(),
          entityCount: this.entities.size,
          relationshipCount: this.relationships.size,
        },
      };
      
      const dir = path.dirname(this.storagePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      fs.writeFileSync(this.storagePath, JSON.stringify(data, null, 2));
      console.log('💾 Knowledge graph saved');
    } catch (error) {
      console.error('❌ Error saving graph:', error.message);
    }
  }
  
  /**
   * Index entity for fast lookup
   */
  _indexEntity(entity) {
    // Index by name
    const nameKey = entity.name.toLowerCase();
    if (!this.entityIndex.has(nameKey)) {
      this.entityIndex.set(nameKey, new Set());
    }
    this.entityIndex.get(nameKey).add(entity.id);
    
    // Index by type
    if (!this.typeIndex.has(entity.type)) {
      this.typeIndex.set(entity.type, new Set());
    }
    this.typeIndex.get(entity.type).add(entity.id);
  }
  
  /**
   * Index relationship for adjacency list
   */
  _indexRelationship(relationship) {
    // Source adjacency
    if (!this.adjacencyList.has(relationship.sourceId)) {
      this.adjacencyList.set(relationship.sourceId, new Set());
    }
    this.adjacencyList.get(relationship.sourceId).add(relationship.id);
    
    // Target adjacency (for reverse lookup)
    if (!this.adjacencyList.has(relationship.targetId)) {
      this.adjacencyList.set(relationship.targetId, new Set());
    }
    this.adjacencyList.get(relationship.targetId).add(relationship.id);
  }
  
  /**
   * Add entity to graph
   */
  addEntity(entity) {
    if (!(entity instanceof Entity)) {
      entity = new Entity(entity);
    }
    
    this.entities.set(entity.id, entity);
    this._indexEntity(entity);
    this._saveGraph();
    
    return entity;
  }
  
  /**
   * Add relationship to graph
   */
  addRelationship(relationship) {
    if (!(relationship instanceof Relationship)) {
      relationship = new Relationship(relationship);
    }
    
    // Validate source and target entities exist
    if (!this.entities.has(relationship.sourceId)) {
      throw new Error(`Source entity ${relationship.sourceId} not found`);
    }
    if (!this.entities.has(relationship.targetId)) {
      throw new Error(`Target entity ${relationship.targetId} not found`);
    }
    
    this.relationships.set(relationship.id, relationship);
    this._indexRelationship(relationship);
    this._saveGraph();
    
    return relationship;
  }
  
  /**
   * Get entity by ID
   */
  getEntity(id) {
    return this.entities.get(id);
  }
  
  /**
   * Get entity by name
   */
  getEntityByName(name) {
    const nameKey = name.toLowerCase();
    const entityIds = this.entityIndex.get(nameKey);
    
    if (!entityIds || entityIds.size === 0) {
      return null;
    }
    
    // Return first match (or could return all)
    const firstId = Array.from(entityIds)[0];
    return this.entities.get(firstId);
  }
  
  /**
   * Get entities by type
   */
  getEntitiesByType(type) {
    const entityIds = this.typeIndex.get(type) || new Set();
    return Array.from(entityIds).map(id => this.entities.get(id));
  }
  
  /**
   * Search entities by name (fuzzy match)
   */
  searchEntities(query, limit = 10) {
    const queryLower = query.toLowerCase();
    const results = [];
    
    for (const [nameKey, entityIds] of this.entityIndex) {
      if (nameKey.includes(queryLower)) {
        for (const entityId of entityIds) {
          const entity = this.entities.get(entityId);
          if (entity) {
            results.push(entity);
          }
        }
      }
    }
    
    // Sort by relevance (exact match first)
    results.sort((a, b) => {
      const aExact = a.name.toLowerCase() === queryLower;
      const bExact = b.name.toLowerCase() === queryLower;
      if (aExact && !bExact) return -1;
      if (!aExact && bExact) return 1;
      return 0;
    });
    
    return results.slice(0, limit);
  }
  
  /**
   * Get relationships for an entity
   */
  getRelationships(entityId, direction = 'both') {
    const relationshipIds = this.adjacencyList.get(entityId) || new Set();
    const relationships = [];
    
    for (const relId of relationshipIds) {
      const rel = this.relationships.get(relId);
      if (rel) {
        if (direction === 'both') {
          relationships.push(rel);
        } else if (direction === 'outgoing' && rel.sourceId === entityId) {
          relationships.push(rel);
        } else if (direction === 'incoming' && rel.targetId === entityId) {
          relationships.push(rel);
        }
      }
    }
    
    return relationships;
  }
  
  /**
   * Get connected entities
   */
  getConnectedEntities(entityId, relationshipType = null, maxDepth = 1) {
    const visited = new Set();
    const results = [];
    const queue = [{ entityId, depth: 0 }];
    
    while (queue.length > 0) {
      const { entityId: currentId, depth } = queue.shift();
      
      if (visited.has(currentId) || depth > maxDepth) {
        continue;
      }
      
      visited.add(currentId);
      
      if (depth > 0) {
        const entity = this.entities.get(currentId);
        if (entity) {
          results.push({ entity, depth });
        }
      }
      
      const relationships = this.getRelationships(currentId);
      for (const rel of relationships) {
        if (relationshipType && rel.type !== relationshipType) {
          continue;
        }
        
        const nextId = rel.sourceId === currentId ? rel.targetId : rel.sourceId;
        if (!visited.has(nextId)) {
          queue.push({ entityId: nextId, depth: depth + 1 });
        }
      }
    }
    
    return results;
  }
  
  /**
   * Find shortest path between entities
   */
  findPath(sourceId, targetId) {
    const visited = new Set();
    const queue = [{ entityId: sourceId, path: [] }];
    
    while (queue.length > 0) {
      const { entityId, path } = queue.shift();
      
      if (entityId === targetId) {
        return path;
      }
      
      if (visited.has(entityId)) {
        continue;
      }
      
      visited.add(entityId);
      
      const relationships = this.getRelationships(entityId);
      for (const rel of relationships) {
        const nextId = rel.sourceId === entityId ? rel.targetId : rel.sourceId;
        if (!visited.has(nextId)) {
          queue.push({
            entityId: nextId,
            path: [...path, { relationship: rel, from: entityId, to: nextId }],
          });
        }
      }
    }
    
    return null;  // No path found
  }
  
  /**
   * Semantic search using embeddings
   */
  semanticSearch(queryEmbedding, limit = 10) {
    const results = [];
    
    for (const [id, entity] of this.entities) {
      if (entity.embeddings) {
        const similarity = this._cosineSimilarity(queryEmbedding, entity.embeddings);
        if (similarity > 0.5) {  // Threshold
          results.push({ entity, similarity });
        }
      }
    }
    
    // Sort by similarity
    results.sort((a, b) => b.similarity - a.similarity);
    
    return results.slice(0, limit);
  }
  
  /**
   * Calculate cosine similarity between embeddings
   */
  _cosineSimilarity(a, b) {
    if (!a || !b || a.length !== b.length) {
      return 0;
    }
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
  
  /**
   * Update entity
   */
  updateEntity(entityId, updates) {
    const entity = this.entities.get(entityId);
    if (!entity) {
      throw new Error(`Entity ${entityId} not found`);
    }
    
    Object.assign(entity.properties, updates.properties || {});
    entity.updatedAt = new Date().toISOString();
    
    this._saveGraph();
    
    return entity;
  }
  
  /**
   * Delete entity
   */
  deleteEntity(entityId) {
    // Remove entity
    this.entities.delete(entityId);
    
    // Remove from indexes
    const entity = this.entities.get(entityId);
    if (entity) {
      const nameKey = entity.name.toLowerCase();
      const nameSet = this.entityIndex.get(nameKey);
      if (nameSet) {
        nameSet.delete(entityId);
      }
      
      const typeSet = this.typeIndex.get(entity.type);
      if (typeSet) {
        typeSet.delete(entityId);
      }
    }
    
    // Remove related relationships
    const relationships = this.getRelationships(entityId);
    for (const rel of relationships) {
      this.relationships.delete(rel.id);
    }
    
    this.adjacencyList.delete(entityId);
    
    this._saveGraph();
  }
  
  /**
   * Delete relationship
   */
  deleteRelationship(relationshipId) {
    const relationship = this.relationships.get(relationshipId);
    if (!relationship) {
      throw new Error(`Relationship ${relationshipId} not found`);
    }
    
    this.relationships.delete(relationshipId);
    
    // Remove from adjacency lists
    const sourceSet = this.adjacencyList.get(relationship.sourceId);
    if (sourceSet) {
      sourceSet.delete(relationshipId);
    }
    
    const targetSet = this.adjacencyList.get(relationship.targetId);
    if (targetSet) {
      targetSet.delete(relationshipId);
    }
    
    this._saveGraph();
  }
  
  /**
   * Get graph statistics
   */
  getStats() {
    return {
      entityCount: this.entities.size,
      relationshipCount: this.relationships.size,
      entityTypes: this._getEntityTypes(),
      relationshipTypes: this._getRelationshipTypes(),
      mostConnectedEntities: this._getMostConnectedEntities(5),
    };
  }
  
  /**
   * Get entity type distribution
   */
  _getEntityTypes() {
    const distribution = {};
    for (const [type, entityIds] of this.typeIndex) {
      distribution[type] = entityIds.size;
    }
    return distribution;
  }
  
  /**
   * Get relationship type distribution
   */
  _getRelationshipTypes() {
    const distribution = {};
    for (const rel of this.relationships.values()) {
      distribution[rel.type] = (distribution[rel.type] || 0) + 1;
    }
    return distribution;
  }
  
  /**
   * Get most connected entities
   */
  _getMostConnectedEntities(limit = 5) {
    const connections = [];
    
    for (const [entityId, relIds] of this.adjacencyList) {
      connections.push({
        entityId,
        connectionCount: relIds.size,
      });
    }
    
    connections.sort((a, b) => b.connectionCount - a.connectionCount);
    
    return connections.slice(0, limit).map(c => ({
      entity: this.entities.get(c.entityId),
      connectionCount: c.connectionCount,
    }));
  }
  
  /**
   * Clear entire graph
   */
  clearGraph() {
    this.entities.clear();
    this.relationships.clear();
    this.entityIndex.clear();
    this.typeIndex.clear();
    this.adjacencyList.clear();
    this._saveGraph();
  }
}

// Singleton instance
let graphStorage = null;

function getGraphStorage(storagePath = null) {
  if (!graphStorage) {
    graphStorage = new GraphStorage(storagePath);
  }
  return graphStorage;
}

module.exports = { GraphStorage, getGraphStorage };

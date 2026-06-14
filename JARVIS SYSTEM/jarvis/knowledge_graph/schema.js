/**
 * JARVIS Knowledge Graph Schema
 * ============================
 * 
 * Defines the data structure for the Subconscious Memory system.
 * Stores entities (People, Projects, Technologies, Preferences) and their relationships.
 */

/**
 * Entity Types
 * Represents different types of entities in the knowledge graph
 */
const EntityTypes = {
  PERSON: 'person',           // People (users, team members)
  PROJECT: 'project',         // Projects (lumina-overmind, etc.)
  TECHNOLOGY: 'technology',   // Technologies (React, Python, etc.)
  PREFERENCE: 'preference',   // User preferences
  TASK: 'task',               // Tasks and activities
  FILE: 'file',               // Code files
  BUG: 'bug',                 // Bugs and issues
  FEATURE: 'feature',         // Features and requirements
  CONCEPT: 'concept',         // Abstract concepts
  LOCATION: 'location',       // Physical locations
  TIME: 'time',               // Temporal references
};

/**
 * Relationship Types
 * Represents different types of relationships between entities
 */
const RelationshipTypes = {
  // Person relationships
  WORKS_ON: 'works_on',           // Person -> Project
  OWNS: 'owns',                   // Person -> Project
  COLLABORATES_WITH: 'collaborates_with', // Person -> Person
  PREFERS: 'prefers',             // Person -> Preference
  KNOWS: 'knows',                 // Person -> Technology
  
  // Project relationships
  USES: 'uses',                   // Project -> Technology
  CONTAINS: 'contains',           // Project -> File
  HAS_BUG: 'has_bug',             // Project -> Bug
  HAS_FEATURE: 'has_feature',     // Project -> Feature
  DEPENDS_ON: 'depends_on',       // Project -> Project
  
  // Technology relationships
  IMPLEMENTED_IN: 'implemented_in', // File -> Technology
  COMPATIBLE_WITH: 'compatible_with', // Technology -> Technology
  REPLACES: 'replaces',           // Technology -> Technology
  
  // Task relationships
  ASSIGNED_TO: 'assigned_to',     // Task -> Person
  RELATED_TO: 'related_to',       // Task -> Bug/Feature
  BLOCKED_BY: 'blocked_by',       // Task -> Bug
  
  // Bug relationships
  FOUND_IN: 'found_in',           // Bug -> File
  FIXED_IN: 'fixed_in',           // Bug -> File
  REPORTED_BY: 'reported_by',     // Bug -> Person
  
  // Feature relationships
  REQUESTED_BY: 'requested_by',   // Feature -> Person
  IMPLEMENTED_IN: 'implemented_in', // Feature -> File
  
  // Temporal relationships
  CREATED_AT: 'created_at',       // Entity -> Time
  MODIFIED_AT: 'modified_at',     // Entity -> Time
  OCCURRED_DURING: 'occurred_during', // Event -> Time
  
  // Spatial relationships
  LOCATED_AT: 'located_at',       // Entity -> Location
  
  // Semantic relationships
  SIMILAR_TO: 'similar_to',       // Entity -> Entity
  RELATED_TO: 'related_to',       // Entity -> Entity
  PART_OF: 'part_of',             // Entity -> Entity
  INSTANCE_OF: 'instance_of',     // Entity -> Concept
};

/**
 * Entity Schema
 * Structure for storing entity information
 */
class Entity {
  constructor(data) {
    this.id = data.id || this._generateId();
    this.type = data.type;
    this.name = data.name;
    this.properties = data.properties || {};
    this.embeddings = data.embeddings || null;  // Vector embeddings for semantic search
    this.createdAt = data.createdAt || new Date().toISOString();
    this.updatedAt = data.updatedAt || new Date().toISOString();
    this.confidence = data.confidence || 1.0;  // Confidence score (0-1)
    this.source = data.source || 'conversation';  // Source of entity
  }
  
  _generateId() {
    return `${this.type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  toJSON() {
    return {
      id: this.id,
      type: this.type,
      name: this.name,
      properties: this.properties,
      embeddings: this.embeddings,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      confidence: this.confidence,
      source: this.source,
    };
  }
}

/**
 * Relationship Schema
 * Structure for storing relationship information
 */
class Relationship {
  constructor(data) {
    this.id = data.id || this._generateId();
    this.sourceId = data.sourceId;      // From entity
    this.targetId = data.targetId;      // To entity
    this.type = data.type;              // Relationship type
    this.properties = data.properties || {};
    this.weight = data.weight || 1.0;   // Relationship strength (0-1)
    this.createdAt = data.createdAt || new Date().toISOString();
    this.updatedAt = data.updatedAt || new Date().toISOString();
    this.confidence = data.confidence || 1.0;
    this.source = data.source || 'conversation';
  }
  
  _generateId() {
    return `rel_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  toJSON() {
    return {
      id: this.id,
      sourceId: this.sourceId,
      targetId: this.targetId,
      type: this.type,
      properties: this.properties,
      weight: this.weight,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      confidence: this.confidence,
      source: this.source,
    };
  }
}

/**
 * Knowledge Graph Schema
 * Complete schema definition for the knowledge graph
 */
const KnowledgeGraphSchema = {
  // Entity types with their property schemas
  entities: {
    [EntityTypes.PERSON]: {
      required: ['name'],
      optional: ['email', 'phone', 'role', 'skills', 'preferences'],
      properties: {
        name: 'string',
        email: 'string',
        phone: 'string',
        role: 'string',
        skills: 'array<string>',
        preferences: 'object',
      },
    },
    [EntityTypes.PROJECT]: {
      required: ['name'],
      optional: ['description', 'status', 'startDate', 'endDate', 'repository'],
      properties: {
        name: 'string',
        description: 'string',
        status: 'string',  // active, completed, archived
        startDate: 'date',
        endDate: 'date',
        repository: 'string',
      },
    },
    [EntityTypes.TECHNOLOGY]: {
      required: ['name'],
      optional: ['version', 'category', 'language', 'framework'],
      properties: {
        name: 'string',
        version: 'string',
        category: 'string',  // frontend, backend, database, devops
        language: 'string',
        framework: 'boolean',
      },
    },
    [EntityTypes.PREFERENCE]: {
      required: ['name'],
      optional: ['value', 'category', 'priority'],
      properties: {
        name: 'string',
        value: 'string',
        category: 'string',  // coding, communication, workflow
        priority: 'number',  // 1-10
      },
    },
    [EntityTypes.TASK]: {
      required: ['name'],
      optional: ['status', 'priority', 'dueDate', 'assignedTo'],
      properties: {
        name: 'string',
        status: 'string',  // pending, in_progress, completed
        priority: 'string',  // low, medium, high, critical
        dueDate: 'date',
        assignedTo: 'string',  // Person entity ID
      },
    },
    [EntityTypes.FILE]: {
      required: ['name', 'path'],
      optional: ['language', 'size', 'lastModified'],
      properties: {
        name: 'string',
        path: 'string',
        language: 'string',
        size: 'number',
        lastModified: 'date',
      },
    },
    [EntityTypes.BUG]: {
      required: ['name'],
      optional: ['severity', 'status', 'description', 'fileId'],
      properties: {
        name: 'string',
        severity: 'string',  // low, medium, high, critical
        status: 'string',  // open, in_progress, resolved, closed
        description: 'string',
        fileId: 'string',  // File entity ID
      },
    },
    [EntityTypes.FEATURE]: {
      required: ['name'],
      optional: ['status', 'description', 'priority'],
      properties: {
        name: 'string',
        status: 'string',  // planned, in_progress, completed
        description: 'string',
        priority: 'string',  // low, medium, high, critical
      },
    },
    [EntityTypes.CONCEPT]: {
      required: ['name'],
      optional: ['description', 'category'],
      properties: {
        name: 'string',
        description: 'string',
        category: 'string',
      },
    },
    [EntityTypes.LOCATION]: {
      required: ['name'],
      optional: ['type', 'coordinates'],
      properties: {
        name: 'string',
        type: 'string',  // office, home, remote
        coordinates: 'object',  // {lat, lng}
      },
    },
    [EntityTypes.TIME]: {
      required: ['timestamp'],
      optional: ['type', 'duration'],
      properties: {
        timestamp: 'date',
        type: 'string',  // absolute, relative
        duration: 'string',
      },
    },
  },
  
  // Relationship types with their property schemas
  relationships: {
    [RelationshipTypes.WORKS_ON]: {
      source: EntityTypes.PERSON,
      target: EntityTypes.PROJECT,
      properties: {
        role: 'string',
        startDate: 'date',
        endDate: 'date',
      },
    },
    [RelationshipTypes.OWNS]: {
      source: EntityTypes.PERSON,
      target: EntityTypes.PROJECT,
      properties: {
        ownership: 'number',  // percentage
      },
    },
    [RelationshipTypes.COLLABORATES_WITH]: {
      source: EntityTypes.PERSON,
      target: EntityTypes.PERSON,
      properties: {
        context: 'string',
        frequency: 'number',
      },
    },
    [RelationshipTypes.PREFERS]: {
      source: EntityTypes.PERSON,
      target: EntityTypes.PREFERENCE,
      properties: {
        strength: 'number',  // 0-1
      },
    },
    [RelationshipTypes.KNOWS]: {
      source: EntityTypes.PERSON,
      target: EntityTypes.TECHNOLOGY,
      properties: {
        proficiency: 'string',  // beginner, intermediate, expert
        years: 'number',
      },
    },
    [RelationshipTypes.USES]: {
      source: EntityTypes.PROJECT,
      target: EntityTypes.TECHNOLOGY,
      properties: {
        version: 'string',
        purpose: 'string',
      },
    },
    [RelationshipTypes.CONTAINS]: {
      source: EntityTypes.PROJECT,
      target: EntityTypes.FILE,
      properties: {
        path: 'string',
      },
    },
    [RelationshipTypes.HAS_BUG]: {
      source: EntityTypes.PROJECT,
      target: EntityTypes.BUG,
      properties: {
        severity: 'string',
      },
    },
    [RelationshipTypes.HAS_FEATURE]: {
      source: EntityTypes.PROJECT,
      target: EntityTypes.FEATURE,
      properties: {
        status: 'string',
      },
    },
    [RelationshipTypes.DEPENDS_ON]: {
      source: EntityTypes.PROJECT,
      target: EntityTypes.PROJECT,
      properties: {
        type: 'string',  // direct, indirect
      },
    },
    [RelationshipTypes.IMPLEMENTED_IN]: {
      source: EntityTypes.FILE,
      target: EntityTypes.TECHNOLOGY,
      properties: {
        version: 'string',
      },
    },
    [RelationshipTypes.COMPATIBLE_WITH]: {
      source: EntityTypes.TECHNOLOGY,
      target: EntityTypes.TECHNOLOGY,
      properties: {
        version: 'string',
      },
    },
    [RelationshipTypes.REPLACES]: {
      source: EntityTypes.TECHNOLOGY,
      target: EntityTypes.TECHNOLOGY,
      properties: {
        reason: 'string',
      },
    },
    [RelationshipTypes.ASSIGNED_TO]: {
      source: EntityTypes.TASK,
      target: EntityTypes.PERSON,
      properties: {
        assignedAt: 'date',
      },
    },
    [RelationshipTypes.RELATED_TO]: {
      source: EntityTypes.TASK,
      target: [EntityTypes.BUG, EntityTypes.FEATURE],
      properties: {
        type: 'string',
      },
    },
    [RelationshipTypes.BLOCKED_BY]: {
      source: EntityTypes.TASK,
      target: EntityTypes.BUG,
      properties: {
        reason: 'string',
      },
    },
    [RelationshipTypes.FOUND_IN]: {
      source: EntityTypes.BUG,
      target: EntityTypes.FILE,
      properties: {
        line: 'number',
      },
    },
    [RelationshipTypes.FIXED_IN]: {
      source: EntityTypes.BUG,
      target: EntityTypes.FILE,
      properties: {
        line: 'number',
        commit: 'string',
      },
    },
    [RelationshipTypes.REPORTED_BY]: {
      source: EntityTypes.BUG,
      target: EntityTypes.PERSON,
      properties: {
        reportedAt: 'date',
      },
    },
    [RelationshipTypes.REQUESTED_BY]: {
      source: EntityTypes.FEATURE,
      target: EntityTypes.PERSON,
      properties: {
        requestedAt: 'date',
      },
    },
    [RelationshipTypes.IMPLEMENTED_IN]: {
      source: EntityTypes.FEATURE,
      target: EntityTypes.FILE,
      properties: {
        line: 'number',
        commit: 'string',
      },
    },
    [RelationshipTypes.CREATED_AT]: {
      source: 'any',
      target: EntityTypes.TIME,
      properties: {},
    },
    [RelationshipTypes.MODIFIED_AT]: {
      source: 'any',
      target: EntityTypes.TIME,
      properties: {},
    },
    [RelationshipTypes.OCCURRED_DURING]: {
      source: 'any',
      target: EntityTypes.TIME,
      properties: {
        duration: 'string',
      },
    },
    [RelationshipTypes.LOCATED_AT]: {
      source: 'any',
      target: EntityTypes.LOCATION,
      properties: {},
    },
    [RelationshipTypes.SIMILAR_TO]: {
      source: 'any',
      target: 'any',
      properties: {
        similarity: 'number',  // 0-1
      },
    },
    [RelationshipTypes.RELATED_TO]: {
      source: 'any',
      target: 'any',
      properties: {
        context: 'string',
      },
    },
    [RelationshipTypes.PART_OF]: {
      source: 'any',
      target: 'any',
      properties: {},
    },
    [RelationshipTypes.INSTANCE_OF]: {
      source: 'any',
      target: EntityTypes.CONCEPT,
      properties: {},
    },
  },
  
  // Validation rules
  validation: {
    entity: {
      required: ['id', 'type', 'name'],
      types: Object.values(EntityTypes),
    },
    relationship: {
      required: ['id', 'sourceId', 'targetId', 'type'],
      types: Object.values(RelationshipTypes),
    },
  },
};

/**
 * Example Knowledge Graph Instance
 * Shows how the graph would look in practice
 */
const ExampleGraph = {
  entities: [
    {
      id: 'person_1',
      type: EntityTypes.PERSON,
      name: 'John Doe',
      properties: {
        email: 'john@example.com',
        role: 'Senior Developer',
        skills: ['React', 'Python', 'FastAPI'],
      },
    },
    {
      id: 'project_1',
      type: EntityTypes.PROJECT,
      name: 'lumina-overmind',
      properties: {
        description: 'AI-powered project management system',
        status: 'active',
        repository: 'https://github.com/johndoe/lumina-overmind',
      },
    },
    {
      id: 'tech_1',
      type: EntityTypes.TECHNOLOGY,
      name: 'React',
      properties: {
        version: '18.2.0',
        category: 'frontend',
        framework: true,
      },
    },
    {
      id: 'tech_2',
      type: EntityTypes.TECHNOLOGY,
      name: 'FastAPI',
      properties: {
        version: '0.95.0',
        category: 'backend',
        framework: true,
      },
    },
    {
      id: 'bug_1',
      type: EntityTypes.BUG,
      name: 'Button click not working',
      properties: {
        severity: 'high',
        status: 'open',
        description: 'Button click handler not firing on mobile',
      },
    },
  ],
  relationships: [
    {
      id: 'rel_1',
      sourceId: 'person_1',
      targetId: 'project_1',
      type: RelationshipTypes.WORKS_ON,
      properties: {
        role: 'Senior Developer',
        startDate: '2024-01-01',
      },
    },
    {
      id: 'rel_2',
      sourceId: 'project_1',
      targetId: 'tech_1',
      type: RelationshipTypes.USES,
      properties: {
        version: '18.2.0',
        purpose: 'Frontend framework',
      },
    },
    {
      id: 'rel_3',
      sourceId: 'project_1',
      targetId: 'tech_2',
      type: RelationshipTypes.USES,
      properties: {
        version: '0.95.0',
        purpose: 'Backend API',
      },
    },
    {
      id: 'rel_4',
      sourceId: 'person_1',
      targetId: 'tech_1',
      type: RelationshipTypes.KNOWS,
      properties: {
        proficiency: 'expert',
        years: 5,
      },
    },
    {
      id: 'rel_5',
      sourceId: 'project_1',
      targetId: 'bug_1',
      type: RelationshipTypes.HAS_BUG,
      properties: {
        severity: 'high',
      },
    },
  ],
};

module.exports = {
  EntityTypes,
  RelationshipTypes,
  Entity,
  Relationship,
  KnowledgeGraphSchema,
  ExampleGraph,
};

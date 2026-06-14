# JARVIS Hive Mind & Knowledge Graph Documentation

Complete guide for JARVIS's advanced multi-agent orchestration and subconscious memory system.

## Overview

JARVIS has evolved into a "Hive Mind" orchestrator with:
- **Multi-Agent System**: Specialized agents for different tasks (DevAgent, QAAgent, AnalystAgent, ArchitectAgent)
- **Knowledge Graph**: Subconscious memory storing entities and relationships
- **Semantic Search**: Context-aware retrieval using graph traversal
- **Task Routing**: Intelligent delegation based on task complexity

## Multi-Agent System (Hive Mind)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│              JARVIS Manager Agent (Orchestrator)        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Analyze Task Complexity                             │
│  2. Select Specialized Agents                           │
│  3. Delegate Sub-tasks                                  │
│  4. Synthesize Agent Outputs                            │
│  5. Provide Final Response                              │
│                                                          │
└─────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  DevAgent   │ │  QAAgent    │ │ AnalystAgent │ │ArchitectAgent│
│ Code Gen    │ │ Code Review │ │ System Analysis│ │System Design │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### Specialized Agents

**Manager Agent (JARVIS)**
- Role: Orchestrator
- Capabilities: Task delegation, synthesis, coordination
- Model: gemini-1.5-pro
- Responsibilities:
  - Analyze task complexity
  - Select appropriate agents
  - Coordinate parallel execution
  - Synthesize results
  - Present final response

**DevAgent**
- Role: Code Generator
- Capabilities: Code generation, refactoring, debugging
- Model: gemini-1.5-pro
- Responsibilities:
  - Generate clean, efficient code
  - Refactor existing code
  - Debug and fix issues
  - Follow coding standards

**QAAgent**
- Role: Code Reviewer
- Capabilities: Code review, testing, quality assurance
- Model: gemini-1.5-pro
- Responsibilities:
  - Review code for quality
  - Identify bugs and edge cases
  - Suggest improvements
  - Write test cases

**AnalystAgent**
- Role: System Analyst
- Capabilities: System analysis, performance review
- Model: gemini-1.5-pro
- Responsibilities:
  - Analyze system performance
  - Identify bottlenecks
  - Review metrics
  - Suggest optimizations

**ArchitectAgent**
- Role: System Architect
- Capabilities: System design, architecture review
- Model: gemini-1.5-pro
- Responsibilities:
  - Review architecture
  - Design scalable solutions
  - Evaluate technology choices
  - Ensure best practices

### Task Routing Flow

**Example: Complex Code Request**

```
User: "Create a REST API for user authentication with JWT, refresh tokens, and role-based access control. Include proper error handling, validation, and unit tests."

┌─────────────────────────────────────────────────────────┐
│ Step 1: Task Analysis                                  │
│ Complexity: High                                       │
│ Required Capabilities: code_generation, testing,       │
│                        quality_assurance, design          │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Agent Selection                                 │
│ Selected: DevAgent, QAAgent, ArchitectAgent            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Parallel Execution                              │
│                                                          │
│ DevAgent: Generate authentication code                  │
│ QAAgent: Review code and write tests                    │
│ ArchitectAgent: Validate architecture                   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Synthesis                                       │
│ Combine agent outputs into cohesive response            │
│ Resolve conflicts between recommendations                │
│ Prioritize most critical insights                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Final Response                                   │
│ Present polished, actionable response to user           │
└─────────────────────────────────────────────────────────┘
```

### Implementation

**Agent Router (`jarvis/agents/agentRouter.js`)**

```javascript
const { getAgentRouter } = require('../../agents/agentRouter');

// Route task to appropriate agents
const result = await agentRouter.routeTask(task, {
  userId,
  persona,
  platform,
});

// Result includes:
// - success: boolean
// - response: synthesized final response
// - agentResults: individual agent outputs
// - timestamp: ISO string
```

**Integration with geminiService.js**

```javascript
// In generateResponse()
const isComplexTask = this._isComplexTask(message, context);

if (this.hiveMindEnabled && this.agentRouter && isComplexTask) {
  // Use Hive Mind for complex tasks
  result = await this.agentRouter.routeTask(message, {
    ...context,
    ...graphContext,
    userId,
    persona,
  });
} else {
  // Use standard conversational model
  result = await this.conversationalModel.generateContent(conversation);
}
```

## Knowledge Graph (Subconscious Memory)

### Schema

**Entity Types**

| Type | Description | Properties |
|------|-------------|------------|
| person | People (users, team members) | name, email, phone, role, skills |
| project | Projects | name, description, status, repository |
| technology | Technologies (React, Python) | name, version, category, framework |
| preference | User preferences | name, value, category, priority |
| task | Tasks and activities | name, status, priority, dueDate |
| file | Code files | name, path, language, size |
| bug | Bugs and issues | name, severity, status, description |
| feature | Features and requirements | name, status, description, priority |
| concept | Abstract concepts | name, description, category |
| location | Physical locations | name, type, coordinates |
| time | Temporal references | timestamp, type, duration |

**Relationship Types**

| Type | Source → Target | Description |
|------|-----------------|-------------|
| works_on | person → project | Person works on project |
| uses | project → technology | Project uses technology |
| knows | person → technology | Person knows technology |
| prefers | person → preference | Person has preference |
| has_bug | project → bug | Project has bug |
| has_feature | project → feature | Project has feature |
| found_in | bug → file | Bug found in file |
| related_to | any → any | General semantic relationship |

### Example Graph

```
Person (John Doe)
    │
    ├── works_on → Project (lumina-overmind)
    │                 │
    │                 ├── uses → Technology (React)
    │                 ├── uses → Technology (FastAPI)
    │                 ├── has_bug → Bug (Button click not working)
    │                 └── has_feature → Feature (User authentication)
    │
    ├── knows → Technology (React)
    └── knows → Technology (Python)

Bug (Button click not working)
    │
    └── found_in → File (Button.tsx)
```

### Entity Extraction

**Automatic Extraction from Conversations**

```javascript
const { getEntityExtractor } = require('../../knowledge_graph/entityExtractor');

// Extract entities from conversation
const extraction = await entityExtractor.extractEntities(message, {
  userId,
  platform,
  timestamp,
});

// Result includes:
// - entities: Array of extracted entities
// - relationships: Array of extracted relationships
// - confidence: Overall confidence score
```

**Extraction Process**

1. **NLP Analysis**: Gemini analyzes conversation text
2. **Entity Recognition**: Identifies people, projects, technologies
3. **Relationship Extraction**: Finds connections between entities
4. **Confidence Scoring**: Assigns confidence to each extraction
5. **Deduplication**: Merges duplicate entities
6. **Storage**: Stores in knowledge graph

### Graph Storage

**JSON-Based Storage**

```javascript
const { getGraphStorage } = require('../../knowledge_graph/graphStorage');

// Get graph storage instance
const graph = getGraphStorage('./jarvis/data/knowledge_graph.json');

// Add entity
const entity = {
  type: 'technology',
  name: 'React',
  properties: {
    version: '18.2.0',
    category: 'frontend',
    framework: true,
  },
};
graph.addEntity(entity);

// Add relationship
const relationship = {
  sourceId: 'project_1',
  targetId: 'tech_1',
  type: 'uses',
  properties: {
    version: '18.2.0',
    purpose: 'Frontend framework',
  },
};
graph.addRelationship(relationship);

// Search entities
const results = graph.searchEntities('React', 10);

// Get connected entities
const connected = graph.getConnectedEntities('project_1', 'uses', 2);

// Find path between entities
const path = graph.findPath('person_1', 'bug_1');
```

### Semantic Search

**Context-Aware Retrieval**

```javascript
// Query knowledge graph for relevant context
const graphContext = await this._queryKnowledgeGraph(message, userId);

// Returns:
{
  relevantEntities: [
    { name: 'React', type: 'technology', properties: {...} },
    { name: 'lumina-overmind', type: 'project', properties: {...} },
  ],
  userConnections: [
    { entity: 'John Doe', type: 'person', depth: 1 },
    { entity: 'React', type: 'technology', depth: 2 },
  ],
}
```

**Graph Traversal**

```javascript
// Get all entities connected to a given entity
const connected = graph.getConnectedEntities(entityId, null, 2);

// Get entities by specific relationship type
const technologies = graph.getConnectedEntities(entityId, 'uses', 1);

// Find shortest path between entities
const path = graph.findPath(sourceId, targetId);
// Returns: [{ relationship, from, to }, ...]
```

## Integration Flow

### Complete Request Processing

```
User Message
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Entity Extraction (Background)                      │
│    - Extract entities from message                      │
│    - Update knowledge graph                             │
│    - Store relationships                                │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Knowledge Graph Query                                │
│    - Search for relevant entities                        │
│    - Get user-specific context                           │
│    - Retrieve connected entities                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Task Complexity Analysis                             │
│    - Check for complexity indicators                      │
│    - Evaluate message length                             │
│    - Detect code context                                │
└─────────────────────────────────────────────────────────┘
    │
    ├─ Simple Task ──► Standard Gemini Response
    │
    └─ Complex Task ──► Hive Mind Orchestration
                         │
                         ▼
                ┌──────────────────────┐
                │ Agent Selection      │
                └──────────────────────┘
                         │
                         ▼
                ┌──────────────────────┐
                │ Parallel Execution   │
                │ DevAgent + QAAgent   │
                └──────────────────────┘
                         │
                         ▼
                ┌──────────────────────┐
                │ Result Synthesis     │
                └──────────────────────┘
                         │
                         ▼
                Final Response to User
```

## Configuration

### Environment Variables

```bash
# Hive Mind
JARVIS_HIVE_MIND_ENABLED=true
JARVIS_AGENT_ROUTER_ENABLED=true

# Knowledge Graph
JARVIS_KNOWLEDGE_GRAPH_ENABLED=true
JARVIS_ENTITY_EXTRACTION_ENABLED=true
JARVIS_GRAPH_STORAGE_PATH=./jarvis/data/knowledge_graph.json

# Agent Configuration
JARVIS_DEVAGENT_MODEL=gemini-1.5-pro
JARVIS_QAAGENT_MODEL=gemini-1.5-pro
JARVIS_ANALYSTAGENT_MODEL=gemini-1.5-pro
JARVIS_ARCHITECTAGENT_MODEL=gemini-1.5-pro
```

### geminiService.js Configuration

```javascript
const config = {
  knowledge_graph_enabled: true,
  hive_mind_enabled: true,
  agent_router_enabled: true,
  entity_extraction_enabled: true,
};
```

## Usage Examples

### Example 1: Simple Query (No Hive Mind)

```
User: "What's the system status?"

Process:
1. Extract entities: "system" (concept)
2. Query graph: No relevant entities
3. Complexity analysis: Simple task
4. Route to: Standard Gemini model

Response: "All systems are operational. CPU at 45%, memory at 62%."
```

### Example 2: Complex Code Request (Hive Mind)

```
User: "Create a REST API for user authentication with JWT and role-based access control. Include proper error handling and unit tests."

Process:
1. Extract entities: "REST API" (concept), "JWT" (technology), "authentication" (concept)
2. Query graph: Retrieve related technologies
3. Complexity analysis: Complex task (create, JWT, authentication, tests)
4. Route to: Hive Mind

Agent Execution:
- DevAgent: Generate authentication code with JWT
- QAAgent: Review code, write unit tests
- ArchitectAgent: Validate architecture

Synthesis:
"Here's a complete authentication system with JWT and role-based access control..."

Response: Polished, synthesized response with code and tests
```

### Example 3: Contextual Query (Knowledge Graph)

```
User: "What was that bug from last month's project?"

Process:
1. Extract entities: "bug" (bug), "last month" (time), "project" (project)
2. Query graph: Search for bugs, find connections to user's projects
3. Retrieve: Bug entity with relationships to project and file
4. Context: Found "Button click not working" bug in lumina-overmind project

Response: "You're referring to the 'Button click not working' bug in the lumina-overmind project. It was found in Button.tsx and has been resolved."
```

## Best Practices

### For Multi-Agent System

1. **Task Delegation**: Only use Hive Mind for complex tasks
2. **Parallel Execution**: Run independent agents in parallel
3. **Synthesis Quality**: Ensure Manager Agent produces cohesive output
4. **Error Handling**: Gracefully handle agent failures
5. **Performance**: Monitor agent execution times

### For Knowledge Graph

1. **Entity Extraction**: Run extraction in background
2. **Deduplication**: Merge duplicate entities intelligently
3. **Confidence Scoring**: Use confidence for quality filtering
4. **Graph Traversal**: Limit depth to prevent performance issues
5. **Storage**: Regularly backup graph data

### For Integration

1. **Modular Design**: Keep components independent
2. **Configuration**: Allow enabling/disabling features
3. **Fallback**: Always have fallback to standard model
4. **Monitoring**: Track agent performance and graph growth
5. **Testing**: Test each component independently

## Troubleshooting

### Hive Mind Issues

**Agents not executing:**
```javascript
// Check if Hive Mind is enabled
console.log('Hive Mind enabled:', this.hiveMindEnabled);
console.log('Agent router:', this.agentRouter);

// Check task complexity detection
const isComplex = this._isComplexTask(message, context);
console.log('Is complex:', isComplex);
```

**Synthesis fails:**
```javascript
// Check agent results
console.log('Agent results:', result.agentResults);

// Verify Manager Agent is working
const testResult = await this.agentRouter.routeTask('test', {});
console.log('Test result:', testResult);
```

### Knowledge Graph Issues

**Entities not being extracted:**
```javascript
// Check entity extractor
const extraction = await this.entityExtractor.extractEntities(message, context);
console.log('Extraction result:', extraction);

// Verify Gemini API is working
const test = await this.entityExtractor.extractEntities('test', {});
console.log('Test extraction:', test);
```

**Graph not storing entities:**
```javascript
// Check graph storage
const graph = getGraphStorage();
const stats = graph.getStats();
console.log('Graph stats:', stats);

// Verify file permissions
const path = './jarvis/data/knowledge_graph.json';
console.log('File exists:', fs.existsSync(path));
```

**Search not finding entities:**
```javascript
// Check entity index
const entity = graph.getEntityByName('React');
console.log('Entity found:', entity);

// Check search function
const results = graph.searchEntities('React', 10);
console.log('Search results:', results);
```

## Performance Considerations

### Multi-Agent System

- **Latency**: Adds 2-5 seconds for complex tasks
- **Parallel Execution**: Reduces total time by 50-70%
- **Memory**: Each agent uses ~100MB memory
- **API Calls**: One call per agent + one for synthesis

### Knowledge Graph

- **Storage**: JSON file grows with entities (~1KB per entity)
- **Query Time**: O(n) for search, O(d) for traversal (d = depth)
- **Extraction**: Adds 500ms-2s per message
- **Memory**: Graph in memory (~10-50MB for 1000 entities)

### Optimization Tips

1. **Limit Graph Size**: Prune old/unused entities
2. **Cache Queries**: Cache frequent graph queries
3. **Batch Extraction**: Extract entities in batches
4. **Lazy Loading**: Load graph on demand
5. **Index Optimization**: Use efficient data structures

## Monitoring

### Hive Mind Metrics

```javascript
// Get agent router status
const status = agentRouter.getAgentStatus();
console.log('Agent status:', status);
// Returns: { availableAgents, agentCount, isProcessing, queueLength }
```

### Knowledge Graph Metrics

```javascript
// Get graph statistics
const stats = graphStorage.getStats();
console.log('Graph stats:', stats);
// Returns: { entityCount, relationshipCount, entityTypes, relationshipTypes, mostConnectedEntities }
```

### Entity Extraction Metrics

```javascript
// Track extraction performance
const extraction = await entityExtractor.extractEntities(message, context);
console.log('Extraction confidence:', extraction.confidence);
console.log('Entities extracted:', extraction.entities.length);
console.log('Relationships extracted:', extraction.relationships.length);
```

## Security Considerations

### Multi-Agent System

- **Task Validation**: Validate tasks before delegation
- **Agent Isolation**: Agents should not access sensitive data
- **Output Sanitization**: Sanitize agent outputs before synthesis
- **Rate Limiting**: Limit agent execution frequency
- **Audit Logging**: Log all agent executions

### Knowledge Graph

- **Data Privacy**: Don't store sensitive personal data
- **Access Control**: Limit graph access to authorized users
- **Data Retention**: Implement data retention policies
- **Encryption**: Encrypt graph data at rest
- **Validation**: Validate all graph modifications

## Future Enhancements

### Planned Features

- **Vector Embeddings**: Use embeddings for semantic search
- **Graph Database**: Migrate to Neo4j or similar
- **Dynamic Agents**: Create agents on-demand based on task
- **Agent Collaboration**: Allow agents to communicate directly
- **Graph Visualization**: Visual graph exploration UI
- **Temporal Graph**: Track entity relationships over time
- **Multi-User Graph**: Separate graphs per user
- **Graph Export**: Export graph to various formats

### Community Contributions

Contributions welcome for:
- Additional specialized agents
- Better entity extraction algorithms
- Enhanced graph query capabilities
- Performance optimizations
- Cross-platform adaptations
- Visualization tools

## Support

For issues or questions:
- Check agent router status
- Verify knowledge graph storage
- Monitor extraction logs
- Review configuration settings
- Test with simple tasks first
- Check API rate limits
- Verify file permissions

## License

This feature is part of JARVIS AI System.
See main project license for details.

/**
 * JARVIS Multi-Agent Router (Hive Mind)
 * =====================================
 * 
 * Orchestrates multiple specialized agents for complex tasks.
 * JARVIS acts as the Manager Agent that delegates and synthesizes.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class AgentRouter {
  /**
   * Initialize the agent router with specialized agents
   */
  constructor() {
    this.agents = {};
    this.taskQueue = [];
    this.isProcessing = false;
    
    // Initialize specialized agents
    this._initializeAgents();
  }
  
  /**
   * Initialize all specialized agents
   */
  _initializeAgents() {
    // Manager Agent (JARVIS - Orchestrator)
    this.agents.manager = {
      name: 'Manager Agent',
      role: 'Orchestrator',
      model: 'gemini-1.5-pro',
      systemPrompt: this._getManagerSystemPrompt(),
      capabilities: ['task_delegation', 'synthesis', 'coordination'],
    };
    
    // DevAgent (Code Generation)
    this.agents.dev = {
      name: 'DevAgent',
      role: 'Code Generator',
      model: 'gemini-1.5-pro',
      systemPrompt: this._getDevAgentSystemPrompt(),
      capabilities: ['code_generation', 'refactoring', 'debugging'],
    };
    
    // QAAgent (Code Review)
    this.agents.qa = {
      name: 'QAAgent',
      role: 'Code Reviewer',
      model: 'gemini-1.5-pro',
      systemPrompt: this._getQAAgentSystemPrompt(),
      capabilities: ['code_review', 'testing', 'quality_assurance'],
    };
    
    // AnalystAgent (System Analysis)
    this.agents.analyst = {
      name: 'AnalystAgent',
      role: 'System Analyst',
      model: 'gemini-1.5-pro',
      systemPrompt: this._getAnalystAgentSystemPrompt(),
      capabilities: ['system_analysis', 'performance_review', 'optimization'],
    };
    
    // ArchitectAgent (System Design)
    this.agents.architect = {
      name: 'ArchitectAgent',
      role: 'System Architect',
      model: 'gemini-1.5-pro',
      systemPrompt: this._getArchitectAgentSystemPrompt(),
      capabilities: ['system_design', 'architecture_review', 'best_practices'],
    };
    
    console.log('✅ Multi-Agent Router initialized with specialized agents');
  }
  
  /**
   * Manager Agent System Prompt
   */
  _getManagerSystemPrompt() {
    return `You are the Manager Agent of the JARVIS Hive Mind system.

**Your Role:**
- Analyze incoming tasks and determine the best approach
- Delegate sub-tasks to specialized agents
- Synthesize outputs from multiple agents
- Coordinate agent execution
- Provide final, polished responses to the user

**Available Agents:**
- DevAgent: Code generation, refactoring, debugging
- QAAgent: Code review, testing, quality assurance
- AnalystAgent: System analysis, performance review
- ArchitectAgent: System design, architecture review

**Task Delegation Strategy:**
1. Analyze task complexity and requirements
2. Identify which agents are needed
3. Create sub-tasks for each agent
4. Execute agents in parallel when possible
5. Synthesize results into cohesive response
6. Present final result to user

**Synthesis Guidelines:**
- Combine agent outputs logically
- Resolve conflicts between agent recommendations
- Prioritize most critical insights
- Provide clear, actionable final response
- Maintain JARVIS persona throughout`;
  }
  
  /**
   * DevAgent System Prompt
   */
  _getDevAgentSystemPrompt() {
    return `You are the DevAgent, a specialized code generation agent in the JARVIS Hive Mind.

**Your Role:**
- Generate clean, efficient code
- Refactor existing code for better performance
- Debug and fix code issues
- Follow best practices and coding standards
- Write self-documenting code

**Code Standards:**
- Follow Lumina Overmind coding conventions
- Use TypeScript/JavaScript for frontend
- Use Python/FastAPI for backend
- Write clear, descriptive variable names
- Add comments for complex logic
- Handle errors gracefully

**Output Format:**
- Provide complete, runnable code
- Include necessary imports
- Add usage examples
- Explain key decisions
- Note any dependencies`;
  }
  
  /**
   * QAAgent System Prompt
   */
  _getQAAgentSystemPrompt() {
    return `You are the QAAgent, a specialized code review agent in the JARVIS Hive Mind.

**Your Role:**
- Review code for quality and correctness
- Identify potential bugs and edge cases
- Suggest improvements and optimizations
- Ensure code follows best practices
- Write test cases when needed

**Review Criteria:**
- Code correctness and logic
- Performance implications
- Security vulnerabilities
- Error handling
- Code readability
- Test coverage

**Output Format:**
- Overall assessment (pass/fail/needs review)
- Specific issues found
- Severity levels (critical/high/medium/low)
- Recommended fixes
- Test suggestions`;
  }
  
  /**
   * AnalystAgent System Prompt
   */
  _getAnalystAgentSystemPrompt() {
    return `You are the AnalystAgent, a specialized system analysis agent in the JARVIS Hive Mind.

**Your Role:**
- Analyze system performance
- Identify bottlenecks and issues
- Review system metrics
- Suggest optimizations
- Monitor system health

**Analysis Focus:**
- CPU and memory usage
- Response times and latency
- Error rates and patterns
- Database performance
- Network issues
- Resource utilization

**Output Format:**
- Performance summary
- Identified issues
- Root cause analysis
- Optimization recommendations
- Priority rankings`;
  }
  
  /**
   * ArchitectAgent System Prompt
   */
  _getArchitectAgentSystemPrompt() {
    return `You are the ArchitectAgent, a specialized system design agent in the JARVIS Hive Mind.

**Your Role:**
- Review system architecture
- Design scalable solutions
- Suggest architectural improvements
- Evaluate technology choices
- Ensure best practices

**Architecture Principles:**
- Scalability and performance
- Maintainability and modularity
- Security and reliability
- Cost-effectiveness
- Developer experience

**Output Format:**
- Architecture assessment
- Design recommendations
- Technology stack suggestions
- Implementation roadmap
- Risk assessment`;
  }
  
  /**
   * Route task to appropriate agents
   */
  async routeTask(task, context = {}) {
    try {
      console.log(`🧠 Routing task: ${task.substring(0, 50)}...`);
      
      // Analyze task complexity
      const taskAnalysis = await this._analyzeTask(task, context);
      
      // Determine which agents to use
      const selectedAgents = this._selectAgents(taskAnalysis);
      
      console.log(`📋 Selected agents: ${selectedAgents.map(a => a.name).join(', ')}`);
      
      // If single agent, execute directly
      if (selectedAgents.length === 1) {
        const result = await this._executeAgent(selectedAgents[0], task, context);
        return result;
      }
      
      // If multiple agents, orchestrate parallel execution
      const results = await this._orchestrateAgents(selectedAgents, task, context);
      
      // Synthesize results
      const synthesized = await this._synthesizeResults(results, task, context);
      
      return synthesized;
    
    } catch (error) {
      console.error('❌ Error routing task:', error.message);
      return {
        success: false,
        error: error.message,
        response: 'I encountered an error processing your request.',
      };
    }
  }
  
  /**
   * Analyze task to determine complexity and requirements
   */
  async _analyzeTask(task, context) {
    try {
      const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({
        model: 'gemini-1.5-flash',
        systemInstruction: `Analyze the task and determine:
1. Task complexity (simple/medium/complex)
2. Required capabilities (code generation, review, analysis, design)
3. Estimated time to complete
4. Dependencies on other tasks
5. Risk level

Output as JSON with these fields.`,
      });
      
      const result = await model.generateContent(task);
      const analysis = JSON.parse(result.response.text());
      
      return analysis;
    
    } catch (error) {
      console.error('Error analyzing task:', error.message);
      // Default analysis
      return {
        complexity: 'medium',
        required_capabilities: ['code_generation'],
        estimated_time: '5 minutes',
        dependencies: [],
        risk_level: 'low',
      };
    }
  }
  
  /**
   * Select appropriate agents based on task analysis
   */
  _selectAgents(taskAnalysis) {
    const selectedAgents = [];
    const capabilities = taskAnalysis.required_capabilities || [];
    
    // Map capabilities to agents
    const capabilityMap = {
      code_generation: ['dev'],
      code_review: ['qa'],
      testing: ['qa'],
      debugging: ['dev', 'qa'],
      refactoring: ['dev', 'architect'],
      system_analysis: ['analyst'],
      performance_review: ['analyst'],
      optimization: ['analyst', 'dev'],
      system_design: ['architect'],
      architecture_review: ['architect'],
    };
    
    // Select agents based on required capabilities
    for (const capability of capabilities) {
      const agentNames = capabilityMap[capability] || [];
      for (const agentName of agentNames) {
        if (!selectedAgents.find(a => a.name === this.agents[agentName].name)) {
          selectedAgents.push(this.agents[agentName]);
        }
      }
    }
    
    // Default to DevAgent if no specific capabilities
    if (selectedAgents.length === 0) {
      selectedAgents.push(this.agents.dev);
    }
    
    return selectedAgents;
  }
  
  /**
   * Execute a single agent
   */
  async _executeAgent(agent, task, context) {
    try {
      console.log(`🤖 Executing ${agent.name}...`);
      
      const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({
        model: agent.model,
        systemInstruction: agent.systemPrompt,
      });
      
      const prompt = this._buildAgentPrompt(agent, task, context);
      const result = await model.generateContent(prompt);
      
      return {
        agent: agent.name,
        success: true,
        response: result.response.text(),
        timestamp: new Date().toISOString(),
      };
    
    } catch (error) {
      console.error(`❌ Error executing ${agent.name}:`, error.message);
      return {
        agent: agent.name,
        success: false,
        error: error.message,
        response: `I encountered an error in ${agent.name}.`,
      };
    }
  }
  
  /**
   * Orchestrate multiple agents in parallel
   */
  async _orchestrateAgents(agents, task, context) {
    try {
      console.log(`🔄 Orchestrating ${agents.length} agents in parallel...`);
      
      // Execute all agents in parallel
      const promises = agents.map(agent => this._executeAgent(agent, task, context));
      const results = await Promise.all(promises);
      
      console.log(`✅ All agents completed`);
      
      return results;
    
    } catch (error) {
      console.error('❌ Error orchestrating agents:', error.message);
      return [];
    }
  }
  
  /**
   * Synthesize results from multiple agents
   */
  async _synthesizeResults(results, task, context) {
    try {
      console.log(`🧩 Synthesizing results from ${results.length} agents...`);
      
      const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({
        model: 'gemini-1.5-pro',
        systemInstruction: this.agents.manager.systemPrompt,
      });
      
      // Build synthesis prompt
      const prompt = `
**Original Task:**
${task}

**Agent Results:**
${results.map(r => `**${r.agent}:**\n${r.response}`).join('\n\n')}

**Context:**
${JSON.stringify(context, null, 2)}

**Your Task:**
Synthesize these agent outputs into a cohesive, polished response for the user.
- Combine insights logically
- Resolve any conflicts
- Prioritize most important information
- Provide clear, actionable final response
- Maintain JARVIS persona
`;
      
      const result = await model.generateContent(prompt);
      
      return {
        success: true,
        response: result.response.text(),
        agentResults: results,
        timestamp: new Date().toISOString(),
      };
    
    } catch (error) {
      console.error('❌ Error synthesizing results:', error.message);
      return {
        success: false,
        error: error.message,
        response: 'I encountered an error synthesizing the agent results.',
      };
    }
  }
  
  /**
   * Build prompt for a specific agent
   */
  _buildAgentPrompt(agent, task, context) {
    return `
**Task:**
${task}

**Context:**
${JSON.stringify(context, null, 2)}

**Your Role:**
You are ${agent.name}, the ${agent.role}.

**Your Capabilities:**
${agent.capabilities.join(', ')}

**Instructions:**
Complete the task according to your role and capabilities.
Provide a clear, actionable response.
`;
  }
  
  /**
   * Get agent status
   */
  getAgentStatus() {
    return {
      availableAgents: Object.keys(this.agents),
      agentCount: Object.keys(this.agents).length,
      isProcessing: this.isProcessing,
      queueLength: this.taskQueue.length,
    };
  }
}

// Singleton instance
let agentRouter = null;

function getAgentRouter() {
  if (!agentRouter) {
    agentRouter = new AgentRouter();
  }
  return agentRouter;
}

module.exports = { AgentRouter, getAgentRouter };

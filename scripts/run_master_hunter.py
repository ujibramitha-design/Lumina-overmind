"""
Master Hunter Orchestrator - Multi-Agent Parallel Execution
Executes 4 scouting agents simultaneously using ThreadPoolExecutor

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import json
import time
import logging
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all scout agents
from agents.scout_agent.market_intelligence import MarketIntelligence
from agents.scout_agent.urban_foresight_scout import UrbanForesightScout
from agents.scout_agent.gov_affinity_scout import GovAffinityScout
from agents.scout_agent.social_intent_scout import SocialIntentScout
from agents.scout_agent.linkedin_exec_scout import LinkedInExecScout

# Configure logging with colored output
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for different log levels"""
    
    COLORS = {
        'DEBUG': '\033[92m',    # Green
        'INFO': '\033[94m',     # Blue
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[91m', # Red
        'THREAD': '\033[96m',   # Cyan
        'SUCCESS': '\033[92m',  # Green
        'HIGHLIGHT': '\033[95m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add custom thread coloring
        if hasattr(record, 'thread_id'):
            record.msg = f"{self.COLORS['THREAD']}[THREAD-{record.thread_id}]{self.COLORS['RESET']} {record.msg}"
        
        # Add color based on level
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        return f"{log_color}{formatted}{reset_color}"

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler with colored formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

@dataclass
class AgentTask:
    """Data class for agent task configuration"""
    name: str
    agent_class: Callable
    method_name: str
    method_args: tuple
    method_kwargs: dict
    thread_id: int
    priority: int = 1  # 1=High, 2=Medium, 3=Low

@dataclass
class AgentResult:
    """Data class for agent execution results"""
    agent_name: str
    thread_id: int
    success: bool
    result: Any
    execution_time: float
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class MasterHunterOrchestrator:
    """Master orchestrator for parallel execution of multiple scouting agents"""
    
    def __init__(self, max_workers: int = 5):
        self.name = "Master Hunter Orchestrator"
        self.version = "2.0.0"  # Enhanced with LinkedIn Executive Scout
        self.max_workers = max_workers
        self.execution_id = f"master_hunter_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize all agents
        self.agents = {
            'Market Intelligence': MarketIntelligence(),
            'Urban Foresight': UrbanForesightScout(),
            'Government Affinity': GovAffinityScout(),
            'Social Intent': SocialIntentScout(),
            'LinkedIn Executive': LinkedInExecScout()
        }
        
        # Thread safety
        self._lock = threading.Lock()
        self._results = {}
        self._active_threads = {}
        
        logger.info(f"🎯 {self.name} v{self.version} initialized")
        logger.info(f"🚀 Execution ID: {self.execution_id}")
        logger.info(f"⚡ Max Workers: {self.max_workers}")
        logger.info(f"🤖 Agents Loaded: {list(self.agents.keys())}")
        logger.info(f"👔 Added LinkedIn Executive Scout for High-Net-Worth hunting")
    
    def _execute_agent_task(self, task: AgentTask) -> AgentResult:
        """
        Execute a single agent task with comprehensive error handling
        
        Args:
            task: AgentTask configuration
            
        Returns:
            AgentResult with execution details
        """
        
        thread_id = task.thread_id
        agent_name = task.name
        
        # Record thread start
        with self._lock:
            self._active_threads[thread_id] = {
                'agent_name': agent_name,
                'start_time': datetime.now(),
                'status': 'running'
            }
        
        start_time = datetime.now()
        
        try:
            # Log thread start
            logger.info(f"🚀 [THREAD-{thread_id}] Starting {agent_name} execution...")
            
            # Get agent instance
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent {agent_name} not found")
            
            # Get method to execute
            method = getattr(agent, task.method_name)
            if not method:
                raise ValueError(f"Method {task.method_name} not found in {agent_name}")
            
            # Execute method with arguments
            logger.info(f"⚙️ [THREAD-{thread_id}] Executing {task.method_name} with args: {task.method_args}")
            result = method(*task.method_args, **task.method_kwargs)
            
            # Calculate execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Log success
            logger.info(f"✅ [THREAD-{thread_id}] {agent_name} completed successfully in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=agent_name,
                thread_id=thread_id,
                success=True,
                result=result,
                execution_time=execution_time,
                start_time=start_time,
                end_time=end_time
            )
            
        except Exception as e:
            # Calculate execution time even for failures
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            error_message = f"Error in {agent_name}: {str(e)}"
            logger.error(f"❌ [THREAD-{thread_id}] {error_message}")
            
            return AgentResult(
                agent_name=agent_name,
                thread_id=thread_id,
                success=False,
                result=None,
                execution_time=execution_time,
                error_message=error_message,
                start_time=start_time,
                end_time=end_time
            )
            
        finally:
            # Record thread completion
            with self._lock:
                if thread_id in self._active_threads:
                    self._active_threads[thread_id]['status'] = 'completed'
                    self._active_threads[thread_id]['end_time'] = datetime.now()
    
    def run_parallel_scouting(self, keywords: List[str] = None) -> Dict[str, Any]:
        """
        Run all 4 scouting agents in parallel
        
        Args:
            keywords: Keywords for social intent scanning
            
        Returns:
            Dict containing comprehensive execution results
        """
        
        if keywords is None:
            keywords = ['butuh rumah', 'cari KPR murah', 'overkredit rumah']
        
        logger.info("🎯 Starting Master Hunter Parallel Execution...")
        logger.info(f"🔍 Keywords for Social Intent: {keywords}")
        logger.info("=" * 80)
        
        # Prepare agent tasks
        tasks = self._prepare_agent_tasks(keywords)
        
        # Execute tasks in parallel
        execution_results = self._execute_parallel_tasks(tasks)
        
        # Generate comprehensive report
        final_report = self._generate_final_report(execution_results)
        
        logger.info("=" * 80)
        logger.info("🎉 Master Hunter Parallel Execution Completed!")
        logger.info(f"📊 Total Execution Time: {final_report['summary']['total_execution_time']:.2f}s")
        logger.info(f"✅ Successful Agents: {final_report['summary']['successful_agents']}")
        logger.info(f"❌ Failed Agents: {final_report['summary']['failed_agents']}")
        
        return final_report
    
    def _prepare_agent_tasks(self, keywords: List[str]) -> List[AgentTask]:
        """Prepare all agent tasks for parallel execution"""
        
        tasks = [
            # Market Intelligence - Analyze Serang market
            AgentTask(
                name="Market Intelligence",
                agent_class=MarketIntelligence,
                method_name="run_cipocok_jaya_research",
                method_args=(),
                method_kwargs={},
                thread_id=1,
                priority=1
            ),
            
            # Urban Foresight - Generate 10-year development map
            AgentTask(
                name="Urban Foresight",
                agent_class=UrbanForesightScout,
                method_name="generate_future_map",
                method_args=((-6.1256, 106.1445), "Serang"),
                method_kwargs={},
                thread_id=2,
                priority=1
            ),
            
            # Government Affinity - Analyze PNS/P3K market
            AgentTask(
                name="Government Affinity",
                agent_class=GovAffinityScout,
                method_name="generate_market_intelligence_report",
                method_args=((-6.1256, 106.1445),),
                method_kwargs={},
                thread_id=3,
                priority=1
            ),
            
            # Social Intent Scout - Enhanced Deep Comment Analysis
            AgentTask(
                name="Social Intent",
                agent_class=SocialIntentScout,
                method_name="run_social_intent_analysis",
                method_args=(keywords,),
                method_kwargs={},
                thread_id=4,
                priority=1
            ),
            
            # LinkedIn Executive Scout - High-Net-Worth Hunting
            AgentTask(
                name="LinkedIn Executive",
                agent_class=LinkedInExecScout,
                method_name="run_executive_hunting",
                method_args=(),
                method_kwargs={},
                thread_id=5,
                priority=1
            )
        ]
        
        return tasks
    
    def _execute_parallel_tasks(self, tasks: List[AgentTask]) -> Dict[str, AgentResult]:
        """Execute all tasks in parallel using ThreadPoolExecutor"""
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="Hunter") as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._execute_agent_task, task): task
                for task in tasks
            }
            
            # Process completed tasks as they finish
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                
                try:
                    result = future.result()
                    results[result.agent_name] = result
                    
                    # Store in thread-safe results dict
                    with self._lock:
                        self._results[result.agent_name] = result
                    
                    # Log intermediate progress
                    completed_count = len([r for r in results.values() if r.success])
                    total_count = len(tasks)
                    progress = (completed_count / total_count) * 100
                    
                    logger.info(f"📈 Progress: {completed_count}/{total_count} agents completed ({progress:.1f}%)")
                    
                except Exception as e:
                    error_msg = f"Unexpected error in task execution: {str(e)}"
                    logger.error(f"💥 {error_msg}")
                    
                    # Create error result
                    error_result = AgentResult(
                        agent_name=task.name,
                        thread_id=task.thread_id,
                        success=False,
                        result=None,
                        execution_time=0.0,
                        error_message=error_msg
                    )
                    results[task.name] = error_result
        
        return results
    
    def _generate_final_report(self, results: Dict[str, AgentResult]) -> Dict[str, Any]:
        """Generate comprehensive final execution report"""
        
        # Calculate summary statistics
        successful_agents = [r for r in results.values() if r.success]
        failed_agents = [r for r in results.values() if not r.success]
        
        total_execution_time = max(
            (r.end_time - r.start_time).total_seconds() 
            for r in results.values() 
            if r.start_time and r.end_time
        ) if results else 0
        
        # Prepare agent summaries
        agent_summaries = {}
        for agent_name, result in results.items():
            agent_summaries[agent_name] = {
                'success': result.success,
                'execution_time': result.execution_time,
                'thread_id': result.thread_id,
                'error_message': result.error_message,
                'result_summary': self._summarize_agent_result(result)
            }
        
        # Generate insights and recommendations
        insights = self._generate_execution_insights(results)
        recommendations = self._generate_recommendations(results)
        
        final_report = {
            'execution_id': self.execution_id,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_agents': len(results),
                'successful_agents': len(successful_agents),
                'failed_agents': len(failed_agents),
                'total_execution_time': total_execution_time,
                'success_rate': (len(successful_agents) / len(results)) * 100 if results else 0
            },
            'agent_results': agent_summaries,
            'performance_metrics': {
                'fastest_agent': min(results.items(), key=lambda x: x[1].execution_time) if results else None,
                'slowest_agent': max(results.items(), key=lambda x: x[1].execution_time) if results else None,
                'average_execution_time': sum(r.execution_time for r in results.values()) / len(results) if results else 0,
                'thread_utilization': f"{self.max_workers}/{len(results)} threads used"
            },
            'insights': insights,
            'recommendations': recommendations,
            'detailed_results': {
                agent_name: result.result if result.success else None
                for agent_name, result in results.items()
            }
        }
        
        return final_report
    
    def _summarize_agent_result(self, result: AgentResult) -> str:
        """Generate a summary of agent execution result"""
        
        if not result.success:
            return f"Failed: {result.error_message}"
        
        try:
            agent_result = result.result
            
            if isinstance(agent_result, dict):
                # Extract key metrics based on agent type
                if result.agent_name == "Market Intelligence":
                    return f"Market analysis completed with {len(agent_result.get('market_trends', []))} trends"
                
                elif result.agent_name == "Urban Foresight":
                    return f"Urban analysis completed with {len(agent_result.get('timeline_data', []))} timeline entries"
                
                elif result.agent_name == "Government Affinity":
                    return f"Gov analysis completed with density score {agent_result.get('density_score', 0)}/10"
                
                elif result.agent_name == "Social Intent":
                    scan_summary = agent_result.get('scan_summary', {})
                    return f"Social scan completed: {scan_summary.get('total_posts_found', 0)} posts, {scan_summary.get('high_intent_prospects', 0)} prospects"
                
                else:
                    return f"Completed with {len(str(agent_result))} characters of data"
            
            else:
                return f"Completed with result type: {type(agent_result).__name__}"
                
        except Exception as e:
            return f"Result summary failed: {str(e)}"
    
    def _generate_execution_insights(self, results: Dict[str, AgentResult]) -> List[str]:
        """Generate insights from execution results"""
        
        insights = []
        
        # Performance insights
        execution_times = [r.execution_time for r in results.values() if r.success]
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            insights.append(f"Average agent execution time: {avg_time:.2f}s")
        
        # Success rate insights
        success_count = len([r for r in results.values() if r.success])
        if success_count == len(results):
            insights.append("All agents executed successfully - system is fully operational")
        elif success_count > 0:
            insights.append(f"Partial success - {success_count}/{len(results)} agents operational")
        else:
            insights.append("All agents failed - system needs immediate attention")
        
        # Thread utilization insights
        if len(results) == self.max_workers:
            insights.append("Optimal thread utilization - all agents running in parallel")
        else:
            insights.append(f"Thread utilization could be optimized - {len(results)}/{self.max_workers} threads used")
        
        return insights
    
    def _generate_recommendations(self, results: Dict[str, AgentResult]) -> List[str]:
        """Generate recommendations based on execution results"""
        
        recommendations = []
        
        # Failed agent recommendations
        failed_agents = [name for name, result in results.items() if not result.success]
        if failed_agents:
            recommendations.append(f"Investigate and fix failed agents: {', '.join(failed_agents)}")
        
        # Performance recommendations
        slow_agents = [(name, result.execution_time) for name, result in results.items() 
                      if result.success and result.execution_time > 30]
        if slow_agents:
            recommendations.append(f"Optimize slow agents: {', '.join([f'{name} ({time:.1f}s)' for name, time in slow_agents])}")
        
        # Success recommendations
        successful_agents = [name for name, result in results.items() if result.success]
        if len(successful_agents) == len(results):
            recommendations.append("System ready for production deployment")
        
        # Resource recommendations
        if len(results) < self.max_workers:
            recommendations.append("Consider adding more agents to fully utilize thread pool")
        
        return recommendations
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status"""
        
        with self._lock:
            return {
                'execution_id': self.execution_id,
                'active_threads': len(self._active_threads),
                'completed_results': len(self._results),
                'thread_details': dict(self._active_threads),
                'agent_status': {
                    name: 'completed' if name in self._results else 'pending'
                    for name in self.agents.keys()
                }
            }


# Convenience function for standalone execution
def run_master_hunter(keywords: List[str] = None) -> Dict[str, Any]:
    """
    Convenience function to run Master Hunter with all agents
    
    Args:
        keywords: Keywords for social intent scanning
        
    Returns:
        Dict containing complete execution results
    """
    orchestrator = MasterHunterOrchestrator()
    return orchestrator.run_parallel_scouting(keywords)


if __name__ == "__main__":
    # Example usage
    print("🎯 Master Hunter Orchestrator - Example Usage")
    print("=" * 80)
    
    # Define keywords for social intent
    keywords = ['butuh rumah', 'cari KPR murah', 'overkredit rumah']
    
    print(f"🔍 Keywords: {keywords}")
    print(f"⚡ Starting parallel execution of 4 agents...")
    print("=" * 80)
    
    # Run master hunter
    start_time = time.time()
    results = run_master_hunter(keywords)
    end_time = time.time()
    
    print("=" * 80)
    print("🎉 EXECUTION SUMMARY")
    print("=" * 80)
    
    # Print summary
    summary = results['summary']
    print(f"📊 Total Agents: {summary['total_agents']}")
    print(f"✅ Successful: {summary['successful_agents']}")
    print(f"❌ Failed: {summary['failed_agents']}")
    print(f"⏱️ Total Time: {summary['total_execution_time']:.2f}s")
    print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
    
    print("\n🚀 AGENT RESULTS:")
    for agent_name, agent_result in results['agent_results'].items():
        status = "✅" if agent_result['success'] else "❌"
        print(f"{status} {agent_name}: {agent_result['result_summary']} ({agent_result['execution_time']:.2f}s)")
    
    print("\n💡 INSIGHTS:")
    for insight in results['insights']:
        print(f"• {insight}")
    
    print("\n🎯 RECOMMENDATIONS:")
    for rec in results['recommendations']:
        print(f"• {rec}")
    
    print("=" * 80)
    print(f"🏁 Master Hunter execution completed in {end_time - start_time:.2f}s")
    print("=" * 80)

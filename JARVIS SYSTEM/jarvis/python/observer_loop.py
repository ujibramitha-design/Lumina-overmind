"""
JARVIS Observer Loop - Self-Evolution System
==========================================

Background cron job that runs weekly to analyze JARVIS's own performance
and implement self-improvements through autonomous code fixes.
"""

import asyncio
import logging
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import subprocess
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ObserverLoop:
    """
    The Observer Loop - JARVIS's self-evolution system.
    Analyzes chat logs and error logs to identify improvements.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Database paths
        self.chat_db_path = config.get('chat_db_path', './jarvis/data/jarvis_memory.db')
        self.error_log_path = config.get('error_log_path', './logs/jarvis_channels.log')
        
        # Git configuration
        self.git_repo_path = config.get('git_repo_path', os.getcwd())
        self.git_branch_prefix = config.get('git_branch_prefix', 'jarvis/auto-fix-')
        
        # Notification settings
        self.notification_channel = config.get('notification_channel', 'whatsapp')
        self.notification_user_id = config.get('notification_user_id')
        
        # Analysis settings
        self.analysis_weeks = config.get('analysis_weeks', 1)  # Analyze past 1 week
        self.min_confidence = config.get('min_confidence', 0.7)  # Minimum confidence for auto-fix
        
        # Statistics
        self.stats = {
            'last_analysis': None,
            'total_analyses': 0,
            'auto_fixes_applied': 0,
            'pr_notifications_sent': 0,
        }
    
    async def run_weekly_analysis(self):
        """
        Run the weekly self-refinement analysis.
        """
        logger.info('🔄 Starting JARVIS Observer Loop - Weekly Analysis')
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Gather chat logs
            chat_logs = await self._gather_chat_logs()
            logger.info(f'📊 Gathered {len(chat_logs)} chat log entries')
            
            # Step 2: Gather error logs
            error_logs = await self._gather_error_logs()
            logger.info(f'📊 Gathered {len(error_logs)} error log entries')
            
            # Step 3: Generate self-refinement report
            refinement_report = await self._generate_refinement_report(chat_logs, error_logs)
            logger.info('📝 Self-refinement report generated')
            
            # Step 4: Analyze report for actionable improvements
            actionable_items = self._analyze_refinement_report(refinement_report)
            logger.info(f'🎯 Found {len(actionable_items)} actionable items')
            
            # Step 5: Process actionable items
            for item in actionable_items:
                await self._process_actionable_item(item)
            
            # Step 6: Update statistics
            self.stats['last_analysis'] = datetime.utcnow().isoformat()
            self.stats['total_analyses'] += 1
            
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f'✅ Observer Loop completed in {elapsed:.2f}s')
            
            return {
                'success': True,
                'chat_logs_analyzed': len(chat_logs),
                'error_logs_analyzed': len(error_logs),
                'actionable_items': len(actionable_items),
                'stats': self.stats,
            }
        
        except Exception as e:
            logger.error(f'❌ Observer Loop failed: {e}')
            return {
                'success': False,
                'error': str(e),
            }
    
    async def _gather_chat_logs(self) -> List[Dict[str, Any]]:
        """
        Gather chat logs from the database for the past week.
        """
        try:
            conn = sqlite3.connect(self.chat_db_path)
            cursor = conn.cursor()
            
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(weeks=self.analysis_weeks)
            
            # Query conversation summaries (lightweight)
            cursor.execute('''
                SELECT id, platform, user_id, date, summary, key_points, token_count
                FROM conversation_summaries
                WHERE date >= ?
                ORDER BY date DESC
            ''', (start_date.isoformat(),))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'platform': row[1],
                    'user_id': row[2],
                    'date': row[3],
                    'summary': row[4],
                    'key_points': json.loads(row[5]) if row[5] else [],
                    'token_count': row[6],
                }
                for row in rows
            ]
        
        except Exception as e:
            logger.error(f'Error gathering chat logs: {e}')
            return []
    
    async def _gather_error_logs(self) -> List[Dict[str, Any]]:
        """
        Gather error logs from the log file for the past week.
        """
        try:
            if not os.path.exists(self.error_log_path):
                logger.warning(f'Error log file not found: {self.error_log_path}')
                return []
            
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(weeks=self.analysis_weeks)
            
            error_logs = []
            
            with open(self.error_log_path, 'r') as f:
                for line in f:
                    # Parse log line (assuming standard format)
                    if 'ERROR' in line or 'error' in line:
                        # Extract timestamp and error message
                        try:
                            # Simple parsing - adjust based on actual log format
                            parts = line.split(' - ')
                            if len(parts) >= 4:
                                timestamp_str = parts[0]
                                level = parts[2]
                                message = ' - '.join(parts[3:])
                                
                                # Parse timestamp
                                try:
                                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                                    
                                    # Check if within date range
                                    if start_date <= timestamp <= end_date:
                                        error_logs.append({
                                            'timestamp': timestamp.isoformat(),
                                            'level': level,
                                            'message': message,
                                        })
                                except ValueError:
                                    continue
                        except Exception:
                            continue
            
            return error_logs
        
        except Exception as e:
            logger.error(f'Error gathering error logs: {e}')
            return []
    
    async def _generate_refinement_report(self, chat_logs: List[Dict], error_logs: List[Dict]) -> Dict[str, Any]:
        """
        Generate self-refinement report using Gemini AI.
        """
        try:
            # Import Gemini service
            sys.path.append('./jarvis/channels')
            from services.geminiService import getGeminiService
            
            gemini_service = getGeminiService()
            
            # Build analysis prompt
            prompt = self._build_analysis_prompt(chat_logs, error_logs)
            
            # Generate analysis using Gemini
            result = await gemini_service.performAnalysis(
                'observer_loop',
                {
                    'chat_logs': chat_logs[:50],  # Limit to prevent token overflow
                    'error_logs': error_logs[:50],
                },
                'self_refinement',
                {
                    'analysis_type': 'self_evolution',
                    'date_range': f'Past {self.analysis_weeks} week(s)',
                }
            )
            
            if result.success:
                # Parse the analysis response
                refinement_report = self._parse_refinement_response(result.response)
                return refinement_report
            else:
                logger.error(f'Failed to generate refinement report: {result.error}')
                return {
                    'summary': 'Analysis failed',
                    'misunderstandings': [],
                    'weak_prompts': [],
                    'code_bottlenecks': [],
                    'suggestions': [],
                }
        
        except Exception as e:
            logger.error(f'Error generating refinement report: {e}')
            return {
                'summary': 'Analysis error',
                'misunderstandings': [],
                'weak_prompts': [],
                'code_bottlenecks': [],
                'suggestions': [],
            }
    
    def _build_analysis_prompt(self, chat_logs: List[Dict], error_logs: List[Dict]) -> str:
        """
        Build the analysis prompt for Gemini.
        """
        prompt = f"""
**JARVIS Self-Refinement Analysis**
================================

You are JARVIS, analyzing your own performance over the past {self.analysis_weeks} week(s).

**Chat Logs Summary:**
- Total conversations: {len(chat_logs)}
- Platforms: {', '.join(set(log['platform'] for log in chat_logs))}
- Date range: {chat_logs[0]['date'] if chat_logs else 'N/A'} to {chat_logs[-1]['date'] if chat_logs else 'N/A'}

**Error Logs Summary:**
- Total errors: {len(error_logs)}
- Error types: {', '.join(set(log['level'] for log in error_logs))}

**Your Task:**
Analyze these logs and identify:
1. **Misunderstandings**: Where you misunderstood user intent or context
2. **Weak Prompts**: Areas where your system prompts could be improved
3. **Code Bottlenecks**: Performance issues or inefficient code patterns
4. **Suggestions**: Concrete improvements you can make

**Output Format:**
Provide a JSON-structured response with:
- summary: Overall assessment
- misunderstandings: List of specific misunderstandings with context
- weak_prompts: List of prompt improvements needed
- code_bottlenecks: List of code issues found
- suggestions: List of actionable improvements
- code_fixes: List of specific code fixes (if any) with:
  - file_path: Path to file to fix
  - issue: Description of the issue
  - fix_code: The fixed code
  - confidence: Your confidence in this fix (0-1)

**Chat Log Sample:**
{json.dumps(chat_logs[:5], indent=2) if chat_logs else 'No chat logs'}

**Error Log Sample:**
{json.dumps(error_logs[:5], indent=2) if error_logs else 'No error logs'}
"""
        return prompt
    
    def _parse_refinement_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the refinement response from Gemini.
        """
        try:
            # Try to extract JSON from response
            # Gemini might wrap JSON in markdown code blocks
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
            elif '```' in response:
                json_start = response.find('```') + 3
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            # Parse JSON
            refinement_data = json.loads(json_str)
            
            # Ensure required fields
            return {
                'summary': refinement_data.get('summary', 'No summary provided'),
                'misunderstandings': refinement_data.get('misunderstandings', []),
                'weak_prompts': refinement_data.get('weak_prompts', []),
                'code_bottlenecks': refinement_data.get('code_bottlenecks', []),
                'suggestions': refinement_data.get('suggestions', []),
                'code_fixes': refinement_data.get('code_fixes', []),
            }
        
        except Exception as e:
            logger.error(f'Error parsing refinement response: {e}')
            return {
                'summary': 'Failed to parse analysis',
                'misunderstandings': [],
                'weak_prompts': [],
                'code_bottlenecks': [],
                'suggestions': [],
                'code_fixes': [],
            }
    
    def _analyze_refinement_report(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze the refinement report and extract actionable items.
        """
        actionable_items = []
        
        # Process code fixes
        for fix in report.get('code_fixes', []):
            confidence = fix.get('confidence', 0.5)
            
            if confidence >= self.min_confidence:
                actionable_items.append({
                    'type': 'code_fix',
                    'priority': 'high' if confidence >= 0.9 else 'medium',
                    'data': fix,
                })
        
        # Process suggestions
        for suggestion in report.get('suggestions', []):
            actionable_items.append({
                'type': 'suggestion',
                'priority': 'low',
                'data': suggestion,
            })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        actionable_items.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return actionable_items
    
    async def _process_actionable_item(self, item: Dict[str, Any]):
        """
        Process an actionable item from the refinement report.
        """
        try:
            item_type = item['type']
            item_data = item['data']
            
            if item_type == 'code_fix':
                await self._apply_code_fix(item_data)
            elif item_type == 'suggestion':
                await self._log_suggestion(item_data)
        
        except Exception as e:
            logger.error(f'Error processing actionable item: {e}')
    
    async def _apply_code_fix(self, fix_data: Dict[str, Any]):
        """
        Apply a code fix autonomously.
        """
        try:
            file_path = fix_data.get('file_path')
            issue = fix_data.get('issue')
            fix_code = fix_data.get('fix_code')
            confidence = fix_data.get('confidence', 0.5)
            
            if not file_path or not fix_code:
                logger.warning('Invalid code fix data')
                return
            
            logger.info(f'🔧 Applying code fix: {file_path} (confidence: {confidence})')
            
            # Step 1: Create new git branch
            branch_name = f'{self.git_branch_prefix}{datetime.utcnow().strftime("%Y%m%d-%H%M%S")}'
            await self._create_git_branch(branch_name)
            
            # Step 2: Apply the fix
            await self._apply_fix_to_file(file_path, fix_code)
            
            # Step 3: Run tests
            test_result = await self._run_tests()
            
            # Step 4: Commit changes
            await self._commit_changes(branch_name, issue)
            
            # Step 5: Push branch
            await self._push_branch(branch_name)
            
            # Step 6: Notify user
            await self._notify_user_of_pr(branch_name, issue, test_result)
            
            # Update statistics
            self.stats['auto_fixes_applied'] += 1
            self.stats['pr_notifications_sent'] += 1
            
            logger.info(f'✅ Code fix applied and PR created: {branch_name}')
        
        except Exception as e:
            logger.error(f'Error applying code fix: {e}')
    
    async def _create_git_branch(self, branch_name: str):
        """
        Create a new git branch.
        """
        try:
            # Checkout to main branch first
            subprocess.run(['git', 'checkout', 'main'], cwd=self.git_repo_path, check=True)
            
            # Pull latest changes
            subprocess.run(['git', 'pull', 'origin', 'main'], cwd=self.git_repo_path, check=True)
            
            # Create and checkout new branch
            subprocess.run(['git', 'checkout', '-b', branch_name], cwd=self.git_repo_path, check=True)
            
            logger.info(f'🌿 Created git branch: {branch_name}')
        
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to create git branch: {e}')
            raise
    
    async def _apply_fix_to_file(self, file_path: str, fix_code: str):
        """
        Apply the fix to the specified file.
        """
        try:
            # Resolve absolute path
            abs_path = os.path.join(self.git_repo_path, file_path)
            
            # Create backup
            backup_path = f'{abs_path}.backup_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
            if os.path.exists(abs_path):
                import shutil
                shutil.copy2(abs_path, backup_path)
                logger.info(f'📦 Backup created: {backup_path}')
            
            # Write fixed code
            with open(abs_path, 'w') as f:
                f.write(fix_code)
            
            logger.info(f'✅ Fix applied to: {abs_path}')
        
        except Exception as e:
            logger.error(f'Failed to apply fix to file: {e}')
            raise
    
    async def _run_tests(self) -> Dict[str, Any]:
        """
        Run tests to verify the fix.
        """
        try:
            # Run npm test or pytest based on project type
            if os.path.exists(os.path.join(self.git_repo_path, 'package.json')):
                # Node.js project
                result = subprocess.run(
                    ['npm', 'test'],
                    cwd=self.git_repo_path,
                    capture_output=True,
                    text=True
                )
            else:
                # Python project
                result = subprocess.run(
                    ['python', '-m', 'pytest'],
                    cwd=self.git_repo_path,
                    capture_output=True,
                    text=True
                )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
            }
        
        except Exception as e:
            logger.error(f'Error running tests: {e}')
            return {
                'success': False,
                'error': str(e),
            }
    
    async def _commit_changes(self, branch_name: str, issue: str):
        """
        Commit the changes.
        """
        try:
            # Stage changes
            subprocess.run(['git', 'add', '.'], cwd=self.git_repo_path, check=True)
            
            # Commit with message
            commit_message = f'JARVIS Auto-Fix: {issue}\n\nAuto-generated by JARVIS Observer Loop'
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.git_repo_path,
                check=True
            )
            
            logger.info(f'✅ Changes committed to {branch_name}')
        
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to commit changes: {e}')
            raise
    
    async def _push_branch(self, branch_name: str):
        """
        Push the branch to remote.
        """
        try:
            subprocess.run(
                ['git', 'push', 'origin', branch_name],
                cwd=self.git_repo_path,
                check=True
            )
            
            logger.info(f'🚀 Branch pushed: {branch_name}')
        
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to push branch: {e}')
            raise
    
    async def _notify_user_of_pr(self, branch_name: str, issue: str, test_result: Dict[str, Any]):
        """
        Notify the user about the new PR.
        """
        try:
            # Import notification service
            sys.path.append('./jarvis/channels')
            from hub import JarvisCommunicationHub
            
            hub = JarvisCommunicationHub()
            
            # Build notification message
            message = f"""
🤖 JARVIS Auto-Fix PR Created
==============================

**Branch:** {branch_name}
**Issue:** {issue}
**Tests:** {'✅ Passed' if test_result['success'] else '❌ Failed'}

**Summary:**
I've identified and fixed an issue autonomously. Please review the changes and merge if approved.

**Next Steps:**
1. Review the PR
2. Merge if approved
3. Delete the branch after merging

This was auto-generated by the JARVIS Observer Loop.
"""
            
            # Send notification via configured channel
            if self.notification_channel == 'whatsapp':
                await hub.whatsapp.sendMessage(self.notification_user_id, message)
            elif self.notification_channel == 'telegram':
                await hub.telegram.sendMessage(self.notification_user_id, message)
            
            logger.info(f'📢 User notified of PR: {branch_name}')
        
        except Exception as e:
            logger.error(f'Failed to notify user: {e}')
    
    async def _log_suggestion(self, suggestion: str):
        """
        Log a suggestion for later review.
        """
        try:
            logger.info(f'💡 Suggestion logged: {suggestion}')
            
            # Save to suggestions file
            suggestions_path = './jarvis/data/suggestions.json'
            os.makedirs(os.path.dirname(suggestions_path), exist_ok=True)
            
            suggestions = []
            if os.path.exists(suggestions_path):
                with open(suggestions_path, 'r') as f:
                    suggestions = json.load(f)
            
            suggestions.append({
                'suggestion': suggestion,
                'timestamp': datetime.utcnow().isoformat(),
            })
            
            with open(suggestions_path, 'w') as f:
                json.dump(suggestions, f, indent=2)
        
        except Exception as e:
            logger.error(f'Failed to log suggestion: {e}')

# Singleton instance
observer_loop: Optional[ObserverLoop] = None

def get_observer_loop(config: Dict[str, Any] = None) -> ObserverLoop:
    """Get or create observer loop singleton"""
    global observer_loop
    
    if observer_loop is None:
        if config is None:
            config = {}
        observer_loop = ObserverLoop(config)
    
    return observer_loop

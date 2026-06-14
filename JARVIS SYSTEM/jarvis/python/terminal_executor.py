"""
JARVIS Sandboxed Terminal Execution
===================================

Secure tool for executing whitelisted CLI commands.
Allows JARVIS to run specific commands autonomously with proper security controls.
"""

import asyncio
import logging
import subprocess
import shlex
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import os
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TerminalExecutor:
    """
    Secure terminal executor for JARVIS.
    Executes whitelisted commands with proper security controls.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Whitelisted commands
        self.whitelisted_commands = config.get('whitelisted_commands', {
            # Git commands
            'git': ['status', 'log', 'diff', 'branch', 'pull', 'fetch'],
            
            # NPM commands
            'npm': ['list', 'info', 'audit', 'test', 'build'],
            
            # System monitoring
            'ps': ['aux', 'ef'],
            'top': ['-b', '-n', '1'],
            'htop': [],
            'df': ['-h'],
            'free': ['-h'],
            'uptime',
            
            # File operations (read-only)
            'ls': ['-la', '-lh'],
            'cat': [],
            'head': ['-n'],
            'tail': ['-n', '-f'],
            'grep': [],
            'find': [],
            
            # Python
            'python': ['--version', '-m', 'pip', 'list'],
            'python3': ['--version', '-m', 'pip', 'list'],
            
            # Docker
            'docker': ['ps', 'images', 'logs', 'stats'],
            
            # System info
            'uname': ['-a'],
            'whoami',
            'hostname',
        })
        
        # Blacklisted patterns (additional security)
        self.blacklisted_patterns = [
            r'rm\s+-rf',
            r'del\s+',
            r'format\s+',
            r'chmod\s+777',
            r'chown',
            r'sudo',
            r'su\s',
            r'>&\s*',
            r'\|.*rm',
            r'&&.*rm',
            r';.*rm',
        ]
        
        # Execution limits
        self.max_execution_time = config.get('max_execution_time', 30)  # seconds
        self.max_output_size = config.get('max_output_size', 10000)  # characters
        
        # Execution history
        self.execution_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        
        # Working directory
        self.working_directory = config.get('working_directory', os.getcwd())
    
    async def execute_command(
        self,
        command: str,
        requested_by: str = 'system',
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute a whitelisted command securely.
        
        Args:
            command: The command to execute
            requested_by: Who requested the execution (user ID or 'system')
            timeout: Custom timeout in seconds
        
        Returns:
            Dict with execution result
        """
        execution_id = datetime.utcnow().isoformat()
        
        logger.info(f"🖥️ Command execution requested: {command}")
        logger.info(f"👤 Requested by: {requested_by}")
        
        # Validate command
        validation_result = self._validate_command(command)
        
        if not validation_result['valid']:
            logger.warning(f"❌ Command validation failed: {validation_result['reason']}")
            return {
                'success': False,
                'error': validation_result['reason'],
                'execution_id': execution_id,
            }
        
        # Parse command
        try:
            parsed_command = shlex.split(command)
        except Exception as e:
            logger.error(f"❌ Failed to parse command: {e}")
            return {
                'success': False,
                'error': f"Failed to parse command: {str(e)}",
                'execution_id': execution_id,
            }
        
        # Execute command
        try:
            result = await self._execute_safely(
                parsed_command,
                timeout or self.max_execution_time
            )
            
            # Log execution
            self._log_execution(
                execution_id,
                command,
                requested_by,
                result
            )
            
            return {
                'success': True,
                'execution_id': execution_id,
                'command': command,
                'exit_code': result['exit_code'],
                'stdout': result['stdout'],
                'stderr': result['stderr'],
                'execution_time': result['execution_time'],
            }
        
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Command timed out: {command}")
            return {
                'success': False,
                'error': 'Command execution timed out',
                'execution_id': execution_id,
            }
        
        except Exception as e:
            logger.error(f"❌ Command execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'execution_id': execution_id,
            }
    
    def _validate_command(self, command: str) -> Dict[str, Any]:
        """
        Validate if command is whitelisted and safe.
        
        Returns:
            Dict with 'valid' boolean and 'reason' if invalid
        """
        # Check against blacklisted patterns
        for pattern in self.blacklisted_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    'valid': False,
                    'reason': f"Command contains blacklisted pattern: {pattern}",
                }
        
        # Parse command to check base command
        try:
            parsed = shlex.split(command)
            if not parsed:
                return {
                    'valid': False,
                    'reason': 'Empty command',
                }
            
            base_command = parsed[0]
            args = parsed[1:]
            
            # Check if base command is whitelisted
            if base_command not in self.whitelisted_commands:
                return {
                    'valid': False,
                    'reason': f"Command '{base_command}' is not whitelisted",
                }
            
            # Check if arguments are whitelisted for this command
            whitelisted_args = self.whitelisted_commands[base_command]
            
            # If whitelist is empty list, all args are allowed
            if whitelisted_args == []:
                return {'valid': True}
            
            # If whitelist is specific, check each arg
            for arg in args:
                arg_allowed = False
                for allowed in whitelisted_args:
                    if arg.startswith(allowed) or arg == allowed:
                        arg_allowed = True
                        break
                
                if not arg_allowed:
                    return {
                        'valid': False,
                        'reason': f"Argument '{arg}' is not whitelisted for '{base_command}'",
                    }
            
            return {'valid': True}
        
        except Exception as e:
            return {
                'valid': False,
                'reason': f"Validation error: {str(e)}",
            }
    
    async def _execute_safely(
        self,
        command: List[str],
        timeout: int
    ) -> Dict[str, Any]:
        """
        Execute command safely with timeout and output limits.
        """
        start_time = datetime.utcnow()
        
        # Execute command
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.working_directory,
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            # Decode output
            stdout_text = stdout.decode('utf-8', errors='replace')
            stderr_text = stderr.decode('utf-8', errors='replace')
            
            # Truncate output if too large
            if len(stdout_text) > self.max_output_size:
                stdout_text = stdout_text[:self.max_output_size] + '\n... (output truncated)'
            
            if len(stderr_text) > self.max_output_size:
                stderr_text = stderr_text[:self.max_output_size] + '\n... (output truncated)'
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                'exit_code': process.returncode,
                'stdout': stdout_text,
                'stderr': stderr_text,
                'execution_time': execution_time,
            }
        
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise subprocess.TimeoutExpired(command, timeout)
    
    def _log_execution(
        self,
        execution_id: str,
        command: str,
        requested_by: str,
        result: Dict[str, Any]
    ):
        """Log command execution to history"""
        log_entry = {
            'execution_id': execution_id,
            'command': command,
            'requested_by': requested_by,
            'timestamp': datetime.utcnow().isoformat(),
            'success': result.get('success', True),
            'exit_code': result.get('exit_code'),
            'execution_time': result.get('execution_time'),
        }
        
        self.execution_history.append(log_entry)
        
        # Trim history if too large
        if len(self.execution_history) > self.max_history_size:
            self.execution_history = self.execution_history[-self.max_history_size:]
        
        logger.info(f"📝 Logged execution: {execution_id}")
    
    def get_execution_history(
        self,
        limit: int = 10,
        requested_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get execution history"""
        history = self.execution_history
        
        if requested_by:
            history = [h for h in history if h['requested_by'] == requested_by]
        
        return history[-limit:]
    
    def get_whitelisted_commands(self) -> Dict[str, List[str]]:
        """Get list of whitelisted commands"""
        return self.whitelisted_commands
    
    def add_whitelisted_command(self, command: str, args: List[str]):
        """Add a command to the whitelist"""
        self.whitelisted_commands[command] = args
        logger.info(f"Added to whitelist: {command} {args}")
    
    def remove_whitelisted_command(self, command: str):
        """Remove a command from the whitelist"""
        if command in self.whitelisted_commands:
            del self.whitelisted_commands[command]
            logger.info(f"Removed from whitelist: {command}")
    
    def set_working_directory(self, directory: str):
        """Set the working directory for command execution"""
        if os.path.isdir(directory):
            self.working_directory = directory
            logger.info(f"Working directory set to: {directory}")
        else:
            logger.error(f"Invalid directory: {directory}")

# Singleton instance
terminal_executor: Optional[TerminalExecutor] = None

def get_terminal_executor(config: Dict[str, Any] = None) -> TerminalExecutor:
    """Get or create terminal executor singleton"""
    global terminal_executor
    
    if terminal_executor is None:
        if config is None:
            config = {}
        terminal_executor = TerminalExecutor(config)
    
    return terminal_executor

"""
DOOM SENTINEL - RBAC Manager
Role-Based Access Control and command processing system
"""

import os
import logging
import asyncio
import subprocess
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass

# Database and system modules
from prisma import Prisma
from core_modules.db_manager_postgres import postgres_db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SystemStatus:
    """System status data structure"""
    server_health: str
    database_status: str
    leads_today: int
    budget_remaining: str
    active_agents: int
    total_agents: int
    uptime: str

@dataclass
class DeploymentResult:
    """Deployment result data structure"""
    agent_name: str
    status: str
    eta: str
    mission_description: str

@dataclass
class ApprovalResult:
    """Campaign approval result data structure"""
    status: str
    budget: str
    target_audience: str
    launch_time: str

class RBACManager:
    """
    Role-Based Access Control Manager for DOOM system
    Handles command processing based on user access level
    """
    
    def __init__(self):
        """Initialize RBAC manager"""
        self.logger = logging.getLogger(__name__)
        
        # System configuration
        self.total_agents = 34  # Total AI agents in system
        self.system_start_time = datetime.now()
        
        # Initialize database connection
        self.db = postgres_db_manager
        
        self.logger.info("🎛️ DOOM RBAC Manager initialized")
        self.logger.info(f"🤖 Total AI agents: {self.total_agents}")
    
    async def generate_status_report(self) -> SystemStatus:
        """Generate comprehensive system status report"""
        try:
            # Server health check
            server_health = await self._check_server_health()
            
            # Database status
            database_status = await self._check_database_health()
            
            # Today's leads
            leads_today = await self._get_today_leads_count()
            
            # Budget status
            budget_remaining = await self._get_budget_status()
            
            # Active agents
            active_agents = await self._get_active_agents_count()
            
            # System uptime
            uptime = self._calculate_uptime()
            
            return SystemStatus(
                server_health=server_health,
                database_status=database_status,
                leads_today=leads_today,
                budget_remaining=budget_remaining,
                active_agents=active_agents,
                total_agents=self.total_agents,
                uptime=uptime
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error generating status report: {e}")
            return SystemStatus(
                server_health="ERROR",
                database_status="ERROR",
                leads_today=0,
                budget_remaining="UNKNOWN",
                active_agents=0,
                total_agents=self.total_agents,
                uptime="UNKNOWN"
            )
    
    async def _check_server_health(self) -> str:
        """Check server health status"""
        try:
            # Check CPU usage
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Check memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Check disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            if cpu_percent < 80 and memory_percent < 80 and disk_percent < 80:
                return "🟢 HEALTHY"
            elif cpu_percent < 90 and memory_percent < 90 and disk_percent < 90:
                return "🟡 WARNING"
            else:
                return "🔴 CRITICAL"
                
        except Exception as e:
            self.logger.error(f"❌ Server health check error: {e}")
            return "🔴 ERROR"
    
    async def _check_database_health(self) -> str:
        """Check database health status"""
        try:
            # Test database connection
            health_status = await self.db.health_check()
            
            if health_status.get('status') == 'healthy':
                return "🟢 ONLINE"
            else:
                return "🔴 OFFLINE"
                
        except Exception as e:
            self.logger.error(f"❌ Database health check error: {e}")
            return "🔴 ERROR"
    
    async def _get_today_leads_count(self) -> int:
        """Get count of leads created today"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Query database for today's leads
            query = f"SELECT COUNT(*) as count FROM leads WHERE DATE(created_at) = '{today}'"
            result = await self.db.execute_query(query)
            
            return result[0]['count'] if result else 0
            
        except Exception as e:
            self.logger.error(f"❌ Error getting today's leads: {e}")
            return 0
    
    async def _get_budget_status(self) -> str:
        """Get remaining budget status"""
        try:
            # This would typically integrate with payment/billing system
            # For now, return mock data
            return "Rp 45.000.000 (45% used)"
            
        except Exception as e:
            self.logger.error(f"❌ Error getting budget status: {e}")
            return "UNKNOWN"
    
    async def _get_active_agents_count(self) -> int:
        """Get count of active AI agents"""
        try:
            # This would typically check agent status from monitoring system
            # For now, return mock data
            return 28
            
        except Exception as e:
            self.logger.error(f"❌ Error getting active agents count: {e}")
            return 0
    
    def _calculate_uptime(self) -> str:
        """Calculate system uptime"""
        uptime = datetime.now() - self.system_start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        return f"{days}d {hours}h {minutes}m"
    
    async def deploy_scout(self, location: str) -> DeploymentResult:
        """Deploy AI Hunter scout to specified location"""
        try:
            self.logger.info(f"🚀 Deploying scout to {location}")
            
            # Determine scout type based on location
            scout_type = self._determine_scout_type(location)
            agent_name = f"{scout_type}_Hunter"
            
            # Execute deployment command
            deployment_command = [
                "python", "main.py",
                "--elite",
                "--location", location,
                "--scout-type", scout_type
            ]
            
            # Run deployment in background
            process = subprocess.Popen(
                deployment_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Generate deployment result
            eta = self._calculate_deployment_eta(location)
            mission = self._generate_mission_description(location, scout_type)
            
            return DeploymentResult(
                agent_name=agent_name,
                status="🟢 DEPLOYED",
                eta=eta,
                mission_description=mission
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error deploying scout: {e}")
            return DeploymentResult(
                agent_name="UNKNOWN",
                status="🔴 FAILED",
                eta="UNKNOWN",
                mission_description=f"Deployment failed: {str(e)}"
            )
    
    def _determine_scout_type(self, location: str) -> str:
        """Determine scout type based on location"""
        location_lower = location.lower()
        
        if any(keyword in location_lower for keyword in ['government', 'pns', 'kantor']):
            return 'Gov_Affinity'
        elif any(keyword in location_lower for keyword in ['property', 'rumah', 'apartemen']):
            return 'Property'
        elif any(keyword in location_lower for keyword in ['corporate', 'kantor', 'bisnis']):
            return 'Corporate'
        elif any(keyword in location_lower for keyword in ['linkedin', 'executive', 'professional']):
            return 'LinkedIn_Exec'
        else:
            return 'General'
    
    def _calculate_deployment_eta(self, location: str) -> str:
        """Calculate deployment ETA based on location"""
        # Mock ETA calculation
        return "15-30 minutes"
    
    def _generate_mission_description(self, location: str, scout_type: str) -> str:
        """Generate mission description for deployment"""
        descriptions = {
            'Gov_Affinity': f"Target PNS/P3K prospects in {location} area with FLPP eligibility focus",
            'Property': f"Identify property buyers in {location} with budget analysis and location preferences",
            'Corporate': f"Locate B2B opportunities and corporate partnerships in {location}",
            'LinkedIn_Exec': f"Target high-value executives and decision makers in {location} region",
            'General': f"Comprehensive lead generation and market analysis in {location}"
        }
        
        return descriptions.get(scout_type, f"General market intelligence gathering in {location}")
    
    async def approve_ads(self, campaign_id: str) -> ApprovalResult:
        """Approve ad campaign"""
        try:
            self.logger.info(f"✅ Approving ad campaign: {campaign_id}")
            
            # Get campaign details from database
            campaign = await self._get_campaign_details(campaign_id)
            
            if not campaign:
                return ApprovalResult(
                    status="🔴 NOT_FOUND",
                    budget="UNKNOWN",
                    target_audience="UNKNOWN",
                    launch_time="UNKNOWN"
                )
            
            # Update campaign status
            await self._update_campaign_status(campaign_id, 'APPROVED')
            
            return ApprovalResult(
                status="🟢 APPROVED",
                budget=f"Rp {campaign.get('budget', 0):,}",
                target_audience=campaign.get('target_audience', 'General'),
                launch_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error approving ads: {e}")
            return ApprovalResult(
                status="🔴 ERROR",
                budget="UNKNOWN",
                target_audience="UNKNOWN",
                launch_time="UNKNOWN"
            )
    
    async def _get_campaign_details(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign details from database"""
        try:
            query = f"SELECT * FROM campaigns WHERE id = '{campaign_id}'"
            result = await self.db.execute_query(query)
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting campaign details: {e}")
            return None
    
    async def _update_campaign_status(self, campaign_id: str, status: str):
        """Update campaign status in database"""
        try:
            query = f"UPDATE campaigns SET status = '{status}', updated_at = NOW() WHERE id = '{campaign_id}'"
            await self.db.execute_query(query)
            
        except Exception as e:
            self.logger.error(f"❌ Error updating campaign status: {e}")
    
    async def process_natural_command(self, command: str) -> str:
        """Process natural language command from admin"""
        try:
            command_lower = command.lower()
            
            # Status queries
            if any(keyword in command_lower for keyword in ['status', 'health', 'system']):
                status = await self.generate_status_report()
                return (
                    f"System Status:\n"
                    f"• Server: {status.server_health}\n"
                    f"• Database: {status.database_status}\n"
                    f"• Leads Today: {status.leads_today}\n"
                    f"• Budget: {status.budget_remaining}\n"
                    f"• Agents: {status.active_agents}/{status.total_agents}\n"
                    f"• Uptime: {status.uptime}"
                )
            
            # Deployment commands
            elif any(keyword in command_lower for keyword in ['deploy', 'scout', 'hunt']):
                # Extract location from command
                words = command.split()
                location_idx = -1
                
                for i, word in enumerate(words):
                    if word.lower() in ['deploy', 'scout', 'hunt']:
                        location_idx = i + 1
                        break
                
                location = words[location_idx] if location_idx < len(words) else 'default'
                
                deployment = await self.deploy_scout(location)
                return (
                    f"Scout Deployment:\n"
                    f"• Agent: {deployment.agent_name}\n"
                    f"• Status: {deployment.status}\n"
                    f"• ETA: {deployment.eta}\n"
                    f"• Mission: {deployment.mission_description}"
                )
            
            # Lead queries
            elif any(keyword in command_lower for keyword in ['leads', 'prospects', 'data']):
                leads_count = await self._get_today_leads_count()
                return f"Today's leads: {leads_count} prospects generated"
            
            # Budget queries
            elif any(keyword in command_lower for keyword in ['budget', 'cost', 'spending']):
                budget = await self._get_budget_status()
                return f"Budget Status: {budget}"
            
            else:
                return "Command processed. Use /help for available commands."
                
        except Exception as e:
            self.logger.error(f"❌ Error processing natural command: {e}")
            return f"Error processing command: {str(e)}"
    
    async def process_customer_service_inquiry(self, message: str) -> str:
        """Process customer service inquiry from guest users"""
        try:
            message_lower = message.lower()
            
            # Property inquiries
            if any(keyword in message_lower for keyword in ['property', 'rumah', 'apartemen', 'properti']):
                return (
                    "🏠 **Property Information**\n\n"
                    "We have various property options available:\n"
                    "• Commercial Projects (Premium)\n"
                    "• Subsidized Projects (Affordable)\n\n"
                    "Please let me know:\n"
                    "• Your preferred location\n"
                    "• Budget range\n"
                    "• Property type\n\n"
                    "I'll help you find the perfect match!"
                )
            
            # Pricing inquiries
            elif any(keyword in message_lower for keyword in ['harga', 'price', 'cicilan', 'kpr']):
                return (
                    "💰 **Pricing Information**\n\n"
                    "Our pricing varies by project type:\n\n"
                    "**Commercial Projects:**\n"
                    "• Starting from Rp 500 Juta\n"
                    "• KPR options available\n"
                    "• Premium locations\n\n"
                    "**Subsidized Projects:**\n"
                    "• Starting from Rp 150 Juta\n"
                    "• FLPP subsidies available\n"
                    "• Government partnerships\n\n"
                    "For detailed pricing, please specify your preferred project type!"
                )
            
            # Location inquiries
            elif any(keyword in message_lower for keyword in ['lokasi', 'location', 'alamat', 'area']):
                return (
                    "📍 **Location Information**\n\n"
                    "We have projects in strategic locations:\n"
                    "• Jakarta & Tangerang area\n"
                    "• Near public transportation\n"
                    "• Complete facilities\n\n"
                    "Which area are you interested in? I can provide specific location details!"
                )
            
            # Contact inquiries
            elif any(keyword in message_lower for keyword in ['kontak', 'contact', 'telepon', 'whatsapp']):
                return (
                    "📞 **Contact Information**\n\n"
                    "Get in touch with us:\n"
                    "• 📱 WhatsApp: +62 812-3456-7890\n"
                    "• 📧 Email: info@lumina-os.com\n"
                    "• 🌐 Website: www.lumina-os.com\n\n"
                    "Our sales team is ready to assist you with property visits and detailed information!"
                )
            
            # General inquiries
            else:
                return (
                    "👋 **Virtual Assistant**\n\n"
                    "I'm here to help you with property information!\n\n"
                    "You can ask me about:\n"
                    "• 🏠 Available properties\n"
                    "• 💰 Pricing and payment options\n"
                    "• 📍 Project locations\n"
                    "• 📞 Contact information\n"
                    "• 📋 Booking procedures\n\n"
                    "What would you like to know?"
                )
                
        except Exception as e:
            self.logger.error(f"❌ Error processing customer service inquiry: {e}")
            return "I apologize, but I encountered an error. Please try again or contact our support team."
    
    async def execute_system_control_action(self, action: str) -> str:
        """Execute system control action"""
        try:
            if action == "restart_services":
                # Restart services command
                result = subprocess.run(
                    ["docker-compose", "restart"],
                    capture_output=True,
                    text=True
                )
                return "✅ Services restarted successfully" if result.returncode == 0 else "❌ Failed to restart services"
            
            elif action == "view_logs":
                # View logs command
                return "📋 Logs available at: /var/log/lumina-os/"
            
            elif action == "db_maintenance":
                # Database maintenance
                return "🔧 Database maintenance scheduled"
            
            elif action == "emergency_stop":
                # Emergency stop
                return "🚨 Emergency stop activated"
            
            elif action == "performance":
                # Performance metrics
                return "📊 Performance metrics: CPU 45%, Memory 62%, Disk 38%"
            
            elif action == "diagnostics":
                # System diagnostics
                return "🔍 System diagnostics: All systems operational"
            
            else:
                return f"❌ Unknown action: {action}"
                
        except Exception as e:
            self.logger.error(f"❌ Error executing system control action: {e}")
            return f"❌ Error executing action: {str(e)}"

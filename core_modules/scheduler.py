"""
Automated Scheduler Module for HUNTER_AGENT_AI_MARKETING_DIGITAL
Handles background automation with intelligent scheduling and error recovery
"""

import schedule
import time
import logging
import threading
import signal
import sys
from datetime import datetime, timedelta
from typing import Optional
import traceback
import json

# Import our modules
try:
    from .intelligence_aggregator_working import run_daily_scan_deep_crawl
except ImportError:
    # Fallback for direct execution
    from intelligence_aggregator_working import run_daily_scan_deep_crawl

try:
    from ..agents.scout_agent.lead_hunter import lead_hunter_run
except ImportError:
    # Fallback for direct execution
    try:
        from agents.scout_agent.lead_hunter import lead_hunter_run
    except ImportError:
        # Mock function for testing
        def lead_hunter_run():
            return {"leads_found": 0, "high_intent_leads": 0, "status": "mock"}

# Import revival protocol
try:
    from ..scripts.cron_revival_protocol import RevivalProtocol
    REVIVAL_AVAILABLE = True
except ImportError:
    try:
        from scripts.cron_revival_protocol import RevivalProtocol
        REVIVAL_AVAILABLE = True
    except ImportError:
        REVIVAL_AVAILABLE = False
        print("Warning: Revival Protocol not available, revival jobs disabled")

# Telegram alert for heartbeat
try:
    from core_modules.notifications.alert_manager import send_telegram_message
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("Warning: Telegram not available, heartbeat notifications disabled")

class AutomatedScheduler:
    """
    Advanced scheduler with error recovery and heartbeat monitoring
    """
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.running = False
        self.last_scrape_time = None
        self.last_lead_hunt_time = None
        self.last_revival_time = None
        self.heartbeat_interval = 24 * 60 * 60  # 24 hours in seconds
        self.scheduler_thread = None
        self.heartbeat_thread = None
        self.revival_protocol = None
        
        # Initialize revival protocol if available
        if REVIVAL_AVAILABLE:
            try:
                self.revival_protocol = RevivalProtocol()
                self.logger.info("🔄 Revival Protocol initialized")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize Revival Protocol: {e}")
                self.revival_protocol = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("Automated Scheduler initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging system"""
        logger = logging.getLogger('AutomatedScheduler')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if not exists
        import os
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # File handler for system logs
        file_handler = logging.FileHandler(
            os.path.join(logs_dir, 'system.log'),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def _run_daily_intelligence_scan(self):
        """Run daily intelligence scan with error recovery"""
        try:
            self.logger.info("🚀 Starting Daily Intelligence Scan...")
            start_time = time.time()
            
            # Run the deep crawl scan
            result = run_daily_scan_deep_crawl()
            
            # Update last scrape time
            self.last_scrape_time = datetime.now()
            
            # Log results
            duration = time.time() - start_time
            self.logger.info(f"✅ Daily scan completed in {duration:.2f} seconds")
            self.logger.info(f"📊 Results: {result.get('successful_sources', 0)} successful, "
                           f"{result.get('failed_sources', 0)} failed, "
                           f"{result.get('skipped_sources', 0)} skipped, "
                           f"{result.get('total_articles', 0)} articles")
            
            # Check for critical alerts
            if result.get('scan_results'):
                religious_alerts = []
                for scan_result in result.get('scan_results', []):
                    if scan_result.get('religious_alerts'):
                        religious_alerts.extend(scan_result['religious_alerts'])
                
                if religious_alerts:
                    self.logger.warning(f"🚨 {len(religious_alerts)} RELIGIOUS AFFAIRS ALERTS DETECTED")
                    for alert in religious_alerts[:3]:  # Log first 3 alerts
                        self.logger.warning(f"Alert: {alert.get('title', 'Unknown')} - {alert.get('keyword', 'Unknown')}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Daily intelligence scan failed: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Schedule retry in 1 hour
            self.logger.info("🔄 Scheduling retry in 1 hour...")
            schedule.every(1).hours.do(self._run_daily_intelligence_scan)
            
            return False
    
    def _run_lead_hunting(self):
        """Run lead hunting with error recovery"""
        try:
            self.logger.info("🎯 Starting Lead Hunting...")
            start_time = time.time()
            
            # Run lead hunting
            result = lead_hunter_run()
            
            # Update last lead hunt time
            self.last_lead_hunt_time = datetime.now()
            
            # Log results
            duration = time.time() - start_time
            self.logger.info(f"✅ Lead hunting completed in {duration:.2f} seconds")
            
            if result and isinstance(result, dict):
                self.logger.info(f"📊 Leads found: {result.get('leads_found', 0)}, "
                               f"High intent: {result.get('high_intent_leads', 0)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lead hunting failed: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Schedule retry in 1 hour
            self.logger.info("🔄 Scheduling retry in 1 hour...")
            schedule.every(1).hours.do(self._run_lead_hunting)
            
            return False
    
    def _run_revival_protocol(self):
        """Run revival protocol with error recovery"""
        if not self.revival_protocol:
            self.logger.warning("⚠️ Revival Protocol not available, skipping revival job")
            return False
        
        try:
            self.logger.info("🔄 Starting Revival Protocol...")
            start_time = time.time()
            
            # Run revival protocol
            result = self.revival_protocol.scan_and_revive_dead_leads()
            
            # Update last revival time
            self.last_revival_time = datetime.now()
            
            # Log results
            duration = time.time() - start_time
            self.logger.info(f"✅ Revival Protocol completed in {duration:.2f} seconds")
            
            if result and isinstance(result, dict):
                self.logger.info(f"📊 Dead leads found: {result.get('dead_leads_found', 0)}, "
                               f"Revival attempts: {result.get('revival_attempts', 0)}, "
                               f"Successful revivals: {result.get('successful_revivals', 0)}")
                
                # Send Telegram alert for successful revivals
                if result.get('successful_revivals', 0) > 0 and TELEGRAM_AVAILABLE:
                    try:
                        message = f"""🔄 REVIVAL PROTOCOL SUCCESS
                        
✅ Successfully revived {result.get('successful_revivals', 0)} dead leads
📊 Total attempts: {result.get('revival_attempts', 0)}
🎯 Dead leads found: {result.get('dead_leads_found', 0)}

Revival Protocol completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Check logs/revival_protocol.log for detailed results."""
                        
                        send_telegram_message(message)
                        self.logger.info("📱 Revival success alert sent to Telegram")
                        
                    except Exception as e:
                        self.logger.error(f"Failed to send revival alert: {e}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Revival Protocol failed: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Schedule retry in 1 hour
            self.logger.info("🔄 Scheduling revival retry in 1 hour...")
            schedule.every(1).hours.do(self._run_revival_protocol)
            
            return False
    
    def _heartbeat_check(self):
        """Check system heartbeat and send alerts if needed"""
        try:
            now = datetime.now()
            
            # Check if we haven't scraped in 24 hours
            if self.last_scrape_time:
                time_since_scrape = now - self.last_scrape_time
                if time_since_scrape.total_seconds() > self.heartbeat_interval:
                    self.logger.warning("⚠️ HEARTBEAT ALERT: No successful scrape in 24 hours")
                    
                    # Send Telegram alert if available
                    if TELEGRAM_AVAILABLE:
                        try:
                            message = f"""🚨 SYSTEM HEARTBEAT ALERT
                        
⚠️ Sistem mengalami hambatan, mohon cek log

Last successful scrape: {self.last_scrape_time.strftime('%Y-%m-%d %H:%M:%S')}
Time since last scrape: {time_since_scrape_time.total_seconds() / 3600:.1f} hours

Please check logs/system.log for details."""
                            
                            send_telegram_message(message)
                            self.logger.info("📱 Heartbeat alert sent to Telegram")
                            
                        except Exception as e:
                            self.logger.error(f"Failed to send heartbeat alert: {e}")
                    else:
                        self.logger.warning("Telegram not available, heartbeat alert not sent")
            
            # Log heartbeat status
            status_parts = []
            if self.last_scrape_time:
                status_parts.append(f"Last scan: {self.last_scrape_time.strftime('%H:%M')}")
            if self.last_lead_hunt_time:
                status_parts.append(f"Last hunt: {self.last_lead_hunt_time.strftime('%H:%M')}")
            if self.last_revival_time:
                status_parts.append(f"Last revival: {self.last_revival_time.strftime('%H:%M')}")
            
            self.logger.info(f"💓 Heartbeat check - {' | '.join(status_parts) if status_parts else 'No activities yet'}")
            
        except Exception as e:
            self.logger.error(f"Heartbeat check failed: {e}")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        self.logger.info("📅 Scheduler loop started")
        
        while self.running:
            try:
                # Run pending scheduled jobs
                schedule.run_pending()
                
                # Sleep for 1 minute before next check
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Scheduler loop error: {e}")
                time.sleep(60)  # Wait before retry
    
    def _heartbeat_loop(self):
        """Heartbeat monitoring loop"""
        self.logger.info("💓 Heartbeat monitoring started")
        
        while self.running:
            try:
                # Check heartbeat every hour
                self._heartbeat_check()
                
                # Sleep for 1 hour
                time.sleep(3600)
                
            except Exception as e:
                self.logger.error(f"Heartbeat loop error: {e}")
                time.sleep(3600)  # Wait before retry
    
    def setup_schedule(self):
        """Setup the automated schedule"""
        self.logger.info("📅 Setting up automated schedule...")
        
        # Daily intelligence scan at 06:00 WIB (UTC+7 = UTC-1)
        # Note: schedule uses local time, so we adjust for WIB
        schedule.every().day.at("06:00").do(self._run_daily_intelligence_scan)
        self.logger.info("📅 Daily intelligence scan scheduled for 06:00 WIB")
        
        # Lead hunting every 4 hours
        schedule.every(4).hours.do(self._run_lead_hunting)
        self.logger.info("📅 Lead hunting scheduled every 4 hours")
        
        # Revival protocol daily at 10:00 WIB
        schedule.every().day.at("10:00").do(self._run_revival_protocol)
        self.logger.info("📅 Revival Protocol scheduled for 10:00 WIB")
        
        # Heartbeat check every hour (handled in separate loop)
        self.logger.info("💓 Heartbeat monitoring active")
        
        self.logger.info("✅ Schedule setup completed")
    
    def start(self):
        """Start the automated scheduler"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.logger.info("🚀 Starting Automated Scheduler...")
        self.running = True
        
        # Setup the schedule
        self.setup_schedule()
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            name="SchedulerThread",
            daemon=True
        )
        self.scheduler_thread.start()
        
        # Start heartbeat thread
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            name="HeartbeatThread", 
            daemon=True
        )
        self.heartbeat_thread.start()
        
        self.logger.info("✅ Automated Scheduler started successfully")
        self.logger.info("📅 Next jobs will run according to schedule")
        self.logger.info("💓 Heartbeat monitoring active")
        self.logger.info("🔄 Press Ctrl+C to stop gracefully")
    
    def stop(self):
        """Stop the automated scheduler"""
        if not self.running:
            return
        
        self.logger.info("🛑 Stopping Automated Scheduler...")
        self.running = False
        
        # Wait for threads to finish (with timeout)
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=5)
        
        self.logger.info("✅ Automated Scheduler stopped")
    
    def get_status(self) -> dict:
        """Get current scheduler status"""
        now = datetime.now()
        
        status = {
            'running': self.running,
            'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
            'last_scrape_time': self.last_scrape_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_scrape_time else None,
            'last_lead_hunt_time': self.last_lead_hunt_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_lead_hunt_time else None,
            'last_revival_time': self.last_revival_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_revival_time else None,
            'revival_protocol_available': REVIVAL_AVAILABLE,
            'next_jobs': []
        }
        
        # Get next scheduled jobs
        for job in schedule.jobs:
            status['next_jobs'].append({
                'job': str(job.job_func),
                'next_run': job.next_run.strftime('%Y-%m-%d %H:%M:%S') if job.next_run else None,
                'interval': str(job.interval)
            })
        
        return status

# Global scheduler instance
scheduler = AutomatedScheduler()

def start_scheduler():
    """Start the automated scheduler"""
    scheduler.start()

def stop_scheduler():
    """Stop the automated scheduler"""
    scheduler.stop()

def get_scheduler_status():
    """Get scheduler status"""
    return scheduler.get_status()

if __name__ == "__main__":
    # Run scheduler directly
    print("🚀 Starting HUNTER_AGENT_AI_MARKETING_DIGITAL Automated Scheduler")
    print("📅 Schedule: Daily scan at 06:00 WIB, Lead hunting every 4 hours")
    print("� Revival Protocol: Daily at 10:00 WIB")
    print("�💓 Heartbeat monitoring: Active")
    print("🔄 Press Ctrl+C to stop gracefully")
    print("=" * 60)
    
    try:
        start_scheduler()
        
        # Keep main thread alive
        while scheduler.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown signal received")
        stop_scheduler()
        print("✅ Scheduler stopped gracefully")
